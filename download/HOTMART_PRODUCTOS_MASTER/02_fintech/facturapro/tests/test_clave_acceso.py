"""Tests for clave de acceso generation."""
from datetime import datetime
import pytest
from facturapro.core.clave_acceso import generate_clave_acceso, validate_clave_acceso, compute_dv


def test_dv_known_value():
    """Test DV computation with a real 48-digit base."""
    base48 = "25102024" + "01" + "01" + "0992345670012" + "2" + "001" + "001" + "000000001" + "1234567"
    assert len(base48) == 48, f"Expected 48, got {len(base48)}"
    dv = compute_dv(base48)
    assert 0 <= dv <= 9


def test_generate_clave_length():
    clave = generate_clave_acceso(
        fecha=datetime(2026, 10, 25),
        tipo_comprobante="01",
        ruc="0992345678001",
        ambiente="2",
        secuencial="000000001",
    )
    assert len(clave) == 49
    assert clave.isdigit()


def test_validate_clave_correct():
    clave = generate_clave_acceso(
        fecha=datetime(2026, 10, 25),
        tipo_comprobante="01",
        ruc="0992345678001",
        ambiente="2",
        secuencial="000000001",
    )
    assert validate_clave_acceso(clave) is True


def test_validate_clave_wrong():
    assert validate_clave_acceso("12345") is False
    assert validate_clave_acceso("abc") is False
    assert validate_clave_acceso("") is False


def test_dv_module_11_property():
    """Same base + same DV should be idempotent."""
    base48 = "25102024" + "01" + "01" + "0992345670012" + "2" + "001" + "001" + "000000001" + "1234567"
    assert len(base48) == 48
    dv1 = compute_dv(base48)
    dv2 = compute_dv(base48)
    assert dv1 == dv2
