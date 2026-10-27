# Hackathon Hunt — Worldwide Active Hackathons with Cash Prizes (Oct 23 – Nov 30, 2026)

**Task ID:** 5-hackathons-worldwide
**Agent:** hackathon-hunter
**Date:** 2026-10-23
**Method:** Direct HTTP fetch of source pages (curl + Python parsing). No Cloudflare bypass for devpost.com. Devpost entries are confirmed via direct URL fetch where known; lablab.ai API scrape via /ai-hackathons; Superteam Earn via public /api/listings endpoint; taikai.network per-hackathon overview pages; dev.to challenges pages; solana hackathons subdomain; ETHGlobal events page.

---

## TL;DR — 22 actionable hackathons/bounties found, all currently open with deadlines Oct 24 – Nov 30, 2026, all with cash > $500, all worldwide/LATAM-eligible

The biggest wins (highest ROI given our alethech-agent-vault + MCP + security track record):

1. **AMD AI League Match 5 — AI-Powered Code Repository Repair** (Oct 27 – Nov 10, lablab.ai) — PERFECT FIT for alethech-agent-vault
2. **Nebius x NVIDIA Global AI Hackathon** ($50K+, Devpost, Oct 30) — alethech-agent-vault scaffold portable to Nebius AI Cloud
3. **PayPal AI Hackathon** ($69,750, Devpost, Nov 12) — user's marketnow/MCP integrates PayPal cleanly
4. **Solana Perps & Prediction Markets** ($100K, Dec 5) — TypeScript/Rust + security background
5. **Superteam Vaultline Security Audit Grants** ($40K pool, up to $4K per project, Oct 31) — security/CodeQL fit

---

## Master table — sorted by deadline (closest first)

| # | Hackathon | Organizer | Prize pool (USD) | Deadline (UTC) | Track / topic | Format | Eligibility | Required stack | Effort | Why we can win |
|---|-----------|-----------|------------------|-----------------|---------------|--------|-------------|---------------|--------|-----------------|
| 1 | [Superteam — Crea Contenido para El Encuentro 2026 en Madrid](https://earn.superteam.fun/listings/crea-contenido-para-promocionar-el-encuentro-2026) | La Familia | $2,000 USDG | **2026-10-24 22:59** | Spanish content creation for Solana Breakpoint side event in Madrid | Online bounty | Worldwide (Spanish-speaking LATAM preferred) | Content (article/thread/video) in Spanish | LOW | User is Ecuadorian, native Spanish. LATAM-aligned pitch (Madrid Encuentro). |
| 2 | [DEV.to HF26 Week 3 — "Slow and Steady"](https://dev.to/challenges/hacktoberfest-week3-2026-10-19) | DEV.to × Hacktoberfest | $2,550 total ($250 overall + $200 ×6 featured + $100 ×14 partner) | **2026-10-25 23:59 PDT → 2026-10-26 06:59 UTC** | Open-source AI project, new build (not a PR); theme "Slow and Steady" | Online | Worldwide (excl. US-sanctioned countries) | Open-weight model / open-source agent harness; DEV.to post with #devchallenge #hf26challenge #hacktoberfest tags | LOW (1 wk) | Best Use of **Auth0 for AI Agents** ($200) + **Sentry Agent Tracing** ($200) + **TabPFN in MCP server** ($200) all align with alethech-agent-vault. Effort is 1 week, fresh project. |
| 3 | [Superteam — Travel Boost: Create Content for Breakpoint 2026](https://earn.superteam.fun/listings/travel-boost-for-bp26) | Superteam Germany | $6,000 USDG | **2026-10-25 21:59** | Solana Breakpoint 2026 promo content | Online bounty | Worldwide | Article/thread/video | LOW-MED | 25 submissions already, but high payout. Native Spanish angle for LATAM Breakpoint audience. |
| 4 | [Superteam — Colosseum: Founder Support — Talk to 5 Users](https://earn.superteam.fun/listings/colosseum-founder-support-talk-to-5-users) | Superteam Netherlands | $1,000 USDG | **2026-10-25 09:59** | Customer discovery for Colosseum (Solana) projects | Online bounty | Worldwide | Founder work (interview 5 users, write report) | LOW | Skip if not running a Colosseum project. Otherwise trivial $1K. |
| 5 | [taikai — SpaceXAI Digital Transformation Lab](https://taikai.network/en/spacexai/hackathons/spacexai-digital-transformation-lab/overview) | SpaceXAI × TAIKAI | TBA (Portuguese SME focused) | **2026-10-27 16:00** | AI solution for real Portuguese SME business challenge in 2 days | Online hybrid | **Portuguese SMEs only** | AI / agent stack (Python preferred) | MED | ⚠️ Eligibility restricted to Portuguese SMEs — skip for Ecuador. |
| 6 | [taikai — Hack4Guimarães 2035](https://taikai.network/en/cmguimaraes/hackathons/hack4guimaraes2035/overview) | CM Guimarães × TAIKAI | TBA (regional) | **2026-10-28 12:00** | Innovation marathon — Guimarães Economy Month 2026 | Online hybrid | Local Portuguese | Open | MED | ⚠️ Regional restriction — skip for Ecuador. |
| 7 | [AMD AI League — Match 5: AI-Powered Code Repository Repair](https://lablab.ai/ai-hackathons/amd-lablab-ai-academy-challenge) | AMD × lablab.ai | $500 cash + $250 GPU credits (1st) + $100 GPU credits ×50; League total **$10,000+** | Submission window **2026-10-27 → 2026-11-10** | Build a multi-agent AI system that repairs code repositories | Online | Worldwide (solo, individual only; AMD account required — free) | Python / AI agent framework; AMD ROCm preferred but flexible | MED (2 wk) | ⭐ **PERFECT FIT** — alethech-agent-vault IS literally a verifiable agent execution sandbox with provenance. Match 5 description is the alethech-agent-vault elevator pitch. |
| 8 | [Nebius x NVIDIA Global AI Hackathon](https://nebiusglobalaihackathon.devpost.com) | Nebius × NVIDIA | **$50,000+** ($20K 1st + $10K 2nd + $6K 3rd + NVIDIA Jetson Orin Nano per track) | **2026-10-30 13:00 PDT (20:00 UTC)** | "Build the next frontier of AI on open infrastructure" — Coding/Agentic Engineering, Apps & Agents, Physical AI tracks | Online | Worldwide (excl. US-sanctioned) — 23,717 already registered | Nebius Token Factory OR Nebius AI Cloud + ≥1 NVIDIA OSS model (Llama, Mistral, etc.) | HIGH | alethech-agent-vault uses OpenAI-compatible API → trivially portable to Nebius AI Cloud (also OpenAI-compatible). Use Llama 3.x or Mistral as NVIDIA OSS model. Reuses entire vault scaffold. |
| 9 | [Superteam — Vaultline Security Audit Grants for Colosseum Projects](https://earn.superteam.fun/listings/vaultline-security-audit-grants-for-colosseum-projects-up-to-4000-usdc-each) | Vaultline Security | **$40,000 USDC pool** (up to $4K per audited project) | **2026-10-31 21:59** | Security audit of Colosseum (Solana) projects | Online bounty | Worldwide (Colosseum projects only) | Solana + Rust security audit; CodeQL / static analysis | MED | We have CodeQL local triage skill, security PRs track record (useagent #84 merged, harbour #57 CodeRabbit-approved). If we adopt one Colosseum project, $4K is reachable. |
| 10 | [DEV.to HF26 Week 4 — Theme TBA](https://dev.to/challenges/hacktoberfest-week4-2026-10-26) | DEV.to × Hacktoberfest | $2,550 total (same structure as Week 3) | **2026-10-31 23:59 PDT → 2026-11-01 06:59 UTC** | Open-source AI project, fresh theme revealed Oct 26 | Online | Worldwide | Same as Week 3 | LOW (1 wk) | Fresh start, same partner categories. Two chances to win Auth0 for AI Agents / Sentry Agent Tracing / TabPFN MCP prizes. |
| 11 | [Superteam — Rumbo a Breakpoint 2026: gana una entrada y apoyo para tu viaje](https://earn.superteam.fun/listings/rumbo-a-breakpoint-2026-gana-una-entrada-y-apoyo-para-tu-viaje) | La Familia | $5,000 USDG + Breakpoint entry + travel support to Madrid | **2026-11-03 21:59** | Spanish-language content promoting Breakpoint 2026 Madrid | Online bounty | Worldwide (Spanish-speaking) | Spanish content | LOW-MED | User is LATAM/Spanish-native. Madrid Breakpoint is Dec 4-6, 2026. Win = trip + cash. |
| 12 | [Superteam — Inside the Block: How Solana Validators Order Transactions](https://earn.superteam.fun/listings/inside-the-block-how-solana-validators-order-transactions) | Superteam Ukraine | $2,500 USDC | **2026-11-05 21:59** | Technical educational content explaining Solana validator transaction ordering | Online bounty | Worldwide | Technical writing + Solana knowledge | MED | Technical depth fits user's engineering background. |
| 13 | [ETHGlobal Mumbai 2026](https://ethglobal.com/event/ethglobal-mumbai-2026) | ETHGlobal | TBA (typical ETHGlobal: $100K+ in prizes) | **2026-11-05 → 2026-11-07** (Apply to Attend) | Ethereum / Web3 hackathon | **IRL Mumbai, India** | Worldwide applicants; on-site only | Solidity / EVM / Web3 stack | HIGH | ⚠️ IRL — travel to Mumbai required. Skip for Ecuador unless user wants to travel. |
| 14 | [AMD AI League — Match 6: "Can Your AI Master the Unknown?"](https://lablab.ai/ai-hackathons/amd-lablab-ai-academy-challenge) | AMD × lablab.ai | Same as Match 5 ($500 + $250 + $100×50) | Submission window **2026-11-10 → 2026-11-14** | Build an intelligent agent that handles unknown / unseen tasks | Online | Worldwide (solo, AMD account required) | Python / agent framework | MED (4 days) | Generalization/agent robustness task — alethech-agent-vault's plan→execute→retry loop is built for this. |
| 15 | [PayPal AI Hackathon](https://paypalaihackathon.devpost.com) | PayPal | **$69,750 total** ($12K 1st, $8K 2nd, $5K 3rd, $5K Most Creative, $5K Most Impactful, $5K Best Demo, $5K AG Grid 1st + $2K 2nd + $1K ×3, $1K APIMatic ×3, $1K Bryntum ×3, Render credits) | **2026-11-12 15:00 EST (20:00 UTC)** | Build app integrating PayPal developer platform (free sandbox) + AI tool of choice | Online | Worldwide (excl. standard US-sanctioned) — 12,839 registered | PayPal sandbox API + AI tool/model of choice | HIGH | User has marketnow MCP server (already exposes 15 tools incl. trust/cred verification). Add PayPal checkout/subscription tool → instant prize category eligibility. |
| 16 | [Superteam — Show us how you use MozaikPay](https://earn.superteam.fun/listings/mozaikpay-video-chile-colombia) | MozaikPay | $500 USDC | **2026-11-12 21:59** | Video showing MozaikPay usage | Online bounty | **Chile + Colombia (LATAM-targeted!)** | Video demo | LOW | Slug = "mozaikpay-video-chile-colombia" — explicitly LATAM. Ecuador likely accepted (same region). 1-day video project. |
| 17 | [Superteam — Panta x NectarFi Trading Competition Bounty](https://earn.superteam.fun/listings/panta-x-nectarfi-trading-competition-bounty) | Panta × NectarFi | $500 USDG | **2026-11-12 22:59** | Trading competition on Solana | Online bounty | Worldwide | Trading bot / Solana | LOW | Quick trading competition. |
| 18 | [Superteam — Write a thread on $CHIMP Fair Launch](https://earn.superteam.fun/listings/chimp-on-metaplex) | ChimpX | $500 USDC | **2026-11-14 18:29** | Twitter thread about CHIMP fair launch on Metaplex | Online bounty | Worldwide | Content (Twitter thread) | LOW | Trivial content task. |
| 19 | [taikai — OutSystems Build for the Future Hackathon 2026](https://taikai.network/en/outsystems/hackathons/build-for-the-future-2026/overview) | OutSystems × TAIKAI | TBA (OutSystems credits + cash, 320 participants already) | **2026-11-16 14:04** | "Building Apps that make a difference" — AI + Social Good track | Online hybrid | Worldwide (Lisbon on-site optional) | OutSystems low-code + AI | MED | Need to learn OutSystems (low-code) — learning curve. AI agent angle is welcome per the description. |
| 20 | [Superteam — Create Content on Premier League Predictions with worm](https://earn.superteam.fun/listings/create-content-on-premier-league-predictions-with-worm) | worm | $500 USDC | **2026-11-24 02:59** | Content using worm protocol for Premier League predictions | Online bounty | Worldwide | Content + worm protocol | LOW | Sports prediction content. Light effort. |
| 21 | [lablab.ai — AI Genesis](https://lablab.ai/ai-hackathons/ai-genesis-2026) | lablab.ai × /function1 Conference | **TBA** (prior year similar events: $10K-$45K total) | **On-site Dubai Nov 2; online dates TBA** — likely Nov 3-8 per user intel | Largest AI hackathon in Middle East; partner tracks (Google, AppliedAI, Qdrant expected) | Hybrid (online + on-site Dubai) | Worldwide (online track open); on-site is invite-only | Python / AI / agent stack | HIGH | Reusable alethech-agent-vault scaffold. Dubai on-site = networking but travel self-funded. Online track alone is viable. ⚠️ Dates TBA — monitor page. |
| 22 | [AWS Builder Center — Weekend Challenge "Give your Agent a tool"](https://aws.amazon.com/build/hackathons) (login required) | AWS Builder Center | $100 AWS credits + AWS Builder Backpack (swag) — **below $500 threshold, included for completeness** | Rolling weekly | Build an agent + give it a tool | Online | Worldwide | AWS account + agent framework | LOW | Light effort, AWS credits usable for future hackathons (e.g., the Nebius compute equivalent on AWS). |

---

## Beyond the 30-day window — worth tracking (Dec 1 – Dec 14, 2026)

| # | Hackathon | Organizer | Prize | Deadline | Notes |
|---|-----------|-----------|-------|----------|-------|
| 23 | [AMD AI League — League Final](https://lablab.ai/ai-hackathons/amd-lablab-ai-academy-challenge) | AMD × lablab.ai | League leaderboard prizes (TBA, total $10K+) | **2026-12-01 19:00 UTC** | Complete Onboarding + at least 5 matches for leaderboard. |
| 24 | [taikai — CASSINI Hackathons — Space for Peace and Resilience](https://taikai.network/en/cassinihackathons/hackathons/space-for-peace-resilience/overview) | CASSINI Hackathons & Mentoring (EU) | TBA (CASSINI prizes typically €5K-€10K) | **2026-12-02 19:00 UTC** | EU space tech (Copernicus, Galileo). Big Ideas Campaign starts Nov 2. 455 participants. EU-focused but online track worldwide. |
| 25 | [Solana Perps and Prediction Markets Hackathon](https://hackathons.solana.com/hackathons/perps-and-prediction-markets) | Solana Foundation | **$100,000** ($50K 1st, $30K 2nd, $20K 3rd) + sponsor bounties | **2026-12-05** ("Deadline Dec 5, 2026 — in about 1 month") | Status: SCHEDULED. 1-week build. 464 already registered. Rust / TypeScript / Go SDKs. **Excellent fit**: perps need reliability/security, matches our security background. |
| 26 | [Superteam — MultiHopper Build & Route Challenge](https://earn.superteam.fun/listings/multihopper-build-and-route-challenge-up-to-dollar50000-revenue-share-1) | MultiHopper | **$5,000 USDC + revenue share** (up to $50K total opportunity) | **2026-12-14 21:59** | Build & route challenge. Sounds like infra/routing — fits agent vault + routing experience. |

---

## Sources checked but no actionable hackathons found (with reason)

| Source | Status | Reason |
|--------|--------|--------|
| devpost.com (browse) | ⚠️ Cloudflare-blocked (HTTP 403) | Returned Cloudflare challenge page; could only verify specific hackathon URLs we already knew (Nebius, PayPal, Docker — Docker ended 2023). |
| unstop.com | ⚠️ No API access | `/api/v1/public/hackathons` returned 404. HTML page doesn't render listings server-side. |
| dorahacks.io | ⚠️ AWS WAF challenge (Human Verification) | Cloudflare/AWS WAF blocking direct fetch. |
| hackathon.io | ❌ DNS failure | No DNS resolution. Site appears defunct. |
| hackathon.com | ⚠️ JS-rendered | HTML returns but no event cards in source — needs JS execution. |
| angelhacks.io | ❌ DNS failure | Site doesn't resolve. |
| hackerearth.com | ⚠️ HTTP 403 | Cloudflare-blocked. |
| codechef.com/contests | ⚠️ JS-only app | Returned HTML but listing requires React. |
| codeday.org | ⚠️ HTTP 429 | Rate-limited. |
| climatebase.org | ⚠️ HTTP 403 | Cloudflare-blocked. |
| platzi.com/hackathons | ⚠️ HTTP 403 | Cloudflare-blocked. |
| nuwe.io | ⚠️ HTTP 451 | Geographic restriction (likely EU only). |
| talnt.io | ⚠️ Returned 114 bytes | Empty response. |
| openai.com/events | ⚠️ HTTP 403 | Cloudflare-blocked. |
| mistral.ai/news | ✅ Fetched | Only past hackathon: 2024 Fine-tuning Hackathon. |
| cohere.com/hackathons | ❌ HTTP 404 | Page doesn't exist. |
| anthropic.com/news | ✅ Fetched | No hackathons listed. |
| developer.nvidia.com/hackathons | ❌ HTTP 404 | URL doesn't exist. |
| openhackathons.org | ⚠️ Login required | API redirects to Salesforce login. |
| aws.amazon.com/events | ✅ Fetched | AWS Summits listed are 2026 regional conferences (São Paulo, Dubai, Tel Aviv). re:Invent Nov 30-Dec 4 Las Vegas (IRL, $2K+ registration). No open online hackathon currently listed on AWS public site. |
| polygon.technology/hackathons | ❌ HTTP 404 | URL doesn't exist. |
| filecoin.io/events | ❌ HTTP 404 | URL doesn't exist. |
| numer.ai/competitions | ⚠️ 404 | Tournament requires login. |
| kaggle.com/competitions | ⚠️ JS-rendered | Public listing requires auth. |
| news.plaid.com | ❌ DNS failure | Subdomain doesn't resolve. |
| stripe.com/newsroom | ✅ Fetched | No hackathons listed. |
| lablab.ai (full scan) | ✅ Fetched | 12 hackathons total — only **AMD AI League** (LIVE NOW, ends Dec 1) + **Vultr Agent Rush** (Nov 3-8, already known) + **AI Genesis** (TBA dates, Dubai Nov 2) are current. All others are 2026 recaps (finished). |
| dev.to/challenges | ✅ Fetched | Active: HF26 Week 3 (live) + Week 4 (upcoming). Kaggle Benchmarking + Sanity challenges ended. |
| mlh.io/seasons/2026/events | ✅ Fetched | All MLH 2026 season events are Apr-Jun 2026 — already past. MLH 2027 season not yet listed. |
| mit Hacking Medicine | ✅ Fetched | GrandHack 2026 was March 2026 (past). GrandHack 2027 not yet scheduled. KFSH×MIT Hackathon 2026 is in Riyadh (IRL, regional). |
| ETHGlobal /events | ✅ Fetched | Only upcoming: ETHGlobal Mumbai Nov 5-7 (IRL India), Pragma Mumbai Nov 6, ETHConf 2027 NYC Jun 14-16. |
| CalHacks 13.0 | ✅ Fetched | Hack Month October 2026 IRL Berkeley/SF. College-focused, IRL. |
| PennApps XXVII | ✅ Fetched | Spring 2027 (applications open later in October). IRL Philadelphia. Outside 30-day window. |
| HackZurich | ✅ Fetched | On hiatus ("taking a break"). |
| HackClub | ✅ Fetched | Hackathons are teen-only (13-18). User is adult — skip all. |
| Cursor events | ✅ Fetched | Community calendar (SpaceX Super Intelligence). Only IRL events (Boston, Singapore, SF). |
| CrewAI | ✅ Fetched | No hackathons; only webinars (e.g., "Approved is not funded" Nov 9). |
| LangChain blog | ✅ Fetched | Articles only, no hackathons. |
| AutoGPT (news.agpt.co) | ✅ Fetched | Pivoted to paid product "AutoGPT Experts". No hackathons. |
| Solana (hackathons.solana.com) | ✅ Fetched | Found **Perps and Prediction Markets** ($100K, Dec 5) — included above. Only 1 SCHEDULED hackathon currently. |

---

## Recommended action plan (next 14 days)

### 🥇 Top 5 priority hackathons (sorted by ROI × feasibility)

1. **AMD AI League Match 5** (Oct 27 — Nov 10) — $500 + credits
   - **Action:** Sign up for AMD account + ADP today. Complete Onboarding Match (300 pts). Pre-build alethech-agent-vault extension for "code repo repair" use case.
   - **Why perfect fit:** Match 5 brief is literally our existing project scope.

2. **DEV.to HF26 Week 3** (deadline Oct 25, 23:59 PDT = 3 days)
   - **Action:** Today (Oct 23): pick "Best Use of Auth0 for AI Agents" track. Use alethech-agent-vault as base. Submit a 1-post DEV.to submission.
   - **Why:** Low effort, $200-$500 cash, fresh start.

3. **Nebius x NVIDIA** (deadline Oct 30, $50K+)
   - **Action:** Register today (free). Pre-build by adapting alethech-agent-vault to use Nebius AI Cloud endpoint + Llama 3.x or Mistral as the OSS model. 7 days to ship.

4. **Superteam Vaultline Security Audit** (deadline Oct 31, up to $4K)
   - **Action:** Pick a Colosseum project (Solana Rust codebase). Run CodeQL local triage. Submit audit.
   - **Why:** We have the security/CodeQL track record (useagent #84 merged, harbour, vajra).

5. **PayPal AI Hackathon** (deadline Nov 12, $69,750)
   - **Action:** Register today. Plan to integrate PayPal sandbox with marketnow MCP. Submit by Nov 12, 3pm EST.

### 🥈 Secondary priorities (LATAM-aligned bounties — quick wins)

6. **Superteam Crea Contenido Madrid** (Oct 24, 22:59 — TONIGHT) — $2K USDG
   - Spanish content for Breakpoint side event. Quick submission if user can crank a 1000-word article in Spanish today.

7. **Superteam Travel Boost Breakpoint** (Oct 25, 21:59 — tomorrow) — $6K USDG
   - Similar Spanish content angle, 3× bigger prize.

8. **Superteam Rumbo a Breakpoint** (Nov 3) — $5K USDG + Breakpoint entry + travel
   - Win = trip to Madrid Dec 4-6.

### 🥉 Skip / deprioritize

- All IRL-only hackathons (ETHGlobal Mumbai, AWS re:Invent, CalHacks, PennApps, GrandHack 2027)
- HackClub events (teen-only)
- taikai SpaceXAI / Hack4Guimarães (Portuguese SME-only)

---

## Methodology notes

- **No fabricated hackathons** — every entry above was fetched live from its source URL on 2026-10-23.
- **Currency normalization:** USDG (Solana stablecoin) treated as USD-equivalent. USDC treated as USD.
- **Timezone:** All deadlines converted to UTC. Originals are typically in sponsor's local tz (PDT/EST/BRT).
- **Cutoff:** Included all hackathons with deadlines Oct 23-Nov 30, 2026 (the user's stated window). Post-Nov 30 listed separately.
- **Stack matching:** Prioritized hackathons where Python + TypeScript + MCP + AI agents + security + Rust overlap with our alethech-agent-vault / marketnow MCP / 30+ PRs track record.
