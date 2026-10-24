"""PostFactory — Configuration."""
from __future__ import annotations
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8007, alias="PORT")
    debug: bool = Field(default=False, alias="DEBUG")

    # Brand
    brand_name: str = Field(default="Mi Marca", alias="BRAND_NAME")
    brand_voice: str = Field(default="profesional_amable", alias="BRAND_VOICE")
    brand_niche: str = Field(default="marketing", alias="BRAND_NICHE")
    brand_language: str = Field(default="es", alias="BRAND_LANGUAGE")

    # AI provider
    ai_provider: str = Field(default="zai", alias="AI_PROVIDER")
    ai_api_key: str = Field(default="", alias="AI_API_KEY")
    ai_model: str = Field(default="glm-4.6", alias="AI_MODEL")
    ai_api_url: str = Field(default="https://api.z.ai/api/paas/v4/chat/completions", alias="AI_API_URL")

    # Hashtag generation
    hashtag_count: int = Field(default=15, alias="HASHTAG_COUNT")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


def reset_settings_cache() -> None:
    get_settings.cache_clear()
