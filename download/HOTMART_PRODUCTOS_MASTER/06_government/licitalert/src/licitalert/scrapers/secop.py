"""LicitAlert — SECOP Colombia scraper (SECOP II API).

Uses the public Colombia Compra Eficiente API:
https://www.colombiacompra.gov.co/transparencia/api

Note: SECOP II has a REST API. This module queries it.
"""
from __future__ import annotations
from datetime import datetime, timedelta
from decimal import Decimal
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from licitalert.core.models import Tender, Country, TenderStatus
from licitalert.scrapers.base import BaseScraper


class SecopScraper(BaseScraper):
    """SECOP II Colombia scraper."""

    country = Country.COLOMBIA.value
    BASE_URL = "https://www.colombiacompra.gov.co/transparencia/api/SECOP2"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2, min=3, max=15))
    async def fetch_tenders(self, since_hours: int = 24) -> list[Tender]:
        """Fetch recent tenders from SECOP II."""
        since = datetime.utcnow() - timedelta(hours=since_hours)
        # Use the public API endpoint
        params = {
            "$filter": f"fecha_publicacion ge {since.strftime('%Y-%m-%dT00:00:00Z')}",
            "$top": 100,
            "$orderby": "fecha_publicacion desc",
        }
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                r = await client.get(f"{self.BASE_URL}/procesos", params=params)
            if r.status_code != 200:
                return []
            data = r.json()
        except Exception:
            return []

        tenders = []
        for item in data.get("value", data) if isinstance(data, dict) else data:
            try:
                budget = None
                if item.get("valor_total_adjudicacion"):
                    budget = Decimal(str(item["valor_total_adjudicacion"]))
                elif item.get("cuantia_proceso"):
                    budget = Decimal(str(item["cuantia_proceso"]))

                published = None
                if item.get("fecha_publicacion"):
                    try:
                        published = datetime.fromisoformat(item["fecha_publicacion"].replace("Z", "+00:00"))
                    except Exception:
                        pass

                tenders.append(Tender(
                    id=item.get("id_del_proceso", item.get("id", "")),
                    country=Country.COLOMBIA,
                    title=item.get("nombre_del_proceso", "Sin título"),
                    description=item.get("descripcion_del_proceso", ""),
                    entity=item.get("nombre_entidad", ""),
                    entity_nit=item.get("nit_entidad", ""),
                    published_at=published,
                    budget=budget,
                    currency="COP",
                    category=item.get("tipo_de_contrato", ""),
                    modality=item.get("modalidad_de_contratacion", ""),
                    status=self._parse_status(item.get("estado_del_proceso", "")),
                    url=f"https://www.colombiacompra.gov.co/tienda-virtual-del-estado-colombiano/procurement/procurement-notices/{item.get('id_del_proceso','')}",
                ))
            except Exception:
                continue
        return tenders

    def _parse_status(self, status_text: str) -> TenderStatus:
        s = (status_text or "").lower()
        if "cerrado" in s or "closed" in s:
            return TenderStatus.CLOSED
        if "adjudicado" in s or "awarded" in s:
            return TenderStatus.AWARDED
        if "cancelado" in s or "cancelled" in s:
            return TenderStatus.CANCELLED
        if "abierto" in s or "open" in s or "convocado" in s:
            return TenderStatus.OPEN
        return TenderStatus.UNKNOWN
