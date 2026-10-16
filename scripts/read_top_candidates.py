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

# Anti-ban criteria for selection:
# 1. Issue created in last 14 days (not stale)
# 2. Maintainer active recently (commit in last 7 days)
# 3. Clear scope (not a huge refactor)
# 4. Low technical complexity (TypeScript/Python/bash preferred)
# 5. Repo not a mirror of GitHub (avoids duplicate)

ISSUES = [
    ("wafrn/wafrn", 848),      # 173⭐ TS, recent
    ("gvasquez/glical", 8),    # 1⭐ Gleam, recent
    ("gvasquez/glical", 6),    # 1⭐ Gleam, recent
    ("gvasquez/glical", 5),    # 1⭐ Gleam, recent
    ("gvasquez/glical", 4),    # 1⭐ Gleam, recent
    ("gvasquez/glical", 3),    # 1⭐ Gleam, recent
    ("Astrea/RealmsPlayerlistBot", None),  # 1⭐ Python — list its issues
    ("Astrea/PYTHIA", None),   # 1⭐ Python — list its issues
    ("Stellarium-Labs/elytra-ms", None),  # 1⭐ Python
    ("margau/pkg-exporter", None),         # 2⭐ Python
    ("montepy-dev/MontePy", None),         # 1⭐ Python
    ("sp1thas/scrapy-folder-tree", None),  # 0⭐ Python
]

for repo_spec in ISSUES:
    repo, num = repo_spec
    print(f"\n{'='*70}")
    print(f"  {repo}")
    print(f"{'='*70}")
    if num is None:
        # List all open issues
        code, d = api(f"https://codeberg.org/api/v1/repos/{repo}/issues?state=open&type=issues&limit=10", delay=2)
        if code != 200:
            print(f"  HTTP {code}")
            continue
        items = d if isinstance(d, list) else d.get("data", [])
        for it in items[:8]:
            print(f"  - #{it.get('number')} [{[l.get('name','') for l in it.get('labels',[])][:3]}] ({it.get('comments',0)}c): {it.get('title','')[:70]}")
        continue
    code, d = api(f"https://codeberg.org/api/v1/repos/{repo}/issues/{num}", delay=2)
    if code != 200:
        print(f"  HTTP {code}")
        continue
    print(f"  title: {d.get('title','')}")
    print(f"  state: {d.get('state')}  comments: {d.get('comments',0)}")
    print(f"  created: {d.get('created_at','?')[:10]}  updated: {d.get('updated_at','?')[:10]}")
    body = (d.get('body') or '')[:1500]
    print(f"  body ({len(body)} chars):")
    print(body)
