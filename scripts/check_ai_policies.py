import json, urllib.request, ssl, time

HEADERS = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
CTX = ssl.create_default_context()

def api(url, delay=2, raw=False):
    time.sleep(delay)
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            body = resp.read().decode()
            if raw: return resp.status, body
            return resp.status, json.loads(body)
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:200]}
    except Exception as e:
        return -1, {"error": str(e)[:200]}

REPOS = [
    ("mfussenegger/nvim-lint", "master"),
    ("GeopJr/Tuba", "main"),
    ("spade-lang/spade", "main"),
]

for repo, default_branch in REPOS:
    print(f"\n{'='*60}")
    print(f"  {repo} — AI policy check")
    print(f"{'='*60}")
    # CONTRIBUTING.md
    code, body = api(f"https://codeberg.org/api/v1/repos/{repo}/raw/CONTRIBUTING.md?ref={default_branch}", delay=3, raw=True)
    if code == 200:
        body_lower = body.lower()
        print(f"  CONTRIBUTING.md ({len(body)} chars):")
        for kw in ["ai", "llm", "chatgpt", "claude", "copilot", "gpt", "generated", "gen.ai"]:
            if kw in body_lower:
                idx = body_lower.find(kw)
                ctx = body[max(0,idx-50):idx+200].replace('\n',' ')
                print(f"    AI keyword '{kw}': ...{ctx}...")
                break
        else:
            print(f"    No AI/LLM restriction found ✓")
    else:
        print(f"  CONTRIBUTING.md: HTTP {code}")
    # README.md
    code, body = api(f"https://codeberg.org/api/v1/repos/{repo}/raw/README.md?ref={default_branch}", delay=2, raw=True)
    if code == 200:
        body_lower = body.lower()
        for kw in ["no ai", "no llm", "ai-generated", "human-only", "no gpt", "no copilot"]:
            if kw in body_lower:
                idx = body_lower.find(kw)
                ctx = body[max(0,idx-50):idx+200].replace('\n',' ')
                print(f"    README AI keyword '{kw}': ...{ctx}...")
                break
    # Check recent commits for activity
    code, d = api(f"https://codeberg.org/api/v1/repos/{repo}/commits?limit=3", delay=2)
    if code == 200:
        commits = d if isinstance(d, list) else d.get("data", [])
        if commits:
            print(f"\n  Recent commits:")
            for c in commits[:3]:
                sha = c.get('sha','?')[:8]
                msg = (c.get('commit',{}).get('message','') or '').split('\n')[0][:70]
                date = (c.get('commit',{}).get('author',{}).get('date','?') or '?')[:10]
                print(f"    - {sha} ({date}): {msg}")
