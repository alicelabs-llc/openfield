import json, urllib.request, ssl, time

# GraphQL allows more efficient queries even unauthenticated (still rate-limited but more headroom per call)
# Actually GitHub GraphQL requires auth. Let me try REST with longer delays instead.
HEADERS = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
CTX = ssl.create_default_context()

REPOS = [
    ("Ergane-Foundation/vajra", 29),
    ("Ishannaik/harbour", 41),
    ("NovaCode37/Prism-platform", 388),
]

for repo, num in REPOS:
    print(f"\n=== {repo} #{num} ===")
    time.sleep(20)
    url = f"https://api.github.com/repos/{repo}/issues/{num}"
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=15) as resp:
            d = json.loads(resp.read().decode())
        print(f"  state: {d.get('state')}  title: {(d.get('title') or '')[:100]}")
        print(f"  comments: {d.get('comments',0)}  created: {(d.get('created_at') or '?')[:10]}")
        labels = [l.get('name','?') for l in d.get('labels',[])]
        print(f"  labels: {labels}")
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code}: {e.read().decode()[:200]}")
    except Exception as e:
        print(f"  ERR: {e}")
