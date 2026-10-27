import json, urllib.request, ssl, time

GH_TOKEN = "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"
GL_TOKEN = "glpat-VTdIPfmOYCLcAQHp0IdlyWM6MQpvOjEKdTpranZqbQ8.01.17073yv2r"
CB_TOKEN = "86f56136e9bdbe4a6fe60d0b8f2e4c277f407590"

GH_HEADERS = {"Authorization": f"token {GH_TOKEN}", "User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github+json"}
GL_HEADERS = {"PRIVATE-TOKEN": GL_TOKEN, "User-Agent": "Mozilla/5.0", "Accept": "application/json"}
CB_HEADERS = {"Authorization": f"token {CB_TOKEN}", "Content-Type": "application/json", "Accept": "application/json", "User-Agent": "Mozilla/5.0"}
CTX = ssl.create_default_context()

def fetch(url, headers, delay=2):
    time.sleep(delay)
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=15) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:200]}
    except Exception as e:
        return -1, {"error": str(e)[:200]}

OWNED = {
    "alicelabs-llc/universal-trust-adapter", "eddyflores100-lang/marketnow",
    "eddyflores100-lang/alethech", "alicelabs-llc/NexusCold",
    "eddyflores100-lang/alethech-agent-vault", "eddyflores100-lang/ENTITY",
    "eddyflores100-lang/open-source-radar", "eddyflores100-lang/sloptotal",
    "eddyflores100-lang/NexusCold-1",
}

# ============================================================
# GITHUB — Search for trust/ATC/UTA/Ed25519/verifiable/agent identity
# ============================================================
print("=" * 70)
print("GITHUB — Trust/ATC/UTA/Verifiable issues (external repos)")
print("=" * 70)

queries = [
    '"trust verification" state:open type:issue label:"good first issue" -user:eddyflores100-lang',
    '"Ed25519" state:open type:issue label:"good first issue" -user:eddyflores100-lang',
    '"verifiable credentials" state:open type:issue label:"good first issue" -user:eddyflores100-lang',
    '"agent identity" state:open type:issue label:"good first issue" -user:eddyflores100-lang',
    '"cryptographic verification" state:open type:issue label:"good first issue" -user:eddyflores100-lang',
    '"signed" "verify" state:open type:issue label:"help wanted" -user:eddyflores100-lang language:Python',
    '"signature" "verification" state:open type:issue label:"help wanted" -user:eddyflores100-lang language:TypeScript',
    '"zero trust" state:open type:issue label:"good first issue" -user:eddyflores100-lang',
    '"MCP server" "trust" state:open type:issue -user:eddyflores100-lang',
    '"x402" "trust" state:open type:issue -user:eddyflores100-lang',
    '"proof" "signature" state:open type:issue label:"help wanted" -user:eddyflores100-lang language:Rust',
    '"receipt" "verify" "sha256" state:open type:issue label:"good first issue" -user:eddyflores100-lang',
    '"provenance" state:open type:issue label:"good first issue" -user:eddyflores100-lang',
    '"attestation" state:open type:issue label:"good first issue" -user:eddyflores100-lang',
]

all_candidates = []
seen = set()
for q in queries:
    import urllib.parse
    encoded = urllib.parse.quote(q)
    code, d = fetch(f"https://api.github.com/search/issues?q={encoded}&per_page=10&sort=created&order=desc", GH_HEADERS, delay=2)
    if code != 200:
        continue
    for it in d.get("items", []):
        repo_url = it.get("repository_url", "")
        repo = repo_url.replace("https://api.github.com/repos/", "")
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

# Show top 15
print(f"\nFound {len(all_candidates)} candidates\n")
for i, c in enumerate(all_candidates[:15], 1):
    print(f"{i}. {c['repo']}#{c['number']} ({c['comments']}c, {c['created']})")
    print(f"   title: {c['title']}")
    print(f"   labels: {c['labels']}")
    print(f"   url: {c['url']}")
    print()

# For top 3, get body
print("\n" + "="*60)
for c in all_candidates[:3]:
    print(f"\n{'='*50}")
    print(f"  {c['repo']}#{c['number']}")
    print(f"{'='*50}")
    code, d = fetch(f"https://api.github.com/repos/{c['repo']}/issues/{c['number']}", GH_HEADERS, delay=2)
    if code == 200:
        body = (d.get('body') or '')[:800]
        print(f"  body: {body}")

# ============================================================
# CODEBERG — Search for trust/crypto/verify repos
# ============================================================
print("\n\n" + "=" * 70)
print("CODEBERG — Trust/crypto/verification repos")
print("=" * 70)

for q in ["trust", "crypto", "verify", "signature", "provenance"]:
    code, d = fetch(f"https://codeberg.org/api/v1/repos/search?q={q}&limit=5&sort=stars&order=desc", CB_HEADERS, delay=3)
    if code != 200:
        continue
    items = d if isinstance(d, list) else d.get("data", [])
    for r in items[:2]:
        name = r.get("full_name","?")
        stars = r.get("stars_count",0)
        desc = r.get("description","")[:60]
        if stars < 3:
            continue
        if name in OWNED:
            continue
        print(f"  {name} ⭐{stars}: {desc}")

# ============================================================
# GITLAB — Search via API for trust/crypto issues
# ============================================================
print("\n\n" + "=" * 70)
print("GITLAB — Trust/crypto issues")
print("=" * 70)

# Try cross-project search
code, d = fetch("https://gitlab.com/api/v4/issues?search=trust+verification&state=opened&per_page=10", GL_HEADERS, delay=15)
if code == 200 and isinstance(d, list):
    print(f"Found {len(d)} issues mentioning 'trust verification'")
    for it in d[:5]:
        proj = it.get("project_id")
        title = it.get("title","")[:60]
        iid = it.get("iid")
        url = it.get("web_url","")
        print(f"  !{iid}: {title}")
        print(f"    url: {url}")
else:
    print(f"  HTTP {code}: {str(d)[:200]}")

# Also try: search for "Ed25519" in GitLab
time.sleep(10)
code, d = fetch("https://gitlab.com/api/v4/issues?search=Ed25519&state=opened&per_page=10", GL_HEADERS, delay=15)
if code == 200 and isinstance(d, list):
    print(f"\nFound {len(d)} issues mentioning 'Ed25519'")
    for it in d[:3]:
        title = it.get("title","")[:60]
        iid = it.get("iid")
        url = it.get("web_url","")
        print(f"  !{iid}: {title}")
        print(f"    url: {url}")

