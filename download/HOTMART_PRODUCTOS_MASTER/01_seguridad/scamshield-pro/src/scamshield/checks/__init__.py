"""ScamShield Pro — Detectores package."""
from scamshield.checks.base import BaseCheck, CheckContext  # noqa: F401
from scamshield.checks.blocklist import BlocklistCheck
from scamshield.checks.content import ContentCheck
from scamshield.checks.dns import DNSCheck
from scamshield.checks.domain import DomainAgeCheck
from scamshield.checks.phishing import PhishingPatternCheck
from scamshield.checks.redirect import RedirectChainCheck
from scamshield.checks.reputation import ReputationCheck
from scamshield.checks.ssl import SSLCheck
from scamshield.checks.tld import TLDReputationCheck

ALL_CHECKS = [
    DomainAgeCheck,
    SSLCheck,
    DNSCheck,
    TLDReputationCheck,
    RedirectChainCheck,
    ContentCheck,
    PhishingPatternCheck,
    BlocklistCheck,
    ReputationCheck,
]

__all__ = [
    "BaseCheck",
    "CheckContext",
    "ALL_CHECKS",
    "DomainAgeCheck",
    "SSLCheck",
    "DNSCheck",
    "TLDReputationCheck",
    "RedirectChainCheck",
    "ContentCheck",
    "PhishingPatternCheck",
    "BlocklistCheck",
    "ReputationCheck",
]
