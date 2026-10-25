"""ReviewReply AI — Models."""
from __future__ import annotations
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class Platform(str, Enum):
    GOOGLE_REVIEWS = "google_reviews"
    YELP = "yelp"
    APP_STORE = "app_store"
    TRUSTPILOT = "trustpilot"
    FACEBOOK = "facebook"
    AMAZON = "amazon"
    GENERIC = "generic"


class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    MIXED = "mixed"


class Review(BaseModel):
    id: str = ""
    platform: Platform = Platform.GENERIC
    author_name: str = ""
    author_avatar: str = ""
    rating: int = Field(..., ge=1, le=5)
    title: str = ""
    text: str = ""
    date: datetime | None = None
    business_response: str = ""  # existing response if any


class ReviewRequest(BaseModel):
    """Inbound: review to generate reply for."""
    platform: Platform = Platform.GENERIC
    author_name: str = ""
    rating: int = Field(..., ge=1, le=5)
    title: str = ""
    text: str = Field(..., min_length=1)
    language: str = ""
    business_context: str = ""  # extra context like "client bought X"


class ReplySuggestion(BaseModel):
    text: str
    tone: str
    sentiment_addressed: Sentiment
    word_count: int
    tokens_used: int = 0


class GeneratedReply(BaseModel):
    """Outbound: generated reply with multiple options."""
    review_id: str = ""
    review_summary: str = ""  # what was the review about
    detected_sentiment: Sentiment
    suggestions: list[ReplySuggestion] = Field(default_factory=list)
    recommended_index: int = 0
    model_used: str = ""
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class BatchRequest(BaseModel):
    reviews: list[ReviewRequest] = Field(..., min_length=1, max_length=50)
