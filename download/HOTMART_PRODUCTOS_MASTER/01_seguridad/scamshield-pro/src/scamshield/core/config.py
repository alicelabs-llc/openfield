"""ScamShield Pro — Core configuration."""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from env / .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # --- Server ---
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")
    debug: bool = Field(default=False, alias="DEBUG")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    # --- Security ---
    api_key: str = Field(default="", alias="API_KEY")

    # --- External integrations (all optional) ---
    gsb_api_key: str = Field(default="", alias="GSB_API_KEY")
    vt_api_key: str = Field(default="", alias="VT_API_KEY")
    ipqs_api_key: str = Field(default="", alias="IPQS_API_KEY")

    # --- Cache ---
    cache_dir: str = Field(default="~/.scamshield/cache", alias="CACHE_DIR")
    cache_ttl_seconds: int = Field(default=86400, alias="CACHE_TTL_SECONDS")

    # --- Rate limiting ---
    rate_limit_per_minute: int = Field(default=60, alias="RATE_LIMIT_PER_MINUTE")

    # --- Timeouts ---
    http_timeout_seconds: float = Field(default=10.0, alias="HTTP_TIMEOUT_SECONDS")
    dns_timeout_seconds: float = Field(default=5.0, alias="DNS_TIMEOUT_SECONDS")

    @property
    def cache_path(self) -> Path:
        p = Path(os.path.expanduser(self.cache_dir))
        p.mkdir(parents=True, exist_ok=True)
        return p


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()


def reset_settings_cache() -> None:
    """Clear settings cache (used by tests)."""
    get_settings.cache_clear()
