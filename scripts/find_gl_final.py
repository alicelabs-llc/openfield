import json, urllib.request, ssl, time

GL_TOKEN = "glpat-VTdIPfmOYCLcAQHp0IdlyWM6MQpvOjEKdTpranZqbQ8.01.17073yv2r"
GL_HEADERS = {"PRIVATE-TOKEN": GL_TOKEN, "User-Agent": "Mozilla/5.0", "Accept": "application/json"}
CTX = ssl.create_default_context()

def fetch(url, delay=10):
    time.sleep(delay)
    req = urllib.request.Request(url, headers=GL_HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:300]}
    except Exception as e:
        return -1, {"error": str(e)[:200]}

# GitLab GraphQL with correct field name
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
    print(f"Found {len(projects)} GitLab projects via search")
    gl_candidates = []
    for p in projects:
        repo = p.get("fullPath","")
        stars = p.get("starCount",0)
        issues = p.get("issues",{}).get("nodes",[])
        if not issues:
            continue
        for issue in issues:
            labels = [l.get("name","") for l in issue.get("labels",{}).get("nodes",[])]
            gl_candidates.append({
                "repo": repo,
                "iid": issue.get("iid"),
                "title": issue.get("title","")[:80],
                "labels": labels,
                "created": (issue.get("createdAt") or "?")[:10],
                "url": issue.get("webUrl",""),
                "stars": stars,
            })
    
    print(f"\nGitLab hacktoberfest issues: {len(gl_candidates)}")
    for i, c in enumerate(gl_candidates[:10], 1):
        print(f"  {i}. {c['repo']}!{c['iid']} (⭐{c['stars']}, {c['created']})")
        print(f"     title: {c['title']}")
        print(f"     labels: {c['labels']}")
        print(f"     url: {c['url']}")
except Exception as e:
    print(f"GraphQL error: {e}")

# Also try: list GitLab projects with "hacktoberfest" as a topic
print("\n" + "="*60)
print("GitLab projects with hacktoberfest topic")
print("="*60)
code, d = fetch("https://gitlab.com/api/v4/projects?topic=hacktoberfest&per_page=20&order_by=last_activity_at", delay=10)
if code == 200 and isinstance(d, list):
    print(f"Found {len(d)} repos with hacktoberfest topic")
    for p in d[:10]:
        repo = p.get("path_with_namespace","?")
        pid = p.get("id")
        stars = p.get("star_count",0)
        issues_count = p.get("open_issues_count",0)
        pushed = (p.get("last_activity_at","?"))[:10]
        print(f"  - {repo} ⭐{stars} issues:{issues_count} pushed:{pushed}")
        # Get issues for each
        if issues_count > 0:
            code2, d2 = fetch(f"https://gitlab.com/api/v4/projects/{pid}/issues?state=opened&labels=hacktoberfest&per_page=5&sort=desc&order_by=created_at", delay=8)
            if code2 == 200 and isinstance(d2, list):
                for it in d2[:3]:
                    title = it.get("title","")[:60]
                    iid = it.get("iid")
                    labels = it.get("labels",[])
                    if it.get("assignees"):
                        continue
                    print(f"    !{iid}: {title} [{labels[:3]}]")
