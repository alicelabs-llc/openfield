"""PriceWatch — Configuration."""
from __future__ import annotations
import os
from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8003, alias="PORT")
    debug: bool = Field(default=False, alias="DEBUG")

    # Scraping
    user_agent: str = Field(
        default="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        alias="USER_AGENT",
    )
    request_timeout: float = Field(default=15.0, alias="REQUEST_TIMEOUT")
    delay_between_requests: float = Field(default=2.0, alias="DELAY_BETWEEN_REQUESTS")

    # Scheduler (cron)
    check_interval_minutes: int = Field(default=60, alias="CHECK_INTERVAL_MINUTES")

    # Email notifications (SMTP)
    smtp_host: str = Field(default="", alias="SMTP_HOST")
    smtp_port: int = Field(default=587, alias="SMTP_PORT")
    smtp_user: str = Field(default="", alias="SMTP_USER")
    smtp_password: str = Field(default="", alias="SMTP_PASSWORD")
    email_from: str = Field(default="", alias="EMAIL_FROM")

    # Telegram notifications
    telegram_bot_token: str = Field(default="", alias="TELEGRAM_BOT_TOKEN")

    # Discord webhook
    discord_webhook_url: str = Field(default="", alias="DISCORD_WEBHOOK_URL")

    # Storage
    data_dir: str = Field(default="~/.pricewatch/data", alias="DATA_DIR")
    cache_dir: str = Field(default="~/.pricewatch/cache", alias="CACHE_DIR")

    @property
    def data_path(self) -> Path:
        p = Path(os.path.expanduser(self.data_dir))
        p.mkdir(parents=True, exist_ok=True)
        return p


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
