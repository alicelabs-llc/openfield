"""Tests for factura model and totals computation."""
from decimal import Decimal
from datetime import datetime
import pytest

from facturapro.core.models import (
    Factura, Cliente, Emisor, Detalle, TipoComprobante, Totales
)


@pytest.fixture
def sample_emisor():
    return Emisor(
        ruc="0992345678001",
        razon_social="MI EMPRESA SAC",
        nombre_comercial="Mi Empresa",
        direccion="Av. Amazonas N34-451, Quito",
        ambiente="2",
        tipo_emision="1",
    )


@pytest.fixture
def sample_cliente():
    return Cliente(
        ruc_cedula="171234567-001"[:13],
        razon_social="CLIENTE EJEMPLO CIA LTDA",
        tipo_identificacion="04",
        direccion="Guayaquil, Ecuador",
    )


@pytest.fixture
def sample_factura(sample_emisor, sample_cliente):
    return Factura(
        clave_acceso="251020240101001234567001200100100123456780000016",
        secuencial="001001000000001",
        tipo_comprobante=TipoComprobante.FACTURA,
        fecha_emision=datetime(2026, 10, 25, 10, 30),
        emisor=sample_emisor,
        cliente=sample_cliente,
        detalles=[
            Detalle(
                codigo_principal="P001",
                descripcion="Servicio de consultoría",
                cantidad=Decimal("10"),
                precio_unitario=Decimal("50.00"),
                iva_tarifa=Decimal("15"),
            ),
            Detalle(
                codigo_principal="P002",
                descripcion="Hardware server",
                cantidad=Decimal("2"),
                precio_unitario=Decimal("1200.00"),
                iva_tarifa=Decimal("15"),
            ),
        ],
    )


def test_detalle_subtotal():
    d = Detalle(
        codigo_principal="X",
        descripcion="Test",
        cantidad=Decimal("3"),
        precio_unitario=Decimal("100"),
        iva_tarifa=Decimal("15"),
    )
    assert d.subtotal == Decimal("300")
    assert d.iva_valor == Decimal("45.00")
    assert d.total == Decimal("345.00")


def test_factura_compute_totals(sample_factura):
    totals = sample_factura.compute_totals()
    # 10*50 = 500 + 2*1200 = 2400 → subtotal = 2900
    assert totals.subtotal_sin_impuestos == Decimal("2900.00")
    # IVA 15% of 2900 = 435
    assert totals.iva_total == Decimal("435.00")
    # Total = 2900 + 435 = 3335
    assert totals.importe_total == Decimal("3335.00")


def test_factura_empty_detalles_fails():
    with pytest.raises(ValueError):
        Factura(
            emisor=Emisor(ruc="1", razon_social="x"),
            cliente=Cliente(ruc_cedula="1", razon_social="y"),
            detalles=[],
        )


def test_factura_validate_detalles_positive():
    with pytest.raises(Exception):
        # cantidad must be > 0
        Detalle(codigo_principal="X", descripcion="Test",
                cantidad=Decimal("-1"), precio_unitario=Decimal("100"))
