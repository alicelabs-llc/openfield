#!/usr/bin/env python3
"""Save Wellfound job pages as JSON (scraped via agent-browser)."""
import subprocess, json, time
from pathlib import Path

OUT_DIR = Path("/home/z/my-project/jobboards/wellfound/pages")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SLUGS = [
    "4884757-senior-applied-ai-engineer-i",
    "4884694-senior-software-engineer-platform",
    "4881335-senior-backend-engineer-integrations-platform",
    "4875122-lead-database-data-platform-engineer",
    "3670454-senior-full-stack-engineer-core-ux-usa",
    "4884710-recruiting-operations-specialist-contract",
    "4196821-technical-support-engineer",
    "4846255-support-engineer",
    "4867181-software-data-engineer",
    "3154038-senior-solutions-engineer",
    "3994821-2-data-engineer-staff-principal-lead",
    "4875217-account-executive-ai-x-fintech",
]

def get_page(slug):
    print(f"=== {slug} ===")
    subprocess.run(["agent-browser", "open", f"https://wellfound.com/jobs/{slug}", "--timeout", "60000"], capture_output=True)
    time.sleep(3)
    r = subprocess.run(["agent-browser", "eval", """
    (function(){
        var url = location.href;
        var title = document.title;
        var body = document.body ? document.body.innerText : '';
        // Salary
        var salaryMatch = body.match(/\\$[0-9,]+k?\\s*[–-]\\s*\\$?[0-9,]+k?\\s*(?:USD)?/i) || body.match(/\\$[0-9,]+k?\\s*[–-]\\s*[0-9,]+k?/i);
        var salary = salaryMatch ? salaryMatch[0] : '';
        var remoteMatch = body.match(/Hires remotely in[^\\n]+/);
        var remote = remoteMatch ? remoteMatch[0] : '';
        var stageMatch = body.match(/(Early Stage|Growth Stage|Scale Stage|Late Stage)/);
        var stage = stageMatch ? stageMatch[0] : '';
        var typeMatch = body.match(/(Full\\-?time|Part\\-?time|Contract|Contractor|C2C|1099|W2|B2B|Freelance)/i);
        var type = typeMatch ? typeMatch[0] : '';
        // First 3000 chars of body
        return {url: url, title: title, body: body.slice(0, 8000), salary: salary, remote: remote, stage: stage, type: type};
    })()
    """, "--json"], capture_output=True, text=True, timeout=60)
    try:
        d = json.loads(r.stdout)
        return d.get("data", {}).get("result", {})
    except Exception as e:
        return {"error": str(e), "stdout": r.stdout[:500]}

def main():
    out = []
    for slug in SLUGS:
        info = get_page(slug)
        info["slug"] = slug
        out.append(info)
        (OUT_DIR / f"{slug}.json").write_text(json.dumps(info, indent=2, ensure_ascii=False))
    print(f"Saved {len(out)} Wellfound job pages")
    json.dump(out, open("/home/z/my-project/jobboards/wellfound/jobs_detail.json", "w"), indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
