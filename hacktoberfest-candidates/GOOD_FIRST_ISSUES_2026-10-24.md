# Hacktoberfest 2026 — Good-First-Issue Research for @eddyflores100-lang

Generated: 2026-10-24 (UTC). Source: GitHub REST/Search API + local `hacktoberfest-candidates/` clones.
Goal: 5+ new PRs for portfolio/CV (2026 Hacktoberfest is no longer PR-count based, but PRs still valuable).

---

## 1. Existing PR status (verified live via GitHub API)

| PR | Repo | Issue | Title | State | Mergeable | Updated | Notes |
|----|------|-------|-------|-------|-----------|---------|-------|
| [#37](https://github.com/Ergane-Foundation/vajra/pull/37) | Ergane-Foundation/vajra | #29 | fix: skip Linux installer when starting on macOS | **MERGED** 2026-10-17 | — | 17d ago | Merged by @NamanmeetSingh. ✅ |
| [#57](https://github.com/Ishannaik/harbour/pull/57) | Ishannaik/harbour | #41 | fix: filter control characters in push_history | **OPEN** | `unstable` (CI red) | 1d ago | 4 comments + 1 review. **Needs attention — CI is failing.** |
| [#48](https://github.com/Ergane-Foundation/adbt/pull/48) | Ergane-Foundation/adbt | #35 | fix: pin GoReleaser to v2 in the release workflow | **OPEN** | `clean` (ready) | 1d ago | 1 comment. Waiting on maintainer merge. |
| [#554](https://github.com/NovaCode37/Prism-platform/pull/554) | NovaCode37/Prism-platform | — | — | **DOES NOT EXIST** | — | — | ⚠️ 404 on both `/pulls/554` and `/issues/554`; search for the user's PRs in this repo returns 0. Either deleted/closed-without-merge or wrong number. **No active PR to Prism-platform currently.** |
| [#124](https://github.com/meetdino/dino/pull/124) | meetdino/dino | — | Declare rust-version = 1.88 in the workspace package | **MERGED** 2026-10-07 | — | 17d ago | ✅ |

> Bonus found in history: an **additional open PR** to **Vayz0001/polyfarmer #115** ("fix: sanitize user-entered market URLs before resolving") — currently open.

---

## 2. Repos where @eddyflores100-lang has ALREADY contributed (so excluded from "new" pool)

Pulled the user's full PR history (100 most recent PRs). Relevant to target list: **none** of the 12 listed Python repos have been touched yet — all are fresh opportunities. Already-touched repos (from the candidate folder + others): Ergane-Foundation/vajra, Ergane-Foundation/adbt, Ishannaik/harbour, Vayz0001/polyfarmer, meetdino/dino, and **flisk-sh/flisk** (merged #951 — see rename note below).

### ⚠️ Two target repos have been renamed/transferred
- `nexB/scancode-toolkit` → **`aboutcode-org/scancode-toolkit`** (301 redirect). New location has **0** open unassigned 2026 good-first-issues → not viable right now.
- `tdk-landscape/tdk-cli-core` → **`flisk-sh/flisk`** (301 redirect). You already have a **merged PR (#951)** there. flisk currently has **130** open hacktoberfest-labeled good-first-issues, **but they are all <7 days old** (the project is being actively triaged right now) → violates the "last activity >7d" rule. **Revisit flisk in ~1 week** (e.g. #1960 "cli: rename test-support runTdk and tdkBin helpers to flisk" — easy, tests).

> `astral-sh/uv` is **Rust**, not Python — keep that in mind (it's high-profile but #17512 is an investigation/debugging task = medium).

---

## 3. Filter rules applied
- ✅ Issue is OPEN and UNASSIGNED (or assigned but stale >30 days)
- ✅ Created in 2026
- ✅ No `wontfix` / `invalid` / `duplicate` / `spam` label
- ✅ Last activity >7 days ago (idle ≥ 7d) so we don't intrude on active discussion
- ✅ Repo has CONTRIBUTING.md / contributor guide (accepts external PRs) — verified locally for all candidate-folder repos; mainstream for the external ones
- ✅ No anti-AI / "no LLM" policy in CONTRIBUTING — scanned all candidate-folder CONTRIBUTING files; **no anti-AI policy found** (tdk-cli-core is explicitly AI-friendly with "one-click AI review buttons"). polyfarmer has a quality bar: *trivial typo-only PRs are marked invalid/spam; every code change must add/update tests.*

### Per-repo candidate pool (2026, open, unassigned, after filters)

| Repo | Lang | Open eligible | Notes |
|------|------|---------------|-------|
| collective/icalendar | **Python** | 25 | 🏆 richest Python pool; many hacktoberfest-labeled |
| Vayz0001/polyfarmer | Rust | 30 | user has open PR #115; "one issue/contributor" rule |
| Ergane-Foundation/adbt | Go | 21 | user has open PR #48 (clean/mergeable) |
| Ishannaik/harbour | Rust | 18 | user has open PR #57 (CI red) |
| Ergane-Foundation/vajra | **Python**+bash | 6 | user already merged #37 — trusted contributor |
| zulip/zulip | Python | 2 hw | both <7d old (active) — revisit later |
| internetarchive/openlibrary | **Python** | 2 | |
| wger-project/wger | **Python** | 1 | |
| pwndbg/pwndbg | **Python** | 1 hw | |
| astral-sh/uv | Rust | 1 hw | medium investigation |
| home-assistant/core | Python | 1 | assigned to maintainer (allenporter), only 12d stale → skip |
| BlitzKraft/saythanks.io | Python | 1 | assigned, 54d stale; it's a 504/infra bug → marginal |
| scrapy/scrapy / keephq/keep / Avaiga/taipy | Python | 0 | no 2026 unassigned gfi/hw |
| NovaCode37/Prism-platform | Python | 0 | no eligible issues right now |
| aboutcode-org/scancode-toolkit (ex nexB) | Python | 0 | renamed; no eligible issues |

---

## 4. Recommended candidates (14 across 7 repos)

Difficulty legend: **T**=trivial, **E**=easy, **E-M**=easy-medium, **M**=medium.

### 🐍 Python — primary picks (best fit for your strength)

#### 1. collective/icalendar #1868 — Suppress warnings in test run  ·  **E**  ·  Python
- URL: https://github.com/collective/icalendar/issues/1868
- Created 2026-10-02 · updated 2026-10-02 (idle 22d) · unassigned · `good first issue`
- Fix: `uv run pytest` emits warnings (notably `GloballyUniqueTZIDGuessed` in `src/icalendar/prop/dt/types.py:107`); add a `filterwarnings` config / silence-or-fix the vendor-prefix guess so the test run is clean.
- Why you: pure Python/pytest hygiene — exactly your wheelhouse; self-contained.

#### 2. collective/icalendar #1921 — get() for StrEnum  ·  **E**  ·  Python
- URL: https://github.com/collective/icalendar/issues/1921
- Created 2026-10-13 · updated 2026-10-13 (idle 11d) · unassigned · `good first issue`
- Fix: `PARTSTAT("no-value")` raises `ValueError`; add a `StrEnum.get(value)` classmethod that returns `None` for unknown values instead of raising.
- Why you: tiny, well-defined enum API addition with a clear acceptance example in the issue body.

#### 3. collective/icalendar #1802 — [TYPING] TZP.localize and TZP.localize_utc  ·  **E**  ·  Python
- URL: https://github.com/collective/icalendar/issues/1802
- Created 2026-09-16 · updated 2026-09-22 (idle 32d) · unassigned · `good first issue`
- Fix: outdated type hints — both methods should accept `date | datetime | time` (date/datetime → datetime, time → time) and set the timezone; make the typing consistent across all combinations.
- Why you: Python typing pass — high signal-to-noise for a CV PR (typing/protocol correctness).

#### 4. collective/icalendar #1840 — PARTSTAT & other enums should accept case-insensitive values  ·  **E-M**  ·  Python
- URL: https://github.com/collective/icalendar/issues/1840
- Created 2026-09-28 · updated 2026-10-02 (idle 22d) · unassigned · `feature, good first issue`
- Fix: make case-insensitive enums accept lowercase so `PARTSTAT("needs-action") == PARTSTAT("NEEDS-ACTION") == PARTSTAT.NEEDS_ACTION`.
- Why you: real RFC-5545 compliance fix with a concrete acceptance test in the body — good portfolio story.

#### 5. collective/icalendar #1784 — Create ACTION enum  ·  **E-M**  ·  Python
- URL: https://github.com/collective/icalendar/issues/1784
- Created 2026-09-14 · updated 2026-09-14 (idle 40d) · unassigned · `good first issue`
- Fix: introduce a proper `ACTION` enum (AUDIO/DISPLAY/EMAIL/PROCEDURE) following the existing enum pattern in `icalendar.enums`.
- Why you: idiomatic Python enum work; complements #1921/#1840 if you want to do a focused "enums" series in one repo.

#### 6. internetarchive/openlibrary #13648 — Restrict "What work is this an edition of?" to super librarians/admins  ·  **E-M**  ·  Python (Django)
- URL: https://github.com/internetarchive/openlibrary/issues/13648
- Created 2026-09-16 · updated 2026-10-06 (idle 18d) · unassigned · `Good First Issue`, Lead: @cdrini
- Fix: gate the "What work is this an edition of?" edit field behind super-librarian/admin permission (the field is frequently misused).
- Why you: high-impact, well-known OSS project (Internet Archive); clear permission-scope change, Django. Maintainer lead already assigned to triage (@cdrini).

#### 7. wger-project/wger #2205 — Pre-select weight units  ·  **E-M**  ·  Python (Django) + optional Flutter
- URL: https://github.com/wger-project/wger/issues/2205
- Created 2026-02-20 · updated 2026-06-01 (idle 145d) · unassigned · `good first issue`
- Fix: default the routine weight unit to the user's profile `weight_unit` (web/Django part is the easy half; Flutter is optional).
- Why you: cleanly scoped Django feature; long-idle (no active discussion); you can ship the web-only portion.

#### 8. pwndbg/pwndbg #3805 — improve `heap` command output  ·  **M**  ·  Python
- URL: https://github.com/pwndbg/pwndbg/issues/3805
- Created 2026-02-28 · updated 2026-05-03 (idle 174d) · unassigned · `help wanted, feature, heap`
- Fix: reformat the `heap` command so each chunk is exactly one line (current formatting is "bad").
- Why you: real-world Python debugging-tooling PR (pwndbg is widely used by security folks); medium because output formatting touches heap-walking internals — but the acceptance criterion ("one line per chunk") is crisp.

### 🔧 Candidate-folder follow-ups (you already have a foothold — good for fast 2nd PRs)

#### 9. Ergane-Foundation/vajra #15 — Add tests for eve.json alert parsing + severity mapping  ·  **E**  ·  Python (pytest + fixtures)
- URL: https://github.com/Ergane-Foundation/vajra/issues/15
- Created 2026-10-06 · updated 2026-10-06 (idle 18d) · unassigned · `good first issue, hacktoberfest, area: tests`
- Fix: test `SOAREngine._parse_eve_alert` and `KafkaBridge._map_severity` against fixture eve.json lines (severities 1–4 → critical/high/medium/low; missing severity → medium). Files: `new tests/unit/test_eve_parsing.py`, `new tests/fixtures/eve/`, `src/vajra/soar/engine.py`, `src/vajra/pipeline/kafka_bridge.py`.
- Why you: you already merged a PR into vajra (#37) so you're a known/trusted contributor — fast review likely. Pure test addition = low risk.

#### 10. Ergane-Foundation/vajra #18 — Run shellcheck on the scripts and add it to CI  ·  **E**  ·  bash / CI
- URL: https://github.com/Ergane-Foundation/vajra/issues/18
- Created 2026-10-06 · updated 2026-10-06 (idle 18d) · unassigned · `good first issue, hacktoberfest, area: scripts, area: ci`
- Fix: `shellcheck -S warning` over `scripts/*.sh`, `scripts/dpdk/*.sh`, `tests/perf/*/run_*.sh`, `tools/benchmark/run_benchmark.sh`; fix or inline-disable with a reason; add a shellcheck step to CI.
- Why you: your merged vajra PR #37 was exactly a bash/installer fix — this is a natural, on-brand follow-up.

#### 11. Ergane-Foundation/adbt #34 — Update GitHub Actions to versions that run on Node 24  ·  **E**  ·  Go / YAML CI
- URL: https://github.com/Ergane-Foundation/adbt/issues/34
- Created 2026-10-06 · updated 2026-10-06 (idle 18d) · unassigned · `good first issue, area/ci, hacktoberfest`
- Fix: bump `actions/checkout@v4`, `actions/setup-go@v5`, `goreleaser/goreleaser-action@v6` in `.github/workflows/release.yml` to latest majors; check release notes for breaking changes.
- Why you: you already have a clean/mergeable PR (#48) open in adbt — a second small CI PR keeps momentum with the same maintainer. (Different issue from #35/#48.)

#### 12. Ergane-Foundation/adbt #39 — Add tests for parseLsLine and FormatFileSize  ·  **E**  ·  Go (table-driven tests)
- URL: https://github.com/Ergane-Foundation/adbt/issues/39
- Created 2026-10-06 · updated 2026-10-06 (idle 18d) · unassigned · `good first issue, area/ci, hacktoberfest`
- Fix: table-driven tests in `internal/adb/files.go` covering files, folders, symlinks, names-with-spaces, short lines (Android `ls -la` parsing differs across versions).
- Why you: pure test addition (low risk) and you're already familiar with the adbt codebase.

#### 13. Ishannaik/harbour #36 — theme: support 8-digit and 4-digit hex color parsing in parse_hex  ·  **E-M**  ·  Rust
- URL: https://github.com/Ishannaik/harbour/issues/36
- Created 2026-10-05 · updated 2026-10-05 (idle 19d) · unassigned · `good first issue, hacktoberfest`
- Fix: extend `parse_hex` in `src/theme.rs` to accept `#rgba` (4-digit) and `#rrggbbaa` (8-digit); extract RGB (discard/blend alpha); informative `Err` for other lengths; add unit tests; keep existing theme tests green.
- Why you: you already have a Rust PR (#57) into harbour — single-function, well-scope= d follow-up. (Different issue from #41/#57.)

#### 14. Ishannaik/harbour #4 — Add a buffer-snapshot test for the settings overlay  ·  **E**  ·  Rust (tests)
- URL: https://github.com/Ishannaik/harbour/issues/4
- Created 2026-10-05 · updated 2026-10-05 (idle 19d) · unassigned · `good first issue, hacktoberfest, tests`
- Fix: add a snapshot test in `src/ui/tests.rs` for `src/ui/settings.rs` (follow the `search_snapshot_idle_with_results` pattern — plain string snapshots, not `insta`).
- Why you: pure test-addition easy win in a repo you're already active in.

---

## 5. Suggested execution order (to land 5+ PRs fast)

1. **collective/icalendar #1868** (E, Python/pytest) — fastest, cleanest first PR in a brand-new high-profile Python repo.
2. **collective/icalendar #1921** (E, Python enum) — same repo, batch a second PR while context is fresh.
3. **Ergane-Foundation/vajra #15** (E, Python tests) — you're a trusted contributor here → fastest review.
4. **Ergane-Foundation/adbt #34** (E, CI) — quick win, builds on your existing adbt PR #48 momentum.
5. **internetarchive/openlibrary #13648** (E-M, Django) — high-prestige repo for the portfolio.
6. (stretch) **collective/icalendar #1802** or **#1840** — round out a Python-typing/enums series.
7. (stretch) **harbour #36** or **#4** — keep your Rust streak going (but first unblock harbour #57 CI).

---

## 6. Caveats & next actions

- **harbour PR #57 CI is red** (`mergeable_state: unstable`). Before opening more harbour PRs, push a fix so the maintainer isn't juggling two red PRs from the same author. Re-check `/repos/Ishannaik/harbour/pulls/57` after pushing.
- **adbt PR #48 is clean/mergeable** — just waiting on the maintainer; a polite nudge comment is reasonable.
- **Prism #554 does not exist** — confirm with the user whether the number was a typo or the PR was deleted. Prism-platform currently has **0 eligible 2026 good-first-issues**, so it's not a viable new-PR source right now (skip it this cycle).
- **polyfarmer**: you already have open PR #115, and its CONTRIBUTING enforces *"one issue per contributor"* + *"every code change must add/update tests"*. Land #115 first; then pick a **code+test** issue like #24 (snap_to_tick unit test) or #31 (invalid-session-cookie integration test) — **avoid doc-only PRs there** (they're marked invalid/spam).
- **flisk (renamed tdk-cli-core)**: 130 hacktoberfest issues, all <7d fresh — revisit ~Nov 1. You already merged #951 there, so it's a known-friendly repo.
- **Anti-AI policy**: none found in any candidate-folder CONTRIBUTING. polyfarmer's rule is about *quality* (no trivial typo PRs, tests required), not anti-AI.
- **Rate limits**: this research was done unauthenticated (no `gh`/token in the sandbox). If you re-run, add a `GITHUB_TOKEN` to lift the 60→5000 req/h limit.
- **Did NOT open any PRs** — research only, per instructions. Comment-claim the chosen issue on GitHub before starting (vajra/icalendar/adbt/harbour all ask you to comment to claim).
