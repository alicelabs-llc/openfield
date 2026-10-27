import json, urllib.request, ssl, time

GH_TOKEN = "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"
GL_TOKEN = "glpat-VTdIPfmOYCLcAQHp0IdlyWM6MQpvOjEKdTpranZqbQ8.01.17073yv2r"
CB_TOKEN = "86f56136e9bdbe4a6fe60d0b8f2e4c277f407590"

GH_HEADERS = {"Authorization": f"token {GH_TOKEN}", "User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github+json"}
GL_HEADERS = {"PRIVATE-TOKEN": GL_TOKEN, "User-Agent": "Mozilla/5.0", "Accept": "application/json"}
CB_HEADERS = {"Authorization": f"token {CB_TOKEN}", "Content-Type": "application/json", "Accept": "application/json", "User-Agent": "Mozilla/5.0"}
CTX = ssl.create_default_context()

def fetch(url, headers, delay=2):
    time.sleep(delay)
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=15) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:200]}
    except Exception as e:
        return -1, {"error": str(e)[:200]}

# 1. GitHub PRs — search all
print("=" * 70)
print("GITHUB — ALL PRs (merged + open)")
print("=" * 70)
code, d = fetch("https://api.github.com/search/issues?q=author:eddyflores100-lang+type:pr&per_page=50&sort=updated&order=desc", GH_HEADERS, delay=2)
merged_count = 0
open_count = 0
closed_count = 0
if code == 200:
    items = d.get("items", [])
    print(f"Total PRs found: {len(items)}")
    for it in items[:30]:
        repo = it.get("repository_url", "").replace("https://api.github.com/repos/", "")
        num = it.get("number")
        state = it.get("state", "?").upper()
        title = it.get("title", "")[:60]
        # Get PR details for merged status
        time.sleep(0.5)
        _, pr = fetch(f"https://api.github.com/repos/{repo}/pulls/{num}", GH_HEADERS, delay=0.5)
        merged = bool(pr.get("merged_at")) if isinstance(pr, dict) else False
        if merged:
            merged_count += 1
            marker = "✅MERGED"
        elif state == "OPEN":
            open_count += 1
            marker = "🟡OPEN"
        else:
            closed_count += 1
            marker = "❌CLOSED"
        print(f"  {marker:10} {repo}#{num}: {title}")
    print(f"\nHacktoberfest: {merged_count} merged, {open_count} open, {closed_count} closed")

# 2. Codeberg PRs
print("\n" + "=" * 70)
print("CODEBERG — PRs")
print("=" * 70)
for repo, num in [("mfussenegger/nvim-lint", 20), ("gvasquez/glical", 9)]:
    code, d = fetch(f"https://codeberg.org/api/v1/repos/{repo}/pulls/{num}", CB_HEADERS, delay=3)
    if code == 200:
        merged = bool(d.get("merged_at"))
        marker = "✅MERGED" if merged else f"[{d.get('state','?').upper()}]"
        print(f"  {marker:10} {repo}!{num}: {d.get('title','')[:60]}")

# 3. GitLab MRs
print("\n" + "=" * 70)
print("GITLAB — MRs")
print("=" * 70)
for name, pid, iid in [("OpenMW/openmw", 7107382, "5667"), ("fdroid/fdroidclient", 36189, "1786"), ("inkscape/extensions", 5833962, "739")]:
    code, d = fetch(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}", GL_HEADERS, delay=5)
    if code == 200:
        merged = bool(d.get("merged_at"))
        marker = "✅MERGED" if merged else f"[{d.get('state','?').upper()}]"
        print(f"  {marker:10} {name}!{iid}: {d.get('title','')[:60]}")
    else:
        print(f"  HTTP {code} for {name}!{iid}")

# 4. Hacktoberfest sticker count via extension
print("\n" + "=" * 70)
print("HACKTOBERFEST DASHBOARD — via Agent Bridge extension")
print("=" * 70)
