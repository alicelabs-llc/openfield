#!/usr/bin/env bash
# ============================================
# 🚀 INSTALL — Setup one-shot del sistema
# ============================================
# Ejecuta este script UNA sola vez para:
# 1. Verificar dependencias (git, gh, jq)
# 2. Copiar config a ~/.auto-pr-config.env
# 3. Hacer ejecutables los scripts
# 4. Probar con --dry-run
# 5. Preguntar si instalar cron job
# ============================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🤖 Auto PR Sender — Instalador"
echo "=============================="
echo ""

# 1. Verificar dependencias
echo "1️⃣  Verificando dependencias..."
MISSING=()
for tool in git gh jq curl; do
    if ! command -v "$tool" &>/dev/null; then
        MISSING+=("$tool")
    fi
done

if [[ ${#MISSING[@]} -gt 0 ]]; then
    echo "❌ Faltan herramientas: ${MISSING[*]}"
    echo ""
    echo "Instala con:"
    echo "  Ubuntu/Debian: sudo apt install git jq curl"
    echo "  macOS: brew install git jq curl"
    echo "  GitHub CLI: ver https://cli.github.com/"
    exit 1
fi
echo "   ✓ git, gh, jq, curl disponibles"

# 2. Verificar login gh
echo ""
echo "2️⃣  Verificando login de GitHub CLI..."
if ! gh auth status &>/dev/null; then
    echo "   ⚠️  No estás logueado en gh. Ejecutando login..."
    gh auth login
else
    echo "   ✓ Logueado como: $(gh api user --jq .login)"
fi

# 3. Config
echo ""
echo "3️⃣  Configurando ~/.auto-pr-config.env..."
CONFIG_FILE="${HOME}/.auto-pr-config.env"
if [[ ! -f "$CONFIG_FILE" ]]; then
    cp scripts/config.example.env "$CONFIG_FILE"
    chmod 600 "$CONFIG_FILE"
    echo "   ✓ Creado: $CONFIG_FILE"
    echo ""
    echo "   ⚠️  EDITA este archivo con tus tokens reales:"
    echo "   nano $CONFIG_FILE"
    echo ""
    echo "   Presiona ENTER cuando termines de editar..."
    read -r
else
    echo "   ✓ Ya existe: $CONFIG_FILE"
fi

# 4. Hacer scripts ejecutables
echo ""
echo "4️⃣  Haciendo scripts ejecutables..."
chmod +x scripts/*.sh
echo "   ✓ scripts/auto_pr_sender.sh"
echo "   ✓ scripts/setup_cron.sh"

# 5. Dry-run test
echo ""
echo "5️⃣  Ejecutando prueba en modo --dry-run..."
bash scripts/auto_pr_sender.sh --dry-run 2>&1 | head -20

# 6. Cron job
echo ""
echo "6️⃣  Configurar cron job automático?"
read -p "   ¿Instalar cron para correr todos los días? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    bash scripts/setup_cron.sh
else
    echo "   Skip. Puedes correr el sender manualmente cuando quieras:"
    echo "   $SCRIPT_DIR/scripts/auto_pr_sender.sh"
fi

echo ""
echo "✅ ¡Listo!"
echo ""
echo "📋 Próximos pasos:"
echo "   - Revisa el cronograma: cat PACK_PRS_MULTIPLATAFORMA.md"
echo "   - Verifica estado: cat $SCRIPT_DIR/.state"
echo "   - Logs: ls $SCRIPT_DIR/logs/"
echo ""
echo "🚀 Para enviar PRs AHORA mismo (sin esperar al cron):"
echo "   bash $SCRIPT_DIR/scripts/auto_pr_sender.sh --verbose"
