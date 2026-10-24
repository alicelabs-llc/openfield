# -*- coding: utf-8 -*-
"""Fusiona cover.pdf (Playwright) + body.pdf (ReportLab) en el PDF final."""
from pypdf import PdfReader, PdfWriter

A4_W, A4_H = 595.28, 841.89
COVER = "/home/z/my-project/scripts/hotmart10/cover.pdf"
BODY = "/home/z/my-project/scripts/hotmart10/body.pdf"
OUT = "/home/z/my-project/download/HOTMART_10_PRODUCTOS/PLAYBOOK_10_PRODUCTOS_HOTMART.pdf"

def normalize(page):
    w, h = float(page.mediabox.width), float(page.mediabox.height)
    if abs(w - A4_W) > 0.2 or abs(h - A4_H) > 0.2:
        page.scale_to(A4_W, A4_H)
        page.mediabox.lower_left = (0, 0)
        page.mediabox.upper_right = (A4_W, A4_H)
    return page

writer = PdfWriter()
writer.add_page(normalize(PdfReader(COVER).pages[0]))
for pg in PdfReader(BODY).pages:
    writer.add_page(normalize(pg))
writer.add_metadata({
    "/Title": "10 Productos Que Si Venden en Hotmart - Playbook LATAM 2026",
    "/Author": "Z.ai",
    "/Creator": "Z.ai",
    "/Subject": "Playbook de 10 productos de software para vender en Hotmart (LATAM 2026)",
})
with open(OUT, "wb") as f:
    writer.write(f)
print("MERGED:", OUT, "| paginas:", len(writer.pages))
