# Agent Work Opportunities — Research Findings
**Date:** 2026-10-23
**Researcher:** Super Z (as agent for @eddyflores100-lang)
**Goal:** Find platforms where AI agents are looking for work, where work is offered to agents, and where agent-infrastructure builders (alethech, MarketNow, UTA) can earn.

---

## TL;DR — Top 8 platforms to act on now

| # | Platform | Type | Best fit | Action |
|---|---|---|---|---|
| 1 | **huntr.com** | AI/ML bug bounty | Trust/verification vulns in langchain, transformers, mcp libraries | Sign up, browse 240+ active programs ($50k caps) |
| 2 | **OpenAI Safety Bug Bounty** | AI safety bounty | UTA/MarketNow — explicitly scopes "Agentic Risks including MCP" | Apply (private program) |
| 3 | **Superteam Earn** | Solana bounties (agent-eligible) | MarketNow/UTA agent wallet integration | Sign up, claim agent-only listings |
| 4 | **Frantic (gofrantic.com)** | Agent-native bounty board | 8 live bounties $1–$16, USDC on Base | Enlist agent, claim small bounties for runway |
| 5 | **AstralDeep GitHub bounties** | OSS bounties in agent/MCP trust | UTA pattern fits #321, #322, #323 directly | Comment `/claim` on bounties |
| 6 | **ditto-assistant/ditto-subnet** | Bittensor SN118 bounties | alethech + UTA fit #2044, #2046, #2871, #2872 | Read CONTRIBUTING, claim bounties |
| 7 | **Algora** | GitHub bounty marketplace | General OSS bounties ($50–$2,500 typical) | Browse algora.io, comment `/attempt` |
| 8 | **Opire** | GitHub comment bot bounties | General OSS, $20+ floor | Browse opire.dev, install OpireBot |

---

## 1. AI/ML Bug Bounty Platforms (HIGHEST FIT for UTA/MarketNow/alethech)

### huntr.com (acquired by Protect AI → Palo Alto Networks)
- **Focus:** AI/ML open-source vulnerabilities + model file format vulns
- **Scope:** 240+ active programs covering PyTorch, Hugging Face Transformers, LangChain, GGUF, ONNX, safetensors
- **Payouts:** USD via Stripe Connect, monthly on 25th, critical cap **$50,000**
- **Agent policy:** "Agent allowed: yes" (not officially welcomed, but AI-assisted reports accepted)
- **KYC:** at payout (Stripe Connect — works in Ecuador)
- **Realistic earnings:** 5–6 figures/quarter for top researchers; recent #1 climbed from newcomer in 5 months
- **Action:** Sign up at huntr.com, link Stripe Connect, pick LangChain or Transformers program
- **Why it fits UTA:** prompt injection, MCP auth bypasses, agent identity = direct overlap

### OpenAI Safety Bug Bounty (NEW, March 2026)
- **Scope (explicit):**
  - "Agentic Risks including MCP" — third-party prompt injection, data exfiltration
  - ChatGPT Agent harmful actions at scale
  - OpenAI proprietary info leakage (reasoning, internal data)
  - Account/platform integrity bypasses
- **Payouts:** through OpenAI Security Bug Bounty (existing program, $6.5M+ paid historically)
- **How to participate:** Apply through their Safety Bug Bounty portal
- **Why it fits UTA:** UTA's exact wedge — agent trust verification + spend authority + receipts

### HackenProof
- **Focus:** Web3 bug bounties (200+ programs: Ethereum Foundation, NEAR, MetaMask, Aptos, Sui)
- **Payouts:** up to $1M for critical; USDC default
- **Agent-specific:** Has "For AI Agents" directory — explicitly invites AI security agents
- **HackenProof MCP server** exists — agents can list themselves
- **Action:** List MarketNow/UTA agent in the "For AI Agents" directory; pick a program

### Bugcrowd (Savant Pathseeker)
- Top-3 global bug-bounty platform
- **AI-assisted reports allowed** if human-validated
- **Payouts:** PayPal/wire/BTC
- Action: Standard bug bounty hunter signup

---

## 2. Agent-Native Bounty Boards (work posted FOR agents)

### Frantic (gofrantic.com)
- **What:** Public bounty board where AI agents do paid work; every claim/delivery/judgment/payout sealed to public ledger
- **Live now:** 8 open bounties, $1–$16 each, USDC on Base
  - #142 — Approve agent email campaign via MAP description ($3)
  - #141 — Onboard agent via Nitrosend MCP, send 1 email ($1)
  - #140 — Send email via Nitrosend SDK script ($1)
  - #139 — Send first email via Nitrosend CLI ($1)
  - #130 — Answer Reddit threads with verified registry facts ($3)
  - #129 — Earn citation on external page ($16)
  - #128 — Earn citation for open data registry ($8)
  - #97 — First bounty on the house ($10 back when clears)
- **Onboarding:** POST `https://gofrantic.com/v1/signup` → store agent_token → register x402 payout wallet → claim
- **MCP server:** `https://api.gofrantic.com/mcp` (streamable-http) — agents can read board, claim, deliver
- **Total season pool:** $2.7k season total, 132 agents open for work, 1.8k operators enlisted, 635 sworn, $1.6k moved
- **Best agent:** "wubba-lubba-dub-dub" — $106, 13 settled bounties
- **Action:** Enlist MarketNow/UTA agent; do 2-3 small ones for credibility then bigger ones

### Agent Bounties (NSPG13/agent-bounties)
- **Open-source marketplace** for AI agents to autonomously post, fund, claim, solve, verify work
- **Payouts:** Base USDC, verifiable on-chain settlement
- **Has bounty issues in their own repo** — also runs the protocol
- Examples: NSPG13/agent-bounties #590 "[META] Earn 1 USDC margin with an agent-discovery bounty"
- **Action:** Read protocol, become an early agent on the network

### Other agent-task marketplaces (gigs.sh/c/agent-task-marketplace verified 9 platforms):
| Platform | Payment | Friction | Notes |
|---|---|---|---|
| Agent Hansa | USDC | INSTANT | Agent-first |
| Clustly | USDC/Solana | INSTANT | |
| Daydreams TaskMarket | USDC/Base | INSTANT | DaydreamsAI ecosystem |
| AgentHire | USDC/Solana | EASY | 10K jobs self-reported |
| AgentPact | USDC/Base | EASY | MCP-native |
| BountyBook | USDC/Base | EASY | |
| Claw Earn | USDC/Base | EASY | |
| Toku.agency | STRIPE/USD | EASY | 15% fee, race-to-bottom |
| NEAR AI Agent Market | USDC | MODERATE | ~3.8K jobs |

---

## 3. Solana / Crypto Bounties (agent-eligible)

### Superteam Earn (superteam.fun/earn)
- **3,249 opportunities** listed historically, $16M+ total earned
- **240,820+ users** in network
- **Agent API:** Yes, with AGENT_ALLOWED and AGENT_ONLY listing visibility tiers
- **Skill spec:** superteam.fun/skill.md
- **Payment:** USDC on Solana, KYC at payout
- **Current relevant bounties:**
  - "Build Solana-native plugins for Zeroclaw" (agent + Solana)
  - "Steve Agent Arena: Launch Your Agent & Win 500 USDC" (launch agent on Solana)
  - "Break It Before Users Do: MultiHopper Agentic Flow Bugs" (debug agentic flows)
  - "Build for Breakpoint: Agentic Grants" ($200 avg, Superteam UK)
  - "Agentic Engineering Grants" ($200 avg)
- **Action:** Sign up as agent, browse AGENT_ALLOWED listings, apply with alethech/MarketNow/UTA as portfolio

### Gitcoin (gitcoin.co)
- Public goods funding + bounties
- Has research report: "AI Agents and Public Goods: The Emerging Agentic Economy"
- Less direct bounty hunting, more grants-based
- **Action:** Apply for retroactive grants if alethech/UTA adoption grows

---

## 4. GitHub-Native Bounty Platforms (work as PRs)

### Algora (algora.io)
- Companies fund GitHub issues with USD; developers claim + PR + paid on merge
- **Realistic range:** $50–$2,500 per bounty (Archestra $50–$300, Twenty YC S23 $2,500, Isaac $850)
- **Ziverge alone:** $143K distributed via Algora
- **API:** `api.docs.algora.io/bounties` (public, unauthenticated)
- **Action:** Sign up via GitHub OAuth + Stripe Express; scrape live bounties via API

### Opire (opire.dev)
- GitHub-comment-driven bounty bot (5,590 users, ~12K projects installed)
- Anyone can fund any GitHub issue
- **Bounties start at $20 USD**; 4% platform fee
- **Action:** Install OpireBot in repos you contribute to; browse opire.dev

### OpenBounty.ai (openbounty.ai)
- "GitHub-native bounties for humans and AI agents"
- Post bounty on issue → human OR AI agent claims → opens PR → paid on merge
- **Action:** Browse open bounties, claim agent-eligible ones

### boss.dev
- GitHub-issue bounties with auto-payout on close-by-PR
- Bank-transfer settlement in 23 countries, 33 currencies
- **Action:** Standard signup

---

## 5. Specific GitHub Bounties Matching Your Profile (Ed25519 / MCP / Trust / Agent Wallet)

Found via GitHub search of `label:bounty state:open`:

### AstralDeep bounties (DIRECT overlap with UTA pattern)
- **AstralDeep/AstralDeep #321** — "Qualify an isolated OpenAI Agents SDK consumer of Astral Work" (100 points, has 3 comments — likely already claimed)
- **AstralDeep/AstralDeep #322** — "Serve owner-authorized MCP resources for an optional ChatGPT Work panel"
- **AstralDeep/AstralDeep #323** — "Qualify the OpenAI MCP tunnel against Astral authentication and discovery"
- **AstralDeep/AstralDeep #334** — "Import instructions-only Agent Skills into the governed owner catalog"
- **AstralDeep/LETS #71** — "Provide a thin, tested MCP integration profile for protected tool execution" (400 points, P2)
- **AstralDeep/AstralDeep #336** — "Pilot source-span validated extraction from clinical notes"

### ditto-assistant/ditto-subnet bounties (Bittensor SN118 — fits alethech + UTA)
- **#2871** — "Miner CLI: attest a GitHub account and link it to the miner hotkey" (sr25519 signature, identity attestation — overlaps with UTA's Ed25519 trust cards)
- **#2872** — "Miner CLI: sign the contributor licence agreement (CLA) with the miner hotkey" (already claimed by Reggiebro)
- **#2044** — "Specify scoped build-bounty rules, alpha funding and governance" (audit/receipt model — alethech fits)
- **#2046** — "Implement bounty acceptance, alpha awards, fee refunds and accounting" (audit/receipt — alethech fits)

### Other relevant GitHub bounties
- **ak10082247-max/canaryguard-402 #2** — "$5+ USDC: Adversarial Prompt Injection Bypass on CanaryGuard Firewall" (10 comments — perfect fit for UTA's adversarial verification work, may already be claimed)
- **Convex-Dev/bounties #8** — "Unity Game Engine integration (3000 Gold)" (signed transactions, queries — fits Ed25519 work)
- **mergeos-bounties/mergeos #244** — "[50 MRG] Gomi IDE job"
- **NSPG13/agent-bounties #871** — "[DIRECT] Expose bounded-wallet liquidity and authority separately" (UTA-pattern!)

---

## 6. Freelance Platforms Built for AI Agents

### dealwork.ai
- Purpose-built for AI agents (3% AI-to-AI fee)
- Escrow-protected contracts
- Job range: $0.10 micro-tasks to $50+ research
- API access for bidding, contract management, work submission
- **Action:** Register MarketNow/UTA agent, bid on small tasks first

### ClawGig (clawgig.ai)
- AI-agent-only marketplace on Solana
- USDC payments, 10% platform fee
- REST API with API key auth
- Jobs typically $5–$100

### Toku (toku.agency)
- AI agent marketplace, instant services
- 15% fee (high), webhook notifications
- Race-to-bottom pricing

### RentAHuman.ai (different direction — AI hiring humans)
- AI agents can hire humans for tasks they can't do alone
- Native MCP, REST API, escrow
- **Action:** If alethech/MarketNow/UTA agent needs human-in-the-loop, use this

---

## 7. Recommended Action Plan (next 7 days)

### Day 1 (today)
1. **Sign up at huntr.com** — link Stripe Connect. Browse LangChain + Hugging Face Transformers programs.
2. **Sign up at gofrantic.com** — enlist MarketNow/UTA agent. Register x402 payout wallet. Claim #97 ($10 back when first bounty clears).
3. **Sign up at Superteam Earn** (superteam.fun/earn) — set profile as agent.

### Day 2
4. **Browse Algora bounties** via public API at `api.docs.algora.io/bounties`. Filter for MCP/agent/trust keywords.
5. **Comment on AstralDeep bounties** that match UTA pattern (#321, #322, #323, LETS #71) — check if already claimed first.
6. **Apply to OpenAI Safety Bug Bounty** (private program, may take time to admit).

### Day 3-4
7. **Submit first Frantic bounty** (#139 or #140 — Nitrosend CLI email, $1 each). Easy win, gets you on the leaderboard.
8. **Browse Superteam AGENT_ALLOWED listings**, pick one matching UTA (agent wallet, trust verification).
9. **Install OpireBot** in any of your own repos where contributors might want bounties.

### Day 5-7
10. **Hunt first huntr.com vuln** — pick LangChain or Transformers. Even medium-tier vulns pay $500-$2k.
11. **Submit alethech/MarketNow/UTA** to the HackenProof "For AI Agents" directory.
12. **Engage with ditto-subnet** — read CONTRIBUTING, see if #2871 (GitHub attestation) is still open and within reach.

---

## 8. Realistic Earnings Forecast

| Platform | Realistic monthly earnings | Time to first payout |
|---|---:|---|
| Frantic | $10–$100 (small bounties, fast) | 1–3 days |
| Superteam Earn | $200–$2,000 per bounty | 1–2 weeks |
| Algora | $50–$500 per bounty | 1–2 weeks (after merge) |
| huntr.com | $500–$10,000 per vuln (medium-tier) | 1–3 months (validation cycle) |
| OpenAI Safety BB | $1,000–$15,000 per finding | 1–3 months |
| AstralDeep bounties | 100–400 points (no $ value stated) | 1–2 weeks |
| dealwork.ai / ClawGig | $50–$500 per task | 1–2 weeks |
| HackenProof | $500–$50,000 per finding | 1–6 months |

**Realistic first-month target:** $300–$800 from small bounties (Frantic + Superteam + Algora), with longer-term potential $5k–$20k/month from security bounties (huntr + OpenAI + HackenProof).

---

## 9. Strategic Notes

### Your wedge is unique
You've already opened 20+ GitHub issues across major agent platforms (langchain-ai/langgraph, crewAIInc/crewAI, microsoft/autogen, vercel/ai, openai/openai-agents-python, coinbase/agentkit, elizaOS/eliza, daydreamsai/daydreams, etc.) all proposing the SAME pattern: external spend authority + signed receipts + fail-closed verdicts. **This is exactly what UTA does.**

That means you have a **standardization wedge** in progress. Bounties that ask for "isolated MCP consumers" (AstralDeep #321), "owner-authorized MCP resources" (#322), "MCP integration for protected tool execution" (LETS #71), "GitHub account attestation linked to hotkey" (ditto #2871), "CLA signing with hotkey" (ditto #2872) are ALL opportunities to implement the UTA pattern as a reference solution inside other projects.

### Don't spread too thin
- 9 agent-task-marketplace platforms exist but most have low volume.
- Concentrate on **3-4 platforms** with real activity: huntr, Frantic, Superteam Earn, Algora.
- Use the GitHub Issues label:bounty search as a **discovery tool** for one-off OSS bounties that match your skills.

### What you're NOT doing yet (gaps)
- **Not listed on HackenProof "For AI Agents"** — go list UTA/MarketNow
- **Not enlisted on Frantic** — easy onboarding, fast small wins
- **Not signed up on huntr.com** — biggest AI/ML bug bounty platform
- **Not applied to OpenAI Safety Bug Bounty** — perfect scope match
- **Not in Superteam Earn agent tier** — explicit AGENT_ALLOWED listings you're missing
