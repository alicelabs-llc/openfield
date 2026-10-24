"""PriceWatch — Pydantic models."""
from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl


class Store(str, Enum):
    MERCADOLIBRE = "mercadolibre"
    AMAZON = "amazon"
    EBAY = "ebay"
    ALIEXPRESS = "aliexpress"


class AlertChannel(str, Enum):
    EMAIL = "email"
    TELEGRAM = "telegram"
    DISCORD = "discord"
    WEBHOOK = "webhook"


class AlertCondition(str, Enum):
    BELOW = "below"      # price drops below threshold
    ABOVE = "above"      # price rises above threshold
    DROP_PERCENT = "drop_percent"  # price drops X% from initial
    CHANGE = "change"    # any price change


class PricePoint(BaseModel):
    price: Decimal
    currency: str = "USD"
    original_price: Decimal | None = None  # before discount
    discount_percent: Decimal | None = None
    in_stock: bool = True
    captured_at: datetime = Field(default_factory=datetime.utcnow)


class Product(BaseModel):
    """A tracked product."""
    id: str = Field(default="", description="Internal ID (auto-generated)")
    url: str
    store: Store
    name: str = ""
    image_url: str = ""
    target_price: Decimal | None = None  # alert when price <= target
    alert_condition: AlertCondition = AlertCondition.BELOW
    alert_channels: list[AlertChannel] = Field(default_factory=lambda: [AlertChannel.EMAIL])
    alert_recipient: str = ""  # email/chat_id/webhook URL

    initial_price: Decimal | None = None
    last_price: Decimal | None = None
    price_history: list[PricePoint] = Field(default_factory=list)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_checked: datetime | None = None
    active: bool = True


class Alert(BaseModel):
    product_id: str
    product_name: str
    product_url: str
    old_price: Decimal
    new_price: Decimal
    condition: AlertCondition
    captured_at: datetime = Field(default_factory=datetime.utcnow)

    @property
    def price_diff(self) -> Decimal:
        return self.old_price - self.new_price

    @property
    def price_diff_percent(self) -> Decimal:
        if self.old_price == 0:
            return Decimal("0")
        return ((self.old_price - self.new_price) / self.old_price * 100).quantize(Decimal("0.01"))


class TrackRequest(BaseModel):
    """Inbound request to track a product."""
    url: str
    target_price: Decimal | None = None
    alert_condition: AlertCondition = AlertCondition.BELOW
    alert_channels: list[AlertChannel] = Field(default_factory=lambda: [AlertChannel.EMAIL])
    alert_recipient: str = ""
