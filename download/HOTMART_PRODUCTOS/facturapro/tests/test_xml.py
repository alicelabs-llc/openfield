"""Tests for XML generation (Ecuador SRI + Mexico CFDI)."""
from decimal import Decimal
from datetime import datetime
import pytest
from lxml import etree

from facturapro.core.models import Factura, Cliente, Emisor, Detalle, TipoComprobante
from facturapro.xml import generate_xml, generate_factura_xml_sri, generate_cfdi_xml_4_0


@pytest.fixture
def sample_factura():
    emisor = Emisor(
        ruc="0992345678001",
        razon_social="MI EMPRESA",
        direccion="Av. Amazonas, Quito",
        ambiente="2",
        tipo_emision="1",
    )
    cliente = Cliente(
        ruc_cedula="1712345670001",
        razon_social="CLIENTE SAC",
        tipo_identificacion="04",
    )
    f = Factura(
        clave_acceso="251020240101001234567001200100100123456780000016",
        secuencial="001001000000001",
        tipo_comprobante=TipoComprobante.FACTURA,
        fecha_emision=datetime(2026, 10, 25),
        emisor=emisor,
        cliente=cliente,
        detalles=[
            Detalle(
                codigo_principal="P001",
                descripcion="Servicio",
                cantidad=Decimal("2"),
                precio_unitario=Decimal("100"),
                iva_tarifa=Decimal("15"),
            ),
        ],
    )
    f.compute_totals()
    return f


def test_generate_sri_xml_valid(sample_factura):
    xml = generate_xml(sample_factura, country="ecuador")
    assert "factura" in xml
    assert "infoTributaria" in xml
    assert "claveAcceso" in xml
    assert sample_factura.clave_acceso in xml
    # Parse XML to verify structure
    tree = etree.fromstring(xml.encode("utf-8"))
    assert tree.tag == "factura"
    info_trib = tree.find("infoTributaria")
    assert info_trib is not None
    assert info_trib.find("ruc").text == "0992345678001"


def test_generate_cfdi_xml_4_0(sample_factura):
    sample_factura.emisor.regimen_fiscal = "601"
    sample_factura.cliente.regimen_fiscal_receptor = "616"
    xml = generate_xml(sample_factura, country="mexico")
    assert "Comprobante" in xml
    assert "Version" in xml
    assert '"4.0"' in xml
    tree = etree.fromstring(xml.encode("utf-8"))
    assert tree.get("Version") == "4.0"
    assert tree.get("TipoDeComprobante") == "01"


def test_sri_xml_has_iva_15(sample_factura):
    xml = generate_xml(sample_factura, country="ecuador")
    # Ecuador IVA is 15% since 2024
    assert "15" in xml


def test_xml_is_well_formed(sample_factura):
    for country in ("ecuador", "mexico"):
        xml = generate_xml(sample_factura, country=country)
        # Should not raise
        etree.fromstring(xml.encode("utf-8"))
