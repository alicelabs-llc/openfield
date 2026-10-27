"""LicitAlert diagrams."""
import os, matplotlib
matplotlib.use('Agg')
import matplotlib.font_manager as fm
fm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

OUT='/home/z/my-project/download/HOTMART_PRODUCTOS/licitalert/diagrams'
os.makedirs(OUT, exist_ok=True)

BG='#0a1018'; CARD='#0f1825'; BORDER='#1f2d44'; TEXT='#e6ecf5'; MUTED='#7a8aa8'
ACCENT='#3b82f6'; ACCENT2='#10b981'

def box(ax,x,y,w,h,t,fc=CARD,ec=BORDER,tc=TEXT,fs=10,weight='bold'):
    b=FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02",linewidth=1.5,facecolor=fc,edgecolor=ec)
    ax.add_patch(b); ax.text(x+w/2,y+h/2,t,ha='center',va='center',color=tc,fontsize=fs,weight=weight)
def arrow(ax,x1,y1,x2,y2,color=ACCENT):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=18,color=color,linewidth=2))

# Architecture
fig, ax = plt.subplots(figsize=(14,8), facecolor=BG)
ax.set_facecolor(BG); ax.set_xlim(0,14); ax.set_ylim(0,8); ax.axis('off')
ax.text(7,7.5,'LicitAlert — Arquitectura',ha='center',color=TEXT,fontsize=20,weight='bold')
ax.text(7,7.1,'Alertas de licitaciones públicas LatAm',ha='center',color=MUTED,fontsize=11)

box(ax,4.5,5.8,5,0.7,'ADMIN (CRUD reglas) + USUARIO (recibe alertas)',fc='#1a2a4a',tc=ACCENT2,fs=10)
box(ax,3,4.4,8,0.9,'FastAPI Server + APScheduler\nPOST /v1/rules, GET /v1/tenders, POST /v1/check',fc='#0d1525',ec=ACCENT,fs=9)
arrow(ax,7,5.8,7,5.3,color=ACCENT)

# Scheduler
box(ax,0.5,4.4,2.5,0.9,'APScheduler\ncada 6h\n(configurable)',fc='#0d1525',ec=ACCENT2,fs=9)
arrow(ax,1.75,4.4,4.5,4.85,color=ACCENT2)

# 3 country scrapers
box(ax,0.5,2.8,3,1.2,'SecopScraper\n\nColombia\nSECOP II API\nCOP currency',fc='#0d1525',ec=ACCENT,fs=9)
box(ax,4,2.8,3,1.2,'SerCopScraper\n\nEcuador\nSERCOP\nUSD currency',fc='#0d1525',ec=ACCENT2,fs=9)
box(ax,7.5,2.8,3,1.2,'CompraNetScraper\n\nMexico\nIMCO API\nMXN currency',fc='#0d1525',ec=ACCENT,fs=9)

# Matcher
box(ax,11,2.8,2.5,1.2,'Matcher\n\nnormalize\nlowercase\nstrip accents\nkeyword match\nbudget filter',fc='#0d1525',ec=ACCENT2,fs=9)

arrow(ax,7,4.4,2,4.0,color='#3a4365')
arrow(ax,7,4.4,5.5,4.0,color='#3a4365')
arrow(ax,7,4.4,9,4.0,color='#3a4365')
arrow(ax,7,4.4,12.25,4.0,color='#3a4365')

# Notifier
box(ax,0.5,1.3,3,0.6,'[NOTIFY] Email + Telegram',fc='#1a2a4a',tc=ACCENT,fs=9)
box(ax,4,1.3,3,0.6,'[DATA] JSON store',fc='#1a2a4a',tc=ACCENT2,fs=9)
box(ax,7.5,1.3,3,0.6,'[CACHE] dedupe',fc='#1a2a4a',tc=ACCENT,fs=9)
box(ax,11,1.3,2.5,0.6,'[Docker]',fc='#1a2a4a',tc=MUTED,fs=9)

plt.savefig(f'{OUT}/architecture.png',dpi=160,facecolor=BG,bbox_inches='tight',pad_inches=0.2)
plt.close()
print(f'✓ {OUT}/architecture.png')

# Flow
fig, ax = plt.subplots(figsize=(14,5),facecolor=BG)
ax.set_facecolor(BG); ax.set_xlim(0,14); ax.set_ylim(0,5); ax.axis('off')
ax.text(7,4.5,'LicitAlert — Flujo automático',ha='center',color=TEXT,fontsize=18,weight='bold')

steps=[
    (0.3,'1\nScheduler\ndispara','#1a2a4a',ACCENT2),
    (2.5,'2\nScrapers\n3 países','#0d1525',ACCENT),
    (4.7,'3\nNuevos\ntenders','#0d1525',ACCENT2),
    (6.9,'4\nMatcher\nvs reglas','#0d1525',ACCENT),
    (9.1,'5\nAgrupa\npor regla','#0d1525',ACCENT2),
    (11.3,'6\nNotifica\nemail/TG','#1a2a4a',ACCENT),
]
for x,l,fc,ec in steps:
    box(ax,x,1.5,1.7,2,l,fc=fc,ec=ec,fs=9)
for x1,x2 in [(2.0,2.5),(4.2,4.7),(6.4,6.9),(8.6,9.1),(10.8,11.3)]:
    arrow(ax,x1,2.5,x2,2.5,color=ACCENT)

ax.text(7,0.5,'Cada 6 horas automáticamente. Sin intervención manual.',ha='center',color=MUTED,fontsize=10)

plt.savefig(f'{OUT}/flow.png',dpi=160,facecolor=BG,bbox_inches='tight',pad_inches=0.2)
plt.close()
print(f'✓ {OUT}/flow.png')
print('Done!')
