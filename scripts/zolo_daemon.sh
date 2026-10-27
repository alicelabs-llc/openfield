#!/usr/bin/env bash
# ============================================
# 🤖 ZOLO DAEMON — Corre en background mientras la PC está prendida
# ============================================
# Ejecuta el ciclo de auto-mejora continuamente:
#   1. Curador de skills (cada hora)
#   2. Optimizador de descriptions (cada 4h)
#   3. Eval harness (cada 8h)
#   4. Sueño-consolidación (cada 24h)
#   5. Supervisor meta check (cada 30 min)
#
# Instalación:
#   chmod +x scripts/zolo_daemon.sh
#   nohup scripts/zolo_daemon.sh > logs/daemon.log 2>&1 &
#   echo $! > logs/daemon.pid
#
# Para parar:
#   kill $(cat logs/daemon.pid)
# ============================================

set -euo pipefail

SCRIPTS_DIR="/home/z/my-project/scripts"
LOG_DIR="/home/z/my-project/download/agente-zolo/logs"
PID_FILE="$LOG_DIR/daemon.pid"
STATE_FILE="$LOG_DIR/daemon_state.json"

mkdir -p "$LOG_DIR"

# Verificar que no hay otro daemon corriendo
if [[ -f "$PID_FILE" ]]; then
    OLD_PID=$(cat "$PID_FILE")
    if kill -0 "$OLD_PID" 2>/dev/null; then
        echo "❌ Daemon ya corriendo (PID $OLD_PID). Usa 'kill $OLD_PID' primero."
        exit 1
    else
        rm -f "$PID_FILE"
    fi
fi

# Guardar PID
echo $$ > "$PID_FILE"
echo "🤖 ZOLO Daemon iniciado (PID $$)"

# Función de logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_DIR/daemon_$(date +%Y%m%d).log"
}

# Intervalos (en segundos)
INTERVAL_SUPERVISOR=1800      # 30 min
INTERVAL_CURADOR=3600         # 1h
INTERVAL_OPTIMIZER=14400      # 4h
INTERVAL_EVAL=28800           # 8h
INTERVAL_SUEÑO=86400          # 24h

# Timestamps de última ejecución
LAST_SUPERVISOR=0
LAST_CURADOR=0
LAST_OPTIMIZER=0
LAST_EVAL=0
LAST_SUEÑO=0

# Estado inicial
echo "{\"started\":\"$(date -Iseconds)\",\"pid\":$$}" > "$STATE_FILE"

log "=== ZOLO Daemon v7.0 ==="
log "Intervalos: supervisor=${INTERVAL_SUPERVISOR}s curador=${INTERVAL_CURADOR}s optimizer=${INTERVAL_OPTIMIZER}s eval=${INTERVAL_EVAL}s sueño=${INTERVAL_SUEÑO}s"
log "Logs en: $LOG_DIR"
log "Para parar: kill \$(cat $PID_FILE)"
log ""

# Trap para cleanup
cleanup() {
    log "Daemon detenido (signal recibido)"
    rm -f "$PID_FILE"
    echo "{\"stopped\":\"$(date -Iseconds)\"}" > "$STATE_FILE"
    exit 0
}
trap cleanup SIGINT SIGTERM

# Loop principal
while true; do
    NOW=$(date +%s)

    # 1. Supervisor meta check (cada 30 min)
    if (( NOW - LAST_SUPERVISOR >= INTERVAL_SUPERVISOR )); then
        log "🔍 Supervisor meta check..."
        # Verificar si hay patrones de stall en el worklog
        if grep -q "Task ID:" /home/z/my-project/worklog.md 2>/dev/null; then
            LAST_TASK=$(grep "Task ID:" /home/z/my-project/worklog.md | tail -1 | awk '{print $3}')
            log "   Último task: $LAST_TASK"
        fi
        # Verificar auditoría skills
        if python3 "$SCRIPTS_DIR/zolo_auditar_skills.py" &>/dev/null; then
            log "   Auditoría: verde ✓"
        else
            log "   ⚠️ Auditoría: ROJA — auto-curación necesaria"
        fi
        LAST_SUPERVISOR=$NOW
    fi

    # 2. Curador de skills (cada 1h)
    if (( NOW - LAST_CURADOR >= INTERVAL_CURADOR )); then
        log "📦 Curador de skills ejecutando..."
        python3 "$SCRIPTS_DIR/zolo_curador_skills.py" --report &>>"$LOG_DIR/curator.log" || true
        LAST_CURADOR=$NOW
    fi

    # 3. Optimizador de descriptions (cada 4h)
    if (( NOW - LAST_OPTIMIZER >= INTERVAL_OPTIMIZER )); then
        log "⚡ Optimizador de descriptions ejecutando..."
        python3 "$SCRIPTS_DIR/zolo_optimizar_descripcion.py" --all --dry-run &>>"$LOG_DIR/optimizer.log" || true
        LAST_OPTIMIZER=$NOW
    fi

    # 4. Eval harness (cada 8h) — solo skills con baja confianza
    if (( NOW - LAST_EVAL >= INTERVAL_EVAL )); then
        log "🔬 Eval harness ejecutando..."
        # Evaluar primera skill con confidence < 0.7
        LOW_CONF_SKILL=$(python3 -c "
import json
with open('/home/z/my-project/download/agente-zolo/06_aprendizaje/SKILL_REGISTRY.json') as f:
    data = json.load(f)
for name, meta in data.get('skills', {}).items():
    if meta.get('confidence', 1.0) < 0.7 and meta.get('state') == 'active':
        print(name)
        break
" 2>/dev/null || echo "")
        if [[ -n "$LOW_CONF_SKILL" ]]; then
            log "   Evaluando skill con baja confianza: $LOW_CONF_SKILL"
            python3 "$SCRIPTS_DIR/zolo_evaluar_skill.py" "$LOW_CONF_SKILL" --iterations 1 &>>"$LOG_DIR/eval.log" || true
        else
            log "   Todas las skills tienen confidence ≥0.7 ✓"
        fi
        LAST_EVAL=$NOW
    fi

    # 5. Sueño-consolidación (cada 24h)
    if (( NOW - LAST_SUEÑO >= INTERVAL_SUEÑO )); then
        log "😴 Sueño-consolidación ejecutando..."
        # Leer worklog + ledger, detectar patrones
        LEARNING_COUNT=$(grep -c "^### " /home/z/my-project/download/agente-zolo/06_aprendizaje/LEARNINGS.md 2>/dev/null || echo "0")
        ERROR_COUNT=$(grep -c "^### " /home/z/my-project/download/agente-zolo/06_aprendizaje/ERRORS.md 2>/dev/null || echo "0")
        log "   Learnings: $LEARNING_COUNT | Errors: $ERROR_COUNT"
        # Verificar patrones repetidos
        REPEATED=$(grep -oP "LECCIÓN: .*" /home/z/my-project/download/agente-zolo/06_aprendizaje/LEARNINGS.md 2>/dev/null | sort | uniq -d | head -1 || echo "")
        if [[ -n "$REPEATED" ]]; then
            log "   ⚠️ Patrón repetido detectado: ${REPEATED:0:60}..."
            log "   → Promoción a regla/skill propuesta (gate G1 pendiente)"
        fi
        LAST_SUEÑO=$NOW
    fi

    # Actualizar estado
    echo "{\"started\":\"$(date -Iseconds)\",\"pid\":$$,\"last_supervisor\":$LAST_SUPERVISOR,\"last_curador\":$LAST_CURADOR,\"last_optimizer\":$LAST_OPTIMIZER,\"last_eval\":$LAST_EVAL,\"last_sueño\":$LAST_SUEÑO}" > "$STATE_FILE"

    # Esperar 60s antes del próximo check
    sleep 60
done
