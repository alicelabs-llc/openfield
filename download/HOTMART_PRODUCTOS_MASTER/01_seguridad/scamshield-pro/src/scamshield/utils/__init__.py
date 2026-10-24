"""ScamShield Pro — Utils package."""
from scamshield.utils.cache import Cache  # noqa: F401
from scamshield.utils.http_client import get_http_client  # noqa: F401
from scamshield.utils.url_parser import (  # noqa: F401
    has_punycode,
    is_ip_url,
    is_shortener,
    is_suspicious_tld,
    normalize_url,
    parse_domain,
)

__all__ = [
    "Cache",
    "get_http_client",
    "normalize_url",
    "parse_domain",
    "is_ip_url",
    "is_shortener",
    "is_suspicious_tld",
    "has_punycode",
]
