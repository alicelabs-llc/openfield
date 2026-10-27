#!/usr/bin/env python3
"""Parse RemoteOK API JSON and filter roles matching LLC skill profile."""
import json, re, html
from pathlib import Path

DATA = Path("/home/z/my-project/jobboards/remoteok/api.json")
OUT = Path("/home/z/my-project/jobboards/remoteok/filtered.json")
OUT_MD = Path("/home/z/my-project/jobboards/remoteok/matches.md")

# LLC skills comprobadas
SKILLS = {
    "ai_agent": ["ai agent", "ai agents", "llm", "agent framework", "autogen",
                 "langchain", "multi-agent", "mcp server", "function calling",
                 "tools calling", "model context protocol"],
    "python": ["python", "fastapi", "pydantic", "asyncio", "starlette", "uvicorn",
               "celery"],
    "docker": ["docker", "container", "compose", "kubernetes", "k8s"],
    "gitlab": ["gitlab", "gitlab ci", "gitlab-runner"],
    "github": ["github actions", "github api", "gh cli"],
    "webhook": ["webhook", "event-driven", "event driven"],
    "security": ["security", "sandbox", "sandboxing", "tamper", "provenance",
                 "secret scanning", "vulnerability"],
    "automation": ["automation", "ci/cd", "ci cd", "pipeline", "devops",
                   "platform engineer"],
    "backend": ["backend", "back-end", "fullstack", "full-stack", "api design",
                "rest api"],
    "contract": ["contract", "freelance", "part-time", "part time", "b2b",
                 "consulting", "consultant"],
}

def normalize(s):
    return html.unescape(s or "").lower()

def score_job(job):
    text = " ".join([
        job.get("position", ""),
        job.get("description", ""),
        job.get("tags", "") if isinstance(job.get("tags"), str) else " ".join(job.get("tags", []) or []),
        job.get("location", ""),
        job.get("company", ""),
    ])
    ntext = normalize(text)
    matched = []
    for skill, kws in SKILLS.items():
        if any(kw in ntext for kw in kws):
            matched.append(skill)
    # Score 1-5 based on overlap with core skills
    core = {"ai_agent", "python", "gitlab", "github", "security", "automation", "docker", "webhook"}
    core_hits = [s for s in matched if s in core]
    score = 1
    if len(core_hits) >= 5: score = 5
    elif len(core_hits) >= 3: score = 4
    elif len(core_hits) >= 2: score = 3
    elif len(core_hits) >= 1: score = 2
    # Boost contract roles
    if "contract" in matched: score = min(5, score + 1)
    return score, matched, core_hits

def main():
    d = json.load(open(DATA))
    if not isinstance(d, list):
        return
    jobs = [e for e in d if "slug" in e and "position" in e]
    print(f"Total jobs in API: {len(jobs)}")
    results = []
    for j in jobs:
        score, matched, core_hits = score_job(j)
        if score >= 3:
            tags = j.get("tags", [])
            if isinstance(tags, str):
                tags = [tags]
            results.append({
                "id": j.get("id"),
                "company": html.unescape(j.get("company", "")),
                "position": html.unescape(j.get("position", "")),
                "tags": tags,
                "location": j.get("location", ""),
                "salary_min": j.get("salary_min"),
                "salary_max": j.get("salary_max"),
                "date": j.get("date", ""),
                "url": f"https://remoteok.com/remote-jobs/{j.get('id')}",
                "apply_url": j.get("url"),
                "matched_skills": matched,
                "core_hits": core_hits,
                "match_score": score,
            })
    results.sort(key=lambda x: (-x["match_score"], x["date"]))
    json.dump(results, open(OUT, "w"), indent=2, ensure_ascii=False)
    print(f"Saved {len(results)} matched roles (score>=3) to {OUT}")
    # Markdown
    with open(OUT_MD, "w") as f:
        f.write(f"# RemoteOK matches ({len(results)} roles, score >=3)\n\n")
        for r in results[:40]:
            sal = ""
            if r["salary_min"] and r["salary_max"]:
                sal = f"`${r['salary_min']/1000:.0f}k–${r['salary_max']/1000:.0f}k/yr`"
            elif r["salary_max"]:
                sal = f"`up to ${r['salary_max']/1000:.0f}k/yr`"
            tags = ", ".join(r["tags"][:8]) if r["tags"] else "n/a"
            f.write(f"## {r['position']} @ {r['company']}  (★{r['match_score']})\n")
            f.write(f"- **Tags:** {tags}\n")
            f.write(f"- **Location:** {r['location'] or 'Remote (worldwide)'}\n")
            f.write(f"- **Salary:** {sal or 'not listed'}\n")
            f.write(f"- **Date:** {r['date'][:10]}\n")
            f.write(f"- **Matched skills:** {', '.join(r['matched_skills'])}\n")
            f.write(f"- **URL:** {r['url']}\n")
            if r["apply_url"] and r["apply_url"] != r["url"]:
                f.write(f"- **Apply:** {r['apply_url']}\n")
            f.write("\n")
    print(f"Markdown saved to {OUT_MD}")

if __name__ == "__main__":
    main()
