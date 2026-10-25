"""LicitAlert — Mexico CompraNet scraper.

Mexico's portal: https://www.gob.mx/compranet
"""
from __future__ import annotations
from datetime import datetime, timedelta
from decimal import Decimal
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from licitalert.core.models import Tender, Country, TenderStatus
from licitalert.scrapers.base import BaseScraper


class CompraNetScraper(BaseScraper):
    """CompraNet Mexico scraper."""

    country = Country.MEXICO.value
    BASE_URL = "https://imco.org.mx/compranet3/api/v1"
    # CompraNet open data via IMCO portal

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2, min=3, max=15))
    async def fetch_tenders(self, since_hours: int = 24) -> list[Tender]:
        """Fetch recent tenders from CompraNet (via IMCO API)."""
        since = datetime.utcnow() - timedelta(hours=since_hours)
        params = {
            "fecha_inicio": since.strftime("%Y-%m-%d"),
            "limit": 100,
        }
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                r = await client.get(f"{self.BASE_URL}/tendencias", params=params)
            if r.status_code != 200:
                return []
            data = r.json()
        except Exception:
            return []

        tenders = []
        items = data if isinstance(data, list) else data.get("results", [])
        for item in items:
            try:
                budget = None
                if item.get("importe"):
                    budget = Decimal(str(item["importe"]))

                published = None
                if item.get("fecha_publicacion"):
                    try:
                        published = datetime.fromisoformat(str(item["fecha_publicacion"]).replace("Z", "+00:00"))
                    except Exception:
                        pass

                tenders.append(Tender(
                    id=str(item.get("expediente", item.get("id", ""))),
                    country=Country.MEXICO,
                    title=item.get("titulo", "Sin título"),
                    description=item.get("descripcion", ""),
                    entity=item.get("dependencia", ""),
                    published_at=published,
                    budget=budget,
                    currency="MXN",
                    category=item.get("tipo_contratacion", ""),
                    modality=item.get("caracter", ""),
                    status=TenderStatus.OPEN,
                    url=f"https://www.gob.mx/compranet/expediente/{item.get('expediente','')}",
                ))
            except Exception:
                continue
        return tenders
