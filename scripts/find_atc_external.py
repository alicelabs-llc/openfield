import json, urllib.request, ssl, time

GH_TOKEN = "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"
GH_HEADERS = {"Authorization": f"token {GH_TOKEN}", "User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github+json"}
CTX = ssl.create_default_context()

def fetch(url, delay=2):
    time.sleep(delay)
    req = urllib.request.Request(url, headers=GH_HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=15) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:200]}

# Search for repos related to ATC/UTA/trust verification that are NOT ours
OWNED_REPOS = {
    "alicelabs-llc/universal-trust-adapter",
    "eddyflores100-lang/marketnow",
    "eddyflores100-lang/alethech",
    "alicelabs-llc/NexusCold",
    "eddyflores100-lang/alethech-agent-vault",
}

# Search for issues related to trust/ATC/UTA in external repos
queries = [
    # Direct ATC/UTA searches
    '"agent trust" "good first issue" state:open type:issue -user:eddyflores100-lang',
    '"trust verification" "good first issue" state:open type:issue -user:eddyflores100-lang',
    '"UTA" trust adapter state:open type:issue -user:eddyflores100-lang',
    '"ATC" trust credential state:open type:issue -user:eddyflores100-lang',
    '"x402" "good first issue" state:open type:issue -user:eddyflores100-lang',
    '"verifiable" "agent" "good first issue" state:open type:issue -user:eddyflores100-lang',
    '"trust layer" "good first issue" state:open type:issue -user:eddyflores100-lang',
    '"MCP" "trust" "good first issue" state:open type:issue -user:eddyflores100-lang',
    '"Ed25519" "good first issue" state:open type:issue -user:eddyflores100-lang',
    '"cryptographic" "trust" state:open type:issue -user:eddyflores100-lang',
    '"agent identity" state:open type:issue -user:eddyflores100-lang',
    '"verifiable credentials" state:open type:issue -user:eddyflores100-lang',
    '"signed" "trust" state:open type:issue -user:eddyflores100-lang',
]

all_candidates = []
seen = set()

for q in queries:
    import urllib.parse
    encoded = urllib.parse.quote(q)
    code, d = fetch(f"https://api.github.com/search/issues?q={encoded}&per_page=15&sort=created&order=desc")
    if code != 200:
        continue
    for it in d.get("items", []):
        repo_url = it.get("repository_url", "")
        repo = repo_url.replace("https://api.github.com/repos/", "")
        if repo in OWNED_REPOS or repo in seen:
            continue
        if it.get("assignee"):
            continue
        if it.get("comments", 0) > 3:
            continue
        title = it.get("title", "")
        if any(kw in title.lower() for kw in ["update dependency", "chore(deps)", "bump "]):
            continue
        seen.add(repo)
        labels = [l.get("name","") for l in it.get("labels",[])][:5]
        all_candidates.append({
            "repo": repo,
            "number": it.get("number"),
            "title": title[:80],
            "labels": labels,
            "comments": it.get("comments",0),
            "created": (it.get("created_at") or "?")[:10],
            "url": it.get("html_url",""),
        })

# Show results
print(f"Found {len(all_candidates)} candidates across {len(seen)} repos\n")
for i, c in enumerate(all_candidates[:20], 1):
    print(f"{i}. {c['repo']}#{c['number']} ({c['comments']}c, {c['created']})")
    print(f"   title: {c['title']}")
    print(f"   labels: {c['labels']}")
    print(f"   url: {c['url']}")
    print()

# For top 5, get issue body
print("\n" + "="*60)
print("TOP 5 — Full details")
print("="*60)
for c in all_candidates[:5]:
    print(f"\n{'='*50}")
    print(f"  {c['repo']}#{c['number']}")
    print(f"{'='*50}")
    code, d = fetch(f"https://api.github.com/repos/{c['repo']}/issues/{c['number']}")
    if code == 200:
        print(f"  title: {d.get('title','')}")
        body = (d.get('body') or '')[:800]
        print(f"  body: {body}")
