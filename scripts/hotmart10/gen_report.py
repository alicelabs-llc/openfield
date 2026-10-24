# -*- coding: utf-8 -*-
"""Playbook: 10 Productos Que Si Venden En Hotmart - cuerpo ReportLab (ruta Report).
Paleta fija Template 07 Crystal Blue (documentada en typesetting/cover.md).
TOC automatico: TocDocTemplate + multiBuild. Numeracion: Cap 1..12 (portada/indice sin numero).
"""
import os, sys, hashlib

SKILL = "/home/z/my-project/skills/pdf"
sys.path.insert(0, os.path.join(SKILL, "scripts"))
sys.path.insert(0, "/home/z/my-project/scripts/hotmart10")

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                Table, TableStyle, Image, KeepTogether, CondPageBreak,
                                HRFlowable)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from PIL import Image as PILImage

from content_a import CH1, PRODUCTS_A
from content_b import PRODUCTS_B, CH12

PRODUCTS = PRODUCTS_A + PRODUCTS_B
BASE = "/home/z/my-project"
DIAG = os.path.join(BASE, "download/HOTMART_10_PRODUCTOS/diagramas")
OUT_BODY = os.path.join(BASE, "scripts/hotmart10/body.pdf")

# ---------- Fonts (solo las permitidas) ----------
FONT_DIR = "/usr/share/fonts"
pdfmetrics.registerFont(TTFont("NotoSerifSC", f"{FONT_DIR}/truetype/noto-serif-sc/NotoSerifSC-Regular.ttf"))
pdfmetrics.registerFont(TTFont("NotoSerifSC-Bold", f"{FONT_DIR}/truetype/noto-serif-sc/NotoSerifSC-Bold.ttf"))
pdfmetrics.registerFont(TTFont("FreeSerif", f"{FONT_DIR}/truetype/freefont/FreeSerif.ttf"))
pdfmetrics.registerFont(TTFont("FreeSerif-Bold", f"{FONT_DIR}/truetype/freefont/FreeSerifBold.ttf"))
pdfmetrics.registerFont(TTFont("FreeSerif-Italic", f"{FONT_DIR}/truetype/freefont/FreeSerifItalic.ttf"))
pdfmetrics.registerFont(TTFont("FreeSerif-BoldItalic", f"{FONT_DIR}/truetype/freefont/FreeSerifBoldItalic.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSans", f"{FONT_DIR}/truetype/dejavu/DejaVuSansMono.ttf"))
registerFontFamily("NotoSerifSC", normal="NotoSerifSC", bold="NotoSerifSC-Bold")
registerFontFamily("FreeSerif", normal="FreeSerif", bold="FreeSerif-Bold",
                   italic="FreeSerif-Italic", boldItalic="FreeSerif-BoldItalic")
registerFontFamily("DejaVuSans", normal="DejaVuSans", bold="DejaVuSans")

from pdf import install_font_fallback
install_font_fallback()

# ---------- Paleta fija Template 07 (typesetting/cover.md) ----------
PAGE_BG      = colors.HexColor("#f5f8fc")
SECTION_BG   = colors.HexColor("#edf2f9")
CARD_BG      = colors.HexColor("#e4ecf5")
TABLE_STRIPE = colors.HexColor("#eef3fa")
HEADER_FILL  = colors.HexColor("#1a4a7a")
BORDER       = colors.HexColor("#c0d0e2")
ACCENT       = colors.HexColor("#2d7ab3")
TEXT_PRIMARY = colors.HexColor("#142840")
TEXT_MUTED   = colors.HexColor("#5a7a96")
TABLE_HEADER_COLOR = HEADER_FILL
TABLE_ROW_EVEN = colors.white
TABLE_ROW_ODD  = TABLE_STRIPE

# ---------- Geometria ----------
MARGIN = 0.9 * inch
PAGE_W, PAGE_H = A4
AVAIL_W = PAGE_W - 2 * MARGIN
AVAIL_H = PAGE_H - 2 * MARGIN
H1_THRESHOLD = AVAIL_H * 0.25
MAX_KEEP = PAGE_H * 0.4

# ---------- Estilos ----------
def st(name, **kw):
    return ParagraphStyle(name=name, **kw)

body = st("Body", fontName="FreeSerif", fontSize=10.5, leading=16,
          alignment=TA_JUSTIFY, textColor=TEXT_PRIMARY, spaceAfter=8)
body_left = st("BodyL", parent=body, alignment=TA_LEFT)
h1s = st("H1", fontName="FreeSerif", fontSize=19, leading=24,
         textColor=HEADER_FILL, spaceBefore=6, spaceAfter=4)
h2s = st("H2", fontName="FreeSerif", fontSize=13.5, leading=18,
         textColor=TEXT_PRIMARY, spaceBefore=14, spaceAfter=6)
h3s = st("H3", fontName="FreeSerif", fontSize=11.5, leading=15,
         textColor=HEADER_FILL, spaceBefore=10, spaceAfter=4)
kick = st("Kicker", fontName="FreeSerif-Italic", fontSize=11, leading=15,
          textColor=TEXT_MUTED, spaceAfter=10)
bullet = st("Bullet", fontName="FreeSerif", fontSize=10.5, leading=15.5,
            alignment=TA_LEFT, textColor=TEXT_PRIMARY, leftIndent=16,
            bulletIndent=4, spaceAfter=3, bulletFontName="FreeSerif", bulletFontSize=10.5)
caption = st("Caption", fontName="FreeSerif", fontSize=8.5, leading=11,
             alignment=TA_CENTER, textColor=TEXT_MUTED, spaceBefore=3, spaceAfter=6)
quote = st("Quote", fontName="FreeSerif-Italic", fontSize=10.5, leading=16,
           leftIndent=24, textColor=TEXT_PRIMARY, spaceAfter=8)
cell = st("Cell", fontName="FreeSerif", fontSize=9, leading=12.5,
          alignment=TA_LEFT, textColor=TEXT_PRIMARY)
cell_c = st("CellC", parent=cell, alignment=TA_CENTER)
cell_h = st("CellH", fontName="FreeSerif", fontSize=9.5, leading=12.5,
            alignment=TA_CENTER, textColor=colors.white)
copy_head = st("CopyHead", fontName="FreeSerif", fontSize=14, leading=19,
               textColor=HEADER_FILL, spaceBefore=8, spaceAfter=6)
faq_q = st("FaqQ", fontName="FreeSerif", fontSize=10.5, leading=15,
           textColor=ACCENT, spaceBefore=6, spaceAfter=2)
stat_big = st("StatBig", fontName="FreeSerif", fontSize=19, leading=23,
              textColor=ACCENT, alignment=TA_CENTER)
stat_lab = st("StatLab", fontName="FreeSerif", fontSize=8.5, leading=11,
              textColor=TEXT_MUTED, alignment=TA_CENTER)
toc_title = st("TocTitle", fontName="FreeSerif", fontSize=19, leading=24,
               textColor=HEADER_FILL, spaceAfter=14)

# ---------- TOC ----------
class TocDocTemplate(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if hasattr(flowable, "bookmark_name"):
            level = getattr(flowable, "bookmark_level", 0)
            text = getattr(flowable, "bookmark_text", "")
            key = getattr(flowable, "bookmark_key", "")
            self.notify("TOCEntry", (level, text, self.page, key))

def add_heading(text, style, level=0):
    key = "h_%s" % hashlib.md5(text.encode()).hexdigest()[:8]
    p = Paragraph('<a name="%s"/><b>%s</b>' % (key, text), style)
    p.bookmark_name = key
    p.bookmark_level = level
    p.bookmark_text = text
    p.bookmark_key = key
    return p

def h1_block(text):
    """H1 con CondPageBreak + regla de acento (orphan prevention, sin PageBreak forzado)."""
    head = add_heading(text, h1s, level=0)
    rule = HRFlowable(width="100%", color=ACCENT, thickness=1.2,
                      spaceBefore=2, spaceAfter=10)
    return [CondPageBreak(H1_THRESHOLD), KeepTogether([head, rule])]

def safe_keep(elements):
    total = 0
    for el in elements:
        w, h = el.wrap(AVAIL_W, AVAIL_H)
        total += h
    if total <= MAX_KEEP:
        return [KeepTogether(elements)]
    elif len(elements) >= 2:
        return [KeepTogether(elements[:2])] + list(elements[2:])
    return list(elements)

def embed_image(path, max_w=None, max_h=None):
    max_w = max_w or AVAIL_W
    max_h = max_h or 265
    im = PILImage.open(path)
    ow, oh = im.size
    r = min(max_w / ow, max_h / oh, 1.0)
    return Image(path, width=ow * r, height=oh * r)

def make_table(head, rows, ratios, font=9, align_cols_center=()):
    cw = [r * AVAIL_W for r in ratios]
    hd = [Paragraph("<b>%s</b>" % h, cell_h) for h in head]
    data = [hd]
    for row in rows:
        line = []
        for i, c in enumerate(row):
            s = cell_c if i in align_cols_center else cell
            line.append(Paragraph(str(c), s))
        data.append(line)
    t = Table(data, colWidths=cw, hAlign="CENTER", repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER_COLOR),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        style.append(("BACKGROUND", (0, i), (-1, i),
                      TABLE_ROW_EVEN if i % 2 == 1 else TABLE_ROW_ODD))
    t.setStyle(TableStyle(style))
    return t

def ficha_table(p):
    head = ["Cliente objetivo", "Precio Hotmart", "Esfuerzo MVP", "Potencial"]
    row = [p["cliente"], p["precio_hotmart"], p["esfuerzo"], p["potencial"]]
    return make_table(head, [row], [0.42, 0.20, 0.16, 0.22], align_cols_center=(1, 2, 3))

def callout_row(stats):
    """Fila de 3 callouts de metricas (data-to-ink)."""
    cells, cw = [], (AVAIL_W - 24) / 3.0
    for big, lab in stats:
        inner = Table([[Paragraph("<b>%s</b>" % big, stat_big)],
                       [Paragraph(lab, stat_lab)]], colWidths=[cw])
        inner.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), CARD_BG),
            ("BOX", (0, 0), (-1, -1), 1, ACCENT),
            ("TOPPADDING", (0, 0), (-1, 0), 9), ("BOTTOMPADDING", (0, 1), (-1, 1), 9),
            ("TOPPADDING", (0, 1), (-1, 1), 2), ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        cells.append(inner)
    outer = Table([cells], colWidths=[cw + 8] * 3, hAlign="CENTER")
    outer.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return outer

def bullets(story, items):
    for it in items:
        story.append(Paragraph(it, bullet, bulletText="\u2022"))

def copy_block(story, cp):
    """Bloque de copy de landing, listo para pegar en Hotmart."""
    story.append(Paragraph("Landing lista para pegar en Hotmart", h2s))
    story.append(Paragraph("<b>%s</b>" % cp["headline"], copy_head))
    story.append(Paragraph(cp["sub"], quote))
    story.append(Paragraph("Beneficios que venden", h3s))
    bullets(story, cp["bullets"])
    story.append(Paragraph("Para quién es (y para quién no)", h3s))
    story.append(Paragraph(cp["para_quien"], body))
    story.append(Paragraph("Qué incluye la oferta", h3s))
    bullets(story, cp["incluye"])
    story.append(Paragraph("Garantía", h3s))
    story.append(Paragraph(cp["garantia"], body))
    story.append(Paragraph("Preguntas frecuentes", h3s))
    for q, a in cp["faq"]:
        story.append(Paragraph("<b>%s</b>" % q, faq_q))
        story.append(Paragraph(a, body_left))
    story.append(Paragraph("Llamado a la acción", h3s))
    story.append(Paragraph("<b>%s</b>" % cp["cta"], copy_head))

def product_chapter(story, p):
    story.extend(h1_block("%d. %s" % (p["num"] + 1, p["name"])))
    story.append(Paragraph(p["tagline"], kick))
    story.append(ficha_table(p))
    story.append(Spacer(1, 12))
    story.append(Paragraph("El dolor y el mercado", h2s))
    story.append(Paragraph(p["pain"], body))
    story.append(Paragraph(p["market"], body))
    story.append(Paragraph("Competidores verificados y el estilo que copiamos", h2s))
    story.append(make_table(["Plataforma", "Modelo", "Precio verificado", "Nota clave"],
                            p["competitors"], [0.20, 0.17, 0.21, 0.42]))
    story.append(Spacer(1, 10))
    story.append(Paragraph(p["estilo"], body))
    copy_block(story, p["copy"])
    story.append(Paragraph("Arquitectura del producto", h2s))
    img = embed_image(os.path.join(DIAG, "%s.png" % p["key"]))
    story.extend(safe_keep([img, Paragraph(
        "Figura %d - Arquitectura funcional de %s" % (p["num"], p["name"].split(" - ")[0]),
        caption)]))
    story.append(Paragraph("Stack técnico y fases hasta el MVP", h2s))
    story.append(Paragraph(p["stack"], body))
    story.append(make_table(["Fase", "Alcance"], p["fases"], [0.30, 0.70]))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Precios en Hotmart", h2s))
    story.append(make_table(["Plan", "Precio", "Qué incluye"], p["pricing"],
                            [0.22, 0.18, 0.60], align_cols_center=(1,)))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Plan de lanzamiento", h2s))
    story.append(Paragraph(p["launch"], body))
    story.append(Paragraph("<b>Riesgo y mitigación.</b> %s" % p["risk"], body))

# ---------- Header / Footer ----------
DOC_TITLE = "10 Productos Que Sí Venden en Hotmart - Playbook LATAM 2026"

def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("FreeSerif", 7.5)
    canvas.setFillColor(TEXT_MUTED)
    canvas.drawString(MARGIN, PAGE_H - 0.55 * inch, DOC_TITLE)
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(1.2)
    canvas.line(MARGIN, PAGE_H - 0.62 * inch, PAGE_W - MARGIN, PAGE_H - 0.62 * inch)
    canvas.setFont("FreeSerif", 9)
    canvas.drawCentredString(PAGE_W / 2.0, 0.5 * inch, str(doc.page))
    canvas.restoreState()

# ---------- Story ----------
story = []

toc = TableOfContents()
toc.levelStyles = [
    st("TOC0", fontName="FreeSerif", fontSize=11.5, leading=18, leftIndent=14,
       firstLineIndent=-14, textColor=TEXT_PRIMARY),
]
story.append(Paragraph("<b>Índice</b>", toc_title))
story.append(HRFlowable(width="100%", color=ACCENT, thickness=1.2, spaceAfter=12))
story.append(toc)
story.append(PageBreak())

# Capitulo 1
story.extend(h1_block("1. Resumen ejecutivo y matriz de oportunidad"))
story.append(Paragraph(CH1["intro"], body))
story.append(Paragraph(CH1["metodo"], body))
story.append(Paragraph("<b>La matriz completa</b>", h2s))
story.append(make_table(CH1["matriz_head"], CH1["matriz"],
                        [0.24, 0.19, 0.16, 0.17, 0.09, 0.15],
                        align_cols_center=(4,)))
story.append(Spacer(1, 6))
story.append(Paragraph(CH1["matriz_nota"], body))

# Capitulos 2-11
for p in PRODUCTS:
    story.append(Spacer(1, 12))
    product_chapter(story, p)

# Capitulo 12
story.append(Spacer(1, 12))
story.extend(h1_block("12. Plan maestro de lanzamiento en cuatro meses"))
story.append(Paragraph(CH12["intro"], body))
story.append(Paragraph("<b>Oleadas de ejecución</b>", h2s))
for titulo, texto in CH12["fases"]:
    story.append(Paragraph("<b>%s</b>" % titulo, h3s))
    story.append(Paragraph(texto, body))
story.append(Paragraph("<b>Sinergias técnicas: un esqueleto, diez productos</b>", h2s))
story.append(Paragraph(CH12["sinergias"], body))
story.append(Paragraph("<b>El embudo de Hotmart</b>", h2s))
story.append(Paragraph(CH12["funnel"], body))
story.append(Paragraph("<b>Proyección conservadora a 12 meses</b>", h2s))
story.append(callout_row([
    ("$3,000 MRR", "meta con 5 productos activos y 30 clientes de promedio"),
    ("~10%", "comisión de plataforma + pasarela sobre el ingreso bruto"),
    ("$20K-$35K", "resultado neto esperable del primer año completo"),
]))
story.append(Spacer(1, 10))
story.append(Paragraph(CH12["proyeccion"], body))
story.append(Paragraph("<b>Checklist de lanzamiento en Hotmart</b>", h2s))
bullets(story, CH12["checklist"])

# ---------- Build ----------
doc = TocDocTemplate(
    OUT_BODY, pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=MARGIN, bottomMargin=MARGIN,
    title=DOC_TITLE, author="Z.ai", creator="Z.ai",
    subject="Playbook de 10 productos de software para vender en Hotmart (LATAM 2026)",
)
doc.multiBuild(story, onFirstPage=on_page, onLaterPages=on_page)
print("BODY OK:", OUT_BODY)
