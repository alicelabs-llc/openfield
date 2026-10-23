#!/usr/bin/env python3
"""
Verify status of all PRs where we sent pings.
Check for: new comments, reviews, status changes (merged/closed), CI status.
"""
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone

# PRs from worklog + summary we pinged or are waiting on
PRS = [
    # Active PRs from summary
    ("basitalisandhu/agent-security-skills", 32),
    ("aniruddhaadak80/skills", 471),
    ("basitalisandhu/mcp-egress", 28),
    ("devilking7x/skillbadge", 4),
    ("Spotflow-One/new-spotflow-docs", 85),
    ("vieanderes/understory", 72),
    ("jbilcke-hf/clapper", 163),
    ("Parabola-org/parabola", 131),
    ("Chain-Love/chain-love", 4483),
    # Older Hacktoberfest PRs
    ("Ergane-Foundation/vajra", 37),
    ("Ishannaik/harbour", 57),
    ("NovaCode37/Prism-platform", 554),
    # Marketing awesome-list PRs
    ("stacklok/toolhive-catalog", 1619),
    ("docker/mcp-registry", 5175),
    ("CodeSigils/awesome-agent-trust", 52),
    ("useagenthq/useagent", 84),
]

def gh_get(url):
    """Anonymous GitHub API GET (60/hour limit)."""
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "eddyflores100-lang-bot"
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"_error": f"HTTP {e.code}", "_url": url}
    except Exception as e:
        return {"_error": str(e), "_url": url}

def parse_dt(s):
    if not s or s.startswith("_"):
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except:
        return None

def fmt_age(dt):
    if not dt:
        return "?"
    now = datetime.now(timezone.utc)
    age = now - dt
    days = age.days
    if days == 0:
        hours = int(age.seconds / 3600)
        return f"{hours}h ago"
    return f"{days}d ago"

results = []
for repo, num in PRS:
    print(f"\n--- {repo}#{num} ---")
    pr = gh_get(f"https://api.github.com/repos/{repo}/pulls/{num}")
    if "_error" in pr:
        print(f"  ERROR: {pr['_error']}")
        results.append((repo, num, "ERROR", pr["_error"]))
        continue
    
    state = pr.get("state", "?")
    merged = pr.get("merged", False)
    merged_at = pr.get("merged_at")
    updated = pr.get("updated_at")
    title = pr.get("title", "?")[:80]
    
    # Get last 5 comments
    comments = gh_get(f"https://api.github.com/repos/{repo}/issues/{num}/comments?per_page=100")
    last_comments = []
    if isinstance(comments, list):
        last_comments = comments[-5:] if len(comments) > 5 else comments
    
    # Get reviews
    reviews = gh_get(f"https://api.github.com/repos/{repo}/pulls/{num}/reviews?per_page=50")
    last_reviews = []
    if isinstance(reviews, list):
        last_reviews = reviews[-3:] if len(reviews) > 3 else reviews
    
    print(f"  Title: {title}")
    print(f"  State: {state} | Merged: {merged} | Updated: {fmt_age(parse_dt(updated))}")
    if merged_at:
        print(f"  Merged at: {merged_at}")
    print(f"  Comments: {len(comments) if isinstance(comments, list) else '?'} | Reviews: {len(reviews) if isinstance(reviews, list) else '?'}")
    
    # Show last 3 comments/reviews with author + date
    for c in last_comments[-3:]:
        user = c.get("user", {}).get("login", "?")
        body = (c.get("body") or "")[:200].replace("\n", " ")
        created = c.get("created_at", "?")
        print(f"  💬 [{fmt_age(parse_dt(created))}] @{user}: {body}")
    
    for r in last_reviews[-2:]:
        user = r.get("user", {}).get("login", "?")
        state_r = r.get("state", "?")
        body = (r.get("body") or "")[:200].replace("\n", " ")
        submitted = r.get("submitted_at", "?")
        print(f"  🔍 [{fmt_age(parse_dt(submitted))}] @{user} ({state_r}): {body}")
    
    results.append((repo, num, state, "merged" if merged else "open", fmt_age(parse_dt(updated))))

print("\n\n=== SUMMARY ===")
for r in results:
    print(f"  {r[0]}#{r[1]}: {r[2]}/{r[3]} updated {r[4]}")
