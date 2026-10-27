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
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:200]}
    except Exception as e:
        return -1, {"error": str(e)[:200]}

# Repos we already touched (anti-ban: don't repeat)
REPOS_TO_AVOID = {
    "meetdino/dino", "Ergane-Foundation/vajra", "Ishannaik/harbour",
    "NovaCode37/Prism-platform", "pacocartones/market-data-sanity-checker",
    "alicelabs-llc/NexusCold", "mfussenegger/nvim-lint", "gvasquez/glical",
    "OpenMW/openmw", "fdroid/fdroidclient", "inkscape/extensions",
    "inkscape/inkscape",
}

# ============================================================
# GITHUB — 2 candidates
# ============================================================
print("=" * 70)
print("GITHUB — Searching for 2 good-first-issues")
print("=" * 70)

# Search for hacktoberfest-tagged repos with good first issues, created recently
queries = [
    'label:"good first issue" label:hacktoberfest state:open no:assignee created:>2026-10-10 language:Python',
    'label:"good first issue" label:hacktoberfest state:open no:assignee created:>2026-10-10 language:TypeScript',
    'label:"good first issue" label:hacktoberfest state:open no:assignee created:>2026-10-10 language:Rust',
    'label:"good first issue" label:hacktoberfest state:open no:assignee created:>2026-10-10 language:JavaScript',
    'label:"good first issue" label:hacktoberfest state:open no:assignee created:>2026-10-10 language:Go',
    'label:"help wanted" label:hacktoberfest state:open no:assignee created:>2026-10-12 language:Python',
]

gh_candidates = []
seen_repos = set()
for q in queries:
    import urllib.parse
    encoded = urllib.parse.quote(q)
    code, d = fetch(f"https://api.github.com/search/issues?q={encoded}&sort=created&order=desc&per_page=15", GH_HEADERS, delay=2)
    if code != 200:
        continue
    for it in d.get("items", []):
        repo_url = it.get("repository_url", "")
        repo = repo_url.replace("https://api.github.com/repos/", "")
        if repo in REPOS_TO_AVOID or repo in seen_repos:
            continue
        if it.get("comments", 0) > 2:
            continue
        if it.get("assignees"):
            continue
        title = it.get("title", "")
        if any(kw in title.lower() for kw in ["update dependency", "chore(deps)", "bump ", "renovate"]):
            continue
        seen_repos.add(repo)
        labels = [l.get("name","") for l in it.get("labels",[])][:5]
        gh_candidates.append({
            "repo": repo,
            "number": it.get("number"),
            "title": title[:80],
            "labels": labels,
            "comments": it.get("comments",0),
            "created": (it.get("created_at") or "?")[:10],
            "url": it.get("html_url",""),
        })
        if len(gh_candidates) >= 20:
            break
    if len(gh_candidates) >= 20:
        break

# Show top 10
print(f"\nFound {len(gh_candidates)} candidates. Top 10:")
for i, c in enumerate(gh_candidates[:10], 1):
    print(f"\n  {i}. {c['repo']}#{c['number']} ({c['comments']}c, {c['created']})")
    print(f"     title: {c['title']}")
    print(f"     labels: {c['labels']}")
    print(f"     url: {c['url']}")

# For top 2, get the issue body
print("\n" + "=" * 70)
print("TOP 2 GITHUB CANDIDATES — Full details")
print("=" * 70)
for c in gh_candidates[:2]:
    print(f"\n{'='*60}")
    print(f"  {c['repo']}#{c['number']}")
    print(f"{'='*60}")
    code, d = fetch(f"https://api.github.com/repos/{c['repo']}/issues/{c['number']}", GH_HEADERS, delay=2)
    if code == 200:
        print(f"  title: {d.get('title','')}")
        print(f"  state: {d.get('state')}  comments: {d.get('comments',0)}")
        body = (d.get('body') or '')[:1000]
        print(f"  body: {body}")

# ============================================================
# GITLAB — 2 candidates
# ============================================================
print("\n\n" + "=" * 70)
print("GITLAB — Searching for 2 issues")
print("=" * 70)

# Search GitLab for issues with hacktoberfest label
# GitLab doesn't have a global issue search like GitHub, so we search by project
# Use the /issues endpoint with search
gl_candidates = []
# Try searching across projects
code, d = fetch("https://gitlab.com/api/v4/issues?search=hacktoberfest&state=opened&per_page=20&sort=desc&order_by=created_at", GL_HEADERS, delay=5)
if code == 200 and isinstance(d, list):
    for it in d:
        proj = it.get("project_id")
        if not proj:
            continue
        # Get project info
        time.sleep(2)
        _, proj_data = fetch(f"https://gitlab.com/api/v4/projects/{proj}", GL_HEADERS, delay=2)
        if not isinstance(proj_data, dict):
            continue
        repo = proj_data.get("path_with_namespace", "?")
        if repo in REPOS_TO_AVOID:
            continue
        labels = it.get("labels", [])
        if "hacktoberfest" not in labels and "good first issue" not in labels:
            continue
        if it.get("assignees"):
            continue
        gl_candidates.append({
            "repo": repo,
            "iid": it.get("iid"),
            "title": it.get("title","")[:80],
            "labels": labels[:5],
            "comments": 0,  # GitLab doesn't return comment count in list
            "created": (it.get("created_at") or "?")[:10],
            "url": it.get("web_url",""),
        })
        if len(gl_candidates) >= 10:
            break

print(f"\nFound {len(gl_candidates)} candidates:")
for i, c in enumerate(gl_candidates[:5], 1):
    print(f"\n  {i}. {c['repo']}#{c['iid']} ({c['created']})")
    print(f"     title: {c['title']}")
    print(f"     labels: {c['labels']}")
    print(f"     url: {c['url']}")

# ============================================================
# CODEBERG — 2 candidates
# ============================================================
print("\n\n" + "=" * 70)
print("CODEBERG — Searching for 2 issues")
print("=" * 70)

# Search Codeberg for issues with hacktoberfest label
cb_candidates = []
for page in range(1, 4):
    code, d = fetch(f"https://codeberg.org/api/v1/repos/issues/search?labels=hacktoberfest&state=open&type=issues&limit=50&page={page}", CB_HEADERS, delay=3)
    if code != 200:
        break
    items = d if isinstance(d, list) else d.get("data", [])
    if not items:
        break
    for it in items:
        repo_data = it.get("repository", {}) or {}
        repo = repo_data.get("full_name", "")
        if not repo or repo in REPOS_TO_AVOID:
            continue
        if it.get("assignees"):
            continue
        title = it.get("title", "")
        if any(kw in title.lower() for kw in ["update dependency", "chore(deps)", "bump "]):
            continue
        labels = [l.get("name","") for l in it.get("labels",[])][:5]
        if "hacktoberfest" not in labels:
            continue
        cb_candidates.append({
            "repo": repo,
            "number": it.get("number"),
            "title": title[:80],
            "labels": labels,
            "comments": it.get("comments", 0),
            "created": (it.get("created_at") or "?")[:10],
            "url": it.get("html_url",""),
        })
        if len(cb_candidates) >= 15:
            break
    if len(cb_candidates) >= 15:
        break

# Filter: 0 comments preferred
cb_zero_comments = [c for c in cb_candidates if c["comments"] == 0]
cb_final = cb_zero_comments[:10] if cb_zero_comments else cb_candidates[:10]

print(f"\nFound {len(cb_candidates)} candidates ({len(cb_zero_comments)} with 0 comments). Top 5:")
for i, c in enumerate(cb_final[:5], 1):
    print(f"\n  {i}. {c['repo']}#{c['number']} ({c['comments']}c, {c['created']})")
    print(f"     title: {c['title']}")
    print(f"     labels: {c['labels']}")
    print(f"     url: {c['url']}")

