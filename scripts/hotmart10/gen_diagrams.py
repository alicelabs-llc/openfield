# -*- coding: utf-8 -*-
"""Genera 10 diagramas de arquitectura (HTML -> PNG 2x) para el playbook Hotmart.
Estilo: familia azul Crystal Blue (Template 07), bandas Entrada/Nucleo/Gestion.
Reglas: <=8 nodos, 3 bandas, flechas solo entre bandas adyacentes (chips de flujo),
fills de baja saturacion, texto legible al incrustar (900px canvas -> 450pt).
"""
import os, json
from playwright.sync_api import sync_playwright

OUT = "/home/z/my-project/download/HOTMART_10_PRODUCTOS/diagramas"
os.makedirs(OUT, exist_ok=True)

CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family: 'Carlito','Liberation Sans',Arial,sans-serif; background:#f5f8fc; }
.canvas { width:900px; padding:26px 28px 30px; background:#f5f8fc; }
.band { background:#edf2f9; border:1px solid #c0d0e2; border-radius:12px; padding:14px 16px 16px; }
.band-label { font-size:12px; font-weight:700; letter-spacing:2.5px; color:#2d7ab3; text-transform:uppercase; margin-bottom:10px; }
.nodes { display:flex; flex-wrap:wrap; gap:12px; max-width:100%%; }
.node { flex:1 1 0; min-width:170px; max-width:100%%; background:#ffffff; border:1px solid #c0d0e2; border-radius:10px; padding:12px 14px; }
.node.core { border-left:4px solid #2d7ab3; }
.node h4 { font-size:17.5px; font-weight:700; color:#142840; line-height:1.25; margin-bottom:5px; }
.node p { font-size:13.5px; color:#5a7a96; line-height:1.35; overflow-wrap:break-word; }
.flow { display:flex; justify-content:center; align-items:center; gap:10px; padding:10px 0; }
.flow .arrow { width:0; height:0; border-left:9px solid transparent; border-right:9px solid transparent; border-top:11px solid #2d7ab3; }
.flow .chip { background:#ffffff; border:1px solid #c0d0e2; color:#1a4a7a; font-size:13.5px; font-weight:700; border-radius:999px; padding:4px 14px; }
"""

def band(label, nodes, core_idx=0):
    nds = []
    for i, (t, d) in enumerate(nodes):
        cls = "node core" if i == core_idx else "node"
        nds.append(f'<div class="{cls}"><h4>{t}</h4><p>{d}</p></div>')
    return f'<div class="band"><div class="band-label">{label}</div><div class="nodes">{"".join(nds)}</div></div>'

def flow(chip):
    return f'<div class="flow"><div class="chip">{chip}</div><div class="arrow"></div></div>'

def page(spec):
    parts = ['<div class="canvas">']
    parts.append(band("ENTRADAS", spec["b1"], spec.get("c1", 0)))
    parts.append(flow(spec["f1"]))
    parts.append(band("NÚCLEO DEL PRODUCTO", spec["b2"], spec.get("c2", 0)))
    parts.append(flow(spec["f2"]))
    parts.append(band("GESTIÓN Y SALIDAS", spec["b3"], spec.get("c3", 0)))
    parts.append('</div>')
    html = f"""<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">
<style>{CSS}</style></head><body>{''.join(parts)}</body></html>"""
    return html

SPECS = {
 "p01_waorder": {
  "b1": [("Clientes que compran por WhatsApp", "Piden sin apps ni registros: todo dentro del chat que ya usan."),
         ("Catálogo y carrito en el chat", "El bot muestra productos, precios y arma el pedido solo.")],
  "f1": "mensajes entrantes · respuesta en segundos",
  "b2": [("Bot Engine (FastAPI)", "Flujos de pedido, preguntas frecuentes con IA, asignación a humano si hace falta."),
         ("Cobro en el flujo", "Link de pago, transferencia o pago contra entrega confirmado en el chat.")],
  "f2": "pedido confirmado",
  "b3": [("Panel del negocio", "Pedidos del día, clientes frecuentes y horarios pico en un solo lugar."),
         ("Base de datos de pedidos y CRM", "Historial por cliente para reventa y promociones."),
         ("Alertas y recordatorios", "Aviso de nuevo pedido, confirmación de entrega y seguimiento.")]},
 "p02_facturaec": {
  "b1": [("Panel web del emisor", "Pensado para freelancers y pymes que facturan poco volumen pero todos los días."),
         ("Importación de clientes y productos", "Carga masiva por CSV/Excel; datos fiscales validados contra RUC.")],
  "f1": "comprobante a emitir",
  "b2": [("Motor de emisión (FastAPI)", "Facturas, notas de crédito y débito, retenciones y guías de remisión."),
         ("Firma XML XAdES", "Firma con el certificado digital .p12 del contribuyente, en navegador o servidor."),
         ("Cola de envío y reintentos", "Si el SRI responde ocupado, el sistema reintenta sin intervención humana.")],
  "f2": "XML firmado → autorización",
  "b3": [("WebServices del SRI", "Recepción y autorización oficial del comprobante electrónico."),
         ("Archivo XML y PDF en la nube", "Toda la documentación tributaria ordenada y descargable."),
         ("Entrega al cliente final", "Envío automático del PDF autorizado por email o WhatsApp.")]},
 "p03_leadminer": {
  "b1": [("Fuentes de captura", "Hashtags de nicho, seguidores de la competencia, ubicaciones y perfiles sugeridos.")],
  "f1": "perfiles objetivo",
  "b2": [("Motor de scraping", "Playwright + instagrapi para perfiles, posts y reels públicos."),
         ("Rotación de proxies y límites", "Ritmo humano, sesiones rotadas y reintentos para evitar bloqueos.")],
  "f2": "perfiles enriquecidos",
  "b3": [("Enriquecimiento de leads", "Email y teléfono públicos en bio, sitio web, tamaño de audiencia."),
         ("Filtros y scoring", "Filtra por país, nicho, tamaño y actividad para dejar solo leads calificados."),
         ("Export a donde se trabaja", "CSV, Google Sheets o push directo al CRM de la agencia.")]},
 "p04_priceradar": {
  "b1": [("URLs de la competencia", "Publicaciones de MercadoLibre y Amazon que el vendedor quiere vigilar."),
         ("Catálogo propio", "Lista de productos del vendedor a comparar contra el mercado.")],
  "f1": "rastreo programado",
  "b2": [("Crawler multi-marketplace", "Parsers dedicados por sitio con horarios configurables."),
         ("Match producto ↔ competencia", "Empareja automáticamente cada producto propio con sus rivales.")],
  "f2": "histórico de precios",
  "b3": [("Base de datos histórica", "Serie de precios y stock por publicación rival."),
         ("Alertas Telegram / email", "Aviso inmediato de baja de precio o quiebre de stock del rival."),
         ("Dashboard competitivo", "Índice de posición de precio y reglas sugeridas de reprecio.")]},
 "p05_scamguard": {
  "b1": [("URL sospechosa", "Llega desde la web pública, la API del partner o un mensaje revisado a mano.")],
  "f1": "verificación en vivo",
  "b2": [("Motor de señales", "Edad del dominio (WHOIS), Google Safe Browsing, blacklists, SSL y similitud de marca."),
         ("Scoring ponderado 0–100", "Combina señales en un veredicto explicable: seguro, dudoso o fraude.")],
  "f2": "veredicto con evidencia",
  "b3": [("Widget de veredicto", "Embebible en cualquier sitio o consultable por API."),
         ("Badge para comercios legítimos", "Sello de verificación que las tiendas reales muestran con orgullo."),
         ("Reporte por URL", "Evidencia punto por punto para decidir con datos.")]},
 "p06_citaya": {
  "b1": [("Reserva desde WhatsApp o link", "El cliente elige servicio, profesional y horario sin llamar."),
         ("Catálogo de servicios", "Duración, precio y profesionales por sucursal.")],
  "f1": "solicitud de cita",
  "b2": [("Motor de agenda (FastAPI)", "Disponibilidad en tiempo real, detección de conflictos y cupos."),
         ("Recordatorios automáticos", "Mensaje 24 horas y 1 hora antes para reducir ausencias.")],
  "f2": "cita agendada",
  "b3": [("Sincronización Google Calendar", "Dos vías: lo agendado en Google bloquea la agenda y viceversa."),
         ("Panel del negocio", "Servicios, horarios, comisiones por profesional y reportes del mes."),
         ("Anticipo contra cancelaciones", "Depósito o prepago opcional para proteger la agenda.")]},
 "p07_reviewreply": {
  "b1": [("Perfil de Google Business", "Uno o varios locales conectados con permisos de administrador."),
         ("Nuevas reseñas", "Positivas, neutrales y negativas detectadas por sondeo continuo.")],
  "f1": "reseña detectada",
  "b2": [("Generador con voz de marca", "IA que escribe en el tono del negocio y escala casos sensibles."),
         ("Reglas de aprobación", "Las positivas se publican solas; las críticas piden visto bueno.")],
  "f2": "respuesta lista para publicar",
  "b3": [("Aprobación en un clic", "Desde el panel o directamente por WhatsApp del dueño."),
         ("Publicación vía API GBP", "La respuesta queda visible en Google en segundos."),
         ("Reporte mensual de reputación", "Nota media, tiempos de respuesta y evolución por local.")]},
 "p08_postfactory": {
  "b1": [("Datos del negocio", "Catálogo, fotos reales, promociones del mes y fechas clave del barrio.")],
  "f1": "brief semanal",
  "b2": [("Generador de contenido IA", "Copys para IG/FB/TikTok con hashtags locales e imágenes de marca."),
         ("Calendario editorial", "Plan de publicaciones de la semana listo para aprobar.")],
  "f2": "pauta a aprobar",
  "b3": [("Aprobación del dueño", "Aprueba o edita cada post desde un chat de WhatsApp."),
         ("Autopublicación vía Meta API", "Se publica solo en el día y hora programados."),
         ("Métricas simples", "Alcance, guardados y mejores horarios, explicados sin jerga.")]},
 "p09_menuqr": {
  "b1": [("Comensal escanea el QR", "Cada mesa tiene su QR; abre la carta al instante, sin apps."),
         ("Carta web con fotos", "Fotos, descripciones, alérgenos y precios siempre actualizados.")],
  "f1": "pedido armado",
  "b2": [("Motor de pedidos", "Carrito por mesa, notas de cocina y propina opcional."),
         ("Puente a WhatsApp", "El pedido completo cae en el WhatsApp del restaurante, listo para confirmar.")],
  "f2": "pedido confirmado",
  "b3": [("Panel del restaurante", "Edita platos y precios al instante; la carta se actualiza sola."),
         ("Estados del pedido", "Cocina, en preparación y entregado, visibles para el equipo."),
         ("Estadísticas de venta", "Los platos más vendidos y las horas pico para decidir menú.")]},
 "p10_licitalert": {
  "b1": [("Portal público SERCOP", "Procesos de compra pública publicados, datos abiertos oficiales.")],
  "f1": "rastreo diario",
  "b2": [("Clasificador semántico", "Interpreta rubros NPU y detecta procesos que calzan con el perfil del proveedor."),
         ("Motor de alertas", "Filtra por monto, cantón y fecha de cierre; elimina duplicados.")],
  "f2": "oportunidad calificada",
  "b3": [("Alertas email / Telegram", "Notificación al momento de la publicación del proceso relevante."),
         ("Dashboard de oportunidades", "Pipeline con plazos, montos y estado de cada proceso."),
         ("Reportes de seguimiento", "Histórico de procesos vistos, presentados y adjudicados.")]},
}

HTMLS, PNGS = {}, {}
for name, spec in SPECS.items():
    html = page(spec)
    p_html = os.path.join(OUT, f"{name}.html")
    p_png = os.path.join(OUT, f"{name}.png")
    with open(p_html, "w", encoding="utf-8") as f:
        f.write(html)
    HTMLS[name], PNGS[name] = p_html, p_png

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    pg = browser.new_page(viewport={"width": 960, "height": 1400}, device_scale_factor=2)
    for name, p_html in HTMLS.items():
        pg.goto("file://" + p_html)
        pg.wait_for_timeout(120)
        el = pg.locator(".canvas")
        el.screenshot(path=PNGS[name])
        print("OK", name)
    browser.close()
print("LISTO:", len(PNGS), "diagramas")
