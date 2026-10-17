import json, urllib.request, ssl, time

GH_TOKEN = "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"
HEADERS = {"Authorization": f"token {GH_TOKEN}", "User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github+json"}
CTX = ssl.create_default_context()

# Check comments on the awesome-list PRs that have comments
PRS_WITH_COMMENTS = [
    ("punkpeye/awesome-remote-mcp-servers", 1928, 1),
    ("x402-foundation/x402", 3815, 3),
    ("stacklok/toolhive-catalog", 1619, 5),
    ("docker/mcp-registry", 5175, 3),
    ("CodeSigils/awesome-agent-trust", 52, 3),
    ("useagenthq/useagent", 84, 2),
]
for repo, num, _ in PRS_WITH_COMMENTS:
    print(f"\n=== {repo}#{num} comments ===")
    time.sleep(2)
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/issues/{num}/comments?per_page=10",
        headers=HEADERS, method="GET",
    )
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=15) as resp:
            arr = json.loads(resp.read().decode())
        for c in arr[-5:]:
            body = (c.get('body') or '').replace('\n',' ')[:280]
            print(f"  - {c.get('user',{}).get('login','?')}: {body}")
    except Exception as e:
        print(f"  ERR: {e}")
