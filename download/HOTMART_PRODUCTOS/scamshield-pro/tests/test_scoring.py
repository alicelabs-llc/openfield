"""Tests for the trust score aggregation."""
from scamshield.core.models import CheckResult, Verdict
from scamshield.core.scoring import compute_score


def _chk(passed, weight=10, severity="medium"):
    return CheckResult(
        name="x",
        passed=passed,
        severity=severity,
        weight=weight,
        message="",
    )


def test_all_pass_returns_high_score():
    checks = [_chk(True, weight=w) for w in (30, 25, 20, 15, 10)]
    score = compute_score(checks)
    assert score.value >= 80
    assert score.verdict == Verdict.VERY_SAFE or score.verdict == Verdict.LIKELY_SAFE


def test_all_fail_returns_low_score():
    checks = [_chk(False, weight=w, severity="critical") for w in (35, 30, 25, 20, 15)]
    score = compute_score(checks)
    assert score.value <= 20
    assert score.verdict == Verdict.VERY_UNSAFE


def test_mixed_signals_returns_mid_range():
    checks = [
        _chk(True, weight=30, severity="high"),
        _chk(True, weight=20, severity="medium"),
        _chk(False, weight=25, severity="high"),
        _chk(False, weight=15, severity="medium"),
    ]
    score = compute_score(checks)
    assert 20 <= score.value <= 80


def test_score_bounded():
    """Even extreme inputs must produce 1-100."""
    # Critical failures all over
    checks = [_chk(False, weight=100, severity="critical") for _ in range(20)]
    score = compute_score(checks)
    assert score.value == 1

    # Massive positives
    checks = [_chk(True, weight=100, severity="high") for _ in range(20)]
    score = compute_score(checks)
    assert score.value == 100


def test_few_checks_lowers_confidence():
    checks = [_chk(True, weight=30, severity="high")]
    score = compute_score(checks)
    assert score.confidence <= 30
