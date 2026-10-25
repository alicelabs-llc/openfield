"""PriceWatch — Amazon scraper."""
from __future__ import annotations
import json
import re
from decimal import Decimal

import httpx
from bs4 import BeautifulSoup

from pricewatch.core.config import get_settings
from pricewatch.core.models import PricePoint, Store
from pricewatch.scrapers.base import BaseScraper


class AmazonScraper(BaseScraper):
    store = Store.AMAZON.value

    async def scrape(self, url: str) -> tuple[str, str, PricePoint]:
        s = get_settings()
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        }
        async with httpx.AsyncClient(timeout=s.request_timeout, follow_redirects=True, headers=headers) as client:
            r = await client.get(url)
            r.raise_for_status()
        html = r.text
        soup = BeautifulSoup(html, "lxml")

        name = ""
        image_url = ""
        price = Decimal("0")
        currency = "USD"
        in_stock = True

        # Title
        title_el = soup.find(id="productTitle")
        if title_el:
            name = title_el.get_text().strip()

        # Image
        img_el = soup.find(id="landingImage")
        if img_el:
            image_url = img_el.get("data-old-hires") or img_el.get("src", "")

        # JSON-LD
        ld_scripts = soup.find_all("script", type="application/ld+json")
        for script in ld_scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, list):
                    data = data[0]
                if data.get("@type") == "Product":
                    if not name:
                        name = data.get("name", "")
                    offers = data.get("offers", {})
                    if isinstance(offers, list):
                        offers = offers[0]
                    price = Decimal(str(offers.get("price", "0")))
                    currency = offers.get("priceCurrency", "USD")
                    break
            except (json.JSONDecodeError, KeyError, ValueError):
                continue

        # Fallback: scrape price from common Amazon classes
        if price == 0:
            price_el = soup.find(class_="a-price")
            if price_el:
                offscreen = price_el.find(class_="a-offscreen")
                if offscreen:
                    text = offscreen.get_text()
                    # Parse "$1,234.56" or "US$ 1.234,56" depending on locale
                    cleaned = re.sub(r"[^\d\.,]", "", text)
                    # Try US format
                    if "." in cleaned and "," in cleaned:
                        cleaned = cleaned.replace(",", "")
                    elif "," in cleaned and "." not in cleaned:
                        cleaned = cleaned.replace(",", ".")
                    try:
                        price = Decimal(cleaned)
                    except Exception:
                        pass

        # Stock
        if soup.find(id="outOfStock") or soup.find(class_="a-color-price", string=re.compile("unavailable", re.I)):
            in_stock = False

        # Original price
        original_price = None
        discount_percent = None
        old_price_el = soup.find(class_="a-text-price")
        if old_price_el:
            try:
                old_text = re.sub(r"[^\d\.,]", "", old_price_el.get_text())
                if "." in old_text and "," in old_text:
                    old_text = old_text.replace(",", "")
                elif "," in old_text and "." not in old_text:
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
