#!/usr/bin/env python3
"""Parse HN Who is Hiring Oct 2026 thread comments and extract job postings."""
import json, re, os, glob
from pathlib import Path

RAW = Path('/home/z/my-project/freelance-scout/raw')
OUT = Path('/home/z/my-project/freelance-scout/hn-jobs.json')

SKILL_KEYWORDS = [
    'python', 'typescript', 'javascript', 'next.js', 'nextjs', 'react',
    'fastapi', 'flask', 'django', 'mcp', 'model context protocol', 'ai agent',
    'llm', 'openai', 'anthropic', 'claude', 'gpt', 'automation', 'rust',
    'alexa', 'stripe', 'api', 'web app', 'security audit', 'devsecops',
    'remote', 'contract', 'freelance', 'part-time', 'consultant',
]

KEYWORD_FILES = {
    'python': 'hn-oct2026-Python.json',
    'typescript': 'hn-oct2026-TypeScript.json',
    'nextjs': 'hn-oct2026-Next.js.json',
    'fastapi': 'hn-oct2026-FastAPI.json',
    'mcp': 'hn-oct2026-MCP.json',
    'aiagent': 'hn-oct2026-AI_agent.json',
    'llmintegration': 'hn-oct2026-LLM_integration.json',
    'automation': 'hn-oct2026-automation.json',
    'llm': 'hn-oct2026-LLM.json',
    'openai': 'hn-oct2026-OpenAI.json',
    'rust': 'hn-oct2026-Rust.json',
    'apidev': 'hn-oct2026-API_development.json',
}

seen_ids = set()
jobs = []

for kw, fname in KEYWORD_FILES.items():
    fp = RAW / fname
    if not fp.exists():
        continue
    try:
        data = json.loads(fp.read_text())
    except Exception as e:
        print(f'  ! parse error {fname}: {e}')
        continue
    for hit in data.get('hits', []):
        cid = hit.get('objectID')
        if not cid or cid in seen_ids:
            continue
        seen_ids.add(cid)
        text = hit.get('comment_text') or hit.get('story_text') or ''
        # Strip HTML
        text_clean = re.sub(r'<[^>]+>', ' ', text)
        text_clean = re.sub(r'\s+', ' ', text_clean).strip()
        # Only keep comments that look like job postings:
        # - Mention Remote/Onsite/Office location pattern OR
        # - Have a URL/email contact OR
        # - Mention keywords like hiring, full-time, contract, etc.
        post_lower = text_clean.lower()
        is_job = any(s in post_lower for s in [
            'remote', 'onsite', 'hybrid', 'hiring', 'full-time', 'full time',
            'part-time', 'part time', 'contract', 'freelance', 'contractor',
            'internship', 'applying', 'email', '@', 'cv ', 'resume', 'apply',
            'salary', 'compensation', 'usd', 'eur', 'k year', '/year', '/hr',
            'per hour', '€', '$', 'k/yr', 'k/yr',
        ])
        if not is_job:
            continue
        # Match at least one of our skills
        skill_hits = [k for k in SKILL_KEYWORDS if k in post_lower]
        if not skill_hits:
            continue
        # Skip if the comment is short (likely not a real posting)
        if len(text_clean) < 100:
            continue
        # Try to extract first line as title (often "Company | Role | Location")
        first_line = text_clean.split('. ')[0][:300] if text_clean else ''
        jobs.append({
            'id': cid,
            'author': hit.get('author'),
            'created_at': hit.get('created_at'),
            'first_line': first_line,
            'text': text_clean[:2000],
            'url': f"https://news.ycombinator.com/item?id={cid}",
            'skills_matched': skill_hits,
            'query_match': kw,
        })

# Sort by date desc
jobs.sort(key=lambda x: x.get('created_at', ''), reverse=True)
OUT.write_text(json.dumps(jobs, indent=2, ensure_ascii=False))
print(f'Total unique job-like comments: {len(jobs)}')
for j in jobs[:30]:
    print(f"- [{j['created_at'][:10]}] {j['first_line'][:130]}")
    print(f"  skills: {j['skills_matched'][:5]}")
    print(f"  {j['url']}")
