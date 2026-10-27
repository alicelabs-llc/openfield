#!/usr/bin/env python3
"""
Score Reddit leads based on LLC skill match.
LLC skills: AI agents (alethech-agent-vault Docker sandbox + provenance),
Python/FastAPI/Docker, GitLab/GitHub automation (webhooks, MR bots, Duo),
security sandboxing, devtools.

Skill buckets (1 point each, max 5):
- ai_agent: "AI agent", "LLM", "GPT", "agent", "RAG", "agentic"
- python: "Python", "FastAPI", "Django", "Flask", "pandas"
- docker: "Docker", "container", "sandbox"
- gitlab/github: "GitLab", "GitHub", "CI/CD", "webhook", "MR bot"
- security: "security", "sandbox", "tamper", "audit", "secret"
- automation: "automation", "automate", "script", "scraping", "workflow"
- backend: "backend", "API", "FastAPI", "REST"
- contract: "contract", "freelance", "hiring", "wanted", "looking for"

Also flags "warm lead" markers: "DM me", "reply if interested",
"contact me", "PM me", "email me", "hit me up".
"""
import json, re, sys

SKILL_PATTERNS = {
    "ai_agent": [r"\bAI agent", r"\bLLM\b", r"\bGPT", r"\bagentic", r"\bRAG\b", r"\bagent\b"],
    "python": [r"\bPython\b", r"\bFastAPI\b", r"\bDjango\b", r"\bFlask\b", r"\bpandas\b", r"\bpytest\b"],
    "docker": [r"\bDocker\b", r"\bcontainer", r"\bk8s\b", r"\bKubernetes\b"],
    "gitlab_github": [r"\bGitLab\b", r"\bGitHub\b", r"\bCI/CD\b", r"\bwebhook", r"\bMR bot", r"\bGitHub Actions"],
    "security": [r"\bsecurity", r"\bsandbox", r"\btamper", r"\baudit", r"\bsecret", r"\bvuln"],
    "automation": [r"\bautomation", r"\bautomate", r"\bscript", r"\bscraping", r"\bworkflow", r"\bdevtools"],
    "backend": [r"\bbackend", r"\bAPI\b", r"\bREST\b", r"\bGraphQL\b"],
    "contract": [r"\bcontract", r"\bfreelance", r"\bhiring\b", r"\bwanted", r"\blooking for", r"\bneed someone", r"\blooking to hire"],
}

WARM_MARKERS = [r"DM me", r"reply if interested", r"contact me", r"PM me", r"email me", r"hit me up", r"reach out", r"send me", r"message me"]

def score_lead(text_blob):
    """Return dict of skill matches + total score (0-8)."""
    blob = text_blob.lower()
    matches = {}
    for skill, patterns in SKILL_PATTERNS.items():
        for p in patterns:
            if re.search(p.lower(), blob):
                matches[skill] = True
                break
    # cap to 5
    score = min(5, len(matches))
    return {"matches": sorted(matches.keys()), "score": score}

def is_warm(text_blob):
    blob = text_blob
    for p in WARM_MARKERS:
        if re.search(p, blob, re.I):
            return True, p
    return False, None

if __name__ == "__main__":
    # Read stdin JSON: list of {title, snippet, url, author, ...}
    leads = json.load(sys.stdin)
    scored = []
    for l in leads:
        text = " ".join(filter(None, [l.get("title",""), l.get("snippet","")]))
        s = score_lead(text)
        warm, why = is_warm(text)
        l["matches"] = s["matches"]
        l["score"] = s["score"]
        l["warm"] = warm
        if warm:
            l["warm_marker"] = why
        scored.append(l)
    # sort by score desc, then warm first
    scored.sort(key=lambda x: (-x["score"], -int(x.get("warm",False))))
    print(json.dumps(scored, ensure_ascii=False, indent=2))
