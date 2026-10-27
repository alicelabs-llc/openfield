#!/usr/bin/env python3
"""Consolidate all board results into a unified ranked list of actionable roles."""
import json, re, html
from pathlib import Path

ROOT = Path("/home/z/my-project/jobboards")

# LLC skill profile (Ecuador-based, 100% remote)
LLC_SKILLS_TEXT = (
    "AI agents, Python, FastAPI, Docker, GitLab/GitHub automation, webhooks, "
    "security sandboxing, tamper-evident provenance, devtools, MCP"
)

def load(name, *paths):
    p = ROOT / name / "filtered.json"
    if not p.exists():
        for path in paths:
            if Path(path).exists():
                p = Path(path)
                break
        else:
            return []
    try:
        return json.load(open(p))
    except Exception as e:
        print(f"Error loading {p}: {e}")
        return []

remoteok = load("remoteok")
wwr = load("wwr")
hn = load("hn")
pyjobs = load("python-org")
linkedin = load("linkedin")
landing = load("landingjobs")
wellfound_detail = ROOT / "wellfound" / "jobs_detail.json"
wellfound = json.load(open(wellfound_detail)) if wellfound_detail.exists() else []

# Also list YC top 5 (manually picked from details) plus wellfound top picks
yc_picks = [
    {
        "company": "Luca IQ",
        "position": "AI Engineer",
        "url": "https://www.workatastartup.com/jobs/110614",
        "location": "Chicago, IL, US / Remote (US)",
        "type": "Full-time",
        "salary": "$100K - $200K",
        "stage": "YC",
        "skills_required": ["Python", "LLMs", "AI Agents", "document OCR", "structured data extraction"],
        "notes": "Own intelligence layer of tax-prep workflow; build agentic return review w/ citations; evaluation/observability systems.",
        "match_score": 5,
    },
    {
        "company": "COACH",
        "position": "Founding AI Engineer",
        "url": "https://www.workatastartup.com/jobs/111820",
        "location": "San Francisco, CA, US",
        "type": "Full-time",
        "salary": "$150K - $250K",
        "stage": "YC",
        "skills_required": ["Python", "SQL", "AI Agents", "ML models in production", "cloud infra"],
        "notes": "Build AI harness for agents that gather context, access tools, retain knowledge; evaluation/experimentation; production infra. SF/Paris team.",
        "match_score": 5,
    },
    {
        "company": "Torus",
        "position": "AI Engineer (physical infrastructure)",
        "url": "https://www.workatastartup.com/jobs/105565",
        "location": "San Francisco / Houston, TX",
        "type": "Full-time",
        "salary": "$150K - $250K + 0.25-0.50% equity",
        "stage": "YC",
        "skills_required": ["Python", "Rust", "TypeScript", "PyTorch/JAX", "LLM orchestration", "RAG"],
        "notes": "Generalist seat. From CAD/drawings ingestion to agent-generated outputs engineers trust. Fortune 500 customers.",
        "match_score": 5,
    },
    {
        "company": "Pluto",
        "position": "Founding Engineer (LinkedIn for agents)",
        "url": "https://www.workatastartup.com/jobs/115910",
        "location": "San Francisco, CA, US / New York, NY, US",
        "type": "Full-time",
        "salary": "$120K - $200K",
        "stage": "YC",
        "skills_required": ["TypeScript", "React", "Next.js", "Node.js", "PostgreSQL", "LLMs", "agents", "tool calling"],
        "notes": "$2.6M ARR. Building headless professional network for AI era. True 0-to-1 build with existing tech & data.",
        "match_score": 5,
    },
    {
        "company": "LemonLime",
        "position": "AI Engineer",
        "url": "https://www.workatastartup.com/jobs/94768",
        "location": "San Francisco, CA, US",
        "type": "Full-time",
        "salary": "$90K - $120K",
        "stage": "YC",
        "skills_required": ["Python", "TypeScript", "agent orchestration", "Postgres/Supabase", "Vercel", "evaluations"],
        "notes": "Automating sales/marketing for SMBs. Agent orchestration, retrieval, structured LLM outputs, evaluations, data pipelines, third-party integrations.",
        "match_score": 4,
    },
    {
        "company": "Bloomy",
        "position": "Founding Engineer",
        "url": "https://www.workatastartup.com/jobs/100730",
        "location": "US / Remote (US)",
        "type": "Full-time",
        "salary": "$175K - $200K",
        "stage": "YC",
        "skills_required": ["TypeScript", "React", "Postgres", "LLMs in production", "agents", "evals", "tool use", "context management"],
        "notes": "AI tutor K-12. ~50% shipping product, 25% agent infra, 25% talking to teachers. Agent orchestration as first-class eng problem.",
        "match_score": 4,
    },
    {
        "company": "Volaren Inc.",
        "position": "Software Engineer (investing agent)",
        "url": "https://www.workatastartup.com/jobs/111785",
        "location": "San Francisco, CA, US / Remote (US)",
        "type": "Full-time",
        "salary": "$50K -",
        "stage": "YC",
        "skills_required": ["Python", "data analysis", "Backend", "APIs", "data pipelines", "AI harnesses & agents"],
        "notes": "Deploy AI agents that run evals, review/optimize code, automate processes; deploy user-facing agents. Quant + fundamentals.",
        "match_score": 4,
    },
]

# Wellfound picks - manually extract details
def wf_parse(j):
    if not isinstance(j, dict):
        return None
    body = j.get('body', '')
    title = j.get('title', '')
    url = j.get('url', '')
    slug = j.get('slug', '')
    salary = j.get('salary', '')
    stage = j.get('stage', '')
    type_ = j.get('type', '')
    # Find company (right before "at" in title)
    company = ''
    m = re.match(r'(.+?)\s+at\s+(.+?)\s+•', title)
    if m:
        position = m.group(1).strip()
        company = m.group(2).strip()
    else:
        position = title
    # Find hires remotely / location
    remote_match = re.search(r'Hires remotely in\s*\n([^\n]+)', body)
    if remote_match:
        remote_hires = remote_match.group(1).strip()[:200]
    else:
        remote_hires = ''
    return {
        "company": company,
        "position": position,
        "url": url,
        "slug": slug,
        "salary": salary,
        "stage": stage,
        "type": type_,
        "remote_hires": remote_hires,
        "notes": "",
        "match_score": 0,  # to be set manually
    }

wf_picks = []
for j in wellfound:
    p = wf_parse(j)
    if p:
        wf_picks.append(p)

# Manually score Wellfound picks
wf_scores = {
    "4884757-senior-applied-ai-engineer-i": (5, "Juniper Square", "Senior Applied AI Engineer I", "$165K-$200K", "Remote (US)", "Full-time", "Building JunieAI: AI platform for private markets. Embed intelligence across workflows."),
    "4884694-senior-software-engineer-platform": (4, "CreativeX", "Senior Software Engineer, Platform", "$132K-$162K", "Portland (hybrid)", "Full-time", "AI-first marketing creative control; computer vision + ML at scale. NOTE: hybrid Portland, NOT full-remote — partial match."),
    "4881335-senior-backend-engineer-integrations-platform": (5, "FutureFit AI", "Senior Backend Engineer (Integrations & Platform)", "$150K-$185K", "Remote (US/Canada)", "Full-time", "Backend for AI-powered career GPS. Complex data integrations with government/enterprise partners. Remove manual operational work."),
    "4875122-lead-database-data-platform-engineer": (4, "Strider", "Lead Database & Data Platform Engineer", "$60K-$96K", "Remote only", "Full-time", "Lead DB & data platform. NOTE: Salary low for lead ($60k-$96k) but stage=strider could be international. Verify."),
    "3670454-senior-full-stack-engineer-core-ux-usa": (3, "Kalepa", "Senior Full Stack Engineer - Core UX (USA)", "n/a", "Remote (US)", "Full-time", "Full-stack role, USA-only. Stretch fit — strong on React+Python; verify they hire outside US."),
    "4884710-recruiting-operations-specialist-contract": (2, "Labelbox", "Recruiting Operations Specialist (Contract)", "n/a", "San Francisco", "Contract", "CONTRACT role but recruiting ops, NOT engineering. Discard as engineering match."),
    "4196821-technical-support-engineer": (4, "Kalepa", "Technical Support Engineer", "$85K-$135K", "Remote (US)", "Full-time", "Support eng, USA-only. Lower match (support not backend engineering) but reasonable."),
    "4846255-support-engineer": (3, "MOLTEN Cloud", "Support Engineer", "n/a", "Remote", "Full-time", "Early stage. Cloud support eng."),
    "4867181-software-data-engineer": (3, "Alto Cirra", "Software & Data Engineer", "$115K-$155K", "Salt Lake City", "Full-time", "SWE+Data eng. SLC — verify remote."),
    "3154038-senior-solutions-engineer": (4, "Cyberhaven", "Senior Solutions Engineer", "n/a", "Remote", "Full-time", "Security/data provenance adjacent. Scale-stage. Solutions eng = customer-facing eng, not pure backend."),
    "3994821-2-data-engineer-staff-principal-lead": (3, "Unknown", "Data Engineer (Staff, Principal, Lead)", "n/a", "Remote", "Full-time", "Senior data eng role."),
    "4875217-account-executive-ai-x-fintech": (1, "Unknown", "Account Executive, AI x Fintech", "n/a", "Remote", "Full-time", "Sales, NOT engineering. Discard."),
}

wf_top = []
for p in wf_picks:
    slug = p["slug"]
    if slug in wf_scores:
        sc, company, position, salary, location, type_, notes = wf_scores[slug]
        p["match_score"] = sc
        p["company"] = company
        p["position"] = position
        p["salary"] = salary
        p["location"] = location
        p["type"] = type_
        p["notes"] = notes
        wf_top.append(p)

# Combine all into unified list
all_roles = []

# HN matches - the richest source
for r in hn[:40]:
    if r["match_score"] >= 4:
        all_roles.append({
            "source": "HN Ask HN: Who is hiring? (Oct 2026)",
            "company": r["first_line"].split("|")[0].strip()[:80],
            "position": re.search(r'\|\s*([^\|]+?)\s*\|', r["first_line"]),
            "position": (r["first_line"].split("|")[1].strip()[:120] if "|" in r["first_line"] else r["first_line"][:120]),
            "url": r["url"],
            "type": "contract/freelance/full-time (per comment)",
            "location": r["first_line"].split("|")[2].strip()[:80] if r["first_line"].count("|") >= 3 else "see comment",
            "salary": "",
            "skills_required": r["matched_skills"],
            "contact_email": r["email"],
            "match_score": r["match_score"],
            "notes": r["text_excerpt"][:300],
        })

# Python.org jobs - very high quality
for r in pyjobs[:15]:
    if r["match_score"] >= 4:
        all_roles.append({
            "source": "python.org/jobs",
            "company": r["title"].split(",")[-1].strip() if "," in r["title"] else "",
            "position": r["title"].split(",")[0].strip() if "," in r["title"] else r["title"],
            "url": r["link"],
            "type": "varies",
            "location": "",
            "salary": "",
            "skills_required": r["matched_skills"],
            "contact_email": "",
            "match_score": r["match_score"],
            "notes": r["description_excerpt"][:300],
        })

# RemoteOK matches
for r in remoteok[:15]:
    if r["match_score"] >= 4:
        sal = ""
        if r.get("salary_min") and r.get("salary_max"):
            sal = f"${r['salary_min']/1000:.0f}k-${r['salary_max']/1000:.0f}k/yr"
        elif r.get("salary_max"):
            sal = f"up to ${r['salary_max']/1000:.0f}k/yr"
        all_roles.append({
            "source": "RemoteOK",
            "company": r["company"],
            "position": r["position"],
            "url": r["url"],
            "apply_url": r.get("apply_url"),
            "type": ", ".join(r["tags"][:5]),
            "location": r["location"] or "Remote (worldwide)",
            "salary": sal,
            "skills_required": r["matched_skills"],
            "contact_email": "",
            "match_score": r["match_score"],
            "notes": "",
        })

# WWR matches
for r in wwr[:15]:
    if r["match_score"] >= 4:
        all_roles.append({
            "source": "We Work Remotely",
            "company": r["company"],
            "position": r["position"],
            "url": r["link"],
            "type": r["type"],
            "location": r["region"],
            "salary": "",
            "skills_required": r["matched_skills"],
            "contact_email": "",
            "match_score": r["match_score"],
            "notes": r["description_excerpt"][:300],
        })

# LinkedIn matches
for r in linkedin[:15]:
    if r["match_score"] >= 3:
        all_roles.append({
            "source": "LinkedIn guest API",
            "company": r["company"],
            "position": r["title"],
            "url": r["url"],
            "type": "",
            "location": r["location"],
            "salary": "",
            "skills_required": r["matched_skills"],
            "contact_email": "",
            "match_score": r["match_score"],
            "notes": f"Query: {r['query']}",
        })

# Landing.jobs
for r in json.load(open(ROOT / "landingjobs" / "filtered.json")):
    if r["match_score"] >= 3:
        all_roles.append({
            "source": "Landing.jobs",
            "company": r["company"],
            "position": r["title"],
            "url": r["url"],
            "type": r["contract_type"],
            "location": r["remote_label"][:100],
            "salary": "",
            "skills_required": r["skills"] + r["matched_skills"],
            "contact_email": "",
            "match_score": r["match_score"],
            "notes": f"Industry: {r['industry']}",
        })

# YC picks
for r in yc_picks:
    all_roles.append({
        "source": "YC Work at a Startup",
        "company": r["company"],
        "position": r["position"],
        "url": r["url"],
        "type": r["type"],
        "location": r["location"],
        "salary": r["salary"],
        "skills_required": r["skills_required"] if isinstance(r["skills_required"], list) else [r["skills_required"]],
        "contact_email": "",
        "match_score": r["match_score"],
        "notes": r["notes"],
    })

# Wellfound picks
for r in wf_top:
    if r["match_score"] >= 4:
        all_roles.append({
            "source": "Wellfound",
            "company": r["company"],
            "position": r["position"],
            "url": r["url"],
            "type": r["type"],
            "location": r["location"],
            "salary": r["salary"],
            "skills_required": [],
            "contact_email": "",
            "match_score": r["match_score"],
            "notes": r["notes"],
        })

# Sort by score
all_roles.sort(key=lambda x: -x["match_score"])

# Save full
json.dump(all_roles, open(ROOT / "all_roles.json", "w"), indent=2, ensure_ascii=False)
print(f"Total consolidated roles (score>=3 from any board): {len(all_roles)}")

# Stats by score
from collections import Counter
c = Counter(r["match_score"] for r in all_roles)
for sc in sorted(c.keys(), reverse=True):
    print(f"  ★{sc}: {c[sc]} roles")

# Stats by source
c2 = Counter(r["source"] for r in all_roles)
print("\nBy source:")
for s, n in c2.most_common():
    print(f"  {s}: {n}")
