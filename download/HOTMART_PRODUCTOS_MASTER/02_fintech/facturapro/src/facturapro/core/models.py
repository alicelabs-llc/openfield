"""FacturaPro — Pydantic models for invoices."""
from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, Field, field_validator


class TipoComprobante(str, Enum):
    FACTURA = "01"          # SRI: factura
    NOTA_CREDITO = "04"
    NOTA_DEBITO = "05"
    GUIA_REMISION = "06"
    COMPROBANTE_RETENCION = "07"
    # Mexico CFDI tipos
    INGRESO = "I"           # CFDI Ingreso (factura)
    EGRESO = "E"            # CFDI Egreso (nota de crédito)
    TRASLADO = "T"          # CFDI Traslado (traslado de bienes)
    NOMINA = "N"            # CFDI Nómina
    PAGO = "P"              # CFDI Recibo de pago


class Cliente(BaseModel):
    ruc_cedula: str = Field(..., description="RUC (13) o cédula (10) Ecuador / RFC (13) México")
    razon_social: str
    direccion: str = ""
    email: str = ""
    telefono: str = ""
    # Mexico-specific
    regimen_fiscal_receptor: str = ""
    uso_cfdi: str = "G01"   # default: adquisición mercancias
    # Ecuador-specific
    tipo_identificacion: str = Field(default="06", description="04=ruc 05=cedula 06=consumidor final 07=passport")


class Detalle(BaseModel):
    codigo_principal: str
    descripcion: str
    cantidad: Decimal = Field(default=Decimal("1"), gt=0)
    precio_unitario: Decimal = Field(..., gt=0)
    descuento: Decimal = Field(default=Decimal("0"), ge=0)
    # Ecuador: IVA 15% desde 2024; Mexico: 16% IVA
    iva_tarifa: Decimal = Field(default=Decimal("15"), description="Ecuador 15 / Mexico 16")
    iva_codigo: str = "2"   # SRI 2=IVA
    ice_tarifa: Decimal = Field(default=Decimal("0"))

    @property
    def subtotal(self) -> Decimal:
        return (self.cantidad * self.precio_unitario) - self.descuento

    @property
    def iva_valor(self) -> Decimal:
        return (self.subtotal * self.iva_tarifa / Decimal("100")).quantize(Decimal("0.01"))

    @property
    def total(self) -> Decimal:
        return self.subtotal + self.iva_valor


class Emisor(BaseModel):
    ruc: str
    razon_social: str
    nombre_comercial: str = ""
    direccion: str = ""
    contribuyente_especial: str = ""
    obligado_contabilidad: bool = True
    ambiente: str = "2"
    tipo_emision: str = "1"
    # Mexico
    regimen_fiscal: str = ""
    lugar_expedicion: str = ""


class Impuestos(BaseModel):
    iva_base: Decimal = Decimal("0")
    iva_tarifa: Decimal = Decimal("15")
    iva_valor: Decimal = Decimal("0")
    ice_valor: Decimal = Decimal("0")


class Totales(BaseModel):
    subtotal_sin_impuestos: Decimal = Decimal("0")
    descuento_total: Decimal = Decimal("0")
    iva_total: Decimal = Decimal("0")
    ice_total: Decimal = Decimal("0")
    importe_total: Decimal = Decimal("0")


class Factura(BaseModel):
    """Modelo unificado Ecuador/México."""
    # Identification
    clave_acceso: str = ""        # Ecuador: 49 dígitos
    uuid: str = ""                # Mexico: 36 dígitos CFDI
    secuencial: str = ""
    tipo_comprobante: TipoComprobante = TipoComprobante.FACTURA
    fecha_emision: datetime = Field(default_factory=datetime.utcnow)

    # Parties
    emisor: Emisor
    cliente: Cliente
    detalles: list[Detalle] = Field(..., min_length=1)

    # Computed
    impuestos: Impuestos | None = None
    totales: Totales | None = None

    # Status
    estado: str = Field(default="borrador", description="borrador|firmada|enviada|autorizada|rechazada")
    observaciones: str = ""

    @field_validator("detalles")
    @classmethod
    def validate_detalles(cls, v):
        if not v:
            raise ValueError("Debe tener al menos 1 detalle")
        return v

    def compute_totals(self) -> Totales:
        subtotal = sum((d.subtotal for d in self.detalles), Decimal("0"))
        descuento = sum((d.descuento for d in self.detalles), Decimal("0"))
        iva = sum((d.iva_valor for d in self.detalles), Decimal("0"))
        ice = sum((d.ice_tarifa * d.subtotal / Decimal("100") for d in self.detalles), Decimal("0"))
        total = subtotal + iva + ice
        self.totales = Totales(
            subtotal_sin_impuestos=subtotal.quantize(Decimal("0.01")),
            descuento_total=descuento.quantize(Decimal("0.01")),
            iva_total=iva.quantize(Decimal("0.01")),
            ice_total=ice.quantize(Decimal("0.01")),
            importe_total=total.quantize(Decimal("0.01")),
        )
        # Impuestos aggregate
        iva_base = sum((d.subtotal for d in self.detalles), Decimal("0"))
        self.impuestos = Impuestos(
            iva_base=iva_base.quantize(Decimal("0.01")),
            iva_tarifa=self.detalles[0].iva_tarifa,
            iva_valor=iva.quantize(Decimal("0.01")),
            ice_valor=ice.quantize(Decimal("0.01")),
        )
        return self.totales


class FacturaRequest(BaseModel):
    cliente: Cliente
    detalles: list[Detalle]
    tipo_comprobante: TipoComprobante = TipoComprobante.FACTURA
