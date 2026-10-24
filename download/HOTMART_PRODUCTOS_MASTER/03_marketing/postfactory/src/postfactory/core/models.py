"""PostFactory — Models."""
from __future__ import annotations
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class Platform(str, Enum):
    INSTAGRAM = "instagram"
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    TIKTOK = "tiktok"
    FACEBOOK = "facebook"
    YOUTUBE = "youtube"
    BLOG = "blog"


class ContentType(str, Enum):
    EDUCATIONAL = "educational"
    PROMOTIONAL = "promotional"
    ENGAGEMENT = "engagement"
    STORYTELLING = "storytelling"
    BEHIND_SCENES = "behind_scenes"
    USER_GENERATED = "user_generated"
    NEWS = "news"
    INSPIRATIONAL = "inspirational"
    LISTICLE = "listicle"
    HOW_TO = "how_to"


class PostRequest(BaseModel):
    topic: str = Field(..., min_length=3, description="Topic or main theme")
    platform: Platform = Platform.INSTAGRAM
    content_type: ContentType = ContentType.EDUCATIONAL
    tone: str = "profesional_amable"
    target_audience: str = ""
    key_points: list[str] = Field(default_factory=list)
    call_to_action: str = ""
    brand_name: str = ""
    include_emojis: bool = True
    include_hashtags: bool = True
    language: str = "es"
    variations: int = Field(default=3, ge=1, le=5)


class Post(BaseModel):
    text: str
    platform: Platform
    content_type: ContentType
    hashtags: list[str] = Field(default_factory=list)
    emoji_count: int = 0
    word_count: int = 0
    char_count: int = 0
    suggested_image_prompt: str = ""
    best_posting_time: str = ""


class GeneratedContent(BaseModel):
    """Response: multiple post variations + extras."""
    posts: list[Post] = Field(default_factory=list)
    suggested_hashtags: list[str] = Field(default_factory=list)
    content_ideas: list[str] = Field(default_factory=list)
    content_calendar: list[dict] = Field(default_factory=list)
    model_used: str = ""
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class CalendarRequest(BaseModel):
    """Generate a content calendar for N days."""
    days: int = Field(default=7, ge=1, le=30)
    platforms: list[Platform] = Field(default_factory=lambda: [Platform.INSTAGRAM, Platform.LINKEDIN])
    topics: list[str] = Field(default_factory=list, description="Optional: if empty, auto-generated from niche")
