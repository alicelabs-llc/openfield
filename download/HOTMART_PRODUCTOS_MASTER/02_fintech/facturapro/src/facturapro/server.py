"""FacturaPro — FastAPI server."""
from __future__ import annotations
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse, Response
from fastapi.security import APIKeyHeader
import base64
import io

from facturapro import __version__
from facturapro.core.config import get_settings
from facturapro.core.models import Factura, FacturaRequest, Emisor, TipoComprobante
from facturapro.core.clave_acceso import generate_clave_acceso
from facturapro.xml import generate_xml
from facturapro.xml.signer import wrap_with_xades_envelope, sign_xml
from facturapro.pdf import generate_pdf
from facturapro.api import send_to_sri, authorize_in_sri, stamp_with_pac

app = FastAPI(
    title="FacturaPro",
    description="Facturación electrónica SRI (Ecuador) + CFDI 4.0 (México) self-hosted",
    version=__version__,
    docs_url="/docs",
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

WEB_DIR = Path(__file__).parent.parent.parent / "web"


def _verify_key(provided: str | None) -> None:
    s = get_settings()
    if not s.cert_path:  # dev mode: no auth required
        return
    # In production we'd check a real API key; for now we allow
    pass


@app.get("/", response_class=HTMLResponse)
async def root():
    idx = WEB_DIR / "index.html"
    if idx.exists():
        return HTMLResponse(idx.read_text(encoding="utf-8"))
    return HTMLResponse(f"<h1>FacturaPro v{__version__}</h1>")


@app.get("/healthz")
async def healthz():
    s = get_settings()
    return {
        "status": "ok",
        "version": __version__,
        "country": s.country,
        "ambiente": "producción" if s.emisor_ambiente == "2" else "pruebas",
        "emisor_ruc": s.emisor_ruc or "no-configurado",
    }


@app.post("/v1/factura/create")
async def create_factura(req: FacturaRequest):
    """Create a factura draft: generates clave + XML + PDF (without sending)."""
    s = get_settings()
    emisor = Emisor(
        ruc=s.emisor_ruc,
        razon_social=s.emisor_razon_social,
        nombre_comercial=s.emisor_nombre_comercial,
        direccion=s.emisor_direccion,
        contribuyente_especial=s.emisor_contribuyente_especial,
        obligado_contabilidad=s.emisor_obligado_contabilidad,
        ambiente=s.emisor_ambiente,
        tipo_emision=s.emisor_tipo_emision,
        regimen_fiscal=s.emisor_regimen_fiscal,
    )

    # Generate sequential (in production this would be a DB sequence)
    secuencial = f"{datetime.utcnow().strftime('%H%M%S')}000"

    # Generate clave de acceso (Ecuador) or leave UUID empty for PAC (Mexico)
    clave = ""
    if s.country.lower() == "ecuador":
        clave = generate_clave_acceso(
            fecha=datetime.utcnow(),
            tipo_comprobante=req.tipo_comprobante.value,
            ruc=emisor.ruc,
            ambiente=emisor.ambiente,
            secuencial=secuencial,
        )

    factura = Factura(
        clave_acceso=clave,
        secuencial=secuencial,
        tipo_comprobante=req.tipo_comprobante,
        fecha_emision=datetime.utcnow(),
        emisor=emisor,
        cliente=req.cliente,
        detalles=req.detalles,
    )
    factura.compute_totals()

    # Generate XML
    xml = generate_xml(factura, country=s.country)

    # Save artifacts
    out_dir = s.data_path / "facturas" / factura.clave_acceso or factura.secuencial
    out_dir.mkdir(parents=True, exist_ok=True)
    xml_path = out_dir / "factura.xml"
    xml_path.write_text(xml, encoding="utf-8")

    # PDF
    pdf_path = out_dir / "factura.pdf"
    generate_pdf(factura, pdf_path)

    return {
        "clave_acceso": factura.clave_acceso,
        "secuencial": factura.secuencial,
        "totales": factura.totales.model_dump(),
        "xml_path": str(xml_path),
        "pdf_path": str(pdf_path),
        "xml_preview": xml[:500],
        "estado": "borrador",
    }


@app.post("/v1/factura/sign")
async def sign_factura(xml: str = None, key: str = Depends(api_key_header)):
    """Sign a factura XML with XAdES-EPES envelope."""
    s = get_settings()
    if not xml:
        raise HTTPException(400, "Missing XML body")
    envelope = wrap_with_xades_envelope(xml)
    if s.cert_path and s.cert_password:
        signed = sign_xml(envelope, s.cert_path, s.cert_password)
    else:
        # Dev mode — no signing
        signed = envelope
    return {"signed_xml": signed, "ambiente": s.emisor_ambiente}


@app.post("/v1/factura/send-sri")
async def send_factura_sri(xml_signed_b64: str = None, key: str = Depends(api_key_header)):
    """Send signed XML to SRI (Ecuador only)."""
    s = get_settings()
    if s.country.lower() != "ecuador":
        raise HTTPException(400, "Endpoint only for Ecuador")
    if not xml_signed_b64:
        raise HTTPException(400, "Missing xml_signed_b64")
    response = await send_to_sri(xml_signed_b64, s.sri_receipts_url)
    return response.to_dict()


@app.get("/v1/factura/authorize/{clave}")
async def authorize_factura(clave: str, key: str = Depends(api_key_header)):
    """Poll SRI for authorization status."""
    s = get_settings()
    return await authorize_in_sri(clave, s.sri_auth_url)


@app.post("/v1/factura/stamp-pac")
async def stamp_pac(xml_b64: str = None, key: str = Depends(api_key_header)):
    """Stamp XML with PAC (Mexico only)."""
    s = get_settings()
    if s.country.lower() != "mexico":
        raise HTTPException(400, "Endpoint only for Mexico")
    if not xml_b64:
        raise HTTPException(400, "Missing xml_b64")
    return await stamp_with_pac(xml_b64, s.pac_url, s.pac_user, s.pac_password)


@app.get("/v1/factura/pdf/{clave}")
async def download_pdf(clave: str):
    """Download PDF by clave de acceso."""
    s = get_settings()
    pdf_path = s.data_path / "facturas" / clave / "factura.pdf"
    if not pdf_path.exists():
        raise HTTPException(404, f"PDF not found for clave {clave}")
    return FileResponse(str(pdf_path), media_type="application/pdf",
                        filename=f"factura_{clave}.pdf")
