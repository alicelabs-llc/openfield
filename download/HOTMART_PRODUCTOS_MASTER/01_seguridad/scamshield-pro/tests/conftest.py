"""Pytest config — shared fixtures."""
import os
import sys
from pathlib import Path

# Ensure src/ is importable
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

# Disable external network calls by default during tests
os.environ.setdefault("HTTP_TIMEOUT_SECONDS", "3")
os.environ.setdefault("DNS_TIMEOUT_SECONDS", "2")

import pytest


@pytest.fixture
def sample_urls():
    return {
        "good": "https://www.example.com",
        "good_github": "https://github.com/python/cpython",
        "no_scheme": "example.com",
        "ip": "https://192.168.1.1/",
        "punycode": "https://xn--80ak6aa92e.com/",
        "suspicious_tld": "https://free-stuff-claim.top/",
    }
