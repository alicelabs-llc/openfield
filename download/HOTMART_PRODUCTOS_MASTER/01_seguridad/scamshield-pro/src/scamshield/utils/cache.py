"""ScamShield Pro — Disk cache wrapper."""
from __future__ import annotations

from typing import Any, Callable

import diskcache

from scamshield.core.config import get_settings


class Cache:
    """Thin wrapper around diskcache.Cache with TTL."""

    _instance: "Cache | None" = None

    def __init__(self) -> None:
        s = get_settings()
        self._cache = diskcache.Cache(str(s.cache_path))
        self._ttl = s.cache_ttl_seconds

    @classmethod
    def get(cls) -> "Cache":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_or_set(self, key: str, factory: Callable[[], Any], ttl: int | None = None) -> Any:
        if (val := self._cache.get(key)) is not None:
            return val
        val = factory()
        self._cache.set(key, val, expire=ttl or self._ttl)
        return val

    def get(self, key: str) -> Any | None:
        return self._cache.get(key)

    def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        self._cache.set(key, value, expire=ttl or self._ttl)

    def clear(self) -> None:
        self._cache.clear()

    def close(self) -> None:
        self._cache.close()
