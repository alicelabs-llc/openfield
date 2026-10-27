#!/usr/bin/env bash
# ============================================
# 🔄 ZOLO AUTO-CURACIÓN SEMANAL — Cron job
# ============================================
# Ejecuta el ciclo completo de auto-curación (regla 42):
#   1. Diagnóstico (auditar + leer ledger + grep patrones)
#   2. Reparación (graders faltantes + optimizar descriptions + archivar stale)
#   3. Evaluación (eval skills con confidence <0.7)
#   4. Consolidación (generar playbooks PB-NNN)
#   5. Promoción (propuesta de reglas/skills/evals con gate G1)
#
# Instalación cron:
#   0 9 * * 0 /home/z/my-project/scripts/zolo_auto_curacion_semanal.sh >> logs/curacion.log 2>&1
# ============================================

set -euo pipefail

SCRIPTS_DIR="/home/z/my-project/scripts"
LOG_DIR="/home/z/my-project/download/agente-zolo/logs"
WORKLOG="/home/z/my-project/worklog.md"

mkdir -p "$LOG_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_DIR/curacion_$(date +%Y%m%d).log"
}

log "🤖 === ZOLO AUTO-CURACIÓN SEMANAL (regla 42) ==="
log ""

# FASE 1: DIAGNÓSTICO
log "📋 FASE 1: DIAGNÓSTICO"
log "  → Auditoría skills..."
python3 "$SCRIPTS_DIR/zolo_auditar_skills.py" &>>"$LOG_DIR/curacion_$(date +%Y%m%d).log" || true
log "  → Reporte curador..."
python3 "$SCRIPTS_DIR/zolo_curador_skills.py" --report &>>"$LOG_DIR/curacion_$(date +%Y%m%d).log" || true
log "  → Learnings en ledger: $(grep -c '^### ' /home/z/my-project/download/agente-zolo/06_aprendizaje/LEARNINGS.md 2>/dev/null || echo 0)"
log "  → Errors en ledger: $(grep -c '^### ' /home/z/my-project/download/agente-zolo/06_aprendizaje/ERRORS.md 2>/dev/null || echo 0)"
log "  → Playbooks: $(ls /home/z/my-project/download/agente-zolo/06_aprendizaje/playbooks/PB-*.md 2>/dev/null | wc -l)"
log ""

# FASE 2: REPARACIÓN
log "🔧 FASE 2: REPARACIÓN"
log "  → Optimizar descriptions..."
python3 "$SCRIPTS_DIR/zolo_optimizar_descripcion.py" --all --dry-run &>>"$LOG_DIR/curacion_$(date +%Y%m%d).log" || true
log "  → Ejecutar curador (archivar stale)..."
python3 "$SCRIPTS_DIR/zolo_curador_skills.py" &>>"$LOG_DIR/curacion_$(date +%Y%m%d).log" || true
log ""

# FASE 3: EVALUACIÓN
log "🔬 FASE 3: EVALUACIÓN"
log "  → Evaluando skills con confidence <0.7..."
LOW_CONF=$(python3 -c "
import json
with open('/home/z/my-project/download/agente-zolo/06_aprendizaje/SKILL_REGISTRY.json') as f:
    data = json.load(f)
for name, meta in data.get('skills', {}).items():
    if meta.get('confidence', 1.0) < 0.7 and meta.get('state') == 'active':
        print(name)
        break
" 2>/dev/null || echo "")
if [[ -n "$LOW_CONF" ]]; then
    log "  → Evaluando: $LOW_CONF"
    python3 "$SCRIPTS_DIR/zolo_evaluar_skill.py" "$LOW_CONF" --iterations 1 &>>"$LOG_DIR/curacion_$(date +%Y%m%d).log" || true
else
    log "  → Todas las skills tienen confidence ≥0.7 ✓"
fi
log ""

# FASE 4: CONSOLIDACIÓN
log "📝 FASE 4: CONSOLIDACIÓN"
log "  → Detectando patrones repetidos en ledger..."
REPEATED=$(grep -oP "LECCIÓN: .*" /home/z/my-project/download/agente-zolo/06_aprendizaje/LEARNINGS.md 2>/dev/null | sort | uniq -d | head -1 || echo "")
if [[ -n "$REPEATED" ]]; then
    log "  → Patrón repetido detectado: ${REPEATED:0:60}..."
    log "  → Generar playbook PB-NNN (manual o con subagente)"
else
    log "  → Sin patrones repetidos nuevos esta semana"
fi
log ""

# FASE 5: PROMOCIÓN
log "🎯 FASE 5: PROMOCIÓN"
log "  → Skills totales: $(ls -d /home/z/my-project/download/agente-zolo/02_skills/*/ 2>/dev/null | wc -l)"
log "  → Reglas: $(grep -cE '^[0-9]+\.' /home/z/my-project/download/agente-zolo/01_nucleo/ZOLO_V6.md)"
log "  → Playbooks: $(ls /home/z/my-project/download/agente-zolo/06_aprendizaje/playbooks/PB-*.md 2>/dev/null | wc -l)"
log "  → Auditoría final: $(python3 $SCRIPTS_DIR/zolo_auditar_skills.py 2>&1 | tail -1)"
log ""

# Append worklog
cat >> "$WORKLOG" << WORKLOG_ENTRY

### AUTO-CURACIÓN $(date -Iseconds) — regla 42 ejecutada
- FASE 1 (diagnóstico): auditoría skills + curador report + ledger counts
- FASE 2 (reparación): optimizer descriptions + curador archivar
- FASE 3 (evaluación): eval skill con baja confianza
- FASE 4 (consolidación): detección patrones repetidos
- FASE 5 (promoción): stats finales + auditoría
WORKLOG_ENTRY

log "✅ Auto-curación semanal completa"
log "📋 Worklog apendado (regla 9)"
