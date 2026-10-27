#!/usr/bin/env python3
"""Fetch all comments of HN thread 49922569 (Oct 2026 Who is hiring) and filter
roles matching the LLC skill profile."""
import json, urllib.request, time, re, html
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

STORY_ID = 49922569
OUT_DIR = Path("/home/z/my-project/jobboards/hn")
OUT_DIR.mkdir(parents=True, exist_ok=True)
RAW = OUT_DIR / "comments.json"
OUT = OUT_DIR / "filtered.json"
OUT_MD = OUT_DIR / "matches.md"

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()

def fetch_item(item_id):
    try:
        data = json.loads(fetch(f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"))
        return data
    except Exception as e:
        return {"id": item_id, "error": str(e)}

SKILLS = {
    "ai_agent": ["ai agent", "ai agents", "llm", "agent framework", "langchain",
                 "multi-agent", "mcp server", "model context protocol", "rag",
                 "agentic", "genai", "gen ai"],
    "python": ["python", "fastapi", "pydantic", "asyncio", "uvicorn", "celery",
               "django", "flask"],
    "docker": ["docker", "container", "kubernetes", "k8s"],
    "gitlab": ["gitlab"],
    "github": ["github actions", "github api", "gh cli"],
    "webhook": ["webhook", "event-driven", "event driven"],
    "security": ["security", "sandbox", "sandboxing", "tamper", "provenance",
                 "secret scanning", "vulnerability", "infosec", "appsec"],
    "automation": ["automation", "ci/cd", "ci cd", "pipeline", "devops",
                   "platform engineer", "sre"],
    "backend": ["backend", "back-end", "fullstack", "full-stack"],
    "contract": ["contract", "freelance", "part-time", "part time", "b2b",
                 "consulting", "consultant", "fractional"],
}

def score(text):
    ntext = text.lower()
    matched = []
    for skill, kws in SKILLS.items():
        if any(kw in ntext for kw in kws):
            matched.append(skill)
    core = {"ai_agent", "python", "gitlab", "github", "security", "automation",
            "docker", "webhook"}
    core_hits = [s for s in matched if s in core]
    score = 1
    if len(core_hits) >= 5: score = 5
    elif len(core_hits) >= 3: score = 4
    elif len(core_hits) >= 2: score = 3
    elif len(core_hits) >= 1: score = 2
    if "contract" in matched: score = min(5, score + 1)
    return score, matched, core_hits

def extract_meta(text):
    # Try to detect company, contact, location
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    company = ""
    email = ""
    location = ""
    # Usually first non-empty line is "Company Name | Location | Remote/Onsite"
    first_line = lines[0] if lines else ""
    # Email
    m = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    if m:
        email = m.group(0)
    # Remote keyword
    remote = "remote" in text.lower() or "anywhere" in text.lower()
    return first_line, email, remote

def main():
    story = json.load(open(OUT_DIR / "oct2026_story.json"))
    kids = story.get("kids", [])
    print(f"Fetching {len(kids)} top-level comments…")
    comments = []
    with ThreadPoolExecutor(max_workers=20) as ex:
        futures = {ex.submit(fetch_item, k): k for k in kids}
        for i, fut in enumerate(as_completed(futures)):
            r = fut.result()
            if r and r.get("text") is not None:
                comments.append(r)
            if (i + 1) % 50 == 0:
                print(f"  {i+1}/{len(kids)} fetched")
    print(f"Fetched {len(comments)} comments with text")
    json.dump(comments, open(RAW, "w"), indent=2)
    results = []
    for c in comments:
        text = html.unescape(c.get("text", ""))
        text_plain = re.sub(r"<[^>]+>", " ", text)
        text_plain = re.sub(r"\s+", " ", text_plain).strip()
        sc, matched, core_hits = score(text_plain)
        if sc >= 3:
            first_line, email, remote = extract_meta(text_plain)
            results.append({
                "id": c.get("id"),
                "user": c.get("by"),
                "time": c.get("time"),
                "first_line": first_line,
                "email": email,
                "remote": remote,
                "matched_skills": matched,
                "core_hits": core_hits,
                "match_score": sc,
                "url": f"https://news.ycombinator.com/item?id={c.get('id')}",
                "text_excerpt": text_plain[:600],
            })
    results.sort(key=lambda x: (-x["match_score"], -x["time"]))
    json.dump(results, open(OUT, "w"), indent=2, ensure_ascii=False)
    print(f"Saved {len(results)} matched HN comments to {OUT}")
    with open(OUT_MD, "w") as f:
        f.write(f"# HN Ask HN: Who is hiring? (Oct 2026) matches ({len(results)})\n\n")
        for r in results[:60]:
            f.write(f"## {r['first_line'][:120]}  (★{r['match_score']})\n")
            f.write(f"- **User:** {r['user']} | **Comment ID:** {r['id']}\n")
            f.write(f"- **Remote:** {'yes' if r['remote'] else 'unspecified'} | **Email:** {r['email'] or 'n/a'}\n")
            f.write(f"- **Matched:** {', '.join(r['matched_skills'])}\n")
            f.write(f"- **URL:** {r['url']}\n")
            f.write(f"- **Excerpt:** {r['text_excerpt'][:400]}…\n\n")
    print(f"Markdown saved to {OUT_MD}")

if __name__ == "__main__":
    main()
