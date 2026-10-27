"""
Extrae todos los emails visibles en HN comments + el texto del comentario del autor
para personalizar el outreach. Output: JSON con {email, author, comment_url, comment_text, match_score}
"""
import json
import re
import os
from pathlib import Path

EMAIL_RE = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')

# Keywords para match scoring con LLC skills
SKILL_KEYWORDS = [
    'python', 'fastapi', 'docker', 'sandbox', 'agent', 'ai', 'ml', 'llm',
    'automation', 'security', 'backend', 'devops', 'gitlab', 'github',
    'mcp', 'claude', 'openai', 'gpt', 'rust', 'infrastructure', 'platform',
    'remote', 'contract', 'freelance', 'consultant'
]

EXCLUDE_DOMAINS = {'ycombinator.com', 'example.com', 'sentry.io', 'next.security'}
EXCLUDE_LOCAL = {'noreply', 'no-reply', 'donotreply', 'unsubscribe', 'mailer'}

def is_relevant(email: str) -> bool:
    e = email.lower()
    local, _, domain = e.partition('@')
    if domain in EXCLUDE_DOMAINS:
        return False
    if local in EXCLUDE_LOCAL:
        return False
    if e.endswith(('.png','.jpg','.jpeg','.gif','.css','.js','.svg')):
        return False
    if 'ycombinator' in e:
        return False
    return True

def score_comment(text: str) -> int:
    if not text:
        return 0
    t = text.lower()
    score = 0
    for kw in SKILL_KEYWORDS:
        if kw in t:
            score += 1
    return score

# Cargar HN data
all_leads = []
for fn in ['leads-scrape/hn-oct-all.json', 'leads-scrape/hn-sept-comments.json', 'leads-scrape/hn-oct-comments.json']:
    p = Path('/home/z/my-project') / fn
    if not p.exists():
        continue
    with open(p) as f:
        data = json.load(f)
    
    # HN data structures vary. Walk everything.
    def walk(obj):
        if isinstance(obj, dict):
            # Check if this dict looks like a comment
            text_fields = []
            author = None
            url = None
            for k, v in obj.items():
                if k in ('text', 'comment_text', 'story_text', 'content') and isinstance(v, str):
                    text_fields.append(v)
                if k in ('author', 'by', 'username') and isinstance(v, str):
                    author = v
                if k in ('url', 'link', 'id') and isinstance(v, (str, int)):
                    if isinstance(v, str) and v.startswith('http'):
                        url = v
                    elif k == 'id' and isinstance(v, int):
                        url = f'https://news.ycombinator.com/item?id={v}'
                walk(v)
            if text_fields:
                combined = ' '.join(text_fields)
                emails = EMAIL_RE.findall(combined)
                for em in set(emails):
                    if is_relevant(em):
                        all_leads.append({
                            'email': em,
                            'author': author,
                            'url': url,
                            'comment_text': combined[:2000],
                            'source_file': fn
                        })
            else:
                for k, v in obj.items():
                    walk(v)
        elif isinstance(obj, list):
            for v in obj:
                walk(v)
    walk(data)

# Dedupe by email, keep first
seen = {}
for lead in all_leads:
    e = lead['email'].lower()
    if e not in seen:
        lead['match_score'] = score_comment(lead.get('comment_text', ''))
        seen[e] = lead

# Sort by match score
ranked = sorted(seen.values(), key=lambda x: -x['match_score'])

# Save
out = '/home/z/my-project/scripts/email_leads.json'
with open(out, 'w') as f:
    json.dump(ranked, f, indent=2, ensure_ascii=False)

# Print top 30 with their emails
print(f'Total relevant emails: {len(ranked)}')
print(f'Saved to {out}')
print()
print('=== TOP 30 LEADS BY MATCH SCORE ===')
for i, lead in enumerate(ranked[:30], 1):
    snippet = (lead.get('comment_text','')[:160].replace('\n',' ') + '...') if lead.get('comment_text') else ''
    print(f'{i:2}. [{lead["match_score"]:2}] {lead["email"]}')
    print(f'    author: {lead.get("author","?")}')
    print(f'    url: {lead.get("url","?")}')
    print(f'    text: {snippet}')
    print()
