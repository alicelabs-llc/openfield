#!/usr/bin/env python3
"""
zolo_optimizar_descripcion.py — Optimización de descriptions anti-undertriggering (regla 39)

Loop medible:
1. Generar 20 trigger eval queries (8-10 should-trigger + 8-10 near-miss)
2. 60% train / 40% test split
3. 3x runs por query
4. Iterar hasta 80% test set (no train — evitar overfitting)
5. Description ≤80 chars, "pushy" con condiciones explícitas

Inspirado en: Anthropic improve_description.py
"""
from __future__ import annotations
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SKILLS_DIR = Path("/home/z/my-project/download/agente-zolo/02_skills")
EVALS_DIR = Path("/home/z/my-project/download/agente-zolo/06_aprendizaje/evals")
WORKLOG = Path("/home/z/my-project/worklog.md")
MAX_DESC_CHARS = 80


def log(level: str, msg: str) -> None:
    icons = {"INFO": "ℹ️", "OK": "✅", "WARN": "⚠️", "FAIL": "❌", "OPTIMIZE": "⚡"}
    print(f"{icons.get(level, '•')} [{level}] {msg}")


def extract_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter."""
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    fm_text = parts[1].strip()
    body = parts[2]
    fm = {}
    current_key = None
    current_val = []
    for line in fm_text.splitlines():
        m = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*):\s*(.*)$", line)
        if m:
            if current_key and current_val:
                fm[current_key] = "\n".join(current_val).strip()
            current_key = m.group(1)
            val = m.group(2).strip()
            if val in ("", ">", ">-", "|", "|-"):
                current_val = []
            else:
                fm[current_key] = val.strip("'\"")
                current_val = []
        elif current_key and line.startswith((" ", "\t")):
            current_val.append(line.rstrip())
    if current_key and current_val:
        fm[current_key] = "\n".join(current_val).strip()
    return fm, body


def check_description_length(desc: str) -> bool:
    """Check if description is ≤80 chars."""
    return len(desc) <= MAX_DESC_CHARS


def check_description_pushy(desc: str, skill_name: str) -> list[str]:
    """Check if description is 'pushy' enough (anti-undertriggering)."""
    issues = []
    desc_lower = desc.lower()

    # Should mention skill's trigger conditions explicitly
    if "use when" not in desc_lower and "usa cuando" not in desc_lower and "use" not in desc_lower:
        issues.append("sin frase de activación explícita ('Use when' / 'Usa cuando')")

    # Should be specific enough to trigger on implicit mentions
    if skill_name.lower() not in desc_lower:
        issues.append(f"no menciona el nombre de la skill '{skill_name}'")

    # Should NOT be too vague
    vague_words = ["varias cosas", "general purpose", "when needed", "cuando sea necesario"]
    for vw in vague_words:
        if vw in desc_lower:
            issues.append(f"demasiado vago: contiene '{vw}'")
            break

    return issues


def generate_suggestions(skill_name: str, current_desc: str, trigger: str = "") -> list[str]:
    """Generate improved description variants."""
    suggestions = []

    # Variant 1: Add explicit trigger
    if trigger:
        v1 = f"{current_desc} Use when {trigger[:40]}".strip()
        if len(v1) <= MAX_DESC_CHARS:
            suggestions.append(v1)

    # Variant 2: Make pushy
    v2 = f"Use when {trigger[:50] or skill_name}. {current_desc[:25]}".strip()
    if len(v2) <= MAX_DESC_CHARS:
        suggestions.append(v2)

    # Variant 3: Explicit enumeration
    v3 = f"{skill_name}. Use when {trigger[:50] or 'relevant task'} — even if not explicitly requested.".strip()
    if len(v3) <= MAX_DESC_CHARS:
        suggestions.append(v3)

    # Variant 4: Direct + trigger
    if current_desc and not current_desc.lower().startswith("use when"):
        v4 = f"Use when {trigger[:30] or skill_name}. {current_desc[:40]}".strip()
        if len(v4) <= MAX_DESC_CHARS:
            suggestions.append(v4)

    return suggestions[:3]  # max 3 suggestions


def optimize_skill(skill_name: str, dry_run: bool = False) -> dict:
    """Optimize a skill's description."""
    skill_md = SKILLS_DIR / skill_name / "SKILL.md"
    if not skill_md.exists():
        log("FAIL", f"Skill no encontrada: {skill_md}")
        return {"error": "not found"}

    content = skill_md.read_text(encoding="utf-8")
    fm, body = extract_frontmatter(content)

    current_desc = fm.get("description", "")
    trigger = fm.get("trigger", "")

    log("INFO", f"Skill: {skill_name}")
    log("INFO", f"Description actual ({len(current_desc)} chars): {current_desc[:80]}")
    log("INFO", f"Trigger: {trigger[:60]}")

    # Checks
    issues = []
    if not check_description_length(current_desc):
        issues.append(f"description demasiado larga ({len(current_desc)} > {MAX_DESC_CHARS} chars)")

    issues.extend(check_description_pushy(current_desc, skill_name))

    if issues:
        log("WARN", f"Issues encontrados ({len(issues)}):")
        for issue in issues:
            log("WARN", f"  → {issue}")
    else:
        log("OK", "Description ya cumple estándares")
        return {"skill": skill_name, "status": "already_optimized", "issues": []}

    # Generate suggestions
    suggestions = generate_suggestions(skill_name, current_desc, trigger)
    if not suggestions:
        log("WARN", "No se pudieron generar sugerencias automáticas. Edita manualmente.")
        return {"skill": skill_name, "status": "manual_needed", "issues": issues}

    log("OPTIMIZE", f"Sugerencias generadas ({len(suggestions)}):")
    for i, s in enumerate(suggestions, 1):
        log("INFO", f"  {i}. ({len(s)} chars) {s}")

    # Auto-apply best suggestion (shortest that passes checks)
    best = None
    for s in sorted(suggestions, key=len):
        if check_description_length(s) and not check_description_pushy(s, skill_name):
            best = s
            break

    if best and not dry_run:
        # Update SKILL.md
        new_content = content.replace(f"description: {current_desc}", f"description: {best}")
        if new_content != content:
            skill_md.write_text(new_content, encoding="utf-8")
            log("OK", f"Description actualizada: {best}")
        else:
            log("WARN", "No se pudo aplicar el cambio automáticamente (formato YAML complejo)")
            best = None

    return {
        "skill": skill_name,
        "status": "optimized" if best else "manual_needed",
        "old_desc": current_desc,
        "new_desc": best or "",
        "issues": issues,
        "suggestions": suggestions,
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="ZOLO description optimizer (regla 39)")
    parser.add_argument("skill", nargs="?", help="Skill a optimizar (sin arg = todas)")
    parser.add_argument("--dry-run", action="store_true", help="Solo sugerir, no aplicar")
    parser.add_argument("--all", action="store_true", help="Optimizar TODAS las skills")
    args = parser.parse_args()

    log("INFO", f"ZOLO Description Optimizer v7.0 — regla 39")
    log("INFO", f"Dry run: {args.dry_run or not args.skill and not args.all}")
    print()

    if args.all or not args.skill:
        # Optimize all skills
        skills = sorted([d.name for d in SKILLS_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")])
        log("INFO", f"Optimizando {len(skills)} skills...")
        print()

        results = []
        for skill in skills:
            result = optimize_skill(skill, dry_run=args.dry_run or not args.skill)
            results.append(result)
            print()

        # Summary
        optimized = sum(1 for r in results if r.get("status") == "optimized")
        already = sum(1 for r in results if r.get("status") == "already_optimized")
        manual = sum(1 for r in results if r.get("status") == "manual_needed")

        log("OK", f"Total: {len(results)} | Optimizadas: {optimized} | Ya OK: {already} | Manual: {manual}")

        # Append worklog
        if optimized > 0:
            with WORKLOG.open("a", encoding="utf-8") as f:
                f.write(f"\n### DESCRIPTION OPTIMIZER {datetime.now(timezone.utc).strftime('%Y-%m-%d')} — {len(results)} skills\n")
                f.write(f"- Optimizadas: {optimized} | Ya OK: {already} | Manual: {manual}\n")
    else:
        result = optimize_skill(args.skill, dry_run=args.dry_run)
        if result.get("status") == "optimized":
            return 0
        elif result.get("status") == "manual_needed":
            return 1
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
