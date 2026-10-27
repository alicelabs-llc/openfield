"""PriceWatch diagrams."""
import os, matplotlib
matplotlib.use('Agg')
import matplotlib.font_manager as fm
fm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

OUT='/home/z/my-project/download/HOTMART_PRODUCTOS/pricewatch/diagrams'
os.makedirs(OUT, exist_ok=True)

BG='#0a0f1a'; CARD='#101828'; BORDER='#1f2d44'; TEXT='#e6ecf5'; MUTED='#7a8aa8'
ACCENT='#ffb020'; ACCENT2='#10b981'

def box(ax,x,y,w,h,t,fc=CARD,ec=BORDER,tc=TEXT,fs=10,weight='bold'):
    b=FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02",linewidth=1.5,facecolor=fc,edgecolor=ec)
    ax.add_patch(b); ax.text(x+w/2,y+h/2,t,ha='center',va='center',color=tc,fontsize=fs,weight=weight)
def arrow(ax,x1,y1,x2,y2,color=ACCENT):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=18,color=color,linewidth=2))

fig, ax = plt.subplots(figsize=(14,8), facecolor=BG)
ax.set_facecolor(BG); ax.set_xlim(0,14); ax.set_ylim(0,8); ax.axis('off')
ax.text(7,7.5,'PriceWatch — Arquitectura',ha='center',color=TEXT,fontsize=20,weight='bold')
ax.text(7,7.1,'Monitor de precios MercadoLibre + Amazon',ha='center',color=MUTED,fontsize=11)

box(ax,5,5.8,4,0.7,'CLIENTE (CLI / curl / Web)',fc='#1a2a4a',tc=ACCENT2,fs=10)
box(ax,3.5,4.4,7,0.9,'FastAPI Server\nPOST /v1/track → product_id\nGET /v1/products → list',fc='#0d1525',ec=ACCENT,fs=9)
arrow(ax,7,5.8,7,5.3,color=ACCENT)

# Scheduler
box(ax,0.5,4.4,2.5,0.9,'APScheduler\n(cada 60 min)',fc='#0d1525',ec=ACCENT2,fs=9)
arrow(ax,1.75,4.4,4.5,4.85,color=ACCENT2)

# 2 scrapers
box(ax,0.5,2.8,3,1,'MercadoLibreScraper\nJSON-LD parsing\n+ meta tags',fc='#0d1525',ec=ACCENT,fs=9)
box(ax,4,2.8,3,1,'AmazonScraper\nJSON-LD + DOM\na-price classes',fc='#0d1525',ec=ACCENT,fs=9)
box(ax,7.5,2.8,3,1,'Tracker service\npersiste products.json\n+ price_history',fc='#0d1525',ec=ACCENT2,fs=9)
box(ax,11,2.8,2.5,1,'3 channels\nemail\ntelegram\ndiscord',fc='#0d1525',ec=ACCENT,fs=9)

for x in [2,5.5,9,12.25]:
    arrow(ax,7,4.4,x,3.8,color='#3a4365')

# Bottom
box(ax,0.5,1.3,3,0.6,'[DATA] products.json',fc='#1a2a4a',tc=ACCENT,fs=9)
box(ax,4,1.3,3,0.6,'[CACHE] diskcache',fc='#1a2a4a',tc=ACCENT2,fs=9)
box(ax,7.5,1.3,3,0.6,'[SMTP] email server',fc='#1a2a4a',tc=ACCENT,fs=9)
box(ax,11,1.3,2.5,0.6,'[TG bot] optional',fc='#1a2a4a',tc=MUTED,fs=9)

# Stores
box(ax,0.5,0.3,3,0.6,'mercadolibre.com.ec / mx / co / ar / cl / pe',fc='#1a2a4a',tc=ACCENT2,fs=8)
box(ax,4,0.3,3,0.6,'amazon.com / .mx / .br / .uk',fc='#1a2a4a',tc=ACCENT2,fs=8)

plt.savefig(f'{OUT}/architecture.png',dpi=160,facecolor=BG,bbox_inches='tight',pad_inches=0.2)
plt.close()
print(f'✓ {OUT}/architecture.png')

# Flow
fig, ax = plt.subplots(figsize=(14,4),facecolor=BG)
ax.set_facecolor(BG); ax.set_xlim(0,14); ax.set_ylim(0,4); ax.axis('off')
ax.text(7,3.5,'PriceWatch — Flujo de tracking',ha='center',color=TEXT,fontsize=18,weight='bold')

steps=[
    (0.3,'1\nTrack URL\n+target price','#1a2a4a',ACCENT2),
    (2.5,'2\nScraper\nfetches page','#0d1525',ACCENT),
    (4.7,'3\nParse price\n+ discount','#0d1525',ACCENT),
    (6.9,'4\nSave to\nhistory','#0d1525',ACCENT2),
    (9.1,'5\nCheck\ncondition','#0d1525',ACCENT),
    (11.3,'6\nNotify\nemail/TG/Discord','#1a2a4a',ACCENT2),
]
for x,l,fc,ec in steps:
    box(ax,x,1,1.7,1.8,l,fc=fc,ec=ec,fs=9)
for x1,x2 in [(2.0,2.5),(4.2,4.7),(6.4,6.9),(8.6,9.1),(10.8,11.3)]:
    arrow(ax,x1,1.9,x2,1.9,color=ACCENT)

plt.savefig(f'{OUT}/flow.png',dpi=160,facecolor=BG,bbox_inches='tight',pad_inches=0.2)
plt.close()
print(f'✓ {OUT}/flow.png')
print('Done!')
