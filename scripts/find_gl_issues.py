import json, urllib.request, ssl, time

GL_TOKEN = "glpat-PfWyLHoeZpLOyyQSzyDX72M6MQpvOjEKdTpranZqbQ8.01.1715hm5mn"
GL_HEADERS = {"PRIVATE-TOKEN": GL_TOKEN, "User-Agent": "Mozilla/5.0", "Accept": "application/json"}
CTX = ssl.create_default_context()

def fetch(url, delay=3):
    time.sleep(delay)
    req = urllib.request.Request(url, headers=GL_HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:300]}
    except Exception as e:
        return -1, {"error": str(e)[:200]}

# ============================================================
# GITLAB — Global issue search (now works with new token!)
# ============================================================
print("=" * 70)
print("GITLAB — Global issue search")
print("=" * 70)

search_terms = [
    "trust verification",
    "Ed25519",
    "signature verify",
    "cryptographic",
    "attestation",
    "provenance",
    "key rotation",
    "HMAC",
    "zero trust",
    "agent trust",
]

all_candidates = []
seen = set()

for term in search_terms:
    import urllib.parse
    encoded = urllib.parse.quote(term)
    code, d = fetch(f"https://gitlab.com/api/v4/issues?search={encoded}&state=opened&per_page=5&sort=desc&order_by=created_at", delay=5)
    if code != 200:
        print(f"  search '{term}': HTTP {code}")
        continue
    if not isinstance(d, list):
        continue
    for it in d[:3]:
        proj_id = it.get("project_id")
        key = f"{proj_id}#{it.get('iid')}"
        if key in seen:
            continue
        seen.add(key)
        title = it.get("title","")[:70]
        iid = it.get("iid")
        labels = it.get("labels",[])
        if it.get("assignees"):
            continue
        created = (it.get("created_at","?"))[:10]
        url = it.get("web_url","")
        # Get project name
        code2, d2 = fetch(f"https://gitlab.com/api/v4/projects/{proj_id}", delay=3)
        repo = d2.get("path_with_namespace","?") if isinstance(d2, dict) else "?"
        stars = d2.get("star_count",0) if isinstance(d2, dict) else 0
        all_candidates.append({
            "repo": repo,
            "iid": iid,
            "title": title,
            "labels": labels[:5],
            "created": created,
            "url": url,
            "stars": stars,
            "term": term,
        })

print(f"\nFound {len(all_candidates)} GitLab issues\n")
for i, c in enumerate(all_candidates[:15], 1):
    print(f"{i}. {c['repo']}!{c['iid']} (⭐{c['stars']}, {c['created']}) — search: '{c['term']}'")
    print(f"   title: {c['title']}")
    print(f"   labels: {c['labels']}")
    print(f"   url: {c['url']}")
    print()

# Get full body for top 3
print("\n" + "="*60)
print("TOP 3 — Full details")
print("="*60)
for c in all_candidates[:3]:
    print(f"\n{'='*50}")
    print(f"  {c['repo']}!{c['iid']}")
    print(f"{'='*50}")
    proj_id = None
    # Find proj_id from URL
    code, d = fetch(f"https://gitlab.com/api/v4/projects/{c['repo'].replace('/','%2F')}", delay=5)
    if code == 200:
        proj_id = d.get("id")
    if proj_id:
        code, d = fetch(f"https://gitlab.com/api/v4/projects/{proj_id}/issues/{c['iid']}", delay=5)
        if code == 200:
            body = (d.get("description","") or "")[:800]
            print(f"  body: {body}")
            print(f"  state: {d.get('state')}")
            print(f"  assignees: {d.get('assignees')}")
