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

# GitLab has a /issues endpoint for cross-project search
print("=== GitLab cross-project issue search ===")
code, d = fetch("https://gitlab.com/api/v4/issues?search=hacktoberfest&state=opened&per_page=20&sort=desc&order_by=created_at", delay=10)
if code == 200 and isinstance(d, list):
    print(f"Found {len(d)} issues mentioning hacktoberfest")
    for it in d[:10]:
        proj_id = it.get("project_id")
        title = it.get("title","")[:70]
        iid = it.get("iid")
        labels = it.get("labels",[])
        created = (it.get("created_at","?"))[:10]
        url = it.get("web_url","")
        print(f"  !{iid} ({created}): {title}")
        print(f"    labels: {labels[:5]}")
        print(f"    url: {url}")
else:
    print(f"  HTTP {code}: {str(d)[:200]}")

# Also search for "good first issue" label
print("\n=== GitLab cross-project search: good first issue ===")
code, d = fetch("https://gitlab.com/api/v4/issues?labels=good+first+issue&state=opened&per_page=20&sort=desc&order_by=created_at", delay=15)
if code == 200 and isinstance(d, list):
    print(f"Found {len(d)} issues with 'good first issue' label")
    for it in d[:10]:
        proj_id = it.get("project_id")
        title = it.get("title","")[:70]
        iid = it.get("iid")
        labels = it.get("labels",[])
        created = (it.get("created_at","?"))[:10]
        url = it.get("web_url","")
        if it.get("assignees"):
            continue
        print(f"  !{iid} ({created}): {title}")
        print(f"    labels: {labels[:5]}")
        print(f"    url: {url}")
else:
    print(f"  HTTP {code}: {str(d)[:200]}")
