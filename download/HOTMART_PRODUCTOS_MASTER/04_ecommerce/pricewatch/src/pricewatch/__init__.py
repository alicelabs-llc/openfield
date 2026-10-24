"""PriceWatch — Monitor de precios MercadoLibre + Amazon."""
__version__ = "1.0.0"
__author__ = "Eddy Flores"

from pricewatch.core.config import Settings, get_settings  # noqa: F401
from pricewatch.core.models import Product, PricePoint, Alert, AlertChannel  # noqa: F401
