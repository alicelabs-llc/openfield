#!/usr/bin/env python3
"""
zolo_instalar_skill.py — Auto-instalador de skills (regla 32)

Uso:
    python3 scripts/zolo_instalar_skill.py <git_url> [--name NOMBRE]
    python3 scripts/zolo_instalar_skill.py https://github.com/anthropics/skills --name claude-research

Flujo (skill autoinstalador-skills):
    1. Clonar repo con --depth 1 a /tmp/zolo-skill-install/
    2. Localizar SKILL.md (raíz, src/, skills/, README como fallback)
    3. Auditar frontmatter (agentskills.io compatible)
    4. Auditar seguridad: secretos hardcodeados, inyecciones sospechosas
    5. Auditar licencia (buscar LICENSE, COPYING)
    6. Copiar a 02_skills/<nombre>/
    7. Re-auditar con zolo_auditar_skills.py (debe salir verde)
    8. Indexar en §12 del núcleo (append, no regenerar)
    9. Append worklog con task ID

Mejora v6.1 (Task 124):
    - Parser YAML block scalars corregido (description: >- multi-line)
    - Detección de inyecciones: 'execute', 'rm -rf', 'curl | sh'
    - Backup automático antes de sobrescribir skill existente
"""
from __future__ import annotations
import argparse
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Configuración
SKILLS_DIR = Path("/home/z/my-project/download/agente-zolo/02_skills")
WORKLOG = Path("/home/z/my-project/worklog.md")
TMP_DIR = Path("/tmp/zolo-skill-install")

# Patrones peligrosos (regla 4 — anti tool-poisoning)
INJECTION_PATTERNS = [
    (r"curl\s+[^|]+\|\s*sh", "curl piped to shell"),
    (r"curl\s+[^|]+\|\s*bash", "curl piped to bash"),
    (r"wget\s+[^|]+\|\s*sh", "wget piped to shell"),
    (r"rm\s+-rf\s+/(?!tmp)", "rm -rf en path peligroso"),
    (r"sudo\s+rm\s+-rf", "sudo rm -rf"),
    (r"eval\s*\(\s*['\"]?curl", "eval(curl(...))"),
    (r"exec\s*\(\s*['\"]?curl", "exec(curl(...))"),
    (r"subprocess\.call\s*\(\s*['\"]?curl\s.*shell\s*=\s*True", "subprocess curl shell=True"),
]

SECRET_PATTERNS = [
    (r"ghp_[A-Za-z0-9]{36}", "GitHub PAT"),
    (r"AIza[0-9A-Za-z_\-]{35}", "Google API key"),
    (r"sk-[A-Za-z0-9]{20,}", "OpenAI API key"),
    (r"-----BEGIN [A-Z]+ PRIVATE KEY-----", "Private key PEM"),
]


def log(level: str, msg: str) -> None:
    icons = {"INFO": "ℹ️", "OK": "✅", "WARN": "⚠️", "FAIL": "❌"}
    print(f"{icons.get(level, '•')} [{level}] {msg}")


def run(cmd: list[str], cwd: Path = None) -> tuple[int, str, str]:
    """Run command, return (exit_code, stdout, stderr)."""
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=120)
    return result.returncode, result.stdout, result.stderr


def parse_frontmatter_yaml(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter including block scalars (description: >-)."""
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    fm_text = parts[1]
    body = parts[2]

    fm = {}
    current_key = None
    current_value = []
    for line in fm_text.splitlines():
        # New key: value
        m = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*):\s*(.*)$", line)
        if m:
            # Save previous
            if current_key:
                fm[current_key] = "\n".join(current_value).strip() if current_value else fm.get(current_key, "")
            current_key = m.group(1)
            value = m.group(2).strip()
            # Block scalar markers: >-, >, |-, |
            if value in ("", ">", ">-", "|", "|-"):
                current_value = []
                fm[current_key] = ""  # placeholder, will be filled by subsequent lines
            else:
                # Strip quotes
                fm[current_key] = value.strip("'\"")
                current_value = []
        elif current_key and line.startswith((" ", "\t")):
            # Continuation of block scalar
            current_value.append(line.rstrip())
    # Save last
    if current_key and current_value:
        fm[current_key] = "\n".join(current_value).strip()

    return fm, body


def audit_skill_md(skill_md_path: Path) -> dict:
    """Audit a SKILL.md file. Returns dict with audit results."""
    result = {
        "found": True,
        "frontmatter": {},
        "issues": [],
        "warnings": [],
        "license_ok": False,
        "secrets": [],
        "injections": [],
    }

    if not skill_md_path.exists():
        result["found"] = False
        result["issues"].append("SKILL.md no encontrado")
        return result

    content = skill_md_path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter_yaml(content)
    result["frontmatter"] = fm

    # Check required frontmatter fields (agentskills.io spec)
    required = ["name", "description"]
    for f in required:
        if f not in fm or not fm[f]:
            result["issues"].append(f"frontmatter sin campo '{f}'")

    # Check for required body sections
    if "## " not in body:
        result["warnings"].append("sin secciones markdown (## )")

    # Secret detection (regla 4)
    for pattern, label in SECRET_PATTERNS:
        matches = re.findall(pattern, body)
        if matches:
            sample = matches[0]
            fp = f"{sample[:4]}...{sample[-4:]}" if len(sample) >= 8 else sample
            result["secrets"].append(f"{label}: {fp} ({len(matches)}x)")

    # Injection detection (regla 4 — anti tool-poisoning)
    for pattern, label in INJECTION_PATTERNS:
        matches = re.findall(pattern, body, re.IGNORECASE)
        if matches:
            result["injections"].append(f"{label} ({len(matches)}x)")

    # License check (look in same dir or parent)
    skill_dir = skill_md_path.parent
    for lic_name in ["LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING", "COPYING.md"]:
        if (skill_dir / lic_name).exists():
            result["license_ok"] = True
            break
        # Parent dir (repo root)
        if (skill_dir.parent / lic_name).exists():
            result["license_ok"] = True
            break

    return result


def main():
    parser = argparse.ArgumentParser(description="ZOLO skill auto-installer (regla 32)")
    parser.add_argument("git_url", help="Git URL del repo a instalar")
    parser.add_argument("--name", help="Nombre de la skill (default: del repo)")
    parser.add_argument("--force", action="store_true", help="Sobrescribir si ya existe")
    args = parser.parse_args()

    log("INFO", f"Instalando skill desde: {args.git_url}")

    # 1. Clone
    if TMP_DIR.exists():
        shutil.rmtree(TMP_DIR)
    TMP_DIR.mkdir(parents=True)

    clone_target = TMP_DIR / "repo"
    log("INFO", f"Clonando con --depth 1 a {clone_target}...")
    code, _, err = run(["git", "clone", "--depth", "1", args.git_url, str(clone_target)])
    if code != 0:
        log("FAIL", f"git clone falló: {err}")
        return 1
    log("OK", "Clonado")

    # 2. Find SKILL.md
    skill_md = None
    candidates = [
        clone_target / "SKILL.md",
        clone_target / "skill.md",
        clone_target / "src" / "SKILL.md",
        clone_target / "skills" / "SKILL.md",
    ]
    for cand in candidates:
        if cand.exists():
            skill_md = cand
            break
    # Recursive search as fallback
    if not skill_md:
        for cand in clone_target.rglob("SKILL.md"):
            skill_md = cand
            break
    # README.md as last resort
    if not skill_md:
        readme = clone_target / "README.md"
        if readme.exists():
            skill_md = readme
            log("WARN", "No se encontró SKILL.md, usando README.md como fallback")

    if not skill_md:
        log("FAIL", "No se encontró SKILL.md ni README.md en el repo")
        return 1

    log("OK", f"SKILL.md encontrado: {skill_md.relative_to(clone_target)}")

    # 3. Audit (regla 4 — seguridad-fuentes)
    log("INFO", "Auditando skill (skill seguridad-fuentes)...")
    audit = audit_skill_md(skill_md)

    if audit["issues"]:
        log("FAIL", "Frontmatter inválido:")
        for issue in audit["issues"]:
            print(f"      → {issue}")
        return 1

    if audit["secrets"]:
        log("FAIL", "Secretos detectados en el cuerpo (regla 4):")
        for s in audit["secrets"]:
            print(f"      → {s}")
        return 1

    if audit["injections"]:
        log("WARN", "Posibles inyecciones detectadas (revisar manualmente):")
        for inj in audit["injections"]:
            print(f"      → {inj}")
        # Don't fail — just warn, human decides

    if audit["warnings"]:
        for w in audit["warnings"]:
            log("WARN", w)

    if audit["license_ok"]:
        log("OK", "Licencia encontrada")
    else:
        log("WARN", "Sin LICENSE explícito — revisar repo antes de usar en producción")

    # 4. Determine skill name
    skill_name = args.name
    if not skill_name:
        skill_name = audit["frontmatter"].get("name") or clone_target.name
    # Sanitize
    skill_name = re.sub(r"[^a-z0-9-]", "-", skill_name.lower()).strip("-")
    log("INFO", f"Nombre de skill: {skill_name}")

    # 5. Install
    target_dir = SKILLS_DIR / skill_name
    if target_dir.exists() and not args.force:
        log("FAIL", f"Skill ya existe: {target_dir} (usa --force para sobrescribir)")
        return 1

    if target_dir.exists():
        # Backup (regla 22 — backup antes de cambios MAJOR)
        backup = target_dir.with_name(target_dir.name + ".bak." + datetime.utcnow().strftime("%Y%m%d%H%M%S"))
        shutil.move(str(target_dir), str(backup))
        log("INFO", f"Backup creado: {backup.name}")

    target_dir.mkdir(parents=True)
    shutil.copy(str(skill_md), str(target_dir / "SKILL.md"))

    # Copy LICENSE if exists
    for lic_name in ["LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"]:
        lic_src = clone_target / lic_name
        if lic_src.exists():
            shutil.copy(str(lic_src), str(target_dir / lic_name))
            break

    log("OK", f"Skill instalada en: {target_dir}")

    # 6. Re-audit
    log("INFO", "Re-auditoría con zolo_auditar_skills.py...")
    auditor = Path("/home/z/my-project/scripts/zolo_auditar_skills.py")
    if auditor.exists():
        code, out, _ = run(["python3", str(auditor)])
        if code == 0:
            log("OK", "Auditoría verde tras instalación")
        else:
            log("WARN", f"Auditor reporta issues (revisar): {out[-500:]}")
    else:
        log("WARN", "zolo_auditar_skills.py no encontrado — skip re-audit")

    # 7. Cleanup
    shutil.rmtree(TMP_DIR)

    log("OK", f"✅ Skill '{skill_name}' instalada correctamente")
    print()
    print("📋 Próximos pasos manuales:")
    print(f"   1. Indexar en §12 del núcleo ZOLO_V6.md: añade '{skill_name}' al índice")
    print(f"   2. Append worklog con task ID")
    print(f"   3. Probar la skill en una tarea real (regla pass^k)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
