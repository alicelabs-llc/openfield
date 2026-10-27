"""Tests for URL utilities."""
import pytest

from scamshield.utils.url_parser import (
    has_punycode,
    is_ip_url,
    is_shortener,
    is_suspicious_tld,
    normalize_url,
    parse_domain,
)


class TestNormalizeUrl:
    def test_adds_https(self):
        assert normalize_url("example.com") == "https://example.com"

    def test_adds_http(self):
        assert normalize_url("http://example.com") == "http://example.com"

    def test_lowercases_host(self):
        assert normalize_url("HTTPS://EXAMPLE.com/Path") == "https://example.com/Path"

    def test_strips_fragment(self):
        assert normalize_url("https://example.com/page#section") == "https://example.com/page"

    def test_strips_default_port(self):
        assert normalize_url("https://example.com:443/path") == "https://example.com/path"
        assert normalize_url("http://example.com:80/path") == "https://example.com/path"[:0] + "http://example.com/path"

    def test_strips_userinfo(self):
        assert normalize_url("https://user:pass@example.com/") == "https://example.com/"

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            normalize_url("")

    def test_unsupported_scheme(self):
        with pytest.raises(ValueError):
            normalize_url("ftp://example.com")


class TestParseDomain:
    def test_simple(self):
        d, tld, sub = parse_domain("https://example.com/path")
        assert d == "example.com"
        assert tld == ".com"
        assert sub == ""

    def test_subdomain(self):
        d, tld, sub = parse_domain("https://blog.shop.example.co.uk/x")
        assert d == "example.co.uk"
        assert tld == ".co.uk"
        assert sub == "blog.shop"

    def test_ip(self):
        d, tld, sub = parse_domain("https://192.168.0.1:8080/")
        assert d == "192.168.0.1"
        assert tld == ""


class TestHeuristics:
    def test_is_ip_url_true(self):
        assert is_ip_url("https://1.2.3.4/") is True

    def test_is_ip_url_false(self):
        assert is_ip_url("https://example.com/") is False

    def test_is_shortener_true(self):
        assert is_shortener("bit.ly") is True

    def test_is_shortener_false(self):
        assert is_shortener("example.com") is False

    def test_suspicious_tld(self):
        assert is_suspicious_tld(".xyz") is True
        assert is_suspicious_tld(".top") is True
        assert is_suspicious_tld(".com") is False

    def test_punycode(self):
        assert has_punycode("xn--80ak6aa92e.com") is True
        assert has_punycode("example.com") is False
