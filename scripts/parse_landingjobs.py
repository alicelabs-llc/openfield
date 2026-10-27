#!/usr/bin/env python3
"""Parse Landing.jobs JSON search results and filter for LLC matches."""
import json, os
from pathlib import Path

LJ_DIR = Path("/home/z/my-project/jobboards/landingjobs")
OUT = Path("/home/z/my-project/jobboards/landingjobs/filtered.json")
OUT_MD = Path("/home/z/my-project/jobboards/landingjobs/matches.md")

SKILLS = {
    "ai_agent": ["ai agent", "ai agents", "llm", "agent framework", "langchain",
                 "multi-agent", "mcp server", "model context protocol", "rag",
                 "agentic", "genai", "gen ai", "generative ai", "machine learning"],
    "python": ["python", "fastapi", "pydantic", "asyncio", "uvicorn", "celery",
               "django", "flask"],
    "docker": ["docker", "container", "kubernetes", "k8s"],
    "gitlab": ["gitlab"],
    "github": ["github actions", "github api", "gh cli", "github"],
    "webhook": ["webhook", "event-driven", "event driven"],
    "security": ["security", "sandbox", "sandboxing", "tamper", "provenance",
                 "secret scanning", "vulnerability", "infosec", "appsec"],
    "automation": ["automation", "ci/cd", "ci cd", "pipeline", "devops",
                   "platform engineer", "sre", "infrastructure"],
    "backend": ["backend", "back-end", "fullstack", "full-stack"],
    "contract": ["contract", "freelance", "part-time", "part time", "b2b",
                 "consulting", "consultant", "fractional", "contractor"],
}

def score(text):
    ntext = text.lower()
    matched = []
    for skill, kws in SKILLS.items():
        if any(kw in ntext for kw in kws):
            matched.append(skill)
    core = {"ai_agent", "python", "gitlab", "github", "security", "automation",
            "docker", "webhook"}
    core_hits = [s for s in matched if s in core]
    score = 1
    if len(core_hits) >= 5: score = 5
    elif len(core_hits) >= 3: score = 4
    elif len(core_hits) >= 2: score = 3
    elif len(core_hits) >= 1: score = 2
    if "contract" in matched: score = min(5, score + 1)
    return score, matched, core_hits

def main():
    all_offers = {}
    for f in sorted(os.listdir(LJ_DIR)):
        if not f.endswith(".json"):
            continue
        path = LJ_DIR / f
        try:
            d = json.load(open(path))
        except Exception as e:
            print(f"Error loading {f}: {e}")
            continue
        offers = d.get("offers", [])
        print(f"{f}: {len(offers)} offers")
        for o in offers:
            all_offers[o["id"]] = o
    print(f"Unique offers: {len(all_offers)}")
    results = []
    for o in all_offers.values():
        skills_list = [s["name"] for s in o.get("skills", [])]
        text = f"{o.get('title','')} {' '.join(skills_list)} {o.get('industry','')} {o.get('contract_type','')}"
        sc, matched, core_hits = score(text)
        results.append({
            "id": o["id"],
            "title": o.get("title"),
            "company": o.get("company_name"),
            "company_url": o.get("company_url"),
            "remote": o.get("remote"),
            "full_remote": o.get("full_remote"),
            "remote_label": o.get("remote_label"),
            "contract_type": o.get("contract_type"),
            "experience_level": o.get("experience_level"),
            "published_at": o.get("published_at"),
            "industry": o.get("industry"),
            "skills": skills_list,
            "url": f"https://landing.jobs/jobs/{o.get('slug')}",
            "matched_skills": matched,
            "core_hits": core_hits,
            "match_score": sc,
        })
    results = [r for r in results if r["match_score"] >= 3]
    results.sort(key=lambda x: (-x["match_score"], x["published_at"] or ""))
    json.dump(results, open(OUT, "w"), indent=2, ensure_ascii=False)
    print(f"Saved {len(results)} matched Landing.jobs offers")
    with open(OUT_MD, "w") as f:
        f.write(f"# Landing.jobs matches ({len(results)})\n\n")
        for r in results[:30]:
            f.write(f"## {r['title']} @ {r['company']}  (★{r['match_score']})\n")
            f.write(f"- **Remote:** {r['remote_label'] or 'n/a'}\n")
            f.write(f"- **Contract type:** {r['contract_type'] or 'n/a'} | **Level:** {r['experience_level'] or 'n/a'}\n")
            f.write(f"- **Skills:** {', '.join(r['skills'])}\n")
            f.write(f"- **Industry:** {r['industry']}\n")
            f.write(f"- **Date:** {r['published_at']}\n")
            f.write(f"- **Matched:** {', '.join(r['matched_skills'])}\n")
            f.write(f"- **URL:** {r['url']}\n\n")
    print(f"Markdown saved to {OUT_MD}")

if __name__ == "__main__":
    main()
