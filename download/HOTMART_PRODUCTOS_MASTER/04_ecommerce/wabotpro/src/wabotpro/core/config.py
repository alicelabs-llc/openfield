"""WhatsAppBot Pro — Configuration."""
from __future__ import annotations
import os
from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8004, alias="PORT")
    debug: bool = Field(default=False, alias="DEBUG")

    # WhatsApp Web (Baileys-like via websockets)
    wa_phone_number: str = Field(default="", alias="WA_PHONE_NUMBER")
    session_name: str = Field(default="wabotpro_session", alias="SESSION_NAME")
    session_dir: str = Field(default="~/.wabotpro/sessions", alias="SESSION_DIR")

    # Webhook (Meta Cloud API alternative)
    wa_verify_token: str = Field(default="", alias="WA_VERIFY_TOKEN")
    wa_access_token: str = Field(default="", alias="WA_ACCESS_TOKEN")
    wa_phone_number_id: str = Field(default="", alias="WA_PHONE_NUMBER_ID")
    wa_api_version: str = Field(default="v21.0", alias="WA_API_VERSION")

    # Business info
    business_name: str = Field(default="Mi Negocio", alias="BUSINESS_NAME")
    business_hours: str = Field(default="Lun-Vie 9-18h", alias="BUSINESS_HOURS")
    business_currency: str = Field(default="USD", alias="BUSINESS_CURRENCY")

    # Storage
    data_dir: str = Field(default="~/.wabotpro/data", alias="DATA_DIR")

    @property
    def data_path(self) -> Path:
        p = Path(os.path.expanduser(self.data_dir))
        p.mkdir(parents=True, exist_ok=True)
        return p


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


def reset_settings_cache() -> None:
    """Clear settings cache (used by tests)."""
    get_settings.cache_clear()
