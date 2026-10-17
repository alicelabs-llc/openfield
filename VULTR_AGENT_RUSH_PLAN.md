# Vultr: Agent Rush Hackathon — Project Plan

**Hackathon**: Vultr: Agent Rush Hackathon (lablab.ai × Vultr)
**Dates**: November 3-8, 2026 (6 days online; optional on-site Nov 8 in Salt Lake City, UT)
**URL**: https://lablab.ai/ai-hackathons/vultr-hackathon
**Prize pool**: $9,000 cash + $5,000 Vultr credits
- 🥇 1st: $5,000 + $3,000 credits
- 🥈 2nd: $3,000 + $1,000 credits
- 🥉 3rd: $1,000 + $1,000 credits
- Every participant: $200 in free Vultr credits

---

## The Challenge

**"Blast Radius Zero: Safe Agent Execution on Vultr"**

Build a web-based agent that performs **real work** — writing/running code OR operating a real browser — with every action **contained inside a sandbox running on Vultr**. The system acts as a centralized control layer: it plans a task, dispatches it to an isolated execution environment, and returns **verifiable output**.

> "An agent that only chats is a demo; an agent that executes safely is a product."

### Two execution patterns (build against one or both)

#### Pattern A — Sandboxed code execution
```
User asks → model writes code → code runs in container → real output returns → model explains it
```
On error, stderr is fed back for a retry. Example ideas:
- **CSV Analyst** — upload a spreadsheet, ask a question in plain English, get an actually-executed chart plus the code that produced it
- **Prove-It Code Reviewer** — paste a snippet or PR; agent runs it and its tests in the sandbox and reports what really happened
- **Chart Anything** — natural language in, executed matplotlib/plotly image out
- **File Fixer** — messy CSV or JSON in, cleaned file out, with an executed before/after diff
- **Self-Healing Runner** — agent runs code, reads the error, patches it, and retries (retry loop visible on screen)

#### Pattern B — Sandboxed browser use
```
User gives goal → model plans → Playwright in container → screenshots return → vision model verifies → repeat with human approval for final
```
Example ideas:
- **Comparison Shopper** — URLs in, screenshot-backed comparison table out
- **Form Filler** — structured data in, multi-step web form filled with screenshot trail and approve-before-submit gate
- **Site QA Sweep** — point at a web app, get back broken flows/links with screenshots
- **Research with Receipts** — brief where every claim links to a screenshot of its source
- **Page Watcher** — monitor listing/pricing pages, extract structured data, diff against yesterday

### What they're looking for

1. **Containment focus** — address real safety/reliability challenges; show how isolation makes autonomous execution shippable
   - Process isolation — execution never touches host or app runtime
   - Secret hygiene — no API keys/credentials inside the sandbox
   - Resource limits — time and memory caps on every run
   - Lifecycle discipline — reset or destroy environment after each task
2. **Production-ready web application**
   - Public web URL accessible
   - Real product-style experience
   - Clear user flows, not just a local demo
3. **Vultr as central backend** — Vultr powers execution and orchestration

### Technical requirements (REQUIRED)

1. **Vultr VM backend** — deploy backend on a Vultr VM, runs the whole loop
2. **Vultr Serverless Inference** — all agent LLM calls go through Vultr Serverless Inference (OpenAI-compatible API at `https://api.vultrinference.com/v1`). Vision-capable models available for screenshot reasoning.
3. **Sandbox boundary** — sandboxes run as containers or throwaway instances on Vultr, NEVER inside app process. Docker container strongly recommended. OpenSandbox, gVisor, E2B are starting points.
4. **Vultr API** (optional) — use to spin up throwaway instance per task and destroy after

### What to submit

- [ ] Public GitHub repository with setup and documentation
- [ ] Vultr VM backend deployment, agent LLM calls through Vultr Serverless Inference
- [ ] Public demo URL
- [ ] Recorded demo video (with one **containment moment** — sandbox absorbing something unsafe like `rm -rf`, infinite loop, or hostile web page)
- [ ] Clear explanation of architecture and use case

### Judging criteria

- **Application of Technology** — how effectively the chosen model(s) are integrated
- **Presentation** — clarity and effectiveness of project presentation
- **Business Value** — impact and practical value, fit into business areas
- **Originality** — uniqueness and creativity, ability to demonstrate behaviors

---

## Our Project: **"Alethech Agent Vault"** — Verifiable Agent Execution on Vultr

### The core insight

Most teams will build a sandbox and call it done. We add the missing piece: **cryptographic provenance for every action the agent takes**.

Every step the agent performs — code execution, browser action, retry loop, error recovery — is recorded as a **signed commit in an alethech DAG**. The result is a verifiable audit trail that proves:

- **What the agent did** (the exact code that ran / browser action taken)
- **When it did it** (timestamped, hash-chained)
- **Why it did it** (the LLM's reasoning, signed alongside the action)
- **What the sandbox allowed or blocked** (containment events are first-class commits, not logs that can be tampered with)

This is the perfect demo because:
1. **Fits "verifiable output"** — the hackathon explicitly asks for "verifiable output", not just output. We deliver cryptographic verification.
2. **Natural containment moment** — when the agent tries `rm -rf /` and the sandbox blocks it, alethech logs the attempt as a signed commit. The video shows the agent's hostile action ** cryptographically proven** in the audit trail.
3. **Differentiator** — alethech is your existing project (310+ commits, v0.9.5, MIT licensed, listed in MCP Registry). Most teams start from zero; we start with a working provenance layer.
4. **Business value** — enterprises deploying AI agents need audit trails for compliance (SOC 2, ISO 27001). Alethech delivers that out of the box.

### Architecture (high level)

```
┌─────────────────────────────────────────────────────────────┐
│  Web UI (Next.js / static HTML)                              │
│  - Submit task (CSV upload, code paste, URL)                 │
│  - Watch live execution feed                                 │
│  - View signed audit trail at the end                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  Agent Orchestrator (FastAPI on Vultr VM)                    │
│  1. Receive task                                             │
│  2. Call Vultr Serverless Inference (LLM plans steps)        │
│  3. Dispatch each step to sandbox                            │
│  4. Capture output (stdout, stderr, screenshot, files)      │
│  5. On error: feed stderr back to LLM, retry (max 3)        │
│  6. Sign every step via alethech commit                      │
│  7. Return final result + signed audit trail                 │
└────────────────┬────────────────────────────────────────────┘
                 │
       ┌─────────┴──────────┐
       ▼                    ▼
┌──────────────┐    ┌──────────────────────┐
│ Vultr         │    │ Sandbox (Docker       │
│ Serverless    │    │ container on Vultr VM │
│ Inference     │    │ or throwaway instance)│
│ (LLM)         │    │                       │
│               │    │ - runs user code      │
│ OpenAI-       │    │ - runs Playwright     │
│ compatible    │    │ - network-isolated   │
│               │    │ - resource-limited    │
│               │    │ - destroyed after use │
└──────────────┘    └──────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Alethech Store (local to Vultr VM)                         │
│  - Every agent action → EnrichedCompany-style commit        │
│  - Every sandbox event (allow/block/error) → EvidenceCommit │
│  - Hash-linked DAG, Ed25519-signed                          │
│  - Exportable as .aleth (encrypted portable container)     │
└─────────────────────────────────────────────────────────────┘
```

### Pattern we'll build: Pattern A (Sandboxed code execution) + a hint of B

**Concrete app: "Prove-It Code Runner with Receipts"**

User pastes code (Python snippet, PR diff, or a CSV analysis question). The agent:
1. Plans the execution approach (LLM call via Vultr Serverless Inference)
2. Wraps the code in a Docker container with resource limits (timeout 30s, 512MB RAM, no network)
3. Runs it on the Vultr VM via Docker
4. Captures stdout, stderr, exit code, generated files
5. If it errored: feeds stderr back to LLM, agent proposes a patch, retry (max 3)
6. Every step (plan, execute, error, retry, success) is signed via alethech
7. Final result: code output + a downloadable `.aleth` file with the full signed audit trail

**Containment moment in the demo video**: user submits `os.system("rm -rf /")` disguised as a "CSV cleanup script". The sandbox blocks it (Docker seccomp + read-only root). Alethech logs the blocked action as an EvidenceCommit — the agent's "intent" (the code it wrote before the sandbox caught it) is permanently recorded on the DAG, even though the action never executed. The user sees: "Agent attempted unsafe action. Evidence commit sha256:abc123. Click to view the signed record."

### Tech stack

- **Backend**: Python 3.12, FastAPI, runs on Vultr VM (Ubuntu 22.04)
- **LLM**: Vultr Serverless Inference (OpenAI-compatible, e.g. `gpt-4o` or `claude-sonnet-4-5` depending on what Vultr exposes — vision-capable model required for screenshot reasoning)
- **Sandbox**: Docker container with seccomp profile, network disabled, read-only rootfs, 512MB RAM, 30s timeout. Use `docker run --rm --network=none --memory=512m --cpus=0.5 --read-only --security-opt=no-new-privileges --cap-drop=ALL`
- **Browser (Pattern B optional)**: Playwright inside a separate Docker container with same restrictions
- **Provenance**: alethech (already MIT licensed, PyPI package `alethech==0.9.5`)
- **Frontend**: minimal Next.js or even static HTML + vanilla JS (focus on backend, not UI polish)

### File structure (repo)

```
alethech-agent-vault/
├── README.md                          # Setup, architecture, demo URL
├── docker-compose.yml                 # Orchestrator + sandbox base image
├── Dockerfile.orchestrator            # FastAPI backend image
├── Dockerfile.sandbox                 # Sandbox base image (Python + Playwright)
├── pyproject.toml                     # Python deps (alethech, fastapi, openai, docker)
├── requirements.txt
├── .env.example                       # VULTR_INFERENCE_API_KEY, ALETHECH_STORE_PATH, etc.
├── src/
│   ├── orchestrator/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app
│   │   ├── agent.py                   # LLM planning loop (calls Vultr Serverless Inference)
│   │   ├── sandbox.py                 # Docker container management (run, capture, destroy)
│   │   ├── provenance.py              # alethech wrapper: sign every step
│   │   └── routes.py                  # /submit, /status/{task_id}, /audit/{task_id}
│   └── web/
│       ├── index.html                 # Task submission form + live feed
│       └── app.js                     # SSE client for live execution updates
├── tests/
│   ├── test_sandbox.py                # Sandbox isolation tests (rm -rf blocked, network disabled)
│   ├── test_provenance.py             # alethech commit chain integrity
│   └── test_agent.py                  # LLM planning + retry loop (mocked LLM)
├── docs/
│   ├── ARCHITECTURE.md                # Architecture diagram + data flow
│   ├── CONTAINMENT.md                 # How the sandbox blocks each attack class
│   ├── DEMO_SCRIPT.md                 # Video script with containment moment
│   └── DEPLOYMENT.md                  # Vultr VM setup from scratch
└── scripts/
    ├── setup_vultr_vm.sh              # Provision Vultr VM, install Docker, clone repo
    └── demo.sh                        # End-to-end demo: submit safe task, then unsafe task
```

### Timeline

| When | Task |
|------|------|
| **Today (Oct 16)** | Register on lablab.ai + Discord. Create GitHub repo skeleton. Commit plan + README. |
| **Oct 17-22** | Pre-build the sandbox.py + provenance.py + tests. Get the sandbox blocking `rm -rf` locally. |
| **Oct 23-29** | Build orchestrator + LLM planning loop with mocked LLM (Vultr credits not yet available). Frontend minimal. |
| **Oct 30-Nov 2** | Provision Vultr VM, deploy, smoke test end-to-end. Wait for hackathon kickoff. |
| **Nov 3 (kickoff)** | Switch LLM endpoint to Vultr Serverless Inference. Run real tasks. |
| **Nov 4-6** | Polish demo, record video, write submission. |
| **Nov 7** | Final smoke test, submit. |
| **Nov 8** | Winners announced (optional on-site in SLC). |

### Anti-ban / risk notes

- **This is not a PR to OSS** — it's a hackathon submission, different track from the Hacktoberfest PRs.
- **alethech is your own project** — using it as the trust layer is legitimate (not self-promotion, it's the actual best tool for the job).
- **Team of 1 is fine** — hackathon allows solo entries. We can register solo now, invite teammates via Discord later if needed.

---

## Registration steps (need user action)

1. **Create lablab.ai account**: https://lablab.ai
   - Sign up with email or Google/GitHub.
2. **Register for the hackathon**: https://lablab.ai/ai-hackathons/vultr-hackathon
   - Click "Sign up" / "Enroll" button.
3. **Join lablab.ai Discord**: required for participation.
   - Link: https://discord.gg/lablab-ai (visible after enrollment)
4. **Create a Vultr account** (for credits): https://www.vultr.com
   - The $200 credit code will be published on the hackathon page before kickoff (Nov 3).
   - DO NOT deploy anything yet — credits aren't active until kickoff.
5. **Create a GitHub repo** for the project (I can do this for you when you confirm the name).

---

## Why this project wins (positioning)

1. **"Verifiable output"** is in the hackathon spec — we're the only ones who'll deliver cryptographic verification, not just "I ran it, trust me".
2. **Containment moment is naturally dramatic** — agent tries `rm -rf /`, sandbox blocks, alethech logs the ATTEMPT (not just the block) as a signed commit. The intent is permanently on the DAG even though the action never executed. This is a unique angle no other team will have.
3. **alethech is shipping** — 310 commits, v0.9.5, MCP Registry listed, MIT licensed. Not a hackathon-only toy; it's a real project getting real polish from the hackathon exposure.
4. **Business value is clear** — enterprises deploying AI agents need audit trails for compliance. The "Prove-It Code Runner" use case (run a PR's code safely + prove what it did) is a real product.
5. **Open source + MIT** matches the hackathon's submission requirement ("original work, open source, MIT License unless specified otherwise").

---

## Next steps (today)

- [ ] User registers on lablab.ai + Discord
- [ ] User creates GitHub repo `alethech-agent-vault` (or authorizes me to create it)
- [ ] I scaffold the repo structure above
- [ ] I write the README + ARCHITECTURE + setup scripts
- [ ] I pre-build `sandbox.py` + `provenance.py` + tests locally (Docker required)
- [ ] I write the demo script for the video

The build window is Nov 3-8. We have **2.5 weeks to pre-build everything except the Vultr-specific deployment**, so during the hackathon week we just deploy + polish + record.
