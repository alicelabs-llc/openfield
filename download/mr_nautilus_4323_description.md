## Summary

Closes #4323.

`nautilus_file_get_boolean_metadata()` previously called `g_error()` when the stored value was neither `"true"` nor `"false"`. `g_error()` is documented in GLib as **always aborting the process** with `SIGABRT` — there is no recovery path. Since file metadata is persistent on disk and can be set by external tooling (e.g. `gio set -t string "$DIR" metadata::nautilus-icon-view-sort-reversed garbage`), a single malformed value makes the affected directory **unopenable**: Nautilus crashes every time the user navigates back to it.

## Root cause

In `src/nautilus-file.c`, `nautilus_file_get_boolean_metadata()`:

```c
else
{
    g_error ("boolean metadata with value other than true or false");
    return default_metadata;   // ← unreachable, g_error aborts first
}
```

The function already had the correct fallback (`return default_metadata`) in place — only the abort was wrong.

## Fix

Replace `g_error()` with `g_warning()`. The invalid value is now logged for debugging while the function falls back to the caller-supplied default, matching the existing pattern for `value == NULL`.

The offending value is included in the warning to aid diagnosis.

```diff
-       g_error ("boolean metadata with value other than true or false");
+       g_warning ("boolean metadata with value other than true or false: %s", value);
        return default_metadata;
```

## Test

Added regression test `test_file_metadata_bool_invalid_returns_default` in `test/displayless/test-file-metadata.c`. It writes a non-boolean string into a boolean metadata key and asserts that:

- `nautilus_file_get_boolean_metadata(file, key, TRUE)` returns `TRUE`
- `nautilus_file_get_boolean_metadata(file, key, FALSE)` returns `FALSE`

Before the fix this test would abort the test process with `SIGABRT` on the first call. With the fix it passes cleanly.

### Reproducer from the issue (now harmless)

```bash
DIR="$(mktemp -d)"
gio set -t string "$DIR" metadata::nautilus-icon-view-sort-reversed garbage
nautilus "$DIR"   # Before: SIGABRT.  After: directory opens normally, warning logged.
```

## Checklist

- [x] The fix matches the existing fallback pattern (`value == NULL` → `return default_metadata`)
- [x] No public API changes
- [x] Regression test added that reproduces the original crash
- [x] Commit message follows the [GNOME commit message handbook](https://handbook.gnome.org/development/commit-messages.html)
- [x] `Closes #4323` included so the issue auto-closes on merge
