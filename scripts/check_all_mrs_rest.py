import json, urllib.request, ssl, time

TOKEN = "glpat-gupt0wt_EfWmH99u8NGm6WM6MQpvOjEKdTpranZqbQ8.01.1716a5win"
HEADERS = {
    "PRIVATE-TOKEN": TOKEN,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0 Safari/537.36",
    "Accept": "application/json",
}
CTX = ssl.create_default_context()

def get(url, delay=8):
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
    ("OpenMW/openmw", "5667"),
    ("inkscape/extensions", "739"),
    ("fdroid/fdroidclient", "1786"),
]

for proj, iid in MRS:
    print(f"\n=== {proj} !{iid} ===")
    pid_enc = proj.replace("/", "%2F")
    # 1) project lookup
    s, b = get(f"https://gitlab.com/api/v4/projects/{pid_enc}")
    if s != 200:
        print(f"  project HTTP {s}: {b[:200]}")
        continue
    pid = json.loads(b).get("id")
    print(f"  project id: {pid}")
    # 2) MR info
    s, b = get(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}")
    if s != 200:
        print(f"  MR HTTP {s}: {b[:200]}")
        continue
    mr = json.loads(b)
    print(f"  State: {mr.get('state')}  Merge: {mr.get('detailed_merge_status','?')}  Draft: {mr.get('work_in_progress',False)}")
    print(f"  Title: {(mr.get('title') or '')[:120]}")
    print(f"  URL:   {mr.get('web_url','?')}")
    sha = mr.get('sha')
    if sha:
        s2, b2 = get(f"https://gitlab.com/api/v4/projects/{pid}/repository/commits/{sha}")
        if s2 == 200:
            c = json.loads(b2)
            print(f"  HEAD: {c.get('short_id','?')}  created_at: {c.get('created_at','?')[:19]}  msg: {c.get('title','?')[:120]}")
    # 3) Notes / discussions
    s3, b3 = get(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}/notes?per_page=50&sort=asc&order_by=created_at")
    if s3 == 200:
        notes = json.loads(b3)
        print(f"  Notes: {len(notes)} total (mostrando últimos 8 no-system)")
        count = 0
        for n in reversed(notes):
            if n.get('system'): continue
            created = n.get('created_at','?')[:19]
            body = (n.get('body') or '').replace('\n',' ')[:240]
            print(f"  - {n.get('author',{}).get('username','?')} ({created}): {body}")
            count += 1
            if count >= 8: break
    else:
        print(f"  notes HTTP {s3}: {b3[:200]}")
    # 4) Pipeline
    s4, b4 = get(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}/pipelines?per_page=3")
    if s4 == 200:
        pipes = json.loads(b4)
        for p in pipes[:2]:
            print(f"  pipeline {p.get('id','?')}: status={p.get('status','?')}  ref={p.get('ref','?')}  sha={(p.get('sha') or '')[:8]}  created: {(p.get('created_at') or '?')[:19]}")
    else:
        print(f"  pipelines HTTP {s4}: {b4[:200]}")
