"""Generate architecture + flow diagrams for ScamShield Pro."""
import os
import matplotlib.font_manager as fm

# Register CJK + Latin fallback
fm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

OUT_DIR = '/home/z/my-project/download/HOTMART_PRODUCTOS/scamshield-pro/diagrams'
os.makedirs(OUT_DIR, exist_ok=True)

# Color palette (matches landing dark theme)
BG       = '#0a0e1a'
CARD     = '#131a2e'
BORDER   = '#26314f'
ACCENT   = '#00d97e'
ACCENT2  = '#0af'
DANGER   = '#ff4d4f'
WARN     = '#ffb020'
TEXT     = '#e6ecf5'
MUTED    = '#7a8aa8'


def draw_box(ax, x, y, w, h, text, fc=CARD, ec=BORDER, tc=TEXT, fontsize=10, weight='bold'):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02",
        linewidth=1.5, facecolor=fc, edgecolor=ec
    )
    ax.add_patch(box)
    ax.text(x + w / 2, y + h / 2, text,
            ha='center', va='center', color=tc, fontsize=fontsize, weight=weight)


def draw_arrow(ax, x1, y1, x2, y2, color=ACCENT, label=None, style='-|>'):
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle=style,
        mutation_scale=18,
        color=color, linewidth=2,
        connectionstyle="arc3,rad=0"
    )
    ax.add_patch(arrow)
    if label:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.15, label,
                ha='center', va='bottom', color=MUTED, fontsize=9)


# === DIAGRAMA 1: ARCHITECTURE ===
fig, ax = plt.subplots(figsize=(14, 9), facecolor=BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 14)
ax.set_ylim(0, 9)
ax.axis('off')

# Title
ax.text(7, 8.5, 'ScamShield Pro — Arquitectura',
        ha='center', va='center', color=TEXT, fontsize=20, weight='bold')
ax.text(7, 8.05, 'Self-hosted URL fraud & phishing detector',
        ha='center', va='center', color=MUTED, fontsize=11)

# Client
draw_box(ax, 5, 6.7, 4, 0.7, 'CLIENTE\nBrowser · curl · Python SDK · webhook',
         fc='#1a2238', tc=ACCENT2, fontsize=10)

# FastAPI
draw_box(ax, 4, 5.3, 6, 0.8, 'FastAPI Server (server.py)\n• CORS · Rate limit · API key auth\n• Routes: /, /dashboard, /healthz, /v1/scan, /v1/scan/bulk',
         fc='#0d1525', ec=ACCENT, tc=TEXT, fontsize=9)

draw_arrow(ax, 7, 6.7, 7, 6.1, color=ACCENT)
ax.text(7.1, 6.4, 'POST /v1/scan', color=ACCENT, fontsize=9, ha='left', va='center')

# Scanner
draw_box(ax, 4, 3.8, 6, 0.9, 'Scanner (scanner.py)\n1. normalize_url · parse_domain\n2. Fase 1 paralela (no-content checks)\n3. Fase 2 secuencial (content checks)\n4. compute_score() → TrustScore',
         fc='#0d1525', ec=ACCENT, tc=TEXT, fontsize=9)

draw_arrow(ax, 7, 5.3, 7, 4.7, color=ACCENT)

# 9 checks (3x3 grid)
checks_data = [
    ('1. Domain Age', 'WHOIS lookup', 'high'),
    ('2. SSL Cert', 'socket + ssl', 'high'),
    ('3. DNS Records', 'dnspython', 'medium'),
    ('4. TLD Reputation', 'static list', 'medium'),
    ('5. Redirect Chain', 'httpx async', 'medium'),
    ('6. Content Analysis', 'BeautifulSoup', 'medium'),
    ('7. Phishing Patterns', 'regex + IDN', 'critical'),
    ('8. Blocklist Check', 'URLHaus + GSB + VT', 'critical'),
    ('9. IP Reputation', 'ip-api.com', 'medium'),
]

severity_colors = {
    'high': WARN,
    'medium': ACCENT,
    'critical': DANGER,
}

check_w, check_h = 1.9, 0.75
start_x = 0.7
start_y = 1.5
gap_x = 0.15
gap_y = 0.2

for i, (name, tech, sev) in enumerate(checks_data):
    row = i // 3
    col = i % 3
    x = start_x + col * (check_w + gap_x)
    y = start_y + (2 - row) * (check_h + gap_y)
    sev_color = severity_colors[sev]
    draw_box(ax, x, y, check_w, check_h,
             f'{name}\n{tech}\n[{sev}]', fc=CARD, ec=sev_color, tc=TEXT, fontsize=8)
    # Arrow from scanner to each check (light)
    draw_arrow(ax, 7, 3.8, x + check_w / 2, y + check_h, color='#3a4365', style='-')

# Cache + external
draw_box(ax, 0.5, 0.3, 3, 0.6, '[CACHE] DiskCache\n~/.scamshield/cache', fc='#1a2238', tc=ACCENT, fontsize=9)
draw_box(ax, 4, 0.3, 3, 0.6, '[API] External (optional)\nGSB · VirusTotal · IPQS', fc='#1a2238', tc=MUTED, fontsize=9)
draw_box(ax, 7.5, 0.3, 3, 0.6, '[BLOCKLISTS] Public\nURLHaus · ip-api.com', fc='#1a2238', tc=ACCENT2, fontsize=9)
draw_box(ax, 11, 0.3, 2.5, 0.6, '[DOCKER]\ncontainer', fc='#1a2238', tc=ACCENT, fontsize=9)

# Legend
ax.text(13.7, 8.5, 'Severidad', ha='right', va='center', color=TEXT, fontsize=10, weight='bold')
ax.text(13.7, 8.15, '[high]', ha='right', va='center', color=WARN, fontsize=9)
ax.text(13.7, 7.85, '[medium]', ha='right', va='center', color=ACCENT, fontsize=9)
ax.text(13.7, 7.55, '[critical]', ha='right', va='center', color=DANGER, fontsize=9)

plt.savefig(f'{OUT_DIR}/architecture.png',
            dpi=160, facecolor=BG, bbox_inches='tight', pad_inches=0.2)
plt.close()
print(f'✓ {OUT_DIR}/architecture.png')


# === DIAGRAMA 2: USER FLOW ===
fig, ax = plt.subplots(figsize=(14, 6), facecolor=BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 14)
ax.set_ylim(0, 6)
ax.axis('off')

ax.text(7, 5.5, 'ScamShield Pro — Flujo de un scan',
        ha='center', va='center', color=TEXT, fontsize=18, weight='bold')
ax.text(7, 5.05, 'Tiempo total objetivo: < 2 segundos',
        ha='center', va='center', color=MUTED, fontsize=11)

# Steps (horizontal flow)
steps = [
    (0.3, '1\nCliente\nhace\nPOST\n/v1/scan', '#1a2238', ACCENT2),
    (2.3, '2\nFastAPI\nauth +\nrate limit\ncheck', '#1a2238', ACCENT),
    (4.3, '3\nScanner\nnormaliza\nURL +\nparsea\ndominio', '#0d1525', ACCENT),
    (6.3, '4\nFase 1\nparalela:\nWHOIS, SSL,\nDNS, redirects,\nIP, blocklist,\nphishing, TLD', '#0d1525', WARN),
    (9, '5\nFase 2\nsecuencial:\ncontent\nanalysis\n(usa\nfinal_url)', '#0d1525', WARN),
    (11, '6\ncompute_\nscore()\n→ 0-100\n+ verdict\n+ checks[]', '#0d1525', ACCENT),
    (13, '7\nResponse\nJSON a\ncliente', '#1a2238', ACCENT2),
]

step_w = 1.5
step_h = 2.5

for x, label, fc, ec in steps:
    draw_box(ax, x, 1.3, step_w, step_h, label, fc=fc, ec=ec, tc=TEXT, fontsize=9, weight='bold')

# Arrows between steps
arrow_xs = [(1.8, 2.3), (3.8, 4.3), (5.8, 6.3), (8.5, 9), (10.5, 11), (12.5, 13)]
for x1, x2 in arrow_xs:
    draw_arrow(ax, x1, 2.55, x2, 2.55, color=ACCENT)

# Timeline at bottom
ax.plot([0.3, 14], [0.7, 0.7], color=MUTED, linewidth=1.5)
for i, label in enumerate(['t=0ms', '~5ms', '~50ms', '~500ms', '~1.5s', '~1.8s', '~2s']):
    x = 0.3 + i * 2.3 if i < 4 else 0.3 + 6 * 2.3 + (i - 6) * 1.5
    # Simpler: just put labels under each step
    xs = [0.3, 2.3, 4.3, 6.3, 9, 11, 13]
    ax.text(xs[i] + 0.75, 0.5, label, ha='center', va='top', color=MUTED, fontsize=8)
    ax.plot([xs[i] + 0.75, xs[i] + 0.75], [0.65, 0.75], color=MUTED, linewidth=1)

plt.savefig(f'{OUT_DIR}/flow.png',
            dpi=160, facecolor=BG, bbox_inches='tight', pad_inches=0.2)
plt.close()
print(f'✓ {OUT_DIR}/flow.png')


# === DIAGRAMA 3: SCORE BANDS (palette reference) ===
fig, ax = plt.subplots(figsize=(14, 4), facecolor=BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 14)
ax.set_ylim(0, 4)
ax.axis('off')

ax.text(7, 3.5, 'ScamShield Pro — Trust Score Bands (ScamAdviser-compatible)',
        ha='center', va='center', color=TEXT, fontsize=16, weight='bold')

bands = [
    (0.2, 2.4, '1-20', 'VERY\nUNSAFE', DANGER, 'No visites.\nNo ingreses\ndatos.'),
    (2.8, 2.4, '21-40', 'LIKELY\nUNSAFE', '#ff8a3d', 'Evita\ntransac-\nciones.'),
    (5.4, 2.4, '41-60', 'CAUTION', WARN, 'Verifica\nreseñas,\ndirección.'),
    (8.0, 2.4, '61-80', 'LIKELY\nSAFE', '#4cd964', 'Procede.\nUsa\ntarjeta.'),
    (10.6, 2.4, '81-100', 'VERY\nSAFE', ACCENT, 'Alta\nconfianza.\nProcede.'),
]

for x, w, score, verdict, color, rec in bands:
    draw_box(ax, x, 1.2, w, 1.8, '', fc=CARD, ec=color, tc=TEXT)
    ax.text(x + w/2, 2.65, score, ha='center', va='center', color=color, fontsize=14, weight='bold')
    ax.text(x + w/2, 2.05, verdict, ha='center', va='center', color=color, fontsize=11, weight='bold')
    ax.text(x + w/2, 1.45, rec, ha='center', va='center', color=TEXT, fontsize=9)

plt.savefig(f'{OUT_DIR}/score_bands.png',
            dpi=160, facecolor=BG, bbox_inches='tight', pad_inches=0.2)
plt.close()
print(f'✓ {OUT_DIR}/score_bands.png')

print('\nDone! 3 diagrams generated.')
