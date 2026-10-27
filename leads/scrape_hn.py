#!/usr/bin/env python3
"""Scrape HackerNews Who's Hiring threads via Algolia API (fast version)."""
import urllib.request, urllib.parse, json, time, re, sys

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

WHO_HIRING_THREADS = [
    ("October 2026", 49922569),
    ("September 2026", 49522897),
]

# Streamlined keywords - the most distinctive for the LLC
SKILL_KEYWORDS = {
    "python": ["python"],
    "ai_agent": ["ai agent", "agent", "agentic", "llm agent", "agent framework"],
    "fastapi": ["fastapi"],
    "docker": ["docker", "container"],
    "gitlab": ["gitlab"],
    "github_automation": ["github actions", "github bot"],
    "security": ["security", "sandbox", "audit"],
    "llm": ["llm", "anthropic", "gpt", "claude", "rag"],
    "telegram": ["telegram bot"],
    "remote": ["remote"],
    "contract": ["contract", "freelance", "contractor", "consulting"],
}

def search_hn(query, story_id=None, hits=50):
    params = {"query": query, "tags": "comment", "hitsPerPage": hits}
    if story_id:
        params["tags"] = f"comment,story_{story_id}"
    url = "https://hn.algolia.com/api/v1/search?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"  err: {e}", file=sys.stderr)
        return {"hits": [], "nbHits": 0}

results = []
for thread_name, story_id in WHO_HIRING_THREADS:
    print(f"\n=== {thread_name} ({story_id}) ===", file=sys.stderr)
    for skill, kws in SKILL_KEYWORDS.items():
        for kw in kws:
            d = search_hn(kw, story_id=story_id, hits=50)
            added = 0
            for h in d.get("hits", []):
                results.append({
                    "thread": thread_name,
                    "thread_id": story_id,
                    "skill": skill,
                    "keyword_matched": kw,
                    "comment_id": h.get("objectID"),
                    "author": h.get("author"),
                    "comment_text": (h.get("comment_text") or "")[:1200],
                    "comment_url": f"https://news.ycombinator.com/item?id={h.get('objectID')}",
                    "created_at": h.get("created_at"),
                    "story_title": h.get("story_title"),
                    "points": h.get("points"),
                })
                added += 1
            if added:
                print(f"  {skill}/{kw!r}: +{added}", file=sys.stderr)
            # Save progress after every search
            with open("/home/z/my-project/leads/hn_leads.json", "w") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)

# Dedupe by comment_id
seen = set()
deduped = []
for r in results:
    if r["comment_id"] not in seen:
        seen.add(r["comment_id"])
        deduped.append(r)

with open("/home/z/my-project/leads/hn_leads.json", "w") as f:
    json.dump(deduped, f, indent=2, ensure_ascii=False)
print(f"\nHN: {len(results)} hits, {len(deduped)} unique", file=sys.stderr)
