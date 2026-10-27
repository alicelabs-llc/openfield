"""WhatsAppBot Pro — Catalog & order store (JSON-based)."""
from __future__ import annotations
import json
from pathlib import Path
from decimal import Decimal
from wabotpro.core.config import get_settings
from wabotpro.core.models import Product, Order


class Store:
    """Simple JSON store for products and orders."""

    def __init__(self):
        self.settings = get_settings()

    @property
    def catalog_path(self) -> Path:
        p = self.settings.data_path / "catalog.json"
        if not p.exists():
            p.write_text("[]", encoding="utf-8")
        return p

    @property
    def orders_path(self) -> Path:
        p = self.settings.data_path / "orders.json"
        if not p.exists():
            p.write_text("[]", encoding="utf-8")
        return p

    def get_catalog(self) -> list[Product]:
        data = json.loads(self.catalog_path.read_text(encoding="utf-8"))
        return [Product(**p) for p in data]

    def add_product(self, product: Product) -> Product:
        catalog = self.get_catalog()
        # Replace if exists
        catalog = [p for p in catalog if p.id != product.id]
        catalog.append(product)
        self._save_catalog(catalog)
        return product

    def remove_product(self, product_id: str) -> bool:
        catalog = self.get_catalog()
        before = len(catalog)
        catalog = [p for p in catalog if p.id != product_id]
        if len(catalog) < before:
            self._save_catalog(catalog)
            return True
        return False

    def find_product(self, product_id: str) -> Product | None:
        for p in self.get_catalog():
            if p.id == product_id:
                return p
        return None

    def _save_catalog(self, catalog: list[Product]):
        data = [p.model_dump() for p in catalog]
        # Convert Decimal
        for d in data:
            d["price"] = str(d["price"])
        self.catalog_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    # Orders
    def save_order(self, order: Order) -> Order:
        orders = self.get_orders()
        orders = [o for o in orders if o.id != order.id]
        orders.append(order)
        self._save_orders(orders)
        return order

    def get_orders(self) -> list[Order]:
        data = json.loads(self.orders_path.read_text(encoding="utf-8"))
        orders = []
        for d in data:
            # Deserialize items
            items = []
            for item in d.get("items", []):
                item["unit_price"] = Decimal(str(item["unit_price"]))
                from wabotpro.core.models import CartItem
                items.append(CartItem(**item))
            d["items"] = items
            orders.append(Order(**d))
        return orders

    def get_order(self, order_id: str) -> Order | None:
        for o in self.get_orders():
            if o.id == order_id:
                return o
        return None

    def _save_orders(self, orders: list[Order]):
        data = []
        for o in orders:
            d = o.model_dump()
            d["items"] = [{
                "product_id": i.product_id,
                "product_name": i.product_name,
                "quantity": i.quantity,
                "unit_price": str(i.unit_price),
            } for i in o.items]
            data.append(d)
        self.orders_path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
