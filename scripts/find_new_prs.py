import json, urllib.request, ssl, time, urllib.parse

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

OWNED = {
    "alicelabs-llc/universal-trust-adapter", "eddyflores100-lang/marketnow",
    "eddyflores100-lang/alethech", "alicelabs-llc/NexusCold",
    "eddyflores100-lang/alethech-agent-vault", "eddyflores100-lang/ENTITY",
    "eddyflores100-lang/open-source-radar", "eddyflores100-lang/sloptotal",
    "eddyflores100-lang/NexusCold-1", "eddyflores100-lang/govp",
    "eddyflores100-lang/Sorobill-Backend",
    "TanbirRamim/open-source-radar", "pablocaeg/sloptotal",
    "blackmore-technology-group/ENTITY", "govp-protocol/govp",
    "Sorobill/Sorobill-Backend", "meetdino/dino",
    "Ergane-Foundation/vajra", "Ishannaik/harbour",
    "pacocartones/market-data-sanity-checker", "wafrn/wafrn",
    "mfussenegger/nvim-lint", "gvasquez/glical",
    "OpenMW/openmw", "fdroid/fdroidclient", "inkscape/extensions",
    "inkscape/inkscape", "yunaremaia/mcp-guard",
    "useagenthq/useagent", "floatpane/matcha",
    "flisk-sh/flisk", "run-llama/llama_index",
}

# Search for issues related to trust/crypto/signature/verification
queries = [
    '"Ed25519" "help wanted" state:open type:issue -user:eddyflores100-lang created:>2026-10-01',
    '"signature verification" "good first issue" state:open type:issue -user:eddyflores100-lang created:>2026-09-15',
    '"HMAC" "good first issue" state:open type:issue -user:eddyflores100-lang created:>2026-09-15',
    '"trust anchor" state:open type:issue -user:eddyflores100-lang created:>2026-09-15',
    '"key rotation" "good first issue" state:open type:issue -user:eddyflores100-lang created:>2026-09-15',
    '"provenance" "good first issue" state:open type:issue -user:eddyflores100-lang created:>2026-09-15',
    '"MCP" "security" "good first issue" state:open type:issue -user:eddyflores100-lang created:>2026-09-15',
    '"zero trust" "good first issue" state:open type:issue -user:eddyflores100-lang created:>2026-09-15',
    '"cryptographic" "help wanted" state:open type:issue -user:eddyflores100-lang language:Python created:>2026-09-15',
    '"verify" "signature" "help wanted" state:open type:issue -user:eddyflores100-lang language:TypeScript created:>2026-09-15',
]

all_candidates = []
seen = set()
for q in queries:
    encoded = urllib.parse.quote(q)
    code, d = fetch(f"https://api.github.com/search/issues?q={encoded}&per_page=10&sort=created&order=desc")
    if code != 200:
        continue
    for it in d.get("items", []):
        repo = it.get("repository_url","").replace("https://api.github.com/repos/","")
        if repo in OWNED or repo in seen:
            continue
        if it.get("assignee"):
            continue
        if it.get("comments", 0) > 3:
            continue
        title = it.get("title", "")
        seen.add(f"{repo}#{it.get('number')}")
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

# Show top 10
print(f"Found {len(all_candidates)} candidates\n")
for i, c in enumerate(all_candidates[:10], 1):
    print(f"{i}. {c['repo']}#{c['number']} ({c['comments']}c, {c['created']})")
    print(f"   title: {c['title']}")
    print(f"   labels: {c['labels']}")
    print(f"   url: {c['url']}")
    print()

# Get body for top 3
for c in all_candidates[:3]:
    print(f"\n{'='*50}")
    print(f"  {c['repo']}#{c['number']}")
    print(f"{'='*50}")
    code, d = fetch(f"https://api.github.com/repos/{c['repo']}/issues/{c['number']}")
    if code == 200:
        body = (d.get('body') or '')[:600]
        print(f"  body: {body}")
