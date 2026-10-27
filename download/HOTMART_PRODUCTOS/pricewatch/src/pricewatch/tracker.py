"""PriceWatch — Tracker service (orchestrates scraping + alerts)."""
from __future__ import annotations
import asyncio
import uuid
from datetime import datetime
from decimal import Decimal
from pathlib import Path
import json

from pricewatch.core.config import get_settings
from pricewatch.core.models import (
    Product, PricePoint, Alert, AlertCondition, Store,
    TrackRequest,
)
from pricewatch.core.url_parser import detect_store, extract_product_id
from pricewatch.scrapers import get_scraper
from pricewatch.notifiers import send_alert


class Tracker:
    """Track products, check prices, fire alerts."""

    def __init__(self):
        self.settings = get_settings()
        self.products: dict[str, Product] = {}
        self._load()

    # ----- Persistence (simple JSON) -----

    @property
    def db_path(self) -> Path:
        return self.settings.data_path / "products.json"

    def _load(self):
        if self.db_path.exists():
            data = json.loads(self.db_path.read_text(encoding="utf-8"))
            for p_data in data:
                # Deserialize
                p_data["store"] = Store(p_data["store"])
                if p_data.get("alert_condition"):
                    p_data["alert_condition"] = AlertCondition(p_data["alert_condition"])
                if p_data.get("price_history"):
                    p_data["price_history"] = [
                        PricePoint(**pp) for pp in p_data["price_history"]
                    ]
                p_data["alert_channels"] = [c for c in p_data.get("alert_channels", ["email"])]
                self.products[p_data["id"]] = Product(**p_data)

    def _save(self):
        out = []
        for p in self.products.values():
            d = p.model_dump()
            d["store"] = p.store.value
            d["alert_condition"] = p.alert_condition.value
            d["alert_channels"] = [c.value if hasattr(c, "value") else c for c in p.alert_channels]
            out.append(d)
        self.db_path.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")

    # ----- CRUD -----

    def add(self, req: TrackRequest) -> Product:
        store = detect_store(req.url)
        store_id = extract_product_id(req.url, store)
        pid = f"{store.value}_{store_id}"
        if pid in self.products:
            # Update existing
            existing = self.products[pid]
            existing.target_price = req.target_price
            existing.alert_condition = req.alert_condition
            existing.alert_channels = req.alert_channels
            existing.alert_recipient = req.alert_recipient
            existing.active = True
            self._save()
            return existing

        p = Product(
            id=pid,
            url=req.url,
            store=store,
            target_price=req.target_price,
            alert_condition=req.alert_condition,
            alert_channels=req.alert_channels,
            alert_recipient=req.alert_recipient,
        )
        self.products[pid] = p
        self._save()
        return p

    def remove(self, product_id: str) -> bool:
        if product_id in self.products:
            del self.products[product_id]
            self._save()
            return True
        return False

    def list_all(self) -> list[Product]:
        return list(self.products.values())

    def get(self, product_id: str) -> Product | None:
        return self.products.get(product_id)

    # ----- Scraping -----

    async def check_all(self) -> list[Alert]:
        """Check all active products. Returns list of alerts fired."""
        alerts: list[Alert] = []
        tasks = [self.check_one(pid) for pid, p in self.products.items() if p.active]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for r in results:
            if isinstance(r, Alert):
                alerts.append(r)
            elif isinstance(r, Exception):
                pass  # log
        self._save()
        return alerts

    async def check_one(self, product_id: str) -> Alert | None:
        p = self.products.get(product_id)
        if not p or not p.active:
            return None

        scraper = get_scraper(p.store.value)
        try:
            name, image, pp = await scraper.scrape(p.url)
        except Exception as e:
            return None

        if name and name != p.name:
            p.name = name
        if image and image != p.image_url:
            p.image_url = image

        if not p.initial_price and pp.price > 0:
            p.initial_price = pp.price

        old_price = p.last_price
        p.last_price = pp.price
        p.price_history.append(pp)
        # Cap history to last 1000 points
        if len(p.price_history) > 1000:
            p.price_history = p.price_history[-1000:]
        p.last_checked = datetime.utcnow()

        # Check alert condition
        should_alert = False
        if old_price and old_price != pp.price:
            if p.alert_condition == AlertCondition.BELOW and p.target_price:
                should_alert = pp.price <= p.target_price
            elif p.alert_condition == AlertCondition.ABOVE and p.target_price:
                should_alert = pp.price >= p.target_price
            elif p.alert_condition == AlertCondition.DROP_PERCENT and p.initial_price:
                drop_pct = ((p.initial_price - pp.price) / p.initial_price) * 100
                should_alert = drop_pct >= (p.target_price or Decimal("10"))
            elif p.alert_condition == AlertCondition.CHANGE:
                should_alert = True

        if should_alert and old_price:
            alert = Alert(
                product_id=p.id,
                product_name=p.name or "(unknown)",
                product_url=p.url,
                old_price=old_price,
                new_price=pp.price,
                condition=p.alert_condition,
            )
            # Fire notifications
            channels = [c.value if hasattr(c, "value") else str(c) for c in p.alert_channels]
            try:
                await send_alert(alert, channels, p.alert_recipient)
            except Exception:
                pass
            return alert
        return None
