"""FacturaPro — SRI reception client (SOAP)."""
from __future__ import annotations
from lxml import etree
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential


RECEPCION_SOAP_ENVELOPE = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ec="http://ec.gob.sri.ws.recepcion">
   <soapenv:Header/>
   <soapenv:Body>
      <ec:enviarComprobante>
         <xml>{xml_base64}</xml>
      </ec:enviarComprobante>
   </soapenv:Body>
</soapenv:Envelope>"""

AUTORIZACION_SOAP_ENVELOPE = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ec="http://ec.gob.sri.ws.autorizacion">
   <soapenv:Header/>
   <soapenv:Body>
      <ec:autorizacionComprobante>
         <claveAccesoComprobante>{clave}</claveAccesoComprobante>
      </ec:autorizacionComprobante>
   </soapenv:Body>
</soapenv:Envelope>"""


class SRIResponse:
    def __init__(self, success: bool, mensajes: list[dict], estado: str = "RECIBIDA"):
        self.success = success
        self.mensajes = mensajes
        self.estado = estado

    def to_dict(self) -> dict:
        return {"success": self.success, "estado": self.estado, "mensajes": self.mensajes}


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def send_to_sri(xml_signed_b64: str, receipts_url: str, timeout: float = 30.0) -> SRIResponse:
    """Send signed XML to SRI recepcionComprobantesOffline."""
    body = RECEPCION_SOAP_ENVELOPE.replace("{xml_base64}", xml_signed_b64)
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.post(
            receipts_url,
            content=body,
            headers={"Content-Type": "text/xml; charset=utf-8", "SOAPAction": ""},
        )
    if r.status_code != 200:
        return SRIResponse(False, [{"error": f"HTTP {r.status_code}"}], "ERROR_HTTP")
    # Parse SOAP response
    try:
        root = etree.fromstring(r.content)
        ns = {"ns": "http://ec.gob.sri.ws.recepcion"}
        resp = root.find(".//ns:RespuestaSolicitud", ns)
        if resp is None:
            return SRIResponse(False, [{"error": "no RespuestaSolicitud"}], "ERROR_XML")
        estado = resp.find("ns:estado", ns)
        estado_text = estado.text if estado is not None else "UNKNOWN"
        mensajes = []
        comprobantes = resp.find("ns:comprobantes", ns)
        if comprobantes is not None:
            for c in comprobantes.findall("ns:comprobante", ns):
                clave = c.find("ns:claveAcceso", ns)
                m = c.find("ns:mensajes/ns:mensaje", ns)
                if m is not None:
                    mensajes.append({
                        "clave": clave.text if clave is not None else "",
                        "identificador": m.find("ns:identificador", ns).text if m.find("ns:identificador", ns) is not None else "",
                        "info_adicional": m.find("ns:informacionAdicional", ns).text if m.find("ns:informacionAdicional", ns) is not None else "",
                        "tipo": m.find("ns:tipo", ns).text if m.find("ns:tipo", ns) is not None else "",
                        "mensaje": m.find("ns:mensaje", ns).text if m.find("ns:mensaje", ns) is not None else "",
                    })
        success = estado_text == "RECIBIDA"
        return SRIResponse(success, mensajes, estado_text)
    except Exception as e:
        return SRIResponse(False, [{"error": str(e)}], "ERROR_PARSE")


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=2, min=3, max=30))
async def authorize_in_sri(clave_acceso: str, auth_url: str, timeout: float = 30.0) -> dict:
    """Poll SRI for authorization status of a clave de acceso."""
    body = AUTORIZACION_SOAP_ENVELOPE.replace("{clave}", clave_acceso)
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.post(
            auth_url,
            content=body,
            headers={"Content-Type": "text/xml; charset=utf-8", "SOAPAction": ""},
        )
    if r.status_code != 200:
        return {"success": False, "estado": "ERROR_HTTP", "code": r.status_code}
    root = etree.fromstring(r.content)
    ns = {"ns": "http://ec.gob.sri.ws.autorizacion"}
    resp = root.find(".//ns:RespuestaAutorizacionComprobante", ns)
    if resp is None:
        return {"success": False, "estado": "NO_RESPONSE"}
    autorizacion = resp.find("ns:autorizaciones/ns:autorizacion", ns)
    if autorizacion is None:
        return {"success": False, "estado": "PENDING"}
    estado = autorizacion.find("ns:estado", ns)
    estado_text = estado.text if estado is not None else "UNKNOWN"
    numero = autorizacion.find("ns:numeroAutorizacion", ns)
    return {
        "success": estado_text == "AUTORIZADO",
        "estado": estado_text,
        "numero_autorizacion": numero.text if numero is not None else "",
        "fecha_autorizacion": autorizacion.find("ns:fechaAutorizacion", ns).text if autorizacion.find("ns:fechaAutorizacion", ns) is not None else "",
    }
