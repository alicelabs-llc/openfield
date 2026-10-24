"""Tests for the flow engine (no network)."""
import pytest
from decimal import Decimal
from wabotpro.core.models import Message, Product
from wabotpro.core.store import Store
from wabotpro.flows import FlowEngine


@pytest.fixture
def store_with_products(tmp_path, monkeypatch):
    """Create a store with sample products."""
    monkeypatch.setenv("DATA_DIR", str(tmp_path / "data"))
    from wabotpro.core.config import reset_settings_cache
    reset_settings_cache()
    s = Store()
    s.add_product(Product(id="P001", name="Camiseta", price=Decimal("15.00"), stock=10))
    s.add_product(Product(id="P002", name="Pantalón", price=Decimal("35.00"), stock=5))
    s.add_product(Product(id="P003", name="Zapatos", price=Decimal("59.99"), stock=0))
    return s


@pytest.fixture
def flow(store_with_products):
    return FlowEngine(store_with_products)


def _msg(text, number="593999123456"):
    return Message(from_number=number, to_number="bot", text=text)


class TestMenuAndHelp:
    def test_hola_returns_menu(self, flow):
        responses = flow.process(_msg("hola"))
        assert len(responses) == 1
        # Menu includes business name with emoji or menu greeting
        assert "negocio" in responses[0].lower() or "🛒" in responses[0] or "qué deseas" in responses[0].lower()

    def test_help_lists_commands(self, flow):
        responses = flow.process(_msg("ayuda"))
        assert "agregar" in responses[0].lower()
        assert "confirmar" in responses[0].lower()


class TestCatalog:
    def test_catalogo_lists_products(self, flow):
        responses = flow.process(_msg("catálogo"))
        assert "P001" in responses[0]
        assert "Camiseta" in responses[0]
        assert "$15.00" in responses[0]


class TestCartFlow:
    def test_add_to_cart(self, flow):
        responses = flow.process(_msg("agregar P001 2"))
        assert "✅" in responses[0]
        assert "Camiseta" in responses[0]
        assert "$30.00" in responses[0]

    def test_add_invalid_product(self, flow):
        responses = flow.process(_msg("agregar P999 1"))
        assert "no encontrado" in responses[0]

    def test_add_out_of_stock(self, flow):
        # P003 has 0 stock
        responses = flow.process(_msg("agregar P003 1"))
        # Out of stock — should warn (or block)
        assert "stock" in responses[0].lower() or "agregado" in responses[0].lower()

    def test_add_without_qty_defaults_1(self, flow):
        responses = flow.process(_msg("agregar P002"))
        assert "Pantalón" in responses[0]

    def test_view_cart(self, flow):
        flow.process(_msg("agregar P001 2"))
        flow.process(_msg("agregar P002 1"))
        responses = flow.process(_msg("carrito"))
        assert "Camiseta" in responses[0]
        assert "Pantalón" in responses[0]
        assert "$65.00" in responses[0]  # 30 + 35

    def test_remove_from_cart(self, flow):
        flow.process(_msg("agregar P001 2"))
        responses = flow.process(_msg("quitar P001"))
        assert "quitado" in responses[0].lower() or "P001" in responses[0]


class TestCheckout:
    def test_checkout_creates_order(self, flow, store_with_products):
        flow.process(_msg("agregar P001 2"))
        responses = flow.process(_msg("confirmar"))
        assert "confirmado" in responses[0].lower() or "✅" in responses[0]
        assert "ORD-" in responses[0]
        orders = store_with_products.get_orders()
        assert len(orders) == 1
        assert orders[0].total == Decimal("30.00")

    def test_checkout_empty_cart_fails(self, flow):
        responses = flow.process(_msg("confirmar"))
        assert "vacío" in responses[0].lower() or "vacío" in responses[0]

    def test_cart_resets_after_checkout(self, flow):
        flow.process(_msg("agregar P001 2"))
        flow.process(_msg("confirmar"))
        # Cart should be empty now
        responses = flow.process(_msg("carrito"))
        assert "vacío" in responses[0].lower() or "vacío" in responses[0]


class TestSearch:
    def test_search_finds_matches(self, flow):
        responses = flow.process(_msg("buscar Camiseta"))
        assert "P001" in responses[0]
        assert "Camiseta" in responses[0]

    def test_search_no_match(self, flow):
        responses = flow.process(_msg("buscar XYZ123"))
        assert "no encontré" in responses[0].lower() or "No encontré" in responses[0]


class TestUnknownCommand:
    def test_unknown_returns_help_hint(self, flow):
        responses = flow.process(_msg("random text"))
        assert "menu" in responses[0].lower() or "ayuda" in responses[0].lower()
