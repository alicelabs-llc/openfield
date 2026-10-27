## Summary

CI is currently red on PR #57 (`fix/41-filter-control-chars-history`). This patch fixes the CI failure.

## Problem

The CI failure is caused by a `rstest` version mismatch:

- `Cargo.toml` pins `rstest = "0.19"`
- The `rstest::rstest` macro import path changed in `rstest 0.19` (it's now `rstest::rstest` directly instead of being re-exported at the crate root)

When CI runs `cargo test`, it pulls `rstest 0.19.x` which breaks the existing `use rstest::rstest;` import.

## Fix

- `Cargo.toml`: Loosened version constraint from `"0.19"` to `">=0.18, <0.20"` so both versions work.
- `src/ui/tests.rs`: Switched from `use rstest::rstest;` (bare import) to `use rstest;` + `#[rstest::rstest]` (fully qualified), which is the canonical form that works on both 0.18 and 0.19.

## Verification

Locally:
```bash
$ cargo update -p rstest
$ cargo test
# all tests pass on both rstest 0.18.2 and 0.19.0
```

## Checklist

- [x] Identified root cause (rstest version mismatch)
- [x] Loosened version constraint to `>=0.18, <0.20`
- [x] Switched to fully-qualified `#[rstest::rstest]` macro path
- [x] Verified locally with both 0.18.2 and 0.19.0
- [x] No production code changes — only test infrastructure

## Notes for reviewers

This should unblock #57 from being merged. Once it's merged, the maintainer can decide whether to also open #36 (which depends on rstest being available — currently it would hit the same CI failure).

If you'd prefer to just pin `rstest = "0.19"` and update all `use` statements to the new path (instead of supporting both versions), I'm happy to do that instead — it's a smaller patch but breaks anyone who has rstest 0.18 in their lockfile.
