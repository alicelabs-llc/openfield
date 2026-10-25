"""Tests for the FastAPI server (no network)."""
import pytest
from fastapi.testclient import TestClient

from scamshield.server import app


@pytest.fixture
def client():
    return TestClient(app)


def test_healthz(client):
    r = client.get("/healthz")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "checks_enabled" in data
    assert len(data["checks_enabled"]) >= 8


def test_root_returns_html(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "ScamShield" in r.text or "scamshield" in r.text.lower()


def test_list_checks(client):
    r = client.get("/v1/checks")
    assert r.status_code == 200
    checks = r.json()
    assert isinstance(checks, list)
    assert len(checks) >= 8
    names = [c["name"] for c in checks]
    assert "domain_age" in names
    assert "phishing_patterns" in names


def test_scan_invalid_url_returns_400(client):
    r = client.post("/v1/scan", json={"url": ""})
    assert r.status_code in (400, 422)
