import json, urllib.request, ssl, time

TOKEN = "glpat-gupt0wt_EfWmH99u8NGm6WM6MQpvOjEKdTpranZqbQ8.01.1716a5win"
HEADERS = {
    "PRIVATE-TOKEN": TOKEN,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
}
CTX = ssl.create_default_context()

def get(url, delay=3):
    time.sleep(delay)
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()

print("=== fdroid/fdroidclient !1786 (REST API) ===")
# Project ID for fdroid/fdroidclient
status, body = get("https://gitlab.com/api/v4/projects/fdroid%2Ffdroidclient")
if status != 200:
    print(f"  project lookup HTTP {status}: {body[:200]}")
else:
    pid = json.loads(body).get("id")
    print(f"  project id: {pid}")
    # MR info
    status, body = get(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/1786")
    if status == 200:
        mr = json.loads(body)
        print(f"  State: {mr.get('state')}  Merge: {mr.get('detailed_merge_status','?')}  Draft: {mr.get('work_in_progress',False)}")
        print(f"  Title: {mr.get('title','?')[:120]}")
        print(f"  URL:   {mr.get('web_url','?')}")
        # Pipeline
        sha = mr.get('sha')
        if sha:
            s2, b2 = get(f"https://gitlab.com/api/v4/projects/{pid}/pipelines/{sha}")
            if s2 == 200:
                p = json.loads(b2)
                print(f"  Pipeline: {p.get('status','?')} (id={p.get('id')}, ref={p.get('ref')})")
            else:
                print(f"  Pipeline lookup HTTP {s2}: {b2[:120]}")
        # Notes / discussions
        s3, b3 = get(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/1786/notes?per_page=50&sort=asc&order_by=created_at")
        if s3 == 200:
            notes = json.loads(b3)
            print(f"\n  Notes ({len(notes)} total):")
            for n in notes[-15:]:  # last 15
                if n.get('system'): continue
                created = n.get('created_at','?')[:19]
                body_txt = (n.get('body') or '').replace('\n',' ')[:220]
                print(f"  - {n.get('author',{}).get('username','?')} ({created}): {body_txt}")
        else:
            print(f"  notes HTTP {s3}: {b3[:200]}")
    else:
        print(f"  MR HTTP {status}: {body[:200]}")
