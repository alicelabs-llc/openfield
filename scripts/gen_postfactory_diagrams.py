"""PostFactory diagrams."""
import os, matplotlib
matplotlib.use('Agg')
import matplotlib.font_manager as fm
fm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

OUT='/home/z/my-project/download/HOTMART_PRODUCTOS/postfactory/diagrams'
os.makedirs(OUT, exist_ok=True)

BG='#0a0a14'; CARD='#13131f'; BORDER='#26263f'; TEXT='#e6ecf5'; MUTED='#7a8aa8'
ACCENT='#ec4899'; ACCENT2='#06b6d4'

def box(ax,x,y,w,h,t,fc=CARD,ec=BORDER,tc=TEXT,fs=10,weight='bold'):
    b=FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02",linewidth=1.5,facecolor=fc,edgecolor=ec)
    ax.add_patch(b); ax.text(x+w/2,y+h/2,t,ha='center',va='center',color=tc,fontsize=fs,weight=weight)
def arrow(ax,x1,y1,x2,y2,color=ACCENT):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=18,color=color,linewidth=2))

fig, ax = plt.subplots(figsize=(14,8), facecolor=BG)
ax.set_facecolor(BG); ax.set_xlim(0,14); ax.set_ylim(0,8); ax.axis('off')
ax.text(7,7.5,'PostFactory — Arquitectura',ha='center',color=TEXT,fontsize=20,weight='bold')
ax.text(7,7.1,'Generador de contenido para redes sociales',ha='center',color=MUTED,fontsize=11)

box(ax,4.5,5.8,5,0.7,'REQUEST (topic + platform + type)',fc='#1a2a4a',tc=ACCENT2,fs=10)
box(ax,3,4.4,8,0.9,'FastAPI Server\nPOST /v1/generate (mode=ai|template)\nPOST /v1/calendar, GET /v1/hashtags',fc='#0d1525',ec=ACCENT,fs=9)
arrow(ax,7,5.8,7,5.3,color=ACCENT)

# Templates
box(ax,0.5,2.5,3,1.3,'Templates\n\n7 content types x\n3 variants = 21\n\nEducational\nPromotional\nListicle\nHow-to\netc',fc='#0d1525',ec=ACCENT,fs=9)
# Hashtags
box(ax,4,2.5,3,1.3,'Hashtag Gen\n\n10 niches\n+ topic-derived\n+ platform limits\n\nIG: 30 max\nLinkedIn: 5 max',fc='#0d1525',ec=ACCENT2,fs=9)
# AI Client
box(ax,7.5,2.5,3,1.3,'AI Client\n\nZ.ai GLM-4.6\nOpenAI / Anthropic\nOllama local\n\nbuild_prompt()\ncall_ai()',fc='#0d1525',ec=ACCENT,fs=9)
# Calendar
box(ax,11,2.5,2.5,1.3,'Calendar\n\nN days\nrotating topics\nbest times\nper platform',fc='#0d1525',ec=ACCENT2,fs=9)

arrow(ax,7,4.4,2,4.0,color='#3a4365')
arrow(ax,7,4.4,5.5,4.0,color='#3a4365')
arrow(ax,7,4.4,9,4.0,color='#3a4365')
arrow(ax,7,4.4,12.25,4.0,color='#3a4365')

# Bottom
box(ax,0.5,1.3,3,0.6,'[BRAND] config',fc='#1a2a4a',tc=ACCENT,fs=9)
box(ax,4,1.3,3,0.6,'[AI Provider] Z.ai default',fc='#1a2a4a',tc=ACCENT2,fs=9)
box(ax,7.5,1.3,3,0.6,'[Cache] diskcache',fc='#1a2a4a',tc=ACCENT,fs=9)
box(ax,11,1.3,2.5,0.6,'[Docker]',fc='#1a2a4a',tc=MUTED,fs=9)

plt.savefig(f'{OUT}/architecture.png',dpi=160,facecolor=BG,bbox_inches='tight',pad_inches=0.2)
plt.close()
print(f'✓ {OUT}/architecture.png')

# Flow
fig, ax = plt.subplots(figsize=(14,4),facecolor=BG)
ax.set_facecolor(BG); ax.set_xlim(0,14); ax.set_ylim(0,4); ax.axis('off')
ax.text(7,3.5,'PostFactory — Flujo',ha='center',color=TEXT,fontsize=18,weight='bold')

steps=[
    (0.3,'1\nInput\ntopic','#1a2a4a',ACCENT2),
    (2.5,'2\nPick\ntemplates','#0d1525',ACCENT),
    (4.7,'3\nGenerate\nhashtags','#0d1525',ACCENT2),
    (6.9,'4\nCall AI\n(or template)','#0d1525',ACCENT),
    (9.1,'5\n3 variants\n+ image prompts','#0d1525',ACCENT2),
    (11.3,'6\nReturn JSON','#1a2a4a',ACCENT),
]
for x,l,fc,ec in steps:
    box(ax,x,1,1.7,2,l,fc=fc,ec=ec,fs=9)
for x1,x2 in [(2.0,2.5),(4.2,4.7),(6.4,6.9),(8.6,9.1),(10.8,11.3)]:
    arrow(ax,x1,2,x2,2,color=ACCENT)

ax.text(7,0.3,'Fallback: si AI falla o no configurado, usa 21 templates gratis',ha='center',color=MUTED,fontsize=10)

plt.savefig(f'{OUT}/flow.png',dpi=160,facecolor=BG,bbox_inches='tight',pad_inches=0.2)
plt.close()
print(f'✓ {OUT}/flow.png')
print('Done!')
