#!/usr/bin/env python3
"""
🤖 PR Monitor Agent — Revisa estado de PRs enviados y actualiza tracker.

Corre automáticamente (cron) y hace:
1. Lee el archivo .state (lista de PRs enviados)
2. Para cada PR, consulta GitHub/Codeberg API
3. Clasifica: merged / closed / open / stale
4. Actualiza HACKTOBERFEST_TRACKER.md con estado real
5. Si un PR lleva >7 días sin actividad, genera recordatorio de nudge
6. Genera resumen diario en logs/daily_report.md

Esto es el "agente" que trabaja en background.
"""
from __future__ import annotations
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
import urllib.request
import urllib.error

SCRIPT_DIR = Path(__file__).parent.parent
STATE_FILE = SCRIPT_DIR / ".state"
TRACKER_FILE = SCRIPT_DIR.parent / "HACKTOBERFEST_TRACKER.md"
LOG_DIR = SCRIPT_DIR / "logs"
CONFIG_FILE = Path.home() / ".auto-pr-config.env"


def load_config():
    """Load config from ~/.auto-pr-config.env"""
    config = {}
    if not CONFIG_FILE.exists():
        return config
    for line in CONFIG_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, _, value = line.partition("=")
            config[key.strip()] = value.strip()
    return config


def parse_state():
    """Parse .state file → list of dicts."""
    if not STATE_FILE.exists():
        return []
    entries = []
    for line in STATE_FILE.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("|", 2)
        if len(parts) == 3:
            patch, url, sent_at = parts
            entries.append({
                "patch": patch,
                "url": url,
                "sent_at": sent_at,
            })
    return entries


def github_pr_status(repo_full: str, pr_number: int, token: str) -> dict:
    """Fetch PR status from GitHub API."""
    url = f"https://api.github.com/repos/{repo_full}/pulls/{pr_number}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        return {
            "state": data["state"],  # open, closed
            "merged": data.get("merged", False),
            "mergeable_state": data.get("mergeable_state", "unknown"),
            "updated_at": data.get("updated_at", ""),
            "comments": data.get("comments", 0),
            "review_comments": data.get("review_comments", 0),
            "title": data.get("title", ""),
        }
    except (urllib.error.URLError, urllib.error.HTTPError, KeyError) as e:
        return {"error": str(e), "state": "unknown"}


def codeberg_pr_status(repo_full: str, pr_number: int, token: str) -> dict:
    """Fetch PR status from Codeberg (Gitea API)."""
    url = f"https://codeberg.org/api/v1/repos/{repo_full}/pulls/{pr_number}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"token {token}",
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        return {
            "state": data.get("state", "unknown"),
            "merged": data.get("merged", False),
            "mergeable": data.get("mergeable", "unknown"),
            "updated_at": data.get("updated_at", ""),
            "comments": data.get("comments", 0),
            "title": data.get("title", ""),
        }
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        return {"error": str(e), "state": "unknown"}


def parse_pr_url(url: str) -> dict:
    """Extract platform, repo, PR number from URL."""
    # https://github.com/owner/repo/pull/123
    m = re.match(r"https?://github\.com/([^/]+)/([^/]+)/pull/(\d+)", url)
    if m:
        return {
            "platform": "github",
            "repo_full": f"{m.group(1)}/{m.group(2)}",
            "pr_number": int(m.group(3)),
        }
    # https://codeberg.org/owner/repo/pulls/123
    m = re.match(r"https?://codeberg\.org/([^/]+)/([^/]+)/pulls/(\d+)", url)
    if m:
        return {
            "platform": "codeberg",
            "repo_full": f"{m.group(1)}/{m.group(2)}",
            "pr_number": int(m.group(3)),
        }
    return {"platform": "unknown", "repo_full": "", "pr_number": 0}


def needs_nudge(status: dict, sent_at: str) -> bool:
    """Should we nudge? (>7 days idle AND still open AND no recent comments)."""
    if status.get("state") != "open" or status.get("merged"):
        return False
    try:
        sent = datetime.fromisoformat(sent_at.replace(" ", "T").split(".")[0])
        days_since = (datetime.utcnow() - sent).days
    except (ValueError, AttributeError):
        return False
    return days_since >= 7 and status.get("comments", 0) == 0


def generate_report(entries: list[dict], config: dict) -> str:
    """Generate daily report markdown."""
    today = datetime.utcnow().strftime("%Y-%m-%d")
    lines = [
        f"# 📊 PR Monitor Report — {today}",
        "",
        f"Total PRs tracked: **{len(entries)}**",
        "",
        "| # | Patch | Repo | PR # | State | Merged | Comments | Days idle | Needs nudge? |",
        "|---|-------|------|-------|-------|--------|----------|-----------|---------------|",
    ]
    merged_count = 0
    open_count = 0
    closed_count = 0
    nudge_list = []

    for i, entry in enumerate(entries, 1):
        info = parse_pr_url(entry["url"])
        if info["platform"] == "unknown":
            status = {"state": "invalid_url", "merged": False, "comments": 0, "updated_at": ""}
        elif info["platform"] == "github":
            status = github_pr_status(info["repo_full"], info["pr_number"], config.get("GITHUB_TOKEN", ""))
        else:
            status = codeberg_pr_status(info["repo_full"], info["pr_number"], config.get("CODEBERG_TOKEN", ""))

        if status.get("merged"):
            state_str = "✅ MERGED"
            merged_count += 1
        elif status.get("state") == "closed":
            state_str = "❌ CLOSED"
            closed_count += 1
        elif status.get("state") == "open":
            state_str = "🟢 OPEN"
            open_count += 1
        else:
            state_str = "❓ " + status.get("state", "unknown")

        try:
            sent = datetime.fromisoformat(entry["sent_at"].replace(" ", "T").split(".")[0])
            days_idle = (datetime.utcnow() - sent).days
        except (ValueError, AttributeError):
            days_idle = 0

        nudge = needs_nudge(status, entry["sent_at"])
        nudge_str = "🔔 YES" if nudge else "—"
        if nudge:
            nudge_list.append((entry["patch"], entry["url"]))

        repo_short = info["repo_full"][:30] if info["repo_full"] else "?"
        lines.append(f"| {i} | {entry['patch'][:30]} | {repo_short} | #{info['pr_number']} | {state_str} | {'✓' if status.get('merged') else '—'} | {status.get('comments', 0)} | {days_idle} | {nudge_str} |")

    lines.append("")
    lines.append("## 📈 Resumen")
    lines.append(f"- ✅ Merged: **{merged_count}**")
    lines.append(f"- 🟢 Open: **{open_count}**")
    lines.append(f"- ❌ Closed sin merge: **{closed_count}**")

    if nudge_list:
        lines.append("")
        lines.append("## 🔔 PRs que necesitan nudge (>7 días sin actividad)")
        for patch, url in nudge_list:
            lines.append(f"- `{patch}` → {url}")
        lines.append("")
        lines.append("Acción sugerida: comentar en cada PR con:")
        lines.append("> 'Following up on this PR — happy to make adjustments if needed.'")

    lines.append("")
    lines.append("---")
    lines.append(f"Generado por PR Monitor Agent · {datetime.utcnow().isoformat()}Z")

    return "\n".join(lines)


def main():
    config = load_config()
    entries = parse_state()

    if not entries:
        print("ℹ️  No hay PRs en .state todavía. Corre auto_pr_sender.sh primero.")
        return 0

    print(f"📊 Revisando estado de {len(entries)} PRs...")

    report = generate_report(entries, config)

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.utcnow().strftime("%Y-%m-%d")
    report_file = LOG_DIR / f"daily_report_{today}.md"
    report_file.write_text(report, encoding="utf-8")
    print(f"✅ Reporte guardado: {report_file}")

    # También imprimir resumen en consola
    print("\n" + "=" * 50)
    print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
