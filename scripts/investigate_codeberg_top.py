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
        return e.code, {"error": e.read().decode()[:300]}
    except Exception as e:
        return -1, {"error": str(e)[:200]}

TOP_REPOS = [
    "wafrn/wafrn",       # 173 stars TS, pushed today
    "GeopJr/Tuba",       # 88 stars Vala
    "Calamares/calamares", # 63 stars C++
    "mfussenegger/nvim-lint", # 39 stars Lua
    "spade-lang/spade",   # 30 stars Rust
    "castle-engine/castle-engine",  # 12 stars Pascal
    "codidact/qpixel",   # 7 stars Ruby
    "RIOT/RIOT",         # 22 stars C
]

for repo in TOP_REPOS:
    print(f"\n{'='*60}")
    print(f"  {repo}")
    print(f"{'='*60}")
    code, d = api(f"https://codeberg.org/api/v1/repos/{repo}", delay=3)
    if code != 200:
        print(f"  HTTP {code}")
        continue
    print(f"  ⭐ {d.get('stars_count',0)}  forks: {d.get('forks_count',0)}  lang: {d.get('language','?')}")
    print(f"  default: {d.get('default_branch','?')}  archived: {d.get('archived',False)}")
    print(f"  pushed: {d.get('updated_at','?')[:19]}")
    print(f"  description: {(d.get('description') or '')[:120]}")
    # Check open issues
    open_issues = d.get('open_issues_count', 0)
    print(f"  open_issues: {open_issues}")
    
    # Look at open issues with hacktoberfest label
    code2, d2 = api(f"https://codeberg.org/api/v1/repos/{repo}/issues?labels=hacktoberfest&state=open&type=issues&limit=10", delay=2)
    if code2 == 200:
        items = d2 if isinstance(d2, list) else d2.get("data", [])
        if items:
            print(f"  Issues with 'hacktoberfest' label ({len(items)}):")
            for it in items[:5]:
                num = it.get('number')
                title = it.get('title','')[:80]
                labels = [l.get('name','') for l in it.get('labels',[])][:5]
                assignee = it.get('assignee')
                assignee_login = assignee.get('login','?') if isinstance(assignee, dict) else None
                if assignee_login:
                    continue  # skip assigned
                print(f"    - #{num} [{labels}]: {title}")
        else:
            # Try good first issue
            code3, d3 = api(f"https://codeberg.org/api/v1/repos/{repo}/issues?labels=good%20first%20issue&state=open&type=issues&limit=10", delay=2)
            if code3 == 200:
                items3 = d3 if isinstance(d3, list) else d3.get("data", [])
                if items3:
                    print(f"  Issues with 'good first issue' label ({len(items3)}):")
                    for it in items3[:5]:
                        num = it.get('number')
                        title = it.get('title','')[:80]
                        labels = [l.get('name','') for l in it.get('labels',[])][:5]
                        print(f"    - #{num} [{labels}]: {title}")
