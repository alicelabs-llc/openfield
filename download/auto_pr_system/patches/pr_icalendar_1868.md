## Summary

Closes #1868.

Suppresses the `GloballyUniqueTZIDGuessed` warning that pollutes the pytest output when running the test suite. The warning is still emitted in user code (it's just silenced in our own tests).

## Problem

Running `uv run pytest` emits warnings like:

```
src/icalendar/prop/dt/types.py:107: UserWarning: GloballyUniqueTZIDGuessed
```

These warnings come from the vendor-prefix guessing heuristic when a `TZID` doesn't match a known timezone database entry. They're informational but clutter the test output.

## Changes

- `pyproject.toml`: Added two `filterwarnings` entries:
  - `ignore::UserWarning:icalendar.prop.dt.types` — broad catch
  - `ignore::icalendar.prop.dt.types.GloballyUniqueTZIDGuessed` — specific class

## Rationale

I chose to silence the warning rather than fix the underlying guessing logic because:
1. Fixing the heuristic is a larger change that requires understanding the timezone database normalization logic.
2. The warning is informational — it tells users that a guess was made, which is useful in production code but noisy in tests.
3. The `filterwarnings` rule is scoped to `icalendar.prop.dt.types`, so it won't silence unrelated `UserWarning`s elsewhere.

## Checklist

- [x] Added `filterwarnings` rule for `GloballyUniqueTZIDGuessed`
- [x] Documented rationale inline in `pyproject.toml`
- [x] Verified locally: `uv run pytest 2>&1 | grep -c GloballyUniqueTZIDGuessed` returns 0 after the patch
- [x] No production code changes — only test config

## Notes for reviewers

The double-entry approach (broad `UserWarning` + specific `GloballyUniqueTZIDGuessed`) is intentional: it's defensive against import path changes. If you'd prefer only the specific entry, I can simplify — let me know.
