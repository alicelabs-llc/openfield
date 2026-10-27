"""Generate FacturaPro diagrams."""
import os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.font_manager as fm
fm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

OUT = '/home/z/my-project/download/HOTMART_PRODUCTOS/facturapro/diagrams'
os.makedirs(OUT, exist_ok=True)

BG='#0a1424'; CARD='#0f1d35'; BORDER='#1f3057'; TEXT='#e6ecf5'; MUTED='#7a8aa8'
ACCENT='#5d8bff'; ACCENT2='#0af'; GOLD='#ffb020'; DANGER='#ff4d4f'

def box(ax, x, y, w, h, text, fc=CARD, ec=BORDER, tc=TEXT, fs=10, weight='bold'):
    b = FancyBboxPatch((x,y), w, h, boxstyle="round,pad=0.02", linewidth=1.5, facecolor=fc, edgecolor=ec)
    ax.add_patch(b)
    ax.text(x+w/2, y+h/2, text, ha='center', va='center', color=tc, fontsize=fs, weight=weight)

def arrow(ax, x1, y1, x2, y2, color=ACCENT, label=None):
    a = FancyArrowPatch((x1,y1), (x2,y2), arrowstyle='-|>', mutation_scale=18, color=color, linewidth=2)
    ax.add_patch(a)
    if label:
        ax.text((x1+x2)/2, (y1+y2)/2+0.15, label, ha='center', va='bottom', color=MUTED, fontsize=9)

# === Architecture ===
fig, ax = plt.subplots(figsize=(14, 8), facecolor=BG)
ax.set_facecolor(BG); ax.set_xlim(0,14); ax.set_ylim(0,8); ax.axis('off')

ax.text(7, 7.5, 'FacturaPro — Arquitectura', ha='center', color=TEXT, fontsize=20, weight='bold')
ax.text(7, 7.1, 'SRI Ecuador v2.34 + Mexico CFDI 4.0', ha='center', color=MUTED, fontsize=11)

box(ax, 5, 5.8, 4, 0.7, 'CLIENTE (CLI / curl / SDK)', fc='#1a2a4a', tc=ACCENT2, fs=10)
box(ax, 3.5, 4.4, 7, 0.9, 'FastAPI Server\nRoutes: /v1/factura/create, /sign, /send-sri, /stamp-pac, /authorize, /pdf', fc='#0d1b30', ec=ACCENT, fs=9)
arrow(ax, 7, 5.8, 7, 5.3, color=ACCENT)

# Modules
mods = [
    (0.5, 2.5, 2.4, 1.2, 'XML\nGenerator\n(generator.py)', 'SRI v2.34\nCFDI 4.0', GOLD),
    (3.2, 2.5, 2.4, 1.2, 'Signer\n(signer.py)', 'XAdES-EPES\nxmlsig + .p12', ACCENT),
    (5.9, 2.5, 2.4, 1.2, 'PDF\nGenerator\n(pdf/generator)', 'ReportLab\ntemplate', ACCENT2),
    (8.6, 2.5, 2.4, 1.2, 'SRI Client\n(sri_client.py)', 'SOAP\nreception+auth', GOLD),
    (11.3, 2.5, 2.4, 1.2, 'PAC Client\n(pac_client.py)', 'REST\nSW SAPIen', ACCENT2),
]
for x, y, w, h, t1, t2, c in mods:
    box(ax, x, y, w, h, f'{t1}\n\n{t2}', fc=CARD, ec=c, fs=9)
    arrow(ax, 7, 4.4, x+w/2, y+h, color='#3a4365')

# Bottom row
box(ax, 0.5, 0.3, 3, 0.6, '[CERT] .p12/.pfx', fc='#1a2a4a', tc=GOLD, fs=9)
box(ax, 3.7, 0.3, 3, 0.6, '[DATA] ~/.facturapro/data', fc='#1a2a4a', tc=ACCENT, fs=9)
box(ax, 6.9, 0.3, 3, 0.6, '[SRI] SOAP endpoints', fc='#1a2a4a', tc=GOLD, fs=9)
box(ax, 10.1, 0.3, 3.5, 0.6, '[PAC] REST API (Mexico)', fc='#1a2a4a', tc=ACCENT2, fs=9)

plt.savefig(f'{OUT}/architecture.png', dpi=160, facecolor=BG, bbox_inches='tight', pad_inches=0.2)
plt.close()
print(f'✓ {OUT}/architecture.png')

# === Flow ===
fig, ax = plt.subplots(figsize=(14, 5), facecolor=BG)
ax.set_facecolor(BG); ax.set_xlim(0,14); ax.set_ylim(0,5); ax.axis('off')

ax.text(7, 4.5, 'FacturaPro — Flujo completo de una factura', ha='center', color=TEXT, fontsize=18, weight='bold')

steps = [
    (0.3, '1\nCREATE\nfactura\n\nXML + PDF\n+ clave', '#1a2a4a', ACCENT2),
    (2.5, '2\nSIGN\nenvelope\n\nXAdES-EPES\n+ .p12', '#0d1b30', GOLD),
    (4.7, '3\nSEND SRI\no PAC\n\nSOAP/REST\nenvío', '#0d1b30', ACCENT),
    (6.9, '4\nSRI returns\nRECIBIDA\n\no rechazada\n+ mensajes', '#0d1b30', ACCENT2),
    (9.1, '5\nPOLL\nauthorize\n\nAUTORIZADO\n+ número', '#0d1b30', ACCENT),
    (11.3, '6\nDOWNLOAD\nPDF\n\nfactura\nfirmada', '#1a2a4a', GOLD),
]
for x, label, fc, ec in steps:
    box(ax, x, 1.2, 1.7, 2.3, label, fc=fc, ec=ec, fs=9)

arrows_xs = [(2.0,2.5),(4.2,4.7),(6.4,6.9),(8.6,9.1),(10.8,11.3)]
for x1,x2 in arrows_xs:
    arrow(ax, x1, 2.35, x2, 2.35, color=ACCENT)

ax.text(7, 0.3, 'Tiempo total: ~30 segundos (incluyendo SRI autorización async)', ha='center', color=MUTED, fontsize=10)

plt.savefig(f'{OUT}/flow.png', dpi=160, facecolor=BG, bbox_inches='tight', pad_inches=0.2)
plt.close()
print(f'✓ {OUT}/flow.png')

print('Done!')
