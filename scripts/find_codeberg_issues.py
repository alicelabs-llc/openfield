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

print("=" * 60)
print("CODEBERG (Forgejo) — issues with hacktoberfest label")
print("=" * 60)

# Codeberg API: search issues by labels
# Try different search approaches
queries = [
    # Issues with label "hacktoberfest"
    "https://codeberg.org/api/v1/repos/issues/search?labels=hacktoberfest&state=open&type=issues&limit=30",
    # Issues with label "good first issue"
    "https://codeberg.org/api/v1/repos/issues/search?labels=good%20first%20issue&state=open&type=issues&limit=30",
    # Recent open issues (last week)
    "https://codeberg.org/api/v1/repos/issues/search?since=2026-10-01T00%3A00%3A00Z&state=open&type=issues&limit=20",
]

for q in queries:
    print(f"\n--- Query: {q[:80]}... ---")
    code, d = api(q, delay=3)
    if code != 200:
        print(f"  HTTP {code}: {str(d)[:300]}")
        continue
    items = d if isinstance(d, list) else d.get("data", [])
    print(f"  results: {len(items)}")
    for it in items[:10]:
        repo = it.get("repository", {})
        repo_full = repo.get("full_name", "?") if repo else "?"
        number = it.get("number")
        title = it.get("title", "")[:80]
        labels = [l.get("name", "") for l in it.get("labels", [])][:5]
        print(f"  - {repo_full}#{number}: {title}")
        print(f"    labels: {labels}")
