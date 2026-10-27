import json, urllib.request, ssl, time

GL_TOKEN = "glpat-VTdIPfmOYCLcAQHp0IdlyWM6MQpvOjEKdTpranZqbQ8.01.17073yv2r"
CB_TOKEN = "86f56136e9bdbe4a6fe60d0b8f2e4c277f407590"

GL_HEADERS = {"PRIVATE-TOKEN": GL_TOKEN, "User-Agent": "Mozilla/5.0", "Accept": "application/json"}
CB_HEADERS = {"Authorization": f"token {CB_TOKEN}", "Content-Type": "application/json", "Accept": "application/json", "User-Agent": "Mozilla/5.0"}
CTX = ssl.create_default_context()

def fetch(url, headers, delay=3):
    time.sleep(delay)
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:300]}
    except Exception as e:
        return -1, {"error": str(e)[:200]}

# ============================================================
# GITLAB MRs
# ============================================================
print("=" * 70)
print("GITLAB — ALL MRs")
print("=" * 70)

GL_MRS = [
    ("OpenMW/openmw", 7107382, "5667"),
    ("fdroid/fdroidclient", 36189, "1786"),
    ("inkscape/extensions", 5833962, "739"),
    ("inkscape/inkscape", 3472737, "8203"),
]

for name, pid, iid in GL_MRS:
    print(f"\n{'='*60}")
    print(f"  {name} !{iid}")
    print(f"{'='*60}")
    
    # MR details
    code, d = fetch(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}", GL_HEADERS, delay=5)
    if code != 200:
        print(f"  HTTP {code}: {str(d)[:200]}")
        continue
    state = d.get("state","?")
    merged = bool(d.get("merged_at"))
    print(f"  state: {state}  merged: {merged}")
    print(f"  title: {d.get('title','')[:80]}")
    print(f"  updated: {(d.get('updated_at') or '?')[:19]}")
    sha = d.get("sha","")
    print(f"  sha: {sha[:10]}")
    
    # Pipelines
    code2, d2 = fetch(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}/pipelines?per_page=3", GL_HEADERS, delay=4)
    if code2 == 200:
        for p in d2[:3]:
            print(f"  pipeline {p.get('id','?')}: {p.get('status','?')} sha={(p.get('sha') or '')[:8]} created={(p.get('created_at') or '?')[:19]}")
    
    # Notes (comments)
    code3, d3 = fetch(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}/notes?per_page=50&sort=asc&order_by=created_at", GL_HEADERS, delay=5)
    if code3 == 200:
        non_sys = [n for n in d3 if not n.get("system")]
        print(f"\n  Comments ({len(non_sys)} non-system):")
        for n in non_sys:
            author = n.get("author",{}).get("username","?")
            created = (n.get("created_at") or "?")[:19]
            body = (n.get("body") or "").replace("\n"," ").replace("\r"," ")[:300]
            # Highlight if it's from maintainer (not eddyflores100)
            marker = "💬" if author != "eddyflores100" else "  "
            print(f"  {marker} {author} ({created}): {body}")

# ============================================================
# CODEBERG PRs
# ============================================================
print("\n" + "=" * 70)
print("CODEBERG — ALL PRs")
print("=" * 70)

CB_PRS = [
    ("mfussenegger/nvim-lint", 20),
    ("gvasquez/glical", 9),
]

for repo, num in CB_PRS:
    print(f"\n{'='*60}")
    print(f"  {repo} !{num}")
    print(f"{'='*60}")
    
    # PR details
    code, d = fetch(f"https://codeberg.org/api/v1/repos/{repo}/pulls/{num}", CB_HEADERS, delay=4)
    if code != 200:
        print(f"  HTTP {code}: {str(d)[:200]}")
        continue
    state = d.get("state","?")
    merged = bool(d.get("merged_at"))
    print(f"  state: {state}  merged: {merged}")
    print(f"  title: {d.get('title','')[:80]}")
    print(f"  updated: {(d.get('updated_at') or '?')[:19]}")
    print(f"  mergeable: {d.get('mergeable','?')}")
    
    # Comments
    code2, d2 = fetch(f"https://codeberg.org/api/v1/repos/{repo}/issues/{num}/comments?per_page=30", CB_HEADERS, delay=4)
    if code2 == 200:
        comments = d2 if isinstance(d2, list) else d2.get("data", [])
        print(f"\n  Comments ({len(comments)}):")
        for c in comments:
            author = c.get("user",{}).get("login","?")
            created = (c.get("created_at") or "?")[:19]
            body = (c.get("body") or "").replace("\n"," ").replace("\r"," ")[:300]
            marker = "💬" if author != "eddyflores100" else "  "
            print(f"  {marker} {author} ({created}): {body}")
    
    # Also check review comments
    code3, d3 = fetch(f"https://codeberg.org/api/v1/repos/{repo}/pulls/{num}/comments?per_page=30", CB_HEADERS, delay=4)
    if code3 == 200:
        reviews = d3 if isinstance(d3, list) else d3.get("data", [])
        if reviews:
            print(f"\n  Review comments ({len(reviews)}):")
            for c in reviews:
                author = c.get("user",{}).get("login","?")
                created = (c.get("created_at") or "?")[:19]
                body = (c.get("body") or "").replace("\n"," ").replace("\r"," ")[:300]
                marker = "💬" if author != "eddyflores100" else "  "
                print(f"  {marker} {author} ({created}): {body}")
