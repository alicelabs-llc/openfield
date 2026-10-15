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

# Skip libredb-studio (GitHub mirror, 0 stars/forks, no real activity)
# Investigate other repos with hacktoberfest issues

print("=== Look at other codeberg candidates from earlier query ===")
print("(We had Freeyourgadget/Gadgetbridge#7035, daudix/ametrine#147, etc.)")
print()

# Let me search specifically for repos with hacktoberfest topic in Codeberg
print("=== Codeberg repos with topic 'hacktoberfest' ===")
code, d = api("https://codeberg.org/api/v1/repos/search?q=hacktoberfest&topic=true&limit=20", delay=3)
if code == 200:
    items = d if isinstance(d, list) else d.get("data", [])
    print(f"  results: {len(items)}")
    for r in items[:15]:
        print(f"  - {r.get('full_name','?')} ⭐{r.get('stars_count',0)} forks:{r.get('forks_count',0)} lang:{r.get('language','?')}")
        print(f"    pushed:{r.get('updated_at','?')[:10]}  archived:{r.get('archived',False)}")

print("\n=== Check Freeyourgadget/Gadgetbridge (real Android project) ===")
code, d = api("https://codeberg.org/api/v1/repos/Freeyourgadget/Gadgetbridge", delay=3)
if code == 200:
    print(f"  stars: {d.get('stars_count',0)}  forks: {d.get('forks_count',0)}")
    print(f"  language: {d.get('language','?')}")
    print(f"  description: {(d.get('description') or '')[:120]}")
    print(f"  updated: {d.get('updated_at','?')[:19]}")
