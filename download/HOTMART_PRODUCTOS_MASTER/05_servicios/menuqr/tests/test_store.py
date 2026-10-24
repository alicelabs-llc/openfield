"""Tests for store (categories, items, tables, orders)."""
import pytest
from decimal import Decimal
from menuqr.core.models import Category, MenuItem, Table, Order
from menuqr.core.store import MenuStore


@pytest.fixture
def store(tmp_path, monkeypatch):
    monkeypatch.setenv("DATA_DIR", str(tmp_path / "data"))
    from menuqr.core.config import reset_settings_cache
    reset_settings_cache()
    return MenuStore()


def test_save_and_list_category(store):
    c = Category(id="entradas", name="Entradas", sort_order=1)
    store.save_category(c)
    cats = store.list_categories()
    assert len(cats) == 1
    assert cats[0].name == "Entradas"


def test_save_and_list_items(store):
    c = Category(id="principales", name="Principales")
    store.save_category(c)
    item = MenuItem(
        id="ITM-001", category_id="principales", name="Hamburguesa",
        description="Con queso", price=Decimal("12.50"),
    )
    store.save_item(item)
    items = store.list_items()
    assert len(items) == 1
    assert items[0].name == "Hamburguesa"
    assert items[0].price == Decimal("12.50")


def test_filter_by_category(store):
    store.save_category(Category(id="a", name="A"))
    store.save_category(Category(id="b", name="B"))
    store.save_item(MenuItem(id="1", category_id="a", name="X", price=Decimal("5")))
    store.save_item(MenuItem(id="2", category_id="b", name="Y", price=Decimal("7")))
    items_a = store.list_items(category_id="a")
    assert len(items_a) == 1
    assert items_a[0].id == "1"


def test_save_and_get_table(store):
    t = Table(id="TBL-001", number=1, capacity=4, location="interior")
    store.save_table(t)
    found = store.get_table("TBL-001")
    assert found is not None
    assert found.number == 1


def test_save_and_get_order(store):
    order = Order(
        id="ORD-001", table_id="TBL-001", table_number=1,
        items=[{"item_id": "X", "qty": 2}], total=Decimal("25.00"),
    )
    store.save_order(order)
    found = store.get_order("ORD-001")
    assert found is not None
    assert found.total == Decimal("25.00")
    assert found.status == "pending"


def test_delete_item(store):
    item = MenuItem(id="DEL-001", category_id="x", name="ToDelete", price=Decimal("1"))
    store.save_item(item)
    assert store.delete_item("DEL-001") is True
    assert store.delete_item("NONEXIST") is False


def test_get_full_menu(store):
    store.save_category(Category(id="c1", name="Cat 1"))
    store.save_item(MenuItem(id="i1", category_id="c1", name="Item 1", price=Decimal("10")))
    menu = store.get_full_menu()
    assert menu.restaurant_name  # from settings
    assert len(menu.categories) == 1
    assert len(menu.items) == 1
