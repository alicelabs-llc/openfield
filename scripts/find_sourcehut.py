import json, urllib.request, ssl, time

HEADERS = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
CTX = ssl.create_default_context()

def api(url, delay=2):
    time.sleep(delay)
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:300]}
    except Exception as e:
        return -1, {"error": str(e)[:200]}

# SourceHut has GraphQL API only — let's try REST-ish endpoints they expose
# https://man.sr.ht/api-conventions.md

print("=== SourceHut — try GraphQL ===")
query = """
{
  version {
    major
    minor
    patch
  }
}
"""
req = urllib.request.Request(
    "https://hub.sr.ht/query",
    data=json.dumps({"query": query}).encode(),
    headers={**HEADERS, "Content-Type": "application/json"},
    method="POST",
)
try:
    with urllib.request.urlopen(req, context=CTX, timeout=15) as resp:
        d = json.loads(resp.read().decode())
    print(f"  hub.sr.ht GraphQL: {d}")
except urllib.error.HTTPError as e:
    print(f"  HTTP {e.code}: {e.read().decode()[:300]}")
except Exception as e:
    print(f"  ERR: {e}")

print("\n=== SourceHut todo.sr.ht — bug trackers ===")
# Try listing public trackers
code, d = api("https://todo.sr.ht/api/trackers", delay=3)
print(f"  HTTP {code}: {str(d)[:300]}")

print("\n=== Search Codeberg for repos with hacktoberfest topic, sorted by stars ===")
# Codeberg API v1 supports sort
code, d = api("https://codeberg.org/api/v1/repos/search?q=hacktoberfest&topic=true&limit=30&sort=stars&order=desc", delay=3)
if code == 200:
    items = d if isinstance(d, list) else d.get("data", [])
    print(f"  Top repos with hacktoberfest topic:")
    for r in items[:20]:
        stars = r.get('stars_count',0)
        if stars < 1: continue
        print(f"  - {r.get('full_name','?')} ⭐{stars} forks:{r.get('forks_count',0)} lang:{r.get('language','?')} pushed:{r.get('updated_at','?')[:10]}")
