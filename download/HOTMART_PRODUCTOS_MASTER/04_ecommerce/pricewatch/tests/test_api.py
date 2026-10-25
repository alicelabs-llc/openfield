"""Tests for FastAPI endpoints."""
import pytest
from fastapi.testclient import TestClient
from pricewatch.server import app


@pytest.fixture
def client():
    return TestClient(app)


def test_healthz(client):
    r = client.get("/healthz")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "version" in data


def test_root_html(client):
    r = client.get("/")
    assert r.status_code == 200


def test_list_products_empty_default(client):
    r = client.get("/v1/products")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_get_unknown_product_404(client):
    r = client.get("/v1/products/nonexistent")
    assert r.status_code == 404


def test_delete_unknown_404(client):
    r = client.delete("/v1/products/nonexistent")
    assert r.status_code == 404
