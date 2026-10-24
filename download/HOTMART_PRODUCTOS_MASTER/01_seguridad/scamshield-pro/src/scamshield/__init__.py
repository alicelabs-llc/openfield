"""ScamShield Pro — Self-hosted URL fraud & phishing detector."""

__version__ = "1.0.0"
__author__ = "Eddy Flores"
__email__ = "eddyflores100@gmail.com"

from scamshield.core.config import Settings, get_settings  # noqa: F401
from scamshield.core.models import ScanResult, TrustScore, Verdict  # noqa: F401

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "Settings",
    "get_settings",
    "ScanResult",
    "TrustScore",
    "Verdict",
]
