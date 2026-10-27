#!/usr/bin/env python3
"""
zolo_curador_skills.py — Curador de skills con lifecycle automático (regla 36)

Walks SKILL_REGISTRY.json, applies lifecycle transitions:
- stale_after_days=30 → state=stale
- archive_after_days=60 → state=archived (moved to 02_skills/.archive/, recoverable)
- auto_pin: skills with use_count >= 5 in last 30 days → pinned=true
- NEVER deletes — archive is the maximum

Cadence: MENSUAL §18.
"""
from __future__ import annotations
import json
import os
import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

SKILLS_DIR = Path("/home/z/my-project/download/agente-zolo/02_skills")
ARCHIVE_DIR = SKILLS_DIR / ".archive"
REGISTRY = Path("/home/z/my-project/download/agente-zolo/06_aprendizaje/SKILL_REGISTRY.json")
WORKLOG = Path("/home/z/my-project/worklog.md")


def log(level: str, msg: str) -> None:
    icons = {"INFO": "ℹ️", "OK": "✅", "WARN": "⚠️", "FAIL": "❌", "ARCHIVE": "📦", "PIN": "📌"}
    print(f"{icons.get(level, '•')} [{level}] {msg}")


def load_registry() -> dict:
    if not REGISTRY.exists():
        log("FAIL", f"SKILL_REGISTRY.json no encontrado: {REGISTRY}")
        sys.exit(1)
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def save_registry(data: dict) -> None:
    data["_meta"]["last_updated"] = datetime.now(timezone.utc).isoformat()
    REGISTRY.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def days_since(iso_str: str) -> int:
    """Days since ISO timestamp."""
    try:
        dt = datetime.fromisoformat(iso_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - dt).days
    except (ValueError, TypeError):
        return 9999


def walk_lifecycle(data: dict, dry_run: bool = False) -> dict:
    """Apply lifecycle transitions. Returns stats."""
    config = data.get("config", {})
    stale_days = config.get("stale_after_days", 30)
    archive_days = config.get("archive_after_days", 60)
    auto_pin_threshold = config.get("auto_pin_threshold", 5)
    pinned_skills = set(config.get("pinned_skills", []))

    stats = {"checked": 0, "staled": 0, "archived": 0, "auto_pinned": 0, "unpinned": 0}
    skills = data.get("skills", {})

    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    for name, meta in skills.items():
        stats["checked"] += 1
        is_pinned = meta.get("pinned", False) or name in pinned_skills

        # Auto-pin check
        if meta.get("use_count", 0) >= auto_pin_threshold and not is_pinned:
            log("PIN", f"Auto-pin: {name} (use_count={meta['use_count']})")
            meta["pinned"] = True
            stats["auto_pinned"] += 1
            is_pinned = True

        # Skip pinned skills for stale/archive
        if is_pinned:
            continue

        idle_days = days_since(meta.get("last_activity_at", ""))
        current_state = meta.get("state", "active")

        # Archive check (highest priority)
        if idle_days >= archive_days and current_state != "archived":
            skill_path = SKILLS_DIR / name
            archive_path = ARCHIVE_DIR / name
            if skill_path.exists():
                if not dry_run:
                    if archive_path.exists():
                        shutil.rmtree(archive_path)
                    shutil.move(str(skill_path), str(archive_path))
                log("ARCHIVE", f"{name} (idle {idle_days}d ≥ {archive_days}d) → .archive/")
                meta["state"] = "archived"
                stats["archived"] += 1

        # Stale check
        elif idle_days >= stale_days and current_state == "active":
            log("WARN", f"{name} → stale (idle {idle_days}d ≥ {stale_days}d)")
            meta["state"] = "stale"
            stats["staled"] += 1

        # Recovery: if skill was stale/archived but got used recently
        elif idle_days < stale_days and current_state in ("stale", "archived"):
            skill_path = SKILLS_DIR / name
            archive_path = ARCHIVE_DIR / name
            if current_state == "archived" and archive_path.exists() and not skill_path.exists():
                if not dry_run:
                    shutil.move(str(archive_path), str(skill_path))
                log("OK", f"RESTORED: {name} (used after archive, idle {idle_days}d)")
            meta["state"] = "active"

    return stats


def main():
    import argparse
    parser = argparse.ArgumentParser(description="ZOLO skill curator (regla 36)")
    parser.add_argument("--dry-run", action="store_true", help="Simular sin cambios")
    parser.add_argument("--report", action="store_true", help="Solo reportar estado")
    args = parser.parse_args()

    log("INFO", f"ZOLO Skill Curator v7.0 — regla 36")
    log("INFO", f"Registry: {REGISTRY}")
    log("INFO", f"Dry run: {args.dry_run}")
    print()

    data = load_registry()
    config = data.get("config", {})
    log("INFO", f"Config: stale={config.get('stale_after_days',30)}d archive={config.get('archive_after_days',60)}d pin_threshold={config.get('auto_pin_threshold',5)}")
    print()

    if args.report:
        skills = data.get("skills", {})
        active = sum(1 for m in skills.values() if m.get("state") == "active")
        stale = sum(1 for m in skills.values() if m.get("state") == "stale")
        archived = sum(1 for m in skills.values() if m.get("state") == "archived")
        pinned = sum(1 for m in skills.values() if m.get("pinned"))
        log("INFO", f"Total: {len(skills)} | active: {active} | stale: {stale} | archived: {archived} | pinned: {pinned}")
        print()
        print(f"{'Skill':<40} {'State':<10} {'Use':<5} {'Pin':<4} {'Conf':<5} {'Idle':<5}")
        print("-" * 75)
        for name, meta in sorted(skills.items()):
            idle = days_since(meta.get("last_activity_at", ""))
            pin = "✓" if meta.get("pinned") else ""
            print(f"{name:<40} {meta.get('state','?'):<10} {meta.get('use_count',0):<5} {pin:<4} {meta.get('confidence',0):<5.1f} {idle:<5}d")
        return 0

    stats = walk_lifecycle(data, dry_run=args.dry_run)

    if not args.dry_run:
        save_registry(data)

    print()
    log("OK", f"Checked: {stats['checked']} | Staled: {stats['staled']} | Archived: {stats['archived']} | Auto-pinned: {stats['auto_pinned']}")

    # Append to worklog (regla 9)
    if not args.dry_run and (stats["staled"] + stats["archived"] + stats["auto_pinned"]) > 0:
        with WORKLOG.open("a", encoding="utf-8") as f:
            f.write(f"\n### CURATOR {datetime.now(timezone.utc).strftime('%Y-%m-%d')} — {stats['checked']} skills\n")
            f.write(f"- STALE: {stats['staled']} | ARCHIVED: {stats['archived']} | AUTO-PINNED: {stats['auto_pinned']}\n")
        log("OK", "Worklog appended (regla 9)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
