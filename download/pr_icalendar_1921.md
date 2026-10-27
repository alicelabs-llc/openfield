## Summary

Closes #1921.

Adds a `.get(value, default=None)` classmethod to `StrEnum` so callers can look up enum members without raising `ValueError` for unknown strings. Mirrors `dict.get` semantics and adds proper `@overload` typing.

## Problem

```python
>>> from icalendar import PARTSTAT
>>> PARTSTAT("no-value")
ValueError: 'no-value' is not a valid PARTSTAT
```

When parsing iCalendar data from external sources (e.g. untrusted `.ics` files), an unknown `PARTSTAT` value currently raises `ValueError`, forcing callers to wrap every lookup in `try/except`. A `dict.get`-style API is more ergonomic.

## Changes

- `src/icalendar/enums.py`: Added `StrEnum.get()` classmethod with `@overload` typing (one overload for the no-default case returning `Optional[StrEnum]`, one for the with-default case returning `Any`).
- `src/icalendar/tests/test_enum_get.py`: New test module with 9 tests covering the documented behavior.

## Example usage (matches issue body)

```python
>>> from icalendar import PARTSTAT
>>> PARTSTAT.get("ACCEPTED")
<PARTSTAT.ACCEPTED: 'ACCEPTED'>
>>> PARTSTAT.get("no-value") is None
True
>>> PARTSTAT.get("no-value", "other-value")
'other-value'
>>> PARTSTAT.get("no-value", PARTSTAT.NEEDS_ACTION)
<PARTSTAT.NEEDS_ACTION: 'NEEDS-ACTION'>
```

## Backward compatibility

Fully backward compatible. Existing `PARTSTAT("ACCEPTED")` calls still work and still raise `ValueError` for unknown values. Only the new `.get()` method changes behavior.

## Checklist

- [x] Added `StrEnum.get()` classmethod with `@overload` typing
- [x] Documented behavior in docstring with examples
- [x] Added 9 unit tests covering valid/invalid/default cases
- [x] Mirrored `dict.get` semantics exactly
- [x] Verified locally: `uv run pytest src/icalendar/tests/test_enum_get.py -v` (9 passed)
- [x] No breaking changes — existing API unchanged

## Notes for reviewers

The `@overload` decorators are decorative-only at runtime (Python uses them for static type checkers like mypy/pyright). At runtime only the third definition (with `default=None`) is used. This is the standard pattern from `dict.get` and `os.environ.get`.
