"""Tests for FastAPI endpoints."""
import pytest
from fastapi.testclient import TestClient
from postfactory.server import app


@pytest.fixture
def client():
    return TestClient(app)


def test_healthz(client):
    r = client.get("/healthz")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "brand" in data


def test_root_html(client):
    r = client.get("/")
    assert r.status_code == 200


def test_generate_template_mode(client):
    r = client.post("/v1/generate?mode=template", json={
        "topic": "marketing tips",
        "platform": "instagram",
        "content_type": "educational",
        "variations": 2,
    })
    assert r.status_code == 200
    data = r.json()
    assert len(data["posts"]) == 2
    assert data["model_used"] == "template-fallback"


def test_hashtags_endpoint(client):
    r = client.get("/v1/hashtags?topic=marketing&niche=marketing&platform=instagram&count=10")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_calendar_endpoint(client):
    r = client.post("/v1/calendar", json={
        "days": 3,
        "platforms": ["instagram", "linkedin"],
    })
    assert r.status_code == 200
    data = r.json()
    assert len(data["calendar"]) == 3
    assert len(data["platforms"]) == 2
