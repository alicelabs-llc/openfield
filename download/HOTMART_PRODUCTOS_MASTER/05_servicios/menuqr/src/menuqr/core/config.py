"""MenuQR Pro — Configuration."""
from __future__ import annotations
import os
from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8008, alias="PORT")
    debug: bool = Field(default=False, alias="DEBUG")

    # Restaurant
    restaurant_name: str = Field(default="Mi Restaurante", alias="RESTAURANT_NAME")
    restaurant_logo_url: str = Field(default="", alias="RESTAURANT_LOGO_URL")
    restaurant_currency: str = Field(default="USD", alias="RESTAURANT_CURRENCY")
    restaurant_languages: str = Field(default="es,en", alias="RESTAURANT_LANGUAGES")
    restaurant_phone: str = Field(default="", alias="RESTAURANT_PHONE")
    restaurant_address: str = Field(default="", alias="RESTAURANT_ADDRESS")

    # QR generation
    qr_base_url: str = Field(default="http://localhost:8008", alias="QR_BASE_URL")
    qr_color: str = Field(default="#000000", alias="QR_COLOR")
    qr_bg_color: str = Field(default="#FFFFFF", alias="QR_BG_COLOR")

    # Storage
    data_dir: str = Field(default="~/.menuqr/data", alias="DATA_DIR")

    @property
    def data_path(self) -> Path:
        p = Path(os.path.expanduser(self.data_dir))
        p.mkdir(parents=True, exist_ok=True)
        return p


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


def reset_settings_cache() -> None:
    get_settings.cache_clear()
