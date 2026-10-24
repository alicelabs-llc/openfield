"""ScamShield Pro — TLD reputation check."""
from __future__ import annotations

from scamshield.checks.base import BaseCheck, CheckContext
from scamshield.utils.url_parser import is_suspicious_tld


class TLDReputationCheck(BaseCheck):
    """Flag domains on TLDs over-represented in abuse datasets."""

    name = "tld_reputation"
    severity = "medium"
    weight = 15
    requires_network = False

    async def run(self, ctx: CheckContext) -> object:
        if not ctx.tld:
            return self._pass("No TLD parsed (possibly an IP-address URL)")

        if is_suspicious_tld(ctx.tld):
            return self._fail(
                f"Suspicious TLD: {ctx.tld} — statistically over-represented in abuse",
                tld=ctx.tld,
            )

        # Premium / trustworthy TLDs
        trusted_tlds = {".com", ".org", ".net", ".gov", ".edu", ".io", ".dev", ".ai"}
        if ctx.tld.lower() in trusted_tlds:
            return self._pass(
                f"Common TLD: {ctx.tld}",
                tld=ctx.tld,
            )

        return self._pass(
            f"Country-code or specialty TLD: {ctx.tld}",
            tld=ctx.tld,
        )
