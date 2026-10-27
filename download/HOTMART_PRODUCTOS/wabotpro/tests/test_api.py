"""Tests for FastAPI server."""
import pytest
from fastapi.testclient import TestClient
from wabotpro.server import app


@pytest.fixture
def client():
    return TestClient(app)


def test_healthz(client):
    r = client.get("/healthz")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "business_name" in data


def test_root_html(client):
    r = client.get("/")
    assert r.status_code == 200


def test_webhook_verify_invalid_token(client):
    r = client.get("/webhook?hub.mode=subscribe&hub.challenge=123&hub.verify_token=invalid")
    assert r.status_code == 403


def test_simulate_endpoint(client):
    r = client.post("/v1/simulate?from_number=593999123456&text=hola", )
    assert r.status_code == 200
    data = r.json()
    assert "responses" in data
    assert len(data["responses"]) >= 1
