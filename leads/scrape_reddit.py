#!/usr/bin/env python3
"""Scrape Reddit RSS with proper headers (Accept, Accept-Encoding)."""
import urllib.request, urllib.parse, time, re, json, sys, gzip, io
from xml.etree import ElementTree as ET

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
HEADERS = {
    "User-Agent": UA,
    "Accept": "application/atom+xml,application/xml,text/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
}
NS = {"atom": "http://www.w3.org/2005/Atom", "media": "http://search.yahoo.com/mrss/"}

QUERIES = [
    ("forhire", "hiring python", "python"),
    ("forhire", "AI agent", "ai_agent"),
    ("forhire", "FastAPI", "fastapi"),
    ("forhire", "Docker", "docker"),
    ("forhire", "freelance developer", "freelance"),
    ("forhire", "GitLab", "gitlab"),
    ("forhire", "automation", "automation"),
    ("forhire", "security audit", "security"),
    ("forhire", "LLM", "llm"),
    ("forhire", "telegram bot", "telegram"),
    ("forhire", "remote", "remote"),
    ("freelance", "Hiring", "freelance_hire"),
    ("freelance", "Wanted", "freelance_wanted"),
    ("freelance", "Python", "freelance_py"),
    ("freelance", "developer", "freelance_dev"),
    ("ProgrammingBuddies", "Paid", "paid"),
    ("ProgrammingBuddies", "Python", "progbuddies_py"),
    ("learnpython", "freelance", "learnpy_free"),
    ("learnpython", "help project pay", "learnpy_pay"),
    ("SaaS", "looking for", "saas_looking"),
    ("SaaS", "contractor", "saas_contractor"),
    ("SaaS", "co-founder", "saas_cofounder"),
    ("MLJobs", "contract", "mljobs_contract"),
    ("MLJobs", "remote", "mljobs_remote"),
    ("artificial", "looking for", "artificial_looking"),
    ("artificial", "hiring", "artificial_hire"),
    ("devops", "contract", "devops_contract"),
    ("devops", "freelance", "devops_free"),
    ("MachineLearning", "looking for", "ml_looking"),
    ("MachineLearning", "freelance", "ml_free"),
    ("startups", "looking for developer", "startups_dev"),
    ("Entrepreneur", "looking for developer", "ent_dev"),
    ("LocalLLaMA", "hiring", "locallama_hire"),
    ("LocalLLaMA", "looking for", "locallama_looking"),
    ("mlops", "looking for", "mlops_looking"),
    ("freeCodeCamp", "freelance", "fcc_free"),
    ("ecz", "desarrollador", "ecz_dev"),
    ("comunidadecuatoriana", "desarrollador", "ecuador_dev"),
    ("LATAMPROGRAMMERS", "freelance", "latam_free"),
    ("ProgramacionES", "freelance", "proges_free"),
]

def fetch(sub, q):
    url = f"https://www.reddit.com/r/{sub}/search.rss?{urllib.parse.urlencode({'q':q,'restrict_sr':1,'sort':'new','t':'year','limit':25})}"
    req = urllib.request.Request(url, headers=HEADERS)
    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
                if r.headers.get('Content-Encoding') == 'gzip':
                    data = gzip.decompress(data)
                return data.decode("utf-8", "ignore")
        except Exception as e:
            if attempt == 0:
                time.sleep(15)
                continue
            print(f"  err {sub}/{q!r}: {e}", file=sys.stderr)
            return ""

def parse(xml_text, sub, q, skill_hint):
    out = []
    if not xml_text.strip():
        return out
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as e:
        print(f"  parse err {sub}/{q!r}: {e}", file=sys.stderr)
        return out
    for entry in root.findall("atom:entry", NS):
        title_e = entry.find("atom:title", NS)
        title = title_e.text if title_e is not None else ""
        link_e = entry.find("atom:link", NS)
        link = link_e.get("href", "") if link_e is not None else ""
        if not link:
            # Search <content> for href to comment
            content_e = entry.find("atom:content", NS)
            content_html = content_e.text if content_e is not None else ""
            m = re.search(r'href="(https://www\.reddit\.com/r/[^"<]+/comments/[^"<]+)"', content_html or "")
            if m: link = m.group(1)
        author_e = entry.find("atom:author/atom:name", NS)
        author = author_e.text if author_e is not None else ""
        pub_e = entry.find("atom:published", NS)
        published = pub_e.text if pub_e is not None else ""
        content_e = entry.find("atom:content", NS)
        content_html = content_e.text if content_e is not None else ""
        content = re.sub(r"<[^>]+>", " ", content_html)
        content = re.sub(r"&[a-z]+;", " ", content)
        content = re.sub(r"\s+", " ", content).strip()
        out.append({
            "subreddit": sub,
            "query": q,
            "skill_hint": skill_hint,
            "title": title.strip(),
            "author": author.strip(),
            "url": link.strip(),
            "published": published,
            "snippet": content[:600]
        })
    return out

results = []
for i, (sub, q, hint) in enumerate(QUERIES):
    print(f"[{i+1}/{len(QUERIES)}] r/{sub} q={q!r} hint={hint}", file=sys.stderr)
    xml = fetch(sub, q)
    parsed = parse(xml, sub, q, hint)
    print(f"  got {len(parsed)} entries", file=sys.stderr)
    results.extend(parsed)
    time.sleep(6)  # ~6s throttle to avoid 429
    if (i + 1) % 4 == 0:
        with open("/home/z/my-project/leads/reddit_leads.json", "w") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

# Dedupe by URL
seen = set()
deduped = []
for r in results:
    if r["url"] and r["url"] not in seen:
        seen.add(r["url"])
        deduped.append(r)

with open("/home/z/my-project/leads/reddit_leads.json", "w") as f:
    json.dump(deduped, f, indent=2, ensure_ascii=False)
print(f"\nReddit: {len(results)} hits, {len(deduped)} unique URLs", file=sys.stderr)
