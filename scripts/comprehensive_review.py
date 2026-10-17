import json, urllib.request, ssl, time

GH_TOKEN = "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"
GL_TOKEN = "glpat-gupt0wt_EfWmH99u8NGm6WM6MQpvOjEKdTpranZqbQ8.01.1716a5win"
CB_TOKEN = "86f56136e9bdbe4a6fe60d0b8f2e4c277f407590"

GH_HEADERS = {"Authorization": f"token {GH_TOKEN}", "User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github+json"}
CB_HEADERS = {"Authorization": f"token {CB_TOKEN}", "Content-Type": "application/json", "Accept": "application/json", "User-Agent": "Mozilla/5.0"}
CTX = ssl.create_default_context()

def gh(url, delay=2):
    time.sleep(delay)
    req = urllib.request.Request(url, headers=GH_HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=15) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:200]}

def cb(url, delay=2):
    time.sleep(delay)
    req = urllib.request.Request(url, headers=CB_HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:200]}

print("=" * 70)
print("GITHUB — All PRs by eddyflores100-lang (any state)")
print("=" * 70)

# Search ALL PRs by user (any state)
code, d = gh("https://api.github.com/search/issues?q=author:eddyflores100-lang+type:pr&per_page=30&sort=updated&order=desc", delay=2)
if code == 200:
    items = d.get("items", [])
    print(f"Total PRs: {len(items)}")
    merged_count = 0
    for it in items[:20]:
        repo = it.get("repository_url", "").replace("https://api.github.com/repos/", "")
        num = it.get("number")
        state = it.get("state", "?").upper()
        # Fetch PR details for merged status
        time.sleep(1)
        _, pr = gh(f"https://api.github.com/repos/{repo}/pulls/{num}", delay=1)
        merged = bool(pr.get("merged_at")) if isinstance(pr, dict) else False
        if merged:
            merged_count += 1
            marker = "✅MERGED"
        else:
            marker = f"[{state}]"
        print(f"  - {marker:12} {repo}#{num}: {it.get('title','')[:60]}")
    print(f"\nHacktoberfest score: {merged_count} PRs merged (target 4)")

print("\n" + "=" * 70)
print("CODEBERG — All PRs by eddyflores100")
print("=" * 70)

# Check our 2 Codeberg PRs
CB_PRS = [
    ("mfussenegger/nvim-lint", 20),
    ("gvasquez/glical", 9),
]
for repo, num in CB_PRS:
    code, d = cb(f"https://codeberg.org/api/v1/repos/{repo}/pulls/{num}", delay=3)
    if code == 200:
        state = d.get("state", "?")
        merged = bool(d.get("merged_at"))
        marker = "✅MERGED" if merged else f"[{state.upper()}]"
        print(f"  - {marker:12} {repo}!{num}: {d.get('title','')[:60]}")
    else:
        print(f"  - HTTP {code} for {repo}!{num}")

print("\n" + "=" * 70)
print("GITLAB — MRs status (token may be revoked)")
print("=" * 70)
GL_MRS = [
    ("OpenMW/openmw", 7107382, "5667"),
    ("fdroid/fdroidclient", 36189, "1786"),
]
for name, pid, iid in GL_MRS:
    headers = {"PRIVATE-TOKEN": GL_TOKEN, "User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    time.sleep(3)
    req = urllib.request.Request(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}", headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            d = json.loads(resp.read().decode())
        merged = bool(d.get("merged_at"))
        marker = "✅MERGED" if merged else f"[{d.get('state','?').upper()}]"
        print(f"  - {marker:12} {name}!{iid}: {d.get('title','')[:60]}")
    except urllib.error.HTTPError as e:
        msg = e.read().decode()[:100]
        if "revoked" in msg.lower():
            print(f"  - ⚠️  TOKEN REVOKED — cannot check {name}!{iid}")
        else:
            print(f"  - HTTP {e.code} for {name}!{iid}: {msg}")
    except Exception as e:
        print(f"  - ERR for {name}!{iid}: {e}")
