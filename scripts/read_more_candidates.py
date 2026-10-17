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

# Look at glical's parent issue #1 (describes the spec) + look at wafrn-style repos
ISSUES = [
    ("gvasquez/glical", 1),       # parent issue spec
    ("gvasquez/glical", 2),        # Improve Testing Coverage
    ("wafrn/wafrn", 773),          # Fediverse attachments
    ("wafrn/wafrn", 769),          # schedule post dialog dates
    ("wafrn/wafrn", 766),          # nick for users
]

for repo, num in ISSUES:
    print(f"\n{'='*70}")
    print(f"  {repo}#{num}")
    print(f"{'='*70}")
    code, d = api(f"https://codeberg.org/api/v1/repos/{repo}/issues/{num}", delay=3)
    if code != 200:
        print(f"  HTTP {code}")
        continue
    print(f"  title: {d.get('title','')}")
    print(f"  state: {d.get('state')}  comments: {d.get('comments',0)}")
    print(f"  created: {d.get('created_at','?')[:10]}")
    body = d.get('body','') or ''
    print(f"  body ({len(body)} chars):")
    print(body[:2500])
