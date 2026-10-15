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

ISSUES = [
    ("spade-lang/spade", 185),
    ("GeopJr/Tuba", 1805),
    ("GeopJr/Tuba", 1802),
    ("mfussenegger/nvim-lint", 16),
    ("mfussenegger/nvim-lint", 17),
    ("mfussenegger/nvim-lint", 18),
]

for repo, num in ISSUES:
    print(f"\n{'='*70}")
    print(f"  {repo}#{num}")
    print(f"{'='*70}")
    code, d = api(f"https://codeberg.org/api/v1/repos/{repo}/issues/{num}", delay=3)
    if code != 200:
        print(f"  HTTP {code}: {str(d)[:200]}")
        continue
    print(f"  title: {d.get('title','')}")
    labels = [l.get('name','') for l in d.get('labels',[])]
    print(f"  state: {d.get('state')}  labels: {labels}  assignees: {d.get('assignees')}")
    print(f"  created: {d.get('created_at','?')[:10]}  updated: {d.get('updated_at','?')[:10]}")
    print(f"  comments: {d.get('comments',0)}")
    body = d.get('body','') or ''
    print(f"  body ({len(body)} chars):")
    print(body[:2000])
