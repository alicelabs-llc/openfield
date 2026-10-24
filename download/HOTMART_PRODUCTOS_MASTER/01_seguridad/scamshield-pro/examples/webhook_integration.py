"""Integrate ScamShield Pro into your payment / checkout flow.

Pattern: every time a customer submits a checkout, before charging their
card, scan the source URL of the order (referrer, link in description,
customer's website, etc.).

If score < 41 → block + flag for manual review.
If score 41-60 → allow but tag as "elevated risk" in the database.
If score > 60 → proceed normally.
"""
import asyncio
import sys

from scamshield.core.models import ScanRequest
from scamshield.scanner import Scanner


async def pre_charge_check(url_to_check: str) -> dict:
    """Return a decision dict for the checkout flow."""
    scanner = Scanner()
    result = await scanner.scan(ScanRequest(url=url_to_check))

    score = result.trust_score.value

    if score < 41:
        return {
            "decision": "block",
            "reason": f"Trust score {score}/100 — likely scam",
            "trust_score": score,
            "verdict": result.trust_score.verdict.value,
            "flagged_checks": [c.name for c in result.checks if not c.passed and c.severity in ("high", "critical")],
        }
    if score < 61:
        return {
            "decision": "review",
            "reason": f"Trust score {score}/100 — elevated risk, tag for monitoring",
            "trust_score": score,
            "verdict": result.trust_score.verdict.value,
        }
    return {
        "decision": "allow",
        "reason": f"Trust score {score}/100 — safe",
        "trust_score": score,
        "verdict": result.trust_score.verdict.value,
    }


async def main():
    if len(sys.argv) < 2:
        url = "https://example.com"
    else:
        url = sys.argv[1]
    decision = await pre_charge_check(url)
    print(f"URL: {url}")
    print(f"Decision: {decision['decision'].upper()}")
    print(f"Reason: {decision['reason']}")
    if decision.get("flagged_checks"):
        print(f"Flagged checks: {', '.join(decision['flagged_checks'])}")


if __name__ == "__main__":
    asyncio.run(main())
