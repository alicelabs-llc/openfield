"""MenuQR Pro — Models."""
from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, Field


class Category(BaseModel):
    id: str
    name: str
    name_translations: dict[str, str] = Field(default_factory=dict)
    sort_order: int = 0


class MenuItem(BaseModel):
    id: str
    category_id: str
    name: str
    description: str = ""
    name_translations: dict[str, str] = Field(default_factory=dict)
    description_translations: dict[str, str] = Field(default_factory=dict)
    price: Decimal = Field(..., gt=0)
    currency: str = "USD"
    image_url: str = ""
    available: bool = True
    is_vegetarian: bool = False
    is_vegan: bool = False
    is_gluten_free: bool = False
    is_spicy: bool = False
    calories: int = 0
    sort_order: int = 0
    tags: list[str] = Field(default_factory=list)


class Menu(BaseModel):
    """A complete menu (categories + items)."""
    id: str
    restaurant_name: str
    categories: list[Category] = Field(default_factory=list)
    items: list[MenuItem] = Field(default_factory=list)
    language: str = "es"
    available_languages: list[str] = Field(default_factory=lambda: ["es", "en"])
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def get_by_category(self, category_id: str) -> list[MenuItem]:
        return [i for i in self.items if i.category_id == category_id and i.available]


class Table(BaseModel):
    """A restaurant table with its unique QR code."""
    id: str
    number: int
    name: str = ""
    capacity: int = 4
    location: str = ""  # interior/terraza/bar
    qr_code_id: str = ""
    active: bool = True


class Order(BaseModel):
    """An order placed from a table via QR."""
    id: str
    table_id: str
    table_number: int
    items: list[dict] = Field(default_factory=list)  # [{item_id, qty, notes}]
    status: str = "pending"  # pending|preparing|served|paid|cancelled
    total: Decimal = Decimal("0")
    currency: str = "USD"
    customer_notes: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    served_at: datetime | None = None


class MenuItemCreate(BaseModel):
    category_id: str
    name: str
    description: str = ""
    price: Decimal
    currency: str = "USD"
    is_vegetarian: bool = False
    is_vegan: bool = False
    is_gluten_free: bool = False
    is_spicy: bool = False


class TableCreate(BaseModel):
    number: int
    name: str = ""
    capacity: int = 4
    location: str = ""
