"""MenuQR Pro — Store (JSON-based persistence)."""
from __future__ import annotations
import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from menuqr.core.config import get_settings
from menuqr.core.models import Menu, Category, MenuItem, Table, Order


class MenuStore:
    """JSON file-based store for menus, tables, orders."""

    def __init__(self):
        self.settings = get_settings()

    @property
    def base_path(self) -> Path:
        return self.settings.data_path

    def _file(self, name: str) -> Path:
        p = self.base_path / f"{name}.json"
        if not p.exists():
            p.write_text("[]", encoding="utf-8")
        return p

    def _load(self, name: str) -> list[dict]:
        return json.loads(self._file(name).read_text(encoding="utf-8"))

    def _save(self, name: str, data: list[dict]):
        self._file(name).write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")

    # Categories
    def list_categories(self) -> list[Category]:
        return [Category(**c) for c in self._load("categories")]

    def save_category(self, cat: Category) -> Category:
        items = self._load("categories")
        items = [c for c in items if c["id"] != cat.id]
        items.append(cat.model_dump())
        items.sort(key=lambda c: c.get("sort_order", 0))
        self._save("categories", items)
        return cat

    # Menu items
    def list_items(self, category_id: str = None, available_only: bool = False) -> list[MenuItem]:
        items = self._load("items")
        result = []
        for i in items:
            i["price"] = Decimal(str(i["price"]))
            result.append(MenuItem(**i))
        if category_id:
            result = [i for i in result if i.category_id == category_id]
        if available_only:
            result = [i for i in result if i.available]
        return result

    def get_item(self, item_id: str) -> MenuItem | None:
        for i in self.list_items():
            if i.id == item_id:
                return i
        return None

    def save_item(self, item: MenuItem) -> MenuItem:
        items = self._load("items")
        items = [i for i in items if i["id"] != item.id]
        d = item.model_dump()
        d["price"] = str(d["price"])
        items.append(d)
        self._save("items", items)
        return item

    def delete_item(self, item_id: str) -> bool:
        items = self._load("items")
        before = len(items)
        items = [i for i in items if i["id"] != item_id]
        if len(items) < before:
            self._save("items", items)
            return True
        return False

    # Tables
    def list_tables(self) -> list[Table]:
        return [Table(**t) for t in self._load("tables")]

    def get_table(self, table_id: str) -> Table | None:
        for t in self.list_tables():
            if t.id == table_id:
                return t
        return None

    def save_table(self, table: Table) -> Table:
        tables = self._load("tables")
        tables = [t for t in tables if t["id"] != table.id]
        tables.append(table.model_dump())
        self._save("tables", tables)
        return table

    # Orders
    def list_orders(self, status: str = None) -> list[Order]:
        orders = self._load("orders")
        result = []
        for o in orders:
            o["total"] = Decimal(str(o.get("total", "0")))
            o["created_at"] = datetime.fromisoformat(o["created_at"]) if isinstance(o.get("created_at"), str) else o.get("created_at")
            result.append(Order(**o))
        if status:
            result = [o for o in result if o.status == status]
        return result

    def get_order(self, order_id: str) -> Order | None:
        for o in self.list_orders():
            if o.id == order_id:
                return o
        return None

    def save_order(self, order: Order) -> Order:
        orders = self._load("orders")
        orders = [o for o in orders if o["id"] != order.id]
        d = order.model_dump()
        d["total"] = str(d["total"])
        orders.append(d)
        self._save("orders", orders)
        return order

    # Composite
    def get_full_menu(self) -> Menu:
        s = get_settings()
        return Menu(
            id="default",
            restaurant_name=s.restaurant_name,
            categories=self.list_categories(),
            items=self.list_items(available_only=True),
            available_languages=s.restaurant_languages.split(","),
        )
