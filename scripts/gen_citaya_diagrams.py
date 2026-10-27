"""CitaYa diagrams."""
import os, matplotlib
matplotlib.use('Agg')
import matplotlib.font_manager as fm
fm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

OUT='/home/z/my-project/download/HOTMART_PRODUCTOS/citaya/diagrams'
os.makedirs(OUT, exist_ok=True)

BG='#0a0a1a'; CARD='#13132a'; BORDER='#26264f'; TEXT='#e6ecf5'; MUTED='#7a8aa8'
ACCENT='#a855f7'; ACCENT2='#ec4899'

def box(ax,x,y,w,h,t,fc=CARD,ec=BORDER,tc=TEXT,fs=10,weight='bold'):
    b=FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02",linewidth=1.5,facecolor=fc,edgecolor=ec)
    ax.add_patch(b); ax.text(x+w/2,y+h/2,t,ha='center',va='center',color=tc,fontsize=fs,weight=weight)
def arrow(ax,x1,y1,x2,y2,color=ACCENT):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=18,color=color,linewidth=2))

# Architecture
fig, ax = plt.subplots(figsize=(14,8), facecolor=BG)
ax.set_facecolor(BG); ax.set_xlim(0,14); ax.set_ylim(0,8); ax.axis('off')
ax.text(7,7.5,'CitaYa — Arquitectura',ha='center',color=TEXT,fontsize=20,weight='bold')
ax.text(7,7.1,'Sistema de reservas self-hosted',ha='center',color=MUTED,fontsize=11)

box(ax,4.5,5.8,5,0.7,'CLIENTES (Widget público) + ADMIN',fc='#1a2a4a',tc=ACCENT2,fs=10)
box(ax,3,4.4,8,0.9,'FastAPI Server\n/public/* (no auth)  +  /admin/* (auth)\nAPScheduler reminders cada 60min',fc='#0d1525',ec=ACCENT,fs=9)
arrow(ax,7,5.8,7,5.3,color=ACCENT)

# Services
box(ax,0.5,2.5,3,1.5,'BookingService\n\nbook()\ncancel()\nconfirm/complete\nhas_conflict()',fc='#0d1525',ec=ACCENT,fs=9)
box(ax,4,2.5,3,1.5,'DataStore\n(JSON)\n\nprofessionals\nservices\ncustomers\nappointments',fc='#0d1525',ec=ACCENT2,fs=9)
box(ax,7.5,2.5,3,1.5,'SlotGenerator\n\ngenerate_slots()\nworking_hours\nper day\nper professional',fc='#0d1525',ec=ACCENT,fs=9)
box(ax,11,2.5,2.5,1.5,'Notifiers\n\nemail (SMTP)\ntelegram\nwhatsapp',fc='#0d1525',ec=ACCENT2,fs=9)

arrow(ax,7,4.4,2,4.0,color='#3a4365')
arrow(ax,7,4.4,5.5,4.0,color='#3a4365')
arrow(ax,7,4.4,9,4.0,color='#3a4365')
arrow(ax,7,4.4,12.25,4.0,color='#3a4365')

# Bottom
box(ax,0.5,1,3,0.6,'[BUSINESS] config',fc='#1a2a4a',tc=ACCENT,fs=9)
box(ax,4,1,3,0.6,'[DATA] json files',fc='#1a2a4a',tc=ACCENT2,fs=9)
box(ax,7.5,1,3,0.6,'[SMTP] email',fc='#1a2a4a',tc=ACCENT,fs=9)
box(ax,11,1,2.5,0.6,'[Docker]',fc='#1a2a4a',tc=MUTED,fs=9)

# Appointment states diagram below
ax.text(7,0.5,'Estados: pending → confirmed → completed / cancelled / no_show',ha='center',color=MUTED,fontsize=9)

plt.savefig(f'{OUT}/architecture.png',dpi=160,facecolor=BG,bbox_inches='tight',pad_inches=0.2)
plt.close()
print(f'✓ {OUT}/architecture.png')

# Booking flow
fig, ax = plt.subplots(figsize=(14,5),facecolor=BG)
ax.set_facecolor(BG); ax.set_xlim(0,14); ax.set_ylim(0,5); ax.axis('off')
ax.text(7,4.5,'CitaYa — Flujo de reserva',ha='center',color=TEXT,fontsize=18,weight='bold')

steps=[
    (0.3,'1\nCliente\nve slots','#1a2a4a',ACCENT2),
    (2.5,'2\nPOST\n/public/book','#0d1525',ACCENT),
    (4.7,'3\nBookingService\nvalida','#0d1525',ACCENT),
    (6.9,'4\nCheck\nconflict','#0d1525',ACCENT2),
    (9.1,'5\nSave apt\n+ reminder','#0d1525',ACCENT),
    (11.3,'6\nNotify\nemail/TG/WA','#1a2a4a',ACCENT2),
]
for x,l,fc,ec in steps:
    box(ax,x,1.5,1.7,2,l,fc=fc,ec=ec,fs=9)
for x1,x2 in [(2.0,2.5),(4.2,4.7),(6.4,6.9),(8.6,9.1),(10.8,11.3)]:
    arrow(ax,x1,2.5,x2,2.5,color=ACCENT)

ax.text(7,0.5,'Reminder automático: 2h antes (configurable)',ha='center',color=MUTED,fontsize=10)

plt.savefig(f'{OUT}/flow.png',dpi=160,facecolor=BG,bbox_inches='tight',pad_inches=0.2)
plt.close()
print(f'✓ {OUT}/flow.png')
print('Done!')
