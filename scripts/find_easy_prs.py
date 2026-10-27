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

# Strategy: search for issues with multiple hacktoberfest-friendly labels
# Look for: help wanted + (good first issue OR hacktoberfest) + small repos (more responsive)
# Languages: Python, JavaScript, TypeScript, Rust, Go (quick to fix)
# Updated recently (active maintainers)
# Excluding repos we already touched

queries = [
    # Plain hacktoberfest-accepted issues (most likely to be merged)
    ('hacktoberfest+state:open+label:"good first issue"+no:assignee+created:>2026-09-15+language:Python+stars:<500', 'Python easy'),
    ('hacktoberfest+state:open+label:"good first issue"+no:assignee+created:>2026-09-15+language:JavaScript+stars:<500', 'JS easy'),
    ('hacktoberfest+state:open+label:"good first issue"+no:assignee+created:>2026-09-15+language:TypeScript+stars:<500', 'TS easy'),
    ('hacktoberfest+state:open+label:"good first issue"+no:assignee+created:>2026-09-15+language:Rust+stars:<500', 'Rust easy'),
    ('hacktoberfest+state:open+label:"good first issue"+no:assignee+created:>2026-09-15+language:Go+stars:<500', 'Go easy'),
    # Try docs-only (super easy merges)
    ('label:hacktoberfest+label:documentation+state:open+no:assignee+created:>2026-09-20+stars:<1000', 'Docs'),
    # Try bug-fix tagged with hacktoberfest
    ('label:hacktoberfest+label:bug+state:open+no:assignee+created:>2026-09-15+stars:<300', 'Bug'),
]

print("=" * 70)
print("SEARCH: HACKTOBERFEST-FRIENDLY ISSUES (no assignee, small repos)")
print("=" * 70)

candidates = []
for q, label in queries:
    print(f"\n--- {label} ---")
    url = f"https://api.github.com/search/issues?q={urllib.parse.quote(q)}&sort=updated&order=desc&per_page=10"
    code, d = api(url, delay=3)
    if code != 200:
        print(f"  HTTP {code}: {str(d)[:200]}")
        continue
    items = d.get("items", [])
    total = d.get("total_count", 0)
    print(f"  total_count: {total}, showing top {len(items)}")
    for it in items[:8]:
        repo_url = it.get("repository_url", "")
        repo_full = repo_url.replace("https://api.github.com/repos/", "")
        number = it.get("number")
        title = it.get("title", "")[:80]
        labels = [l.get("name","") for l in it.get("labels",[])]
        comments = it.get("comments", 0)
        updated = it.get("updated_at","?")[:10]
        # Only consider issues with no comments (less competition)
        if comments > 3:
            continue
        print(f"  - {repo_full}#{number} ({comments}c, upd {updated}): {title}")
        print(f"    labels: {labels[:5]}")
        candidates.append({
            "repo": repo_full,
            "number": number,
            "title": title,
            "labels": labels,
            "comments": comments,
            "updated": updated,
            "url": it.get("html_url", ""),
        })

print("\n" + "=" * 70)
print(f"TOTAL CANDIDATES: {len(candidates)}")
print("=" * 70)

# For each candidate, fetch repo info to filter by activity & stars & AI policy
print("\nFetching repo info for top candidates...")
