## Summary

Closes #1921.

Adds a `.get(value, default=None)` classmethod to `StrEnum` so callers can look up enum members without raising `ValueError` for unknown strings. Mirrors `dict.get` semantics with proper `@overload` typing.

## Changes

- `src/icalendar/enums.py`: Added `StrEnum.get()` classmethod with `@overload` typing
- `src/icalendar/tests/test_enum_get.py`: New test module with 8 tests

## Example

```python
>>> PARTSTAT.get("ACCEPTED")
<PARTSTAT.ACCEPTED: 'ACCEPTED'>
>>> PARTSTAT.get("no-value") is None
True
>>> PARTSTAT.get("no-value", "other-value")
'other-value'
```

## Checklist

- [x] Added `StrEnum.get()` classmethod with `@overload` typing
- [x] Documented behavior in docstring with examples
- [x] Added 8 unit tests
- [x] Fully backward compatible — existing API unchanged
