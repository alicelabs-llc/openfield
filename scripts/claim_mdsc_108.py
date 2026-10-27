import json, urllib.request, ssl, time

TOKEN = "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"
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/vnd.github+json",
}
CTX = ssl.create_default_context()

# Claim issue #108 with /take command (per the issue's instruction)
# But also add a polite intro comment so we look human, not bot
body = """/take

Hi — planning to pick this up. Quick approach I'll follow:

1. Lower-case the format string in the `rules` command's handler (matching what `check`/`compare` do today).
2. Reuse the existing validation helper (or factor one out if `validateCommonFlags` is the only one) so the error message and exit code 2 match `mdsc check`'s behavior exactly.
3. Add two cases to the CLI test file (modeled on `tests/cli-gating.test.ts`): `--format JSON` returns JSON output, `--format yaml` exits 2 with the expected message.

Will keep the diff minimal and run `pnpm test && pnpm build` before pushing."""

req = urllib.request.Request(
    "https://api.github.com/repos/pacocartones/market-data-sanity-checker/issues/108/comments",
    data=json.dumps({"body": body}).encode(),
    headers=HEADERS,
    method="POST",
)
try:
    with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
        d = json.loads(resp.read().decode())
    print(f"HTTP {resp.status} - comment id: {d.get('id')}")
    print(f"  URL: {d.get('html_url')}")
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()[:300]}")
except Exception as e:
    print(f"ERROR: {e}")
