import json, urllib.request, ssl, time

GL_TOKEN = "glpat-VTdIPfmOYCLcAQHp0IdlyWM6MQpvOjEKdTpranZqbQ8.01.17073yv2r"
CB_TOKEN = "86f56136e9bdbe4a6fe60d0b8f2e4c277f407590"

GL_HEADERS = {"PRIVATE-TOKEN": GL_TOKEN, "User-Agent": "Mozilla/5.0", "Accept": "application/json"}
CB_HEADERS = {"Authorization": f"token {CB_TOKEN}", "Content-Type": "application/json", "Accept": "application/json", "User-Agent": "Mozilla/5.0"}
CTX = ssl.create_default_context()

def fetch(url, headers, delay=3):
    time.sleep(delay)
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:200]}
    except Exception as e:
        return -1, {"error": str(e)[:200]}

# ============================================================
# GITLAB — Search known hacktoberfest repos
# ============================================================
print("=" * 70)
print("GITLAB — Searching repos with hacktoberfest topic")
print("=" * 70)

# GitLab doesn't have a global issue search, so we list repos with hacktoberfest topic
# and then check each repo's issues
gl_repos_to_check = [
    # Known active repos
    ("inkscape/extensions", 5833962),
    ("OpenMW/openmw", 7107382),
    ("fdroid/fdroidclient", 36189),
    # Try some new ones
]

# Search for repos with hacktoberfest label on GitLab
# GitLab has /projects?with_issues=true&topic=hacktoberfest
code, d = fetch("https://gitlab.com/api/v4/projects?topic=hacktoberfest&per_page=20&order_by=last_activity_at", GL_HEADERS, delay=5)
if code == 200 and isinstance(d, list):
    print(f"Found {len(d)} repos with hacktoberfest topic:")
    for p in d[:10]:
        print(f"  - {p.get('path_with_namespace','?')} ⭐{p.get('star_count',0)} issues:{p.get('open_issues_count',0)} pushed:{p.get('last_activity_at','?')[:10]}")
        gl_repos_to_check.append((p.get('path_with_namespace'), p.get('id')))

# Now check issues for each repo
print(f"\n{'='*60}")
print("Checking issues in GitLab repos...")
print(f"{'='*60}")

gl_candidates = []
seen = set()
for name, pid in gl_repos_to_check[:10]:
    if name in seen:
        continue
    seen.add(name)
    code, d = fetch(f"https://gitlab.com/api/v4/projects/{pid}/issues?state=opened&labels=hacktoberfest&per_page=10&sort=desc&order_by=created_at", GL_HEADERS, delay=8)
    if code != 200:
        # Try without label filter
        code, d = fetch(f"https://gitlab.com/api/v4/projects/{pid}/issues?state=opened&per_page=5&sort=desc&order_by=created_at", GL_HEADERS, delay=8)
        if code != 200:
            continue
    if isinstance(d, list):
        for it in d[:5]:
            labels = it.get("labels", [])
            if "hacktoberfest" not in labels and "good first issue" not in labels:
                continue
            if it.get("assignees"):
                continue
            gl_candidates.append({
                "repo": name,
                "iid": it.get("iid"),
                "title": it.get("title","")[:80],
                "labels": labels[:5],
                "created": (it.get("created_at") or "?")[:10],
                "url": it.get("web_url",""),
            })

print(f"\nGitLab candidates: {len(gl_candidates)}")
for i, c in enumerate(gl_candidates[:5], 1):
    print(f"  {i}. {c['repo']}#{c['iid']} ({c['created']})")
    print(f"     title: {c['title']}")
    print(f"     labels: {c['labels']}")
    print(f"     url: {c['url']}")

# ============================================================
# CODEBERG — Search broader (good first issue OR help wanted)
# ============================================================
print("\n" + "=" * 70)
print("CODEBERG — Searching for issues (good first issue)")
print("=" * 70)

cb_candidates = []
for label in ["good%20first%20issue", "help%20wanted"]:
    for page in range(1, 3):
        code, d = fetch(f"https://codeberg.org/api/v1/repos/issues/search?labels={label}&state=open&type=issues&limit=50&page={page}", CB_HEADERS, delay=3)
        if code != 200:
            break
        items = d if isinstance(d, list) else d.get("data", [])
        if not items:
            break
        for it in items:
            repo_data = it.get("repository", {}) or {}
            repo = repo_data.get("full_name", "")
            if not repo:
                continue
            if it.get("assignees"):
                continue
            title = it.get("title", "")
            if any(kw in title.lower() for kw in ["update dependency", "chore(deps)", "bump "]):
                continue
            labels = [l.get("name","") for l in it.get("labels",[])][:5]
            cb_candidates.append({
                "repo": repo,
                "number": it.get("number"),
                "title": title[:80],
                "labels": labels,
                "comments": it.get("comments", 0),
                "created": (it.get("created_at") or "?")[:10],
                "url": it.get("html_url",""),
                "repo_stars": repo_data.get("stars_count", 0),
                "repo_updated": (repo_data.get("updated_at") or "?")[:10],
            })

# Filter: repo active in last 14 days + 0 comments preferred
recent = [c for c in cb_candidates if c["repo_updated"] >= "2026-10-07"]
zero_c = [c for c in recent if c["comments"] == 0]
final = zero_c[:15] if zero_c else recent[:15]

print(f"\nTotal: {len(cb_candidates)}, recent (14d): {len(recent)}, 0-comments: {len(zero_c)}")
print(f"Top 5:")
for i, c in enumerate(final[:5], 1):
    print(f"\n  {i}. {c['repo']}#{c['number']} ({c['comments']}c, ⭐{c['repo_stars']}, pushed {c['repo_updated']})")
    print(f"     title: {c['title']}")
    print(f"     labels: {c['labels']}")
    print(f"     url: {c['url']}")
