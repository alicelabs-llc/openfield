#!/usr/bin/env python3
"""Parse python.org jobs RSS feed and filter for LLC matches."""
import re, html, json
import xml.etree.ElementTree as ET
from pathlib import Path

RSS = Path("/home/z/my-project/jobboards/python-org/feed.rss")
OUT = Path("/home/z/my-project/jobboards/python-org/filtered.json")
OUT_MD = Path("/home/z/my-project/jobboards/python-org/matches.md")

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

def strip_html(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = html.unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def main():
    text = RSS.read_text()
    # Strip atom namespace declaration to avoid unbound prefix errors
    text = re.sub(r'xmlns:atom="[^"]+"', '', text)
    text = re.sub(r'<atom:[^>]+>', '', text)
    root = ET.fromstring(text)
    items = root.findall(".//item")
    print(f"Total items: {len(items)}")
    results = []
    for it in items:
        title = it.findtext("title") or ""
        link = it.findtext("link") or ""
        desc_raw = it.findtext("description") or ""
        desc = strip_html(desc_raw)
        sc, matched, core_hits = score(f"{title} {desc}")
        if sc >= 3:
            results.append({
                "title": title,
                "link": link,
                "description_excerpt": desc[:600],
                "matched_skills": matched,
                "core_hits": core_hits,
                "match_score": sc,
            })
    results.sort(key=lambda x: -x["match_score"])
    json.dump(results, open(OUT, "w"), indent=2, ensure_ascii=False)
    print(f"Saved {len(results)} python.org matches")
    with open(OUT_MD, "w") as f:
        f.write(f"# Python.org Job Board matches ({len(results)})\n\n")
        for r in results[:30]:
            f.write(f"## {r['title']}  (★{r['match_score']})\n")
            f.write(f"- **Matched:** {', '.join(r['matched_skills'])}\n")
            f.write(f"- **URL:** {r['link']}\n")
            f.write(f"- **Excerpt:** {r['description_excerpt'][:400]}…\n\n")
    print(f"Markdown saved to {OUT_MD}")

if __name__ == "__main__":
    main()
