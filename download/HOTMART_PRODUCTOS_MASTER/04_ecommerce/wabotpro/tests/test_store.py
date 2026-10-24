"""Tests for store/catalog persistence."""
import pytest
from decimal import Decimal
from wabotpro.core.models import Product
from wabotpro.core.store import Store


@pytest.fixture
def store(tmp_path, monkeypatch):
    monkeypatch.setenv("DATA_DIR", str(tmp_path / "data"))
    from wabotpro.core.config import reset_settings_cache
    reset_settings_cache()
    return Store()


def test_add_and_get_product(store):
    p = Product(id="P001", name="Test", price=Decimal("9.99"), stock=5)
    store.add_product(p)
    found = store.find_product("P001")
    assert found is not None
    assert found.name == "Test"
    assert found.price == Decimal("9.99")


def test_remove_product(store):
    p = Product(id="P002", name="To Remove", price=Decimal("19.99"))
    store.add_product(p)
    assert store.remove_product("P002") is True
    assert store.find_product("P002") is None


def test_remove_nonexistent_returns_false(store):
    assert store.remove_product("NONEXISTENT") is False


def test_get_catalog_empty(store):
    catalog = store.get_catalog()
    assert isinstance(catalog, list)
    assert len(catalog) == 0


def test_save_and_get_order(store):
    from wabotpro.core.models import Order, CartItem
    order = Order(
        id="ORD-TEST123",
        customer_number="593999123456",
        items=[
            CartItem(product_id="P001", product_name="X", quantity=2, unit_price=Decimal("10.00")),
        ],
    )
    store.save_order(order)
    found = store.get_order("ORD-TEST123")
    assert found is not None
    assert found.customer_number == "593999123456"
    assert found.total == Decimal("20.00")
