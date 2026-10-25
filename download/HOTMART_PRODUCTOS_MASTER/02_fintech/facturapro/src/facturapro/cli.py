"""FacturaPro — CLI."""
from __future__ import annotations
import json
import sys
from pathlib import Path
from datetime import datetime
from decimal import Decimal
import click
from rich.console import Console
from rich.table import Table
from rich import box

from facturapro import __version__
from facturapro.core.config import get_settings
from facturapro.core.models import (
    Factura, Cliente, Emisor, Detalle, TipoComprobante
)
from facturapro.core.clave_acceso import generate_clave_acceso, validate_clave_acceso
from facturapro.xml import generate_xml
from facturapro.xml.signer import wrap_with_xades_envelope, sign_xml
from facturapro.pdf import generate_pdf

console = Console()


@click.group()
@click.version_option(__version__, prog_name="facturapro")
def main():
    """FacturaPro — Facturación electrónica SRI + CFDI 4.0 self-hosted."""


@main.command()
def version():
    click.echo(f"FacturaPro v{__version__}")


@main.command()
def config():
    """Show current configuration."""
    s = get_settings()
    table = Table(title="Configuración", box=box.ROUNDED)
    table.add_column("Variable", style="bold")
    table.add_column("Valor")
    table.add_row("País", s.country)
    table.add_row("RUC emisor", s.emisor_ruc or "(no seteado)")
    table.add_row("Razón social", s.emisor_razon_social or "(no seteado)")
    table.add_row("Ambiente", "PRODUCCIÓN" if s.emisor_ambiente == "2" else "PRUEBAS")
    table.add_row("Certificado", s.cert_path or "(no seteado — dev mode)")
    table.add_row("Data dir", str(s.data_path))
    console.print(table)


@main.command()
@click.option("--ruc", prompt="RUC/cedula cliente")
@click.option("--razon", prompt="Razón social cliente")
@click.option("--detalle", prompt="Descripción del producto/servicio")
@click.option("--cantidad", type=float, default=1.0, prompt="Cantidad")
@click.option("--precio", type=float, prompt="Precio unitario (sin IVA)")
@click.option("--iva", type=float, default=15.0, help="Tarifa IVA (15=Ecuador, 16=México)")
@click.option("--out", "-o", type=click.Path(), default="factura.pdf", help="PDF output path")
def create(ruc, razon, detalle, cantidad, precio, iva, out):
    """Create a factura draft (XML + PDF)."""
    s = get_settings()
    emisor = Emisor(
        ruc=s.emisor_ruc or "9999999999999",
        razon_social=s.emisor_razon_social or "MI EMPRESA SAC",
        nombre_comercial=s.emisor_nombre_comercial or "",
        direccion=s.emisor_direccion or "Quito, Ecuador",
        ambiente=s.emisor_ambiente,
        tipo_emision=s.emisor_tipo_emision,
        obligado_contabilidad=s.emisor_obligado_contabilidad,
    )
    cliente = Cliente(
        ruc_cedula=ruc,
        razon_social=razon,
        tipo_identificacion="06" if len(ruc) == 10 else "04",
    )
    detalle_obj = Detalle(
        codigo_principal="001",
        descripcion=detalle,
        cantidad=Decimal(str(cantidad)),
        precio_unitario=Decimal(str(precio)),
        iva_tarifa=Decimal(str(iva)),
    )
    secuencial = f"{datetime.utcnow().strftime('%H%M%S')}001"
    clave = generate_clave_acceso(
        fecha=datetime.utcnow(),
        tipo_comprobante="01",
        ruc=emisor.ruc,
        ambiente=emisor.ambiente,
        secuencial=secuencial,
    ) if s.country.lower() == "ecuador" else ""

    factura = Factura(
        clave_acceso=clave,
        secuencial=secuencial,
        emisor=emisor,
        cliente=cliente,
        detalles=[detalle_obj],
    )
    factura.compute_totals()

    xml = generate_xml(factura, country=s.country)
    out_dir = Path(out).parent / "factura_out"
    out_dir.mkdir(parents=True, exist_ok=True)
    xml_path = out_dir / "factura.xml"
    xml_path.write_text(xml, encoding="utf-8")
    generate_pdf(factura, out)

    console.print(f"[green]✓ Factura creada[/green]")
    console.print(f"  Clave de acceso: {clave or '(CFDI: pendiente PAC)'}")
    console.print(f"  Secuencial: {secuencial}")
    console.print(f"  Total: ${factura.totales.importe_total}")
    console.print(f"  XML: {xml_path}")
    console.print(f"  PDF: {out}")


@main.command()
@click.argument("xml_path", type=click.Path(exists=True))
@click.option("--out", "-o", default="factura_signed.xml", help="Output signed XML")
def sign(xml_path, out):
    """Sign XML with XAdES envelope (uses cert from .env)."""
    s = get_settings()
    xml = Path(xml_path).read_text(encoding="utf-8")
    envelope = wrap_with_xades_envelope(xml)
    if s.cert_path and s.cert_password:
        signed = sign_xml(envelope, s.cert_path, s.cert_password)
    else:
        signed = envelope
        console.print("[yellow]⚠ Dev mode: XML not signed (no cert configured)[/yellow]")
    Path(out).write_text(signed, encoding="utf-8")
    console.print(f"[green]✓ Signed XML saved to {out}[/green]")


@main.command()
@click.argument("clave")
def validate_clave(clave):
    """Validate SRI clave de acceso."""
    if validate_clave_acceso(clave):
        console.print(f"[green]✓ Clave válida[/green]: {clave}")
    else:
        console.print(f"[red]✗ Clave inválida[/red]: {clave}")
        sys.exit(1)


@main.command()
@click.option("--host", default="0.0.0.0")
@click.option("--port", default=8001, type=int)
@click.option("--reload", is_flag=True)
def serve(host, port, reload):
    """Start FastAPI server."""
    import uvicorn
    uvicorn.run("facturapro.server:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    main()
