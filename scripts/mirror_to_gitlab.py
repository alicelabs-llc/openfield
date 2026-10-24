#!/usr/bin/env python3
"""
Mirror alethech-agent-vault from GitHub to GitLab.com (required for GitLab Transcend submission).

Steps:
1. Verify GitLab token works
2. Check if repo already exists on GitLab (skip creation if so)
3. Create new GitLab project (mirror mode)
4. Push the local repo to GitLab via git remote add + git push
"""
import json
import os
import subprocess
import sys
import urllib.request
import urllib.error

GITLAB_TOKEN = "glpat-NJNDB08yWG41Xskk0G-mRmM6MQpvOjEKdTpranZqbQ8.01.171wudi4a"
GITLAB_URL = "https://gitlab.com"
NAMESPACE = "eddyflores100-lang"  # try this; will fall back to user namespace
REPO_NAME = "alethech-agent-vault"
LOCAL_REPO = "/home/z/my-project/alethech-agent-vault"

def gl(method, url, body=None):
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Content-Type": "application/json",
        "PRIVATE-TOKEN": GITLAB_TOKEN,
        "User-Agent": "eddyflores100-lang-bot/1.0",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            if r.status == 204:
                return {}
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"_error": f"HTTP {e.code}", "_body": e.read().decode()[:300]}
    except Exception as e:
        return {"_error": str(e)}

# 1. Verify token
print("=== 1. Verify GitLab token ===")
user = gl("GET", f"{GITLAB_URL}/api/v4/user")
if "_error" in user:
    print(f"❌ Token invalid: {user}")
    sys.exit(1)
print(f"✅ Token valid. Logged in as: @{user.get('username')} (id={user.get('id')})")
username = user.get("username")
user_id = user.get("id")

# 2. Check if project already exists
print(f"\n=== 2. Check if {username}/{REPO_NAME} exists ===")
existing = gl("GET", f"{GITLAB_URL}/api/v4/projects/{username}%2F{REPO_NAME}")
if "_error" not in existing:
    print(f"✅ Project already exists: {existing.get('web_url')}")
    gitlab_url = existing.get("web_url")
    gitlab_ssh = existing.get("ssh_url_to_repo")
    gitlab_http = existing.get("http_url_to_repo")
else:
    print(f"  Project does not exist yet ({existing.get('_error')}). Creating...")
    
    # 3. Create the project
    print(f"\n=== 3. Create new GitLab project {username}/{REPO_NAME} ===")
    payload = {
        "name": REPO_NAME,
        "path": REPO_NAME,
        "description": "Verifiable agent execution with sandboxed blast radius + tamper-evident provenance. Submission for GitLab Transcend 'Life After Code' hackathon (Oct 27 2026).",
        "visibility": "public",
        "initialize_with_readme": False,  # we'll push our own
    }
    created = gl("POST", f"{GITLAB_URL}/api/v4/projects", payload)
    if "_error" in created:
        print(f"❌ Failed to create project: {created}")
        sys.exit(2)
    print(f"✅ Project created: {created.get('web_url')}")
    gitlab_url = created.get("web_url")
    gitlab_ssh = created.get("ssh_url_to_repo")
    gitlab_http = created.get("http_url_to_repo")

print(f"\n  GitLab URL:  {gitlab_url}")
print(f"  HTTP URL:    {gitlab_http}")

# 4. Add GitLab as a remote and push
print(f"\n=== 4. Add GitLab remote + push ===")
os.chdir(LOCAL_REPO)

# Check existing remotes
result = subprocess.run(["git", "remote"], capture_output=True, text=True)
remotes = result.stdout.split()
if "gitlab" in remotes:
    print("  gitlab remote already exists, removing...")
    subprocess.run(["git", "remote", "remove", "gitlab"], check=True)

# Use HTTPS with token embedded for push auth
gitlab_push_url = gitlab_http.replace("https://", f"https://oauth2:{GITLAB_TOKEN}@")
print(f"  Adding remote: gitlab -> {gitlab_http}")
subprocess.run(["git", "remote", "add", "gitlab", gitlab_push_url], check=True)

print(f"\n  Pushing main branch to GitLab...")
result = subprocess.run(["git", "push", "gitlab", "main"], capture_output=True, text=True)
if result.returncode == 0:
    print(f"  ✅ Push successful!")
    print(f"     {result.stdout.strip()}")
else:
    print(f"  ❌ Push failed (rc={result.returncode}):")
    print(f"     STDOUT: {result.stdout}")
    print(f"     STDERR: {result.stderr}")
    sys.exit(3)

print(f"\n=== 5. Verify push ===")
project = gl("GET", f"{GITLAB_URL}/api/v4/projects/{username}%2F{REPO_NAME}")
print(f"  Default branch: {project.get('default_branch')}")
print(f"  Web URL: {project.get('web_url')}")
print(f"  Last activity: {project.get('last_activity_at')}")
print(f"  Visibility: {project.get('visibility')}")

print(f"\n🎉 GitLab mirror created!")
print(f"   URL: {gitlab_url}")
print(f"   Clone command: git clone {gitlab_http}")

# Save info to file
with open("/home/z/my-project/download/gitlab_mirror_info.txt", "w") as f:
    f.write(f"GitLab URL: {gitlab_url}\n")
    f.write(f"HTTP clone: {gitlab_http}\n")
    f.write(f"Visibility: public\n")
    f.write(f"Default branch: main\n")
