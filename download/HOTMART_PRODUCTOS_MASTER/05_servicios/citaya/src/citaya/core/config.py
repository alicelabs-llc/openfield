"""CitaYa — Configuration."""
from __future__ import annotations
import os
from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8005, alias="PORT")
    debug: bool = Field(default=False, alias="DEBUG")

    business_name: str = Field(default="Mi Negocio", alias="BUSINESS_NAME")
    business_timezone: str = Field(default="America/Guayaquil", alias="BUSINESS_TIMEZONE")
    business_address: str = Field(default="", alias="BUSINESS_ADDRESS")
    business_phone: str = Field(default="", alias="BUSINESS_PHONE")
    business_email: str = Field(default="", alias="BUSINESS_EMAIL")

    # Slot config
    slot_duration_minutes: int = Field(default=30, alias="SLOT_DURATION_MINUTES")
    default_open_hour: int = Field(default=9, alias="DEFAULT_OPEN_HOUR")
    default_close_hour: int = Field(default=18, alias="DEFAULT_CLOSE_HOUR")
    work_days: str = Field(default="mon,tue,wed,thu,fri,sat", alias="WORK_DAYS")

    # Reminders (APScheduler)
    reminder_hours_before: int = Field(default=2, alias="REMINDER_HOURS_BEFORE")

    # Notifications
    smtp_host: str = Field(default="", alias="SMTP_HOST")
    smtp_port: int = Field(default=587, alias="SMTP_PORT")
    smtp_user: str = Field(default="", alias="SMTP_USER")
    smtp_password: str = Field(default="", alias="SMTP_PASSWORD")
    email_from: str = Field(default="", alias="EMAIL_FROM")
    telegram_bot_token: str = Field(default="", alias="TELEGRAM_BOT_TOKEN")
    whatsapp_access_token: str = Field(default="", alias="WA_ACCESS_TOKEN")

    data_dir: str = Field(default="~/.citaya/data", alias="DATA_DIR")

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
