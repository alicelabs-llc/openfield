#!/bin/bash
# Hacktoberfest runner — ejecutar cuando usuario diga "hacktoberfest"
# Verifica estado de MRs/PRs y muestra plan del día

set -u
DATE=$(date -u +%Y-%m-%dT%H:%M:%SZ)
LOG="/home/z/my-project/hacktoberfest_$(date +%Y%m%d_%H%M).log"

echo "=== Hacktoberfest runner — $DATE ===" | tee "$LOG"
echo "" | tee -a "$LOG"

# Token file: si existe, usar; si no, modo sin auth (solo status público)
TOKEN_PATH="${HOME}/.gitlab_token_v2"
TOKEN=""
if [ -f "$TOKEN_PATH" ]; then
    TOKEN=$(cat "$TOKEN_PATH")
fi

# 1. Estado MRs GitLab
echo "=== Estado MRs GitLab ===" | tee -a "$LOG"

mrs=(
    "OpenMW%2Fopenmw:5667"
    "inkscape%2Fextensions:739"
    "inkscape%2Finkscape:8203"
    "fdroid%2Ffdroidclient:1786"
)

for entry in "${mrs[@]}"; do
    proj="${entry%%:*}"
    iid="${entry##*:}"
    if [ -n "$TOKEN" ]; then
        status=$(curl -sS --max-time 10 -H "PRIVATE-TOKEN: $TOKEN" \
          "https://gitlab.com/api/v4/projects/$proj/merge_requests/$iid" 2>/dev/null | \
          python3 -c "
import json,sys
try:
    d = json.load(sys.stdin)
    print(f\"{d.get('state','?'):10} notes={d.get('user_notes_count',0)} conflicts={d.get('has_conflicts')}\")
except: print('err')
" 2>/dev/null)
    else
        status="(sin token - usa archivo $TOKEN_PATH)"
    fi
    echo "  !${iid} ($proj): $status" | tee -a "$LOG"
    sleep 2
done

# 2. Estado PR GitHub dino #124
echo "" | tee -a "$LOG"
echo "=== PR GitHub dino #124 ===" | tee -a "$LOG"
gh pr view 124 --repo meetdino/dino --json state,mergedAt,title 2>&1 | head -10 | tee -a "$LOG"

# 3. Verificar patches preparados
echo "" | tee -a "$LOG"
echo "=== Patches preparados para hoy ===" | tee -a "$LOG"
for patch in /home/z/my-project/download/hacktoberfest-*.patch; do
    if [ -f "$patch" ]; then
        name=$(basename "$patch")
        lines=$(wc -l < "$patch")
        echo "  $name ($lines líneas)" | tee -a "$LOG"
    fi
done

# 4. Plan del día
echo "" | tee -a "$LOG"
echo "=== Plan para hoy ===" | tee -a "$LOG"
cat <<'PLAN' | tee -a "$LOG"

1. Responder maintainer dino PR #124 (texto en HACKTOBERFEST_TRACKER.md)
2. Enviar PR #1: vajra #29 (Linux installer skip on macOS)
3. Enviar PR #2: harbour #41 (filter control chars in history)
4. Enviar PR #3: Prism-platform #388 (md5 → sha256 cache filenames)

Para enviar cada PR, pídeme "script 1", "script 2" o "script 3".
Te paso el PowerShell completo con todo preparado.

Otros concursos activos:
- MLH Global Hack Week (todo octubre): https://ghw.mlh.io
- 24 Pull Requests (1-24 diciembre): https://24pullrequests.com
- DoraHacks Buidls (continuo, $5000): https://dorahacks.io
- Outreachy ($7000 internships): https://outreachy.org

PLAN

echo "" | tee -a "$LOG"
echo "=== Fin del reporte. Logs en $LOG ===" | tee -a "$LOG"
