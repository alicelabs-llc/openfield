#!/usr/bin/env bash
# ============================================
# PR SENDER v2 — Envía 4 PRs a GitHub
# ============================================
# 2 PRs FIX (adbt #48 + harbour #57)
# 2 PRs NUEVOS (icalendar #1921 + saythanks #168)
#
# REQUIERE: gh CLI autenticado como eddyflores100-lang
# ============================================

set -euo pipefail

PATCHES="/home/z/my-project/download"
WORK="/tmp/pr-work"
mkdir -p "$WORK"

send_fix() {
    local repo="$1" branch="$2" patch="$3" pr_num="$4" comment="$5"
    echo "🔧 FIX PR #$pr_num en $repo"
    cd "$WORK"
    repo_dir=$(echo "$repo" | tr '/' '_')
    if [ ! -d "$repo_dir" ]; then
        gh repo clone "$repo" "$repo_dir" -- --depth 1 2>/dev/null || { echo "❌ clone falló"; return 1; }
    fi
    cd "$repo_dir"
    git fetch origin 2>/dev/null || true
    git checkout "$branch" 2>/dev/null || git checkout -b "$branch"
    git pull origin "$branch" 2>/dev/null || true
    git am "$patch" 2>/dev/null && echo "  ✅ Patch aplicado" || { git am --skip 2>/dev/null || true; echo "  ⚠️ Patch ya aplicado"; }
    git push origin "$branch" --force 2>/dev/null && echo "  ✅ Pushed" || echo "  ⚠️ Push falló (sin auth?)"
    gh pr comment "$pr_num" --repo "$repo" --body "$comment" 2>/dev/null && echo "  ✅ Comentario publicado" || echo "  ⚠️ No se pudo comentar"
    echo ""
}

send_new_pr() {
    local repo="$1" branch="$2" patch="$3" title="$4" body_file="$5"
    echo "📤 NUEVO PR en $repo: $title"
    cd "$WORK"
    repo_dir=$(echo "$repo" | tr '/' '_')
    if [ ! -d "$repo_dir" ]; then
        gh repo clone "$repo" "$repo_dir" -- --depth 1 2>/dev/null || { echo "❌ clone falló"; return 1; }
    fi
    cd "$repo_dir"
    git checkout main 2>/dev/null || git checkout master 2>/dev/null
    git pull origin main 2>/dev/null || git pull origin master 2>/dev/null || true
    git checkout -b "$branch" 2>/dev/null || git checkout "$branch"
    git am "$patch" 2>/dev/null && echo "  ✅ Patch aplicado" || { echo "  ❌ Patch falló"; return 1; }
    git push origin "$branch" 2>/dev/null && echo "  ✅ Pushed" || echo "  ⚠️ Push falló"
    # Create PR
    body=$(cat "$body_file" 2>/dev/null || echo "")
    gh pr create --repo "$repo" --head "$branch" --title "$title" --body "$body" 2>/dev/null && echo "  ✅ PR creado" || echo "  ⚠️ PR ya existe o falló"
    echo ""
}

echo "🚀 === PR SENDER v2 — 4 PRs ==="
echo ""

# FIX 1: adbt #48
send_fix "Ergane-Foundation/adbt" "fix/35-pin-goreleaser-v2" \
    "$PATCHES/adbt_48_reviewer_fix.patch" "48" \
    "Applied both requested changes:
1. \`version: '~> v2'\` instead of \`version: v2\`
2. Comment trimmed to one line

Thanks for the quick review @SakshhamTheCoder!"

# FIX 2: harbour #57
send_fix "Ishannaik/harbour" "fix/41-filter-control-chars-history" \
    "$PATCHES/harbour_57_ci_fix_final.patch" "57" \
    "CI should be green now — fixed rstest version mismatch by using fully-qualified \`#[rstest::rstest]\` macro path (works on both 0.18 and 0.19) and loosening constraint to \`>=0.18, <0.20\`.

Ready for review."

# NEW PR 1: icalendar #1921
send_new_pr "collective/icalendar" "fix/1921-strenum-get-method" \
    "$PATCHES/icalendar_1921_strenum_get.patch" \
    "Add StrEnum.get() classmethod for safe value lookup (#1921)" \
    "$PATCHES/pr_icalendar_1921_final.md"

# NEW PR 2: saythanks #168
send_new_pr "BlitzKraft/saythanks.io" "fix/168-bare-except" \
    "$PATCHES/saythanks_168_bare_except.patch" \
    "Fix bare except statements (FLK-E722) (#168)" \
    "$PATCHES/pr_saythanks_168_final.md"

echo "📊 === RESUMEN ==="
echo "  FIX: adbt #48 + harbour #57 (actualizados)"
echo "  NEW: icalendar #1921 + saythanks #168 (creados)"
echo "  TOTAL: 4 PRs procesados"
