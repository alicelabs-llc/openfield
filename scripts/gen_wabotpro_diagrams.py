"""WhatsAppBot Pro diagrams."""
import os, matplotlib
matplotlib.use('Agg')
import matplotlib.font_manager as fm
fm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

OUT='/home/z/my-project/download/HOTMART_PRODUCTOS/wabotpro/diagrams'
os.makedirs(OUT, exist_ok=True)

BG='#0a1a0e'; CARD='#0f2418'; BORDER='#1f3a26'; TEXT='#e6ecf5'; MUTED='#7a8aa8'
ACCENT='#25d366'; ACCENT2='#0af'

def box(ax,x,y,w,h,t,fc=CARD,ec=BORDER,tc=TEXT,fs=10,weight='bold'):
    b=FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02",linewidth=1.5,facecolor=fc,edgecolor=ec)
    ax.add_patch(b); ax.text(x+w/2,y+h/2,t,ha='center',va='center',color=tc,fontsize=fs,weight=weight)
def arrow(ax,x1,y1,x2,y2,color=ACCENT):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=18,color=color,linewidth=2))

# Architecture
fig, ax = plt.subplots(figsize=(14,8), facecolor=BG)
ax.set_facecolor(BG); ax.set_xlim(0,14); ax.set_ylim(0,8); ax.axis('off')
ax.text(7,7.5,'WhatsAppBot Pro — Arquitectura',ha='center',color=TEXT,fontsize=20,weight='bold')
ax.text(7,7.1,'Bot de WhatsApp self-hosted vía Cloud API oficial',ha='center',color=MUTED,fontsize=11)

box(ax,5,5.8,4,0.7,'CLIENTE en WhatsApp',fc='#1a2a4a',tc=ACCENT2,fs=10)
box(ax,3.5,4.4,7,0.9,'FastAPI Server\n/webhook → procesa mensaje\n/v1/catalog, /v1/orders, /v1/send',fc='#0d1525',ec=ACCENT,fs=9)
arrow(ax,7,5.8,7,5.3,color=ACCENT)

# Flow engine
box(ax,0.5,2.8,4,1.3,'FlowEngine\n\nstate machine\nstart → browsing\n→ cart → checkout\n→ done',fc='#0d1525',ec=ACCENT,fs=9)

# Store
box(ax,4.8,2.8,4,1.3,'Store\n\ncatalog.json\norders.json\n+ CRUD productos',fc='#0d1525',ec=ACCENT2,fs=9)

# WhatsApp client
box(ax,9,2.8,4,1.3,'WhatsAppCloudClient\n\nMeta Cloud API v21.0\nsend_text, send_button\nsend_image',fc='#0d1525',ec=ACCENT,fs=9)

arrow(ax,7,4.4,2.5,4.1,color='#3a4365')
arrow(ax,7,4.4,6.8,4.1,color='#3a4365')
arrow(ax,7,4.4,11,4.1,color='#3a4365')

# Bottom: WA API + storage
box(ax,0.5,1.3,3,0.6,'[WA Cloud API] Meta',fc='#1a2a4a',tc=ACCENT,fs=9)
box(ax,4,1.3,3,0.6,'[DATA] catalog/orders',fc='#1a2a4a',tc=ACCENT2,fs=9)
box(ax,7.5,1.3,3,0.6,'[BUSINESS] config',fc='#1a2a4a',tc=ACCENT,fs=9)
box(ax,11,1.3,2.5,0.6,'[Docker]',fc='#1a2a4a',tc=MUTED,fs=9)

plt.savefig(f'{OUT}/architecture.png',dpi=160,facecolor=BG,bbox_inches='tight',pad_inches=0.2)
plt.close()
print(f'✓ {OUT}/architecture.png')

# Flow
fig, ax = plt.subplots(figsize=(14,5),facecolor=BG)
ax.set_facecolor(BG); ax.set_xlim(0,14); ax.set_ylim(0,5); ax.axis('off')
ax.text(7,4.5,'WhatsAppBot Pro — Flujo conversacional',ha='center',color=TEXT,fontsize=18,weight='bold')

steps=[
    (0.3,'1\nCliente\n"hola"','#1a2a4a',ACCENT2),
    (2.5,'2\nWebhook\nrecibe msg','#0d1525',ACCENT),
    (4.7,'3\nFlowEngine\nprocesa','#0d1525',ACCENT),
    (6.9,'4\nState machine\ncambia estado','#0d1525',ACCENT2),
    (9.1,'5\nGenera\nresponse(s)','#0d1525',ACCENT),
    (11.3,'6\nCloud API\nenvía reply','#1a2a4a',ACCENT2),
]
for x,l,fc,ec in steps:
    box(ax,x,1.5,1.7,2,l,fc=fc,ec=ec,fs=9)
for x1,x2 in [(2.0,2.5),(4.2,4.7),(6.4,6.9),(8.6,9.1),(10.8,11.3)]:
    arrow(ax,x1,2.5,x2,2.5,color=ACCENT)

ax.text(7,0.3,'Tiempo total: < 2 segundos',ha='center',color=MUTED,fontsize=10)

plt.savefig(f'{OUT}/flow.png',dpi=160,facecolor=BG,bbox_inches='tight',pad_inches=0.2)
plt.close()
print(f'✓ {OUT}/flow.png')

# Conversational state diagram
fig, ax = plt.subplots(figsize=(14,5),facecolor=BG)
ax.set_facecolor(BG); ax.set_xlim(0,14); ax.set_ylim(0,5); ax.axis('off')
ax.text(7,4.5,'WhatsAppBot Pro — State Machine',ha='center',color=TEXT,fontsize=18,weight='bold')

states=[
    (1,2.5,'START\n\n/hola\n/menu'),
    (3.5,2.5,'BROWSING\n\n/catálogo'),
    (6,2.5,'CART\n\n/agregar P001 2\n/carrito'),
    (9,2.5,'CHECKOUT\n\n/confirmar'),
    (12,2.5,'DONE\n\npedido creado'),
]
for x,y,t in states:
    box(ax,x-0.7,y,1.4,1.2,t,fc=CARD,ec=ACCENT,fs=9)

for x in [1.7,4.2,6.7,9.7]:
    arrow(ax,x,3.1,x+1.1,3.1,color=ACCENT)

ax.text(7,1,'Reset: /menu  ·  Cancel: any state → reset on checkout',ha='center',color=MUTED,fontsize=10)

plt.savefig(f'{OUT}/state_machine.png',dpi=160,facecolor=BG,bbox_inches='tight',pad_inches=0.2)
plt.close()
print(f'✓ {OUT}/state_machine.png')
print('Done!')
