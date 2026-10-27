import json, urllib.request, ssl, time

GH_TOKEN = "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"
CB_TOKEN = "86f56136e9bdbe4a6fe60d0b8f2e4c277f407590"
GH_HEADERS = {"Authorization": f"token {GH_TOKEN}", "User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github+json"}
CB_HEADERS = {"Authorization": f"token {CB_TOKEN}", "Content-Type": "application/json", "Accept": "application/json", "User-Agent": "Mozilla/5.0"}
CTX = ssl.create_default_context()

def gh_post(url, body):
    req = urllib.request.Request(url, data=json.dumps({"body": body}).encode(), headers=GH_HEADERS, method="POST")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            d = json.loads(resp.read().decode())
        return resp.status, d
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:200]}

def cb_post(url, body):
    req = urllib.request.Request(url, data=json.dumps({"body": body}).encode(), headers=CB_HEADERS, method="POST")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            d = json.loads(resp.read().decode())
        return resp.status, d
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:200]}

# ============================================================
# 1. wafrn/wafrn !864 — respond to gabboman's feedback
# ============================================================
print("=== 1. wafrn/wafrn !864 — respond to gabboman ===")
body = """Thanks for the clear direction @gabboman — three changes coming:

1. **Settings service**: move the toggle to `settings.service.ts` as a server-side preference (default: show results), so it's one setting per user, not one button per poll.
2. **Development branch**: I'll rebase onto `development` instead of `main`.
3. **No per-poll button**: the toggle moves to the settings page; polls just read the preference.

I'll push the refactor within the next day. Should the setting key follow the existing pattern (e.g. `wafrn.hidePollResultsBeforeVoting`) or do you prefer a different name?"""
code, d = cb_post("https://codeberg.org/api/v1/repos/wafrn/wafrn/issues/864/comments", body)
print(f"  HTTP {code}: {'✅ posted' if code == 201 else d}")

# ============================================================
# 2. punkpeye/awesome-remote-mcp-servers #1928 — add Glama badge
# ============================================================
print("\n=== 2. punkpeye/awesome-remote-mcp-servers #1928 ===")
body = """Thanks for the review @punkpeye! I've added the Glama badge to the entry. The server is now listed at [Glama](https://glama.ai/mcp/servers/@alicelabs-llc/marketnow) with its tool definitions and endpoint health visible.

Updated entry with badge:
```
- [@alicelabs-llc/marketnow](https://glama.ai/mcp/servers/@alicelabs-llc/marketnow) 🔓 - MarketNow is a trust layer for AI agents. It verifies agent identity, solvency, and risk via ATC/1.0 signed verdicts — x402 pay-per-call.
```

Let me know if the badge format needs adjustment."""
code, d = gh_post("https://api.github.com/repos/punkpeye/awesome-remote-mcp-servers/issues/1928/comments", body)
print(f"  HTTP {code}: {'✅ posted' if code == 201 else d}")

# ============================================================
# 3. useagenthq/useagent #84 — respond to "recheck"
# ============================================================
print("\n=== 3. useagenthq/useagent #84 ===")
body = """Hi @abhishekgahlot2 — rechecking now. The latest commit (6652c2c5) has:

1. **Wrong-turn scroll fix**: the jump lookup is scoped to this trace's `<section>` via `traceRef.current.querySelector`, so a second failed turn can no longer land on the first turn's failure row. An SSR test was added.
2. **Collapse-all state**: uses a Set of section IDs, so collapsing/expanding doesn't lose state when switching traces.
3. **Jump-to-error**: highlights the row for 2s then scrolls it into view.

The screenshot you asked for in the issue is in the PR description. Is there something specific that didn't look right when you said "recheck"? Happy to dig into it."""
code, d = gh_post("https://api.github.com/repos/useagenthq/useagent/issues/84/comments", body)
print(f"  HTTP {code}: {'✅ posted' if code == 201 else d}")

# ============================================================
# 4. CodeSigils/awesome-agent-trust #52 — gentle ping
# ============================================================
print("\n=== 4. CodeSigils/awesome-agent-trust #52 ===")
body = """Hi @CodeSigils — gentle follow-up. I pushed the revised commit with the licensing-boundary clarification (protocol/spec components are MIT, the hosted verifier is source-available AL-1.0) per your earlier feedback. Is there anything else you'd like me to adjust before this can move forward?"""
code, d = gh_post("https://api.github.com/repos/CodeSigils/awesome-agent-trust/issues/52/comments", body)
print(f"  HTTP {code}: {'✅ posted' if code == 201 else d}")

# ============================================================
# 5. pablocaeg/sloptotal #161 — no maintainer response yet, just wait
# ============================================================
print("\n=== 5. pablocaeg/sloptotal #161 — no action (waiting for human review) ===")

# ============================================================
# 6. docker/mcp-registry #5175 — check for new comments
# ============================================================
print("\n=== 6. docker/mcp-registry #5175 — check comments ===")
req = urllib.request.Request("https://api.github.com/repos/docker/mcp-registry/issues/5175/comments?per_page=10&sort=desc", headers=GH_HEADERS, method="GET")
with urllib.request.urlopen(req, context=CTX, timeout=15) as resp:
    comments = json.loads(resp.read().decode())
for c in comments[:3]:
    author = c.get("user",{}).get("login","?")
    if author == "eddyflores100-lang":
        continue
    body_text = (c.get("body","") or "").replace("\n"," ")[:200]
    print(f"  💬 {author} ({c.get('created_at','?')[:19]}): {body_text}")

# ============================================================
# 7. x402-foundation/x402 #3815 — Vercel auth issue
# ============================================================
print("\n=== 7. x402-foundation/x402 #3815 — Vercel auth ===")
body = """The Vercel deployment notification is a side effect of the PR touching files in a repo with a Vercel project configured. The Vercel auth is not required for this PR to merge — it's an optional preview deployment that needs a Coinbase team member to authorize. The PR itself only adds a markdown entry to the third-party extensions list.

Is there anything else blocking this besides commit signing? The branch was rebased to a single signed commit (9d69a412) and `check-verified-commits` reported success."""
code, d = gh_post("https://api.github.com/repos/x402-foundation/x402/issues/3815/comments", body)
print(f"  HTTP {code}: {'✅ posted' if code == 201 else d}")

# ============================================================
# 8. Ishannaik/harbour #57 — gentle ping
# ============================================================
print("\n=== 8. Ishannaik/harbour #57 ===")
body = """Friendly follow-up — the CodeRabbit feedback (replace \\t/\\r/\\n with spaces before trimming) was applied in commit 8605d4c. The test now asserts `"dune part two"` instead of `"dunepart two"`. Is there anything else before this can be reviewed?"""
code, d = gh_post("https://api.github.com/repos/Ishannaik/harbour/issues/57/comments", body)
print(f"  HTTP {code}: {'✅ posted' if code == 201 else d}")

# ============================================================
# 9. docker/mcp-registry #5263 — gentle ping on local server PR
# ============================================================
print("\n=== 9. docker/mcp-registry #5263 ===")
body = """Friendly follow-up on the local/containerized MarketNow submission. The Docker image (`ghcr.io/alicelabs-llc/marketnow-mcp`) supports anonymous pull (no login required). Is there anything needed to move this forward alongside the remote entry (#5175)?"""
code, d = gh_post("https://api.github.com/repos/docker/mcp-registry/issues/5263/comments", body)
print(f"  HTTP {code}: {'✅ posted' if code == 201 else d}")

