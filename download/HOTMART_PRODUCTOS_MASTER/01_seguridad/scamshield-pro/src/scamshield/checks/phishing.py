"""ScamShield Pro — Phishing pattern detection."""
from __future__ import annotations

import re

from scamshield.checks.base import BaseCheck, CheckContext
from scamshield.utils.url_parser import has_punycode

# Brands most-frequently impersonated (PhishTank top, OpenPhish)
COMMON_BRANDS = [
    "paypal", "apple", "microsoft", "google", "amazon", "netflix",
    "instagram", "facebook", "whatsapp", "coinbase", "binance",
    "bankofamerica", "wellsfargo", "chase", "citibank", "santander",
    "banco", "bbva", "davivienda", "mercantil", "provincial",
    "steam", "fortnite", "roblox", "spotify", "tiktok",
    "linkedin", "twitter", "github", "dropbox", "adobe",
]

# Typosquatting patterns — common substitutions
COMMON_TYPO_PATTERNS = [
    (r"paypa[l1]", "paypal"),
    (r"[a@]pple", "apple"),
    (r"micros[o0]ft", "microsoft"),
    (r"[a@]maz[o0]n", "amazon"),
    (r"netfl[il1]x", "netflix"),
    (r"faceb[o0]{1,2}k", "facebook"),
]

# Login paths commonly used by phishing kits
SUSPICIOUS_PATHS = re.compile(
    r"/(login|signin|verify|update|secure|account|wallet|unlock|confirm)[/?]",
    re.IGNORECASE,
)


class PhishingPatternCheck(BaseCheck):
    """Detect phishing patterns: brand impersonation, typosquatting, IDN homograph."""

    name = "phishing_patterns"
    severity = "critical"
    weight = 35
    requires_network = False

    async def run(self, ctx: CheckContext) -> object:
        flags = []

        # 1. IDN homograph attack (punycode)
        if has_punycode(ctx.domain):
            flags.append("IDN/Punycode domain — possible homograph attack")

        # 2. Brand name in domain without being the legitimate one
        domain_lower = ctx.domain.lower()
        subdomain_part = ctx.url.lower()
        for brand in COMMON_BRANDS:
            # Brand appears in domain but isn't the official one
            if brand in domain_lower and not domain_lower.startswith(brand + "."):
                # e.g. "paypal-login.example.com" or "example-paypal.com"
                if brand in domain_lower.split(".")[0]:
                    flags.append(f"Brand impersonation: '{brand}' in domain '{ctx.domain}'")
                    break

        # 3. Typosquatting patterns
        for pattern, brand in COMMON_TYPO_PATTERNS:
            if re.search(pattern, domain_lower):
                flags.append(f"Typosquatting detected: pattern '{pattern}' (target: {brand})")
                break

        # 4. Suspicious path (login/verify/update) on a non-brand domain
        if SUSPICIOUS_PATHS.search(ctx.url) and not any(
            b in domain_lower for b in COMMON_BRANDS
        ):
            # Suspicious only if combined with other risk factors
            # (login pages on legit sites are common)
            pass

        # 5. Subdomain impersonation (brand.example.com)
        try:
            from scamshield.utils.url_parser import parse_domain

            _, _, subdomain = parse_domain(ctx.url)
            if subdomain:
                sub_parts = subdomain.lower().split(".")
                for part in sub_parts:
                    for brand in COMMON_BRANDS:
                        if brand == part and not domain_lower.startswith(brand + "."):
                            flags.append(
                                f"Subdomain impersonation: '{brand}' as subdomain of '{ctx.domain}'"
                            )
                            break
        except Exception:
            pass

        if flags:
            return self._fail(
                "Phishing patterns detected: " + "; ".join(flags),
                flags=flags,
                brand_impersonation=any("impersonation" in f for f in flags),
            )

        return self._pass(
            "No phishing patterns detected",
            domain=ctx.domain,
        )
