"""ScamShield Pro — Domain age & WHOIS check."""
from __future__ import annotations

from datetime import datetime

from scamshield.checks.base import BaseCheck, CheckContext
from scamshield.core.models import CheckResult


class DomainAgeCheck(BaseCheck):
    """Domain age check — newer domains are riskier.

    Mirrors ScamAdviser's signal: domains < 6 months old get a strong penalty.
    """

    name = "domain_age"
    severity = "high"
    weight = 25
    requires_network = True

    async def run(self, ctx: CheckContext) -> CheckResult:
        # Use cached whois if already fetched by another check
        if not ctx.whois_info:
            try:
                import whois  # python-whois

                w = whois.whois(ctx.domain)
                if w:
                    ctx.whois_info = {
                        k: v for k, v in w.items() if v
                    }
            except Exception as e:
                return self._fail(
                    f"WHOIS lookup failed: {type(e).__name__}",
                    exception=str(e),
                )

        info = ctx.whois_info
        creation_date_raw = info.get("creation_date")
        if not creation_date_raw:
            # Some TLDs hide creation date — moderate penalty
            return self._fail(
                "Domain creation date hidden or unavailable — common red flag",
                whois_keys=list(info.keys()),
            )

        # python-whois sometimes returns a list
        if isinstance(creation_date_raw, list):
            creation_date_raw = creation_date_raw[0]

        try:
            creation_date = (
                creation_date_raw
                if isinstance(creation_date_raw, datetime)
                else datetime.strptime(str(creation_date_raw)[:10], "%Y-%m-%d")
            )
        except Exception:
            return self._fail("Could not parse creation_date", raw=str(creation_date_raw))

        age_days = (datetime.utcnow() - creation_date).days
        ctx.domain_age_days = age_days

        if age_days < 30:
            return self._fail(
                f"Domain created {age_days} days ago — extremely high risk (brand-new)",
                age_days=age_days,
                created_on=creation_date.isoformat(),
            )
        if age_days < 90:
            return self._fail(
                f"Domain created {age_days} days ago — high risk (very new)",
                age_days=age_days,
                created_on=creation_date.isoformat(),
            )
        if age_days < 365:
            return self._fail(
                f"Domain created {age_days} days ago — moderate risk (< 1 year)",
                age_days=age_days,
                created_on=creation_date.isoformat(),
            )
        if age_days < 730:
            return self._pass(
                f"Domain age: {age_days} days (~{age_days // 30} months)",
                age_days=age_days,
            )
        return self._pass(
            f"Domain age: {age_days} days ({age_days // 365} years) — well established",
            age_days=age_days,
        )
