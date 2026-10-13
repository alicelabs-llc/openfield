import json, urllib.request, ssl, sys

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
    except Exception as e:
        return -1, {"error": str(e)}

# 1) Verify token
print("=== TOKEN VERIFICATION ===")
code, d = api("GET", "https://api.github.com/user")
if code != 200:
    print(f"FAILED: HTTP {code}: {d}")
    sys.exit(1)
print(f"Authenticated as: {d.get('login')} (id={d.get('id')})")

# 2) Get user login
USER = d['login']
print()

# 3) For each PR, verify the branch exists in the fork, then create the PR
PRS = [
    {
        "upstream": "Ergane-Foundation/vajra",
        "fork": f"{USER}/vajra",
        "head_branch": "fix/29-skip-linux-installer-on-macos",
        "base": "main",
        "title": "install: refuse to run on macOS instead of failing mid-way",
        "body": """Closes #29.

## Summary

`scripts/install.sh` is a Linux-only installer: it detects the system package manager from a hard-coded list of `apt-get`, `dnf`, `yum` and `pacman`, then invokes it to install `python3`, `build-essential`, `iptables`, `iproute2` and friends. None of these packages exist on macOS in the form the script expects.

## Problem

Previously, running `install.sh` on macOS would either:

1. Find a Homebrew-provided `apt-get` shim in `PATH` and proceed to install the wrong packages, leaving the system in a half-configured state and confusing the user, or
2. Reach the "no supported package manager found" branch deep inside the script after the package lists had already been "updated" by whatever the shim did, leaving stray state behind.

Both outcomes are worse than refusing up front.

## Fix

Add an explicit `Darwin` guard at the top of the script (right after the root check, before any package manager probing) that prints a clear error message pointing the user at `README.md` and the platform-specific scripts in `scripts/`.

No behaviour change on Linux — the guard only fires when `uname -s` returns `Darwin`.

## Testing

- `bash -n scripts/install.sh` — no syntax errors.
- Manual test on Linux (`uname -s` returns `Linux`): script proceeds past the new guard and reaches the package manager detection unchanged.
- The Darwin branch is unreachable on Linux, so existing Linux CI is unaffected.
""",
    },
    {
        "upstream": "Ishannaik/harbour",
        "fork": f"{USER}/harbour",
        "head_branch": "fix/41-filter-control-chars-history",
        "base": "main",
        "title": "persist: strip control characters and newlines from push_history",
        "body": """Closes #41.

## Summary

`push_history()` previously stored the trimmed query as-is, including any ASCII control characters embedded in it. Two failure modes resulted:

1. A pasted multi-line query (e.g. `"dune\\r\\nshogun"`) would corrupt the on-disk history file: each entry is written one per line, so the embedded newline silently split the single entry into two phantom entries on the next load.

2. Control bytes like `ESC` (\\x1b), vertical tabs (\\x0b), form feeds (\\x0c) and `NUL` (\\0) made it into the history file and were echoed back into the UI's history picker, occasionally messing up the terminal that rendered them.

## Fix

Strip every char where `char::is_control()` returns `true`, **except** tab (`\\t`) which is meaningful in pasted structured queries. Empty-after-sanitisation queries are dropped just like blank queries already are.

## Test

Adds a regression test that pastes a multi-line query, an `ESC`-riddled query and a tab-containing query, asserting the resulting history is exactly what a user would expect: three entries, no phantom splits, tabs preserved.

```
$ cargo test --lib persist::tests::control_chars_and_newlines_are_stripped_from_history
running 1 test
test persist::tests::control_chars_and_newlines_are_stripped_from_history ... ok
```

Tabs kept; everything else control stripped.
""",
    },
    {
        "upstream": "NovaCode37/Prism-platform",
        "fork": f"{USER}/Prism-platform",
        "head_branch": "fix/388-md5-to-sha256",
        "base": "main",
        "title": "cache: hash filenames with sha256 instead of md5",
        "body": """Closes #388.

## Summary

The two on-disk caches in `web/app.py` — `_cache_key()` for module results and `_geocode_place()` for geocoded coordinates — were keyed on `hashlib.md5(...)` of the request. MD5 is no longer considered collision-resistant and a number of hardened environments block it outright (Fedora 36+, FIPS mode, OpenSSL 3 in strict mode).

## Fix

Switch both to `hashlib.sha256(...)`. SHA-256 is a drop-in replacement here because the digest is only used as a hex string in a filename — its 64-char length is well within filesystem limits and there is no parsing logic to update.

Old cache files written with md5 will simply be re-generated on first request; there is no migration to run and no data loss.

## Scope

Per issue request: **no changes** to `gravatar.py` (gravatar's API mandates md5) or any other usage that depends on md5 for an externally-defined protocol — only the local cache keys change here.

## Test

- `python -c "import web.app"` — no syntax errors.
- Existing tests pass unchanged.
""",
    },
]

for i, pr in enumerate(PRS, 1):
    print(f"\n=== PR {i}: {pr['upstream']} ← {pr['fork']}:{pr['head_branch']} ===")

    # First, verify the branch exists in the fork
    code, d = api("GET", f"https://api.github.com/repos/{pr['fork']}/branches/{pr['head_branch']}")
    if code != 200:
        print(f"  ❌ branch not found: HTTP {code}: {d.get('message','')}")
        continue
    print(f"  ✅ branch exists in fork. HEAD: {d['commit']['sha'][:8]} ({d['commit']['commit']['message'].splitlines()[0][:80]})")

    # Verify upstream exists and get its default branch
    code, d = api("GET", f"https://api.github.com/repos/{pr['upstream']}")
    if code != 200:
        print(f"  ❌ upstream not found: HTTP {code}: {d.get('message','')}")
        continue
    upstream_default = d['default_branch']
    print(f"  upstream default branch: {upstream_default}")
    if upstream_default != pr['base']:
        print(f"  ⚠️ base differs from upstream default! Using upstream default.")
        pr['base'] = upstream_default

    # Check the issue is open
    issue_num = pr['body'].split('Closes #')[1].split('.')[0].split('\n')[0] if 'Closes #' in pr['body'] else None
    if issue_num:
        code, d = api("GET", f"https://api.github.com/repos/{pr['upstream']}/issues/{issue_num}")
        if code == 200:
            print(f"  issue #{issue_num}: {d['state']} — {(d.get('title',''))[:80]}")
        else:
            print(f"  ⚠️ issue #{issue_num}: HTTP {code} — {d.get('message','')[:120]}")

    # Create the PR
    payload = {
        "title": pr["title"],
        "head": f"{pr['fork'].split('/')[0]}:{pr['head_branch']}",
        "base": pr["base"],
        "body": pr["body"],
    }
    code, d = api("POST", f"https://api.github.com/repos/{pr['upstream']}/pulls", payload)
    if code in (200, 201):
        print(f"  🎉 PR #{d['number']} created: {d['html_url']}")
        print(f"     state: {d['state']}  draft: {d.get('draft',False)}")
    else:
        print(f"  ❌ PR creation failed: HTTP {code}")
        print(f"     message: {d.get('message','')}")
        if 'errors' in d:
            for e in d['errors']:
                print(f"     - {e.get('message','')}")
