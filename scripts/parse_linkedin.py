#!/usr/bin/env python3
"""Parse LinkedIn public guest API HTML responses and extract job postings."""
import re, html, json, os
from pathlib import Path

LINKEDIN_DIR = Path("/home/z/my-project/jobboards/linkedin")
OUT = Path("/home/z/my-project/jobboards/linkedin/filtered.json")
OUT_MD = Path("/home/z/my-project/jobboards/linkedin/matches.md")

SKILLS = {
    "ai_agent": ["ai agent", "ai agents", "llm", "agent framework", "langchain",
                 "multi-agent", "mcp server", "model context protocol", "rag",
                 "agentic", "genai", "gen ai", "generative ai"],
    "python": ["python", "fastapi", "pydantic", "asyncio", "uvicorn", "celery",
               "django", "flask"],
    "docker": ["docker", "container", "kubernetes", "k8s"],
    "gitlab": ["gitlab"],
    "github": ["github actions", "github api", "gh cli"],
    "webhook": ["webhook", "event-driven", "event driven"],
    "security": ["security", "sandbox", "sandboxing", "tamper", "provenance",
                 "secret scanning", "vulnerability", "infosec", "appsec"],
    "automation": ["automation", "ci/cd", "ci cd", "pipeline", "devops",
                   "platform engineer", "sre"],
    "backend": ["backend", "back-end", "fullstack", "full-stack"],
    "contract": ["contract", "freelance", "part-time", "part time", "b2b",
                 "consulting", "consultant", "fractional"],
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

def parse_one(html_text, query_label):
    """Extract job cards from one LinkedIn response."""
    out = []
    # Split by <li> entries
    items = re.split(r'<li>', html_text)
    for it in items:
        # extract job id
        mid = re.search(r'data-entity-urn="urn:li:jobPosting:(\d+)"', it)
        title = re.search(r'<h3 class="base-search-card__title">\s*(.*?)\s*</h3>', it, re.S)
        company = re.search(r'<h4 class="base-search-card__subtitle">.*?<a[^>]*>(.*?)</a>', it, re.S)
        location = re.search(r'<span class="job-search-card__location">\s*(.*?)\s*</span>', it, re.S)
        date = re.search(r'datetime="([^"]+)"', it)
        url = re.search(r'href="(https://[^"]+linkedin\.com/jobs/view/[^"]+)"', it)
        if not (mid and title):
            continue
        def clean(x):
            if not x: return ""
            return re.sub(r"\s+", " ", html.unescape(x.strip())).strip()
        t = clean(title.group(1))
        c = clean(company.group(1)) if company else ""
        l = clean(location.group(1)) if location else ""
        u = url.group(1) if url else ""
        d = date.group(1) if date else ""
        # Score on combined text
        text = f"{t} {c} {query_label}"
        sc, matched, core_hits = score(text)
        out.append({
            "id": mid.group(1),
            "title": t,
            "company": c,
            "location": l,
            "date": d,
            "url": u.split("?")[0],
            "query": query_label,
            "matched_skills": matched,
            "core_hits": core_hits,
            "match_score": sc,
        })
    return out

def main():
    all_jobs = {}
    for f in sorted(os.listdir(LINKEDIN_DIR)):
        if not f.endswith(".html"):
            continue
        path = LINKEDIN_DIR / f
        if path.stat().st_size > 100000:
            continue  # 429 error page
        query_label = f.replace(".html", "")
        text = path.read_text(errors="ignore")
        jobs = parse_one(text, query_label)
        print(f"{f}: {len(jobs)} jobs")
        for j in jobs:
            all_jobs[j["id"]] = j
    results = list(all_jobs.values())
    # Score >= 3
    results = [r for r in results if r["match_score"] >= 3]
    results.sort(key=lambda x: (-x["match_score"], x["date"]))
    json.dump(results, open(OUT, "w"), indent=2, ensure_ascii=False)
    print(f"Saved {len(results)} matched LinkedIn roles (score>=3) to {OUT}")
    with open(OUT_MD, "w") as f:
        f.write(f"# LinkedIn guest API matches ({len(results)})\n\n")
        for r in results[:40]:
            f.write(f"## {r['title']} @ {r['company']}  (★{r['match_score']})\n")
            f.write(f"- **Location:** {r['location'] or 'n/a'} | **Date:** {r['date']}\n")
            f.write(f"- **Query:** {r['query']}\n")
            f.write(f"- **Matched:** {', '.join(r['matched_skills'])}\n")
            f.write(f"- **URL:** {r['url']}\n\n")
    print(f"Markdown saved to {OUT_MD}")

if __name__ == "__main__":
    main()
