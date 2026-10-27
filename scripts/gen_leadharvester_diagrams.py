"""Generate LeadHarvester diagrams."""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.font_manager as fm
fm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

OUT = '/home/z/my-project/download/HOTMART_PRODUCTOS/leadharvester/diagrams'
os.makedirs(OUT, exist_ok=True)

BG='#0a0e1a'; CARD='#131a2e'; BORDER='#26314f'; TEXT='#e6ecf5'; MUTED='#7a8aa8'
ACCENT='#ff5e9c'; ACCENT2='#a855f7'; GOLD='#ffb020'

def box(ax, x, y, w, h, text, fc=CARD, ec=BORDER, tc=TEXT, fs=10, weight='bold'):
    b = FancyBboxPatch((x,y), w, h, boxstyle="round,pad=0.02", linewidth=1.5, facecolor=fc, edgecolor=ec)
    ax.add_patch(b)
    ax.text(x+w/2, y+h/2, text, ha='center', va='center', color=tc, fontsize=fs, weight=weight)

def arrow(ax, x1, y1, x2, y2, color=ACCENT):
    a = FancyArrowPatch((x1,y1), (x2,y2), arrowstyle='-|>', mutation_scale=18, color=color, linewidth=2)
    ax.add_patch(a)

# Architecture
fig, ax = plt.subplots(figsize=(14, 8), facecolor=BG)
ax.set_facecolor(BG); ax.set_xlim(0,14); ax.set_ylim(0,8); ax.axis('off')

ax.text(7, 7.5, 'LeadHarvester — Arquitectura', ha='center', color=TEXT, fontsize=20, weight='bold')
ax.text(7, 7.1, 'Scraper de leads Instagram para agencias', ha='center', color=MUTED, fontsize=11)

box(ax, 5, 5.8, 4, 0.7, 'CLIENTE (CLI / curl / Web)', fc='#1a2a4a', tc=ACCENT2, fs=10)
box(ax, 3.5, 4.4, 7, 0.9, 'FastAPI Server\nPOST /v1/scrape → job_id → poll → export', fc='#0d1525', ec=ACCENT, fs=9)
arrow(ax, 7, 5.8, 7, 5.3, color=ACCENT)

# 3 modes
modes = [
    (0.5, 2.8, 2.5, 1, 'MODO 1\nusername\n\n1 perfil', GOLD),
    (3.3, 2.8, 2.5, 1, 'MODO 2\nhashtag\n\nN perfiles', ACCENT),
    (6.1, 2.8, 2.5, 1, 'MODO 3\nfollowers_of\n\nN seguidores', ACCENT2),
]
for x, y, w, h, t, c in modes:
    box(ax, x, y, w, h, t, fc=CARD, ec=c, fs=9)
    arrow(ax, 7, 4.4, x+w/2, y+h, color='#3a4365')

# Scraper
box(ax, 9.1, 2.8, 4, 1, 'InstagramScraper\n(Playwright + Chromium)\nsession persistente\n+ delays 2-5s', fc='#0d1525', ec=GOLD, fs=9)
arrow(ax, 7, 4.4, 11, 3.8, color='#3a4365')

# Extractors
box(ax, 0.5, 1.3, 4, 0.7, 'Extractores\nemail · phone · website · business · categoría', fc='#0d1525', ec=ACCENT, fs=9)

# Export
box(ax, 5, 1.3, 3, 0.7, 'Export\ncsv · json · excel', fc='#0d1525', ec=ACCENT2, fs=9)

# Output
box(ax, 8.5, 1.3, 4.5, 0.7, 'leads.xlsx/csv/json\n+ hoja Summary', fc='#1a2a4a', tc=ACCENT, fs=9)

arrow(ax, 3, 2.8, 3, 2.0, color=ACCENT)
arrow(ax, 7, 2.8, 6.5, 2.0, color=ACCENT2)
arrow(ax, 11, 2.8, 10, 2.0, color=ACCENT2)

# Storage
box(ax, 0.5, 0.2, 3, 0.6, '[IG session] json', fc='#1a2a4a', tc=GOLD, fs=9)
box(ax, 4, 0.2, 3, 0.6, '[DATA] state', fc='#1a2a4a', tc=ACCENT, fs=9)
box(ax, 7.5, 0.2, 3, 0.6, '[CACHE]', fc='#1a2a4a', tc=ACCENT2, fs=9)
box(ax, 11, 0.2, 2.5, 0.6, '[PROXY] optional', fc='#1a2a4a', tc=MUTED, fs=9)

plt.savefig(f'{OUT}/architecture.png', dpi=160, facecolor=BG, bbox_inches='tight', pad_inches=0.2)
plt.close()
print(f'✓ {OUT}/architecture.png')

# Flow
fig, ax = plt.subplots(figsize=(14, 4), facecolor=BG)
ax.set_facecolor(BG); ax.set_xlim(0,14); ax.set_ylim(0,4); ax.axis('off')
ax.text(7, 3.5, 'LeadHarvester — Flujo async', ha='center', color=TEXT, fontsize=18, weight='bold')

steps = [
    (0.3, '1\nPOST\n/v1/scrape', '#1a2a4a', ACCENT2),
    (2.5, '2\nServer crea\njob (async)', '#0d1525', ACCENT),
    (4.7, '3\nPlaywright\nscraps IG', '#0d1525', GOLD),
    (6.9, '4\nExtractors\n+ filter', '#0d1525', ACCENT),
    (9.1, '5\nExport\ncsv/json/xlsx', '#0d1525', ACCENT2),
    (11.3, '6\nDownload\nfile', '#1a2a4a', ACCENT),
]
for x, label, fc, ec in steps:
    box(ax, x, 1, 1.7, 1.8, label, fc=fc, ec=ec, fs=9)

for x1, x2 in [(2.0,2.5),(4.2,4.7),(6.4,6.9),(8.6,9.1),(10.8,11.3)]:
    arrow(ax, x1, 1.9, x2, 1.9, color=ACCENT)

plt.savefig(f'{OUT}/flow.png', dpi=160, facecolor=BG, bbox_inches='tight', pad_inches=0.2)
plt.close()
print(f'✓ {OUT}/flow.png')
print('Done!')
