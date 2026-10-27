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
        return e.code, {"error": e.read().decode()[:300]}
    except Exception as e:
        return -1, {"error": str(e)[:200]}

# ============================================================
# CODEBERG — Try different search approach
# ============================================================
print("=" * 70)
print("CODEBERG — All repos with hacktoberfest topic (sorted by stars)")
print("=" * 70)

all_repos = []
for page in range(1, 4):
    code, d = fetch(f"https://codeberg.org/api/v1/repos/search?q=hacktoberfest&topic=true&limit=50&page={page}&sort=stars&order=desc", CB_HEADERS, delay=3)
    if code != 200:
        break
    items = d if isinstance(d, list) else d.get("data", [])
    all_repos.extend(items)
    if len(items) < 50:
        break

print(f"Found {len(all_repos)} repos with hacktoberfest topic")

# Filter: active in last 14 days, stars >= 5
active = [r for r in all_repos if r.get("updated_at","2000")[:10] >= "2026-10-07" and r.get("stars_count",0) >= 3 and not r.get("archived",False) and not r.get("fork",False)]
print(f"Active (last 14d, 3+ stars): {len(active)}")

# For top 10 active repos, check their issues
print(f"\nChecking issues in top 10 active repos...")
cb_candidates = []
for r in active[:10]:
    repo = r.get("full_name","")
    stars = r.get("stars_count",0)
    pushed = (r.get("updated_at","?"))[:10]
    lang = r.get("language","?")
    print(f"\n  --- {repo} ⭐{stars} lang={lang} pushed={pushed} ---")
    
    # Get issues
    code, d = fetch(f"https://codeberg.org/api/v1/repos/{repo}/issues?state=open&type=issues&limit=20&sort=created&order=desc", CB_HEADERS, delay=2)
    if code != 200:
        continue
    items = d if isinstance(d, list) else d.get("data", [])
    print(f"  Open issues: {len(items)}")
    for it in items[:8]:
        if it.get("assignees"):
            continue
        title = it.get("title","")
        if any(kw in title.lower() for kw in ["update dependency", "chore(deps)", "bump ", "renovate"]):
            continue
        labels = [l.get("name","") for l in it.get("labels",[])][:5]
        comments = it.get("comments",0)
        if comments > 3:
            continue
        cb_candidates.append({
            "repo": repo,
            "number": it.get("number"),
            "title": title[:80],
            "labels": labels,
            "comments": comments,
            "created": (it.get("created_at") or "?")[:10],
            "url": it.get("html_url",""),
            "repo_stars": stars,
            "repo_lang": lang,
        })

print(f"\n{'='*70}")
print(f"CODEBERG — {len(cb_candidates)} candidates found")
print(f"{'='*70}")
for i, c in enumerate(cb_candidates[:10], 1):
    print(f"\n  {i}. {c['repo']}#{c['number']} ({c['comments']}c, ⭐{c['repo_stars']}, {c['repo_lang']})")
    print(f"     title: {c['title']}")
    print(f"     labels: {c['labels']}")
    print(f"     url: {c['url']}")

# ============================================================
# GITLAB — Try GraphQL for issues with hacktoberfest label
# ============================================================
print("\n\n" + "=" * 70)
print("GITLAB — GraphQL search for hacktoberfest issues")
print("=" * 70)

query = """
{
  projects(membership: false, search: "hacktoberfest", first: 20) {
    nodes {
      fullPath
      starCount
      issues(state: OPENED, labelName: ["hacktoberfest"], first: 5) {
        nodes {
          iid
          title
          createdAt
          webUrl
          labels { nodes { name } }
        }
      }
    }
  }
}
"""
payload = json.dumps({"query": query}).encode()
req = urllib.request.Request(
    "https://gitlab.com/api/graphql",
    data=payload,
    headers={**GL_HEADERS, "Content-Type": "application/json"},
    method="POST",
)
try:
    with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
        d = json.loads(resp.read().decode())
    projects = d.get("data",{}).get("projects",{}).get("nodes",[])
    print(f"Found {len(projects)} projects with hacktoberfest issues:")
    gl_candidates = []
    for p in projects:
        repo = p.get("fullName","")
        stars = p.get("starCount",0)
        issues = p.get("issues",{}).get("nodes",[])
        if not issues:
            continue
        print(f"\n  --- {repo} ⭐{stars} ---")
        for issue in issues:
            labels = [l.get("name","") for l in issue.get("labels",{}).get("nodes",[])]
            print(f"  !{issue.get('iid')}: {issue.get('title','')[:60]} ({issue.get('createdAt','?')[:10]})")
            gl_candidates.append({
                "repo": repo,
                "iid": issue.get("iid"),
                "title": issue.get("title","")[:80],
                "labels": labels,
                "created": (issue.get("createdAt") or "?")[:10],
                "url": issue.get("webUrl",""),
            })
    print(f"\nGitLab candidates: {len(gl_candidates)}")
except Exception as e:
    print(f"GraphQL error: {e}")
