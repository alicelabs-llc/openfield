"""PriceWatch — Base scraper interface."""
from __future__ import annotations
import abc
from pricewatch.core.models import PricePoint


class BaseScraper(abc.ABC):
    """Abstract base for store scrapers."""

    store: str = "base"

    @abc.abstractmethod
    async def scrape(self, url: str) -> tuple[str, str, PricePoint]:
        """Returns (product_name, image_url, price_point)."""
        raise NotImplementedError
