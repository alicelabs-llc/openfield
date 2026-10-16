import json, urllib.request, ssl

TOKEN = "86f56136e9bdbe4a6fe60d0b8f2e4c277f407590"
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0",
}
CTX = ssl.create_default_context()

body = """## Summary

Closes #16.

`for_sarif` crashed with `bad argument #1 to 'ipairs' (table expected, got nil)` when a SARIF `result` object omitted the `locations` field. The SARIF spec (OASIS v2.1.0 sec 3.27.12) allows results without `locations` — e.g. tool-level/summary diagnostics like Verilator's `"Exiting due to N error(s)"` message emitted via `--diagnostics-sarif`.

## Root cause

The outer loop already guarded `run.results` with `or {}`, but the inner loop did not apply the same guard to `result.locations`:

```lua
for _, result in ipairs(run.results or {}) do
  for _, location in ipairs(result.locations) do   -- ← crash if result.locations is nil
```

## Fix

One character change — guard `result.locations` with `or {}`:

```lua
for _, result in ipairs(run.results or {}) do
  for _, location in ipairs(result.locations or {}) do
```

Results without `locations` are silently skipped (no file/line info to attach a diagnostic to), matching the existing behaviour for missing `run.results`.

## Tests

Three new cases in `spec/parser_spec.lua` under `describe('for_sarif')`:

1. **`parses a basic SARIF result with locations`** — happy-path coverage for the existing behaviour (was previously uncovered in spec).
2. **`does not crash when a result has no 'locations' field (issue #16)`** — the regression test. Uses the exact SARIF document shape from the issue body: a tool-level summary result with no `locations` mixed with a regular result that does have `locations`. Asserts the summary is skipped and the regular result is parsed.
3. **`does not crash when run.results is missing entirely`** — pins the contract that a notifications-only run produces an empty diagnostic list (already worked, but worth pinning).

## Reproduction

```lua
-- The exact JSON from the issue body, plus a regular result with locations.
local output = vim.json.encode({
  runs = {{
    tool = { driver = { name = "verilator" } },
    results = {
      -- Tool-level summary: no `locations` field.
      { level = "error", message = { text = "Exiting due to 18 error(s)" } },
      -- Regular result: has `locations`.
      {
        level = "warning",
        message = { text = "Unused signal" },
        locations = {{
          physicalLocation = {
            artifactLocation = { uri = "file:///test.sv" },
            region = { startLine = 42 },
          },
        }},
      },
    },
  }},
})
```

Before the fix: `lua/lint/parser.lua:187: bad argument #1 to 'ipairs' (table expected, got nil)`.

After the fix: `{ { message = "Unused signal", lnum = 41, ... } }` — the summary result is skipped, the regular result is parsed.

## Notes

- The fix is the exact one suggested by @mfussenegger in the issue body. I just added the test coverage and pinned the contract.
- No behavioural change for results that already had `locations` — the `or {}` short-circuits to the existing table.
"""

payload = {
    "title": "fix(parser): guard result.locations in for_sarif (issue #16)",
    "head": "eddyflores100:fix/sarif-missing-locations",
    "base": "master",
    "body": body,
}
req = urllib.request.Request(
    "https://codeberg.org/api/v1/repos/mfussenegger/nvim-lint/pulls",
    data=json.dumps(payload).encode(),
    headers=HEADERS,
    method="POST",
)
try:
    with urllib.request.urlopen(req, context=CTX, timeout=30) as resp:
        d = json.loads(resp.read().decode())
    print(f"HTTP {resp.status} - PR #{d.get('number')} created")
    print(f"  URL: {d.get('html_url')}")
    print(f"  state: {d.get('state')}  draft: {d.get('draft',False)}")
    print(f"  mergeable: {d.get('mergeable','?')}  merged: {bool(d.get('merged'))}")
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()[:500]}")
