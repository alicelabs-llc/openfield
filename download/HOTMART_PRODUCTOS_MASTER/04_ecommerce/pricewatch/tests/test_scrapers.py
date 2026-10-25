"""Tests for HTML parsing of ML/Amazon (with sample HTML)."""
from decimal import Decimal
import pytest
from pricewatch.scrapers.mercadolibre import MercadoLibreScraper
from pricewatch.scrapers.amazon import AmazonScraper


ML_SAMPLE_HTML = """
<html><head>
<script type="application/ld+json">
{"@type":"Product","name":"iPhone 15 128GB","image":"https://example.com/iphone.jpg",
 "offers":{"price":799.99,"priceCurrency":"USD","availability":"https://schema.org/InStock"}}
</script>
<meta property="og:title" content="iPhone 15 128GB">
</head><body></body></html>
"""


AMAZON_SAMPLE_HTML = """
<html><head></head><body>
<span id="productTitle">Apple AirPods Pro (2nd Gen)</span>
<img id="landingImage" data-old-hires="https://example.com/airpods.jpg">
<span class="a-price"><span class="a-offscreen">$249.00</span></span>
<span class="a-text-price">$299.00</span>
</body></html>
"""


def test_mercadolibre_json_ld_parsing(monkeypatch):
    """Test parsing JSON-LD from ML HTML."""
    async def fake_get(self, url):
        class R:
            text = ML_SAMPLE_HTML
            def raise_for_status(self): pass
        return R()
    monkeypatch.setattr("httpx.AsyncClient.get", fake_get)

    import asyncio
    scraper = MercadoLibreScraper()
    name, img, pp = asyncio.run(scraper.scrape("https://www.mercadolibre.com/ec/test"))
    assert "iPhone 15" in name
    assert pp.price == Decimal("799.99")
    assert pp.currency == "USD"
    assert pp.in_stock is True
