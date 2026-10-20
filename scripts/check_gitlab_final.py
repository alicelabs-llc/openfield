import json, urllib.request, ssl, time

TOKEN = "glpat-VTdIPfmOYCLcAQHp0IdlyWM6MQpvOjEKdTpranZqbQ8.01.17073yv2r"
HEADERS = {"PRIVATE-TOKEN": TOKEN, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0", "Accept": "application/json"}
CTX = ssl.create_default_context()

def gl(url, delay=10):
    time.sleep(delay)
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:300]}

MRS = [
    ("OpenMW/openmw", 7107382, "5667"),
    ("inkscape/extensions", 5833962, "739"),  # already known merged
    ("inkscape/inkscape", 3472737, "8203"),  # closed
    ("fdroid/fdroidclient", 36189, "1786"),
]
for name, pid, iid in MRS:
    print(f"\n=== {name} !{iid} ===")
    s, d = gl(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}", delay=8)
    if s != 200:
        print(f"  HTTP {s}: {str(d)[:200]}")
        continue
    state = d.get("state","?")
    merged = bool(d.get("merged_at"))
    if merged:
        print(f"  ✅ MERGED at {(d.get('merged_at') or '?')[:19]}")
    else:
        print(f"  state: {state}  detailed_merge_status: {d.get('detailed_merge_status','?')}  has_conflicts: {d.get('has_conflicts')}")
    print(f"  title: {(d.get('title') or '')[:80]}")
    sha = d.get("sha","")
    print(f"  sha: {sha[:10]}  updated: {(d.get('updated_at') or '?')[:19]}")
    # pipelines
    s2, d2 = gl(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}/pipelines?per_page=3", delay=6)
    if s2 == 200:
        for p in d2[:3]:
            print(f"  pipeline {p.get('id','?')}: {p.get('status','?')} sha={(p.get('sha') or '')[:8]} created={(p.get('created_at') or '?')[:19]}")
    # notes
    s3, d3 = gl(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}/notes?per_page=30&sort=asc&order_by=created_at", delay=8)
    if s3 == 200:
        non_sys = [n for n in d3 if not n.get("system")]
        # Show last 3 + any new since 2026-10-13
        recent = [n for n in non_sys if (n.get("created_at") or "") > "2026-10-13T18:50:00"]
        if recent:
            print(f"  *** NEW notes since last check ({len(recent)}):")
            for n in recent:
                body = (n.get("body") or "").replace("\n"," ").replace("\r"," ")[:280]
                print(f"    - {n.get('author',{}).get('username','?')} ({(n.get('created_at') or '?')[:19]}): {body}")
        else:
            print(f"  No new notes since last check ({len(non_sys)} total non-system)")
            for n in non_sys[-2:]:
                body = (n.get("body") or "").replace("\n"," ").replace("\r"," ")[:200]
                print(f"    last: {n.get('author',{}).get('username','?')} ({(n.get('created_at') or '?')[:19]}): {body}")
