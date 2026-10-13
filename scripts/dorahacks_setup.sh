#!/bin/bash
# DoraHacks setup script - evalúa alethech-publish-2 como Dora Grant DAO candidate

set -u
DATE=$(date -u +%Y-%m-%dT%H:%M:%SZ)
LOG="/home/z/my-project/dorahacks_setup_$(date +%Y%m%d_%H%M).log"

echo "=== DoraHacks setup — $DATE ===" | tee "$LOG"
echo "" | tee -a "$LOG"

REPO_PATH="/home/z/my-project/alethech-publish-2"

if [ ! -d "$REPO_PATH" ]; then
    echo "ERROR: $REPO_PATH no existe" | tee -a "$LOG"
    exit 1
fi

# 1. Métricas del repo
echo "=== Métricas de alethech-publish-2 ===" | tee -a "$LOG"
cd "$REPO_PATH"

echo "" | tee -a "$LOG"
echo "Commits totales: $(git log --oneline 2>/dev/null | wc -l)" | tee -a "$LOG"
echo "Último commit: $(git log -1 --format='%h %ad %s' --date=short 2>/dev/null)" | tee -a "$LOG"
echo "Contributors: $(git shortlog -sn 2>/dev/null | wc -l)" | tee -a "$LOG"
echo "Archivos tracked: $(git ls-files 2>/dev/null | wc -l)" | tee -a "$LOG"
echo "Lenguajes:" | tee -a "$LOG"
echo "  Python: $(git ls-files '*.py' 2>/dev/null | wc -l) archivos" | tee -a "$LOG"
echo "  Rust: $(git ls-files '*.rs' 2>/dev/null | wc -l) archivos" | tee -a "$LOG"
echo "  TypeScript: $(git ls-files '*.ts' 2>/dev/null | wc -l) archivos" | tee -a "$LOG"
echo "  WASM: $(git ls-files '*.wasm' 2>/dev/null | wc -l) archivos" | tee -a "$LOG"

echo "" | tee -a "$LOG"
echo "=== DoraHacks readiness check ===" | tee -a "$LOG"

# Verificar requisitos
check_pass() {
    echo "  [✓] $1" | tee -a "$LOG"
}

check_fail() {
    echo "  [✗] $1" | tee -a "$LOG"
}

check_warn() {
    echo "  [⚠] $1" | tee -a "$LOG"
}

# License
if [ -f "LICENSE" ]; then
    license=$(head -1 LICENSE)
    if echo "$license" | grep -qi "MIT"; then
        check_pass "License MIT (compatible con DoraHacks)"
    elif echo "$license" | grep -qi "Apache"; then
        check_pass "License Apache (compatible con DoraHacks)"
    else
        check_warn "License presente pero tipo: $license"
    fi
else
    check_fail "Sin LICENSE file"
fi

# README
if [ -f "README.md" ]; then
    readme_lines=$(wc -l < README.md)
    if [ "$readme_lines" -gt 100 ]; then
        check_pass "README completo ($readme_lines líneas)"
    else
        check_warn "README corto ($readme_lines líneas)"
    fi
else
    check_fail "Sin README.md"
fi

# CONTRIBUTING
if [ -f "CONTRIBUTING.md" ]; then
    check_pass "CONTRIBUTING.md presente"
else
    check_warn "Sin CONTRIBUTING.md (recomendado para community signal)"
fi

# Tests
test_count=$(find . -name "test_*.py" -o -name "*_test.py" -o -name "tests.rs" 2>/dev/null | grep -v "/.git/\|/node_modules/" | wc -l)
if [ "$test_count" -gt 5 ]; then
    check_pass "Test suite robusta ($test_count archivos de test)"
else
    check_warn "Tests insuficientes ($test_count archivos)"
fi

# CI
if [ -f ".github/workflows/ci.yml" ] || [ -f ".gitlab-ci.yml" ]; then
    check_pass "CI/CD configurado"
else
    check_warn "Sin CI/CD visible"
fi

# PyPI published
if grep -q "PyPI" README.md 2>/dev/null; then
    check_pass "Publicado en PyPI"
else
    check_warn "No visible en PyPI"
fi

# Documentation
if [ -d "docs" ]; then
    docs_count=$(find docs -name "*.md" 2>/dev/null | wc -l)
    check_pass "Documentación ($docs_count archivos en docs/)"
else
    check_warn "Sin directorio docs/"
fi

# Examples
if [ -d "examples" ]; then
    examples_count=$(find examples -name "*.py" -o -name "*.ts" 2>/dev/null | wc -l)
    check_pass "Examples ($examples_count archivos)"
else
    check_warn "Sin directorio examples/"
fi

echo "" | tee -a "$LOG"
echo "=== Gaps identificados (acciones para octubre) ===" | tee -a "$LOG"
cat <<'GAPS' | tee -a "$LOG"

1. STAR COUNT — actualmente 0 stars
   Acción: promocionar en dev.to, HN, Twitter/BlueSky
   Meta: 50 stars para 1 nov 2026

2. DEMO VIDEO — no existe
   Acción: grabar 3 min demo del flujo init → commit → verify
   Meta: subir a YouTube antes de 15 nov 2026

3. EXTERNAL CONTRIBUTORS — solo tú
   Acción: durante Hacktoberfest, marcar issues como "good first issue"
   Meta: 2 contributors externos antes de 1 dic 2026

4. USE CASES DOC — falta casos reales
   Acción: escribir 3 use cases (agent continuity, audit log, supply chain)
   Meta: 1 caso por semana, 3 antes de 1 dic 2026

5. AWESOME-LIST LISTING — no listado
   Acción: PR a awesome-agent-memory, awesome-crypto, awesome-python
   Meta: 1 PR por semana a awesome-lists

GAPS

echo "" | tee -a "$LOG"
echo "=== Siguiente paso ===" | tee -a "$LOG"
echo "Revisar DORAHACKS_PLAN.md para plan completo de Q4 2026 - Q1 2027" | tee -a "$LOG"
