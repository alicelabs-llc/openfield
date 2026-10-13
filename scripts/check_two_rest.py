import json, urllib.request, ssl, time

TOKEN = "glpat-gupt0wt_EfWmH99u8NGm6WM6MQpvOjEKdTpranZqbQ8.01.1716a5win"
HEADERS = {
    "PRIVATE-TOKEN": TOKEN,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0 Safari/537.36",
    "Accept": "application/json",
}
CTX = ssl.create_default_context()

def get(url, delay=20):
    time.sleep(delay)
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]
    except Exception as e:
        return -1, str(e)[:200]

# Cached project IDs (from earlier successful lookups)
MRS = [
    ("OpenMW/openmw", "5667", None),  # don't know yet
    ("fdroid/fdroidclient", "1786", 36189),  # cached from previous run
]

for proj, iid, pid in MRS:
    print(f"\n=== {proj} !{iid} ===")
    if pid is None:
        s, b = get(f"https://gitlab.com/api/v4/projects/{proj.replace('/','%2F')}", delay=30)
        if s != 200:
            print(f"  project HTTP {s}: {b[:200]}")
            continue
        pid = json.loads(b).get("id")
        print(f"  project id: {pid}")
    s, b = get(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}", delay=20)
    if s != 200:
        print(f"  MR HTTP {s}: {b[:200]}")
        continue
    mr = json.loads(b)
    print(f"  State: {mr.get('state')}  Merge: {mr.get('detailed_merge_status','?')}")
    print(f"  Title: {(mr.get('title') or '')[:120]}")
    print(f"  URL:   {mr.get('web_url','?')}")
    sha = mr.get('sha')
    if sha:
        s2, b2 = get(f"https://gitlab.com/api/v4/projects/{pid}/repository/commits/{sha}", delay=10)
        if s2 == 200:
            c = json.loads(b2)
            print(f"  HEAD: {c.get('short_id','?')}  created_at: {c.get('created_at','?')[:19]}  msg: {c.get('title','?')[:120]}")
    s3, b3 = get(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}/notes?per_page=50&sort=asc&order_by=created_at", delay=15)
    if s3 == 200:
        notes = json.loads(b3)
        print(f"  Notes: {len(notes)} total")
        count = 0
        for n in reversed(notes):
            if n.get('system'): continue
            created = n.get('created_at','?')[:19]
            body = (n.get('body') or '').replace('\n',' ')[:280]
            print(f"  - {n.get('author',{}).get('username','?')} ({created}): {body}")
            count += 1
            if count >= 10: break
    else:
        print(f"  notes HTTP {s3}: {b3[:200]}")
    s4, b4 = get(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}/pipelines?per_page=3", delay=10)
    if s4 == 200:
        for p in json.loads(b4)[:2]:
            print(f"  pipeline {p.get('id','?')}: status={p.get('status','?')}  sha={(p.get('sha') or '')[:8]}  created: {(p.get('created_at') or '?')[:19]}")
