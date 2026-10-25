"""Tests for FastAPI endpoints."""
import pytest
from fastapi.testclient import TestClient
from licitalert.server import app


@pytest.fixture
def client():
    return TestClient(app)


def test_healthz(client):
    r = client.get("/healthz")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "countries" in data


def test_root_html(client):
    r = client.get("/")
    assert r.status_code == 200


def test_list_rules_empty(client):
    r = client.get("/v1/rules")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_create_and_delete_rule(client):
    r = client.post("/v1/rules", json={
        "name": "Test rule",
        "countries": ["co"],
        "keywords": ["software"],
        "alert_channels": ["email"],
        "alert_recipient": "test@example.com",
    })
    assert r.status_code == 200
    rule_data = r.json()
    rule_id = rule_data["id"]
    assert rule_data["name"] == "Test rule"

    # Delete
    r2 = client.delete(f"/v1/rules/{rule_id}")
    assert r2.status_code == 200


def test_list_tenders(client):
    r = client.get("/v1/tenders")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_delete_nonexistent_rule(client):
    r = client.delete("/v1/rules/nonexistent")
    assert r.status_code == 404
