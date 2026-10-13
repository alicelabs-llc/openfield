import json, urllib.request, ssl

TOKEN = "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"
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/vnd.github+json",
}
CTX = ssl.create_default_context()

def api(method, url, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())

REPOS = ["Ergane-Foundation/vajra", "Ishannaik/harbour", "NovaCode37/Prism-platform"]
USER = "eddyflores100-lang"

for repo in REPOS:
    print(f"\n=== {repo} — existing PRs from {USER} ===")
    # list all open PRs from the user
    code, d = api("GET", f"https://api.github.com/repos/{repo}/pulls?state=all&sort=created&direction=desc&per_page=20")
    if code != 200:
        print(f"  HTTP {code}: {d.get('message','')}")
        continue
    found = False
    for pr in d:
        head_repo = pr.get('head',{}).get('repo',{})
        if head_repo and head_repo.get('full_name','').startswith(USER):
            print(f"  PR #{pr['number']} [{pr['state']}{'/merged' if pr.get('merged_at') else ''}]: {pr['title'][:80]}")
            print(f"    URL:    {pr['html_url']}")
            print(f"    branch: {pr['head']['ref']}")
            print(f"    base:   {pr['base']['ref']}")
            print(f"    created: {pr['created_at'][:19]}  updated: {pr['updated_at'][:19]}")
            print(f"    mergeable: {pr.get('mergeable','?')}  mergeable_state: {pr.get('mergeable_state','?')}")
            # Latest review/comment count
            print(f"    comments: {pr.get('comments',0)}  review_comments: {pr.get('review_comments',0)}")
            found = True
    if not found:
        print(f"  No PRs found from {USER}.")
