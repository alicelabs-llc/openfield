# Agent Signups — Status Report
**Date:** 2026-10-23
**User:** eddyflores100-lang (eddyflores100@gmail.com)

---

## ✅ Done — Account created and credentials saved

### 1. Frantic (gofrantic.com) — Agent registered + 2 of 3 seals completed

- **Agent name:** MarketNow-UTA-Trust-Agent
- **Agent ID:** `agent-408707`
- **Operator handle:** @eddyflores100-lang
- **Public profile:** https://gofrantic.com/a/agent-408707
- **Status:** registered, oath sealed, lantern sealed, signal pending (requires vouching from another Frantic agent)
- **Eligibility:** requires_email_verification
- **Credentials saved:** /home/z/my-project/credentials/frantic-agent.json
- **Tokens:**
  - agent_token: `fr_agent_5cf9a068ada0b00f08820ef1a540ce58af3bf148652706fb`
  - operator_token: `fr_op_07d561340c9ef1d1a3306d3aca1b6937c2b21fdef22eaea9`

### 2. Superteam Earn (superteam.fun) — Agent registered via API

- **Agent name:** MarketNow-UTA-Trust-Agent
- **Agent ID:** `d212b2c6-ff84-4620-827a-31c7d6a7343d`
- **Username slug:** `marketnow-uta-trust-agent-military-35`
- **Profile:** https://superteam.fun/u/marketnow-uta-trust-agent-military-35
- **API base:** https://superteam.fun
- **API key:** `sk_271c1d383cdbc4574496e1cdf1f8cddc56e3b3404bd756b29c286230e65916bb`
- **Claim code (for linking human payout):** `CA79C3E4F68569FE3607E90D`
- **Credentials saved:** /home/z/my-project/credentials/superteam-earn-agent.json
- **13 agent-eligible listings available** — see below

---

## ✅ Already authenticated (no signup needed)

### 3. huntr.com — Logged in via GitHub OAuth

- The browser already has an active GitHub OAuth session.
- Just visit https://huntr.com to access the dashboard.
- 240+ AI/ML bug bounty programs available (LangChain, HuggingFace Transformers, PyTorch, etc.).
- **Critical cap:** $50,000 USD per finding.

---

## ⏳ Pending — needs browser OAuth (cannot automate via API)

### 4. HackenProof "For AI Agents" directory

- Correct URL: https://hackenproof.com/security-ai-agents (redirects from /ai-agents)
- Behind Cloudflare — page loads but I can't navigate the contact form via Agent Bridge without risking the user losing their place.
- **Action:** Visit https://hackenproof.com/security-ai-agents manually, find the "List your agent" link, fill the form with:
  - Agent name: MarketNow / UTA Trust API
  - Description: Ed25519-signed agent trust verification (ATC/1.0), fail-closed verdicts, x402 v2 native
  - URL: https://uta-trust-api.eddyflores100.workers.dev
  - Repo: https://github.com/alicelabs-llc/universal-trust-adapter

### 5. OpenAI Safety Bug Bounty (Bugcrowd)

- URL: https://bugcrowd.com/engagements/openai
- Requires Bugcrowd account first (sign up at https://bugcrowd.com/hackers)
- Once registered, the OpenAI program is invitation-only — apply through Bugcrowd's researcher portal.
- Scope explicitly includes "Agentic Risks including MCP" (perfect for UTA).

### 6. Superteam Earn — link human payout claim

- The agent is registered (above), but payouts require linking a human claimant via Twitter OAuth.
- Use the **claim code `CA79C3E4F68569FE3607E90D`** at https://superteam.fun/agent-claim
- This will tie the agent's earnings to a real Solana wallet + KYC.

---

## 🎯 What to do RIGHT NOW (5 minutes)

1. **Check your email** (eddyflores100@gmail.com) — there's a verification link from Frantic. Click it. This unlocks paid bounties up to $10 each.

2. **Visit huntr.com** — you're already logged in via GitHub. Browse the bounty programs:
   - LangChain (large pool, AI-agent-relevant)
   - HuggingFace Transformers (largest historical payouts)
   - Look for prompt injection, MCP auth bypass, agent identity vulns

3. **Claim your Superteam agent profile** at https://superteam.fun/agent-claim with code `CA79C3E4F68569FE3607E90D` (links Twitter for payouts).

4. **Visit Bugcrowd** — sign up at https://bugcrowd.com/hackers (free, email/password), then apply to the OpenAI program.

5. **Visit HackenProof** — https://hackenproof.com/security-ai-agents — find "List your agent" and submit UTA/MarketNow.

---

## 📋 Available work RIGHT NOW (no signup needed)

### Superteam Earn — 13 agent-eligible bounties (live)
| Title | Reward | Deadline |
|---|---:|---|
| Travel boost: Create Content for Breakpoint 2026 | $6,000 | Oct 25 |
| Vaultline Security Audit Grants (Colosseum) | up to $40,000 | Oct 31 |
| Redesign Your Favourite App on Solana | $1,500 | Oct 23 (today!) |
| Launch & Trade on Daejin (Twitter thread) | $620 | Oct 23 (today!) |
| Crea Contenido para Encuentro 2026 Madrid | $2,000 | Oct 24 |
| Colosseum: Founder Support - Talk to 5 Users | $1,000 | Oct 25 |
| Rumbo a Breakpoint 2026 | $5,000 | Nov 3 |
| Inside the Block: Solana Validators | $2,500 | Nov 5 |
| Show us how you use MozaikPay | $500 | Nov 12 |
| Panta x NectarFi Trading Competition | $500 | Nov 12 |

### Frantic — 8 bounties ($1–$16 each, after email verification)
| # | Title | $ |
|---|---|---:|
| 142 | Approve email campaign via MAP description | $3 |
| 141 | Onboard agent via Nitrosend MCP, send 1 email | $1 |
| 140 | Send email with 30-line Nitrosend SDK script | $1 |
| 139 | Send first email via Nitrosend CLI | $1 |
| 130 | Answer Reddit threads with verified registry facts | $3 |
| 129 | Earn citation on external page that ranks | $16 |
| 128 | Earn citation for open data registry | $8 |
| 97 | First bounty on the house (rebate) | $10 |

### GitHub bounties matching UTA pattern (from research)
- AstralDeep/AstralDeep #321, #322, #323 (OpenAI Agents SDK + MCP)
- AstralDeep/LETS #71 (MCP for protected tool execution, 400 pts)
- ditto-subnet #2871 (GitHub attestation linked to hotkey)
- ditto-subnet #2044, #2046 (bounty accounting with audit receipts — alethech fits)
- ak10082247-max/canaryguard-402 #2 ($5+ USDC prompt injection bypass)

---

## 📁 Files created/updated

- `/home/z/my-project/credentials/frantic-agent.json` — Frantic credentials
- `/home/z/my-project/credentials/superteam-earn-agent.json` — Superteam Earn credentials
- `/home/z/my-project/AGENT_WORK_OPPORTUNITIES.md` — full research doc
- `/home/z/my-project/AGENT_SIGNUPS_STATUS.md` — this file

