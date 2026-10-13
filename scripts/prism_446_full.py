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

print("=== Issue #446 FULL body ===")
code, d = api("GET", "https://api.github.com/repos/NovaCode37/Prism-platform/issues/446")
print(d.get('body',''))
print()
print("=== Comments ===")
code, d = api("GET", "https://api.github.com/repos/NovaCode37/Prism-platform/issues/446/comments?per_page=20")
if code == 200:
    print(f"  {len(d)} comments")
    for c in d:
        print(f"  - {c.get('user',{}).get('login','?')} ({c.get('created_at','?')[:19]}): {(c.get('body','') or '')[:300]}")
