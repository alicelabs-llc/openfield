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
print("CODEBERG — issues con label 'hacktoberfest' o 'good first issue'")
print("Filtrado: 0 comments, no assignee, pushed last 30 days")
print("=" * 70)

# Get more results across multiple pages
all_items = []
for page in range(1, 5):
    code, d = api(f"https://codeberg.org/api/v1/repos/issues/search?labels=hacktoberfest&state=open&type=issues&limit=50&page={page}", delay=3)
    if code != 200:
        break
    items = d if isinstance(d, list) else d.get("data", [])
    if not items:
        break
    all_items.extend(items)
    print(f"  page {page}: {len(items)} issues")

print(f"\nTotal raw: {len(all_items)}")
print("\n=== Filtering: 0 comments, no assignee, repo active in last 30 days ===")

# Group by repo to avoid duplicate fetches
repos_seen = {}
good_candidates = []
for it in all_items:
    repo = it.get("repository", {}) or {}
    repo_full = repo.get("full_name", "")
    if not repo_full:
        continue
    if repo_full in repos_seen:
        repo_info = repos_seen[repo_full]
    else:
        # Fetch repo info once
        time.sleep(1)
        code, repo_data = api(f"https://codeberg.org/api/v1/repos/{repo_full}", delay=1)
        if code != 200:
            continue
        # Check pushed date
        pushed = repo_data.get("updated_at", "2000-01-01")[:10]
        archived = repo_data.get("archived", False)
        stars = repo_data.get("stars_count", 0)
        forks_count = repo_data.get("forks_count", 0)
        repo_info = {"pushed": pushed, "archived": archived, "stars": stars, "forks": forks_count}
        repos_seen[repo_full] = repo_info
    # Skip if repo not active recently
    if repo_info["pushed"] < "2026-09-15":
        continue
    if repo_info["archived"]:
        continue
    # Filter issues: 0 comments, no assignees
    if it.get("comments", 0) != 0:
        continue
    assignees = it.get("assignees") or []
    if assignees:
        continue
    title = it.get("title", "")
    # Skip auto-generated dep-update issues
    if any(kw in title.lower() for kw in ["update dependency", "chore(deps)", "bump "]):
        continue
    labels = [l.get("name", "") for l in it.get("labels", [])][:5]
    good_candidates.append({
        "repo": repo_full,
        "number": it.get("number"),
        "title": title[:90],
        "labels": labels,
        "created": (it.get("created_at") or "?")[:10],
        "repo_pushed": repo_info["pushed"],
        "repo_stars": repo_info["stars"],
        "repo_forks": repo_info["forks"],
        "url": it.get("html_url", ""),
    })

print(f"\nFiltered candidates: {len(good_candidates)}")
for c in good_candidates[:30]:
    print(f"\n- {c['repo']}#{c['number']} ({c['repo_stars']}⭐ {c['repo_forks']}forks, pushed {c['repo_pushed']})")
    print(f"  title: {c['title']}")
    print(f"  labels: {c['labels']}")
    print(f"  url: {c['url']}")
