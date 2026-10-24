---
title: "I let an AI agent do my overnight chores — but every step is signed so I can prove it didn't go rogue"
published: true
description: "How I built a slow-but-verifiable agent runner with sandboxed execution + tamper-evident provenance, so I can sleep while the agent works and audit it in the morning."
tags: [devchallenge, hf26challenge, hacktoberfest, showdev]
canonical_url: "https://github.com/eddyflores100-lang/alethech-agent-vault"
---

> *Submission for the [Hacktoberfest Open-Source AI Challenge Week 3: Slow and Steady](https://dev.to/challenges/hacktoberfest-week3-2026). The theme: open-source AI that rewards laziness.*

## The lazy thesis

Most "agentic" demos I see on Twitter fall into two buckets:

1. **Fast and loud** — agents that spin up 50 tools, browse the web, send Slack DMs, and post PRs while you watch in real time. Cool demo. Three days later you realize one of them pushed a `console.log` to production.
2. **Slow but invisible** — agents that "think for an hour" and return a paragraph. You have no idea what they actually did. You just trust the output.

Neither is lazy in the way I want to be lazy. I want option three: **let the agent run overnight, doing real work — code review, dependency bumps, security audits, doc regeneration — and in the morning I get a signed audit trail proving nothing sketchy happened.** No "trust me bro." No "the model said it was fine." A cryptographic receipt.

So I built one. It's called [`alethech-agent-vault`](https://github.com/eddyflores100-lang/alethech-agent-vault). Open source under MIT.

## What it does, in one paragraph

You submit a task ("review this PR for security issues", "regenerate the OpenAPI docs from the spec", "audit our deps for known CVEs and propose patches"). The orchestrator plans it, executes the steps **inside a Docker sandbox** with `--network=none --read-only --memory=512m --cpus=0.5 --cap-drop=ALL`, and writes every step (the plan, the tool calls, the tool outputs, the LLM's retry attempts, the sandbox blocks) into a tamper-evident DAG using [alethech](https://github.com/eddyflores100-lang/alethech). When you wake up, you open `provenance.log` and see: 03:14 — agent tried to `os.system("rm -rf /tmp/*")` — sandbox blocked — evidence signed `sha256:b7e3…`. You verify the chain. You go get coffee.

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

The containment moment — the part that makes this not-a-toy — is when the agent's plan includes something like `os.system("rm -rf /tmp/*")` or `socket.connect("evil.example.com")`. The sandbox blocks it. The block is captured as an `EvidenceCommit` and signed. You don't just see "agent failed." You see *exactly* what it tried, with a hash you can verify.

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

## The "rewards laziness" part

Here's the trick: the laziness isn't *my* laziness. It's the laziness of *not having to babysit*. Most agent frameworks I've worked with require either (a) me watching the output stream in case it goes sideways, or (b) me trusting that the framework's "safety guardrails" did their job. Both suck. (a) is not lazy. (b) is lazy in the wrong way — the "I'm too lazy to verify, so I'll just trust it" way.

`alethech-agent-vault` rewards a different kind of lazy: the kind where I can run the agent for 8 hours overnight, wake up, verify the provenance chain in 30 seconds, and *then* read what it actually did. The verification is cheap (one SHA-256 walk over the DAG). The agent's work is preserved. I am lazy in the right direction.

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

## Why this matters for the ecosystem

We're entering a phase where agents are going to run unattended. Not "AI safety" in the abstract — concrete unattended execution: PR reviewers running nightly, dependency updaters running weekly, doc generators running after each merge. The question is not *whether* they will run unattended — they will. The question is *whether you'll be able to verify what they did*.

If the answer is "I'll just look at the LLM output," you're back to trust-me-bro. If the answer is "I'll watch it in real time," you've invented a worse version of being a junior engineer's manager.

`alethech-agent-vault` is my bet on a third path: **slow the agent down, sandbox its blast radius, and sign everything.** Then laziness is just a sustainable operating mode.

---

*I'm [@eddyflores100-lang on GitHub](https://github.com/eddyflores100-lang). The repo is MIT. The [alethech provenance library](https://github.com/eddyflores100-lang/alethech) is also MIT. If you're working on agent safety / sandboxing / MCP / verifiable execution, I'd love to talk — ping me on the issue tracker.*

*This post is part of Hacktoberfest Week 3: Slow and Steady. See the [challenge page](https://dev.to/challenges/hacktoberfest-week3-2026) for other submissions — there's some genuinely cool stuff coming in this week.*
