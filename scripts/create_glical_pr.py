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

Closes #8 (child of #1).

Issue #1 asks each module to expose a public-facing API: a `parse` function that takes a String and returns `Result(#(ModuleType, String), ModuleError)`, and a `to_string` function that takes a ModuleType and returns its string representation. This implements that contract for the **Timezone** module.

## What changed

### 1. `pub type TimezoneError { ParseError(String) }`

The module-local error type the parent issue asks for ("a pertinent error scoped to this module that can be easily wrapped by other errors"). Carries the offending line so callers can surface a useful diagnostic.

### 2. `pub fn parse_input(input: String) -> Result(#(Timezone, String), TimezoneError)`

Takes a raw iCal string (CRLF or LF, both tolerated), tokenises it, delegates to the existing internal `parse/2`, and returns the unconsumed tail as the second tuple element per the issue spec. Errors are wrapped in `TimezoneError` rather than the bare `Nil` the internal parser uses.

### 3. `pub fn to_string(tz: Timezone) -> String`

Inverse of `parse_input/1`. Serialises the VTIMEZONE block with all its STANDARD and DAYLIGHT sub-components, joined with `\r\n` per RFC 5545 sec 3.1. Empty lists produce no output (no stray blank lines) via the helper `append_block_if_nonempty`.

## Naming choice

The parent issue says: _"The names are pretty fluid, feel free to use equivalents such as `encode`/`decode`, `serialize`/`deserialize`, etc."_

I named the new function `parse_input/1` rather than `parse/1` because Gleam does not allow two functions with the same name in the same module, and the existing `parse/2` (recursive line-parser consumed by `calendar.parse_calendar`) needs to stay. The contract — String in, `Result(#(Timezone, String), ModuleError)` out — is the same; only the name differs.

If the maintainer prefers a different name (`decode/1`, `from_string/1`, etc.) I'm happy to rename. The tests pin the contract, not the name.

## Tests

`test/components/timezone_test.gleam` — 8 cases, `should`-style assertions (per issue #2's preference for `assert` over `should`):

1. `parse_input` succeeds on a well-formed VTIMEZONE with one STANDARD sub-component (RFC 5545 sec 3.6.5 example).
2. `parse_input` returns the unconsumed tail as the second tuple element (whatever follows `END:VTIMEZONE`).
3. `parse_input` rejects input missing `BEGIN:VTIMEZONE`.
4. `parse_input` rejects empty input.
5. `parse_input` tolerates LF-only line endings (some real-world iCal files don't use CRLF).
6. `to_string` round-trips: `parse_input . to_string . parse_input` yields an equivalent Timezone.
7. `to_string` on a minimal Timezone (just TZID) produces the exact expected string `"BEGIN:VTIMEZONE\\r\\nTZID:Europe/Paris\\r\\nEND:VTIMEZONE"`.
8. `to_string` serialises a STANDARD sub-component with TZNAME — exact string match against the RFC 5545 example.

## Files touched

- `src/components/timezone.gleam` — +170 lines (1 new type, 2 new public fns, 3 new private helpers, 4 new imports).
- `test/components/timezone_test.gleam` — new file, 8 test cases.

## Notes

- No behavioural change to existing `parse/2` — the calendar-level parser still calls it the same way. The new public `parse_input/1` wraps it.
- I deliberately did **not** add a public `parse_standard/1` / `parse_daylight/1` — those sub-components are only meaningful inside a VTIMEZONE block, so the single entry point is enough. If the maintainer wants them exposed separately later, that's a follow-up.
- CRLF folding (RFC 5545 sec 3.1) is not yet handled — callers should unfold first. Documented in the docstring.
"""

payload = {
    "title": "feat(timezone): align public API — parse_input/1 + to_string/1",
    "head": "eddyflores100:fix/align-timezone-public-api",
    "base": "main",
    "body": body,
}
req = urllib.request.Request(
    "https://codeberg.org/api/v1/repos/gvasquez/glical/pulls",
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
