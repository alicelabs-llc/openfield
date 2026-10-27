#!/usr/bin/env python3
"""ZOLO — Auditor de skills locales (regla 32/28, v6.0).

Verifica TODAS las skills del paquete: frontmatter válido, name/description presentes,
name coherente con la carpeta, sin secretos, longitud razonable. Salida tabla + conteo.
Exit code 1 si hay FAIL (útil como grader determinista de la suite E).
"""
import re
import sys
from pathlib import Path

SKILLS_DIR = Path("/home/z/my-project/download/agente-zolo/02_skills")

SECRET_PATTERNS = [
    r"ghp_[A-Za-z0-9]{20,}", r"github_pat_[A-Za-z0-9_]{20,}",
    r"sk-[A-Za-z0-9]{20,}", r"AKIA[0-9A-Z]{16}",
    r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----",
]


def audit(skill_md: Path):
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return "FAIL", ["sin frontmatter"]
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.strip().startswith(("#", "-")):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip().strip("'\"")
    problems = []
    name = fm.get("name", "")
    desc = fm.get("description", "")
    folder = skill_md.parent.name
    if not name:
        problems.append("sin name")
    elif name != folder and name.replace("_", "-") != folder.replace("_", "-"):
        problems.append(f"name≠carpeta ({name} vs {folder})")
    if len(desc) < 20:
        problems.append("description corta/ausente")
    body_len = len(text) - m.end()
    if body_len < 500:
        problems.append(f"cuerpo muy corto ({body_len} chars) — skill sin sustancia")
    if "grader" not in text.lower() and "GradER" not in text:
        problems.append("sin sección Grader (protocolo ZOLO)")
    for pat in SECRET_PATTERNS:
        if re.search(pat, text):
            problems.append("SECRETO en el cuerpo")
            break
    return ("FAIL" if any("SECRETO" in p or "sin frontmatter" in p for p in problems)
            else "WARN" if problems else "ok"), problems


def main():
    if not SKILLS_DIR.exists():
        sys.exit(f"[ERROR] {SKILLS_DIR} no existe")
    skills = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    if not skills:
        sys.exit("[ERROR] sin skills")
    counts = {"ok": 0, "WARN": 0, "FAIL": 0}
    print(f"== Auditoría de skills — {SKILLS_DIR} ({len(skills)}) ==\n")
    for s in skills:
        status, problems = audit(s)
        counts[status] += 1
        line = f"{status:4} {s.parent.name}"
        if problems:
            line += "  → " + "; ".join(problems)
        print(line)
    print(f"\nRESUMEN: {len(skills)} skills · ok={counts['ok']} · warn={counts['WARN']} · fail={counts['FAIL']}")
    sys.exit(1 if counts["FAIL"] else 0)


if __name__ == "__main__":
    main()
