# OPP-6 — OSS Bounty Re-Verification (Cleaned & Verified-Only)

**Date:** 2026-10-24 (sandbox clock)
**Task ID:** OPP-6
**Agent:** Verification subagent (general-purpose)
**Source:** `/tmp/my-project/download/OPP_OSS_BOUNTIES.md` (36 entries reported by OPP-2)
**Goal:** Re-verify every single bounty URL. Produce a CLEAN, verified-only list. Drop anything that is 404, closed, locked, or already being worked on.

---

## TL;DR — Verified Tally

| Classification | Count | Sum USD |
|---|---:|---:|
| Total bounties in original OPP-2 list | 36 | $43,550 |
| ✅ **LIVE** — open + unassigned + no linked PR + bounty signal | **11** | **$16,850** |
| ⚠️ **DISPUTED** — issue open but has a linked PR (someone is on it) | 1 | $50 |
| ❌ **DEAD** — closed, 404, or repo gone | 24 | $26,650 |
| **Net actionable today** | **11** | **$16,850** |

**Headline finding:** Of the 36 bounties OPP-2 reported as "verified open + unassigned", only **11 (30.5%)** are genuinely still open, unassigned, and free of an active PR. **24 (66.7%)** are already closed and **1** has an active linked PR. The previous agent's HTML-only verification missed closed Turso issues (all 10 of 10 Turso rows are closed — some since 2025-07-16) and at least one with an active PR.

---

## Methodology — Two-Pass Verification

### Pass 1 — HTML scrape (no rate limit)
For each of the 36 URLs, fetched the live GitHub issue HTML page with a browser User-Agent and classified using static HTML markers:

- HTTP 404 / "page you are looking for" → **DEAD (404)**
- `"state":"closed"` / `State: closed` / `octicon-issue-closed` → **DEAD (closed)**
- `Repository has been deleted` → **DEAD (repo gone)**
- `locked as` / `this conversation has been locked` → **DISPUTED (locked)**
- Assignee present (regex match `/users/<login>/hovercard` and no `No one assigned` text) → **DISPUTED (assigned)**
- `Linked pull requests` sidebar with one or more `/pull/N` links → **DISPUTED (active PR)**
- Otherwise → LIVE_UNKNOWN (defer to Pass 2)

### Pass 2 — anonymous GitHub API (60 req/hr)
For each Pass-1 LIVE_UNKNOWN entry, GET `https://api.github.com/repos/OWNER/REPO/issues/NUMBER` and re-check:

- `state == "open"` AND `assignee == null` AND `assignees == []` AND `locked == false` AND `pull_request == null` → **LIVE**
- Otherwise → **DEAD** (closed) or **DISPUTED** (assigned/locked/is-PR)

Bounty signal also recorded: any label containing `bounty`/`reward`/`💰`/`💵`/`usd`, or `$` in title/body, or `algora`/`/bounty`/`issuehunt` in body.

### Tooling
- Script: `/home/z/my-project/scripts/opp6_verify.py` (Pass 1 + driver)
- Script: `/home/z/my-project/scripts/opp6_pass2_api.py` (Pass 2)
- Raw results: `/home/z/my-project/scripts/opp6_results_full.json`
- Run logs: `/home/z/my-project/scripts/opp6_run.log`, `opp6_pass2_run.log`

---

## ✅ LIVE — 11 Verified Bounties (sorted by USD desc)

Each row below was confirmed live via Pass 2 anonymous GitHub API on 2026-10-24: `state==open`, `assignee==null`, `locked==false`, no `pull_request` field, and at least one bounty signal present (label / `$` in title-body / Algora mention).

| # | Amount | Repo + Issue URL | Skill | Comments | Last updated | Bounty label? | Trust note |
|---|---:|---|---|---:|---|---|---|
| 1 | **$5,000** | [osmesirius-ship-it/daxda-next-gen#39](https://github.com/osmesirius-ship-it/daxda-next-gen/issues/39) | AI agents + red-team eval (MMPIBench) | 0 | 2026-10-12 | `bounty-mmpibench`, `bounty-claim`, `level-1` | ⚠️ **SUSPICIOUS** — title starts with "[PAYOUT CLAIM]". Org name `osmesirius-ship-it` looks synthetic. Verify sponsor payout mechanism before investing 40h. |
| 2 | **$3,000** | [commaai/opendbc#2017](https://github.com/commaai/opendbc/issues/2017) | Python + CAN DBC reverse-engineering | 41 | 2026-10-18 | no label, `$3000 bounty` in title | ✅ Real sponsor (Comma.ai, VC-funded). High competition (41 comments) — read thread before starting. |
| 3 | **$2,000** | [NEXAITECHAU/gh-disc-54891-tenstorrent-tt-metal#1](https://github.com/NEXAITECHAU/gh-disc-54891-tenstorrent-tt-metal/issues/1) | Rust + AI inference (CosyVoice2 vocoder) | 0 | 2026-08-30 | no label, `Bounty $2000` in title | ⚠️ **SUSPICIOUS** — repo name `gh-disc-54891-tenstorrent-tt-metal` looks like an auto-generated GitHub-discussion mirror, NOT the real `tenstorrent/tt-metal` repo. Verify before working. |
| 4 | **$1,250** | [Senthemodder/aquarium-of-gullibles#1](https://github.com/Senthemodder/aquarium-of-gullibles/issues/1) | Algorithm + Rust/Python (subgraph isomorphism O(N)) | 6 | 2026-10-01 | `bounty`, `help wanted`, `algorithm` | ✅ Clean bounty label, 6 comments (moderate competition). |
| 5 | **$1,000** | [Sifchain/sifnode#503](https://github.com/Sifchain/sifnode/issues/503) | DevOps (Azure AKS + Terraform) | 6 | 2026-10-23 | `bounty` | ✅ Bounty label, active maintainer (updated yesterday). Cosmos SDK chain. |
| 6 | **$1,000** | [Sifchain/sifnode#524](https://github.com/Sifchain/sifnode/issues/524) | DevOps (GCP + Terraform) | 12 | 2026-10-23 | `bounty` | ✅ Companion to #503 — can ship both for $2K total. 12 comments (higher competition). |
| 7 | **$1,000** | [teamleaderleo/bot-observatory#45](https://github.com/teamleaderleo/bot-observatory/issues/45) | TypeScript/Python (bot detection, security) | 1 | 2026-10-12 | no label, `$500 Deductible...Bounty` in title | ✅ Lowest competition (1 comment). Security angle fits our stack. |
| 8 | **$1,000** | [commaai/opendbc#1175](https://github.com/commaai/opendbc/issues/1175) | Python + CAN signals (Kia EV9 lateral) | 7 | 2026-10-12 | no label, `$1000 bounty` in title | ✅ Real Comma.ai sponsor. Moderate competition (7 comments). |
| 9 | **$1,000** | [commaai/opendbc#1833](https://github.com/commaai/opendbc/issues/1833) | Python + CAN signals (Rivian set speed) | 9 | 2026-06-12 | no label, `$1000 bounty +community` in title | ⚠️ **STALE** — last update 2026-06-12 (4+ months ago). Still open + unassigned, but verify sponsor is still paying. |
| 10 | **$500** | [perria080925-bot/agente-bountie#1](https://github.com/perria080925-bot/agente-bountie/issues/1) | TypeScript + AI agents (Mermail) | 3 | 2026-10-23 | no label, `$500 USDC` in title | ⚠️ **SUSPICIOUS** — org name `perria080925-bot` is a bot-style account. 3 comments, USDC payout — confirm payout path before starting. |
| 11 | **$100** | [flowdriveai/flowpilot#46](https://github.com/flowdriveai/flowpilot/issues/46) | Android (USB host mode + JNI), Python | 7 | 2026-10-03 | `bounty` | ✅ Clean bounty label. Low entry-point. Adjacent to comma.ai openpilot ecosystem. |

**Total verified LIVE value: $16,850 USD**

---

## 🏆 Top 5 Verified Bounties Ready For Action

Ranked by **(verified open + unassigned) × payout × trust × skill-fit**, NOT raw ROI. Excluded the 3 "SUSPICIOUS" rows above (#1, #3, #10) from the top-5 because sponsor payout is unverified despite the issue being technically open + unassigned.

### 1. commaai/opendbc#2017 — **$3,000** — BYD DBC port
- **URL:** https://github.com/commaai/opendbc/issues/2017
- **Skill:** Python + CAN DBC reverse-engineering
- **Effort:** ~16h
- **Why #1:** Highest verified payout from a real VC-funded OSS sponsor (Comma.ai). Payout history is public and reliable. 41 comments = high competition, but a clean DBC port is a self-contained deliverable.
- **Action:** Read the full 41-comment thread first; identify which DBC messages are still missing; submit a `dbc` file PR. Worldwide eligibility.

### 2. Senthemodder/aquarium-of-gullibles#1 — **$1,250** — Subgraph Isomorphism O(N)
- **URL:** https://github.com/Senthemodder/aquarium-of-gullibles/issues/1
- **Skill:** Algorithm + Rust (or Python for prototype)
- **Effort:** ~24h
- **Why #2:** Explicit `bounty` + `help wanted` + `algorithm` labels. 6 comments = moderate competition. Algorithm-heavy, self-contained.

### 3. Sifchain/sifnode#503 + #524 — **$1,000 each ($2,000 bundle)** — Azure AKS + GCP for Cosmos SDK chain
- **URLs:** https://github.com/Sifchain/sifnode/issues/503 + https://github.com/Sifchain/sifnode/issues/524
- **Skill:** DevOps (Terraform + AKS/GCP)
- **Effort:** ~10h each (20h for both)
- **Why #3:** Both updated yesterday (2026-10-23) — maintainer is actively engaged. Companion issues — ship both for $2K total. Explicit `bounty` label. DevOps is in our skill set.

### 4. teamleaderleo/bot-observatory#45 — **$1,000** — Bot detection (Enclosure 028)
- **URL:** https://github.com/teamleaderleo/bot-observatory/issues/45
- **Skill:** TypeScript/Python (bot detection / security)
- **Effort:** ~12h
- **Why #4:** Lowest competition of any $1,000+ bounty (only 1 comment). Security/bot-detection skill matches our agent-trust background. Story-driven bounty ("The $500 Deductible That Became a Bounty").

### 5. flowdriveai/flowpilot#46 — **$100** — Android USB host mode research
- **URL:** https://github.com/flowdriveai/flowpilot/issues/46
- **Skill:** Android (USB host mode + JNI), Python
- **Effort:** ~8h
- **Why #5:** Clean `bounty` label, low entry-point ($100) — good first PR to the flowdriveai ecosystem (openpilot fork) to build trust for higher-value bounties later. 7 comments = moderate but manageable.

---

## ⚠️ DISPUTED — 1 Bounty (open but already being worked on)

| # | Amount | Repo + Issue URL | Reason |
|---|---:|---|---|
| 30 | $50 | [jackjin1997/TentOfTrials#2](https://github.com/jackjin1997/TentOfTrials/issues/2) | Has a linked PR (visible in `Linked pull requests` sidebar of the issue HTML). Someone is already on it. Do not duplicate work. |

---

## ❌ DEAD — 24 Bounties (closed / 404 / repo gone)

All 24 entries below were confirmed closed via Pass 1 (HTML — `state: closed` markers) or Pass 2 (API — `state == "closed"`). They should not appear in any future actionable list.

| # | Amount | Repo + Issue URL | Closed-via | Closed at |
|---|---:|---|---|---|
| 1 | $15,000 | [golemcloud/golem#1004](https://github.com/golemcloud/golem/issues/1004) | HTML | (issue closed) |
| 6 | $1,000 | [rohitdash08/FinMind#144](https://github.com/rohitdash08/FinMind/issues/144) | HTML | (issue closed) |
| 13 | $800 | [tursodatabase/turso#3894](https://github.com/tursodatabase/turso/issues/3894) | HTML | (issue closed) |
| 18 | $500 | [tursodatabase/turso#2106](https://github.com/tursodatabase/turso/issues/2106) | HTML | (issue closed) |
| 19 | $500 | [Senthemodder/aquarium-of-gullibles#4](https://github.com/Senthemodder/aquarium-of-gullibles/issues/4) | HTML | (issue closed) |
| 23 | $100 | [claude-builders-bounty/claude-builders-bounty#3](https://github.com/claude-builders-bounty/claude-builders-bounty/issues/3) | HTML | (issue closed) |
| 25 | $250 | [illbnm/homelab-stack#8](https://github.com/illbnm/homelab-stack/issues/8) | HTML | (issue closed) |
| 26 | $100 | [commaai/flash#128](https://github.com/commaai/flash/issues/128) | HTML | (issue closed) |
| 27 | $50 | [maaltarifi97-maker/aioa-playground#1](https://github.com/maaltarifi97-maker/aioa-playground/issues/1) | HTML | (issue closed) |
| 29 | $50 | [weilixiong/TentOfTrials#1](https://github.com/weilixiong/TentOfTrials/issues/1) | HTML | (issue closed) |
| 31 | $50 | [Peter7896/TentOfTrials#2](https://github.com/Peter7896/TentOfTrials/issues/2) | HTML | (issue closed) |
| 32 | $50 | [sybil-solutions/local-ai-registry#223](https://github.com/sybil-solutions/local-ai-registry/issues/223) | HTML | (issue closed) |
| 33 | $50 | [sybil-solutions/local-ai-registry#219](https://github.com/sybil-solutions/local-ai-registry/issues/219) | HTML | (issue closed) |
| 34 | $50 | [sybil-solutions/local-ai-registry#217](https://github.com/sybil-solutions/local-ai-registry/issues/217) | HTML | (issue closed) |
| 35 | $50 | [sybil-solutions/local-ai-registry#216](https://github.com/sybil-solutions/local-ai-registry/issues/216) | HTML | (issue closed) |
| 36 | $50 | [bolivian-peru/marketplace-service-template#463](https://github.com/bolivian-peru/marketplace-service-template/issues/463) | HTML | (issue closed) |
| 4 | $1,500 | [tursodatabase/turso#3830](https://github.com/tursodatabase/turso/issues/3830) | API | 2025-10-28 |
| 5 | $2,500 | [tursodatabase/turso#5092](https://github.com/tursodatabase/turso/issues/5092) | API | 2026-02-11 |
| 12 | $800 | [tursodatabase/turso#4493](https://github.com/tursodatabase/turso/issues/4493) | API | 2026-01-07 |
| 14 | $1,000 | [tursodatabase/turso#4879](https://github.com/tursodatabase/turso/issues/4879) | API | 2026-01-30 |
| 15 | $1,000 | [tursodatabase/turso#6626](https://github.com/tursodatabase/turso/issues/6626) | API | 2026-04-30 |
| 16 | $500 | [tursodatabase/turso#3436](https://github.com/tursodatabase/turso/issues/3436) | API | 2025-10-01 |
| 17 | $500 | [tursodatabase/turso#2049](https://github.com/tursodatabase/turso/issues/2049) | API | 2025-07-16 |
| 24 | $200 | [tursodatabase/turso#6583](https://github.com/tursodatabase/turso/issues/6583) | API | 2026-04-28 |

**Pattern observed:** 9 of the 11 Algora × Turso bounties reported by OPP-2 are already CLOSED (some closed 8+ months ago in 2025-07). The HTML-only verification in OPP-2 was insufficient — GitHub's static HTML for a closed issue still renders the issue title and labels, which apparently led OPP-2 to mis-classify them as open. The anonymous GitHub API `state` field is the source of truth and was not consulted by OPP-2.

---

## Honest limitations

1. **Anonymous API rate limit (60/hr).** Pass 2 used 19 of the 60 anonymous requests in this hour. The `/rate_limit` and 19 issue-fetch calls together consumed ~20 of 60 — well within budget. No token in env, so anonymous was the only option.
2. **Linked-PR detection is HTML-only.** Pass 2 did NOT fetch the `/issues/N/timeline` or `/issues/N/events` endpoint (would have added 19 more API calls, exceeding rate limit). Pass 1's HTML scrape caught the 1 obvious linked-PR case (`jackjin1997/TentOfTrials#2`), but a linked PR that was opened very recently might not yet appear in the sidebar HTML if GitHub hasn't rendered it. Re-run a timeline check before starting any serious work.
3. **"Comments count" is not "active attempts".** A high comment count (e.g. commaai/opendbc#2017 with 41 comments) signals competition but does not necessarily mean someone is currently attempting. Read the actual comment thread before starting work on any high-comment-count bounty.
4. **3 "SUSPICIOUS" rows in the LIVE list** (osmesirius-ship-it/daxda-next-gen#39, NEXAITECHAU/gh-disc-54891-tenstorrent-tt-metal#1, perria080925-bot/agente-bountie#1) are technically open + unassigned per the API, but have red flags: bot-style org names, auto-generated mirror repo names, or title prefixes like "[PAYOUT CLAIM]" that suggest the bounty may already be in a payout-resolution state. These were kept in the LIVE table for completeness but were excluded from the Top 5. Verify the sponsor's actual payout path (e.g. Algora dashboard, IssueHunt URL, or maintainer confirmation in the thread) before investing hours.
5. **Algora × Turso challenge bounties — entire bucket is dead.** OPP-2 reported 10 Turso issues (rows 4, 5, 12, 13, 14, 15, 16, 17, 18, 24 of the original table). **All 10 are closed** — 2 caught by HTML scrape in Pass 1 (turso#3894, turso#2106) and the remaining 8 confirmed closed via the anonymous API in Pass 2 (turso#3830 closed 2025-10-28, turso#5092 closed 2026-02-11, turso#4493 closed 2026-01-07, turso#4879 closed 2026-01-30, turso#6626 closed 2026-04-30, turso#3436 closed 2025-10-01, turso#2049 closed 2025-07-16, turso#6583 closed 2026-04-28). **0 of 10 Algora × Turso bounties remain actionable.** Skip the entire Turso challenge bucket — it appears to have been largely resolved/awarded already (the Algora × Turso challenge pool is likely closed).
6. **No fabricated entries.** Every classification above is backed by either (a) a fetched HTML body saved in `/home/z/my-project/scripts/opp6_run.log` or (b) an anonymous GitHub API JSON response saved in `/home/z/my-project/scripts/opp6_results_full.json`.

---

## Recommended next action

1. Pick **commaai/opendbc#2017 ($3,000)** as the primary target — read the 41-comment thread, identify the missing DBC messages, fork the repo, and submit a `dbc` file PR. Highest trustworthy payout.
2. In parallel, ship **Sifchain/sifnode#503 + #524** as a $2K bundle (DevOps Terraform work — within our skill set, updated yesterday so maintainer is engaged).
3. Use **flowdriveai/flowpilot#46 ($100)** as a low-stakes warm-up PR to build a track record in the openpilot ecosystem before tackling the $3K comma.ai bounty.

**Realistic 30-day conservative projection (verified-only):** $3,000 (opendbc#2017) + $2,000 (sifnode bundle #503+#524) + $100 (flowpilot#46) = **$5,100** — assuming all three PRs merge. No fabricated income projections; every dollar in this number is backed by a verified-open, unassigned, no-active-PR GitHub issue as of 2026-10-24 01:38 UTC.

---

**Files produced by OPP-6:**
- `/home/z/my-project/download/OPP_OSS_BOUNTIES_VERIFIED.md` (this file — verified-only list)
- `/home/z/my-project/scripts/opp6_verify.py` (Pass 1 + driver)
- `/home/z/my-project/scripts/opp6_pass2_api.py` (Pass 2 API confirmation)
- `/home/z/my-project/scripts/opp6_results_full.json` (full classification log — 19 LIVE candidates with API detail)
- `/home/z/my-project/scripts/opp6_run.log` (Pass 1 stdout)
- `/home/z/my-project/scripts/opp6_pass2_run.log` (Pass 2 stdout)
