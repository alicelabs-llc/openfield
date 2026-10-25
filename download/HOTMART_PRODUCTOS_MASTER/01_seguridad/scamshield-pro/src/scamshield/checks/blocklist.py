"""ScamShield Pro — Blocklist checks."""
from __future__ import annotations

import httpx

from scamshield.checks.base import BaseCheck, CheckContext

# Free public blocklist APIs (no auth required, rate-limited)
BLOCKLISTS = [
    {
        "name": "urlhaus_abuse_ch",
        "url": "https://urlhaus-api.abuse.ch/v1/host/",
        "method": "POST",
        "field": "host_status",
        "malicious_value": "online",
    },
    {
        "name": "phishtank",
        "url": "https://checkurl.phishtank.com/checkurl/",
        "method": "POST",
        # PhishTank requires API key for JSON; we use the public form (returns results)
        "field": None,
        "malicious_value": None,
    },
]


class BlocklistCheck(BaseCheck):
    """Query public blocklists to see if domain is flagged."""

    name = "blocklist_check"
    severity = "critical"
    weight = 40
    requires_network = True

    async def run(self, ctx: CheckContext) -> object:
        hits: list[dict] = []

        # 1. urlhaus.abuse.ch (malicious URLs/phishing)
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                response = await client.post(
                    "https://urlhaus-api.abuse.ch/v1/host/",
                    data={"host": ctx.domain},
                )
                if response.status_code == 200:
                    data = response.json()
                    if data.get("host_status") == "online":
                        hits.append({
                            "source": "urlhaus.abuse.ch",
                            "matched": True,
                            "malicious_urls_count": int(data.get("url_count", 0)),
                        })
        except Exception as e:
            # Soft failure — don't block scan
            hits.append({
                "source": "urlhaus.abuse.ch",
                "error": str(e),
            })

        # 2. Google Safe Browsing (if API key configured)
        from scamshield.core.config import get_settings

        s = get_settings()
        if s.gsb_api_key:
            try:
                gsb_url = (
                    f"https://safebrowsing.googleapis.com/v4/threatMatches:find"
                    f"?key={s.gsb_api_key}"
                )
                payload = {
                    "threatInfo": {
                        "threatEntryTypes": ["URL"],
                        "threatEntries": [{"url": ctx.url}],
                    },
                }
                async with httpx.AsyncClient(timeout=8.0) as client:
                    r = await client.post(gsb_url, json=payload)
                    if r.status_code == 200:
                        data = r.json()
                        if data.get("matches"):
                            hits.append({
                                "source": "google_safe_browsing",
                                "matched": True,
                                "threat_types": [m.get("threatType") for m in data["matches"]],
                            })
            except Exception as e:
                hits.append({
                    "source": "google_safe_browsing",
                    "error": str(e),
                })

        # 3. VirusTotal (if API key configured)
        if s.vt_api_key:
            try:
                headers = {"x-apikey": s.vt_api_key}
                vt_url = f"https://www.virustotal.com/api/v3/domains/{ctx.domain}"
                async with httpx.AsyncClient(timeout=10.0, headers=headers) as client:
                    r = await client.get(vt_url)
                    if r.status_code == 200:
                        data = r.json()
                        stats = (
                            data.get("data", {})
                            .get("attributes", {})
                            .get("last_analysis_stats", {})
                        )
                        malicious = stats.get("malicious", 0)
                        if malicious > 0:
                            hits.append({
                                "source": "virustotal",
                                "matched": True,
                                "malicious_votes": malicious,
                                "total_votes": sum(stats.values()),
                            })
            except Exception as e:
                hits.append({
                    "source": "virustotal",
                    "error": str(e),
                })

        # Aggregate verdict
        true_hits = [h for h in hits if h.get("matched")]
        if true_hits:
            return self._fail(
                f"Domain flagged on {len(true_hits)} blocklist(s): "
                + ", ".join(h["source"] for h in true_hits),
                hits=true_hits,
            )

        # If we got at least some successful queries, this is a pass
        successful_queries = [h for h in hits if "error" not in h]
        if successful_queries:
            return self._pass(
                f"Domain clean on {len(successful_queries)} blocklist(s)",
                queries=successful_queries,
            )

        # All queries failed — neutral
        return self._skip("All blocklist queries failed (network?)")
