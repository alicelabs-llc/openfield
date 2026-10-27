"""MenuQR Pro diagrams."""
import os, matplotlib
matplotlib.use('Agg')
import matplotlib.font_manager as fm
fm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

OUT='/home/z/my-project/download/HOTMART_PRODUCTOS/menuqr/diagrams'
os.makedirs(OUT, exist_ok=True)

BG='#0a1410'; CARD='#0f2418'; BORDER='#1f3a26'; TEXT='#e6ecf5'; MUTED='#7a8aa8'
ACCENT='#f59e0b'; ACCENT2='#10b981'

def box(ax,x,y,w,h,t,fc=CARD,ec=BORDER,tc=TEXT,fs=10,weight='bold'):
    b=FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02",linewidth=1.5,facecolor=fc,edgecolor=ec)
    ax.add_patch(b); ax.text(x+w/2,y+h/2,t,ha='center',va='center',color=tc,fontsize=fs,weight=weight)
def arrow(ax,x1,y1,x2,y2,color=ACCENT):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=18,color=color,linewidth=2))

# Architecture
fig, ax = plt.subplots(figsize=(14,8), facecolor=BG)
ax.set_facecolor(BG); ax.set_xlim(0,14); ax.set_ylim(0,8); ax.axis('off')
ax.text(7,7.5,'MenuQR Pro — Arquitectura',ha='center',color=TEXT,fontsize=20,weight='bold')
ax.text(7,7.1,'Menús digitales con QR para restaurantes',ha='center',color=MUTED,fontsize=11)

box(ax,4.5,5.8,5,0.7,'CLIENTE (escanea QR) + ADMIN (gestiona)',fc='#1a2a4a',tc=ACCENT2,fs=10)
box(ax,3,4.4,8,0.9,'FastAPI Server\n/public/menu/{table_id} (HTML)\n/admin/* (CRUD items/mesas/orders)\n/admin/tables/{id}/qr (image)',fc='#0d1525',ec=ACCENT,fs=9)
arrow(ax,7,5.8,7,5.3,color=ACCENT)

box(ax,0.5,2.8,3,1.3,'Store\nJSON\n\ncategories.json\nitems.json\ntables.json\norders.json',fc='#0d1525',ec=ACCENT,fs=9)
box(ax,4,2.8,3,1.3,'QR Generator\n\nqrcode lib\nstyledpil\nERROR_CORRECT_H\ncolor customizable',fc='#0d1525',ec=ACCENT2,fs=9)
box(ax,7.5,2.8,3,1.3,'HTML Renderer\n\nrender_menu_html()\nresponsive\nmulti-idioma',fc='#0d1525',ec=ACCENT,fs=9)
box(ax,11,2.8,2.5,1.3,'Order Flow\n\npending\npreparing\nserved\npaid\ncancelled',fc='#0d1525',ec=ACCENT2,fs=9)

arrow(ax,7,4.4,2,4.1,color='#3a4365')
arrow(ax,7,4.4,5.5,4.1,color='#3a4365')
arrow(ax,7,4.4,9,4.1,color='#3a4365')
arrow(ax,7,4.4,12.25,4.1,color='#3a4365')

box(ax,0.5,1.3,3,0.6,'[DATA] JSON files',fc='#1a2a4a',tc=ACCENT,fs=9)
box(ax,4,1.3,3,0.6,'[QR] PNG generation',fc='#1a2a4a',tc=ACCENT2,fs=9)
box(ax,7.5,1.3,3,0.6,'[LANG] es/en/pt',fc='#1a2a4a',tc=ACCENT,fs=9)
box(ax,11,1.3,2.5,0.6,'[Docker]',fc='#1a2a4a',tc=MUTED,fs=9)

plt.savefig(f'{OUT}/architecture.png',dpi=160,facecolor=BG,bbox_inches='tight',pad_inches=0.2)
plt.close()
print(f'✓ {OUT}/architecture.png')

# Customer flow
fig, ax = plt.subplots(figsize=(14,4),facecolor=BG)
ax.set_facecolor(BG); ax.set_xlim(0,14); ax.set_ylim(0,4); ax.axis('off')
ax.text(7,3.5,'MenuQR Pro — Flujo del cliente',ha='center',color=TEXT,fontsize=18,weight='bold')

steps=[
    (0.3,'1\nCliente\nescanea QR','#1a2a4a',ACCENT2),
    (2.5,'2\nVe menú\nen celular','#0d1525',ACCENT),
    (4.7,'3\nSelecciona\nitems','#0d1525',ACCENT2),
    (6.9,'4\nPide\n+ notas','#0d1525',ACCENT),
    (9.1,'5\nCocina\nrecibe','#0d1525',ACCENT2),
    (11.3,'6\nSirve\n+ cobra','#1a2a4a',ACCENT),
]
for x,l,fc,ec in steps:
    box(ax,x,1,1.7,2,l,fc=fc,ec=ec,fs=9)
for x1,x2 in [(2.0,2.5),(4.2,4.7),(6.4,6.9),(8.6,9.1),(10.8,11.3)]:
    arrow(ax,x1,2,x2,2,color=ACCENT)

ax.text(7,0.3,'Sin app. Sin descarga. Solo el navegador del celular.',ha='center',color=MUTED,fontsize=10)

plt.savefig(f'{OUT}/flow.png',dpi=160,facecolor=BG,bbox_inches='tight',pad_inches=0.2)
plt.close()
print(f'✓ {OUT}/flow.png')
print('Done!')
