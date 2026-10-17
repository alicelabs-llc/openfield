import json, urllib.request, ssl, time

GH_TOKEN = "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"
CB_TOKEN = "86f56136e9bdbe4a6fe60d0b8f2e4c277f407590"
GH_HEADERS = {"Authorization": f"token {GH_TOKEN}", "User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github+json"}
CB_HEADERS = {"Authorization": f"token {CB_TOKEN}", "Content-Type": "application/json", "Accept": "application/json", "User-Agent": "Mozilla/5.0"}
CTX = ssl.create_default_context()

def gh(url, delay=1):
    time.sleep(delay)
    req = urllib.request.Request(url, headers=GH_HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=15) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:200]}

def cb(url, delay=2):
    time.sleep(delay)
    req = urllib.request.Request(url, headers=CB_HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:200]}

print("=== WHY was glical #9 closed? ===")
code, d = cb("https://codeberg.org/api/v1/repos/gvasquez/glical/pulls/9", delay=3)
if code == 200:
    print(f"  state: {d.get('state')}  merged: {bool(d.get('merged_at'))}")
    print(f"  title: {d.get('title','')[:80]}")
    print(f"  closed_at: {d.get('closed_at','?')[:19]}")
    print(f"  labels: {[l.get('name','') for l in d.get('labels',[])]}")
# Get the comments/notes
code, d = cb("https://codeberg.org/api/v1/repos/gvasquez/glical/issues/9/comments", delay=3)
if code == 200 and isinstance(d, list):
    print(f"  Comments ({len(d)}):")
    for c in d[-5:]:
        body = (c.get('body') or '').replace('\n',' ')[:300]
        print(f"    - {c.get('user',{}).get('login','?')}: {body}")

print("\n=== NexusCold #1 status (mine, still OPEN) ===")
code, d = gh("https://api.github.com/repos/alicelabs-llc/NexusCold/pulls/1")
if code == 200:
    print(f"  state: {d.get('state')}  merged: {bool(d.get('merged_at'))}")
    print(f"  mergeable_state: {d.get('mergeable_state','?')}")
    print(f"  updated: {d.get('updated_at','?')[:19]}")
    print(f"  comments: {d.get('comments',0)}  review_comments: {d.get('review_comments',0)}")

print("\n=== NexusCold #2 (the OTHER PR that got merged) ===")
code, d = gh("https://api.github.com/repos/alicelabs-llc/NexusCold/pulls/2")
if code == 200:
    print(f"  state: {d.get('state')}  merged: {bool(d.get('merged_at'))}")
    print(f"  title: {d.get('title','')[:80]}")
    print(f"  author: {d.get('user',{}).get('login','?')}")
    print(f"  merged_at: {d.get('merged_at','?')[:19]}")

print("\n=== vajra #37 status (still OPEN, my feedback was applied) ===")
code, d = gh("https://api.github.com/repos/Ergane-Foundation/vajra/pulls/37")
if code == 200:
    print(f"  state: {d.get('state')}  merged: {bool(d.get('merged_at'))}")
    print(f"  mergeable_state: {d.get('mergeable_state','?')}")
    print(f"  updated: {d.get('updated_at','?')[:19]}")

print("\n=== harbour #57 status ===")
code, d = gh("https://api.github.com/repos/Ishannaik/harbour/pulls/57")
if code == 200:
    print(f"  state: {d.get('state')}  merged: {bool(d.get('merged_at'))}")
    print(f"  mergeable_state: {d.get('mergeable_state','?')}")
    print(f"  updated: {d.get('updated_at','?')[:19]}")

print("\n=== PRs to awesome-lists (status check) ===")
awesome_prs = [
    ("aeoess/agent-governance-vocabulary", 203),
    ("punkpeye/awesome-remote-mcp-servers", 1928),
    ("sudeepb02/awesome-erc8004", 132),
    ("Chain-Love/chain-love", 4483),
    ("x402-foundation/x402", 3815),
    ("stacklok/toolhive-catalog", 1619),
    ("docker/mcp-registry", 5175),
    ("CodeSigils/awesome-agent-trust", 52),
    ("Merit-Systems/awesome-agentic-commerce", 796),
    ("xpaysh/awesome-x402", 1831),
    ("useagenthq/useagent", 84),
]
for repo, num in awesome_prs:
    code, d = gh(f"https://api.github.com/repos/{repo}/pulls/{num}")
    if code == 200:
        state = d.get('state', '?')
        merged = bool(d.get('merged_at'))
        marker = "✅MERGED" if merged else f"[{state.upper()}]"
        comments = d.get('comments', 0)
        print(f"  {marker:12} {repo}#{num} ({comments}c): {d.get('title','')[:60]}")
