import json, urllib.request, ssl, time

GH_TOKEN = "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"
GL_TOKEN = "glpat-gupt0wt_EfWmH99u8NGm6WM6MQpvOjEKdTpranZqbQ8.01.1716a5win"

GH_HEADERS = {
    "Authorization": f"token {GH_TOKEN}",
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/vnd.github+json",
}
GL_HEADERS = {
    "PRIVATE-TOKEN": GL_TOKEN,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
}
CTX = ssl.create_default_context()

def gh(method, url):
    req = urllib.request.Request(url, headers=GH_HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=15) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())
    except Exception as e:
        return -1, {"error": str(e)[:200]}

def gl(url, delay=8):
    time.sleep(delay)
    req = urllib.request.Request(url, headers=GL_HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:200]}
    except Exception as e:
        return -1, {"error": str(e)[:200]}

# 1) GitHub account health
print("=" * 60)
print("GITHUB ACCOUNT HEALTH")
print("=" * 60)
code, d = gh("GET", "https://api.github.com/user")
print(f"  User: {d.get('login','?')} (id={d.get('id','?')})")
print(f"  Name: {d.get('name','?')}")
print(f"  Public repos: {d.get('public_repos','?')}")
print(f"  Followers: {d.get('followers','?')}  Following: {d.get('following','?')}")
print(f"  Created: {d.get('created_at','?')[:10]}")
print(f"  Suspended flag: {d.get('suspended', False)}")
# Rate limit
code, d = gh("GET", "https://api.github.com/rate_limit")
if code == 200:
    core = d.get("resources", {}).get("core", {})
    print(f"  Rate limit: {core.get('remaining','?')}/{core.get('limit','?')} (resets in {(core.get('reset','0')-int(time.time()))//60 if core.get('reset') else '?'} min)")

# All PRs by eddyflores100-lang (all states)
print("\n=== All PRs created by eddyflores100-lang ===")
all_prs = []
for repo in ["meetdino/dino", "Ergane-Foundation/vajra", "Ishannaik/harbour", "NovaCode37/Prism-platform"]:
    # search PRs by author
    q = f"author:eddyflores100-lang+repo:{repo}+is:pr"
    code, d = gh("GET", f"https://api.github.com/search/issues?q={q}&per_page=20")
    if code == 200:
        for it in d.get("items", []):
            state = it.get("state", "?")
            # Check if it's a PR and its merged state
            pr_url = it.get("pull_request", {}).get("url", "")
            merged = None
            if pr_url:
                time.sleep(1)
                code2, d2 = gh("GET", pr_url)
                if code2 == 200:
                    merged = bool(d2.get("merged_at"))
            print(f"  - [{state.upper()}{'/MERGED' if merged else ''}] {repo}#{it.get('number')}: {it.get('title','')[:80]}")
            print(f"    URL: {it.get('html_url','?')}")
            print(f"    Created: {(it.get('created_at') or '?')[:19]}  Updated: {(it.get('updated_at') or '?')[:19]}")
            print(f"    Comments: {it.get('comments',0)}  Labels: {[l.get('name') for l in it.get('labels',[])]}")
            all_prs.append({
                "repo": repo,
                "number": it.get("number"),
                "state": state,
                "merged": merged,
                "title": it.get("title",""),
                "html_url": it.get("html_url",""),
            })
            time.sleep(2)

# 2) GitLab account health
print("\n" + "=" * 60)
print("GITLAB ACCOUNT HEALTH")
print("=" * 60)
code, d = gl("https://gitlab.com/api/v4/user", delay=5)
if code == 200:
    print(f"  User: {d.get('username','?')} (id={d.get('id','?')})")
    print(f"  Name: {d.get('name','?')}")
    print(f"  Email: {d.get('email','?')}")
    print(f"  State: {d.get('state','?')}  Confirmed: {d.get('confirmed_at','?')[:19] if d.get('confirmed_at') else 'no'}")
    print(f"  Created: {d.get('created_at','?')[:10]}")
    print(f"  Last activity: {d.get('last_activity_on','?')}")
    print(f"  Bot: {d.get('bot',False)}  External: {d.get('external',False)}")
else:
    print(f"  ERR HTTP {code}: {d}")

# GitLab MRs
print("\n=== All MRs created by eddyflores100 across GitLab ===")
# Search MRs authored by user
GL_MRS = [
    ("OpenMW/openmw", 7107382, "5667"),
    ("inkscape/extensions", 5833962, "739"),
    ("inkscape/extensions", 5833962, "738"),  # closed
    ("inkscape/inkscape", 3472737, "8203"),  # closed
    ("fdroid/fdroidclient", 36189, "1786"),
]
for name, pid, iid in GL_MRS:
    print(f"\n  --- {name} !{iid} ---")
    code, d = gl(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}", delay=12)
    if code != 200:
        print(f"    HTTP {code}: {str(d)[:200]}")
        continue
    state = d.get('state','?')
    merged = bool(d.get('merged_at'))
    print(f"    State: {state}{' (MERGED)' if merged else ''}")
    print(f"    Title: {(d.get('title') or '')[:80]}")
    print(f"    Created: {(d.get('created_at') or '?')[:19]}")
    print(f"    Updated: {(d.get('updated_at') or '?')[:19]}")
    if merged:
        print(f"    Merged at: {(d.get('merged_at') or '?')[:19]}")
    print(f"    URL: {d.get('web_url','?')}")

# 3) Summary
print("\n" + "=" * 60)
print("HACKTOBERFEST SCORECARD")
print("=" * 60)
# Count merged PRs (this is what Hacktoberfest counts)
# Hacktoberfest rules (2026): 4 PRs/MRs merged during October, on any public repo
gh_merged = sum(1 for p in all_prs if p["merged"])
print(f"GitHub PRs:")
print(f"  Total created: {len(all_prs)}")
print(f"  Merged:        {gh_merged}")
for p in all_prs:
    status = "MERGED" if p["merged"] else p["state"].upper()
    print(f"    - [{status}] {p['repo']}#{p['number']}: {p['title'][:60]}")
