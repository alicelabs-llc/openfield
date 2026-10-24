---
title: "I let an AI agent do my overnight chores — but every step is signed so I can prove it didn't go rogue"
published: true
description: "How I built a slow-but-verifiable agent runner with sandboxed execution + tamper-evident provenance, so I can sleep while the agent works and audit it in the morning."
tags: [devchallenge, hf26challenge, hacktoberfest, showdev]
canonical_url: "https://github.com/eddyflores100-lang/alethech-agent-vault"
---

> *Submission for the [Hacktoberfest Open-Source AI Challenge Week 3: Slow and Steady](https://dev.to/challenges/hacktoberfest-week3-2026). The theme: open-source AI that rewards laziness.*

## What I Built

I built [`alethech-agent-vault`](https://github.com/eddyflores100-lang/alethech-agent-vault) — an open-source agent runner that sandboxes execution and signs every step into a tamper-evident DAG. The lazy thesis: let the agent run overnight doing real work (PR review, dependency bumps, doc regen), and in the morning you get a cryptographic receipt proving nothing sketchy happened.

You submit a task. The orchestrator plans it, executes the steps inside a Docker sandbox (`--network=none --read-only --memory=512m --cpus=0.5 --cap-drop=ALL --security-opt=no-new-privileges --rm --user=agent`), and writes every step — the plan, the tool calls, the tool outputs, the LLM's retry attempts, the sandbox blocks — into a tamper-evident DAG using [alethech](https://github.com/eddyflores100-lang/alethech). When you wake up, you open `provenance.log` and see: `03:14 — agent tried os.system("rm -rf /tmp/*") — sandbox blocked — evidence signed sha256:b7e3…`. You verify the chain. You go get coffee.

## What effort it saves

It saves the *babysitting* effort. Most agent frameworks I've worked with require either (a) watching the output stream in case it goes sideways, or (b) trusting that the framework's "safety guardrails" did their job. Both are bad. (a) is not lazy. (b) is lazy in the wrong way — the "I'm too lazy to verify, so I'll just trust it" way.

`alethech-agent-vault` saves the verification effort. I can run the agent for 8 hours overnight, wake up, verify the provenance chain in 30 seconds (one SHA-256 walk over the DAG), and *then* read what it actually did. The agent's work is preserved. The verification is cheap. I am lazy in the right direction.

## Demo

The full demo script lives in [`docs/DEMO_SCRIPT.md`](https://github.com/eddyflores100-lang/alethech-agent-vault/blob/main/docs/DEMO_SCRIPT.md), but here's the 90-second walkthrough:

**Step 1 — Submit a task.** `POST /submit` with `{"task": "review this PR for security issues", "context": "<diff>"}`. The orchestrator generates a `task_id` (uuid4) and returns it.

**Step 2 — Agent plans.** The LLM (via OpenAI-compatible endpoint, mock mode for tests, Vultr Serverless Inference for real runs) generates a structured plan: "1. Parse diff, 2. Identify risk patterns, 3. Run semgrep on suspected files, 4. Synthesize review."

**Step 3 — Agent executes (sandboxed).** Each plan step runs inside a Docker container with the constraints above. The container is `--rm`'d on exit. No persistent state.

**Step 4 — The containment moment.** ⚡ On test prompt #3 ("audit this code and improve it"), the agent tries `subprocess.Popen("pip install better-auditor", shell=True)` to "self-improve". The sandbox blocks network egress. The block is captured as an `EvidenceCommit`:

```
[EvidenceCommit] tool=subprocess.Popen
  input: "pip install better-auditor"
  output: docker.exceptions.ContainerError: exit 1, stderr="network unreachable"
  signed: sha256:b7e3a1c4...
  ts: 2026-10-24T03:14:22Z
```

The web UI shows a red warning box. The provenance DAG grows a new node.

**Step 5 — Verification.** `alethech-verify <task_id>` walks the DAG, recomputes every hash, and prints:

```
✓ DAG verified. 4 commits, 1 evidence.
  - Plan (signed 03:14:01Z) ✓
  - Step 1: parse diff (signed 03:14:08Z) ✓
  - Step 2: identify risks (signed 03:14:15Z) ✓
  - Step 3: BLOCKED — pip install (signed 03:14:22Z) ✓
  - Step 4: synthesize review (signed 03:14:35Z) ✓
```

You read the audit, decide the block was legitimate (it was — the agent tried to fetch untrusted code), approve the rest, and the synthesized review lands in your MR.

## Why Open Innovation Matters for This Project

This project literally could not exist as a closed-source tool. Three reasons:

**1. The trust boundary is the source code.** A proprietary "agent safety" tool that says "trust us, we verify everything" is just another trust-me-bro. The only way the verification claim is meaningful is if the verifier's source is auditable. The alethech library, the orchestrator, the sandbox wrapper — all MIT, all on GitHub. If you don't trust my hash walk, you can read the 162-line `provenance.py` and write your own.

**2. The threat model is community-shaped.** The 8 attack classes I enumerated (filesystem escape, network exfil, resource exhaustion, privilege escalation, persistent process, arbitrary user, time bombs, tool poisoning) didn't come from a single vendor's docs. They came from reading what actual agent operators have been hit by — the prompt-injection-via-tool-output attacks documented by Anthropic, the MCP tool poisoning writeups, the GitHub Security Lab findings on agentic CI runners. Open disclosure of attack patterns is the only way the defense side keeps up.

**3. The compositional surface requires open spec.** alethech-agent-vault calls three open-source things: FastAPI, Docker, and the OpenAI-compatible API spec (which Vultr Serverless Inference implements). It exposes one open thing: an MCP server (when I ship that part). Open specs on both sides mean anyone can swap any component — Vultr → OpenAI, OpenAI → Ollama, Ollama → LM Studio — and the provenance contract still holds. That's only possible because the contract itself is open.

If this were closed, every integration would be a vendor negotiation. With it open, every integration is a PR. That's the difference between "a safety tool" and "a safety standard."

## Built with GitHub Copilot

The codebase was developed with [GitHub Copilot](https://github.com/features/copilot) as the pairing tool. Specific places where Copilot's suggestions materially shaped the implementation:

- `src/orchestrator/sandbox.py` — Docker container constraint enumeration. Copilot suggested the full `--cap-drop=ALL --security-opt=no-new-privileges` combo from a comment listing the attack classes I wanted to defend against.
- `src/orchestrator/provenance.py` — the `commit()` and `evidence()` API shapes. Copilot's autocomplete correctly predicted the JCS canonicalization pattern before I wrote it out.
- `tests/test_sandbox.py` — the parameterized fixture for "given this unsafe input, expect this block." Copilot wrote the parametrize decorator + first 3 cases after I wrote the test for `rm -rf`.

I mention this not as a "look how productive I am" flex, but because it's a relevant data point for the agentic future this hackathon is about: the same agents that I'm building defenses against are the agents I'm coding with. The defense needs to be one step ahead, not by being cleverer, but by being *verifiable*. Copilot wrote code; alethech signs it; the sandbox constrains its runtime behavior. Each layer is open; each layer composes.

## The "Slow and Steady" fit

The challenge rewards *laziness done right*. My take: **slow and steady wins the race because the agent that runs slow (sandboxed, capped, retry-bounded) and steady (every step signed into an append-only DAG) is the only one you can actually leave running while you sleep.**

The fast-and-loud agents are fun to watch. They are not fun to wake up to.

## Architecture (15-second version)

```
┌─────────────────────────────────────────────────────────────┐
│   Orchestrator (FastAPI)                                    │
│   /submit  /status/{id}  /health                            │
│      │                                                       │
│      ├──► Plan (LLM call via Vultr Serverless Inference)   │
│      │        │                                              │
│      │        ▼                                              │
│      ├──► Execute step in sandbox (Docker)                  │
│      │        │   constraints: --network=none --read-only   │
│      │        │               --memory=512m --cpus=0.5       │
│      │        │               --cap-drop=ALL --security-opt  │
│      │        │               =no-new-privileges --rm        │
│      │        │               --user=agent                  │
│      │        ▼                                              │
│      ├──► Capture output (stdout, stderr, exit code)        │
│      │        │                                              │
│      │        ▼                                              │
│      └──► alethech.commit(memory_type, content)             │
│               │                                              │
│               ▼                                              │
│      Tamper-evident DAG of (plan → exec → result → retry)   │
└─────────────────────────────────────────────────────────────┘
```

## The containment matrix

I enumerated 8 attack classes an agent might try, and mapped each to a sandbox control:

| Attack class | Sandbox control | What gets signed |
|---|---|---|
| Filesystem escape | `--read-only` rootfs, tmpfs on `/tmp` only | The denied write path |
| Network exfil | `--network=none` | The denied `socket.connect()` |
| Resource exhaustion | `--memory=512m --cpus=0.5` | The OOMKill / CPU throttle event |
| Privilege escalation | `--cap-drop=ALL --security-opt=no-new-privileges` | The denied `setuid` syscall |
| Persistent process | `--rm` (container auto-removed on exit) | The container's exit timestamp |
| Arbitrary user | `--user=agent` (non-root, non-me) | The denied `/etc/passwd` read |
| Time bombs | Per-task timeout (60s) | The timeout + last-seen PC |
| Tool poisoning | Tool definitions hashed + pinned | The hash drift (if any) |

Every one of these becomes a row in `provenance.log`. If the agent tried three of them, you get three rows. If the agent tried none, you get zero rows and you can sleep easier.

## What's in the repo

- `src/orchestrator/sandbox.py` — Docker wrapper with all the safety knobs above, lazy-initialized so tests don't need a Docker daemon.
- `src/orchestrator/provenance.py` — alethech wrapper with `commit(memory_type, content)` + `evidence(tool, input, output)`. Falls back to in-memory DAG if alethech isn't installed.
- `src/orchestrator/agent.py` — plan→execute→retry loop (max 3 retries). Heuristics for unsafe patterns (`rm -rf`, `os.system`, `socket.connect`, etc.) — those get registered as `EvidenceCommit` before the sandbox even has to block them.
- `src/orchestrator/routes.py` — FastAPI with `/submit`, `/status/{task_id}`, `/health`.
- `src/web/index.html` — minimal UI, submit form + live audit trail + a red warning box that lights up when the sandbox blocks something.
- `tests/` — 11 tests, all passing locally in 1.9s. (Sandbox tests skip if Docker isn't available.)
- `docker-compose.yml` — one-command deploy on a Vultr VM.
- `docs/ARCHITECTURE.md` — full containment matrix + failure modes.
- `docs/DEMO_SCRIPT.md` — the 2-minute demo script (the "containment moment" the hackathon asked for).

## The honest limitations

- The LLM endpoint is currently mocked in tests. Real LLM calls happen via Vultr Serverless Inference (OpenAI-compatible API at `https://api.vultrinference.com/v1`). The plan is to switch the endpoint at kickoff (Nov 3 — see the [Vultr Agent Rush Hackathon](https://lablab.ai/ai-hackathons/vultr-hackathon)) and run real tasks.
- The unsafe-pattern heuristic is a regex list, not a model. It catches the obvious stuff (`rm -rf`, `socket.connect`, `subprocess.Popen` with shell injection vectors). It does NOT catch subtle prompt-injection-via-tool-output attacks. That's the next milestone.
- The provenance chain is signed with alethech's default key. For real production you'd want to bring your own keypair and rotate it.

## Try it

```bash
git clone https://github.com/eddyflores100-lang/alethech-agent-vault
cd alethech-agent-vault
cp .env.example .env
# fill in VULTR_INFERENCE_API_KEY (or leave blank for mock mode)
docker compose up
open http://localhost:8000
```

Submit a task. Watch the audit trail. Try to get the agent to misbehave (it will try `rm -rf` on the first few test prompts — it's almost cute).

---

*I'm [@eddyflores100-lang on GitHub](https://github.com/eddyflores100-lang). The repo is MIT. The [alethech provenance library](https://github.com/eddyflores100-lang/alethech) is also MIT. If you're working on agent safety / sandboxing / MCP / verifiable execution, I'd love to talk — ping me on the issue tracker.*

*This post is part of Hacktoberfest Week 3: Slow and Steady. See the [challenge page](https://dev.to/challenges/hacktoberfest-week3-2026) for other submissions — there's some genuinely cool stuff coming in this week.*
