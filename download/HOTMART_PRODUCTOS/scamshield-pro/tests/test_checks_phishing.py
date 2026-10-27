"""Tests for phishing-pattern detector (no network needed)."""
import pytest

from scamshield.checks.base import CheckContext
from scamshield.checks.phishing import PhishingPatternCheck


async def _run(url: str, domain: str, tld: str = ".com"):
    ctx = CheckContext(
        url=url,
        normalized_url=url,
        domain=domain,
        tld=tld,
    )
    return await PhishingPatternCheck().run(ctx)


@pytest.mark.asyncio
async def test_clean_domain_passes():
    result = await _run("https://example-shop.com/", "example-shop.com")
    assert result.passed is True


@pytest.mark.asyncio
async def test_brand_in_domain_fails():
    result = await _run(
        "https://paypal-secure-login.example.com/",
        "paypal-secure-login.example.com",
    )
    assert result.passed is False
    assert any("impersonation" in f for f in result.details.get("flags", []))


@pytest.mark.asyncio
async def test_punycode_fails():
    result = await _run(
        "https://xn--80ak6aa92e.com/",
        "xn--80ak6aa92e.com",
    )
    assert result.passed is False


@pytest.mark.asyncio
async def test_typosquatting_paypa1_fails():
    result = await _run("https://paypa1-login.com/", "paypa1-login.com")
    assert result.passed is False
