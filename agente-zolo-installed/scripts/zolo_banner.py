#!/usr/bin/env python3
# ============================================================
# ZOLO — Composición del banner oficial (Task 126, identidad ②)
# Fondo generado con IA + tipografía real (PIL) = texto perfecto.
# Uso: python3 scripts/zolo_banner.py
# ============================================================
from PIL import Image, ImageDraw, ImageFont

BG = "/home/z/my-project/download/zolo-brand/banner-bg.png"
OUT = "/home/z/my-project/download/zolo-brand/banner-zolo.png"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

ACCENT = (90, 172, 213)      # #5aacd5
WHITE = (225, 227, 228)      # #e1e3e4
DIM = (140, 148, 155)

bg = Image.open(BG).convert("RGBA")
# Center-crop a 2:1 y reescala al lienzo 1440x720 (el fondo es abstracto)
W, H = 1440, 720
sw, sh = bg.size
target_h = sw // 2
top = (sh - target_h) // 2
bg = bg.crop((0, top, sw, top + target_h)).resize((W, H), Image.LANCZOS)
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(overlay)

# Paleta de marca: familia 200° (dark/cold) — igual que la tarjeta de presentación
MARGEN = 112
MAX_W = W - 2 * MARGEN

def fuente_ajustada(texto, size_inicial, minimo=22):
    """Devuelve la fuente cuyo texto cabe en MAX_W (auto-fit)."""
    size = size_inicial
    while size > minimo:
        f = ImageFont.truetype(FONT_BOLD, size)
        bb = d.textbbox((0, 0), texto, font=f)
        if bb[2] - bb[0] <= MAX_W:
            return f, bb
        size -= 2
    return ImageFont.truetype(FONT_BOLD, minimo), d.textbbox((0, 0), texto, font=ImageFont.truetype(FONT_BOLD, minimo))

f_marca = ImageFont.truetype(FONT_BOLD, 190)
f_tag = ImageFont.truetype(FONT_BOLD, 44)
f_meta = ImageFont.truetype(FONT_BOLD, 30)

# Wordmark centrado-izquierdo
marca = "ZOLO"
bb = d.textbbox((0, 0), marca, font=f_marca)
mx, my = 110, 205
# Cursor-accent (firma visual de la tarjeta: cursor teal tras la marca)
cursor_x = mx + (bb[2] - bb[0]) + 28
d.rounded_rectangle([cursor_x, my + 18, cursor_x + 34, my + bb[3] - bb[1] - 6], radius=8, fill=ACCENT)
d.text((mx, my), marca, font=f_marca, fill=WHITE)

# Tagline (auto-fit al ancho seguro)
tag = "AGENTE AUTÓNOMO DE PRODUCCIÓN · AUTO-MEJORA CONTINUA"
f_tag, bb_tag = fuente_ajustada(tag, 44)
d.text((MARGEN, my + 240), tag, font=f_tag, fill=ACCENT)

# Meta (ecosistema, auto-fit)
meta = "AliceLabs · MarketNow · UTA        v6.0 AUTÓMATA · 33 reglas · 26 skills · E01-E55"
f_meta, _ = fuente_ajustada(meta, 30)
d.text((MARGEN, my + 310), meta, font=f_meta, fill=DIM)

# Barra inferior de acento
d.rectangle([0, H - 12, W, H], fill=ACCENT)

out = Image.alpha_composite(bg, overlay).convert("RGB")
out.save(OUT, "PNG")
print(f"OK banner → {OUT} ({out.size[0]}x{out.size[1]})")
