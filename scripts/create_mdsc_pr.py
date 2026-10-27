import json, urllib.request, ssl

TOKEN = "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"
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/vnd.github+json",
}
CTX = ssl.create_default_context()

body = """Closes #108.

## Summary

The `rules` command did a strict-equality check on `options.format === 'json'`, so:

- `mdsc rules --format JSON` silently printed the **table** (the `json` branch never matched).
- `mdsc rules --format yaml` fell through to the table branch instead of erroring.

`check` and `compare` already did both correctly via `validateCommonFlags`. `rules` now mirrors them.

## Fix

Lower-case the format string once at the top of the action, then reject anything other than `table` or `json` with the same error message and exit code 2 that `check`/`compare` use, before branching on the output format:

```ts
const format = options.format.toLowerCase()
if (format !== 'table' && format !== 'json') {
  console.error('mdsc: --format must be one of: table, json')
  process.exit(2)
}
if (format === 'json') {
  // ... unchanged JSON output ...
}
```

I inlined the check rather than reusing `validateCommonFlags` because `rules` doesn't take `--fail-on` or `--min-score` (the other two checks in that helper). Calling it would mean either making up dummy values for those flags or refactoring `validateCommonFlags` to split format-checking out — both are bigger than the one-line fix the issue asked for, so I went with the inlined version. Happy to refactor if the maintainer prefers.

## Tests

Adds two regression tests next to the existing rules tests in `tests/cli-gating.test.ts`, modelled on the existing `accepts --format JSON (case-insensitive)` test for `check`:

- `accepts --format JSON (case-insensitive) and prints parseable JSON on stdout` — was printing a table before.
- `exits 2 on unknown --format with the same message as check/compare` — was exit 0 before.

## Verification

```
$ pnpm build
ESM ⚡️ Build success in 100ms
DTS ⚡️ Build success in 2860ms

$ pnpm test -- --run tests/cli-gating.test.ts
 ✓ tests/cli-gating.test.ts (23 tests) 2691ms     # was 21 before, now 23
 Test Files  42 passed (42)
      Tests  430 passed (430)

$ node dist/cli.js rules --format JSON  | head -3
{
  "single_source": [
    {
$ node dist/cli.js rules --format yaml
mdsc: --format must be one of: table, json
$ echo $?
2
```

## Files touched

- `src/cli.ts` — 8 new lines in the `rules` command action.
- `tests/cli-gating.test.ts` — 2 new test cases (~25 lines).
"""

payload = {
    "title": "fix(cli): rules command respects --format case and rejects unknown formats",
    "head": "eddyflores100-lang:fix/108-rules-format-case-and-validation",
    "base": "main",
    "body": body,
}
req = urllib.request.Request(
    "https://api.github.com/repos/pacocartones/market-data-sanity-checker/pulls",
    data=json.dumps(payload).encode(),
    headers=HEADERS,
    method="POST",
)
try:
    with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
        d = json.loads(resp.read().decode())
    print(f"HTTP {resp.status} - PR #{d.get('number')} created")
    print(f"  URL: {d.get('html_url')}")
    print(f"  state: {d.get('state')}  draft: {d.get('draft',False)}")
    print(f"  mergeable: {d.get('mergeable','?')}  mergeable_state: {d.get('mergeable_state','?')}")
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()[:400]}")
