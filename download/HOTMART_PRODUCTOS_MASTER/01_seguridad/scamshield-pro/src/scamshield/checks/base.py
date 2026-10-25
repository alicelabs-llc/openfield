"""ScamShield Pro — Base detector class."""
from __future__ import annotations

import abc
from dataclasses import dataclass, field
from typing import Any

from scamshield.core.models import CheckResult


@dataclass
class CheckContext:
    """Shared context populated incrementally by checks.

    Allows later checks (e.g. content) to use info gathered by earlier
    checks (e.g. resolved IP from DNS).
    """

    url: str
    normalized_url: str
    domain: str
    tld: str
    follow_redirects: bool = True
    fetch_content: bool = True
    timeout: float = 10.0
    # Populated progressively
    ip_address: str | None = None
    final_url: str | None = None
    redirect_chain: list[str] = field(default_factory=list)
    redirect_count: int | None = None
    http_status: int | None = None
    http_headers: dict[str, str] = field(default_factory=dict)
    html_content: str | None = None
    ssl_cert: Any = None
    whois_info: dict[str, Any] = field(default_factory=dict)
    dns_records: dict[str, list[str]] = field(default_factory=dict)
    server_country: str | None = None
    domain_age_days: int | None = None
    ssl_valid: bool | None = None
    cache: Any = None  # diskcache.Cache or None


class BaseCheck(abc.ABC):
    """Abstract base for all detectors."""

    name: str = "base_check"
    severity: str = "info"           # info|low|medium|high|critical
    weight: int = 0                  # 0-100, points subtracted on failure
    requires_network: bool = False   # needs outbound HTTP/DNS
    requires_content: bool = False   # needs ctx.html_content

    @abc.abstractmethod
    async def run(self, ctx: CheckContext) -> CheckResult:
        """Execute the check, return a CheckResult."""
        raise NotImplementedError

    def _pass(self, message: str, **details: Any) -> CheckResult:
        return CheckResult(
            name=self.name,
            passed=True,
            severity=self.severity,
            weight=self.weight,
            message=message,
            details=details,
        )

    def _fail(self, message: str, **details: Any) -> CheckResult:
        return CheckResult(
            name=self.name,
            passed=False,
            severity=self.severity,
            weight=self.weight,
            message=message,
            details=details,
        )

    def _skip(self, reason: str) -> CheckResult:
        return CheckResult(
            name=self.name,
            passed=True,
            severity="info",
            weight=0,
            message=f"skipped: {reason}",
            details={"skipped": True},
        )
