import json, urllib.request, ssl, time

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
}
CTX = ssl.create_default_context()

# Try the public web UI endpoint directly (Cloudflare-friendly)
print("=== fdroid !1786 - retry GraphQL with longer delay ===")
time.sleep(15)
query = """{
  project(fullPath: "fdroid/fdroidclient") {
    mergeRequest(iid: "1786") {
      state
      title
      webUrl
      detailedMergeStatus
      headPipeline { status }
      discussions(first: 50) {
        nodes {
          notes(first: 50) {
            nodes { author { username } body createdAt system }
          }
        }
      }
    }
  }
}"""
req = urllib.request.Request(
    "https://gitlab.com/api/graphql",
    data=json.dumps({"query": query}).encode(),
    headers=HEADERS,
    method="POST",
)
try:
    with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
        d = json.loads(resp.read().decode())
    mr = d["data"]["project"]["mergeRequest"]
    print(f"  State: {mr['state']}  Merge: {mr.get('detailedMergeStatus','?')}  Pipeline: {(mr.get('headPipeline') or {}).get('status','none')}")
    print(f"  Title: {mr.get('title','?')[:140]}")
    print(f"  URL:   {mr.get('webUrl','?')}")
    for disc in mr.get("discussions", {}).get("nodes", []):
        for note in disc.get("notes", {}).get("nodes", []):
            if note.get("system"): continue
            created = note.get("createdAt","?")[:19]
            body = (note.get("body") or "").replace("\n"," ")[:240]
            print(f"  - {note['author']['username']} ({created}): {body}")
except urllib.error.HTTPError as e:
    print(f"  HTTP {e.code}: {e.read().decode()[:200]}")
except Exception as e:
    print(f"  ERROR: {e}")
