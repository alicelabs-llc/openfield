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

# Top candidate repos to explore
REPOS = [
    # Smaller / more responsive repos
    "DeepGym/deepgym",           # Python, 7⭐, 9 open issues
    "Ranjeet2063/aetherguard",  # Python, 7⭐, 51 open issues
    "nightlark/pymsi",          # Python, 74⭐, 12 open issues
    "meshery/qa",                # JS, 22⭐, 8 open issues
    "patternfly/chatbot",        # TS, 8⭐, 23 open issues
    "pacocartones/market-data-sanity-checker",  # TS, 2⭐, 15 open issues
    "CruGlobal/mpdx-react",      # TS, 1⭐, 20 open issues
    "BrenekH/blinky",            # Go, 7⭐, 5 open issues
    "hivecommons/hive",          # Go, 65⭐, 22 open issues
    "fatfingers23/trackscape-discord-bot",  # Rust, 10⭐, 14 open issues
    "rumahl/rumahl",             # Rust, 0⭐, 11 open issues
    "lenra-io/dofigen",          # Rust, 85⭐, 24 open issues
    "Supinic/supinic.com",       # JS, 5⭐, 5 open issues
]

print("=" * 70)
print("EXPLORING ISSUES IN HACKTOBERFEST-TOPIC REPOS")
print("=" * 70)

candidates = []
for repo in REPOS:
    print(f"\n=== {repo} ===")
    # Get open issues with labels
    code, d = api(f"https://api.github.com/repos/{repo}/issues?state=open&per_page=20&sort=created&direction=desc", delay=2)
    if code != 200:
        print(f"  HTTP {code}: {str(d)[:200]}")
        continue
    # Filter out PRs (issues have no pull_request key)
    issues_only = [i for i in d if "pull_request" not in i]
    print(f"  {len(issues_only)} open issues (out of {len(d)} items)")
    for it in issues_only[:6]:
        num = it.get("number")
        title = it.get("title","")[:75]
        labels = [l.get("name","") for l in it.get("labels",[])]
        comments = it.get("comments",0)
        assignee = it.get("assignee")
        body_preview = (it.get("body") or "")[:200].replace("\n"," ")
        if assignee:
            continue
        # Skip dep-bot issues
        if any(kw in title.lower() for kw in ["update dependency", "bump ", "chore(deps)", "update @types"]):
            continue
        print(f"  - #{num} ({comments}c): {title}")
        print(f"    labels: {labels}")
        print(f"    body: {body_preview}")
        candidates.append({
            "repo": repo,
            "number": num,
            "title": title,
            "labels": labels,
            "comments": comments,
            "url": it.get("html_url",""),
        })

print("\n" + "=" * 70)
print(f"TOTAL CANDIDATES: {len(candidates)}")
print("=" * 70)
