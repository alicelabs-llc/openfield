#!/usr/bin/env python3
"""
Execute 3 actions in parallel:
1. Fork + push + open PR to stacklok/toolhive-catalog with corrected MarketNow entry
2. POST ping comment to jbilcke-hf/clapper #163 ($1,050 bounty)
3. POST ping comment to Parabola-org/parabola #131 ($105 bounty)
4. POST ping comment to Ishannaik/harbour #57 (CodeRabbit already approved)
"""
import json
import urllib.request
import urllib.error
import time
import sys

TOKEN = "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"
USER = "eddyflores100-lang"

def gh(method, url, body=None, expect_json=True):
    """GitHub API call with auth."""
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": f"{USER}-bot",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            if r.status == 204:
                return {"_status": 204}
            body_raw = r.read()
            if expect_json:
                return json.loads(body_raw)
            return {"_status": r.status, "_body": body_raw.decode()[:500]}
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()[:500]
        return {"_error": f"HTTP {e.code}", "_url": url, "_body": err_body}
    except Exception as e:
        return {"_error": str(e), "_url": url}

# === ACTION 1: Fork toolhive-catalog and open PR ===
def action1_toolhive_resubmit():
    print("\n=== ACTION 1: Toolhive-catalog resubmit ===")
    UPSTREAM = "stacklok/toolhive-catalog"
    
    # 1a. Fork
    print(f"[1a] Forking {UPSTREAM}...")
    fork = gh("POST", f"https://api.github.com/repos/{UPSTREAM}/forks")
    if "_error" in fork:
        # If already forked, get existing fork
        print(f"  Fork error (likely exists): {fork['_body'][:200]}")
    else:
        print(f"  Forked: {fork.get('full_name', '?')}")
    
    # Wait for fork to be ready
    print("[1b] Waiting 8s for fork to be ready...")
    time.sleep(8)
    
    # 1c. Get default branch SHA
    print("[1c] Getting default branch info from upstream...")
    upstream_repo = gh("GET", f"https://api.github.com/repos/{UPSTREAM}")
    default_branch = upstream_repo.get("default_branch", "main")
    print(f"  Default branch: {default_branch}")
    
    branch_info = gh("GET", f"https://api.github.com/repos/{UPSTREAM}/branches/{default_branch}")
    base_sha = branch_info.get("commit", {}).get("sha")
    print(f"  Base SHA: {base_sha}")
    
    if not base_sha:
        print(f"  ERROR: couldn't get base SHA. branch_info: {branch_info}")
        return False
    
    # 1d. Create new branch on fork
    new_branch = "resubmit-marketnow-aligned-tools"
    print(f"[1d] Creating branch {new_branch} on fork...")
    branch_create = gh("POST", f"https://api.github.com/repos/{USER}/toolhive-catalog/git/refs", {
        "ref": f"refs/heads/{new_branch}",
        "sha": base_sha,
    })
    if "_error" in branch_create:
        print(f"  Branch create error: {branch_create['_body'][:200]}")
        # Try to update existing branch
        print("  Trying to update existing branch ref...")
        branch_create = gh("PATCH", f"https://api.github.com/repos/{USER}/toolhive-catalog/git/refs/heads/{new_branch}", {
            "sha": base_sha,
            "force": True,
        })
        if "_error" in branch_create:
            print(f"  Branch update error: {branch_create['_body'][:200]}")
            return False
    
    print(f"  Branch created/updated: {new_branch}")
    
    # 1e. Read the entry JSON content
    with open("/home/z/my-project/toolhive-resubmit/io.github.eddyflores100-lang.marketnow.json") as f:
        entry_content = f.read()
    
    import base64
    content_b64 = base64.b64encode(entry_content.encode()).decode()
    file_path = "registries/toolhive/servers/io.github.eddyflores100-lang.marketnow.json"
    
    # 1f. Create file in fork via Contents API
    print(f"[1f] Creating file {file_path} on fork branch {new_branch}...")
    file_create = gh("PUT", f"https://api.github.com/repos/{USER}/toolhive-catalog/contents/{file_path}", {
        "message": f"feat(servers): add MarketNow remote MCP server (aligned tools + _meta fix)\n\nResubmit per feedback from @rdimitrov on #1619:\n- Tool list now matches exactly the 15 tools exposed by https://marketnow.site/api/mcp\n- _meta structure follows the remote server schema example\n- Source repo: https://github.com/eddyflores100-lang/marketnow",
        "content": content_b64,
        "branch": new_branch,
    })
    if "_error" in file_create:
        print(f"  File create error: {file_create['_body'][:300]}")
        # If file exists, try update
        if "already exists" in str(file_create.get("_body", "")):
            print("  File exists, getting SHA to update...")
            existing = gh("GET", f"https://api.github.com/repos/{USER}/toolhive-catalog/contents/{file_path}?ref={new_branch}")
            existing_sha = existing.get("sha") if isinstance(existing, dict) else None
            if existing_sha:
                file_create = gh("PUT", f"https://api.github.com/repos/{USER}/toolhive-catalog/contents/{file_path}", {
                    "message": "feat(servers): add MarketNow remote MCP server (aligned tools + _meta fix)",
                    "content": content_b64,
                    "branch": new_branch,
                    "sha": existing_sha,
                })
                if "_error" in file_create:
                    print(f"  File update error: {file_create['_body'][:300]}")
                    return False
                print(f"  File updated.")
            else:
                print(f"  Could not get existing SHA: {existing}")
                return False
        else:
            return False
    else:
        print(f"  File created: {file_create.get('commit', {}).get('sha', '?')}")
    
    # 1g. Open PR
    print("[1g] Opening PR to upstream...")
    pr_body = """## Resubmission of #1619

Per @rdimitrov's feedback on the closed PR #1619, this resubmission addresses all concerns:

### 1. Tool list aligned with actual remote endpoint

The previous entry described trust/credential verification tools that only the open-source stdio package provides, while the hosted endpoint exposes a different (broader) set. This entry lists exactly the **15 tools** the remote `https://marketnow.site/api/mcp` exposes:

```
marketnow_search_skills        marketnow_get_skill
marketnow_list_categories      marketnow_get_manifest
marketnow_get_install_command  marketnow_verify_trust
marketnow_verify_receipt       marketnow_submit_skill
marketnow_mint_referral        marketnow_lookup_referral
marketnow_recommend_skills     marketnow_get_owasp_compliance
marketnow_check_revocation     marketnow_fingerprint_tool
marketnow_verify_atc_spec
```

### 2. `_meta` structure corrected

The `_meta.io.modelcontextprotocol.registry/publisher-provided` block now follows the remote server schema pattern, with `https://marketnow.site/api/mcp` as the key (matching the `remotes[0].url`).

### 3. Source repo linked

- Live marketplace source: https://github.com/eddyflores100-lang/marketnow
- Listed in the official MCP Registry

### Notes

- The remote endpoint is hosted, no container image is published (hence `remotes` not `packages`).
- All tool names follow the `marketnow_` snake_case convention per the MCP naming spec.
- License: source repo is proprietary (AliceLabs LLC); the remote endpoint is publicly callable without auth for the tools listed.
"""
    pr = gh("POST", f"https://api.github.com/repos/{UPSTREAM}/pulls", {
        "title": "feat(servers): add MarketNow remote MCP server (aligned tools + _meta fix)",
        "head": f"{USER}:{new_branch}",
        "base": default_branch,
        "body": pr_body,
    })
    if "_error" in pr:
        print(f"  PR open error: {pr['_body'][:300]}")
        return False
    print(f"  ✅ PR opened: {pr.get('html_url', '?')}")
    return pr.get("html_url")

# === ACTION 2: Ping clapper #163 ===
def action2_ping_clapper():
    print("\n=== ACTION 2: Ping clapper #163 ($1,050 bounty) ===")
    body = "Friendly ping @jbilcke-hf — saw this PR is tagged with the $1,050 bounty. The ComfyUI workflow browser (OpenArt.ai search) is implemented, builds clean, and the demo screenshot is in the PR description. Happy to address any feedback or rebase if needed. Is there anything blocking review?"
    res = gh("POST", "https://api.github.com/repos/jbilcke-hf/clapper/issues/163/comments", {"body": body})
    if "_error" in res:
        print(f"  ERROR: {res['_body'][:200]}")
        return False
    print(f"  ✅ Comment posted: {res.get('html_url', '?')}")
    return res.get("html_url")

# === ACTION 3: Ping parabola #131 ===
def action3_ping_parabola():
    print("\n=== ACTION 3: Ping parabola #131 ($105 bounty) ===")
    body = "Friendly ping — following up on the stellar account-not-found tightening + retry parameter handling fix. The patch closes the linked issue, tests pass, and the changes are scoped to the retry path. Happy to rebase or address any feedback. Is there anything blocking review?"
    res = gh("POST", "https://api.github.com/repos/Parabola-org/parabola/issues/131/comments", {"body": body})
    if "_error" in res:
        print(f"  ERROR: {res['_body'][:200]}")
        return False
    print(f"  ✅ Comment posted: {res.get('html_url', '?')}")
    return res.get("html_url")

# === ACTION 4: Ping harbour #57 ===
def action4_ping_harbour():
    print("\n=== ACTION 4: Ping harbour #57 ===")
    body = "Friendly ping @Ishannaik — CodeRabbit's review feedback (replace \\t/\\r/\\n with spaces before trimming) was applied in 8605d4c. The test now asserts \"dune part two\" instead of \"dunepart two\". Anything else needed before this can move forward?"
    res = gh("POST", "https://api.github.com/repos/Ishannaik/harbour/issues/57/comments", {"body": body})
    if "_error" in res:
        print(f"  ERROR: {res['_body'][:200]}")
        return False
    print(f"  ✅ Comment posted: {res.get('html_url', '?')}")
    return res.get("html_url")

if __name__ == "__main__":
    # Verify token first
    print("=== Verifying token ===")
    user = gh("GET", "https://api.github.com/user")
    if "_error" in user:
        print(f"Token invalid: {user}")
        sys.exit(1)
    print(f"Token valid. Logged in as: {user.get('login', '?')}")
    
    # Run actions sequentially (parallel would risk rate limits)
    results = {}
    results["clapper"] = action2_ping_clapper()
    results["parabola"] = action3_ping_parabola()
    results["harbour"] = action4_ping_harbour()
    results["toolhive_pr"] = action1_toolhive_resubmit()
    
    print("\n\n=== FINAL SUMMARY ===")
    for k, v in results.items():
        status = "✅" if v else "❌"
        print(f"  {status} {k}: {v if v else 'FAILED'}")
