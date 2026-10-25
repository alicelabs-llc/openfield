"""LeadHarvester — Configuration."""
from __future__ import annotations
import os
from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8002, alias="PORT")
    debug: bool = Field(default=False, alias="DEBUG")

    # Instagram scraping (Playwright login)
    ig_username: str = Field(default="", alias="IG_USERNAME")
    ig_password: str = Field(default="", alias="IG_PASSWORD")
    ig_session_file: str = Field(default="~/.leadharvester/ig_session.json", alias="IG_SESSION_FILE")

    # Scraping limits (be polite, avoid blocks)
    max_profiles_per_run: int = Field(default=200, alias="MAX_PROFILES_PER_RUN")
    delay_min_seconds: float = Field(default=2.0, alias="DELAY_MIN_SECONDS")
    delay_max_seconds: float = Field(default=5.0, alias="DELAY_MAX_SECONDS")

    # Storage
    data_dir: str = Field(default="~/.leadharvester/data", alias="DATA_DIR")
    cache_dir: str = Field(default="~/.leadharvester/cache", alias="CACHE_DIR")

    # Proxy (optional — for rotating IPs at scale)
    proxy_url: str = Field(default="", alias="PROXY_URL")

    # Export
    export_dir: str = Field(default="~/.leadharvester/exports", alias="EXPORT_DIR")

    @property
    def data_path(self) -> Path:
        p = Path(os.path.expanduser(self.data_dir))
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def export_path(self) -> Path:
        p = Path(os.path.expanduser(self.export_dir))
        p.mkdir(parents=True, exist_ok=True)
        return p


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
