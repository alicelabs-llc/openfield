"""Tests for FastAPI server."""
import pytest
from fastapi.testclient import TestClient
from leadharvester.server import app


@pytest.fixture
def client():
    return TestClient(app)


def test_healthz(client):
    r = client.get("/healthz")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "version" in data


def test_root_returns_html(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "LeadHarvester" in r.text or "leadharvester" in r.text.lower()


def test_get_unknown_job_404(client):
    r = client.get("/v1/scrape/nonexistent")
    assert r.status_code == 404
