#!/usr/bin/env python3
"""Create the mailhand-aws-cds GitHub repo and push the code."""
import json
import os
import subprocess
import urllib.request
import urllib.error

TOKEN = "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"
REPO_NAME = "mailhand-aws-cds"
REPO_DESC = "Agentic email code review via AWS SES + Bedrock AgentCore. Submission for AWS CDS Agentic AI Partner Hackathon (Oct 28, 2026)."
LOCAL_DIR = "/home/z/my-project/mailhand-aws-cds"

COMMIT_MSG = """feat: initial release - Mailhand agentic email code review via AWS SES + Bedrock AgentCore

Submission for AWS CDS Agentic AI Partner Hackathon (deadline Oct 28, 2026).
Prize target: 1st Place $18K + Best WhatsApp Solution $10K bonus.

Components:
- src/mailhand_router.py: Lambda entrypoint for SES incoming emails.
- src/review_agent.py: Bedrock AgentCore agent with plan-execute-synthesize loop.
- src/ses_sender.py: SES outgoing email reply with markdown review.
- src/whatsapp_sender.py: AWS End User Messaging Social (WhatsApp).
- src/pr_commenter.py: Posts review comments on GitHub/GitLab PRs.

Tests: 24 tests, all passing in 0.17s.
"""

def run(cmd, **kwargs):
    """Run a shell command in LOCAL_DIR."""
    return subprocess.run(cmd, shell=True, cwd=LOCAL_DIR, capture_output=True, text=True, **kwargs)

# 1. Create repo on GitHub
print(f"=== Creating GitHub repo: {REPO_NAME} ===")
payload = {
    "name": REPO_NAME,
    "description": REPO_DESC,
    "private": False,
    "auto_init": False,
}
req = urllib.request.Request(
    "https://api.github.com/user/repos",
    data=json.dumps(payload).encode(),
    method="POST",
    headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {TOKEN}",
        "User-Agent": "eddyflores100-lang-bot",
    },
)
clone_url = None
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        repo_data = json.loads(r.read())
    print(f"Repo created: {repo_data.get('html_url')}")
    clone_url = repo_data.get("clone_url")
except urllib.error.HTTPError as e:
    body = e.read().decode()
    if "already exists" in body or "name already exists" in body:
        print(f"  Repo already exists, using existing URL")
        clone_url = f"https://github.com/eddyflores100-lang/{REPO_NAME}.git"
    else:
        print(f"Failed: HTTP {e.code}: {body[:300]}")
        raise

# 2. Init local repo + commit + push
print(f"\n=== Initializing local repo + pushing ===")
run("git init -q")
run("git config user.email 'eddyflores100@gmail.com'")
run("git config user.name 'eddyflores100-lang'")
run("git add -A")

st = run("git status --porcelain")
print(f"  Files staged: {len(st.stdout.splitlines())}")

# Write commit message to a file to avoid shell quoting issues
msg_file = "/tmp/mailhand_commit_msg.txt"
with open(msg_file, "w") as f:
    f.write(COMMIT_MSG)

commit_result = run(f"git commit -F {msg_file}")
if commit_result.returncode == 0:
    print(f"  Commit created")
else:
    print(f"  Commit failed: {commit_result.stderr}")
    raise SystemExit(1)

# Add remote with token in URL
clone_url_auth = clone_url.replace("https://", f"https://x-access-token:{TOKEN}@")
run("git remote remove origin 2>/dev/null; true")
run(f"git remote add origin {clone_url_auth}")
print(f"  Remote set: {clone_url}")

push_result = run("git push -u origin main")
if push_result.returncode == 0:
    print(f"  Push successful!")
    print(f"     {push_result.stderr.strip()[-200:]}")
else:
    print(f"  Push failed: {push_result.stderr}")
    raise SystemExit(1)

print(f"\nRepo live: https://github.com/eddyflores100-lang/{REPO_NAME}")
