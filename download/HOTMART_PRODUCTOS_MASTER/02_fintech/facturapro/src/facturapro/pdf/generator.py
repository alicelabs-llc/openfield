"""FacturaPro — PDF generation using ReportLab."""
from __future__ import annotations
from decimal import Decimal
from io import BytesIO
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib.enums import TA_RIGHT
from facturapro.core.models import Factura


def _fmt(value: Decimal | float | str) -> str:
    if isinstance(value, Decimal):
        return f"{value:,.2f}"
    if isinstance(value, float):
        return f"{value:,.2f}"
    return str(value)


def generate_pdf(factura: Factura, output_path: str | Path) -> Path:
    """Generate a printable PDF representation of the factura."""
    if not factura.totales:
        factura.compute_totals()

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        str(buffer), pagesize=letter,
        leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=15 * mm, bottomMargin=15 * mm,
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("Title", parent=styles["Title"], fontSize=18, leading=22)
    small_style = ParagraphStyle("Small", parent=styles["Normal"], fontSize=9, leading=11)
    right_style = ParagraphStyle("Right", parent=styles["Normal"], fontSize=10, alignment=TA_RIGHT)

    story = []

    # Header
    story.append(Paragraph(f"<b>{factura.emisor.razon_social}</b>", title_style))
    story.append(Paragraph(f"RUC: {factura.emisor.ruc}", small_style))
    if factura.emisor.nombre_comercial:
        story.append(Paragraph(f"Nombre comercial: {factura.emisor.nombre_comercial}", small_style))
    story.append(Paragraph(f"Dirección: {factura.emisor.direccion}", small_style))
    story.append(Spacer(1, 6))

    # Invoice metadata
    story.append(Paragraph(f"<b>FACTURA No. {factura.secuencial or '—'}</b>", styles["Heading2"]))
    story.append(Paragraph(f"Clave de acceso: {factura.clave_acceso or '—'}", small_style))
    story.append(Paragraph(f"Fecha emisión: {factura.fecha_emision.strftime('%d/%m/%Y %H:%M')}", small_style))
    story.append(Spacer(1, 8))

    # Cliente
    story.append(Paragraph("<b>Cliente</b>", styles["Heading4"]))
    story.append(Paragraph(f"Razón social: {factura.cliente.razon_social}", small_style))
    story.append(Paragraph(f"Identificación: {factura.cliente.ruc_cedula}", small_style))
    if factura.cliente.direccion:
        story.append(Paragraph(f"Dirección: {factura.cliente.direccion}", small_style))
    if factura.cliente.email:
        story.append(Paragraph(f"Email: {factura.cliente.email}", small_style))
    story.append(Spacer(1, 12))

    # Detalles table
    header = ["Código", "Descripción", "Cant.", "P.Unit", "Desc.", "Subtotal"]
    rows = [header]
    for d in factura.detalles:
        rows.append([
            d.codigo_principal,
            Paragraph(d.descripcion, small_style),
            _fmt(d.cantidad),
            _fmt(d.precio_unitario),
            _fmt(d.descuento),
            _fmt(d.subtotal),
        ])
    # Totals rows
    rows.append(["", "", "", "", "Subtotal:", _fmt(factura.totales.subtotal_sin_impuestos)])
    rows.append(["", "", "", "", "Descuento total:", _fmt(factura.totales.descuento_total)])
    rows.append(["", "", "", "", "IVA:", _fmt(factura.totales.iva_total)])
    if factura.totales.ice_total > 0:
        rows.append(["", "", "", "", "ICE:", _fmt(factura.totales.ice_total)])
    rows.append(["", "", "", "", "TOTAL:", _fmt(factura.totales.importe_total)])

    table = Table(rows, colWidths=[22 * mm, 70 * mm, 15 * mm, 25 * mm, 22 * mm, 30 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#26314f")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (2, 0), (-1, -1), "RIGHT"),
        ("ALIGN", (0, 0), (1, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#f0f4ff")),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("BACKGROUND", (0, -2), (-1, -2), colors.HexColor("#f8f8f8")),
        ("BACKGROUND", (0, -3), (-1, -3), colors.HexColor("#f8f8f8")),
    ]))
    story.append(table)
    story.append(Spacer(1, 16))

    # Ambientes / status
    ambiente_label = "PRODUCCIÓN" if factura.emisor.ambiente == "2" else "PRUEBAS"
    story.append(Paragraph(f"Ambiente: {ambiente_label}", small_style))
    story.append(Paragraph(f"Tipo de emisión: {factura.emisor.tipo_emision}", small_style))
    story.append(Paragraph(f"Estado: {factura.estado.upper()}", small_style))

    if factura.observaciones:
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"<i>Observaciones: {factura.observaciones}</i>", small_style))

    doc.build(story)

    output_path.write_bytes(buffer.getvalue())
    return output_path
