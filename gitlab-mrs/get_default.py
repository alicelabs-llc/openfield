import json, urllib.request, ssl, time, sys
TOKEN = "glpat-gupt0wt_EfWmH99u8NGm6WM6MQpvOjEKdTpranZqbQ8.01.1716a5win"
HEADERS = {"PRIVATE-TOKEN": TOKEN, "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}
CTX = ssl.create_default_context()
def api_get(url, delay=0, retries=3):
    for attempt in range(retries):
        time.sleep(delay)
        req = urllib.request.Request(url, headers=HEADERS, method="GET")
        try:
            with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code in (403,429) and attempt<retries-1:
                delay = max(delay,30)*2; continue
            raise
for pid in ["87321897"]:
    d = api_get(f"https://gitlab.com/api/v4/projects/{pid}", delay=0)
    print(pid, "default_branch=", d.get("default_branch"), "path=", d.get("path_with_namespace"))
