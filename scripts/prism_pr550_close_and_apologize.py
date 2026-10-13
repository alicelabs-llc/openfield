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

# 1) Close PR #550 with an apology
print("=== Closing PR #550 with apology ===")
body = """My apologies — I had not seen #530 before opening this. Closing in favour of the original assignee who picked up #388 on 6 October.

Thanks for the heads-up about #446 (tests for scan result endpoints); I'll take a look at it and comment there if it's still up for grabs.

Sorry for the duplicate noise."""
payload = {"state": "closed", "body": body}
code, d = api("PATCH", "https://api.github.com/repos/NovaCode37/Prism-platform/pulls/550", payload)
print(f"  HTTP {code}: state={d.get('state')}  closed_at={d.get('closed_at')}")
print(f"  URL: {d.get('html_url')}")

# 2) Take a look at #446 to see if it's still available
print("\n=== Issue #446 status ===")
code, d = api("GET", "https://api.github.com/repos/NovaCode37/Prism-platform/issues/446")
if code == 200:
    print(f"  title: {d.get('title','')[:120]}")
    print(f"  state: {d.get('state')}  assignees: {[a.get('login','?') for a in d.get('assignees',[])]}")
    print(f"  labels: {[l.get('name','?') for l in d.get('labels',[])]}")
    print(f"  body preview: {(d.get('body','') or '')[:600]}")
else:
    print(f"  HTTP {code}: {d}")
