#!/usr/bin/env python3
"""Check all open PRs for new maintainer activity (comments/reviews/state changes)."""
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone

TOKEN = "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"

PRS = [
    # Bounty PRs
    ("jbilcke-hf/clapper", 163, "$1,050 bounty"),
    ("Parabola-org/parabola", 131, "$105 bounty"),
    # Resubmit
    ("stacklok/toolhive-catalog", 1777, "resubmit"),
    # Older marketing
    ("docker/mcp-registry", 5175, "remote MCP"),
    ("CodeSigils/awesome-agent-trust", 52, "awesome-list"),
    # Recent Oct 23 PRs
    ("basitalisandhu/agent-security-skills", 32, "PERM-012"),
    ("aniruddhaadak80/skills", 471, "Ed25519"),
    ("basitalisandhu/mcp-egress", 28, "--report-out"),
    ("devilking7x/skillbadge", 4, "scanner"),
    ("Spotflow-One/new-spotflow-docs", 85, "webhook"),
    ("vieanderes/understory", 72, "Cloudflare feed"),
    ("Chain-Love/chain-love", 4483, "CI"),
    # Older Hacktoberfest
    ("Ergane-Foundation/vajra", 37, "macOS"),
    ("Ishannaik/harbour", 57, "control chars"),
    ("NovaCode37/Prism-platform", 554, "scan tests"),
]

def gh(url):
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "eddyflores100-lang-bot",
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"_error": f"HTTP {e.code}", "_body": e.read().decode()[:200]}
    except Exception as e:
        return {"_error": str(e)}

def fmt_age(s):
    if not s or s.startswith("_"):
        return "?"
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        age = datetime.now(timezone.utc) - dt
        d = age.days
        if d == 0:
            h = int(age.seconds / 3600)
            return f"{h}h"
        return f"{d}d"
    except:
        return "?"

print("=== PR STATUS CHECK ===\n")
changes_detected = []
for repo, num, label in PRS:
    pr = gh(f"https://api.github.com/repos/{repo}/pulls/{num}")
    if "_error" in pr:
        print(f"❌ {repo}#{num} ({label}): {pr['_body']}")
        continue
    
    state = pr.get("state", "?")
    merged = pr.get("merged", False)
    updated = pr.get("updated_at")
    age = fmt_age(updated)
    
    # Get comments
    comments = gh(f"https://api.github.com/repos/{repo}/issues/{num}/comments?per_page=100")
    n_comments = len(comments) if isinstance(comments, list) else 0
    
    # Get reviews
    reviews = gh(f"https://api.github.com/repos/{repo}/pulls/{num}/reviews?per_page=50")
    n_reviews = len(reviews) if isinstance(reviews, list) else 0
    
    status = "MERGED" if merged else state.upper()
    icon = "🎉" if merged else ("🟢" if state == "open" else "🔴")
    print(f"{icon} {repo}#{num} ({label}): {status} | {n_comments} comments | {n_reviews} reviews | updated {age}")
    
    # Show last 2 comments from non-eddy users
    if isinstance(comments, list):
        non_eddy = [c for c in comments if c.get("user", {}).get("login", "") != "eddyflores100-lang" and not c.get("user", {}).get("login", "").endswith("[bot]")]
        if non_eddy:
            last = non_eddy[-1]
            user = last.get("user", {}).get("login", "?")
            body = (last.get("body") or "")[:150].replace("\n", " ")
            print(f"     💬 Last non-eddy comment [{fmt_age(last.get('created_at'))}] @{user}: {body}")
            changes_detected.append((repo, num, user, fmt_age(last.get("created_at"))))
    
    # Show last review from non-eddy
    if isinstance(reviews, list):
        non_eddy_r = [r for r in reviews if r.get("user", {}).get("login", "") != "eddyflores100-lang" and not r.get("user", {}).get("login", "").endswith("[bot]")]
        if non_eddy_r:
            last_r = non_eddy_r[-1]
            user = last_r.get("user", {}).get("login", "?")
            state_r = last_r.get("state", "?")
            print(f"     🔍 Last review [{fmt_age(last_r.get('submitted_at'))}] @{user} ({state_r})")

print(f"\n=== Maintainer activity detected in {len(changes_detected)} PRs ===")
for r in changes_detected:
    print(f"  {r[0]}#{r[1]} — @{r[2]} replied {r[3]} ago")
