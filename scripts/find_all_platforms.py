import json, urllib.request, ssl, time

CB_TOKEN = "86f56136e9bdbe4a6fe60d0b8f2e4c277f407590"
GL_TOKEN = "glpat-VTdIPfmOYCLcAQHp0IdlyWM6MQpvOjEKdTpranZqbQ8.01.17073yv2r"
CB_HEADERS = {"Authorization": f"token {CB_TOKEN}", "Content-Type": "application/json", "Accept": "application/json", "User-Agent": "Mozilla/5.0"}
GL_HEADERS = {"PRIVATE-TOKEN": GL_TOKEN, "User-Agent": "Mozilla/5.0", "Accept": "application/json"}
CTX = ssl.create_default_context()

def fetch(url, headers, delay=3):
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
# CODEBERG — Deep search: all repos with hacktoberfest topic
# ============================================================
print("=" * 70)
print("CODEBERG — All active repos with hacktoberfest topic")
print("=" * 70)

all_repos = []
for page in range(1, 6):
    code, d = fetch(f"https://codeberg.org/api/v1/repos/search?q=hacktoberfest&topic=true&limit=50&page={page}&sort=updated&order=desc", CB_HEADERS, delay=3)
    if code != 200:
        break
    items = d if isinstance(d, list) else d.get("data", [])
    if not items:
        break
    all_repos.extend(items)

# Filter: active in last 7 days, not fork, not archived, 3+ stars
recent = [r for r in all_repos if r.get("updated_at","2000")[:10] >= "2026-10-15" and not r.get("archived",False) and not r.get("fork",False)]
print(f"Total repos: {len(all_repos)}, active last 7 days: {len(recent)}")

# Check issues in each active repo
cb_candidates = []
for r in recent:
    repo = r.get("full_name","")
    stars = r.get("stars_count",0)
    lang = r.get("language","?")
    pushed = (r.get("updated_at","?"))[:10]
    # Get ALL open issues
    code, d = fetch(f"https://codeberg.org/api/v1/repos/{repo}/issues?state=open&type=issues&limit=20&sort=created&order=desc", CB_HEADERS, delay=2)
    if code != 200:
        continue
    items = d if isinstance(d, list) else d.get("data", [])
    for it in items[:5]:
        if it.get("assignees"):
            continue
        title = it.get("title","")
        if any(kw in title.lower() for kw in ["update dependency", "chore(deps)", "bump "]):
            continue
        comments = it.get("comments",0)
        if comments > 3:
            continue
        labels = [l.get("name","") for l in it.get("labels",[])][:5]
        cb_candidates.append({
            "repo": repo,
            "number": it.get("number"),
            "title": title[:70],
            "labels": labels,
            "comments": comments,
            "created": (it.get("created_at") or "?")[:10],
            "url": it.get("html_url",""),
            "repo_stars": stars,
            "repo_lang": lang,
            "repo_pushed": pushed,
        })

print(f"\nCodeberg candidates: {len(cb_candidates)}")
for i, c in enumerate(cb_candidates[:10], 1):
    print(f"\n  {i}. {c['repo']}#{c['number']} ({c['comments']}c, ⭐{c['repo_stars']}, {c['repo_lang']}, pushed {c['repo_pushed']})")
    print(f"     title: {c['title']}")
    print(f"     labels: {c['labels']}")
    print(f"     url: {c['url']}")

# ============================================================
# GITLAB — Try direct API on specific known repos
# ============================================================
print("\n\n" + "=" * 70)
print("GITLAB — Direct repo checks")
print("=" * 70)

# Try repos that might have issues
gitlab_targets = [
    ("gitlab-org/gitlab", 278964),
    ("gitlab-org/gitlab-runner", 250833),
    ("gitlab-org/cng", 278962),
    ("gitlab-org/cluster-integration", 4193167),
    ("gitlab-org/release-tools", 727412),
    ("gitlab-org/quality", 7330824),
    ("gitlab-com/www-gitlab-com", 2758335),
]

gl_candidates = []
for name, pid in gitlab_targets:
    code, d = fetch(f"https://gitlab.com/api/v4/projects/{pid}/issues?state=opened&labels=good+first+issue&per_page=5&sort=desc&order_by=created_at", GL_HEADERS, delay=12)
    if code == 200 and isinstance(d, list) and len(d) > 0:
        print(f"\n  {name} ({len(d)} good first issues):")
        for it in d[:3]:
            if it.get("assignees"):
                continue
            title = it.get("title","")[:60]
            iid = it.get("iid")
            labels = it.get("labels",[])
            print(f"    !{iid}: {title} [{labels[:3]}]")
            gl_candidates.append({
                "repo": name,
                "iid": iid,
                "title": title,
                "url": it.get("web_url",""),
            })
    elif code == 200 and isinstance(d, list) and len(d) == 0:
        print(f"  {name}: 0 good first issues")
    else:
        print(f"  {name}: HTTP {code}")

# Also try: search for "help wanted" label
for name, pid in gitlab_targets[:3]:
    code, d = fetch(f"https://gitlab.com/api/v4/projects/{pid}/issues?state=opened&labels=help+wanted&per_page=5&sort=desc&order_by=created_at", GL_HEADERS, delay=10)
    if code == 200 and isinstance(d, list) and len(d) > 0:
        print(f"\n  {name} ({len(d)} help wanted issues):")
        for it in d[:3]:
            if it.get("assignees"):
                continue
            title = it.get("title","")[:60]
            iid = it.get("iid")
            print(f"    !{iid}: {title}")
            gl_candidates.append({
                "repo": name,
                "iid": iid,
                "title": title,
                "url": it.get("web_url",""),
            })

print(f"\nGitLab candidates: {len(gl_candidates)}")

# ============================================================
# Also try: GitLab global issues search with different terms
# ============================================================
print("\n" + "=" * 70)
print("GITLAB — Global issue search")
print("=" * 70)

for search_term in ["trust", "crypto", "signature", "verify", "security", "attestation"]:
    code, d = fetch(f"https://gitlab.com/api/v4/issues?search={search_term}&state=opened&per_page=3&sort=desc&order_by=created_at", GL_HEADERS, delay=15)
    if code == 200 and isinstance(d, list):
        for it in d[:2]:
            proj_id = it.get("project_id")
            title = it.get("title","")[:60]
            iid = it.get("iid")
            url = it.get("web_url","")
            labels = it.get("labels",[])
            print(f"  !{iid}: {title} [{labels[:3]}]")
            print(f"    url: {url}")
    elif code == 200:
        pass  # empty
    else:
        print(f"  search '{search_term}': HTTP {code}")

