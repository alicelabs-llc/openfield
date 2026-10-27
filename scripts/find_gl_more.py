import json, ssl, time, urllib.request, urllib.error, urllib.parse

TOKEN = "glpat-PfWyLHoeZpLOyyQSzyDX72M6MQpvOjEKdTpranZqbQ8.01.1715hm5mn"
headers = {"PRIVATE-TOKEN": TOKEN, "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
CTX = ssl.create_default_context()

def fetch(url, delay=8):
    time.sleep(delay)
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:300]}
    except Exception as e:
        return -1, {"error": str(e)[:200]}

# Search for projects with open issues
print("=" * 70)
print("GITLAB — Searching for repos with open issues")
print("=" * 70)

# Try various search terms for projects
search_terms = [
    "crypto", "signature", "verify", "security", "trust",
    "python", "javascript", "documentation", "testing",
]

gl_projects = []
seen = set()

for term in search_terms:
    encoded = urllib.parse.quote(term)
    code, d = fetch(f"https://gitlab.com/api/v4/projects?search={encoded}&per_page=10&order_by=last_activity_at&sort=desc", delay=5)
    if code != 200 or not isinstance(d, list):
        continue
    for p in d:
        pid = p.get("id")
        if pid in seen:
            continue
        seen.add(pid)
        name = p.get("path_with_namespace","?")
        stars = p.get("star_count",0)
        issues = p.get("open_issues_count",0)
        lang = p.get("language","?")
        last_activity = (p.get("last_activity_at","2000"))[:10]
        if issues == 0:
            continue
        if last_activity < "2026-09-15":
            continue
        gl_projects.append({
            "name": name,
            "pid": pid,
            "stars": stars,
            "issues": issues,
            "lang": lang,
            "last_activity": last_activity,
        })

print(f"\nFound {len(gl_projects)} projects with open issues\n")

# For each project, check for good first issue / help wanted labels
gl_candidates = []
for p in gl_projects[:20]:
    # Get issues with labels
    code, d = fetch(f"https://gitlab.com/api/v4/projects/{p['pid']}/issues?state=opened&per_page=10&sort=desc&order_by=created_at", delay=5)
    if code != 200 or not isinstance(d, list):
        continue
    for it in d[:5]:
        if it.get("assignees"):
            continue
        labels = it.get("labels",[])
        title = it.get("title","")[:70]
        iid = it.get("iid")
        created = (it.get("created_at","?"))[:10]
        # Skip auto-generated/bot issues
        if any(kw in title.lower() for kw in ["update dependency", "chore(deps)", "bump "]):
            continue
        gl_candidates.append({
            "repo": p["name"],
            "iid": iid,
            "title": title,
            "labels": labels[:5],
            "created": created,
            "url": it.get("web_url",""),
            "stars": p["stars"],
            "lang": p["lang"],
        })

print(f"GitLab candidates: {len(gl_candidates)}\n")
for i, c in enumerate(gl_candidates[:15], 1):
    print(f"{i}. {c['repo']}!{c['iid']} (⭐{c['stars']}, {c['lang']}, {c['created']})")
    print(f"   title: {c['title']}")
    print(f"   labels: {c['labels']}")
    print(f"   url: {c['url']}")
    print()
