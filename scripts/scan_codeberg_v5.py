import json, urllib.request, ssl, time

HEADERS = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
CTX = ssl.create_default_context()

def api(url, delay=2):
    time.sleep(delay)
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:200]}
    except Exception as e:
        return -1, {"error": str(e)[:200]}

# Look at the 23 active repos in last 7 days — see what their issues look like
print("=" * 70)
print("ACTIVE repos in last 7 days with topic hacktoberfest — list issues")
print("=" * 70)

all_repos = []
for page in range(1, 6):
    code, d = api(f"https://codeberg.org/api/v1/repos/search?q=hacktoberfest&topic=true&limit=50&page={page}&sort=updated&order=desc", delay=2)
    if code != 200: break
    items = d if isinstance(d, list) else d.get("data", [])
    all_repos.extend(items)

recent = [r for r in all_repos if r.get('updated_at', '2000')[:10] >= '2026-10-09' and not r.get('archived', False) and not r.get('fork', False)]
print(f"\n{len(recent)} active repos in last 7 days:")
for r in recent:
    print(f"  - {r.get('full_name','?')} ⭐{r.get('stars_count',0)} forks:{r.get('forks_count',0)} lang:{r.get('language','?')} pushed:{r.get('updated_at','?')[:10]}")

# For each, list all open issues (not just labeled ones)
print("\n" + "=" * 70)
print("All open issues from these active repos (0 comments, no assignee)")
print("=" * 70)

candidates = []
for r in recent[:20]:
    repo_full = r.get('full_name', '')
    if not repo_full: continue
    stars = r.get('stars_count', 0)
    if stars < 1: continue
    time.sleep(1)
    code, d = api(f"https://codeberg.org/api/v1/repos/{repo_full}/issues?state=open&type=issues&limit=20&sort=created&order=desc", delay=1)
    if code != 200: continue
    items = d if isinstance(d, list) else d.get("data", [])
    for it in items[:8]:
        if it.get("comments", 0) != 0: continue
        if it.get("assignees"): continue
        title = it.get("title", "")
        if any(kw in title.lower() for kw in ["update dependency", "chore(deps)", "bump ", "renovate"]):
            continue
        labels = [l.get("name", "") for l in it.get("labels", [])][:5]
        # Show ALL issues, not just labeled ones
        candidates.append({
            "repo": repo_full,
            "number": it.get("number"),
            "title": title[:90],
            "labels": labels,
            "created": (it.get("created_at") or "?")[:10],
            "repo_stars": stars,
            "repo_lang": r.get('language', '?'),
            "url": it.get("html_url", ""),
        })

print(f"\nTotal candidates: {len(candidates)}")
candidates.sort(key=lambda c: -c["repo_stars"])
for c in candidates[:30]:
    print(f"\n- {c['repo']}#{c['number']} ({c['repo_stars']}⭐ {c['repo_lang']})")
    print(f"  title: {c['title']}")
    print(f"  labels: {c['labels']}")
    print(f"  created: {c['created']}")
    print(f"  url: {c['url']}")
