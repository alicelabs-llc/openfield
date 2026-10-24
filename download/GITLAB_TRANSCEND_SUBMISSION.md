# GitLab Transcend — Life After Code Submission Package

**Deadline:** October 27, 2026 @ 1:00pm UTC (3 days from Oct 24)
**Track:** Path B — Bring Your Own (existing MIT-licensed OSS project)
**Autonomy level:** Supervised (agent proposes, user approves outcome)
**Project name:** alethech-agent-vault — Verifiable Agent Execution on GitLab Duo
**Ecuador eligible:** ✅ (not in exclusion list: Brazil, China, Quebec, Russia, Cuba, Iran, North Korea, Syria, Crimea, Donetsk, Luhansk)
**Prize target:** Best Supervised Agent (Path B) — $4,000 USD

---

## SUBMISSION TEXT (paste into Devpost "text description" field)

### Project Title
**alethech-agent-vault: Verifiable Agent Execution on GitLab Duo**

### What I Built

I extended `alethech-agent-vault` — an open-source agent runner that sandboxes execution and signs every step into a tamper-evident DAG — to integrate with **GitLab Duo Agent Platform** for supervised, post-code automation. The agent runs as a GitLab CI/CD pipeline stage that:

1. **Listens for triggers** — webhook from MR creation, scheduled pipeline, or manual trigger
2. **Plans the work** — using GitLab Duo to generate a structured plan (file changes, test updates, doc regen) from the MR description
3. **Executes each step inside a Docker sandbox** — `--network=none --read-only --memory=512m --cpus=0.5 --cap-drop=ALL --security-opt=no-new-privileges --rm --user=agent`
4. **Captures every tool call, output, and retry attempt into a tamper-evident provenance DAG** — signed with [alethech](https://github.com/eddyflores100-lang/alethech)'s commit/evidence API
5. **Opens a Supervised approval gate** — GitLab MR with the proposed changes + the signed provenance chain as an artifact
6. **On approval** — commits land in the target branch with a `Verified-by-alethech` GitLab MR label; on rejection — provenance log retained for audit

The key novelty: **the agent's plan, every tool call, every sandbox block, and the final approval decision are written to an append-only signed DAG.** A reviewer doesn't have to trust the LLM. They walk the DAG, verify hashes, and see exactly what the agent tried — including the things the sandbox stopped.

### How I Built It

- **Foundation:** `alethech-agent-vault` (existing MIT project — https://github.com/eddyflores100-lang/alethech-agent-vault) — FastAPI orchestrator + Docker sandbox + alethech provenance
- **GitLab Duo integration:** Custom Duo Agent Platform extension that wraps the orchestrator's `submit` endpoint as a GitLab CI stage
- **Webhook bridge:** Lightweight Flask service that translates GitLab MR webhooks → orchestrator `/submit` calls
- **MR templating:** GitLab MR template with embedded provenance summary (commit hashes, evidence count, sandbox blocks)
- **Verification CLI:** `alethech-verify` — walks the DAG for a given MR and produces a human-readable audit report

### Levels of Autonomy — why Supervised

I picked **Supervised** as the primary submission because it's the level where the trust question gets sharp: the human approves the outcome, but the agent did many intermediate steps they didn't see. That's *exactly* the scenario where tamper-evident provenance earns its keep — the human can't review every intermediate step, but they CAN verify the provenance chain in seconds.

A secondary Hands-off configuration is also included (the agent runs on a schedule with no human in the loop) but the Supervised config is the canonical submission because it's the most honest about where verifiable execution matters.

### Open Source Repository (Path B: original project)

- **Original MIT-licensed project:** https://github.com/eddyflores100-lang/alethech-agent-vault
- **License:** MIT
- **Lines of code:** 1,318 (initial scaffold, Oct 23 2026)
- **Tests:** 11 passing (5 provenance + 6 routes)
- **GitLab mirror:** will be created at https://gitlab.com/eddyflores100-lang/alethech-agent-vault (public, MIT)

### Deployed Project URL

- **Live demo:** Will deploy to Google Cloud Run for bonus points (TBD URL by Oct 26)
- **Architecture diagram:** see `docs/ARCHITECTURE.md` in the repo
- **Demo video:** YouTube link will be added by Oct 26

### Demo Video Script (3 minutes)

[0:00] "Hi, I'm Edison. This is a submission for GitLab Transcend, Life After Code, in the Supervised autonomy level. The project is alethech-agent-vault — a verifiable agent runner."

[0:15] **Setup** — Show GitLab MR with a feature request: "Add SHA-256 fingerprinting to all tool definitions."

[0:30] **Trigger** — Webhook fires, agent picks up the MR.

[0:45] **Plan** — GitLab Duo generates a structured plan: modify `tools.py`, add `fingerprint()`, update tests.

[1:00] **Sandboxed execution** — Agent runs each step in a Docker container with `--network=none --read-only`. Show the container constraints.

[1:20] **Containment moment** — Agent tries `subprocess.Popen("pip install ...")` to "self-improve" — sandbox blocks network. Show the red warning box lighting up. Show the `EvidenceCommit` row appearing in `provenance.log`.

[1:45] **Approval gate** — GitLab MR opens with the proposed diff + provenance summary. Show the `Verified-by-alethech` label, the commit count (1 plan + 3 tool calls + 1 block + 1 retry), the SHA-256 chain head.

[2:10] **Verification** — Run `alethech-verify <MR-id>` — walk the DAG, print the audit report. Every step verified.

[2:30] **Approval** — Human reviews the audit (30 seconds, not 30 minutes), approves. Commits land.

[2:45] **Why this matters** — "Slow the agent down. Sandbox its blast radius. Sign everything. Then Supervised autonomy is just a sustainable operating mode — not a leap of faith."

[3:00] End. Link to repo + alethech library.

---

## ARCHITECTURE DIAGRAM (for Devpost upload)

Save the following as `docs/gitlab-transcend-architecture.png` (render the ASCII art or recreate):

```
┌─────────────────────────────────────────────────────────────────────┐
│ GitLab MR webhook (created/updated)                                 │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Webhook Bridge (Flask)                                              │
│ - Validates GitLab signature                                       │
│ - Translates MR payload → orchestrator /submit                     │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Orchestrator (FastAPI — alethech-agent-vault)                       │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ 1. Plan (GitLab Duo Agent Platform)                             │ │
│ │    - structured plan: file changes, tests, docs                │ │
│ └─────────────────────┬───────────────────────────────────────────┘ │
│                       ▼                                             │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ 2. Execute step in sandbox                                      │ │
│ │    Docker: --network=none --read-only --memory=512m           │ │
│ │           --cpus=0.5 --cap-drop=ALL --security-opt              │ │
│ │           =no-new-privileges --rm --user=agent                  │ │
│ └─────────────────────┬───────────────────────────────────────────┘ │
│                       │                                             │
│                       ▼                                             │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ 3. Capture output + alethech.commit(memory_type, content)        │ │
│ │    - signs the step into the tamper-evident DAG                 │ │
│ └─────────────────────┬───────────────────────────────────────────┘ │
│                       │                                             │
│                       ▼                                             │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ 4. Repeat for each plan step                                    │ │
│ │    - retry up to 3 times on failure                            │ │
│ │    - unsafe patterns → EvidenceCommit (signed before block)    │ │
│ └─────────────────────┬───────────────────────────────────────────┘ │
└───────────────────────┼─────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────────┐
│ Supervised Approval Gate                                            │
│ - GitLab MR opens with proposed diff                               │
│ - provenance.log attached as artifact                               │
│ - alethech-verify produces human-readable audit report              │
│ - label: Verified-by-alethech                                       │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
              ┌────────────┴───────────┐
              │                        │
              ▼                        ▼
        [HUMAN APPROVES]         [HUMAN REJECTS]
              │                        │
              ▼                        ▼
      Commits land             Provenance log
      in target branch         retained for audit
```

---

## TODO CHECKLIST (next 3 days)

- [ ] **Oct 24 evening** — Mirror repo to GitLab.com (public, MIT)
- [ ] **Oct 24 evening** — Implement GitLab webhook bridge (Flask, ~100 lines)
- [ ] **Oct 24 evening** — Implement GitLab Duo Agent Platform extension
- [ ] **Oct 25** — Implement `alethech-verify` CLI for GitLab MR audit
- [ ] **Oct 25** — Write 5 end-to-end tests for the GitLab integration
- [ ] **Oct 25** — Deploy to Google Cloud Run (for bonus points)
- [ ] **Oct 26** — Record 3-minute demo video
- [ ] **Oct 26** — Upload video to YouTube (public, unlisted-OK)
- [ ] **Oct 26** — Final review of submission text
- [ ] **Oct 27 before 13:00 UTC** — SUBMIT on Devpost

---

## NOTES FOR JUDGES

- **Stage One (pass/fail baseline):** Project is functional, theme fit is "post-code automation" via GitLab Duo (agent automates post-MR work).
- **Technological Implementation:** Docker sandbox + alethech provenance + GitLab Duo + GitLab MR API + Google Cloud Run deployment.
- **Design:** Minimal UI, focus on audit trail visibility. The "containment moment" (sandbox block) is the visual centerpiece.
- **Potential Impact:** Every team running AI agents on GitLab CI needs verifiable execution. This is a reference implementation.
- **Innovation:** Combining provenance DAGs with supervised agent execution is novel — most agent frameworks treat provenance as optional logging, here it's the trust boundary.
- **Presentation:** 3-min demo shows the actual containment moment + verification walk.
- **Google Cloud bonus:** Deploy on Cloud Run + Artifact Registry.

---

## FILES TO CREATE IN REPO

```
alethech-agent-vault/
├── integrations/
│   └── gitlab/
│       ├── __init__.py
│       ├── webhook_bridge.py       # Flask webhook receiver
│       ├── duo_extension.py        # GitLab Duo Agent Platform extension
│       ├── mr_template.md          # MR template with provenance summary
│       └── verify_cli.py           # alethech-verify CLI
├── tests/
│   ├── test_gitlab_webhook.py
│   ├── test_duo_extension.py
│   ├── test_verify_cli.py
│   ├── test_e2e_gitlab_flow.py
│   └── test_containment_moment.py
├── deploy/
│   ├── gcp_cloudrun.yaml            # Google Cloud Run deploy config
│   └── Dockerfile.webhook          # Image for webhook bridge
├── docs/
│   ├── gitlab-transcend-submission.md  # This file
│   └── gitlab-transcend-architecture.png  # Render of ASCII diagram
└── README.md  (updated with GitLab integration section)
```

---

## SUBMISSION URL (after publishing on Devpost)

TBD — fill in after submission
