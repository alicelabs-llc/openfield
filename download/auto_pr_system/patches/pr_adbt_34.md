## Summary

Closes #34.

Bumps three GitHub Actions used in CI/release workflows to versions that run on Node 24, ahead of the Node 16/20 deprecation in 2026-Q4.

## Changes

| Action | Before | After | Release notes |
|--------|--------|-------|---------------|
| `actions/checkout` | `@v4` | `@v5` | https://github.com/actions/checkout/releases/tag/v5.0.0 |
| `actions/setup-go` | `@v5` | `@v6` | https://github.com/actions/setup-go/releases/tag/v6.0.0 |
| `goreleaser/goreleaser-action` | `@v6` | `@v7` | https://github.com/goreleaser/goreleaser-action/releases/tag/v7.0.0 |

Also bumps the Go CI matrix from `1.22.x - 1.24.x` to `1.23.x - 1.25.x` (drops 1.22 which is EOL, adds 1.25).

## Verification

- Read all three release notes — no breaking changes for our usage (we don't use any of the deprecated options).
- Ran `act -j release` locally — all steps complete successfully.
- `go test ./...` passes on Go 1.23, 1.24, and 1.25 locally.

## Files changed

- `.github/workflows/release.yml` — 3 action bumps
- `.github/workflows/ci.yml` — 2 action bumps + matrix update
- `README.md` — updated Go version compatibility table

## Checklist

- [x] Read release notes for all 3 actions — confirmed no breaking changes
- [x] Bumped actions in release.yml + ci.yml
- [x] Updated Go matrix to drop 1.22, add 1.25
- [x] Updated README compatibility table
- [x] Verified locally with `act -j release`

## Notes for reviewers

The `setup-go` bump also includes a small behavior change: the `check-latest` flag defaults to `true` in v6 (was `false` in v5). This is desirable for us — we always want the latest patch version of the Go toolchain.
