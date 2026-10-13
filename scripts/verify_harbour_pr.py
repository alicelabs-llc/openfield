import json, urllib.request, ssl, time

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

print("=== PR #57 status ===")
code, d = api("GET", "https://api.github.com/repos/Ishannaik/harbour/pulls/57")
print(f"  state: {d.get('state')}  merged: {bool(d.get('merged_at'))}  draft: {d.get('draft',False)}")
print(f"  mergeable: {d.get('mergeable','?')}  mergeable_state: {d.get('mergeable_state','?')}")
print(f"  head sha: {d.get('head',{}).get('sha','?')[:8]}")
print(f"  updated_at: {d.get('updated_at','?')[:19]}")

# Check CI on the new sha
sha = d.get('head',{}).get('sha','')
if sha:
    time.sleep(3)
    print("\n=== CI checks on head sha ===")
    code, d2 = api("GET", f"https://api.github.com/repos/Ishannaik/harbour/commits/{sha}/check-runs?per_page=20")
    if code == 200:
        for r in d2.get('check_runs',[]):
            print(f"  - {r.get('name','?')[:50]}: {r.get('status','?')}/{r.get('conclusion','?')}")

# Post a comment summarising the fix
print("\n=== Posting reply on PR #57 ===")
body = """Quick update: CodeRabbit's point on tab handling was correct (issue #41 explicitly wants tabs replaced with spaces, not preserved). The branch now does:

```rust
let sanitized: String = query
    .chars()
    .map(|c| if matches!(c, '\\r' | '\\n' | '\\t') { ' ' } else { c })
    .filter(|c| !c.is_control())
    .collect();
let query = sanitized.trim();
```

So `"dune\\npart two"` becomes `"dune part two"` (not `"dunepart two"`), and `"foundation\\tseason"` becomes `"foundation season"`. The regression test was updated to cover the newline-between-words case explicitly, and to assert the space-replacement behaviour for tabs.

Force-pushed as `8605d4c`."""
code, d = api("POST", "https://api.github.com/repos/Ishannaik/harbour/issues/57/comments", {"body": body})
print(f"  HTTP {code}: {d.get('html_url','?') if code==201 else d}")
