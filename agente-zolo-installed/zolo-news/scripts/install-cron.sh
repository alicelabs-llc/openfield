#!/usr/bin/env bash
# ============================================================
# ZOLO NEWS — Instalador de despertar programado (crontab)
# Uso: bash scripts/install-cron.sh [HH:MM]
# Ejemplo: bash scripts/install-cron.sh 06:30
# ============================================================
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WAKE="${1:-$(node -e "console.log(require('$DIR/config.json').wakeTime || '06:30')" 2>/dev/null || echo '06:30')}"
HH="${WAKE%%:*}"
MM="${WAKE##*:}"
TZ_NAME="$(node -e "console.log(require('$DIR/config.json').city.timezone)" 2>/dev/null || echo 'America/Guayaquil')"
NODE_BIN="$(command -v node)"

LINE="$MM $HH * * * cd $DIR && $NODE_BIN agent.js run >> $DIR/logs/cron.log 2>&1"

echo "ZOLO NEWS — instalando despertar a las $WAKE ($TZ_NAME)"
mkdir -p "$DIR/logs"

# Instalar/actualizar la entrada idempotentemente (marcador # ZOLO-NEWS)
(crontab -l 2>/dev/null | grep -v "ZOLO-NEWS" || true; echo "$LINE  # ZOLO-NEWS") | crontab -

echo "OK — entrada crontab instalada:"
crontab -l | grep "ZOLO-NEWS"
echo ""
echo "Nota: si tu sistema no respeta TZ por entrada, exporta CRON_TZ=$TZ_NAME al inicio del crontab:"
echo "  CRON_TZ=$TZ_NAME"
