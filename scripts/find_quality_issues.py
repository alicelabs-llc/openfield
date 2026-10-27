import json, urllib.request, ssl, time

TOKEN = "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"
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/vnd.github+json",
}
CTX = ssl.create_default_context()

def api(url, delay=2):
    time.sleep(delay)
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=15) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())

# Better queries: search for repos with hacktoberfest topic
# Then list their open issues with good-first-issue label
# Use proper URL encoding

queries = [
    # 1. repos with hacktoberfest topic, sorted by recency
    ("https://api.github.com/search/repositories?q=topic:hacktoberfest+language:Python+stars:<2000+pushed:>2026-10-01&sort=updated&order=desc&per_page=15", "Hacktoberfest topic Python"),
    ("https://api.github.com/search/repositories?q=topic:hacktoberfest+language:JavaScript+stars:<2000+pushed:>2026-10-01&sort=updated&order=desc&per_page=15", "Hacktoberfest topic JS"),
    ("https://api.github.com/search/repositories?q=topic:hacktoberfest+language:TypeScript+stars:<2000+pushed:>2026-10-01&sort=updated&order=desc&per_page=15", "Hacktoberfest topic TS"),
    ("https://api.github.com/search/repositories?q=topic:hacktoberfest+language:Go+stars:<2000+pushed:>2026-10-01&sort=updated&order=desc&per_page=15", "Hacktoberfest topic Go"),
    ("https://api.github.com/search/repositories?q=topic:hacktoberfest+language:Rust+stars:<2000+pushed:>2026-10-01&sort=updated&order=desc&per_page=15", "Hacktoberfest topic Rust"),
]

print("=" * 70)
print("STEP 1: Find hacktoberfest-topic repos (active in last 2 weeks)")
print("=" * 70)

candidate_repos = []
for url, label in queries:
    print(f"\n--- {label} ---")
    code, d = api(url, delay=3)
    if code != 200:
        print(f"  HTTP {code}: {str(d)[:200]}")
        continue
    items = d.get("items", [])
    print(f"  total: {d.get('total_count',0)}, top {len(items)}")
    for r in items[:10]:
        repo_full = r.get("full_name","?")
        stars = r.get("stargazers_count",0)
        pushed = r.get("pushed_at","?")[:10]
        open_issues = r.get("open_issues_count",0)
        archived = r.get("archived",False)
        disabled = r.get("disabled",False)
        # Filter: active, not too few issues, not archived
        if archived or disabled or open_issues < 3:
            continue
        print(f"  - {repo_full} ⭐{stars} open:{open_issues} pushed:{pushed}")
        candidate_repos.append({
            "full_name": repo_full,
            "stars": stars,
            "open_issues": open_issues,
            "pushed": pushed,
        })

# Step 2: For each candidate, list issues with good-first-issue or help wanted
print("\n" + "=" * 70)
print(f"STEP 2: Look at issues in {len(candidate_repos)} repos")
print("=" * 70)

good_candidates = []
for repo in candidate_repos[:25]:  # limit to top 25
    rf = repo["full_name"]
    time.sleep(2)
    # Search for open issues with help wanted or good first issue
    q = f"repo:{rf}+state:open+label:\"good first issue\""
    url = f"https://api.github.com/search/issues?q={urllib.parse.quote(q)}&per_page=5"
    code, d = api(url, delay=1)
    if code != 200:
        continue
    items = d.get("items", [])
    if not items:
        # try help wanted
        q = f"repo:{rf}+state:open+label:\"help wanted\""
        url = f"https://api.github.com/search/issues?q={urllib.parse.quote(q)}&per_page=5"
        time.sleep(2)
        code, d = api(url, delay=1)
        if code == 200:
            items = d.get("items", [])
    if not items:
        continue
    print(f"\n  {rf} ({repo['stars']}⭐, {repo['open_issues']} open issues, last push {repo['pushed']}):")
    for it in items[:3]:
        num = it.get("number")
        title = it.get("title","")[:75]
        labels = [l.get("name","") for l in it.get("labels",[])][:4]
        comments = it.get("comments",0)
        assignee = it.get("assignee")
        if assignee:
            continue  # skip assigned
        # Skip auto-generated issues (dependabot etc.)
        if any(kw in title.lower() for kw in ["update dependency", "update dependency @types", "bump ", "chore(deps)"]):
            continue
        print(f"    #{num} ({comments}c): {title}")
        print(f"      labels: {labels}")
        print(f"      url: {it.get('html_url','?')}")
        good_candidates.append({
            "repo": rf,
            "number": num,
            "title": title,
            "labels": labels,
            "comments": comments,
            "url": it.get("html_url",""),
        })

print("\n" + "=" * 70)
print(f"FINAL CANDIDATES: {len(good_candidates)}")
print("=" * 70)
for c in good_candidates[:20]:
    print(f"- {c['repo']}#{c['number']} ({c['comments']}c): {c['title']}")
