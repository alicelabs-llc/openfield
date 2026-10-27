#!/usr/bin/env python3
"""
zolo_auditar_skills.py — Auditor de skills del paquete ZOLO (regla 32, E52)

Uso:
    python3 scripts/zolo_auditar_skills.py

Salida:
    - Por cada skill en 02_skills/: verifica SKILL.md, frontmatter, secretos
    - Exit code 0 = todas OK (auditor verde)
    - Exit code 1 = al menos una skill falla (auditor rojo, no eres ZOLO)

Criterios (alineados con agentskills.io spec v1):
    BLOCKING (fail):
      - SKILL.md no existe
      - Sin frontmatter YAML (no empieza con ---)
      - Sin campo 'name' o 'description' en frontmatter
      - Secretos hardcodeados en el cuerpo (regla 4)
    NON-BLOCKING (warn):
      - Sin sección '## Grader' (regla 28, recomendado)
      - Sin sección '## Cuándo' / '## Pasos' (nomenclatura flexible)
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

# Configuración
SKILLS_DIR = Path("/home/z/my-project/download/agente-zolo/02_skills")

# Patrones de secretos sospechosos — específicos para evitar false positives
SECRET_PATTERNS = [
    (r"ghp_[A-Za-z0-9]{36}", "GitHub PAT"),
    (r"github_pat_[A-Za-z0-9_]{82}", "GitHub PAT v2"),
    (r"AIza[0-9A-Za-z_\-]{35}", "Google API key"),
    (r"sk-[A-Za-z0-9]{20,}", "OpenAI API key"),
    (r"-----BEGIN [A-Z]+ PRIVATE KEY-----", "Private key PEM"),
]


def extract_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter between --- markers."""
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    fm_text = parts[1].strip()
    body = parts[2]
    fm = {}
    for line in fm_text.splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip().strip("'\"")
    return fm, body


def audit_skill(skill_dir: Path) -> dict:
    """Audit one skill directory. Returns dict with status."""
    skill_md = skill_dir / "SKILL.md"
    name = skill_dir.name

    result = {
        "name": name,
        "ok": True,
        "issues": [],          # blocking
        "warnings": [],        # non-blocking
        "frontmatter": {},
        "has_grader": False,
        "has_secret": False,
    }

    # 1. SKILL.md exists (BLOCKING)
    if not skill_md.exists():
        result["ok"] = False
        result["issues"].append("SKILL.md no existe")
        return result

    content = skill_md.read_text(encoding="utf-8")

    # 2. Frontmatter (BLOCKING if missing)
    fm, body = extract_frontmatter(content)
    result["frontmatter"] = fm
    if not fm:
        result["ok"] = False
        result["issues"].append("sin frontmatter YAML (debe empezar con ---)")
    else:
        # agentskills.io spec: 'name' and 'description' are required
        for field in ["name", "description"]:
            if field not in fm or not fm[field]:
                result["ok"] = False
                result["issues"].append(f"frontmatter sin campo '{field}'")

    # 3. Grader section (NON-BLOCKING — regla 28, recomendado)
    if "## Grader" in body or "## grader" in body.lower() or "## Cómo verificar" in body or "## Verificación" in body:
        result["has_grader"] = True
    else:
        result["warnings"].append("sin sección '## Grader' (regla 28 — recomendado)")

    # 4. Sections (NON-BLOCKING — nomenclatura flexible)
    if "## " not in body:
        result["warnings"].append("sin secciones markdown (## )")

    # 5. Secret detection (BLOCKING — regla 4)
    for pattern, label in SECRET_PATTERNS:
        matches = re.findall(pattern, body)
        if matches:
            result["has_secret"] = True
            result["ok"] = False
            sample = matches[0]
            fp = f"{sample[:4]}...{sample[-4:]}" if len(sample) >= 8 else sample
            result["issues"].append(f"posible {label} en cuerpo: {fp} ({len(matches)} ocurrencias)")

    return result


def main():
    if not SKILLS_DIR.exists():
        print(f"❌ No encuentro skills dir: {SKILLS_DIR}", file=sys.stderr)
        return 1

    skills = sorted([d for d in SKILLS_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")])
    print(f"🔍 Auditoría de skills ZOLO v6.1")
    print(f"   Directorio: {SKILLS_DIR}")
    print(f"   Skills encontradas: {len(skills)}")
    print()

    ok_count = 0
    fail_count = 0
    results = []

    for skill_dir in skills:
        r = audit_skill(skill_dir)
        results.append(r)
        if r["ok"]:
            ok_count += 1
            grader = "✓" if r["has_grader"] else "—"
            warn_str = f" [{len(r['warnings'])} warn]" if r["warnings"] else ""
            print(f"  ✓ {r['name']:40s} grader={grader}{warn_str}")
        else:
            fail_count += 1
            print(f"  ✗ {r['name']:40s}")
            for issue in r["issues"]:
                print(f"      → {issue}")
            for w in r["warnings"]:
                print(f"      (warn) {w}")

    print()
    print(f"📊 Resultado: {ok_count}/{len(skills)} OK · {fail_count} FAIL")

    if fail_count == 0:
        print("✅ Auditoría VERDE — paquete ZOLO consistente (regla E52)")
        return 0
    else:
        print("❌ Auditoría ROJA — paquete ZOLO inconsistente. NO eres ZOLO hasta arreglar.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
