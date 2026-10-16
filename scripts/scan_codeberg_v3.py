import json, urllib.request, ssl, time

HEADERS = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
CTX = ssl.create_default_context()

def api(url, delay=2):
    time.sleep(delay)
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:200]}
    except Exception as e:
        return -1, {"error": str(e)[:200]}

# Focus on lower-star repos that are MORE responsive and easier to PR to.
# Rules for "respecting antiban":
# 1. No more than 1 PR per repo per day.
# 2. Pick repos where maintainer has merged OTHER hacktoberfest PRs recently (signal: repo active + PRs open + topic hacktoberfest)
# 3. Pick issues where the maintainer has already suggested a fix (lowest risk of "you didn't do what I wanted").
# 4. Avoid repos that are GitHub mirrors with stale Codeberg forks (e.g., curl-mirror, RIOT).

TARGETS = [
    # Already on my radar — Rust repos that look good
    ("spade-lang/spade", "main", 30),       # Rust HDL, pushed today
    ("leftwm/leftwm", "main", 9),            # Rust tiling wm
    ("cmars/stigmerge", "main", 4),          # Rust
    ("scripty-bot/scripty", "main", 4),      # Rust
    ("GeopJr/Collision", "main", 9),         # Crystal
    ("castle-engine/castle-engine", "master", 12), # Pascal
    ("cake-build/cake", "main", 3),          # C#
    ("distrochooser/distrochooser", "master", 4),  # Python
    ("codidact/qpixel", "develop", 7),       # Ruby
    ("oSoWoSo/oco", "main", 15),             # bash
]

print("=" * 70)
print("PROBING TARGETS — issues with hacktoberfest OR good-first-issue label")
print("=" * 70)

candidates = []
for repo, branch, stars in TARGETS:
    print(f"\n=== {repo} ({stars}⭐) ===")
    # Get repo info first
    code, d = api(f"https://codeberg.org/api/v1/repos/{repo}", delay=2)
    if code != 200:
        print(f"  HTTP {code}")
        continue
    # Check if it's a fork/mirror
    if d.get("fork"):
        print(f"  SKIP: is a fork of {d.get('parent',{}).get('full_name','?')}")
        continue
    print(f"  ⭐{d.get('stars_count',0)} forks:{d.get('forks_count',0)} pushed:{d.get('updated_at','?')[:10]}")
    # Get issues
    code, d = api(f"https://codeberg.org/api/v1/repos/{repo}/issues?state=open&type=issues&limit=20", delay=2)
    if code != 200:
        continue
    items = d if isinstance(d, list) else d.get("data", [])
    print(f"  Open issues: {len(items)}")
    # Look for hacktoberfest / good first issue / help wanted
    for it in items[:15]:
        title = it.get("title", "")
        if any(kw in title.lower() for kw in ["update dependency", "chore(deps)", "bump ", "renovate"]):
            continue
        if it.get("comments", 0) != 0:
            continue
        if it.get("assignees"):
            continue
        labels = [l.get("name", "") for l in it.get("labels", [])][:5]
        if not any(kw in labels for kw in ["hacktoberfest", "good first issue", "help wanted", "good-first-issue"]):
            continue
        candidates.append({
            "repo": repo,
            "number": it.get("number"),
            "title": title[:90],
            "labels": labels,
            "created": (it.get("created_at") or "?")[:10],
            "url": it.get("html_url", ""),
        })
        print(f"  - #{it.get('number')} [{labels}]: {title[:70]}")

print("\n" + "=" * 70)
print(f"FINAL CANDIDATES: {len(candidates)}")
print("=" * 70)
for c in candidates:
    print(f"- {c['repo']}#{c['number']} ({c['created']}): {c['title']}")
    print(f"  labels: {c['labels']}")
