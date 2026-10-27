"""
Genera emails .eml personalizados para cada lead con match score >= 6
y que sea remote/contract elegible para LLC.

NO envía — solo crea archivos .eml listos para el usuario abrir en su cliente
de correo y enviar manualmente (política anti-ban).

Anti-ban: el usuario debe enviar MÁXIMO 5-10 emails por día, no todos de golpe.
"""
import json
import os
import re
import html
from pathlib import Path
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from pathlib import Path

# Cargar leads
with open('/home/z/my-project/scripts/email_leads.json') as f:
    leads = json.load(f)

# Filtros: match >= 6, NO onsite-only (SF/NYC/BayArea sin remote)
def is_eligible(lead):
    text = (lead.get('comment_text','') or '').lower()
    score = lead.get('match_score', 0)
    if score < 6:
        return False
    # Excluir si es onsite-only SF/NYC sin remote
    onsite_only = (
        ('san francisco' in text or 'sf onsite' in text or 'bay area' in text)
        and 'remote' not in text
    ) or (
        ('new york city' in text or 'nyc onsite' in text)
        and 'remote' not in text
    )
    if onsite_only:
        return False
    # Excluir si pide C1+ Alemán (s&t)
    if 'german c1' in text or 'deutsch' in text:
        return False
    return True

eligible = [l for l in leads if is_eligible(l)]
print(f'Total leads en BD: {len(leads)}')
print(f'Elegibles (match>=6, remote, no language-specific): {len(eligible)}')

# Limpiar HTML del comment text para personalización
HTML_TAG_RE = re.compile(r'<[^>]+>')
HTML_ENTITY_RE = re.compile(r'&#x2F;|&#x27;|&#x2D;|&amp;|&lt;|&gt;|&quot;')

def clean_text(t):
    if not t: return ''
    t = HTML_ENTITY_RE.sub(lambda m: {
        '&#x2F;': '/', '&#x27;': "'", '&#x2D;': '-',
        '&amp;': '&', '&lt;': '<', '&gt;': '>',
        '&quot;': '"'
    }.get(m.group(), m.group()), t)
    t = HTML_TAG_RE.sub('', t)
    t = html.unescape(t)
    return t.strip()

# Generar subject + body personalizado según el match
def make_email(lead):
    email_addr = lead['email']
    author = lead.get('author', 'there')
    comment = clean_text(lead.get('comment_text', ''))
    # Primera línea del comment suele ser: Company | Role | Location | Type | ...
    first_line = comment.split('\n')[0] if comment else ''
    # Detectar keywords en el comment para personalizar pitch
    cl = comment.lower()
    
    # Construir pitch según skills mencionados
    pitch_parts = []
    if 'python' in cl or 'fastapi' in cl:
        pitch_parts.append('Python/FastAPI orchestration with Docker sandboxing')
    if 'agent' in cl or 'ai' in cl or 'llm' in cl:
        pitch_parts.append('AI agent platforms with tamper-evident provenance (alethech)')
    if 'security' in cl or 'audit' in cl or 'sandbox' in cl:
        pitch_parts.append('security sandboxing + Ed25519 signed audit trails')
    if 'gitlab' in cl or 'github' in cl or 'mcp' in cl:
        pitch_parts.append('GitLab/GitHub automation (webhooks, MR bots, Duo Agent Platform)')
    if 'devops' in cl or 'infrastructure' in cl or 'platform' in cl:
        pitch_parts.append('platform engineering with provenance-by-default')
    if 'rust' in cl:
        pitch_parts.append('(I also write Rust for performance-critical paths)')
    
    if not pitch_parts:
        pitch_parts.append('AI agent platforms with Docker sandbox + tamper-evident provenance')
    
    pitch = ', '.join(pitch_parts[:3])
    
    # Subject line según el rol
    subject = f"HN — saw your post about {first_line[:60]}{'...' if len(first_line)>60 else ''}"
    
    body = f"""Hi {author},

I saw your post on the "Ask HN: Who is hiring?" October thread — {first_line[:140]}

I run an LLC based in Ecuador (UTC-5, fully remote) doing exactly {pitch}. Public proof: github.com/eddyflores100-lang/alethech-agent-vault — FastAPI orchestrator with Docker sandbox (--network=none --read-only --cap-drop=ALL --security-opt=no-new-privileges), GitLab Duo Agent Platform integration, and tamper-evident provenance via alethech (hash-linked DAG, Ed25519-signed commits).

If {email_addr.split('@')[0]} still has the role open, I'd like to apply. Can you share the next step (apply link, intro call, take-home)?

If the role is filled, no worries — happy to be added to your bench for future openings.

Thanks,
Edison Flores
https://github.com/eddyflores100-lang
https://gitlab.com/eddyflores100
"""
    return subject, body

# Generar y guardar .eml files
out_dir = Path('/home/z/my-project/download/EMAILS_OUTREACH')
out_dir.mkdir(parents=True, exist_ok=True)

# Tomar top 30 elegibles (no todos — el usuario debe enviar max 5-10/día)
top = eligible[:30]

manifest_lines = []
for i, lead in enumerate(top, 1):
    subject, body = make_email(lead)
    email_addr = lead['email']
    author = lead.get('author','unknown')
    
    # Filename seguro
    safe_email = re.sub(r'[^A-Za-z0-9._-]', '_', email_addr)
    fn = out_dir / f'{i:02d}_{safe_email}.eml'
    
    msg = EmailMessage()
    msg['From'] = 'eddyflores100@example.com'  # Reemplazar por el usuario
    msg['To'] = email_addr
    msg['Subject'] = subject
    msg['Date'] = formatdate(localtime=True)
    msg['Message-ID'] = make_msgid()
    msg.set_content(body)
    
    with open(fn, 'wb') as f:
        f.write(bytes(msg))
    
    manifest_lines.append(f'{i:2}. {email_addr:<40} author={author:<25} file={fn.name}')

# Manifest
manifest = out_dir / 'MANIFEST.md'
with open(manifest, 'w') as f:
    f.write('# Emails Outreach — Lista para enviar\n\n')
    f.write(f'Total: {len(top)} emails generados\n\n')
    f.write('**Instrucciones:**\n')
    f.write('1. Antes de enviar, edita el `From:` en cada .eml file con tu email real\n')
    f.write('2. Abre cada .eml en tu cliente (Apple Mail / Thunderbird / Outlook)\n')
    f.write('3. **MAX 5-10 por día** para evitar marca spam\n')
    f.write('4. Personaliza el body si el rol mencionado no encaja exactamente\n')
    f.write('5. After 3-5 días sin respuesta, follow-up 1 vez, luego abandona\n\n')
    f.write('---\n\n')
    f.write('| # | Email | HN author | Archivo |\n')
    f.write('|---|-------|-----------|---------|\n')
    for i, lead in enumerate(top, 1):
        email_addr = lead['email']
        author = lead.get('author','?')
        safe_email = re.sub(r'[^A-Za-z0-9._-]', '_', email_addr)
        fn = f'{i:02d}_{safe_email}.eml'
        f.write(f'| {i} | `{email_addr}` | {author} | `{fn}` |\n')

print(f'\nGenerados {len(top)} emails en {out_dir}/')
print(f'Manifest: {manifest}')
print(f'\nPrimeros 10 emails:')
for l in manifest_lines[:10]:
    print(f'  {l}')
