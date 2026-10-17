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

# New strategy: search repos by language with hacktoberfest topic
# Languages we know well: Python, Rust, Lua, TypeScript, JavaScript
print("=" * 70)
print("CODEBERG — repos sorted by recency (pushed last 7 days)")
print("=" * 70)

all_repos = []
for page in range(1, 6):
    code, d = api(f"https://codeberg.org/api/v1/repos/search?q=hacktoberfest&topic=true&limit=50&page={page}&sort=updated&order=desc", delay=2)
    if code != 200:
        break
    items = d if isinstance(d, list) else d.get("data", [])
    if not items:
        break
    all_repos.extend(items)

print(f"Total repos with topic hacktoberfest: {len(all_repos)}")
# Filter to active in last 7 days
recent = [r for r in all_repos if r.get('updated_at', '2000')[:10] >= '2026-10-09']
print(f"Active in last 7 days: {len(recent)}")

# Now check issues with any label of interest
print("\n=== Checking active repos for hacktoberfest issues (any state) ===")
candidates = []
for r in recent:
    repo_full = r.get('full_name', '')
    if r.get('archived', False): continue
    if r.get('fork', False): continue  # skip forks
    stars = r.get('stars_count', 0)
    if stars < 1: continue
    # Get ALL open issues
    time.sleep(1)
    code, d = api(f"https://codeberg.org/api/v1/repos/{repo_full}/issues?state=open&type=issues&limit=30", delay=1)
    if code != 200:
        continue
    items = d if isinstance(d, list) else d.get("data", [])
    for it in items[:10]:
        if it.get("comments", 0) != 0: continue
        if it.get("assignees"): continue
        title = it.get("title", "")
        if any(kw in title.lower() for kw in ["update dependency", "chore(deps)", "bump ", "renovate"]):
            continue
        labels = [l.get("name", "") for l in it.get("labels", [])][:5]
        # Filter: must have hacktoberfest label OR repo has topic hacktoberfest
        has_hf_label = any("hacktober" in l.lower() for l in labels)
        has_gfi_label = any("good first" in l.lower() for l in labels)
        has_help_label = any("help wanted" in l.lower() for l in labels)
        # Pick only if label has hacktoberfest OR (repo has topic hacktoberfest AND has gfi/help)
        if has_hf_label or ((has_gfi_label or has_help_label) and stars >= 5):
            candidates.append({
                "repo": repo_full,
                "number": it.get("number"),
                "title": title[:90],
                "labels": labels,
                "created": (it.get("created_at") or "?")[:10],
                "repo_stars": stars,
                "repo_forks": r.get('forks_count', 0),
                "repo_lang": r.get('language', '?'),
                "repo_pushed": r.get('updated_at', '?')[:10],
                "url": it.get("html_url", ""),
            })

# Sort by repo stars desc, then by created desc
candidates.sort(key=lambda c: (-c["repo_stars"], c["created"]), reverse=False)
candidates.sort(key=lambda c: -c["repo_stars"])

print(f"\nFiltered candidates: {len(candidates)}")
for c in candidates[:25]:
    print(f"\n- {c['repo']}#{c['number']} ({c['repo_stars']}⭐ {c['repo_lang']} pushed {c['repo_pushed']})")
    print(f"  title: {c['title']}")
    print(f"  labels: {c['labels']}")
    print(f"  url: {c['url']}")
