"""PriceWatch — URL parsing utilities for store detection."""
from __future__ import annotations
from urllib.parse import urlsplit
from pricewatch.core.models import Store


def detect_store(url: str) -> Store:
    """Detect which store a URL belongs to."""
    host = urlsplit(url).netloc.lower()
    if "mercadolibre" in host or "mercadolivre" in host:
        return Store.MERCADOLIBRE
    if "amazon." in host:
        return Store.AMAZON
    if "ebay." in host:
        return Store.EBAY
    if "aliexpress." in host:
        return Store.ALIEXPRESS
    raise ValueError(f"Unknown store: {host}")


def extract_product_id(url: str, store: Store) -> str:
    """Extract the canonical product ID from a URL."""
    path = urlsplit(url).path
    if store == Store.MERCADOLIBRE:
        # /ML-123456789-/title  or  /p/MLB1234567890
        parts = path.split("/")
        for p in parts:
            if p.startswith(("ML", "MCO", "MLB", "MLM", "MLC", "MLM")):
                # ML ID format: "ML-123456789" or "MLB1234567890"
                # Take the ID + numeric portion before next "-..."
                if "-" in p:
                    # ML-123456789-some-title → ML-123456789
                    segments = p.split("-")
                    if len(segments) >= 2 and segments[1].isdigit():
                        return f"{segments[0]}-{segments[1]}"
                return p
        return path.strip("/")
    elif store == Store.AMAZON:
        # /dp/ASIN/  or  /gp/product/ASIN/
        if "/dp/" in path:
            return path.split("/dp/")[1].split("/")[0]
        if "/gp/product/" in path:
            return path.split("/gp/product/")[1].split("/")[0]
        return path.strip("/")
    elif store == Store.EBAY:
        # /itm/123456789012
        if "/itm/" in path:
            return path.split("/itm/")[1].split("/")[0].split("?")[0]
        return path.strip("/")
    elif store == Store.ALIEXPRESS:
        # /item/1234567890123.html
        if "/item/" in path:
            return path.split("/item/")[1].split(".")[0]
        return path.strip("/")
    return path.strip("/")
