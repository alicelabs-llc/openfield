import json, urllib.request, ssl

TOKEN = "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"
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/vnd.github+json",
}
CTX = ssl.create_default_context()

body = """/take

Hi — picking this one up. Plan:

1. Add an optional `[id]` positional argument to the `rules` command (Commander.js supports `command('rules [id]')`).
2. Match case-insensitively against both the single-source `registry` and `compareRegistry` — print the matching rule's existing fields (severity, dimension, description, defaultParams, references) when found.
3. When `--format json` is set with an id: print only that rule's `meta` object (single object, not array).
4. Unknown id: exit code 1 with `mdsc: unknown rule "<id>"` plus up to 3 closest prefix matches (case-insensitive `startsWith`).
5. No id: behaviour unchanged.
6. README: one new line under the CLI section showing `mdsc rules SERIES_TAIL_TRUNCATED`.

Will keep the diff minimal and run `pnpm test && pnpm typecheck && pnpm lint` before pushing."""

req = urllib.request.Request(
    "https://api.github.com/repos/pacocartones/market-data-sanity-checker/issues/74/comments",
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
