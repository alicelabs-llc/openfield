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

print("=" * 70)
print("CODEBERG — repos con topic 'hacktoberfest' (sorted by stars)")
print("=" * 70)

# Get top repos with hacktoberfest topic
all_repos = []
for page in range(1, 4):
    code, d = api(f"https://codeberg.org/api/v1/repos/search?q=hacktoberfest&topic=true&limit=50&page={page}&sort=stars&order=desc", delay=3)
    if code != 200:
        break
    items = d if isinstance(d, list) else d.get("data", [])
    if not items:
        break
    all_repos.extend(items)
    print(f"  page {page}: {len(items)} repos")

print(f"\nTotal repos: {len(all_repos)}")
print("\n=== Top 25 repos with topic hacktoberfest ===")
for r in all_repos[:25]:
    stars = r.get('stars_count', 0)
    forks = r.get('forks_count', 0)
    if stars < 1: continue
    print(f"  - {r.get('full_name','?')} ⭐{stars} forks:{forks} lang:{r.get('language','?')} pushed:{r.get('updated_at','?')[:10]}")

print("\n" + "=" * 70)
print("ISSUES — top repos with topic hacktoberfest (0 comments, no assignee)")
print("=" * 70)

candidates = []
for r in all_repos[:30]:
    repo_full = r.get('full_name', '')
    if not repo_full:
        continue
    stars = r.get('stars_count', 0)
    if stars < 1:
        continue
    pushed = r.get('updated_at', '2000')[:10]
    if pushed < '2026-09-01':
        continue
    # Get open issues with labels hacktoberfest OR good first issue
    for label_query in ["hacktoberfest", "good%20first%20issue", "help%20wanted"]:
        time.sleep(1)
        code, d = api(f"https://codeberg.org/api/v1/repos/{repo_full}/issues?labels={label_query}&state=open&type=issues&limit=15", delay=1)
        if code != 200:
            continue
        items = d if isinstance(d, list) else d.get("data", [])
        for it in items:
            if it.get("comments", 0) != 0:
                continue
            if it.get("assignees"):
                continue
            title = it.get("title", "")
            if any(kw in title.lower() for kw in ["update dependency", "chore(deps)", "bump "]):
                continue
            labels = [l.get("name", "") for l in it.get("labels", [])][:5]
            # Skip if we already have this issue
            num = it.get("number")
            key = (repo_full, num)
            if any(c["repo"] == repo_full and c["number"] == num for c in candidates):
                continue
            candidates.append({
                "repo": repo_full,
                "number": num,
                "title": title[:90],
                "labels": labels,
                "created": (it.get("created_at") or "?")[:10],
                "repo_stars": stars,
                "repo_forks": r.get('forks_count', 0),
                "repo_pushed": pushed,
                "url": it.get("html_url", ""),
            })

print(f"\nFiltered candidates: {len(candidates)}")
for c in candidates[:20]:
    print(f"\n- {c['repo']}#{c['number']} ({c['repo_stars']}⭐ pushed {c['repo_pushed']})")
    print(f"  title: {c['title']}")
    print(f"  labels: {c['labels']}")
    print(f"  url: {c['url']}")
