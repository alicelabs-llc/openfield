"""ScamShield Pro — Async HTTP client."""
from __future__ import annotations

from typing import Any

import httpx

from scamshield.core.config import get_settings


def get_http_client(**kwargs: Any) -> httpx.AsyncClient:
    """Return a configured async HTTP client."""
    s = get_settings()
    defaults = {
        "timeout": httpx.Timeout(s.http_timeout_seconds, connect=5.0),
        "follow_redirects": True,
        "http2": True,
        "headers": {
            "User-Agent": (
                "Mozilla/5.0 (compatible; ScamShieldPro/1.0; "
                "+https://github.com/eddyflores100-lang/scamshield-pro)"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        },
        "verify": True,
    }
    defaults.update(kwargs)
    return httpx.AsyncClient(**defaults)
