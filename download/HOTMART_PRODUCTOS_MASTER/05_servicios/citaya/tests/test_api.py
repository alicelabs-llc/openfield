"""Tests for FastAPI server."""
import pytest
from fastapi.testclient import TestClient
from citaya.server import app


@pytest.fixture
def client():
    return TestClient(app)


def test_healthz(client):
    r = client.get("/healthz")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"


def test_root_html(client):
    r = client.get("/")
    assert r.status_code == 200


def test_public_professionals_returns_list(client):
    r = client.get("/public/professionals")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_public_services_returns_list(client):
    r = client.get("/public/services")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
