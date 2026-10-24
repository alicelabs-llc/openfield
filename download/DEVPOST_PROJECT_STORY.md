# Devpost Project Story — alethech-agent-vault
# GitLab Transcend "Life After Code" Hackathon

> Copy-paste the **entire block below** into the "Project Story" Markdown editor on Devpost
> (the editor on the left of the screenshot — "Project details" page).
> The 7 section headers (Inspiration → What's next) are already in the template; replace
> each section's body with the text under each `##` heading here.

---

## Inspiration

AI coding agents are now writing commits, opening MRs, and answering reviewers on GitLab — but they're still treated as black boxes. When an agent proposes a 200-line diff at 3 AM, you have two bad options: trust the LLM and ship it, or block everything and lose the time you were supposed to save. Both are unsafe at scale.

I've been running my own agentic automation for a few weeks (PR reviewers, dep updaters, doc regenerators). The pattern that broke me wasn't hallucination — it was **trust drift**. By the third night, you stop reading the diffs because they "look reasonable." That's when agents go off the rails and you don't notice until a customer files a bug.

GitLab Transcend asks what "life after code" looks like. My answer: **life after code is verifiable or it doesn't ship.** The agent runs; the human verifies a single hash. That's the project.

## What it does

`alethech-agent-vault` is a FastAPI orchestrator that runs an AI agent inside a locked-down Docker sandbox, and signs every plan, code execution, and sandbox block into a **tamper-evident provenance DAG** built on [alethech](https://github.com/eddyflores100-lang/alethech).

You submit a task on `/submit` ("review this MR", "audit these deps", "regenerate these docs"). The orchestrator:

1. Calls **GitLab Duo Agent Platform** to plan the task
2. Executes each step inside a Docker sandbox with `--network=none --read-only --memory=512m --cpus=0.5 --cap-drop=ALL --security-opt=no-new-privileges --rm --user=agent`
3. Captures every plan, tool call, output, and sandbox denial into an alethech DAG
4. Opens a GitLab MR with the proposed diff + a signed provenance summary
5. The human reviews the audit trail (or runs `alethech-verify`) in 30 seconds, approves, and ships

When you run verify:

```
✅ DAG verified. 4 commits, 1 evidence.
  - Plan (signed 03:14:01Z) ✓
  - Step 1: parse diff (signed 03:14:08Z) ✓
  - Step 2: identify risks (signed 03:14:15Z) ✓
  - Step 3: BLOCKED — pip install (signed 03:14:22Z) ✓
  - Step 4: synthesize review (signed 03:14:35Z) ✓

Chain head SHA-256: b7e3a1c4f8e9...
Recomputed head:    b7e3a1c4f8e9...
MATCH ✓
```

One SHA-256 walk. No LLM trust required.

## How we built it

- **FastAPI orchestrator** (`src/orchestrator/`) — plan → execute → retry loop, 3 attempts max
- **Docker sandbox** (`src/orchestrator/sandbox.py`) — wrapper around `docker run` with eight safety knobs
- **alethech provenance** (`src/orchestrator/provenance.py`) — wraps `alethech.commit()` and `alethech.evidence()` calls
- **GitLab integration** (`integrations/gitlab/`):
  - `webhook_bridge.py` — Flask receiver, HMAC verify of `X-Gitlab-Token`
  - `duo_extension.py` — GitLab Duo Agent Platform wrapper
  - `mr_creator.py` — opens MR with proposed diff + provenance summary, applies `Verified-by-alethech` label
  - `verify_cli.py` — `alethech-verify` CLI that produces a human-readable audit report
- **Tests** — 41 tests passing in 2.71s (10 orchestrator + 30 GitLab integration)
- **Slide deck** (`docs/gitlab-transcend-demo.html`) — 11-slide standalone HTML for the demo video

The **containment matrix** maps each attack class to the specific Docker flag that blocks it:

| Attack class | Sandbox control | What gets signed |
|---|---|---|
| Filesystem escape | `--read-only` rootfs, tmpfs on `/tmp` only | The denied write path |
| Network exfil | `--network=none` | The denied `socket.connect()` |
| Resource exhaustion | `--memory=512m --cpus=0.5` | The OOMKill event |
| Privilege escalation | `--cap-drop=ALL --security-opt=no-new-privileges` | The denied `setuid` |
| Persistent process | `--rm` | The container's exit timestamp |
| Arbitrary user | `--user=agent` | The denied `/etc/passwd` read |
| Time bombs | Per-task 60s timeout | The timeout + last-seen PC |
| Tool poisoning | Tool definitions hashed + pinned | The hash drift (if any) |

## Challenges we ran into

- **Webhook signature verification** had to use `hmac.compare_digest`, not `==`, to prevent timing attacks. The test suite explicitly covers the constant-time comparison.
- **Docker sandbox flag drift** between Docker Engine versions (1.13 vs 1.41+) — solved by pinning the API version in the test container.
- **GitLab Duo Agent Platform webhook delivery** required retry-with-backoff because GitLab can replay events; the `webhook_bridge` filters by action (open/reopen/update) to avoid duplicate orchestrator runs.
- **Mock mode for tests** — we didn't want CI to require a real Docker daemon or a real LLM endpoint, so every external dependency is mockable. The 41 tests run with zero network calls.
- **Time pressure** — built in two sprints: sprint 1 was the core orchestrator + alethech; sprint 2 was the full GitLab integration with 30 dedicated tests.

## Accomplishments that we're proud of

- **41 tests passing in 2.71s**, including 30 GitLab integration tests (webhook HMAC verify, MR creation, verify CLI output format)
- **8 attack classes explicitly mapped** to Docker flags — not just "we sandbox," but "this exact flag blocks this exact attack, and here's the signed evidence"
- **End-to-end verification** — from task submit to MR open to `alethech-verify` chain walk, all in one workflow
- **Honest mock mode** — the entire system runs locally with no LLM/Docker/cloud dependencies for testing, which made the 41-test suite tractable in CI
- **Real shipped artifacts** — GitHub repo at [github.com/eddyflores100-lang/alethech-agent-vault](https://github.com/eddyflores100-lang/alethech-agent-vault), GitLab mirror at [gitlab.com/eddyflores100/alethech-agent-vault](https://gitlab.com/eddyflores100/alethech-agent-vault)

## What we learned

- **Tamper-evidence is cheap; trust is expensive.** Adding a hash-linked commit per step costs ~5ms; rebuilding trust after a hallucinated diff costs an incident postmortem. The ROI is obvious in hindsight.
- **`--cap-drop=ALL` is non-negotiable.** Anything less and you're running an LLM with `CAP_SYS_ADMIN`, which is a problem the moment the agent's prompt is poisoned.
- **`hmac.compare_digest`** instead of `==` for signature checks — small detail, big difference if someone is brute-forcing the webhook secret.
- **GitLab Duo Agent Platform** has a surprisingly clean webhook contract; the hardest part was filtering the right `action` field to avoid duplicate runs.
- **Test-driven security.** Most "we sandbox the agent" claims have zero tests for the sandbox itself. Writing `test_sandbox.py` first forced every flag to be deliberate, not aspirational.

## What's next for alethech-agent-vault (Verifiable Agents on GitLab Duo)

- **Multi-step agent plans with branching** — currently the DAG is linear; next iteration supports conditional branches (`if risk detected → request human review` becomes a `branch_commit` in the DAG)
- **GitLab Pages export of the provenance DAG** — every MR gets a static HTML audit report rendered from `.aleth` exports, no Python required to view
- **Beyond code: agent-managed environments** — Terraform plan changes, Kubernetes manifest diffs, and Docker Compose updates all flowing through the same `commit → verify → approve` pipeline
- **Cross-agent verification** — agent A signs its plan, agent B (different LLM) signs its critique of agent A's plan, human reviews both — chained attestation
- **Production deployment** — Vultr VM with persistent SQLite-backed task store (currently in-memory for hackathon scope)

---

## Notes for the rest of the Devpost form

### Project name
`alethech-agent-vault (Verifiable Agents on GitLab Duo)`

### Short tagline / pitch (the 1-line field above Project Story)
`Sandboxed AI agents on GitLab Duo with tamper-evident provenance — verify the chain, not the LLM.`

### Tags (Devpost allows up to 4)
`gitlab`  ·  `ai-agents`  ·  `security`  ·  `provenance`

### Project URL (the public repo field)
- Primary (GitLab, required by hackathon): `https://gitlab.com/eddyflores100/alethech-agent-vault`
- Mirror (GitHub): `https://github.com/eddyflores100-lang/alethech-agent-vault`

### Demo video URL
(You'll paste the YouTube Unlisted link here after recording the 3-min walkthrough of `docs/gitlab-transcend-demo.html`)

### Built With (the checkbox list on Devpost)
- Python
- Docker
- FastAPI
- GitLab Duo
- alethech (tamper-evident logging)
- Flask (webhook bridge)

### Custom questions (if Path B / Supervised / Stages fields appear below Project Story)
- **Track / Path:** Path B — Agentic Engineering (supervised approval gate before merge)
- **Level of Autonomy:** Supervised — agent plans and executes, human approves every MR before merge
- **Stages Covered:** Plan → Sandbox Execute → Capture Provenance → Open MR → Human Approval → Merge
