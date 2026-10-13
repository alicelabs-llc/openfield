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

# Get full PR #530 details (closed one) — issue events
print("=== Prism #530 (closed) — issue events ===")
code, d = api("GET", "https://api.github.com/repos/NovaCode37/Prism-platform/issues/530/events?per_page=50")
if code == 200:
    for ev in d:
        if ev.get('event') in ('closed', 'reopened', 'referenced', 'cross-referenced'):
            actor = ev.get('actor',{}).get('login','?')
            created = ev.get('created_at','?')[:19]
            commit_id = ev.get('commit_id','')
            print(f"  {ev.get('event')} by {actor} at {created}" + (f" (commit {commit_id[:8]})" if commit_id else ""))
            if ev.get('commit_id'):
                # show what commit was referenced
                pass

print("\n=== Prism #530 — issue comments ===")
code, d = api("GET", "https://api.github.com/repos/NovaCode37/Prism-platform/issues/530/comments?per_page=50")
if code == 200:
    for c in d:
        print(f"  {c.get('user',{}).get('login','?')} ({c.get('created_at','?')[:19]}):")
        print(f"    {(c.get('body','') or '')[:400]}")
        print()

print("\n=== Prism #550 (open) — checks ===")
code, d = api("GET", "https://api.github.com/repos/NovaCode37/Prism-platform/pulls/550")
if code == 200:
    print(f"  title: {d.get('title','')[:100]}")
    print(f"  state: {d.get('state')}  draft: {d.get('draft',False)}  merged: {d.get('merged',False)}")
    print(f"  mergeable: {d.get('mergeable','?')}  mergeable_state: {d.get('mergeable_state','?')}")
    print(f"  head sha: {d.get('head',{}).get('sha','?')[:8]}")
    print(f"  base sha: {d.get('base',{}).get('sha','?')[:8]}")
    print(f"  changed_files: {d.get('changed_files')}  +{d.get('additions',0)}/-{d.get('deletions',0)}")
    print(f"  commits: {d.get('commits',0)}")

print("\n=== Prism #550 — review status ===")
code, d = api("GET", "https://api.github.com/repos/NovaCode37/Prism-platform/pulls/550/reviews")
if code == 200:
    print(f"  {len(d)} reviews")
    for r in d:
        print(f"  - {r.get('user',{}).get('login','?')} ({r.get('submitted_at','?')[:19]}): {r.get('state')} — {(r.get('body','') or '')[:100]}")

print("\n=== Prism #550 — status checks (CI) ===")
code, d = api("GET", "https://api.github.com/repos/NovaCode37/Prism-platform/commits/33f968ef/check-runs?per_page=20")
if code == 200:
    runs = d.get('check_runs', [])
    print(f"  {len(runs)} check runs")
    for r in runs:
        print(f"  - {r.get('name','?')}: status={r.get('status','?')} conclusion={r.get('conclusion','?')}")
else:
    print(f"  HTTP {code}: {d.get('message','')[:200]}")
