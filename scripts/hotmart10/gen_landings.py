# -*- coding: utf-8 -*-
"""Exporta el copy de landing de cada producto a Markdown listo para pegar en Hotmart."""
import os, sys
sys.path.insert(0, "/home/z/my-project/scripts/hotmart10")
from content_a import PRODUCTS_A
from content_b import PRODUCTS_B

OUT = "/home/z/my-project/download/HOTMART_10_PRODUCTOS/landings"
os.makedirs(OUT, exist_ok=True)

SLUGS = {
 1: ("02_WAOrder", "Bot de pedidos por WhatsApp"),
 2: ("03_FacturaEC", "Facturación electrónica SRI Ecuador"),
 3: ("04_LeadMiner", "Extractor de leads de Instagram"),
 4: ("05_PriceRadar", "Monitor de precios MercadoLibre"),
 5: ("06_ScamGuard", "Validador de URLs y tiendas falsas"),
 6: ("07_CitaYa", "Reservas por WhatsApp"),
 7: ("08_ReviewReply", "Respuestas IA a reseñas de Google"),
 8: ("09_PostFactory", "Contenido IA para redes locales"),
 9: ("10_MenuQR", "Carta digital QR + pedidos WhatsApp"),
 10: ("11_LicitAlert", "Alertas de licitaciones SERCOP"),
}

def render(p):
    cp = p["copy"]
    lines = []
    lines.append("# %s" % cp["headline"])
    lines.append("")
    lines.append("%s" % cp["sub"])
    lines.append("")
    lines.append("## Qué obtienes")
    for b in cp["bullets"]:
        lines.append("- %s" % b)
    lines.append("")
    lines.append("## ¿Es para ti?")
    lines.append(cp["para_quien"])
    lines.append("")
    lines.append("## La oferta incluye")
    for i in cp["incluye"]:
        lines.append("- %s" % i)
    lines.append("")
    lines.append("## Garantía")
    lines.append(cp["garantia"])
    lines.append("")
    lines.append("## Preguntas frecuentes")
    for q, a in cp["faq"]:
        lines.append("**%s**" % q)
        lines.append("")
        lines.append(a)
        lines.append("")
    lines.append("## Llamado a la acción")
    lines.append("**%s**" % cp["cta"])
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Referencia interna (no publicar): competencia ancla: %s | precios Hotmart: %s | MVP: %s*"
                 % ("; ".join(c[0] for c in p["competitors"]), p["precio_hotmart"], p["esfuerzo"]))
    return "\n".join(lines)

for p in PRODUCTS_A + PRODUCTS_B:
    slug, _ = SLUGS[p["num"]]
    path = os.path.join(OUT, "%s.md" % slug)
    with open(path, "w", encoding="utf-8") as f:
        f.write(render(p))
    print("OK", path)
print("LISTO: 10 landings")
