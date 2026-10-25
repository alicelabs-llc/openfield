"""ScamShield Pro — URL utilities."""
from __future__ import annotations

import ipaddress
import re
from urllib.parse import urlsplit, urlunsplit

import tldextract

# Common URL shorteners (expand these via RedirectChainCheck)
URL_SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd",
    "buff.ly", "rebrand.ly", "cutt.ly", "shorturl.at", "rb.gy",
    "shorte.st", "soo.gd", "s.id", "lnkd.in", "tiny.cc",
}

# Suspicious TLDs (statistically over-represented in abuse datasets)
SUSPICIOUS_TLDS = {
    ".xyz", ".top", ".gq", ".cf", ".ml", ".tk", ".click", ".country",
    ".stream", ".download", ".loan", ".work", ".men", ".racing",
    ".online", ".site", ".icu", ".buzz", ".fit", ".review",
    ".party", ".trade", ".science", ".kim", ".bid", ".date",
}

# IDN homograph attack patterns (mixed scripts)
HIGH_RISK_PUNYCODE = re.compile(r"^xn--", re.IGNORECASE)


def normalize_url(url: str) -> str:
    """Normalize a URL — add scheme if missing, strip fragments, lowercase host."""
    if not url or not isinstance(url, str):
        raise ValueError("URL must be a non-empty string")

    url = url.strip()
    if not url:
        raise ValueError("URL must be a non-empty string")

    # Detect scheme case-insensitively before normalization
    lower_prefix = url.lower()
    if lower_prefix.startswith(("http://", "https://")):
        # Strip the original-cased scheme and re-add lowercased
        for sch in ("http://", "https://"):
            if lower_prefix.startswith(sch):
                url = sch + url[len(sch):]
                break
    elif "://" not in url:
        # If user typed "example.com", prepend https
        url = "https://" + url
    else:
        raise ValueError(f"Unsupported URL scheme: {url.split('://')[0]}")

    parts = urlsplit(url)

    # Lowercase the host
    host = parts.netloc.lower()
    if "@" in host:
        # strip userinfo
        host = host.split("@", 1)[1]

    # Strip trailing dot from host
    host = host.rstrip(".")

    # Lowercase scheme
    scheme = parts.scheme.lower()

    # Strip fragment
    fragment = ""

    # Remove default ports
    if (scheme == "https" and host.endswith(":443")) or (
        scheme == "http" and host.endswith(":80")
    ):
        host = host.rsplit(":", 1)[0]

    normalized = urlunsplit((scheme, host, parts.path, parts.query, fragment))
    return normalized


def parse_domain(url: str) -> tuple[str, str, str]:
    """Extract (registered_domain, tld, subdomain) from a URL."""
    parts = urlsplit(url)
    host = parts.netloc.lower().split(":")[0]
    if not host:
        raise ValueError(f"No host in URL: {url}")

    # If host is an IP, return as-is
    try:
        ipaddress.ip_address(host)
        return host, "", ""
    except ValueError:
        pass

    extracted = tldextract.extract(host)
    registered = f"{extracted.domain}.{extracted.suffix}" if extracted.suffix else extracted.domain
    return registered, "." + extracted.suffix if extracted.suffix else "", extracted.subdomain


def is_ip_url(url: str) -> bool:
    parts = urlsplit(url)
    host = parts.netloc.split(":")[0]
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def is_shortener(domain: str) -> bool:
    return domain.lower() in URL_SHORTENERS


def is_suspicious_tld(tld: str) -> bool:
    return tld.lower() in SUSPICIOUS_TLDS


def has_punycode(domain: str) -> bool:
    return bool(HIGH_RISK_PUNYCODE.match(domain))
