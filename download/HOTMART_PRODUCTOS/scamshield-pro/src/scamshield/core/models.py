"""ScamShield Pro — Pydantic models for scan results."""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class Verdict(str, Enum):
    """Final trust verdict band. Mirrors ScamAdviser's 5-tier scale."""

    VERY_SAFE = "very_likely_safe"            # 81-100  ✅
    LIKELY_SAFE = "likely_safe"               # 61-80   🟢
    CAUTION = "caution_recommended"           # 41-60   🟡
    LIKELY_UNSAFE = "likely_unsafe"           # 21-40   🟠
    VERY_UNSAFE = "very_likely_unsafe"        # 1-20    🔴

    @property
    def emoji(self) -> str:
        return {
            Verdict.VERY_SAFE: "✅",
            Verdict.LIKELY_SAFE: "🟢",
            Verdict.CAUTION: "🟡",
            Verdict.LIKELY_UNSAFE: "🟠",
            Verdict.VERY_UNSAFE: "🔴",
        }[self]

    @property
    def recommendation(self) -> str:
        return {
            Verdict.VERY_SAFE: "High confidence. Standard good practice still applies.",
            Verdict.LIKELY_SAFE: "Reasonable to proceed. Read returns policy, use a credit card.",
            Verdict.CAUTION: "Verify physical address and independent reviews before transacting.",
            Verdict.LIKELY_UNSAFE: "Avoid transactions. Search independent reviews on Google.",
            Verdict.VERY_UNSAFE: "Do not visit. Do not enter any personal or payment info.",
        }[self]


class CheckResult(BaseModel):
    """Result of a single detector."""

    name: str
    passed: bool = Field(description="True = no risk detected by this check")
    severity: str = Field(default="info", description="info|low|medium|high|critical")
    weight: int = Field(default=0, ge=0, le=100)
    message: str
    details: dict[str, Any] = Field(default_factory=dict)


class TrustScore(BaseModel):
    """Composite trust score 0-100 (100 = safest)."""

    value: int = Field(ge=0, le=100)
    verdict: Verdict
    positive_signals: int = Field(default=0)
    negative_signals: int = Field(default=0)
    confidence: int = Field(default=50, ge=0, le=100, description="Confidence in the score")


class ScanResult(BaseModel):
    """Full scan report for a URL."""

    url: str
    normalized_url: str
    final_url: Optional[str] = None
    domain: str
    tld: str
    scanned_at: datetime = Field(default_factory=datetime.utcnow)
    duration_ms: int = Field(default=0)

    trust_score: TrustScore
    checks: list[CheckResult] = Field(default_factory=list)

    # Key fields for quick UI display
    ip_address: Optional[str] = None
    server_country: Optional[str] = None
    domain_age_days: Optional[int] = None
    ssl_valid: Optional[bool] = None
    redirect_count: Optional[int] = None

    class Config:
        use_enum_values = True

    def summary(self) -> str:
        """One-line human summary."""
        return (
            f"{self.trust_score.verdict.emoji} Score {self.trust_score.value}/100 "
            f"({self.trust_score.verdict.value}) — {self.domain}"
        )


class ScanRequest(BaseModel):
    """Inbound scan request."""

    url: str = Field(..., description="URL to analyze")
    follow_redirects: bool = Field(default=True)
    fetch_content: bool = Field(default=True, description="Fetch & analyze HTML content")
    timeout: Optional[float] = Field(default=None, ge=1, le=60)


class BulkScanRequest(BaseModel):
    """Bulk scan request."""

    urls: list[str] = Field(..., min_length=1, max_length=100)


class HealthResponse(BaseModel):
    status: str
    version: str
    checks_enabled: list[str]
