"""ScamShield Pro — Trust score aggregation.

Mirrors the 5-tier band used by ScamAdviser (0-100 scale, 100 = safest),
so output is directly comparable to consumer-trusted references.
"""
from __future__ import annotations

from scamshield.core.models import CheckResult, TrustScore, Verdict


def _verdict_for(score: int) -> Verdict:
    if score >= 81:
        return Verdict.VERY_SAFE
    if score >= 61:
        return Verdict.LIKELY_SAFE
    if score >= 41:
        return Verdict.CAUTION
    if score >= 21:
        return Verdict.LIKELY_UNSAFE
    return Verdict.VERY_UNSAFE


def compute_score(checks: list[CheckResult]) -> TrustScore:
    """Aggregate per-check results into a single 0-100 trust score.

    Algorithm:
      - Start at 75 (neutral-leaning-safe baseline)
      - Subtract weighted penalties for each failed check
      - Add small bonus for each passed high-weight check
      - Clamp to [1, 100]
      - Confidence = coverage of high-severity checks
    """
    score = 75
    positives = 0
    negatives = 0
    high_weight_executed = 0
    high_weight_passed = 0

    for c in checks:
        if c.severity in ("high", "critical"):
            high_weight_executed += 1
            if c.passed:
                high_weight_passed += 1

        if c.passed:
            # Reward for passing high-weight checks (positive drift)
            if c.weight >= 20:
                score += min(c.weight // 8, 6)
                positives += 1
        else:
            penalty = c.weight
            if c.severity == "critical":
                penalty = min(penalty * 1.5, 60)
            score -= penalty
            negatives += 1

    score = max(1, min(100, round(score)))
    confidence = (
        round((high_weight_passed / high_weight_executed) * 100) if high_weight_executed else 40
    )
    # Confidence also lowered when very few checks executed
    if len(checks) < 5:
        confidence = min(confidence, 30)

    return TrustScore(
        value=score,
        verdict=_verdict_for(score),
        positive_signals=positives,
        negative_signals=negatives,
        confidence=confidence,
    )
