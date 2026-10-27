#!/usr/bin/env python3
"""Parse WWR RSS feed and filter for LLC-matching roles."""
import re, html
import xml.etree.ElementTree as ET
from pathlib import Path

RSS = Path("/home/z/my-project/jobboards/wwr/all.rss")
OUT = Path("/home/z/my-project/jobboards/wwr/filtered.json")
OUT_MD = Path("/home/z/my-project/jobboards/wwr/matches.md")

SKILLS = {
    "ai_agent": ["ai agent", "ai agents", "llm", "agent framework", "langchain",
                 "multi-agent", "mcp server", "model context protocol", "rag",
                 "generative ai", "ai engineering"],
    "python": ["python", "fastapi", "pydantic", "asyncio", "uvicorn", "celery",
               "django"],
    "docker": ["docker", "container", "kubernetes", "k8s"],
    "gitlab": ["gitlab"],
    "github": ["github actions", "github api", "gh cli"],
    "webhook": ["webhook", "event-driven", "event driven"],
    "security": ["security", "sandbox", "sandboxing", "tamper", "provenance",
                 "secret scanning", "vulnerability", "infosec", "appsec"],
    "automation": ["automation", "ci/cd", "ci cd", "pipeline", "devops",
                   "platform engineer", "sre"],
    "backend": ["backend", "back-end", "fullstack", "full-stack", "api"],
    "contract": ["contract", "freelance", "part-time", "part time", "b2b",
                 "consulting", "consultant"],
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
    # Strip namespace for simplicity
    text = re.sub(r'xmlns:[a-z]+="[^"]+"', "", text)
    text = text.replace("media:content", "media_content").replace("dc:creator", "dc_creator")
    root = ET.fromstring(text)
    items = root.findall(".//item")
    print(f"Total items: {len(items)}")
    results = []
    for it in items:
        title = it.findtext("title") or ""
        link = it.findtext("link") or ""
        desc_raw = it.findtext("description") or ""
        region = it.findtext("region") or ""
        cat = it.findtext("category") or ""
        type_ = it.findtext("type") or ""
        skills_tag = it.findtext("skills") or ""
        desc = strip_html(desc_raw)
        company = ""
        m = re.match(r"^(.+?):\s*(.+)$", title)
        if m:
            company, position = m.group(1), m.group(2)
        else:
            position = title
        full_text = f"{title} {desc} {skills_tag} {cat} {type_}"
        sc, matched, core_hits = score(full_text)
        if sc >= 3:
            results.append({
                "company": company,
                "position": position,
                "category": cat,
                "type": type_,
                "region": region,
                "skills": skills_tag,
                "description_excerpt": desc[:400],
                "link": link,
                "matched_skills": matched,
                "core_hits": core_hits,
                "match_score": sc,
            })
    results.sort(key=lambda x: (-x["match_score"], x["company"]))
    import json
    json.dump(results, open(OUT, "w"), indent=2, ensure_ascii=False)
    print(f"Saved {len(results)} matched roles (score>=3) to {OUT}")
    with open(OUT_MD, "w") as f:
        f.write(f"# We Work Remotely matches ({len(results)} roles, score >=3)\n\n")
        for r in results[:50]:
            f.write(f"## {r['position']} @ {r['company']}  (★{r['match_score']})\n")
            f.write(f"- **Category:** {r['category'] or 'n/a'} | **Type:** {r['type'] or 'n/a'}\n")
            f.write(f"- **Region:** {r['region'] or 'Anywhere'}\n")
            f.write(f"- **Skills:** {r['skills'] or 'n/a'}\n")
            f.write(f"- **Matched:** {', '.join(r['matched_skills'])}\n")
            f.write(f"- **URL:** {r['link']}\n")
            f.write(f"- **Excerpt:** {r['description_excerpt'][:300]}…\n\n")
    print(f"Markdown saved to {OUT_MD}")

if __name__ == "__main__":
    main()
