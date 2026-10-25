"""Tests for FastAPI endpoints."""
import pytest
from fastapi.testclient import TestClient
from facturapro.server import app


@pytest.fixture
def client():
    return TestClient(app)


def test_healthz(client):
    r = client.get("/healthz")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "country" in data


def test_root_returns_html(client):
    r = client.get("/")
    assert r.status_code == 200
