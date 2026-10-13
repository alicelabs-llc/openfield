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

CHECKS = [
    ("Ergane-Foundation/vajra", 37),
    ("Ishannaik/harbour", 57),
    ("NovaCode37/Prism-platform", 446),  # the issue we just claimed
]

for repo, num in CHECKS:
    print(f"\n=== {repo} #{num} ===")
    # PR details
    is_pr = repo != "NovaCode37/Prism-platform" or num != 446
    if is_pr:
        code, d = api("GET", f"https://api.github.com/repos/{repo}/pulls/{num}")
    else:
        code, d = api("GET", f"https://api.github.com/repos/{repo}/issues/{num}")
    if code != 200:
        print(f"  HTTP {code}: {d.get('message','')[:200]}")
        continue
    if is_pr:
        print(f"  title: {(d.get('title') or '')[:100]}")
        print(f"  state: {d.get('state')}  draft: {d.get('draft',False)}  merged: {bool(d.get('merged_at'))}")
        print(f"  mergeable: {d.get('mergeable','?')}  mergeable_state: {d.get('mergeable_state','?')}")
        print(f"  created: {(d.get('created_at') or '?')[:19]}  updated: {(d.get('updated_at') or '?')[:19]}")
        print(f"  comments: {d.get('comments',0)}  review_comments: {d.get('review_comments',0)}")
        # CI checks
        sha = d.get('head',{}).get('sha','')
        if sha:
            code2, d2 = api("GET", f"https://api.github.com/repos/{repo}/commits/{sha}/check-runs?per_page=20")
            if code2 == 200:
                runs = d2.get('check_runs',[])
                print(f"  CI checks ({len(runs)}):")
                for r in runs:
                    print(f"    - {r.get('name','?')[:50]}: {r.get('status','?')}/{r.get('conclusion','?')}")
    # Comments on the PR/issue
    kind = "pulls" if is_pr else "issues"
    code, d = api("GET", f"https://api.github.com/repos/{repo}/{kind}/{num}/comments?per_page=30")
    if code == 200:
        if d:
            print(f"  Comments:")
            for c in d:
                print(f"    - {c.get('user',{}).get('login','?')} ({(c.get('created_at') or '?')[:19]}): {(c.get('body','') or '')[:240].replace(chr(10),' ')}")
