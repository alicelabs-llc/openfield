"""ScamShield Pro — Scanner engine.

Orchestrates all checks, accumulates context, computes final trust score.
"""
from __future__ import annotations

import asyncio
import time
from typing import Optional

from scamshield.checks import ALL_CHECKS, BaseCheck, CheckContext
from scamshield.core.models import CheckResult, ScanResult, ScanRequest
from scamshield.core.scoring import compute_score
from scamshield.utils.url_parser import normalize_url, parse_domain


class Scanner:
    """Run all detectors against a URL and produce a ScanResult."""

    def __init__(
        self,
        check_classes: Optional[list[type[BaseCheck]]] = None,
        parallel: bool = True,
    ) -> None:
        self.check_classes = check_classes or ALL_CHECKS
        self.parallel = parallel

    async def scan(self, request: ScanRequest) -> ScanResult:
        t0 = time.perf_counter()

        # Normalize URL
        normalized = normalize_url(request.url)
        domain, tld, _ = parse_domain(normalized)

        ctx = CheckContext(
            url=request.url,
            normalized_url=normalized,
            domain=domain,
            tld=tld,
            follow_redirects=request.follow_redirects,
            fetch_content=request.fetch_content,
            timeout=request.timeout or 10.0,
        )

        # Order matters: domain/SSL/DNS first (populate ctx),
        # then content/phishing (use ctx), then blocklist/reputation.
        checks = [cls() for cls in self.check_classes]

        # Two-phase: parallel batch of independent checks, then sequential
        # for checks that depend on prior ctx (reputation needs IP, content needs HTML)
        phase1 = [c for c in checks if not c.requires_content]
        phase2 = [c for c in checks if c.requires_content]

        results: list[CheckResult] = []

        # Phase 1
        if self.parallel:
            done = await asyncio.gather(
                *[c.run(ctx) for c in phase1], return_exceptions=True
            )
        else:
            done = []
            for c in phase1:
                done.append(await c.run(ctx))

        for i, r in enumerate(done):
            if isinstance(r, Exception):
                results.append(CheckResult(
                    name=phase1[i].name,
                    passed=False,
                    severity="medium",
                    weight=phase1[i].weight,
                    message=f"Check raised: {type(r).__name__}: {r}",
                ))
            else:
                results.append(r)

        # Phase 2 (after phase 1 populated ctx.ip_address, ctx.final_url, etc.)
        for c in phase2:
            try:
                results.append(await c.run(ctx))
            except Exception as e:
                results.append(CheckResult(
                    name=c.name,
                    passed=False,
                    severity="medium",
                    weight=c.weight,
                    message=f"Check raised: {type(e).__name__}: {e}",
                ))

        # Compute final score
        trust_score = compute_score(results)
        duration_ms = int((time.perf_counter() - t0) * 1000)

        return ScanResult(
            url=request.url,
            normalized_url=normalized,
            final_url=ctx.final_url,
            domain=domain,
            tld=tld,
            duration_ms=duration_ms,
            trust_score=trust_score,
            checks=results,
            ip_address=ctx.ip_address,
            server_country=ctx.server_country,
            domain_age_days=ctx.domain_age_days,
            ssl_valid=ctx.ssl_valid,
            redirect_count=ctx.redirect_count,
        )
