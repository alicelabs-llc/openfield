#!/usr/bin/env python3
"""
Comprehensive parser for all fetched freelance/job data sources.

Inputs:
  - HN Algolia JSON results (Oct 2026 + Sep 2026 Who is Hiring threads)
  - WeWorkRemotely RSS feeds (programming, backend, frontend, devops)
  - Freelancer.com RSS feeds (python, nextjs, aiagent, mcp, ts, automation, openai, api, stripe, llm, security, fastapi)
  - RemoteOK JSON API (100 entries)
  - Python.org jobs RSS

Output:
  - unified jobs list (JSON)
  - markdown table sorted by budget desc
"""
import json, re, os, glob, html
from pathlib import Path
from datetime import datetime, timezone

RAW = Path('/home/z/my-project/freelance-scout/raw')
OUT = Path('/home/z/my-project/freelance-scout/jobs-unified.json')
MD_OUT = Path('/home/z/my-project/freelance-scout/jobs-table.md')

# Skills we target (lowercase match)
TARGET_SKILLS = [
    ('python', 'Python'),
    ('typescript', 'TypeScript'),
    ('next.js', 'Next.js'),
    ('nextjs', 'Next.js'),
    ('react', 'React'),
    ('fastapi', 'FastAPI'),
    ('flask', 'Flask'),
    ('django', 'Django'),
    ('mcp', 'MCP'),
    ('model context protocol', 'MCP'),
    ('ai agent', 'AI agents'),
    ('ai-agent', 'AI agents'),
    ('llm', 'LLM'),
    ('openai', 'OpenAI'),
    ('anthropic', 'Anthropic'),
    ('claude', 'Claude'),
    ('gpt', 'GPT'),
    ('automation', 'Automation'),
    ('rust', 'Rust'),
    ('alexa', 'Alexa'),
    ('stripe', 'Stripe'),
    ('api', 'API'),
    ('web app', 'Web app'),
    ('security audit', 'Security audit'),
    ('security', 'Security'),
    ('devsecops', 'DevSecOps'),
    ('contract', 'Contract'),
    ('freelance', 'Freelance'),
    ('part-time', 'Part-time'),
    ('consultant', 'Consultant'),
    ('latam', 'LATAM'),
    ('remote worldwide', 'Worldwide'),
    ('worldwide', 'Worldwide'),
    ('anywhere', 'Worldwide'),
]

# Key skills that MUST be present (at least one) for the job to qualify
REQUIRED_SKILL_PATTERNS = [
    r'\bpython\b', r'\btypescript\b', r'\bnext\.?js\b', r'\breact\b',
    r'\bfastapi\b', r'\bflask\b', r'\bdjango\b', r'\bmcp\b',
    r'model context protocol', r'ai[- ]?agent', r'\bllm\b',
    r'openai', r'anthropic', r'\bclaude\b', r'\bgpt-?\d?\b',
    r'automation', r'\brust\b', r'alexa', r'stripe',
    r'security audit', r'devsecops',
]

def strip_html(text):
    if not text: return ''
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_skills(text):
    if not text: return []
    t = text.lower()
    found = set()
    for pat, label in TARGET_SKILLS:
        if pat in t:
            found.add(label)
    return sorted(found)

def matches_required(text):
    t = text.lower()
    for pat in REQUIRED_SKILL_PATTERNS:
        if re.search(pat, t):
            return True
    return False

def parse_budget(text):
    """Try to extract budget info from text. Returns dict with budget fields."""
    if not text: return None
    t = text
    budget = {}
    # Hourly rates: $30/hr, $50/hour, $30-$100/hr, etc.
    m = re.search(r'\$(\d{1,4})\s*(?:-|to|–)\s*\$?(\d{1,4})\s*/\s*(hr|hour|week|month)', t, re.I)
    if m:
        budget['rate_min'] = int(m.group(1))
        budget['rate_max'] = int(m.group(2))
        budget['rate_unit'] = m.group(3).lower()
        return budget
    m = re.search(r'\$(\d{2,4})\s*/\s*(hr|hour|week|month)', t, re.I)
    if m:
        budget['rate_min'] = int(m.group(1))
        budget['rate_max'] = int(m.group(1))
        budget['rate_unit'] = m.group(2).lower()
        return budget
    # Annual salary: $80K-$150K, $80,000 - $150,000
    m = re.search(r'\$(\d{2,3})\s*k\s*(?:-|to|–)\s*\$?(\d{2,3})\s*k', t, re.I)
    if m:
        budget['annual_min'] = int(m.group(1)) * 1000
        budget['annual_max'] = int(m.group(2)) * 1000
        return budget
    m = re.search(r'\$(\d{2,3})\s*k\b', t, re.I)
    if m:
        budget['annual_min'] = int(m.group(1)) * 1000
        budget['annual_max'] = int(m.group(1)) * 1000
        return budget
    # Fixed price: $500-$2000, $1,000, $5000
    m = re.search(r'\$(\d{1,3}(?:,\d{3})*|\d{3,6})\s*(?:-|to|–)\s*\$?(\d{1,3}(?:,\d{3})*|\d{3,6})', t)
    if m:
        def to_int(s): return int(s.replace(',', ''))
        budget['fixed_min'] = to_int(m.group(1))
        budget['fixed_max'] = to_int(m.group(2))
        return budget
    m = re.search(r'\$(\d{3,6})\b', t)
    if m:
        budget['fixed_min'] = int(m.group(1))
        budget['fixed_max'] = int(m.group(1))
        return budget
    # Salary in thousands e.g. "$100k-$200k USD"
    m = re.search(r'(\d{2,3})\s*[-–]\s*(\d{2,3})\s*k\s*usd', t, re.I)
    if m:
        budget['annual_min'] = int(m.group(1)) * 1000
        budget['annual_max'] = int(m.group(2)) * 1000
        return budget
    return None

def budget_score(budget):
    """Single number for sorting (estimated total or annual)."""
    if not budget: return 0
    if 'annual_min' in budget:
        return budget.get('annual_max', budget['annual_min'])
    if 'fixed_max' in budget:
        return budget.get('fixed_max', budget.get('fixed_min', 0))
    if 'rate_max' in budget:
        # estimate as 6 months at rate
        return budget.get('rate_max', 0) * 80  # ~80 hours/month * ... or rough
    return 0

def is_remote(text):
    if not text: return 'Unknown'
    t = text.lower()
    if 'remote worldwide' in t or 'worldwide' in t or 'global' in t or 'anywhere' in t:
        return 'Worldwide'
    if 'remote (us' in t or 'remote us' in t or 'u.s. only' in t or 'us only' in t or 'north america' in t:
        return 'US/North America only'
    if 'remote (eu' in t or 'europe only' in t or 'european union' in t:
        return 'Europe only'
    if 'remote (uk' in t or 'remote (cet' in t:
        return 'UK/Europe'
    if 'remote (latam' in t or 'latam' in t or 'latin america' in t:
        return 'LATAM'
    if 'remote (asia' in t or 'asia only' in t:
        return 'Asia only'
    if 'remote' in t:
        return 'Remote (specific region)'
    if 'onsite' in t:
        return 'Onsite'
    if 'hybrid' in t:
        return 'Hybrid'
    return 'Unknown'

def parse_hn_files(prefix):
    """Parse all HN files matching prefix pattern."""
    jobs = []
    seen_ids = set()
    for fp in RAW.glob(f'{prefix}*.json'):
        try:
            data = json.loads(fp.read_text())
        except Exception:
            continue
        for hit in data.get('hits', []):
            cid = hit.get('objectID')
            if not cid or cid in seen_ids:
                continue
            seen_ids.add(cid)
            text_raw = hit.get('comment_text') or hit.get('story_text') or ''
            text = strip_html(text_raw)
            if len(text) < 100:
                continue
            post_lower = text.lower()
            is_job = any(s in post_lower for s in [
                'remote', 'onsite', 'hybrid', 'hiring', 'full-time', 'full time',
                'part-time', 'part time', 'contract', 'freelance', 'contractor',
                'internship', 'applying', 'email', '@', 'cv ', 'resume', 'apply',
                'salary', 'compensation', 'usd', 'eur', '/year', '/hr',
                'per hour', '€', '$', 'k/yr',
            ])
            if not is_job:
                continue
            if not matches_required(text):
                continue
            first_line = text.split('. ')[0][:300] if text else ''
            # First 250 chars for description
            skills = extract_skills(text)
            budget = parse_budget(text)
            # Skip if no detectable budget OR no remote/contract mention
            is_remote_str = is_remote(text[:500])
            jobs.append({
                'source': 'HN Who is Hiring',
                'source_detail': f"Hacker News {prefix.split('-')[1].capitalize()} 2026 thread",
                'title': first_line.split('|')[0].strip()[:120] if '|' in first_line else first_line[:120],
                'company': first_line.split('|')[1].strip()[:60] if '|' in first_line else '',
                'description': first_line[:300],
                'full_text': text[:3000],
                'budget': budget,
                'budget_score': budget_score(budget),
                'skills_matched': skills,
                'remote': is_remote_str,
                'posted_date': hit.get('created_at', '')[:10],
                'url': f"https://news.ycombinator.com/item?id={cid}",
                'application_url': f"https://news.ycombinator.com/item?id={cid}",
                'author': hit.get('author', ''),
            })
    return jobs

def parse_rss_items(xml_path, source_name):
    """Parse generic RSS XML file."""
    import xml.etree.ElementTree as ET
    jobs = []
    try:
        tree = ET.parse(xml_path)
        items = tree.getroot().findall('.//item')
    except Exception as e:
        print(f'  ! parse_rss: {xml_path.name}: {e}')
        return jobs
    for item in items:
        title = item.findtext('title', '') or ''
        link = item.findtext('link', '') or ''
        pub = item.findtext('pubDate', '') or ''
        desc_raw = item.findtext('description', '') or ''
        desc = strip_html(desc_raw)
        text = f"{title}. {desc}"
        if len(text) < 30:
            continue
        if not matches_required(text):
            continue
        budget = parse_budget(text)
        skills = extract_skills(text)
        # First line of title for company
        company = ''
        if ':' in title:
            company = title.split(':')[0].strip()[:60]
        elif '|' in title:
            company = title.split('|')[0].strip()[:60]
        jobs.append({
            'source': source_name,
            'source_detail': xml_path.name,
            'title': title[:150],
            'company': company,
            'description': desc[:400] if desc else title,
            'full_text': text[:3000],
            'budget': budget,
            'budget_score': budget_score(budget),
            'skills_matched': skills,
            'remote': is_remote(text[:600]),
            'posted_date': pub,
            'url': link,
            'application_url': link,
            'author': '',
        })
    return jobs

def parse_remoteok_json():
    jobs = []
    fp = RAW / 'remoteok.json'
    if not fp.exists(): return jobs
    try:
        data = json.loads(fp.read_text())
    except Exception as e:
        print(f'  ! remoteok: {e}')
        return jobs
    if not isinstance(data, list): return jobs
    for item in data[1:]:  # skip meta first item
        if not isinstance(item, dict): continue
        position = item.get('position', '') or ''
        company = item.get('company', '') or ''
        tags = item.get('tags', []) or []
        text = f"{position} at {company}. Tags: {', '.join(tags)}. {item.get('description','')[:500]}"
        if not matches_required(text):
            continue
        budget = {
            'annual_min': item.get('salary_min'),
            'annual_max': item.get('salary_max'),
        } if item.get('salary_min') else parse_budget(text)
        # Validate budget > $500 fixed or > $30/hr hourly (or salary > $50K)
        skills = extract_skills(text) + [t for t in tags if t]
        skills = sorted(set(skills))
        epoch = item.get('epoch')
        posted = ''
        if epoch:
            try:
                posted = datetime.fromtimestamp(int(epoch), tz=timezone.utc).strftime('%Y-%m-%d')
            except Exception:
                posted = item.get('date', '')[:10]
        jobs.append({
            'source': 'RemoteOK',
            'source_detail': 'remoteok.com/api',
            'title': position[:150],
            'company': company,
            'description': strip_html(item.get('description', ''))[:400],
            'full_text': strip_html(item.get('description', ''))[:3000],
            'budget': budget,
            'budget_score': budget_score(budget),
            'skills_matched': skills,
            'remote': 'Worldwide' if 'remote' in tags or 'worldwide' in str(item).lower() else 'Unknown',
            'posted_date': posted,
            'url': item.get('url', ''),
            'application_url': item.get('url', ''),
            'author': company,
        })
    return jobs

def parse_pythonorg_jobs():
    jobs = []
    fp = RAW / 'pythonorg-jobs.rss'
    if not fp.exists(): return jobs
    import xml.etree.ElementTree as ET
    try:
        tree = ET.parse(fp)
        items = tree.getroot().findall('.//item')
    except Exception as e:
        print(f'  ! python.org: {e}')
        return jobs
    for item in items:
        title = item.findtext('title', '') or ''
        link = item.findtext('link', '') or ''
        pub = item.findtext('pubDate', '') or ''
        desc_raw = item.findtext('description', '') or ''
        desc = strip_html(desc_raw)
        text = f"{title}. {desc}"
        if not matches_required(text):
            continue
        # Parse company from title (after comma)
        company = ''
        if ',' in title:
            company = title.split(',')[-1].strip()[:60]
        # First line of desc is usually location
        loc_line = desc.split('\n')[0].strip() if desc else ''
        budget = parse_budget(text)
        jobs.append({
            'source': 'Python.org Jobs',
            'source_detail': 'python.org/jobs',
            'title': title[:150],
            'company': company,
            'description': desc[:400],
            'full_text': text[:3000],
            'budget': budget,
            'budget_score': budget_score(budget),
            'skills_matched': extract_skills(text),
            'remote': is_remote(loc_line) if loc_line else is_remote(text[:300]),
            'posted_date': pub or '',
            'url': link,
            'application_url': link,
            'author': company,
        })
    return jobs

# Run all parsers
all_jobs = []

print('Parsing HN Who is Hiring Oct 2026...')
all_jobs.extend(parse_hn_files('hn-oct2026'))

print('Parsing HN Who is Hiring Sep 2026...')
all_jobs.extend(parse_hn_files('hn-sep2026'))

print('Parsing WWR feeds...')
for f in ['wwr-programming.rss', 'wwr-backend.rss', 'wwr-frontend.rss', 'wwr-devops.rss', 'wwr-support.rss']:
    all_jobs.extend(parse_rss_items(RAW / f, 'WeWorkRemotely'))

print('Parsing Freelancer.com feeds...')
for f in sorted(RAW.glob('freelancer-*.xml')):
    all_jobs.extend(parse_rss_items(f, 'Freelancer.com'))

print('Parsing RemoteOK...')
all_jobs.extend(parse_remoteok_json())

print('Parsing Python.org jobs...')
all_jobs.extend(parse_pythonorg_jobs())

print(f'\nTotal raw matches: {len(all_jobs)}')

# De-duplicate by URL/title
seen = set()
deduped = []
for j in all_jobs:
    key = (j.get('url', ''), j.get('title', '')[:80].lower())
    if key in seen:
        continue
    seen.add(key)
    deduped.append(j)
print(f'After dedup: {len(deduped)}')

# Sort by budget score desc
deduped.sort(key=lambda x: x.get('budget_score', 0), reverse=True)

# Save full unified JSON
OUT.write_text(json.dumps(deduped, indent=2, ensure_ascii=False, default=str))
print(f'\nWrote {OUT}')

# Print top 60 by budget
print('\n=== TOP 60 by budget ===')
for i, j in enumerate(deduped[:60], 1):
    b = j.get('budget') or {}
    bstr = ''
    if b.get('annual_min'):
        bstr = f"${b['annual_min']//1000}K-${b.get('annual_max',0)//1000}K/yr"
    elif b.get('fixed_min'):
        bstr = f"${b['fixed_min']}-${b.get('fixed_max',0)} fixed"
    elif b.get('rate_min'):
        bstr = f"${b['rate_min']}-${b.get('rate_max',0)}/{b.get('rate_unit','hr')}"
    else:
        bstr = '(budget not visible)'
    print(f"{i:3}. [{j['source']}] {j['title'][:90]}")
    print(f"     Company: {j.get('company','')[:50]} | Budget: {bstr} | Remote: {j.get('remote','?')[:30]}")
    print(f"     Posted: {j.get('posted_date','?')[:30]} | Skills: {', '.join(j.get('skills_matched', [])[:6])}")
    print(f"     URL: {j.get('url','')}")
