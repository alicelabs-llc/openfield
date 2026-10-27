import json, urllib.request, ssl, time

TOKEN = "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"
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/vnd.github+json",
}
CTX = ssl.create_default_context()

def api(url, delay=2):
    time.sleep(delay)
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=15) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())

# Top candidates
ISSUES = [
    ("pacocartones/market-data-sanity-checker", 108),
    ("pacocartones/market-data-sanity-checker", 74),
    ("pacocartones/market-data-sanity-checker", 75),
    ("pacocartones/market-data-sanity-checker", 79),
    ("DeepGym/deepgym", 27),
    ("fatfingers23/trackscape-discord-bot", 53),
    ("fatfingers23/trackscape-discord-bot", 45),
    ("lenra-io/dofigen", 476),
]

for repo, num in ISSUES:
    print(f"\n{'='*70}")
    print(f"  {repo}#{num}")
    print(f"{'='*70}")
    code, d = api(f"https://api.github.com/repos/{repo}/issues/{num}")
    if code != 200:
        print(f"  HTTP {code}")
        continue
    print(f"  title: {d.get('title','')}")
    print(f"  state: {d.get('state')}  comments: {d.get('comments',0)}  assignee: {(d.get('assignee') or {}).get('login','none')}")
    print(f"  created: {d.get('created_at','?')[:10]}  updated: {d.get('updated_at','?')[:10]}")
    print(f"  labels: {[l.get('name','') for l in d.get('labels',[])]}")
    print(f"  body:")
    print(d.get('body','')[:1500])
    print()
