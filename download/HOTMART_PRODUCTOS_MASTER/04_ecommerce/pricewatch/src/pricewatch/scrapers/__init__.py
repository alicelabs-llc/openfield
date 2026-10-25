"""PriceWatch — Scrapers package."""
from pricewatch.scrapers.base import BaseScraper  # noqa: F401
from pricewatch.scrapers.mercadolibre import MercadoLibreScraper  # noqa: F401
from pricewatch.scrapers.amazon import AmazonScraper  # noqa: F401


SCRAPERS = {
    "mercadolibre": MercadoLibreScraper,
    "amazon": AmazonScraper,
}


def get_scraper(store: str) -> BaseScraper:
    cls = SCRAPERS.get(store)
    if not cls:
        raise ValueError(f"No scraper for store: {store}")
    return cls()
