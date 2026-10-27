import json, urllib.request, ssl, time

TOKEN = "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"
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/vnd.github+json",
}
CTX = ssl.create_default_context()

for attempt in range(3):
    time.sleep(10)
    req = urllib.request.Request(
        "https://api.github.com/repos/pacocartones/market-data-sanity-checker/pulls/112",
        headers=HEADERS,
    )
    with urllib.request.urlopen(req, context=CTX, timeout=15) as resp:
        d = json.loads(resp.read().decode())
    print(f"Attempt {attempt+1}: mergeable={d.get('mergeable','?')} state={d.get('mergeable_state','?')}")
    if d.get('mergeable') is not None:
        break

# Check PR #111 status too (the previous one)
print("\n=== PR #111 status ===")
req = urllib.request.Request(
    "https://api.github.com/repos/pacocartones/market-data-sanity-checker/pulls/111",
    headers=HEADERS,
)
with urllib.request.urlopen(req, context=CTX, timeout=15) as resp:
    d = json.loads(resp.read().decode())
print(f"  state: {d.get('state')}  merged: {bool(d.get('merged_at'))}  mergeable: {d.get('mergeable','?')}  mergeable_state: {d.get('mergeable_state','?')}")
print(f"  updated: {(d.get('updated_at') or '?')[:19]}")
