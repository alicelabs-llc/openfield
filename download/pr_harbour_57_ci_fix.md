## Summary

CI is currently red on PR #57. Root cause: rstest 0.19 changed the macro import path.

This patch:
- Switches from `use rstest::rstest;` to `use rstest;` + `#[rstest::rstest]` (fully qualified — works on both 0.18 and 0.19)
- Loosens Cargo.toml version constraint to `>=0.18, <0.20` so both versions work

Verified locally on both rstest 0.18.2 and 0.19.0. This should turn CI green and unblock the merge.
