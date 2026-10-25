"""FacturaPro — XML generators (SRI Ecuador esquema offline v2.34 + Mexico CFDI 4.0)."""
from __future__ import annotations
from datetime import datetime
from lxml import etree
from facturapro.core.models import Factura, TipoComprobante


# ============================================================
# ECUADOR — SRI esquema offline v2.34
# ============================================================

SRI_NS = "http://www.gob.ec/sri/empleo/esquema/factura"


def generate_factura_xml_sri(factura: Factura) -> str:
    """Generate SRI factura XML v2.34 (offline scheme)."""
    # Compute totals if not done
    if not factura.totales:
        factura.compute_totals()

    info_factura = etree.Element("factura", attrib={
        "id": "comprobante",
        "version": "2.0.0",
    })

    # infoTributaria
    info_trib = etree.SubElement(info_factura, "infoTributaria")
    etree.SubElement(info_trib, "ambiente").text = factura.emisor.ambiente
    etree.SubElement(info_trib, "tipoEmision").text = factura.emisor.tipo_emision
    etree.SubElement(info_trib, "razonSocial").text = factura.emisor.razon_social
    if factura.emisor.nombre_comercial:
        etree.SubElement(info_trib, "nombreComercial").text = factura.emisor.nombre_comercial
    etree.SubElement(info_trib, "ruc").text = factura.emisor.ruc
    etree.SubElement(info_trib, "claveAcceso").text = factura.clave_acceso
    etree.SubElement(info_trib, "codDoc").text = factura.tipo_comprobante.value
    etree.SubElement(info_trib, "estab").text = factura.secuencial[:3] if len(factura.secuencial) >= 3 else "001"
    etree.SubElement(info_trib, "ptoEmi").text = factura.secuencial[3:6] if len(factura.secuencial) >= 6 else "001"
    etree.SubElement(info_trib, "secuencial").text = factura.secuencial[-9:].zfill(9)
    etree.SubElement(info_trib, "dirMatriz").text = factura.emisor.direccion

    # infoFactura
    info_fac = etree.SubElement(info_factura, "infoFactura")
    etree.SubElement(info_fac, "fechaEmision").text = factura.fecha_emision.strftime("%d/%m/%Y")
    etree.SubElement(info_fac, "dirEstablecimiento").text = factura.emisor.direccion
    if factura.emisor.contribuyente_especial:
        etree.SubElement(info_fac, "contribuyenteEspecial").text = factura.emisor.contribuyente_especial
    etree.SubElement(info_fac, "obligadoContabilidad").text = "SI" if factura.emisor.obligado_contabilidad else "NO"

    # Tipo identificación comprador
    etree.SubElement(info_fac, "tipoIdentificacionComprador").text = factura.cliente.tipo_identificacion
    etree.SubElement(info_fac, "razonSocialComprador").text = factura.cliente.razon_social
    etree.SubElement(info_fac, "identificacionComprador").text = factura.cliente.ruc_cedula
    if factura.cliente.direccion:
        etree.SubElement(info_fac, "direccionComprador").text = factura.cliente.direccion

    # Totales
    t = factura.totales
    etree.SubElement(info_fac, "totalSinImpuestos").text = str(t.subtotal_sin_impuestos)
    etree.SubElement(info_fac, "totalDescuento").text = str(t.descuento_total)

    # totalConImpuestos
    imp = etree.SubElement(info_fac, "totalConImpuestos")
    if factura.impuestos and factura.impuestos.iva_valor > 0:
        iva_node = etree.SubElement(imp, "totalImpuesto")
        etree.SubElement(iva_node, "codigo").text = "2"
        etree.SubElement(iva_node, "codigoPorcentaje").text = "4"  # 4 = 15% Ecuador
        etree.SubElement(iva_node, "baseImponible").text = str(factura.impuestos.iva_base)
        etree.SubElement(iva_node, "valor").text = str(factura.impuestos.iva_valor)
    etree.SubElement(info_fac, "propina").text = "0.00"
    etree.SubElement(info_fac, "importeTotal").text = str(t.importe_total)
    etree.SubElement(info_fac, "moneda").text = "DOLAR"

    # Pagos
    pagos = etree.SubElement(info_fac, "pagos")
    pago = etree.SubElement(pagos, "pago")
    etree.SubElement(pago, "formaPago").text = "20"  # 20=otros
    etree.SubElement(pago, "total").text = str(t.importe_total)
    etree.SubElement(pago, "plazo").text = "0"
    etree.SubElement(pago, "unidadTiempo").text = "dias"

    # detalles
    dets = etree.SubElement(info_factura, "detalles")
    for d in factura.detalles:
        det = etree.SubElement(dets, "detalle")
        etree.SubElement(det, "codigoPrincipal").text = d.codigo_principal
        etree.SubElement(det, "descripcion").text = d.descripcion
        etree.SubElement(det, "cantidad").text = str(d.cantidad)
        etree.SubElement(det, "precioUnitario").text = str(d.precio_unitario)
        etree.SubElement(det, "descuento").text = str(d.descuento)
        etree.SubElement(det, "precioTotalSinImpuesto").text = str(d.subtotal)

        imp_det = etree.SubElement(det, "impuestos")
        if d.iva_tarifa > 0:
            imp_node = etree.SubElement(imp_det, "impuesto")
            etree.SubElement(imp_node, "codigo").text = "2"
            etree.SubElement(imp_node, "codigoPorcentaje").text = "4"
            etree.SubElement(imp_node, "tarifa").text = str(d.iva_tarifa)
            etree.SubElement(imp_node, "baseImponible").text = str(d.subtotal)
            etree.SubElement(imp_node, "valor").text = str(d.iva_valor)

    # infoAdicional
    if factura.cliente.email:
        info_ad = etree.SubElement(info_factura, "infoAdicional")
        campo = etree.SubElement(info_ad, "campoAdicional", attrib={"nombre": "email"})
        campo.text = factura.cliente.email

    # Pretty print
    xml_str = etree.tostring(info_factura, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    return xml_str.decode("utf-8")


# ============================================================
# MEXICO — CFDI 4.0 (Comprobante Fiscal Digital por Internet)
# ============================================================

def generate_cfdi_xml_4_0(factura: Factura) -> str:
    """Generate CFDI 4.0 XML (pre-PAC stamp)."""
    if not factura.totales:
        factura.compute_totals()

    # Namespace
    nsmap = {"cfdi": "http://www.sat.gob.mx/cfd/4"}
    root = etree.Element("{http://www.sat.gob.mx/cfd/4}Comprobante", attrib={
        "Version": "4.0",
        "Fecha": factura.fecha_emision.strftime("%Y-%m-%dT%H:%M:%S"),
        "Sello": "",  # filled by signer post-PAC
        "FormaPago": "99",
        "NoCertificado": "",
        "Certificado": "",
        "SubTotal": str(factura.totales.subtotal_sin_impuestos),
        "Moneda": "MXN",
        "Total": str(factura.totales.importe_total),
        "TipoDeComprobante": factura.tipo_comprobante.value,
        "Exportacion": "01",
        "LugarExpedicion": factura.emisor.lugar_expedicion or "29001",
    }, nsmap=nsmap)

    # Emisor
    emisor = etree.SubElement(root, "{http://www.sat.gob.mx/cfd/4}Emisor", attrib={
        "Rfc": factura.emisor.ruc,
        "Nombre": factura.emisor.razon_social,
        "RegimenFiscal": factura.emisor.regimen_fiscal or "601",
    })

    # Receptor
    receptor = etree.SubElement(root, "{http://www.sat.gob.mx/cfd/4}Receptor", attrib={
        "Rfc": factura.cliente.ruc_cedula,
        "Nombre": factura.cliente.razon_social,
        "DomicilioFiscalReceptor": factura.cliente.direccion or "29001",
        "RegimenFiscalReceptor": factura.cliente.regimen_fiscal_receptor or "616",
        "UsoCFDI": factura.cliente.uso_cfdi or "G01",
    })

    # Conceptos
    conceptos = etree.SubElement(root, "{http://www.sat.gob.mx/cfd/4}Conceptos")
    for d in factura.detalles:
        concepto = etree.SubElement(conceptos, "{http://www.sat.gob.mx/cfd/4}Concepto", attrib={
            "ClaveProdServ": "01010101",  # default genérico
            "Cantidad": str(d.cantidad),
            "ClaveUnidad": "ACT",  # actividad
            "Descripcion": d.descripcion,
            "ValorUnitario": str(d.precio_unitario),
            "Importe": str(d.subtotal),
            "ObjetoImp": "02",  # objeto de IVA
        })
        # Impuestos del concepto
        imp = etree.SubElement(concepto, "{http://www.sat.gob.mx/cfd/4}Impuestos")
        traslados = etree.SubElement(imp, "{http://www.sat.gob.mx/cfd/4}Traslados")
        etree.SubElement(traslados, "{http://www.sat.gob.mx/cfd/4}Traslado", attrib={
            "Base": str(d.subtotal),
            "Impuesto": "002",  # IVA
            "TipoFactor": "Tasa",
            "TasaOCuota": "0.16",
            "Importe": str(d.iva_valor),
        })

    # Impuestos globales
    imp_root = etree.SubElement(root, "{http://www.sat.gob.mx/cfd/4}Impuestos", attrib={
        "TotalImpuestosTrasladados": str(factura.totales.iva_total),
    })
    traslados_global = etree.SubElement(imp_root, "{http://www.sat.gob.mx/cfd/4}Traslados")
    etree.SubElement(traslados_global, "{http://www.sat.gob.mx/cfd/4}Traslado", attrib={
        "Impuesto": "002",
        "TipoFactor": "Tasa",
        "TasaOCuota": "0.16",
        "Importe": str(factura.totales.iva_total),
    })

    xml_str = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    return xml_str.decode("utf-8")


def generate_xml(factura: Factura, country: str = "ecuador") -> str:
    """Dispatch to country-specific generator."""
    if country.lower() == "mexico":
        return generate_cfdi_xml_4_0(factura)
    return generate_factura_xml_sri(factura)
