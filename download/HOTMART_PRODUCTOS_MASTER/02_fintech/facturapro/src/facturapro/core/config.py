"""FacturaPro — Configuration."""
from __future__ import annotations
import os
from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Server
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8001, alias="PORT")
    debug: bool = Field(default=False, alias="DEBUG")

    # Country regime: ecuador | mexico
    country: str = Field(default="ecuador", alias="COUNTRY")

    # Emisor (defaults — can be overridden per invoice)
    emisor_ruc: str = Field(default="", alias="EMISOR_RUC")
    emisor_razon_social: str = Field(default="", alias="EMISOR_RAZON_SOCIAL")
    emisor_nombre_comercial: str = Field(default="", alias="EMISOR_NOMBRE_COMERCIAL")
    emisor_direccion: str = Field(default="", alias="EMISOR_DIRECCION")
    emisor_contribuyente_especial: str = Field(default="", alias="EMISOR_CONTRIBUYENTE_ESPECIAL")
    emisor_obligado_contabilidad: bool = Field(default=True, alias="EMISOR_OBLIGADO_CONTABILIDAD")
    emisor_ambiente: str = Field(default="2", alias="EMISOR_AMBIENTE")  # 1=pruebas 2=producción
    emisor_tipo_emision: str = Field(default="1", alias="EMISOR_TIPO_EMISION")  # 1=normal

    # Mexico CFDI
    emisor_regimen_fiscal: str = Field(default="601", alias="EMISOR_REGIMEN_FISCAL")  # 601=general

    # Certificado digital (.p12 / .pfx)
    cert_path: str = Field(default="", alias="CERT_PATH")
    cert_password: str = Field(default="", alias="CERT_PASSWORD")

    # SRI endpoints
    sri_receipts_url: str = Field(
        default="https://cel.sri.gob.ec/comprobantes-electronicos-ws/RecepcionComprobantesOffline",
        alias="SRI_RECEIPTS_URL",
    )
    sri_auth_url: str = Field(
        default="https://cel.sri.gob.ec/comprobantes-electronicos-ws/AutorizacionComprobantesOffline",
        alias="SRI_AUTH_URL",
    )

    # Mexico PAC (must be configured by user)
    pac_url: str = Field(default="", alias="PAC_URL")
    pac_user: str = Field(default="", alias="PAC_USER")
    pac_password: str = Field(default="", alias="PAC_PASSWORD")

    # Storage
    data_dir: str = Field(default="~/.facturapro/data", alias="DATA_DIR")

    @property
    def data_path(self) -> Path:
        p = Path(os.path.expanduser(self.data_dir))
        p.mkdir(parents=True, exist_ok=True)
        return p


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
