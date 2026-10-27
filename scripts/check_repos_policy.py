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
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]
    except Exception as e:
        return -1, str(e)[:200]

REPOS = [
    "pacocartones/market-data-sanity-checker",
    "DeepGym/deepgym",
    "fatfingers23/trackscape-discord-bot",
    "Supinic/supinic.com",
    "lenra-io/dofigen",
]

for repo in REPOS:
    print(f"\n{'='*60}")
    print(f"  {repo}")
    print(f"{'='*60}")
    # Repo info
    code, body = api(f"https://api.github.com/repos/{repo}")
    if code != 200:
        print(f"  HTTP {code}")
        continue
    d = json.loads(body)
    print(f"  ⭐ {d.get('stargazers_count',0)}  forks: {d.get('forks_count',0)}  open issues: {d.get('open_issues_count',0)}")
    print(f"  archived: {d.get('archived',False)}  disabled: {d.get('disabled',False)}")
    print(f"  default_branch: {d.get('default_branch','?')}")
    print(f"  pushed_at: {d.get('pushed_at','?')[:19]}  created: {d.get('created_at','?')[:10]}")
    print(f"  license: {(d.get('license') or {}).get('spdx_id','?')}")
    print(f"  description: {(d.get('description') or '')[:120]}")
    
    # CONTRIBUTING.md
    time.sleep(2)
    code, body = api(f"https://raw.githubusercontent.com/{repo}/{d.get('default_branch','main')}/CONTRIBUTING.md")
    if code == 200:
        # Look for AI policy
        body_lower = body.lower()
        print(f"  CONTRIBUTING.md ({len(body)} chars):")
        for keyword in ["ai", "llm", "chatgpt", "claude", "copilot", "gpt", "generated"]:
            if keyword in body_lower:
                # find context
                idx = body_lower.find(keyword)
                ctx = body[max(0,idx-60):idx+200].replace('\n',' ')
                print(f"    AI keyword '{keyword}' found: ...{ctx}...")
                break
        else:
            print(f"    No AI/LLM restrictions found ✓")
    else:
        print(f"  CONTRIBUTING.md: HTTP {code}")
    
    # Look at recent merged PRs (responsiveness signal)
    time.sleep(2)
    code, body = api(f"https://api.github.com/repos/{repo}/pulls?state=closed&sort=updated&direction=desc&per_page=3")
    if code == 200:
        prs = json.loads(body)
        for pr in prs[:3]:
            merged = bool(pr.get('merged_at'))
            if merged:
                print(f"  recent PR #{pr.get('number')} MERGED: {pr.get('title','')[:60]} ({(pr.get('merged_at') or '?')[:10]})")
            else:
                print(f"  recent PR #{pr.get('number')} closed-no-merge ({(pr.get('closed_at') or '?')[:10]})")
