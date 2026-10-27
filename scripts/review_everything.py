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
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:200]}
    except Exception as e:
        return -1, {"error": str(e)[:200]}

# ============================================================
# GITHUB — ALL PRs by eddyflores100-lang
# ============================================================
print("=" * 70)
print("GITHUB — ALL PRs (merged + open + closed)")
print("=" * 70)

code, d = fetch("https://api.github.com/search/issues?q=author:eddyflores100-lang+type:pr&per_page=100&sort=updated&order=desc", GH_HEADERS, delay=2)
merged = 0
open_prs = 0
closed_not_merged = 0
if code == 200:
    items = d.get("items", [])
    print(f"Total PRs: {len(items)}\n")
    print("MERGED:")
    for it in items:
        repo = it.get("repository_url","").replace("https://api.github.com/repos/","")
        num = it.get("number")
        time.sleep(0.5)
        _, pr = fetch(f"https://api.github.com/repos/{repo}/pulls/{num}", GH_HEADERS, delay=0.5)
        is_merged = bool(pr.get("merged_at")) if isinstance(pr, dict) else False
        if is_merged:
            merged += 1
            title = it.get("title","")[:60]
            merged_date = (pr.get("merged_at","?") or "?")[:10]
            print(f"  ✅ {repo}#{num} ({merged_date}): {title}")
    print(f"\nOPEN ({open_prs}):")
    for it in items:
        repo = it.get("repository_url","").replace("https://api.github.com/repos/","")
        num = it.get("number")
        state = it.get("state","?")
        if state.upper() != "OPEN":
            continue
        open_prs += 1
        title = it.get("title","")[:60]
        updated = (it.get("updated_at","?"))[:10]
        comments = it.get("comments",0)
        # Get PR details
        time.sleep(0.5)
        _, pr = fetch(f"https://api.github.com/repos/{repo}/pulls/{num}", GH_HEADERS, delay=0.5)
        mergeable = pr.get("mergeable","?") if isinstance(pr, dict) else "?"
        ms = pr.get("mergeable_state","?") if isinstance(pr, dict) else "?"
        print(f"  🟡 {repo}#{num} ({comments}c, {updated}): {title} [mergeable={mergeable}/{ms}]")
    print(f"\nCLOSED (not merged):")
    for it in items:
        repo = it.get("repository_url","").replace("https://api.github.com/repos/","")
        num = it.get("number")
        state = it.get("state","?")
        if state.upper() != "CLOSED":
            continue
        time.sleep(0.5)
        _, pr = fetch(f"https://api.github.com/repos/{repo}/pulls/{num}", GH_HEADERS, delay=0.5)
        is_merged = bool(pr.get("merged_at")) if isinstance(pr, dict) else False
        if not is_merged:
            closed_not_merged += 1
            title = it.get("title","")[:60]
            print(f"  ❌ {repo}#{num}: {title}")
    
    print(f"\n--- GITHUB SUMMARY ---")
    print(f"  Merged: {merged}")
    print(f"  Open: {open_prs}")
    print(f"  Closed (not merged): {closed_not_merged}")
    print(f"  Total: {merged + open_prs + closed_not_merged}")

# ============================================================
# Check for new comments on OPEN PRs
# ============================================================
print("\n" + "=" * 70)
print("NEW COMMENTS ON OPEN PRs (from maintainers)")
print("=" * 70)

code, d = fetch("https://api.github.com/search/issues?q=author:eddyflores100-lang+type:pr+state:open&per_page=30&sort=updated&order=desc", GH_HEADERS, delay=2)
if code == 200:
    for it in d.get("items", []):
        repo = it.get("repository_url","").replace("https://api.github.com/repos/","")
        num = it.get("number")
        # Get comments
        _, comments = fetch(f"https://api.github.com/repos/{repo}/issues/{num}/comments?per_page=5&sort=desc", GH_HEADERS, delay=1)
        if isinstance(comments, list):
            for c in comments[-3:]:
                author = c.get("user",{}).get("login","?")
                if author == "eddyflores100-lang":
                    continue
                if "github-actions" in author or "coderabbit" in author:
                    continue
                created = (c.get("created_at","?"))[:19]
                body = (c.get("body","") or "").replace("\n"," ")[:200]
                print(f"  💬 {repo}#{num} — {author} ({created}): {body}")
                print()

# ============================================================
# GITLAB — MRs
# ============================================================
print("=" * 70)
print("GITLAB — MRs")
print("=" * 70)

for name, pid, iid in [("OpenMW/openmw", 7107382, "5667"), ("fdroid/fdroidclient", 36189, "1786")]:
    code, d = fetch(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}", GL_HEADERS, delay=10)
    if code != 200:
        print(f"  {name}!{iid}: HTTP {code}")
        continue
    state = d.get("state","?")
    is_merged = bool(d.get("merged_at"))
    if is_merged:
        print(f"  ✅ {name}!{iid}: MERGED")
    else:
        print(f"  🟡 {name}!{iid}: {state} (merge_status: {d.get('detailed_merge_status','?')})")
    # Get latest comments
    code2, d2 = fetch(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}/notes?per_page=50&sort=asc&order_by=created_at", GL_HEADERS, delay=8)
    if code2 == 200:
        non_sys = [n for n in d2 if not n.get("system")]
        if non_sys:
            last = non_sys[-1]
            author = last.get("author",{}).get("username","?")
            created = (last.get("created_at","?"))[:19]
            body = (last.get("body","") or "").replace("\n"," ")[:200]
            marker = "💬" if author != "eddyflores100" else "  "
            print(f"    {marker} last comment: {author} ({created}): {body}")

# ============================================================
# CODEBERG — PRs
# ============================================================
print("\n" + "=" * 70)
print("CODEBERG — PRs")
print("=" * 70)

for repo, num in [("mfussenegger/nvim-lint", 20), ("wafrn/wafrn", 864)]:
    code, d = fetch(f"https://codeberg.org/api/v1/repos/{repo}/pulls/{num}", CB_HEADERS, delay=3)
    if code != 200:
        print(f"  {repo}!{num}: HTTP {code}")
        continue
    state = d.get("state","?")
    is_merged = bool(d.get("merged_at"))
    mergeable = d.get("mergeable","?")
    if is_merged:
        print(f"  ✅ {repo}!{num}: MERGED")
    else:
        print(f"  🟡 {repo}!{num}: {state} (mergeable={mergeable})")
    # Get comments
    code2, d2 = fetch(f"https://codeberg.org/api/v1/repos/{repo}/issues/{num}/comments?per_page=10", CB_HEADERS, delay=3)
    if code2 == 200:
        comments = d2 if isinstance(d2, list) else d2.get("data", [])
        if comments:
            last = comments[-1]
            author = last.get("user",{}).get("login","?")
            created = (last.get("created_at","?"))[:19]
            body = (last.get("body","") or "").replace("\n"," ")[:200]
            marker = "💬" if author != "eddyflores100" else "  "
            print(f"    {marker} last comment: {author} ({created}): {body}")
        else:
            print(f"    No comments yet")

