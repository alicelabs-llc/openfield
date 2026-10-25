"""Tests for models."""
from decimal import Decimal
from datetime import datetime
import pytest

from pricewatch.core.models import (
    Product, PricePoint, Alert, Store, AlertCondition, AlertChannel
)


def test_pricepoint_defaults():
    pp = PricePoint(price=Decimal("99.99"))
    assert pp.price == Decimal("99.99")
    assert pp.currency == "USD"
    assert pp.in_stock is True


def test_product_defaults():
    p = Product(url="https://example.com", store=Store.AMAZON)
    assert p.active is True
    assert p.price_history == []
    assert p.last_price is None


def test_alert_price_diff():
    a = Alert(
        product_id="test",
        product_name="test",
        product_url="https://example.com",
        old_price=Decimal("100"),
        new_price=Decimal("80"),
        condition=AlertCondition.BELOW,
    )
    assert a.price_diff == Decimal("20")
    assert a.price_diff_percent == Decimal("20.00")


def test_alert_zero_old_price():
    a = Alert(
        product_id="test",
        product_name="test",
        product_url="https://example.com",
        old_price=Decimal("0"),
        new_price=Decimal("10"),
        condition=AlertCondition.CHANGE,
    )
    assert a.price_diff_percent == Decimal("0")
