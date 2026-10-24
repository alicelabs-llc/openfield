"""ReviewReply AI — Configuration."""
from __future__ import annotations
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8006, alias="PORT")
    debug: bool = Field(default=False, alias="DEBUG")

    # Business info (used in responses)
    business_name: str = Field(default="Mi Negocio", alias="BUSINESS_NAME")
    business_type: str = Field(default="tienda", alias="BUSINESS_TYPE")  # tienda/restaurante/clinica/hotel
    business_tone: str = Field(default="profesional_amable", alias="BUSINESS_TONE")  # profesional_amable/casual/lujoso/divertido
    business_language: str = Field(default="es", alias="BUSINESS_LANGUAGE")
    signature: str = Field(default="", alias="SIGNATURE")  # e.g. "— Equipo Mi Negocio"

    # AI provider: zai / openai / anthropic / local_ollama
    ai_provider: str = Field(default="zai", alias="AI_PROVIDER")
    ai_api_key: str = Field(default="", alias="AI_API_KEY")
    ai_model: str = Field(default="glm-4.6", alias="AI_MODEL")
    ai_api_url: str = Field(default="https://api.z.ai/api/paas/v4/chat/completions", alias="AI_API_URL")

    # Fallback templates
    cache_dir: str = Field(default="~/.reviewreply/cache", alias="CACHE_DIR")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


def reset_settings_cache() -> None:
    get_settings.cache_clear()
