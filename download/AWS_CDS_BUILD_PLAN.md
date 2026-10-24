# AWS CDS Agentic AI Partner Hackathon — Build Plan

**Deadline:** October 28, 2026 @ 1:00pm PT (8pm UTC) — 5 days from Oct 24
**Prize target:** 1st Place $18,000 USD (+ Best WhatsApp $10,000 bonus potential)
**Ecuador eligible:** ✅ (same exclusion list as GitLab Transcend)

---

## PROJECT CONCEPT

### Name: **"Mailhand" — Agentic Email Code Review via AWS SES + Bedrock**

An agentic AI service that turns any developer's inbox into a code review queue. Developers CC `review@mailhand.example.com` on a GitLab/GitHub PR notification email, and the agent:

1. **Receives the email via AWS SES** (incoming email setup)
2. **Parses the PR URL** from the email body
3. **Fetches the diff** via the Git host's API
4. **Runs an agentic review loop** with Bedrock AgentCore:
   - Plan: identify risk areas in the diff
   - Execute: run security/static analysis tools in a sandbox
   - Synthesize: write a structured review with severity ratings
5. **Replies via AWS SES** with the review attached as markdown + posted as PR comment via API
6. **Sends a WhatsApp summary** via AWS End User Messaging Social (for the "Best WhatsApp Solution" bonus)

The agentic angle: the review isn't a single LLM call — it's a Bedrock AgentCore agent that iterates (plan→execute→retry→synthesize), with each step captured.

---

## TECH STACK

| Component | AWS Service | Why |
|-----------|-------------|-----|
| Email receiving | **AWS SES incoming** | Required by hackathon (must use SES, EUM, or WhatsApp) |
| Email sending | **AWS SES outgoing** | Reply with review |
| Agent runtime | **Amazon Bedrock AgentCore** | Recommended by hackathon, agentic AI |
| LLM | **Bedrock Claude 3.5 Sonnet** | For code reasoning |
| WhatsApp notifications | **AWS End User Messaging Social** | For Best WhatsApp bonus prize |
| Compute (sandbox) | **AWS Lambda + container image** | Run static analysis tools isolated |
| State | **DynamoDB** | Track review sessions |
| Deployment | **AWS App Runner** | Simple deploy |
| Repo | **GitHub** (public, MIT) | Required |

---

## SUBMISSION CHECKLIST

### Required:
- [ ] AWS Partner Network registration (15 min) — **USER ACTION REQUIRED**
- [ ] ACE opportunity ID created in Partner Central — **USER ACTION REQUIRED**
- [ ] Public code repository (GitHub, MIT license)
- [ ] Architecture diagram (PNG)
- [ ] Text description (~500 words)
- [ ] Demo video (~3 min, YouTube link)
- [ ] Deployed project URL

### Bonus:
- [ ] Use AWS End User Messaging Social (WhatsApp) — qualifies for $10K bonus
- [ ] Use Amazon Bedrock AgentCore — recommended by hackathon
- [ ] Use multiple CDS services (SES + WhatsApp) — strengthens submission

---

## ARCHITECTURE DIAGRAM

```
┌──────────────────────────────────────────────────────────────────┐
│ Developer inbox (Gmail/Outlook/any)                              │
│  ├─ Forwards PR notification email to review@mailhand.example.com│
└──────────────────────────┬───────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│ AWS SES (incoming email)                                          │
│  - Receipt rule triggers Lambda                                   │
└──────────────────────────┬───────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│ Lambda: mailhand-router                                           │
│  - Parse email body                                               │
│  - Extract PR URL                                                │
│  - Create review session in DynamoDB                             │
└──────────────────────────┬───────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│ Bedrock AgentCore agent (Mailhand Review Agent)                  │
│                                                                   │
│  Plan:                                                            │
│   - Fetch diff from GitHub/GitLab API                            │
│   - Identify risk areas (security, perf, correctness)             │
│                                                                   │
│  Execute (in Lambda sandbox):                                     │
│   - Run semgrep/bandit/eslint on diff                           │
│   - Capture findings                                             │
│                                                                   │
│  Synthesize:                                                      │
│   - Generate structured review (severity, line, suggestion)      │
│   - Markdown format                                              │
└──────────────────────────┬───────────────────────────────────────┘
                           │
              ┌────────────┴───────────┐
              ▼                        ▼
┌──────────────────────────┐  ┌──────────────────────────────────┐
│ AWS SES (outgoing)       │  │ AWS End User Messaging Social    │
│  - Email review to dev   │  │  - WhatsApp summary to dev       │
│  - Markdown attachment    │  │  - "Review complete: 3 findings" │
└──────────────────────────┘  └──────────────────────────────────┘
                           │
                           ▼
                  PR comment via
                  Git host API
```

---

## DEMO VIDEO SCRIPT (3 min)

[0:00] "Hi, I'm Edison. This is Mailhand, a submission for the AWS CDS Agentic AI Partner Hackathon. The idea is simple: turn any developer's inbox into an agentic code review queue."

[0:15] **Setup** — Show a Gmail inbox. Forward a GitHub PR notification to `review@mailhand.example.com`.

[0:30] **SES receives** — Show CloudWatch logs of SES receiving the email, Lambda triggering.

[0:45] **Agent runs** — Show Bedrock AgentCore agent plan: fetch diff, identify risks, run semgrep, synthesize review. Show the agent's tool calls.

[1:15] **WhatsApp notification** — Show phone receiving WhatsApp message via AWS End User Messaging Social: "Mailhand: review complete. 3 findings: 1 high, 2 medium."

[1:30] **Email reply** — Show Gmail receiving the full review markdown, with code snippets and severity ratings.

[1:45] **PR comment** — Show the GitHub PR with the agent's review posted as a comment.

[2:00] **Architecture** — Show diagram, explain AWS services used (SES in/out, Bedrock AgentCore, EUM Social, Lambda, DynamoDB, App Runner).

[2:30] **Why agentic** — "This isn't a single LLM call. The agent plans, executes static analysis in a sandbox, synthesizes a structured review, and reports across multiple channels. Each step is logged."

[2:45] "Try it yourself — repo link in description."

[3:00] End.

---

## TODO (5 days)

### Day 1 (Oct 24)
- [ ] User: register AWS Partner Network (15 min)
- [ ] User: create ACE opportunity in Partner Central (5 min)
- [ ] Set up AWS account (if not already)
- [ ] Provision SES (verify domain or use sandbox mode)
- [ ] Provision Bedrock AgentCore
- [ ] Create GitHub repo `mailhand-aws-cds` (MIT)

### Day 2 (Oct 25)
- [ ] Implement `mailhand-router` Lambda
- [ ] Implement SES receipt rule
- [ ] Implement Bedrock AgentCore agent
- [ ] Test end-to-end with sandbox SES

### Day 3 (Oct 26)
- [ ] Implement WhatsApp notification via AWS End User Messaging Social
- [ ] Implement PR comment via Git host API (GitHub + GitLab)
- [ ] Deploy to AWS App Runner

### Day 4 (Oct 27)
- [ ] Record 3-min demo video
- [ ] Upload to YouTube (unlisted OK)
- [ ] Write architecture diagram (PNG)
- [ ] Write text description (500 words)

### Day 5 (Oct 28 before 1pm PT)
- [ ] Final review of all submission components
- [ ] SUBMIT on Devpost
- [ ] Cross fingers

---

## USER ACTION REQUIRED

**The hackathon REQUIRES AWS Partner Network registration. This is a 15-min manual signup that I cannot do for you (would violate ToS).**

1. Go to https://partners.amazonaws.com/
2. Click "Join AWS Partner Network"
3. Register as an Individual Partner (free)
4. Once registered, go to Partner Central → ACE → Create Opportunity (this generates the required opportunity ID for submission)

**Without this, the submission will be rejected. Please do it TODAY.**

---

## REPO STRUCTURE

```
mailhand-aws-cds/
├── README.md
├── LICENSE (MIT)
├── architecture.png
├── sam-template.yaml          # AWS SAM deployment
├── src/
│   ├── mailhand_router.py     # Lambda for SES incoming
│   ├── review_agent.py        # Bedrock AgentCore agent
│   ├── ses_sender.py          # SES outgoing
│   ├── whatsapp_sender.py    # AWS End User Messaging Social
│   ├── pr_commenter.py        # Git host API integration
│   └── requirements.txt
├── tests/
│   ├── test_router.py
│   ├── test_agent.py
│   └── test_e2e.py
├── deploy/
│   ├── Dockerfile.lambda
│   └── app-runner.yaml
└── docs/
    ├── SUBMISSION_TEXT.md     # Devpost submission
    └── DEMO_SCRIPT.md
```
