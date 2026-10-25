"""WhatsAppBot Pro — Models."""
from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, Field


class MessageType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    BUTTON = "button"
    LIST = "list"
    CATALOG = "catalog"
    ORDER = "order"
    LOCATION = "location"


class Message(BaseModel):
    from_number: str
    to_number: str
    text: str = ""
    type: MessageType = MessageType.TEXT
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    media_url: str = ""
    buttons: list[dict] = Field(default_factory=list)
    raw: dict = Field(default_factory=dict)


class Product(BaseModel):
    id: str
    name: str
    description: str = ""
    price: Decimal = Field(..., gt=0)
    currency: str = "USD"
    image_url: str = ""
    category: str = ""
    stock: int = 0


class CartItem(BaseModel):
    product_id: str
    product_name: str
    quantity: int = Field(default=1, gt=0)
    unit_price: Decimal
    @property
    def subtotal(self) -> Decimal:
        return self.unit_price * self.quantity


class Order(BaseModel):
    id: str
    customer_number: str
    customer_name: str = ""
    items: list[CartItem] = Field(default_factory=list)
    status: str = "pending"  # pending|confirmed|shipped|delivered|cancelled
    notes: str = ""
    delivery_address: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = None

    @property
    def total(self) -> Decimal:
        return sum((i.subtotal for i in self.items), Decimal("0"))


class ConversationState(BaseModel):
    customer_number: str
    state: str = "start"  # start|browsing|cart|checkout|confirming|done
    cart: list[CartItem] = Field(default_factory=list)
    context: dict = Field(default_factory=dict)
    last_interaction: datetime = Field(default_factory=datetime.utcnow)


class IncomingWebhook(BaseModel):
    """Meta Cloud API webhook payload."""
    object: str = ""
    entry: list[dict] = Field(default_factory=list)
