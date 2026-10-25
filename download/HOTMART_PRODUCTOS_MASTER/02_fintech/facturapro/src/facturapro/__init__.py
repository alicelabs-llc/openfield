"""FacturaPro — Facturación electrónica SRI + CFDI 4.0 self-hosted."""

__version__ = "1.0.0"
__author__ = "Eddy Flores"

from facturapro.core.config import Settings, get_settings  # noqa: F401
from facturapro.core.models import (  # noqa: F401
    Factura, Cliente, Emisor, Detalle, Impuestos, Totales,
)

__all__ = ["__version__", "Settings", "get_settings",
           "Factura", "Cliente", "Emisor", "Detalle", "Impuestos", "Totales"]
