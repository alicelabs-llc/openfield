"""ScamShield Pro — IP reputation check."""
from __future__ import annotations

import httpx

from scamshield.checks.base import BaseCheck, CheckContext


class ReputationCheck(BaseCheck):
    """IP & ASN reputation — uses free ip-api.com (no key required, 45 req/min)."""

    name = "ip_reputation"
    severity = "medium"
    weight = 12
    requires_network = True

    async def run(self, ctx: CheckContext) -> object:
        if not ctx.ip_address:
            return self._skip("No IP resolved yet (DNS check may have failed)")

        ip = ctx.ip_address

        # Free, no-auth: ip-api.com (45 req/min limit)
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                r = await client.get(
                    f"http://ip-api.com/json/{ip}?fields=status,message,country,city,isp,org,as,proxy,hosting"
                )
                if r.status_code != 200:
                    return self._skip(f"ip-api returned {r.status_code}")
                data = r.json()
                if data.get("status") != "success":
                    return self._skip(f"ip-api error: {data.get('message', 'unknown')}")
        except Exception as e:
            return self._fail(
                f"IP reputation lookup failed: {type(e).__name__}",
                error=str(e),
            )

        ctx.server_country = data.get("country")

        flags = []

        # 1. Hosting/CDN detection — not necessarily malicious but worth noting
        is_hosting = data.get("hosting", False)
        if is_hosting:
            flags.append("Hosted on datacenter IP (common for scam sites)")

        # 2. Proxy/VPN detection
        is_proxy = data.get("proxy", False)
        if is_proxy:
            flags.append("IP flagged as proxy/VPN")

        # 3. High-risk countries (subjective — these are countries with high
        # concentration of bulletproof hosting per Spamhaus reports)
        high_risk_countries = {"Russia", "China", "Nigeria", "Iran", "North Korea"}
        if data.get("country") in high_risk_countries:
            flags.append(f"Server located in {data['country']} (higher abuse rate)")

        # 4. ISP known for abuse
        isp = (data.get("isp") or "").lower()
        abuse_isps = {"team internet ag", "alexhost srl", "ovh sas", "choopa llc"}
        for ab in abuse_isps:
            if ab in isp:
                flags.append(f"ISP flagged: {data.get('isp')}")
                break

        if flags:
            self.severity = "high" if is_proxy else "medium"
            return self._fail(
                "IP reputation issues: " + "; ".join(flags),
                ip=ip,
                country=data.get("country"),
                city=data.get("city"),
                isp=data.get("isp"),
                asn=data.get("as"),
                is_proxy=is_proxy,
                is_hosting=is_hosting,
            )

        return self._pass(
            "IP reputation clean",
            ip=ip,
            country=data.get("country"),
            isp=data.get("isp"),
            asn=data.get("as"),
        )
