"""Tests for FastAPI endpoints."""
import pytest
from fastapi.testclient import TestClient
from reviewreply.server import app


@pytest.fixture
def client():
    return TestClient(app)


def test_healthz(client):
    r = client.get("/healthz")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "ai_provider" in data


def test_root_html(client):
    r = client.get("/")
    assert r.status_code == 200


def test_templates_list(client):
    r = client.get("/v1/templates")
    assert r.status_code == 200
    data = r.json()
    assert "positive" in data
    assert "negative" in data
    assert "corto" in data["positive"]


def test_generate_template_mode(client):
    """Test template mode (no AI required)."""
    r = client.post("/v1/generate?mode=template", json={
        "rating": 5,
        "text": "Excelente servicio",
        "author_name": "Test",
    })
    assert r.status_code == 200
    data = r.json()
    assert "suggestions" in data
    assert len(data["suggestions"]) == 3


def test_generate_negative_review_template(client):
    r = client.post("/v1/generate?mode=template", json={
        "rating": 1,
        "text": "Pesimo servicio, lento y sucio",
        "author_name": "Pedro",
    })
    assert r.status_code == 200
    data = r.json()
    assert data["detected_sentiment"] == "negative"
    assert len(data["suggestions"]) == 3
