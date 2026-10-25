"""LeadHarvester — Pydantic models."""
from __future__ import annotations
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl


class LeadSource(str, Enum):
    INSTAGRAM = "instagram"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    TIKTOK = "tiktok"


class Lead(BaseModel):
    """A single lead extracted from a social profile."""
    username: str
    full_name: str = ""
    bio: str = ""
    profile_url: str = ""
    avatar_url: str = ""
    followers: int = 0
    following: int = 0
    posts_count: int = 0
    verified: bool = False
    is_business: bool = False
    category: str = ""  # business category if available
    email: str = ""
    phone: str = ""
    website: str = ""
    location: str = ""
    source: LeadSource = LeadSource.INSTAGRAM
    scraped_at: datetime = Field(default_factory=datetime.utcnow)


class LeadList(BaseModel):
    """A collection of leads with metadata."""
    name: str
    query: str = ""
    source: LeadSource = LeadSource.INSTAGRAM
    leads: list[Lead] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @property
    def count(self) -> int:
        return len(self.leads)

    @property
    def with_email(self) -> int:
        return sum(1 for l in self.leads if l.email)

    @property
    def with_phone(self) -> int:
        return sum(1 for l in self.leads if l.phone)

    @property
    def business_count(self) -> int:
        return sum(1 for l in self.leads if l.is_business)


class ScrapeRequest(BaseModel):
    """Inbound scrape request."""
    target: str = Field(..., description="Username, hashtag, or location")
    target_type: str = Field(default="username", description="username|hashtag|location|followers_of")
    max_results: int = Field(default=50, ge=1, le=500)
    extract_contact: bool = Field(default=True, description="Extract email/phone from bio")
    only_business: bool = Field(default=False, description="Only business accounts")


class ScrapeJob(BaseModel):
    job_id: str
    status: str = "pending"  # pending|running|completed|failed
    request: ScrapeRequest
    progress: int = 0  # 0-100
    leads: list[Lead] = Field(default_factory=list)
    error: str = ""
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: datetime | None = None
