"""Tests for extractors (no network)."""
import pytest
from leadharvester.core.extractors import (
    extract_email, extract_phone, extract_website, is_business_bio, extract_category
)


class TestExtractEmail:
    def test_simple(self):
        assert extract_email("Contact: hola@empresa.com") == "hola@empresa.com"

    def test_obfuscated_at(self):
        assert extract_email("ventas [at] tienda dot com") == "ventas@tienda.com"

    def test_obfuscated_ar(self):
        assert extract_email("info [ar] ejemplo [punto] com") == "info@ejemplo.com"

    def test_no_email(self):
        assert extract_email("Sin contacto") == ""

    def test_empty(self):
        assert extract_email("") == ""

    def test_multiple_returns_first(self):
        result = extract_email("a@x.com b@y.com")
        assert result in ("a@x.com", "b@y.com")


class TestExtractPhone:
    def test_with_country_code(self):
        phone = extract_phone("+593 99 123 4567")
        assert phone.startswith("+593") or phone.startswith("593")

    def test_mexico_format(self):
        phone = extract_phone("+52 55 1234 5678")
        assert "55" in phone

    def test_no_phone(self):
        assert extract_phone("Sin teléfono") == ""


class TestIsBusinessBio:
    def test_venta(self):
        assert is_business_bio("Ventas de ropa y accesorios") is True

    def test_personal(self):
        assert is_business_bio("Just living life 🌴") is False

    def test_business_with_dm(self):
        assert is_business_bio("DM for orders 🛍️") is True


class TestExtractCategory:
    def test_restaurante(self):
        assert extract_category("El mejor restaurante de la ciudad") == "restaurante"

    def test_moda(self):
        assert extract_category("Tienda de moda femenina") == "moda"

    def test_no_category(self):
        assert extract_category("Random bio sin categoría") == ""


class TestExtractWebsite:
    def test_simple(self):
        url = extract_website("Visita https://mitienda.com")
        assert "mitienda.com" in url

    def test_skip_social(self):
        url = extract_website("Sígueme en https://instagram.com/yo")
        assert url == ""
