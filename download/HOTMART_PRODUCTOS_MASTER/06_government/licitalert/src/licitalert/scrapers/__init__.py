"""LicitAlert — Scrapers package."""
from licitalert.scrapers.base import BaseScraper  # noqa: F401
from licitalert.scrapers.secop import SecopScraper  # noqa: F401
from licitalert.scrapers.sercop import SerCopScraper  # noqa: F401
from licitalert.scrapers.compranet import CompraNetScraper  # noqa: F401


SCRAPERS = {
    "co": SecopScraper,
    "ec": SerCopScraper,
    "mx": CompraNetScraper,
}


def get_scraper(country_code: str) -> BaseScraper:
    cls = SCRAPERS.get(country_code.lower())
    if not cls:
        raise ValueError(f"No scraper for country: {country_code}")
    return cls()
