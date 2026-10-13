import json, urllib.request, ssl, time

TOKEN = "glpat-gupt0wt_EfWmH99u8NGm6WM6MQpvOjEKdTpranZqbQ8.01.1716a5win"
HEADERS = {
    "PRIVATE-TOKEN": TOKEN,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
}
CTX = ssl.create_default_context()

# 1) First test: is the token even valid?
print("=== TOKEN VALIDATION ===")
url = "https://gitlab.com/api/v4/user"
req = urllib.request.Request(url, headers=HEADERS, method="GET")
try:
    with urllib.request.urlopen(req, context=CTX, timeout=15) as resp:
        d = json.loads(resp.read().decode())
        print(f"  HTTP {resp.status} - token OK - user: {d.get('username','?')} id={d.get('id','?')}")
except urllib.error.HTTPError as e:
    print(f"  HTTP {e.code} - {e.read().decode()[:200]}")
except Exception as e:
    print(f"  ERROR: {e}")

# 2) Try public GraphQL without token, in case token is dead
print("\n=== PUBLIC CHECK (no token) ===")
MRS = [
    ("OpenMW/openmw", "5667"),
    ("inkscape/extensions", "739"),
    ("fdroid/fdroidclient", "1786"),
]
for proj, iid in MRS:
    print(f"\n--- !{iid} @ {proj} ---")
    query = """{
  project(fullPath: "%s") {
    mergeRequest(iid: "%s") {
      state
      title
      webUrl
      headPipeline { status }
      detailedMergeStatus
      discussions(first: 50) {
        nodes {
          notes(first: 30) {
            nodes { author { username } body createdAt system }
          }
        }
      }
    }
  }
}""" % (proj, iid)
    req = urllib.request.Request(
        "https://gitlab.com/api/graphql",
        data=json.dumps({"query": query}).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            d = json.loads(resp.read().decode())
        if not d.get("data") or not d["data"].get("project"):
            print("  (no data - project not found or private)")
            continue
        mr = d["data"]["project"]["mergeRequest"]
        if not mr:
            print("  (MR not found)")
            continue
        print(f"  State: {mr['state']}  Pipeline: {(mr.get('headPipeline') or {}).get('status','none')}  Merge: {mr.get('detailedMergeStatus','?')}")
        print(f"  Title: {mr.get('title','?')[:120]}")
        print(f"  URL:   {mr.get('webUrl','?')}")
        for disc in mr.get("discussions", {}).get("nodes", []):
            for note in disc.get("notes", {}).get("nodes", []):
                if note.get("system"):
                    continue
                created = note.get("createdAt", "?")[:19]
                body = (note.get("body") or "").replace("\n", " ")[:220]
                print(f"  - {note['author']['username']} ({created}): {body}")
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code} - {e.read().decode()[:200]}")
    except Exception as e:
        print(f"  ERROR: {e}")
    time.sleep(2)
