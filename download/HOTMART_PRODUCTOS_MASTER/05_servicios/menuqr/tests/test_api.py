"""Tests for FastAPI endpoints."""
import pytest
from fastapi.testclient import TestClient
from menuqr.server import app


@pytest.fixture
def client():
    return TestClient(app)


def test_healthz(client):
    r = client.get("/healthz")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "restaurant" in data


def test_root_html(client):
    r = client.get("/")
    assert r.status_code == 200


def test_list_items_empty_default(client):
    r = client.get("/admin/items")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_create_category(client):
    r = client.post("/admin/categories", json={"id": "test", "name": "Test Cat", "sort_order": 1})
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "Test Cat"


def test_create_item(client):
    r = client.post("/admin/items", json={
        "category_id": "test",
        "name": "Test Item",
        "price": 9.99,
    })
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "Test Item"
    assert "id" in data


def test_create_table_and_get_qr(client):
    r = client.post("/admin/tables", json={
        "number": 5, "name": "Mesa Ventana", "capacity": 2, "location": "terraza",
    })
    assert r.status_code == 200
    table_data = r.json()
    table_id = table_data["id"]

    r2 = client.get(f"/admin/tables/{table_id}/qr")
    assert r2.status_code == 200
    assert r2.headers["content-type"] == "image/png"


def test_get_menu_qr(client):
    r = client.get("/admin/menu/qr")
    assert r.status_code == 200
    assert r.headers["content-type"] == "image/png"
