import json, urllib.request, ssl, time

TOKEN = "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"
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/vnd.github+json",
}
CTX = ssl.create_default_context()

# Create fork
req = urllib.request.Request(
    "https://api.github.com/repos/pacocartones/market-data-sanity-checker/forks",
    data=json.dumps({}).encode(),
    headers=HEADERS,
    method="POST",
)
try:
    with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
        d = json.loads(resp.read().decode())
    print(f"HTTP {resp.status} - fork created: {d.get('full_name')}")
    print(f"  URL: {d.get('html_url')}")
    print(f"  parent: {d.get('parent',{}).get('full_name')}")
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()[:300]}")
