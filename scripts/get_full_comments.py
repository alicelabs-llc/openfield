import json, urllib.request, ssl

TOKEN = "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"
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/vnd.github+json",
}
CTX = ssl.create_default_context()

def api(method, url, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())

print("=== vajra #37 comments ===")
code, d = api("GET", "https://api.github.com/repos/Ergane-Foundation/vajra/issues/37/comments?per_page=30")
if code == 200:
    for c in d:
        print(f"--- {c.get('user',{}).get('login','?')} ({c.get('created_at','?')[:19]}) ---")
        print(c.get('body',''))
        print()

print("\n=== harbour #57 comments (issue-level) ===")
code, d = api("GET", "https://api.github.com/repos/Ishannaik/harbour/issues/57/comments?per_page=30")
if code == 200:
    for c in d:
        print(f"--- {c.get('user',{}).get('login','?')} ({c.get('created_at','?')[:19]}) ---")
        print(c.get('body',''))
        print()

print("\n=== harbour #57 review comments ===")
code, d = api("GET", "https://api.github.com/repos/Ishannaik/harbour/pulls/57/comments?per_page=30")
if code == 200:
    for c in d:
        print(f"--- {c.get('user',{}).get('login','?')} ({c.get('created_at','?')[:19]}) on {c.get('path','?')}:{c.get('line','?')} ---")
        print(c.get('body',''))
        print()

print("\n=== harbour #57 reviews ===")
code, d = api("GET", "https://api.github.com/repos/Ishannaik/harbour/pulls/57/reviews?per_page=30")
if code == 200:
    for r in d:
        print(f"--- {r.get('user',{}).get('login','?')} ({r.get('submitted_at','?')[:19]}) state={r.get('state','?')} ---")
        print(r.get('body',''))
        print()
