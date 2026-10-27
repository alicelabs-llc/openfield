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
        return e.code, {"error": e.read().decode()[:300]}
    except Exception as e:
        return -1, {"error": str(e)[:200]}

# ============================================================
# GITHUB — Search for issues in your own repos (ATC/UTA related)
# ============================================================
print("=" * 70)
print("GITHUB — Issues in alicelabs-llc repos (ATC/UTA)")
print("=" * 70)

YOUR_REPOS = [
    "alicelabs-llc/universal-trust-adapter",
    "alicelabs-llc/marketnow",
    "eddyflores100-lang/alethech",
    "alicelabs-llc/NexusCold",
]

for repo in YOUR_REPOS:
    print(f"\n--- {repo} ---")
    code, d = fetch(f"https://api.github.com/repos/{repo}/issues?state=open&per_page=10&sort=created&direction=desc", GH_HEADERS, delay=2)
    if code != 200:
        print(f"  HTTP {code}")
        continue
    items = [it for it in d if "pull_request" not in it]
    print(f"  Open issues: {len(items)}")
    for it in items[:5]:
        num = it.get("number")
        title = it.get("title","")[:70]
        labels = [l.get("name","") for l in it.get("labels",[])][:5]
        comments = it.get("comments",0)
        assignee = it.get("assignee")
        if assignee:
            continue
        print(f"  #{num} ({comments}c): {title}")
        print(f"    labels: {labels}")

# ============================================================
# GITHUB — Search for UTA/ATC related repos with open issues
# ============================================================
print("\n" + "=" * 70)
print("GITHUB — Search: 'universal trust adapter' OR 'agent trust'")
print("=" * 70)

queries = [
    "universal+trust+adapter+in:readme+state:open+type:issue",
    "agent+trust+verification+in:readme+state:open+type:issue",
    "ATC+1.0+trust+state:open+type:issue",
    "x402+trust+state:open+type:issue",
    "verifiable+agent+trust+state:open+type:issue",
]

for q in queries:
    code, d = fetch(f"https://api.github.com/search/issues?q={q}&per_page=5&sort=created&order=desc", GH_HEADERS, delay=3)
    if code != 200:
        continue
    items = d.get("items", [])
    if not items:
        continue
    for it in items[:3]:
        if "pull_request" in it:
            continue
        repo = it.get("repository_url","").replace("https://api.github.com/repos/","")
        num = it.get("number")
        title = it.get("title","")[:60]
        print(f"  {repo}#{num}: {title}")

# ============================================================
# GITLAB — Search for ATC/UTA in your own GitLab repos
# ============================================================
print("\n" + "=" * 70)
print("GITLAB — Search in eddyflores100 repos")
print("=" * 70)

# List your GitLab projects
code, d = fetch("https://gitlab.com/api/v4/users/eddyflores100/projects?per_page=20&order_by=last_activity_at", GL_HEADERS, delay=10)
if code == 200 and isinstance(d, list):
    print(f"Your GitLab projects: {len(d)}")
    for p in d:
        name = p.get("path_with_namespace","?")
        pid = p.get("id")
        issues_count = p.get("open_issues_count",0)
        print(f"  {name} (pid={pid}) open_issues={issues_count}")
        if issues_count > 0:
            # Get issues
            code2, d2 = fetch(f"https://gitlab.com/api/v4/projects/{pid}/issues?state=opened&per_page=10&sort=desc&order_by=created_at", GL_HEADERS, delay=8)
            if code2 == 200 and isinstance(d2, list):
                for it in d2[:5]:
                    if it.get("assignees"):
                        continue
                    title = it.get("title","")[:60]
                    iid = it.get("iid")
                    labels = it.get("labels",[])
                    print(f"    !{iid}: {title} [{labels[:3]}]")
else:
    print(f"  HTTP {code}: {str(d)[:200]}")

# ============================================================
# CODEBERG — Search for trust/ATC/UTA related repos
# ============================================================
print("\n" + "=" * 70)
print("CODEBERG — Search for trust/ATC/UTA repos")
print("=" * 70)

for q in ["trust", "agent+trust", "verifiable", "ATC"]:
    code, d = fetch(f"https://codeberg.org/api/v1/repos/search?q={q}&limit=10&sort=stars&order=desc", CB_HEADERS, delay=3)
    if code != 200:
        continue
    items = d if isinstance(d, list) else d.get("data", [])
    for r in items[:3]:
        name = r.get("full_name","?")
        stars = r.get("stars_count",0)
        desc = r.get("description","")[:60]
        if stars < 1:
            continue
        print(f"  {name} ⭐{stars}: {desc}")

# ============================================================
# Also check: issues in eddyflores100-lang GitHub repos
# ============================================================
print("\n" + "=" * 70)
print("GITHUB — Issues in ALL eddyflores100-lang repos")
print("=" * 70)

code, d = fetch("https://api.github.com/users/eddyflores100-lang/repos?per_page=100&sort=updated&direction=desc", GH_HEADERS, delay=2)
if code == 200:
    for r in d[:20]:
        name = r.get("name","?")
        issues = r.get("open_issues_count",0)
        if issues > 0:
            print(f"\n  --- {name} ({issues} open issues) ---")
            code2, d2 = fetch(f"https://api.github.com/repos/eddyflores100-lang/{name}/issues?state=open&per_page=10&sort=created&direction=desc", GH_HEADERS, delay=2)
            if code2 == 200:
                items = [it for it in d2 if "pull_request" not in it]
                for it in items[:5]:
                    if it.get("assignee"):
                        continue
                    num = it.get("number")
                    title = it.get("title","")[:60]
                    labels = [l.get("name","") for l in it.get("labels",[])][:5]
                    print(f"    #{num}: {title} [{labels[:3]}]")
