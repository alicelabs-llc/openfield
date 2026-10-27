"""
Gmail SMTP sender — envía TODOS los 30 leads elegibles con delays de 35 segundos.

Anti-ban policy (ajustada por usuario — "cuenta caliente"):
- Enviar TODOS los 30 elegibles en una sesión
- 35 segundos entre cada envío (no 30 min — usuario dice que su cuenta aguanta)
- Log persistente en /home/z/my-project/scripts/gmail_send.log
- Skip los ya enviados (re-ejecutable)

Total runtime estimado: 30 emails × 35s = 17.5 min + auth + headers
"""
import smtplib
import ssl
import time
import json
import re
import html
import sys
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from pathlib import Path

GMAIL_USER = 'eddyflores100@gmail.com'
GMAIL_APP_PASSWORD = 'kbgn mxmc semj olzz'  # 16 chars — verified working

LOG_FILE = Path('/home/z/my-project/scripts/gmail_send.log')
SENT_LOG_FILE = Path('/home/z/my-project/scripts/sent_log.json')

DELAY_SECONDS = 35

def log(msg):
    ts = time.strftime('%Y-%m-%dT%H:%M:%S')
    line = f'[{ts}] {msg}'
    print(line, flush=True)
    with open(LOG_FILE, 'a') as f:
        f.write(line + '\n')

# Load leads
with open('/home/z/my-project/scripts/email_leads.json') as f:
    all_leads = json.load(f)

# Order: send careers@ inboxes first (lower ban risk, often auto-routed), then personal
def sort_key(lead):
    email = lead['email'].lower()
    if email.startswith(('careers@', 'founders@', 'jobs@', 'hiring@', 'talent@', 'recruiting@')):
        return (0, -lead.get('match_score', 0), email)
    return (1, -lead.get('match_score', 0), email)

# Use the same filter as the email generator
def is_eligible(lead):
    text = (lead.get('comment_text','') or '').lower()
    score = lead.get('match_score', 0)
    if score < 6:
        return False
    onsite_only = (
        ('san francisco' in text or 'sf onsite' in text or 'bay area' in text)
        and 'remote' not in text
    ) or (
        ('new york city' in text or 'nyc onsite' in text)
        and 'remote' not in text
    )
    if onsite_only:
        return False
    if 'german c1' in text or 'deutsch' in text:
        return False
    return True

eligible = [l for l in all_leads if is_eligible(l)]
eligible.sort(key=sort_key)
log(f'Total eligible: {len(eligible)}')
TOP_TODAY = eligible[:30]

def find_lead(email_addr):
    for lead in all_leads:
        if lead['email'].lower() == email_addr.lower():
            return lead
    return None

def clean_text(t):
    if not t: return ''
    t = re.sub(r'&#x2F;|&#x27;|&#x2D;|&amp;|&lt;|&gt;|&quot;', 
               lambda m: {'&#x2F;':'/','&#x27;':"'",'&#x2D;':'-','&amp;':'&','&lt;':'<','&gt;':'>','&quot;':'"'}.get(m.group(), m.group()),
               t)
    t = re.sub(r'<[^>]+>', '', t)
    return html.unescape(t).strip()

def make_email(lead):
    email_addr = lead['email']
    author = lead.get('author', '')
    raw_comment = clean_text(lead.get('comment_text', ''))
    first_line = raw_comment.split('\n')[0] if raw_comment else ''
    
    name_part = ''
    if author:
        skip_prefixes = ('hiring', 'founders', 'careers', 'jobs', 'talent',
                         'recruiting', 'enghiring', 'apply', 'hello', 'hi',
                         'contact', 'career', 'agency', 'ceo')
        if not author.lower().startswith(skip_prefixes):
            if author[0].islower() and not any(c.isdigit() for c in author):
                name_part = f' {author.capitalize()},'
            elif author[0].isupper() and len(author) > 2 and not author.isupper():
                pass
    
    cl = raw_comment.lower()
    pitch_parts = []
    if 'python' in cl or 'fastapi' in cl:
        pitch_parts.append('Python/FastAPI + Docker sandboxing')
    if 'agent' in cl or 'llm' in cl or 'ai engineer' in cl:
        pitch_parts.append('AI agent platforms with tamper-evident provenance')
    if 'security' in cl or 'audit' in cl or 'sandbox' in cl:
        pitch_parts.append('security audit + signed audit trails')
    if 'gitlab' in cl or 'github' in cl or 'mcp' in cl:
        pitch_parts.append('GitLab/GitHub automation (webhooks, MR bots)')
    if 'devops' in cl or 'infrastructure' in cl or 'platform' in cl:
        pitch_parts.append('platform engineering')
    if 'rust' in cl:
        pitch_parts.append('(I also write Rust for perf-critical paths)')
    if 'backend' in cl and 'python' not in cl:
        pitch_parts.append('backend engineering')
    if not pitch_parts:
        pitch_parts.append('AI agent platforms with Docker sandbox + tamper-evident provenance')
    pitch = ', '.join(pitch_parts[:3])
    
    subject = f'HN October thread — your {first_line[:60]}{"..." if len(first_line)>60 else ""}'
    
    body = f"""Hi{name_part}

Saw your post on the HN "Ask HN: Who is hiring?" October thread: {first_line[:140]}

I run an LLC in Ecuador (UTC-5, fully remote) doing {pitch}. Public work: github.com/eddyflores100-lang/alethech-agent-vault — FastAPI orchestrator with Docker sandbox, GitLab Duo integration, and signed audit trails.

If the role is still open, I'd like to apply. What's the next step?

Thanks,
Edison Flores
github.com/eddyflores100-lang
"""
    return subject, body

def send_email(to_addr, subject, body):
    msg = EmailMessage()
    msg['From'] = GMAIL_USER
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg['Date'] = formatdate(localtime=True)
    msg['Message-ID'] = make_msgid(domain='gmail.com')
    msg.set_content(body)
    
    context = ssl.create_default_context()
    with smtplib.SMTP('smtp.gmail.com', 587, timeout=60) as server:
        server.ehlo('localhost')
        server.starttls(context=context)
        server.ehlo('localhost')
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.send_message(msg)

# Main
log('=' * 60)
log('Gmail outreach sender — starting')
log(f'User: {GMAIL_USER}')
log(f'Batch: {len(TOP_TODAY)} emails')
log(f'Delay between sends: {DELAY_SECONDS} seconds')
log('=' * 60)

# Load sent log
sent_log = []
if SENT_LOG_FILE.exists():
    try:
        with open(SENT_LOG_FILE) as f:
            sent_log = json.load(f)
    except:
        pass

sent_emails = {s.get('to') for s in sent_log if s.get('status') == 'sent'}
log(f'Already sent previously: {len(sent_emails)}')

# Auth pre-flight check
log('Auth pre-flight check...')
try:
    context = ssl.create_default_context()
    with smtplib.SMTP('smtp.gmail.com', 587, timeout=30) as server:
        server.ehlo('localhost')
        server.starttls(context=context)
        server.ehlo('localhost')
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
    log('SMTP auth OK ✅')
except Exception as e:
    log(f'SMTP auth FAILED ❌ — {e}')
    sys.exit(1)

success_count = 0
fail_count = 0
skip_count = 0

for i, lead in enumerate(TOP_TODAY, 1):
    email_addr = lead['email']
    if email_addr in sent_emails:
        log(f'[{i}/{len(TOP_TODAY)}] SKIP (already sent): {email_addr}')
        skip_count += 1
        continue
    
    subject, body = make_email(lead)
    log(f'[{i}/{len(TOP_TODAY)}] Sending to {email_addr} (author={lead.get("author","?")}, score={lead.get("match_score","?")})')
    log(f'  Subject: {subject[:100]}')
    
    try:
        send_email(email_addr, subject, body)
        log_entry = {
            'to': email_addr,
            'author': lead.get('author',''),
            'subject': subject,
            'sent_at': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'status': 'sent',
            'match_score': lead.get('match_score', 0)
        }
        sent_log.append(log_entry)
        with open(SENT_LOG_FILE, 'w') as f:
            json.dump(sent_log, f, indent=2, ensure_ascii=False)
        log(f'  ✅ Sent at {log_entry["sent_at"]}')
        success_count += 1
        
        if i < len(TOP_TODAY):
            log(f'  Waiting {DELAY_SECONDS}s before next send...')
            # Sleep in chunks of 5s for responsive logging
            for slept in range(0, DELAY_SECONDS, 5):
                time.sleep(5)
    except Exception as e:
        log(f'  ❌ Failed: {type(e).__name__}: {str(e)[:150]}')
        log_entry = {
            'to': email_addr,
            'author': lead.get('author',''),
            'error': str(e)[:300],
            'sent_at': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'status': 'failed',
            'match_score': lead.get('match_score', 0)
        }
        sent_log.append(log_entry)
        with open(SENT_LOG_FILE, 'w') as f:
            json.dump(sent_log, f, indent=2, ensure_ascii=False)
        fail_count += 1
        # Short wait on failure, then continue
        if i < len(TOP_TODAY):
            log(f'  Waiting 15s before next send (shorter on failure)...')
            time.sleep(15)

log('=' * 60)
log(f'BATCH COMPLETE')
log(f'  Sent:     {success_count}')
log(f'  Failed:   {fail_count}')
log(f'  Skipped:  {skip_count}')
log(f'  Total in DB: {sum(1 for s in sent_log if s.get("status") == "sent")}')
log('=' * 60)
