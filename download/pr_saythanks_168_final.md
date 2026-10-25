## Summary

Closes #168.

Replaces 2 bare `except:` statements with specific exception types to satisfy flake8 FLK-E722 linting. Bare excepts catch `KeyboardInterrupt` and `SystemExit`, which is almost never intended.

## Changes

- `saythanks/storage.py` line 123: `except:` → `except (URLError, HTTPError, TimeoutError, OSError):` (network I/O)
- `saythanks/storage.py` line 142: `except:` → `except (json.JSONDecodeError, ValueError):` (JSON parsing)

## Checklist

- [x] Replaced both bare except statements
- [x] Used specific exception types relevant to each operation
- [x] No breaking changes — same behavior except no longer catches KeyboardInterrupt/SystemExit
