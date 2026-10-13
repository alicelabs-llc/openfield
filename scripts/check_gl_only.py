import json, urllib.request, ssl, time

GL_TOKEN = "glpat-gupt0wt_EfWmH99u8NGm6WM6MQpvOjEKdTpranZqbQ8.01.1716a5win"
HEADERS = {
    "PRIVATE-TOKEN": GL_TOKEN,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
}
CTX = ssl.create_default_context()

def gl(url, delay=15):
    time.sleep(delay)
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]
    except Exception as e:
        return -1, str(e)[:200]

# Already know pid for OpenMW (7107382) and inkscape/ext (5833962)
# inkscape/inkscape pid unknown
MRS = [
    ("OpenMW/openmw", 7107382, "5667"),
    ("inkscape/extensions", 5833962, "739"),  # merged
    ("inkscape/inkscape", None, "8203"),
    ("fdroid/fdroidclient", 36189, "1786"),
]

for name, pid, iid in MRS:
    print(f"\n=== {name} !{iid} ===")
    if pid is None:
        s, b = gl(f"https://gitlab.com/api/v4/projects/{name.replace('/','%2F')}", delay=30)
        if s != 200:
            print(f"  project HTTP {s}: {b[:200]}")
            continue
        pid = json.loads(b).get('id')
        print(f"  project id: {pid}")
    s, b = gl(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}", delay=15)
    if s != 200:
        print(f"  MR HTTP {s}: {b[:200]}")
        continue
    d = json.loads(b)
    print(f"  state: {d.get('state')}  detailed_merge_status: {d.get('detailed_merge_status','?')}")
    if d.get('merged_at'):
        print(f"  merged_at: {d['merged_at'][:19]}")
    sha = d.get('sha','')
    print(f"  sha: {sha[:10]}  has_conflicts: {d.get('has_conflicts')}")
    # pipelines
    s2, b2 = gl(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}/pipelines?per_page=3", delay=20)
    if s2 == 200:
        for p in json.loads(b2)[:3]:
            print(f"  pipeline {p.get('id','?')}: status={p.get('status','?')} sha={(p.get('sha') or '')[:8]} created={(p.get('created_at') or '?')[:19]}")
    else:
        print(f"  pipelines HTTP {s2}: {b2[:200]}")
    # notes
    s3, b3 = gl(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}/notes?per_page=50&sort=asc&order_by=created_at", delay=20)
    if s3 == 200:
        notes = [n for n in json.loads(b3) if not n.get('system')]
        print(f"  notes: {len(notes)} non-system (last 4)")
        for n in notes[-4:]:
            body = (n.get('body') or '').replace('\n',' ').replace('\r',' ')[:200]
            print(f"    - {n.get('author',{}).get('username','?')} ({(n.get('created_at') or '?')[:19]}): {body}")
    else:
        print(f"  notes HTTP {s3}: {b3[:200]}")
