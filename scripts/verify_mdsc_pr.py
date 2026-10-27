import json, urllib.request, ssl, time

TOKEN = "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"
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/vnd.github+json",
}
CTX = ssl.create_default_context()

# Wait for mergeable calc
for attempt in range(3):
    time.sleep(15)
    req = urllib.request.Request(
        "https://api.github.com/repos/pacocartones/market-data-sanity-checker/pulls/111",
        headers=HEADERS,
    )
    with urllib.request.urlopen(req, context=CTX, timeout=15) as resp:
        d = json.loads(resp.read().decode())
    print(f"Attempt {attempt+1}: mergeable={d.get('mergeable','?')} state={d.get('mergeable_state','?')}")
    if d.get('mergeable') is not None:
        break

# Check CI status
sha = d.get('head',{}).get('sha','')
if sha:
    time.sleep(5)
    req = urllib.request.Request(
        f"https://api.github.com/repos/pacocartones/market-data-sanity-checker/commits/{sha}/check-runs?per_page=20",
        headers=HEADERS,
    )
    with urllib.request.urlopen(req, context=CTX, timeout=15) as resp:
        d2 = json.loads(resp.read().decode())
    runs = d2.get('check_runs',[])
    print(f"\nCI checks ({len(runs)}):")
    for r in runs[:10]:
        print(f"  - {r.get('name','?')[:50]}: {r.get('status','?')}/{r.get('conclusion','?')}")
