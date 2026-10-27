import json, urllib.request, ssl, time

GL_TOKEN = "glpat-VTdIPfmOYCLcAQHp0IdlyWM6MQpvOjEKdTpranZqbQ8.01.17073yv2r"
GL_HEADERS = {"PRIVATE-TOKEN": GL_TOKEN, "User-Agent": "Mozilla/5.0", "Accept": "application/json"}
CTX = ssl.create_default_context()

def fetch(url, delay=15):
    time.sleep(delay)
    req = urllib.request.Request(url, headers=GL_HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:300]}
    except Exception as e:
        return -1, {"error": str(e)[:200]}

for name, pid, iid in [
    ("fdroid/fdroidclient", 36189, "1786"),
    ("inkscape/extensions", 5833962, "739"),
    ("inkscape/inkscape", 3472737, "8203"),
]:
    print(f"\n=== {name} !{iid} ===")
    
    # MR details
    code, d = fetch(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}", delay=20)
    if code != 200:
        print(f"  HTTP {code} (Cloudflare) — will retry notes only")
        # Try notes directly
        code2, d2 = fetch(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}/notes?per_page=50&sort=asc&order_by=created_at", delay=20)
        if code2 == 200:
            non_sys = [n for n in d2 if not n.get("system")]
            print(f"  Notes ({len(non_sys)} non-system):")
            for n in non_sys[-5:]:
                author = n.get("author",{}).get("username","?")
                created = (n.get("created_at") or "?")[:19]
                body = (n.get("body") or "").replace("\n"," ").replace("\r"," ")[:300]
                marker = "💬" if author != "eddyflores100" else "  "
                print(f"  {marker} {author} ({created}): {body}")
        else:
            print(f"  notes also blocked: {code2}")
        continue
    
    state = d.get("state","?")
    merged = bool(d.get("merged_at"))
    print(f"  state: {state}  merged: {merged}")
    print(f"  updated: {(d.get('updated_at') or '?')[:19]}")
    
    # Notes
    code3, d3 = fetch(f"https://gitlab.com/api/v4/projects/{pid}/merge_requests/{iid}/notes?per_page=50&sort=asc&order_by=created_at", delay=15)
    if code3 == 200:
        non_sys = [n for n in d3 if not n.get("system")]
        print(f"  Notes ({len(non_sys)} non-system):")
        for n in non_sys[-5:]:
            author = n.get("author",{}).get("username","?")
            created = (n.get("created_at") or "?")[:19]
            body = (n.get("body") or "").replace("\n"," ").replace("\r"," ")[:300]
            marker = "💬" if author != "eddyflores100" else "  "
            print(f"  {marker} {author} ({created}): {body}")
