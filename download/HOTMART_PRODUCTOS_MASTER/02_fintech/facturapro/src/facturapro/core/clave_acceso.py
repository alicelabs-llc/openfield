"""FacturaPro — Clave de acceso SRI Ecuador (49 dígitos).

Estructura:
- 8 dígitos: fecha (ddmmyyyy)
- 2 dígitos: tipo comprobante (01=factura)
- 2 dígitos: RUC tipo (ruc 13 → '01', cedula → '02')
- 13 dígitos: RUC emisor
- 3 dígitos: ambiente (1=pruebas, 2=producción)
- 1 dígito: serie (001-001 → uso 1)
- 9 dígitos: secuencial
- 8 dígitos: código numérico (aleatorio)
- 1 dígito: dígito verificador (módulo 11)
"""
from __future__ import annotations
from datetime import datetime
import random


def compute_dv(digits_48: str) -> int:
    """Compute check digit (module 11, SRI spec)."""
    if len(digits_48) != 48:
        raise ValueError(f"Need 48 digits, got {len(digits_48)}")
    weights = [2, 3, 4, 5, 6, 7] * 8  # 48 weights
    total = sum(int(d) * weights[i] for i, d in enumerate(reversed(digits_48)))
    rem = total % 11
    dv = 11 - rem
    if dv == 11:
        dv = 0
    elif dv == 10:
        dv = 1
    return dv


def generate_clave_acceso(
    fecha: datetime,
    tipo_comprobante: str,
    ruc: str,
    ambiente: str,
    secuencial: str,
    codigo_numerico: str | None = None,
) -> str:
    """Generate SRI clave de acceso (49 digits)."""
    fecha_str = fecha.strftime("%d%m%Y")
    if len(ruc) < 13:
        ruc = ruc.ljust(13, "0")
    tipo_doc = tipo_comprobante.zfill(2)[:2]
    sec = secuencial.zfill(9)[:9]
    cod_num = codigo_numerico or f"{random.randint(0, 99999999):08d}"
    base = (
        fecha_str +
        tipo_doc +
        "01" +            # tipo de identificación del emisor (01=ruc)
        ruc +
        ambiente +
        sec[:3] +         # serie (establecimiento)
        sec[3:6] +        # punto emisión
        sec               # secuencial
    )
    # Recalcular para asegurar 48 antes del DV
    base48 = base[:48]
    if len(base48) < 48:
        base48 = base48.ljust(48, "0")
    dv = compute_dv(base48)
    return base48 + str(dv)


def validate_clave_acceso(clave: str) -> bool:
    """Validate SRI clave de acceso."""
    if len(clave) != 49:
        return False
    if not clave.isdigit():
        return False
    return compute_dv(clave[:48]) == int(clave[-1])
