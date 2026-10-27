"""LicitAlert — Models."""
from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, Field


class Country(str, Enum):
    COLOMBIA = "co"
    ECUADOR = "ec"
    MEXICO = "mx"
    CHILE = "cl"
    PERU = "pe"


class TenderStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    AWARDED = "awarded"
    CANCELLED = "cancelled"
    UNKNOWN = "unknown"


class Tender(BaseModel):
    """A public procurement tender / licitación."""
    id: str
    country: Country
    title: str
    description: str = ""
    entity: str = ""  # entidad contratante
    entity_nit: str = ""  # NIT/RUC
    published_at: datetime | None = None
    deadline: datetime | None = None
    budget: Decimal | None = None
    currency: str = "USD"
    category: str = ""
    modality: str = ""  # licitación pública / selección abreviada / etc.
    status: TenderStatus = TenderStatus.OPEN
    url: str = ""
    documents: list[dict] = Field(default_factory=list)


class AlertRule(BaseModel):
    """User-defined alert rule."""
    id: str
    name: str
    countries: list[Country] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    exclude_keywords: list[str] = Field(default_factory=list)
    min_budget: Decimal | None = None
    max_budget: Decimal | None = None
    categories: list[str] = Field(default_factory=list)
    alert_channels: list[str] = Field(default_factory=lambda: ["email"])
    alert_recipient: str = ""
    active: bool = True


class TenderMatch(BaseModel):
    """A tender that matched an alert rule."""
    tender: Tender
    rule_id: str
    rule_name: str
    matched_keywords: list[str] = Field(default_factory=list)
    score: int = 0  # relevance score 0-100


class AlertRequest(BaseModel):
    """Inbound request to create an alert rule."""
    name: str
    countries: list[Country] = Field(default_factory=list)
    keywords: list[str]
    exclude_keywords: list[str] = Field(default_factory=list)
    min_budget: Decimal | None = None
    max_budget: Decimal | None = None
    categories: list[str] = Field(default_factory=list)
    alert_channels: list[str] = Field(default_factory=lambda: ["email"])
    alert_recipient: str
