"""LicitAlert — Base scraper."""
from __future__ import annotations
import abc
from licitalert.core.models import Tender


class BaseScraper(abc.ABC):
    """Abstract base for country-specific tender scrapers."""

    country: str = "base"

    @abc.abstractmethod
    async def fetch_tenders(self, since_hours: int = 24) -> list[Tender]:
        """Fetch tenders published in the last N hours."""
        raise NotImplementedError
