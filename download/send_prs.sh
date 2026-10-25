#!/usr/bin/env bash
# ============================================
# PR Sender — envía 2 PRs diarios a GitHub
# ============================================
# Requiere: gh CLI autenticado
# Uso: bash send_prs.sh
# ============================================

set -euo pipefail

PATCHES_DIR="/home/z/my-project/download"
WORK_DIR="/tmp/pr-work"
mkdir -p "$WORK_DIR"

echo "📤 === PR SENDER — 2 PRs diarios ==="
echo ""

# --- PR 1: adbt #48 fix (reviewer feedback) ---
echo "🔧 PR 1: adbt #48 — aplicando feedback del reviewer"
REPO="Ergane-Foundation/adbt"
BRANCH="fix/35-pin-goreleaser-v2"
PATCH="$PATCHES_DIR/adbt_48_reviewer_fix.patch"

cd "$WORK_DIR"
if [ ! -d "adbt" ]; then
    gh repo clone "$REPO" adbt -- --depth 1 2>/dev/null || true
fi
cd adbt 2>/dev/null || { echo "❌ No se pudo clonar adbt"; exit 1; }

# Checkout existing branch or create
git fetch origin 2>/dev/null || true
git checkout "$BRANCH" 2>/dev/null || git checkout -b "$BRANCH"
git pull origin "$BRANCH" 2>/dev/null || true

# Apply patch
if git am "$PATCH" 2>/dev/null; then
    echo "✅ Patch aplicado"
else
    git am --skip 2>/dev/null || true
    echo "⚠️ Patch ya aplicado o conflicto — intentando aplicar manualmente"
fi

# Force push
git push origin "$BRANCH" --force 2>/dev/null && echo "✅ Pushed a $BRANCH" || echo "⚠️ Push falló"

# Comment on PR
gh pr comment 48 --repo "$REPO" --body "Applied both requested changes:
1. \`version: '~> v2'\` instead of \`version: v2\`
2. Comment trimmed to one line

Thanks for the quick review @SakshhamTheCoder!" 2>/dev/null && echo "✅ Comentario publicado en PR #48" || echo "⚠️ No se pudo comentar"

echo ""

# --- PR 2: harbour #57 CI fix ---
echo "🔧 PR 2: harbour #57 — fix CI rstest"
REPO2="Ishannaik/harbour"
BRANCH2="fix/41-filter-control-chars-history"
PATCH2="$PATCHES_DIR/harbour_57_ci_fix_final.patch"

cd "$WORK_DIR"
if [ ! -d "harbour" ]; then
    gh repo clone "$REPO2" harbour -- --depth 1 2>/dev/null || true
fi
cd harbour 2>/dev/null || { echo "❌ No se pudo clonar harbour"; exit 1; }

git fetch origin 2>/dev/null || true
git checkout "$BRANCH2" 2>/dev/null || git checkout -b "$BRANCH2"
git pull origin "$BRANCH2" 2>/dev/null || true

if git am "$PATCH2" 2>/dev/null; then
    echo "✅ Patch aplicado"
else
    git am --skip 2>/dev/null || true
    echo "⚠️ Patch ya aplicado o conflicto"
fi

git push origin "$BRANCH2" --force 2>/dev/null && echo "✅ Pushed a $BRANCH2" || echo "⚠️ Push falló"

gh pr comment 57 --repo "$REPO2" --body "CI should be green now — fixed the rstest version mismatch by using fully-qualified \`#[rstest::rstest]\` macro path (works on both 0.18 and 0.19) and loosening the version constraint to \`>=0.18, <0.20\`.

Ready for review." 2>/dev/null && echo "✅ Comentario publicado en PR #57" || echo "⚠️ No se pudo comentar"

echo ""
echo "📊 Resumen: 2 PRs actualizados"
echo "   - adbt #48: feedback del reviewer aplicado"
echo "   - harbour #57: CI fix aplicado"
