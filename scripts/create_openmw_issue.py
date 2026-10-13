import json, urllib.request, ssl, time

TOKEN = "glpat-gupt0wt_EfWmH99u8NGm6WM6MQpvOjEKdTpranZqbQ8.01.1716a5win"
HEADERS = {
    "PRIVATE-TOKEN": TOKEN,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0 Safari/537.36",
    "Accept": "application/json",
}
CTX = ssl.create_default_context()

with open("/tmp/openmw_followup_issue.txt") as f:
    body = f.read()

PID = 7107382  # OpenMW/openmw

url = f"https://gitlab.com/api/v4/projects/{PID}/issues"
payload = json.dumps({
    "title": "Storm direction: port C++ calculations to a Lua player script (follow-up to !5667)",
    "description": body,
    "labels": "feature,refactor,Lua API",  # may be ignored if labels don't exist
}).encode()
req = urllib.request.Request(url, data=payload, headers=HEADERS, method="POST")
try:
    with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
        d = json.loads(resp.read().decode())
    print(f"HTTP {resp.status} - issue iid: {d.get('iid')}")
    print(f"  web_url: {d.get('web_url')}")
    print(f"  state: {d.get('state')}")
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()[:400]}")
except Exception as e:
    print(f"ERROR: {e}")
