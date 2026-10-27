#!/usr/bin/env bash
# ============================================
# ⚙️  SETUP CRON — Instala el job automático
# ============================================
# Esto configura un cron job que ejecuta
# auto_pr_sender.sh todos los días a las 9:00 AM
# (cuando la PC esté encendida)
# ============================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SENDER="${SCRIPT_DIR}/auto_pr_sender.sh"

if [[ ! -x "$SENDER" ]]; then
    chmod +x "$SENDER"
fi

# Verificar que el sender existe
if [[ ! -f "$SENDER" ]]; then
    echo "❌ No encuentro auto_pr_sender.sh en $SCRIPT_DIR"
    exit 1
fi

# Verificar config
if [[ ! -f "${HOME}/.auto-pr-config.env" ]]; then
    echo "❌ Falta config: ~/.auto-pr-config.env"
    echo "   Copia scripts/config.example.env a ~/.auto-pr-config.env y edita"
    exit 1
fi

# Comprobar si ya existe el cron job
CRON_MARKER="# auto-pr-sender"
EXISTING=$(crontab -l 2>/dev/null | grep -F "$CRON_MARKER" || true)

if [[ -n "$EXISTING" ]]; then
    echo "✅ Cron job ya está instalado:"
    echo "$EXISTING"
    echo ""
    read -p "¿Reinstalar? (y/N) " -n 1 -r
    echo
    [[ ! $REPLY =~ ^[Yy]$ ]] && exit 0
    # Eliminar entrada existente
    (crontab -l 2>/dev/null | grep -v -F "$CRON_MARKER"; true) | crontab -
fi

# Preguntar hora
read -p "¿A qué hora enviar PRs cada día? [9] " HOUR
HOUR=${HOUR:-9}

# Crear entrada cron para SENDER
CRON_ENTRY="0 ${HOUR} * * * ${SENDER} >> ${SCRIPT_DIR}/logs/cron.log 2>&1 ${CRON_MARKER}"

# Crear entrada cron para MONITOR (1 hora después del sender, lee estado real)
MONITOR="${SCRIPT_DIR}/pr_monitor.py"
[[ ! -x "$MONITOR" ]] && chmod +x "$MONITOR"
MONITOR_HOUR=$((HOUR + 1))
MONITOR_ENTRY="0 ${MONITOR_HOUR} * * * python3 ${MONITOR} >> ${SCRIPT_DIR}/logs/monitor.log 2>&1 ${CRON_MARKER}-monitor"

# Agregar a crontab
(crontab -l 2>/dev/null | grep -v -F "$CRON_MARKER"; echo "$CRON_ENTRY"; echo "$MONITOR_ENTRY") | crontab -

echo ""
echo "✅ Cron jobs instalados:"
echo "   📤 Sender:  $CRON_ENTRY"
echo "   📊 Monitor: $MONITOR_ENTRY"
echo ""
echo "📋 Para verificar:    crontab -l | grep auto-pr"
echo "🗑️  Para desinstalar: crontab -e (borra la línea con # auto-pr-sender)"
echo ""
echo "📝 Logs en:           ${SCRIPT_DIR}/logs/"
echo "📊 Estado en:         ${SCRIPT_DIR}/.state"
echo ""
echo "🔍 Probar manualmente:"
echo "   $SENDER --dry-run   (simula, no envía nada)"
echo "   $SENDER --verbose   (envía con output detallado)"
echo "   $SENDER github      (solo GitHub)"
echo "   $SENDER codeberg    (solo Codeberg)"
