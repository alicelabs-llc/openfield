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

print("=== libredb/libredb-studio repo info ===")
code, d = api("https://codeberg.org/api/v1/repos/libredb/libredb-studio", delay=3)
if code == 200:
    print(f"  stars: {d.get('stars_count',0)}  forks: {d.get('forks_count',0)}")
    print(f"  default branch: {d.get('default_branch','?')}")
    print(f"  language: {d.get('language','?')}")
    print(f"  updated: {d.get('updated_at','?')[:19]}")
    print(f"  archived: {d.get('archived',False)}")
    print(f"  description: {(d.get('description') or '')[:120]}")
    print(f"  url: https://codeberg.org/libredb/libredb-studio")

print("\n=== Look at issue #610 (Russian README) - simplest candidate ===")
code, d = api("https://codeberg.org/api/v1/repos/libredb/libredb-studio/issues/610", delay=3)
if code == 200:
    print(f"  title: {d.get('title','?')}")
    print(f"  state: {d.get('state')}  assignees: {[a.get('login','?') for a in d.get('assignees',[])]}")
    print(f"  created: {d.get('created_at','?')[:10]}  updated: {d.get('updated_at','?')[:10]}")
    print(f"  comments: {d.get('comments',0)}")
    print(f"  body:")
    print(d.get('body','')[:1500])

print("\n=== Look at issue #963 (remove logout note) ===")
code, d = api("https://codeberg.org/api/v1/repos/libredb/libredb-studio/issues/963", delay=3)
if code == 200:
    print(f"  title: {d.get('title','?')}")
    print(f"  state: {d.get('state')}  assignees: {[a.get('login','?') for a in d.get('assignees',[])]}")
    print(f"  created: {d.get('created_at','?')[:10]}  updated: {d.get('updated_at','?')[:10]}")
    print(f"  body:")
    print(d.get('body','')[:1200])

print("\n=== Look at issue #751 (copy button on schema diff) ===")
code, d = api("https://codeberg.org/api/v1/repos/libredb/libredb-studio/issues/751", delay=3)
if code == 200:
    print(f"  title: {d.get('title','?')}")
    print(f"  state: {d.get('state')}  assignees: {[a.get('login','?') for a in d.get('assignees',[])]}")
    print(f"  created: {d.get('created_at','?')[:10]}  updated: {d.get('updated_at','?')[:10]}")
    print(f"  body:")
    print(d.get('body','')[:1200])
