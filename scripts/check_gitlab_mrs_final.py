import json, urllib.request, ssl, time

TOKEN = "glpat-gupt0wt_EfWmH99u8NGm6WM6MQpvOjEKdTpranZqbQ8.01.1716a5win"
HEADERS = {
    "PRIVATE-TOKEN": TOKEN,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0 Safari/537.36",
    "Accept": "application/json",
}
CTX = ssl.create_default_context()

def get(url, delay=10):
    time.sleep(delay)
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]
    except Exception as e:
        return -1, str(e)[:200]

MRS = [
    ("OpenMW/openmw", 7107382, "5667"),
    ("inkscape/extensions", 5833962, "739"),
    ("fdroid/fdroidclient", 36189, "1786"),
]

for name, pid, iid in MRS:
    print(f"\n=== {name} !{iid} ===")
    s, b = get(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}", delay=20)
    if s != 200:
        print(f"  MR HTTP {s}: {b[:200]}")
        continue
    mr = json.loads(b)
    print(f"  state: {mr.get('state')}  detailed_merge_status: {mr.get('detailed_merge_status','?')}  has_conflicts: {mr.get('has_conflicts')}")
    sha = mr.get('sha','')
    print(f"  sha: {sha[:10]}")
    # pipelines
    s2, b2 = get(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}/pipelines?per_page=3", delay=15)
    if s2 == 200:
        for p in json.loads(b2)[:3]:
            print(f"  pipeline {p.get('id','?')}: status={p.get('status','?')} sha={(p.get('sha') or '')[:8]} created={(p.get('created_at') or '?')[:19]}")
    # notes
    s3, b3 = get(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}/notes?per_page=50&sort=asc&order_by=created_at", delay=15)
    if s3 == 200:
        notes = json.loads(b3)
        # show only last 5 non-system
        non_sys = [n for n in notes if not n.get('system')]
        print(f"  notes: {len(non_sys)} non-system (showing last 4)")
        for n in non_sys[-4:]:
            body = (n.get('body') or '').replace('\n',' ')[:240]
            print(f"  - {n.get('author',{}).get('username','?')} ({n.get('created_at','?')[:19]}): {body}")
