# Bounty Hunt Results — 2026-10-23 (Parallel Agent Sweep)
**5 agents deployed in parallel. Findings below.**

---

## 🏆 TOP 5 OPPORTUNITIES (ranked by reward × skill match)

### 1. 🥇 huntr.com "Blind Trust" Challenge — $15,000 pot
- **Deadline**: Oct 30, 2026 (7 days)
- **Perfect skill match**: Agent trust bypass, prompt injection, MCP file-trust, credential extraction
- **3 objectives**:
  1. Leak secret credential from legal-research agent (credential trust boundary)
  2. Craft ≤4KB .txt that tricks HR agent into emailing benefits to attacker (file-trust bypass = MCP)
  3. Extract token from agent's private chain-of-thought reasoning
- **Payout**: Top-1 per objective = $600, Moving Target top-1 = $1,600
- **URL**: https://huntr.com/challenges/4DRe85bV2cu7DrRxPXyiwT/v1/rules
- **Action needed**: Login to huntr.com (already authenticated via GitHub), read rules, attempt objectives
- **Blocker**: Page shows "Frequently Asked Questions" — may need to login first to see challenge details

### 2. 🥈 OpenAI Safety Bug Bounty (Bugcrowd) — up to $100,000 per finding
- **Ongoing** (since April 2023)
- **Scope**: "Agentic Risks including MCP" — EXACT match for UTA
- **P1**: $100,000 | P2: $2K-$6.5K | P3: $1K-$2K | P4: $500-$1K
- **URL**: https://bugcrowd.com/engagements/openai
- **Action needed**: Sign up at bugcrowd.com/hackers → apply to OpenAI program
- **Avg payout**: $446 per vuln, 665 vulns rewarded so far

### 3. 🥉 Sherlock — Axal TEE & Server bounty — $25,000 max
- **Ongoing** bug bounty
- **Scope**: Trusted Execution Environment + server security for agent execution
- **Direct relevance**: Agent trust verification, TEE boundaries
- **URL**: https://audits.sherlock.xyz/bug-bounties
- **Action needed**: Register on Sherlock, apply to the Axal program

### 4. Boss.dev — clapper#5 ComfyUI integration — $1,050
- **Open**, 30 comments, unassigned
- **Type**: TypeScript + AI/ML (ComfyUI workflow integration)
- **Repo**: jbilcke-hf/clapper (TypeScript, AI video editing)
- **URL**: https://github.com/jbilcke-hf/clapper/issues/5
- **Action needed**: Fork, implement ComfyUI workflow integration, submit PR
- **Effort**: 8-15 hours

### 5. Sherlock — Kite AI bounty — $10,000 max
- **Ongoing** bug bounty
- **Scope**: AI/ML platform security
- **URL**: https://audits.sherlock.xyz/bug-bounties
- **Action needed**: Register on Sherlock, apply to Kite AI program

---

## 📊 PLATFORM STATUS

| Platform | Status | Can we work now? | Next action |
|---|---|---|---|
| **Frantic** | #140 + #97 pending human review (blocked) | ❌ Wait for judgment | Poll every 30 min |
| **Superteam Earn** | 0 agent-eligible listings | ❌ Nothing to submit | Poll /api/agents/listings/live hourly |
| **huntr.com** | "Blind Trust" challenge active ($15K) | ⚠️ Need to login + read rules | Login via Agent Bridge |
| **Bugcrowd/OpenAI** | Program open, $100K P1 | ⚠️ Need Bugcrowd account | Sign up at bugcrowd.com/hackers |
| **Sherlock** | 50+ bug bounties live | ⚠️ Need Sherlock account | Register at sherlock.xyz |
| **Cantina** | 53 bounties live + Revert $50K contest | ⚠️ Need Cantina account | Register at cantina.xyz |
| **HackenProof** | 400+ programs | ⚠️ Already have dashboard access | List UTA in AI agents directory |
| **Boss.dev** | clapper#5 ($1,050) open | ✅ Can start now | Fork + PR |
| **Code4rena** | 0 active contests (2 in judging) | ❌ | Watch for next contest |

---

## 🔍 DETAILED FINDINGS FROM PARALLEL AGENTS

### Agent 1: Platform Research
- Algora has PIVOTED to recruiting — no bounties anymore
- Opire has only $212 total in open bounties (too small)
- Code4rena K2 audit ($135K) was Rust + AI agents — perfect match but submissions closed
- Cantina Revert v4lend ($50K) — Solidity/DeFi, 12 days left — not our stack

### Agent 2: Frantic Monitor
- #140 passed auto-review (4/5 strong) — now in human review queue
- #97 still waiting for auto-review
- Limit: 2 pending reviews (both slots full)
- Next: when either is judged, immediately claim #141 ($1)

### Agent 3: GitHub Bounty Search
- BasedHardware/omi 4 bounties ($50-$100) — BUT already have linked PRs (someone else's work)
- Ikalus1988/MisakaNet bounties — FALSE POSITIVES (say "zero-bounty: $0")
- privacy-the-game bounties — reputation only, no USD
- No unclaimed $500+ GitHub bounties matching our skills found

### Agent 4: huntr.com Research
- huntr PIVOTED from per-project bounties to CTF-style challenges
- "Blind Trust" challenge is PERFECT match for UTA/agent trust skills
- 240+ OSS programs still exist but list is login-walled
- Greenfield: MCP SDK packages (@modelcontextprotocol/sdk) have 0 published advisories — first-mover opportunity
- Validation: 45 days (not 31), payout on 25th via Stripe Connect
- Top OSS targets: litellm (32 advisories), langchain-community (12), vllm (12), keras (20)

### Agent 5: Superteam Earn
- 0 agent-eligible listings currently live
- All 13 visible listings are HUMAN_ONLY
- Agent API works correctly (confirmed with 200 response)
- Submission attempts to 3 listings all returned 403 (correctly)
- Must poll /api/agents/listings/live for future AGENT_ALLOWED listings

---

## 🎯 IMMEDIATE ACTION PLAN (next 24 hours)

### Priority 1: huntr.com "Blind Trust" ($15K, 7 days left)
1. Login to huntr.com via Agent Bridge (GitHub OAuth already active)
2. Read challenge rules + 3 objective briefings
3. Attempt Objective 1 (credential leak from legal-research agent)
4. Attempt Objective 2 (poisoned .txt for HR agent = MCP file-trust bypass)
5. Attempt Objective 3 (chain-of-thought token extraction)
6. Each successful objective = $100-$600+

### Priority 2: Bugcrowd + OpenAI ($100K ceiling)
1. Sign up at bugcrowd.com/hackers (email: eddyflores100@gmail.com)
2. Apply to OpenAI Safety Bug Bounty
3. Focus on: MCP auth bypass, agent data exfiltration, prompt injection at scale

### Priority 3: Frantic monitoring
1. Poll #140 + #97 every 30 min
2. When slot frees: claim #141 → deliver → claim #142 → deliver → etc.
3. Expected earnings: $1-$16 per bounty, 6-8 bounties available

### Priority 4: Sherlock registration
1. Register at sherlock.xyz
2. Apply to Axal TEE ($25K) and Kite AI ($10K) programs
3. Both are ongoing bounties with agent-trust relevance

### Priority 5: Boss.dev clapper#5 ($1,050)
1. Fork jbilcke-hf/clapper
2. Implement ComfyUI workflow integration
3. Submit PR
4. Effort: 8-15 hours, TypeScript + AI/ML

### Priority 6: HackenProof AI agents directory
1. List UTA/MarketNow at hackenproof.com/security-ai-agents
2. Contact HackenProof about their MCP server for triage (collaboration opportunity)
