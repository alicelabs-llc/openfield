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

def gh(method, url, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=GH_HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())

def gl(method, url, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=GL_HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode()[:500])

# GitHub PRs
print("=" * 60)
print("GITHUB PRs")
print("=" * 60)

GH_PRS = [
    ("Ergane-Foundation/vajra", 37),
    ("Ishannaik/harbour", 57),
    ("NovaCode37/Prism-platform", 550),  # closed
    ("NovaCode37/Prism-platform", 446),  # issue we claimed
    ("meetdino/dino", 124),  # already merged
]
for repo, num in GH_PRS:
    time.sleep(2)
    # First try as PR
    code, d = gh("GET", f"https://api.github.com/repos/{repo}/pulls/{num}")
    if code == 200:
        kind = "PR"
    else:
        # try as issue
        code, d = gh("GET", f"https://api.github.com/repos/{repo}/issues/{num}")
        kind = "issue" if code == 200 else "?"
    print(f"\n--- {repo} #{num} ({kind}) ---")
    if code != 200:
        print(f"  HTTP {code}: {d.get('message','')[:150]}")
        continue
    if kind == "PR":
        print(f"  title: {(d.get('title') or '')[:90]}")
        print(f"  state: {d.get('state')}  draft: {d.get('draft',False)}  merged: {bool(d.get('merged_at'))}")
        if d.get('merged_at'):
            print(f"  merged_at: {d['merged_at'][:19]}")
        print(f"  mergeable: {d.get('mergeable','?')}  mergeable_state: {d.get('mergeable_state','?')}")
        sha = d.get('head',{}).get('sha','')
        if sha:
            print(f"  head sha: {sha[:8]}")
            # check runs
            code2, d2 = gh("GET", f"https://api.github.com/repos/{repo}/commits/{sha}/check-runs?per_page=10")
            if code2 == 200:
                runs = d2.get('check_runs',[])
                if runs:
                    print(f"  CI ({len(runs)}):")
                    for r in runs[:6]:
                        print(f"    - {r.get('name','?')[:45]}: {r.get('status','?')}/{r.get('conclusion','?')}")
        # comments
        code3, d3 = gh("GET", f"https://api.github.com/repos/{repo}/issues/{num}/comments?per_page=20&sort=created&direction=desc")
        if code3 == 200 and d3:
            print(f"  comments ({len(d3)}):")
            for c in d3[-5:]:
                body = (c.get('body') or '').replace('\n',' ').replace('\r',' ')[:180]
                print(f"    - {c.get('user',{}).get('login','?')} ({(c.get('created_at') or '?')[:19]}): {body}")
    else:
        # issue
        print(f"  title: {(d.get('title') or '')[:90]}")
        print(f"  state: {d.get('state')}  assignees: {[a.get('login','?') for a in d.get('assignees',[])]}")
        print(f"  comments: {d.get('comments',0)}")

# GitLab MRs
print("\n" + "=" * 60)
print("GITLAB MRs")
print("=" * 60)

GL_MRS = [
    ("OpenMW/openmw", 7107382, "5667"),
    ("inkscape/extensions", 5833962, "739"),  # merged
    ("inkscape/inkscape", None, "8203"),  # not checked recently
    ("fdroid/fdroidclient", 36189, "1786"),
]
for name, pid, iid in GL_MRS:
    print(f"\n--- {name} !{iid} ---")
    if pid is None:
        # need to lookup project id first
        time.sleep(15)
        code, d = gl("GET", f"https://gitlab.com/api/v4/projects/{name.replace('/','%2F')}")
        if code != 200:
            print(f"  project lookup HTTP {code}: {str(d)[:200]}")
            continue
        pid = d.get('id')
        print(f"  project id: {pid}")
    time.sleep(8)
    code, d = gl("GET", f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}")
    if code != 200:
        print(f"  MR HTTP {code}: {str(d)[:200]}")
        continue
    print(f"  title: {(d.get('title') or '')[:90]}")
    print(f"  state: {d.get('state')}  detailed_merge_status: {d.get('detailed_merge_status','?')}")
    if d.get('merged_at'):
        print(f"  merged_at: {d['merged_at'][:19]}")
    print(f"  sha: {(d.get('sha') or '')[:10]}  has_conflicts: {d.get('has_conflicts')}")
    # pipelines
    time.sleep(6)
    code2, d2 = gl("GET", f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}/pipelines?per_page=3")
    if code2 == 200:
        for p in d2[:3]:
            print(f"  pipeline {p.get('id','?')}: status={p.get('status','?')} sha={(p.get('sha') or '')[:8]} created={(p.get('created_at') or '?')[:19]}")
    # notes
    time.sleep(6)
    code3, d3 = gl("GET", f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}/notes?per_page=50&sort=asc&order_by=created_at")
    if code3 == 200:
        non_sys = [n for n in d3 if not n.get('system')]
        print(f"  notes: {len(non_sys)} non-system (last 3)")
        for n in non_sys[-3:]:
            body = (n.get('body') or '').replace('\n',' ').replace('\r',' ')[:200]
            print(f"    - {n.get('author',{}).get('username','?')} ({(n.get('created_at') or '?')[:19]}): {body}")
