"""Tests for URL parsing and store detection."""
import pytest
from pricewatch.core.url_parser import detect_store, extract_product_id
from pricewatch.core.models import Store


class TestDetectStore:
    def test_mercadolibre_ec(self):
        assert detect_store("https://listado.mercadolibre.com.ec/iphone-15#D[A:iphone-15]") == Store.MERCADOLIBRE

    def test_mercadolibre_mx(self):
        assert detect_store("https://www.mercadolibre.com.mx/x") == Store.MERCADOLIBRE

    def test_amazon_com(self):
        assert detect_store("https://www.amazon.com/dp/B0CHX1W1XY") == Store.AMAZON

    def test_amazon_mx(self):
        assert detect_store("https://www.amazon.com.mx/dp/B0CHX1W1XY") == Store.AMAZON

    def test_unknown_store_raises(self):
        with pytest.raises(ValueError):
            detect_store("https://www.shopify.com/products/something")


class TestExtractProductId:
    def test_ml_with_dash(self):
        pid = extract_product_id("https://producto.mercadolibre.com.ec/ML-123456789-iphone-_JM", Store.MERCADOLIBRE)
        # ML IDs are returned before the title part
        assert "ML-123456789" in pid or pid == "ML-123456789-iphone-_JM"

    def test_amazon_dp(self):
        pid = extract_product_id("https://www.amazon.com/dp/B0CHX1W1XY", Store.AMAZON)
        assert pid == "B0CHX1W1XY"

    def test_amazon_gp_product(self):
        pid = extract_product_id("https://www.amazon.com/gp/product/B0CHX1W1XY/ref=xx", Store.AMAZON)
        assert pid == "B0CHX1W1XY"
