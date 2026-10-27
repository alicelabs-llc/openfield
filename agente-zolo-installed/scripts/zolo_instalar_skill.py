#!/usr/bin/env python3
"""ZOLO — Autoinstalador de skills (regla 32, v6.0).

Ciclo automatizado: CLONAR → localizar SKILL.md → AUDITAR (frontmatter, secretos, licencia).
Los pasos ADAPTAR → INDEXAR siempre los hace el agente (skill autoinstalador-skills §1).

Uso:
  python3 zolo_instalar_skill.py --repo owner/repo [--skill nombre] [--list] [--dry-run] [--dest DIR]
  python3 zolo_instalar_skill.py --local ruta/al/repo-clonado [--skill nombre] [--list]
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPOS_DIR = Path("/home/z/my-project/repos")
DEFAULT_DEST = Path("/home/z/my-project/download/agente-zolo/02_skills")

SECRET_PATTERNS = [
    (r"ghp_[A-Za-z0-9]{20,}", "token GitHub"),
    (r"github_pat_[A-Za-z0-9_]{20,}", "fine-grained GitHub PAT"),
    (r"sk-[A-Za-z0-9]{20,}", "API key estilo OpenAI"),
    (r"AKIA[0-9A-Z]{16}", "AWS Access Key"),
    (r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----", "clave privada"),
    (r"xox[baprs]-[A-Za-z0-9-]{10,}", "token Slack"),
]

DANGEROUS_HINTS = [
    ("~/.ssh", "pide clave SSH"),
    (".env", "referencia a archivo de secretos"),
    ("send.*token", "envío de token"),
    ("curl.*&&.*sh", "pipe a shell"),
]


def clone(repo: str) -> Path:
    REPOS_DIR.mkdir(parents=True, exist_ok=True)
    dest = REPOS_DIR / repo.replace("/", "_")
    if dest.exists() and (dest / ".git").exists():
        print(f"[reuso] {dest} ya clonado")
        return dest
    url = f"https://github.com/{repo}.git" if "/" in repo and not repo.startswith("http") else repo
    print(f"[clone --depth 1] {url} → {dest}")
    r = subprocess.run(["git", "clone", "--depth", "1", "--quiet", url, str(dest)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"[ERROR] clone falló: {r.stderr.strip()[:300]}")
    return dest


def parse_frontmatter(path: Path):
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return None, text
    fm, body_lines = {}, m.group(1).splitlines()
    i = 0
    while i < len(body_lines):
        line = body_lines[i]
        if ":" in line and not line.strip().startswith(("#", "-")):
            k, _, v = line.partition(":")
            key, val = k.strip(), v.strip()
            # YAML block scalars: >-, >, |, |+ (descripciones multi-línea)
            if val in (">-", ">", "|", "|-", "|+") and i + 1 < len(body_lines):
                chunks, i = [], i + 1
                while i < len(body_lines) and (
                    body_lines[i].startswith("  ") or not body_lines[i].strip()
                ):
                    chunks.append(body_lines[i].strip())
                    i += 1
                fm[key] = " ".join(c for c in chunks if c).strip('"\'')
                continue
            fm[key] = val.strip('"\'')
        i += 1
    return fm, text


def audit(path: Path):
    """Devuelve (hallazgos, severidad_max) — severidad: ok|warn|FAIL."""
    findings, sev = [], "ok"
    fm, body = parse_frontmatter(path)
    if not fm:
        findings.append(("FAIL", "sin frontmatter YAML — no es una skill instalable"))
        return findings, "FAIL"
    name, desc = fm.get("name", ""), fm.get("description", "")
    if not name:
        findings.append(("FAIL", "frontmatter sin 'name'"))
    if len(desc) < 20:
        findings.append(("FAIL", "descripción ausente o demasiado corta (<20) — no hay disparadores"))
    else:
        findings.append(("ok", f"name={name} · description={len(desc)} chars"))
    if (path.parent / "LICENSE").exists() or any(p.name.upper().startswith("LICENSE") for p in path.parent.glob("*")):
        findings.append(("ok", "licencia presente en el repo"))
    else:
        findings.append(("warn", "sin LICENSE en la raíz del repo — revisar antes de adaptar"))
    for pat, label in SECRET_PATTERNS:
        if re.search(pat, body):
            findings.append(("FAIL", f"SECRETO detectado en el cuerpo ({label}) — NO instalar sin saneo"))
    for hint, label in DANGEROUS_HINTS:
        if re.search(hint, body, re.IGNORECASE):
            findings.append(("warn", f"patrón sensible: {label} — revisar contexto"))
    if re.search(r"ignore (all|previous|prior) instructions", body, re.IGNORECASE):
        findings.append(("FAIL", "intentos de inyección ('ignore previous instructions') — DATO tóxico"))
    worst = "ok"
    for s, _ in findings:
        if s == "FAIL":
            worst = "FAIL"
        elif s == "warn" and worst != "FAIL":
            worst = "warn"
    return findings, worst


def find_skills(root: Path):
    return sorted(root.rglob("SKILL.md"))


def install(src_skill: Path, name_hint: str | None, dest_dir: Path, dry: bool):
    fm, _ = parse_frontmatter(src_skill)
    name = (fm or {}).get("name") or name_hint or src_skill.parent.name
    name = re.sub(r"[^a-z0-9-]", "-", name.lower()).strip("-")
    dest = dest_dir / name
    if dest.exists():
        return dest, "warn", "ya existe en destino (usar flujo de MEJORA, autoinstalador-skills §2)"
    if dry:
        return dest, "ok", "dry-run: no se copió"
    shutil.copytree(src_skill.parent, dest, ignore=shutil.ignore_patterns(".git", "node_modules"))
    return dest, "ok", "instalado (pendiente ADAPTAR al protocolo ZOLO + INDEXAR §12)"


def main():
    ap = argparse.ArgumentParser(description="ZOLO autoinstalador de skills (regla 32)")
    ap.add_argument("--repo", help="owner/repo o URL git")
    ap.add_argument("--local", help="ruta a repo ya clonado")
    ap.add_argument("--skill", help="nombre de skill concreta (opcional)")
    ap.add_argument("--list", action="store_true", help="solo listar skills del repo")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--dest", default=str(DEFAULT_DEST))
    args = ap.parse_args()

    if not (args.repo or args.local):
        sys.exit("requiere --repo owner/repo o --local ruta")
    root = Path(args.local) if args.local else clone(args.repo)
    if not root.exists():
        sys.exit(f"[ERROR] {root} no existe")

    skills = find_skills(root)
    if args.skill:
        skills = [s for s in skills if args.skill.lower() in str(s).lower() or args.skill.lower() in s.parent.name.lower()]
    if not skills:
        sys.exit("[INFO] sin SKILL.md — repo no instala skills (usarlo como fuente de patrones)")

    print(f"\n== {len(skills)} skill(s) en {root.name} ==")
    report = []
    for s in skills:
        findings, worst = audit(s)
        print(f"\n— {s.relative_to(root)}  [{worst.upper()}]")
        for sev, msg in findings:
            print(f"    {sev:4} {msg}")
        report.append({"skill": str(s.relative_to(root)), "estado": worst})
        if worst == "FAIL":
            print("    → NO instalar: auditar con seguridad-fuentes o descartar")
            continue
        if not args.list and worst in ("ok", "warn"):
            dest, st, msg = install(s, args.skill, Path(args.dest), args.dry_run)
            print(f"    → [{st}] {dest} — {msg}")

    out = Path("/home/z/my-project/scripts/zolo_instalador_last.json")
    out.write_text(json.dumps({"repo": str(root), "skills": report}, ensure_ascii=False, indent=2))
    print(f"\n[reporte] {out} — los pasos ADAPTAR+INDEXAR son del agente (regla 32)")


if __name__ == "__main__":
    main()
