"""PriceWatch — MercadoLibre scraper.

MercadoLibre product pages expose JSON-LD structured data with price.
This scraper parses the JSON-LD and falls back to meta tags.
"""
from __future__ import annotations
import json
import re
from decimal import Decimal
from urllib.parse import urlsplit

import httpx
from bs4 import BeautifulSoup

from pricewatch.core.config import get_settings
from pricewatch.core.models import PricePoint, Store
from pricewatch.scrapers.base import BaseScraper


class MercadoLibreScraper(BaseScraper):
    store = Store.MERCADOLIBRE.value

    async def scrape(self, url: str) -> tuple[str, str, PricePoint]:
        s = get_settings()
        async with httpx.AsyncClient(
            timeout=s.request_timeout,
            follow_redirects=True,
            headers={"User-Agent": s.user_agent, "Accept-Language": "es-419,es;q=0.9"},
        ) as client:
            r = await client.get(url)
            r.raise_for_status()
        html = r.text
        soup = BeautifulSoup(html, "lxml")

        # Method 1: JSON-LD structured data
        name = ""
        image_url = ""
        price = Decimal("0")
        currency = "USD"
        in_stock = True

        ld_scripts = soup.find_all("script", type="application/ld+json")
        for script in ld_scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, list):
                    data = data[0]
                if data.get("@type") in ("Product", "ItemPage"):
                    name = data.get("name", "")
                    offers = data.get("offers", {})
                    if isinstance(offers, list):
                        offers = offers[0]
                    price = Decimal(str(offers.get("price", "0")))
                    currency = offers.get("priceCurrency", "USD")
                    availability = offers.get("availability", "")
                    in_stock = "InStock" in availability
                    image_url = data.get("image", "")
                    if isinstance(image_url, list):
                        image_url = image_url[0] if image_url else ""
                    break
            except (json.JSONDecodeError, KeyError, ValueError):
                continue

        # Method 2: meta tags fallback
        if not name:
            og_title = soup.find("meta", property="og:title")
            if og_title:
                name = og_title.get("content", "")

        if price == 0:
            # Try meta price tag
            meta_price = soup.find("meta", itemprop="price")
            if meta_price:
                try:
                    price = Decimal(str(meta_price.get("content", "0")))
                except Exception:
                    pass

        if price == 0:
            # Try regex on common ML price pattern
            m = re.search(r'"price":\s*(\d+(?:\.\d+)?)', html)
            if m:
                price = Decimal(m.group(1))

        # Currency from URL (ML regional)
        host = urlsplit(url).netloc
        if "mercadolibre.com.ar" in host:
            currency = "ARS"
        elif "mercadolibre.com.mx" in host:
            currency = "MXN"
        elif "mercadolibre.com.co" in host:
            currency = "COP"
        elif "mercadolibre.com.ec" in host:
            currency = "USD"
        elif "mercadolibre.cl" in host:
            currency = "CLP"
        elif "mercadolibre.com.pe" in host:
            currency = "PEN"

        # Original price (before discount)
        original_price = None
        discount_percent = None
        # Look for discount markers
        old_price_el = soup.find(class_=re.compile("price-view__original", re.I))
        if not old_price_el:
            old_price_el = soup.find("s", class_=re.compile("price", re.I))
        if old_price_el:
            try:
                old_text = re.sub(r"[^\d,\.]", "", old_price_el.get_text())
                old_text = old_text.replace(",", ".")
                original_price = Decimal(old_text)
                if original_price > price and price > 0:
                    discount_percent = ((original_price - price) / original_price * 100).quantize(Decimal("0.1"))
            except Exception:
                pass

        return name, image_url, PricePoint(
            price=price,
            currency=currency,
            original_price=original_price,
            discount_percent=discount_percent,
            in_stock=in_stock,
        )
