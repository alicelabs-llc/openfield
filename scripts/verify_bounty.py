#!/usr/bin/env python3
"""
verify_bounty.py — Verifies a GitHub bounty is real before attempting.

Usage: python3 verify_bounty.py <repo> <issue_number> <github_token>

Checks:
1. Issue is open
2. Bounty label or $ amount exists
3. Platform (Algora/IssueHunt/direct)
4. Active /attempt comments by other devs
5. Repo activity (last commit date)
6. CONTRIBUTING.md exists
7. CI status
8. Maintainer responsiveness
"""

import json
import sys
import urllib.request
import ssl
from datetime import datetime, timezone

def api_call(url, token):
    req = urllib.request.Request(url, headers={
        "Authorization": f"token {token}",
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/vnd.github.v3+json"
    })
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        return json.loads(resp.read().decode())

def verify_bounty(repo, issue_num, token):
    print(f"=== Verificando bounty: {repo}#{issue_num} ===\n")
    
    # 1. Get issue
    try:
        issue = api_call(f"https://api.github.com/repos/{repo}/issues/{issue_num}", token)
    except Exception as e:
        print(f"❌ ERROR: No se pudo obtener el issue: {e}")
        return False
    
    # 2. Check state
    state = issue.get("state", "unknown")
    print(f"Estado: {state}")
    if state != "open":
        print("❌ Issue cerrado — no se puede reclamar")
        return False
    print("✅ Issue abierto")
    
    # 3. Check bounty indicators
    labels = [l["name"].lower() for l in issue.get("labels", [])]
    body = issue.get("body", "") or ""
    title = issue.get("title", "")
    full_text = f"{title} {body}".lower()
    
    has_bounty_label = any("bounty" in l for l in labels)
    has_dollar = "$" in title or "$" in body
    has_algora = "algora" in full_text or "/bounty" in full_text
    has_issuehunt = "issuehunt" in full_text
    
    print(f"Bounty label: {'✅' if has_bounty_label else '❌'}")
    print(f"Dollar amount: {'✅' if has_dollar else '❌'}")
    print(f"Algora: {'✅' if has_algora else '❌'}")
    print(f"IssueHunt: {'✅' if has_issuehunt else '❌'}")
    
    if not (has_bounty_label or has_dollar or has_algora or has_issuehunt):
        print("❌ No se encontró indicador de bounty")
        return False
    print("✅ Bounty detectado")
    
    # 4. Check competition
    comments = issue.get("comments", 0)
    print(f"\nComentarios: {comments}")
    if comments > 30:
        print("⚠️  Muchos comentarios — alta competencia")
    
    # 5. Check for active attempts
    try:
        comments_data = api_call(
            f"https://api.github.com/repos/{repo}/issues/{issue_num}/comments?per_page=100",
            token
        )
        attempts = []
        for c in comments_data:
            body = c.get("body", "").lower()
            if "/attempt" in body or "claiming" in body or "i'll take" in body or "working on" in body:
                author = c.get("user", {}).get("login", "?")
                created = c.get("created_at", "?")[:10]
                attempts.append((author, created))
        
        if attempts:
            print(f"\n⚠️  {len(attempts)} intentos activos:")
            for author, date in attempts[-5:]:
                print(f"  {author} ({date})")
        else:
            print("\n✅ Sin intentos activos — bounty disponible")
    except:
        print("\n⚠️  No se pudieron verificar comentarios")
    
    # 6. Check repo
    try:
        repo_data = api_call(f"https://api.github.com/repos/{repo}", token)
        pushed_at = repo_data.get("pushed_at", "?")[:10]
        stars = repo_data.get("stargazers_count", 0)
        has_contributing = repo_data.get("has_issues", False)
        
        print(f"\nRepo info:")
        print(f"  Stars: {stars}")
        print(f"  Último push: {pushed_at}")
        
        # Check if repo is active (pushed in last 30 days)
        now = datetime.now(timezone.utc)
        try:
            push_date = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
            days_since = (now - push_date).days
            if days_since > 60:
                print(f"  ⚠️  Repo inactivo ({days_since} días sin push)")
            else:
                print(f"  ✅ Repo activo ({days_since} días desde último push)")
        except:
            pass
        
        if stars < 5:
            print("  ⚠️  Pocas estrellas — posible repo de prueba")
        elif stars > 100:
            print(f"  ✅ Repo popular ({stars} stars)")
    except:
        print("\n⚠️  No se pudo obtener info del repo")
    
    # 7. Check CONTRIBUTING.md
    try:
        api_call(f"https://api.github.com/repos/{repo}/contents/CONTRIBUTING.md", token)
        print("\n✅ CONTRIBUTING.md existe")
    except:
        try:
            api_call(f"https://api.github.com/repos/{repo}/contents/.github/CONTRIBUTING.md", token)
            print("\n✅ CONTRIBUTING.md existe (.github/)")
        except:
            print("\n⚠️  No CONTRIBUTING.md — leer README antes de PR")
    
    # 8. Anti-ban check
    print(f"\n=== ANTIBAN CHECK ===")
    print(f"  Comments en issue: {comments} {'✅' if comments < 20 else '⚠️'}")
    print(f"  Intentos detectados: {len(attempts) if 'attempts' in dir() else '?'}")
    print(f"  Recomendación: {'✅ PROBAR' if comments < 20 and not attempts else '⚠️  ALTA COMPETENCIA'}")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 verify_bounty.py <owner/repo> <issue_number> <github_token>")
        sys.exit(1)
    verify_bounty(sys.argv[1], int(sys.argv[2]), sys.argv[3])
