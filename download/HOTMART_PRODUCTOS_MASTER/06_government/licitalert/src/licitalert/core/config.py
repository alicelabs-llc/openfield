"""LicitAlert — Configuration."""
from __future__ import annotations
import os
from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8009, alias="PORT")
    debug: bool = Field(default=False, alias="DEBUG")

    # Countries to monitor (co, ec, mx)
    countries: str = Field(default="co,ec,mx", alias="COUNTRIES")

    # Scraping schedule
    check_interval_hours: int = Field(default=6, alias="CHECK_INTERVAL_HOURS")

    # Email
    smtp_host: str = Field(default="", alias="SMTP_HOST")
    smtp_port: int = Field(default=587, alias="SMTP_PORT")
    smtp_user: str = Field(default="", alias="SMTP_USER")
    smtp_password: str = Field(default="", alias="SMTP_PASSWORD")
    email_from: str = Field(default="", alias="EMAIL_FROM")

    # Telegram
    telegram_bot_token: str = Field(default="", alias="TELEGRAM_BOT_TOKEN")

    # Storage
    data_dir: str = Field(default="~/.licitalert/data", alias="DATA_DIR")
    cache_dir: str = Field(default="~/.licitalert/cache", alias="CACHE_DIR")

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
