"""ScamShield Pro — DNS records check."""
from __future__ import annotations

import dns.resolver

from scamshield.checks.base import BaseCheck, CheckContext
from scamshield.core.config import get_settings


class DNSCheck(BaseCheck):
    """Resolve A, MX, NS, TXT records; flag suspicious patterns."""

    name = "dns_records"
    severity = "medium"
    weight = 15
    requires_network = True

    async def run(self, ctx: CheckContext) -> object:
        s = get_settings()
        resolver = dns.resolver.Resolver()
        resolver.lifetime = s.dns_timeout_seconds
        resolver.timeout = s.dns_timeout_seconds

        records: dict[str, list[str]] = {}

        # A record (IPv4)
        try:
            a_records = resolver.resolve(ctx.domain, "A")
            records["A"] = [r.to_text() for r in a_records]
            ctx.ip_address = records["A"][0] if records["A"] else None
        except Exception:
            records["A"] = []

        # AAAA (IPv6)
        try:
            records["AAAA"] = [r.to_text() for r in resolver.resolve(ctx.domain, "AAAA")]
        except Exception:
            records["AAAA"] = []

        # MX (mail)
        try:
            records["MX"] = [r.to_text() for r in resolver.resolve(ctx.domain, "MX")]
        except Exception:
            records["MX"] = []

        # NS (nameservers)
        try:
            records["NS"] = [r.to_text() for r in resolver.resolve(ctx.domain, "NS")]
        except Exception:
            records["NS"] = []

        # TXT (SPF, etc)
        try:
            records["TXT"] = [r.to_text() for r in resolver.resolve(ctx.domain, "TXT")]
        except Exception:
            records["TXT"] = []

        ctx.dns_records = records

        # Evaluate
        if not records["A"] and not records["AAAA"]:
            return self._fail("Domain does not resolve — no A/AAAA records", records=records)

        failures = []
        if not records["MX"]:
            failures.append("no MX records (cannot receive email)")
        if not records["NS"]:
            failures.append("no NS records")
        if not records["TXT"]:
            failures.append("no TXT records (no SPF/DKIM)")

        # Check for SPF
        spf_present = any("v=spf1" in t for t in records["TXT"])
        if not spf_present:
            failures.append("no SPF record")

        if failures:
            severity = "high" if len(failures) >= 3 else "medium"
            self.severity = severity
            return self._fail(
                "DNS configuration issues: " + ", ".join(failures),
                records=records,
                issues=failures,
            )

        return self._pass(
            "DNS records complete (A, MX, NS, TXT, SPF)",
            records=records,
            ip=ctx.ip_address,
        )
