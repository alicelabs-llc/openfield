import json, urllib.request, ssl, time

TOKEN = "glpat-gupt0wt_EfWmH99u8NGm6WM6MQpvOjEKdTpranZqbQ8.01.1716a5win"
HEADERS = {
    "PRIVATE-TOKEN": TOKEN,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0 Safari/537.36",
    "Accept": "application/json",
}
CTX = ssl.create_default_context()

with open("/tmp/openmw_reply_body.txt") as f:
    body = f.read()

PID = 7107382
MR_IID = 5667

url = f"https://gitlab.com/api/v4/projects/{PID}/merge_requests/{MR_IID}/notes"
payload = json.dumps({"body": body}).encode()
req = urllib.request.Request(url, data=payload, headers=HEADERS, method="POST")
try:
    with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
        d = json.loads(resp.read().decode())
    print(f"HTTP {resp.status} - note id: {d.get('id')}")
    print(f"  author: {d.get('author',{}).get('username')}")
    print(f"  created_at: {d.get('created_at')}")
    print(f"  preview: {d.get('body','')[:200]}")
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()[:300]}")
except Exception as e:
    print(f"ERROR: {e}")
