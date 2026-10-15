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

def gh(url, delay=2):
    time.sleep(delay)
    req = urllib.request.Request(url, headers=GH_HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=15) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())
    except Exception as e:
        return -1, {"error": str(e)[:200]}

def gl(url, delay=10):
    time.sleep(delay)
    req = urllib.request.Request(url, headers=GL_HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:300]}
    except Exception as e:
        return -1, {"error": str(e)[:200]}

print("=" * 70)
print("GITHUB PRs — STATUS CHECK")
print("=" * 70)

GH_PRS = [
    ("meetdino/dino", 124),
    ("Ergane-Foundation/vajra", 37),
    ("Ishannaik/harbour", 57),
    ("NovaCode37/Prism-platform", 554),
    ("pacocartones/market-data-sanity-checker", 111),
    ("pacocartones/market-data-sanity-checker", 112),
]

for repo, num in GH_PRS:
    print(f"\n--- {repo} #{num} ---")
    code, d = gh(f"https://api.github.com/repos/{repo}/pulls/{num}")
    if code != 200:
        print(f"  HTTP {code}: {d.get('message','')[:150]}")
        continue
    state = d.get('state','?')
    merged = bool(d.get('merged_at'))
    if merged:
        print(f"  ✅ MERGED at {(d.get('merged_at') or '?')[:19]}")
    else:
        print(f"  state: {state}  mergeable: {d.get('mergeable','?')}  mergeable_state: {d.get('mergeable_state','?')}")
    print(f"  title: {(d.get('title') or '')[:90]}")
    sha = d.get('head',{}).get('sha','')
    if sha:
        # CI checks
        code2, d2 = gh(f"https://api.github.com/repos/{repo}/commits/{sha}/check-runs?per_page=20")
        if code2 == 200:
            runs = d2.get('check_runs',[])
            if runs:
                # Count by conclusion
                from collections import Counter
                c = Counter(r.get('conclusion') for r in runs)
                statuses = Counter(r.get('status') for r in runs)
                print(f"  CI ({len(runs)} runs): status={dict(statuses)} conclusions={dict(c)}")
    # Comments since last check (since 2026-10-13T18:50:00)
    code3, d3 = gh(f"https://api.github.com/repos/{repo}/issues/{num}/comments?per_page=20&sort=created&direction=desc")
    if code3 == 200 and d3:
        # Show comments since 2026-10-13T18:50:00
        recent = [c for c in d3 if (c.get('created_at') or '') > '2026-10-13T18:50:00']
        if recent:
            print(f"  New comments since last check ({len(recent)}):")
            for c in recent[-5:]:
                body = (c.get('body') or '').replace('\n',' ').replace('\r',' ')[:280]
                print(f"    - {c.get('user',{}).get('login','?')} ({(c.get('created_at') or '?')[:19]}): {body}")
        else:
            print(f"  No new comments since last check ({len(d3)} total)")

print("\n" + "=" * 70)
print("GITLAB MRs — STATUS CHECK")
print("=" * 70)

GL_MRS = [
    ("OpenMW/openmw", 7107382, "5667"),
    ("inkscape/extensions", 5833962, "739"),  # merged
    ("fdroid/fdroidclient", 36189, "1786"),
]
for name, pid, iid in GL_MRS:
    print(f"\n--- {name} !{iid} ---")
    code, d = gl(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}", delay=15)
    if code != 200:
        print(f"  HTTP {code}: {str(d)[:200]}")
        continue
    state = d.get('state','?')
    merged = bool(d.get('merged_at'))
    if merged:
        print(f"  ✅ MERGED at {(d.get('merged_at') or '?')[:19]}")
    else:
        print(f"  state: {state}  detailed_merge_status: {d.get('detailed_merge_status','?')}")
    print(f"  title: {(d.get('title') or '')[:80]}")
    sha = d.get('sha','')
    print(f"  sha: {sha[:10]}  updated: {(d.get('updated_at') or '?')[:19]}")
    # Pipelines
    code2, d2 = gl(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}/pipelines?per_page=2", delay=10)
    if code2 == 200:
        for p in d2[:2]:
            print(f"  pipeline {p.get('id','?')}: {p.get('status','?')} sha={(p.get('sha') or '')[:8]} {(p.get('created_at') or '?')[:19]}")
    # Last 2 notes
    code3, d3 = gl(f"https://api.gitlab.com/v4/projects/{pid}/merge_requests/{iid}/notes?per_page=20&sort=asc&order_by=created_at", delay=8) if False else gl(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}/notes?per_page=20&sort=asc&order_by=created_at", delay=10)
    if code3 == 200:
        non_sys = [n for n in d3 if not n.get('system')]
        # Show last 2 + any new since 2026-10-13T18:50:00
        recent = [n for n in non_sys if (n.get('created_at') or '') > '2026-10-13T18:50:00']
        if recent:
            print(f"  New notes since last check ({len(recent)}):")
            for n in recent[-3:]:
                body = (n.get('body') or '').replace('\n',' ').replace('\r',' ')[:280]
                print(f"    - {n.get('author',{}).get('username','?')} ({(n.get('created_at') or '?')[:19]}): {body}")
        else:
            print(f"  No new notes since last check ({len(non_sys)} total non-system)")
