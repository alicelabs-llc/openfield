#!/usr/bin/env bash
# ============================================
# 🤖 AUTO PR SENDER — Cronograma automático
# ============================================
# Ejecuta 2 PRs por día en GitHub + Codeberg + GitLab
# Diseñado para correr en background (cron) en la PC del usuario
#
# Instalación:
#   1. Configurar ~/.auto-pr-config.env (ver config.example.env)
#   2. Probar manualmente: ./auto_pr_sender.sh --dry-run
#   3. Instalar cron: ./setup_cron.sh
# ============================================

set -euo pipefail

# --- Configuración ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${HOME}/.auto-pr-config.env"
PATCHES_DIR="${SCRIPT_DIR}/patches"
LOG_DIR="${SCRIPT_DIR}/logs"
STATE_FILE="${SCRIPT_DIR}/.state"
TODAY=$(date +%Y-%m-%d)
NOW=$(date +"%Y-%m-%d %H:%M:%S")

# Cargar config
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "❌ Config file no encontrado: $CONFIG_FILE"
    echo "   Copia config.example.env a $CONFIG_FILE y edita los valores"
    exit 1
fi
source "$CONFIG_FILE"

# --- Flags ---
DRY_RUN=false
VERBOSE=false
PLATFORM="${1:-all}"  # all | github | codeberg | gitlab

for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=true ;;
        --verbose|-v) VERBOSE=true ;;
    esac
done

# --- Helpers ---
log() {
    local level=$1; shift
    local msg=$1
    local color=""
    case "$level" in
        INFO)  color="\033[0;36m" ;;
        OK)    color="\033[0;32m" ;;
        WARN)  color="\033[0;33m" ;;
        ERROR) color="\033[0;31m" ;;
    esac
    echo -e "${color}[$(date +%H:%M:%S)] $level:${color:0:0} $msg\033[0m" | tee -a "$LOG_DIR/${TODAY}.log"
}

# Verificar que las herramientas existen
require_tool() {
    if ! command -v "$1" &>/dev/null; then
        log ERROR "Falta instalar: $1"
        exit 1
    fi
}

require_tool git
require_tool curl
[[ "$PLATFORM" == "all" || "$PLATFORM" == "github" ]] && require_tool gh

# --- State management ---
# .state guarda qué patches ya se enviaron (un patch por línea)
touch "$STATE_FILE"

already_sent() {
    local patch_name=$1
    grep -qF "$patch_name" "$STATE_FILE" 2>/dev/null
}

mark_sent() {
    local patch_name=$1
    local pr_url=$2
    echo "$patch_name|$pr_url|$NOW" >> "$STATE_FILE"
}

# --- GitHub PR creation ---
send_github_pr() {
    local patch_file=$1
    local pr_desc_file=$2
    local repo_full=$3  # owner/repo
    local issue_number=$4
    local branch_name=$5

    log INFO "GitHub: enviando $patch_file a $repo_full (issue #$issue_number)"

    if $DRY_RUN; then
        log INFO "[DRY-RUN] No se enviará nada. Branch: $branch_name"
        return 0
    fi

    local work_dir="${SCRIPT_DIR}/work/${repo_full}"
    mkdir -p "$work_dir"
    cd "$work_dir"

    # Verificar si el repo ya está clonado
    if [[ ! -d "$repo_full" ]]; then
        log INFO "Clonando $repo_full..."
        if ! gh repo clone "$repo_full" "$repo_full" -- --depth 1 2>/dev/null; then
            log ERROR "No se pudo clonar $repo_full. ¿Estás logueado en gh?"
            return 1
        fi
    fi

    cd "$repo_full"
    git fetch origin
    git checkout main 2>/dev/null || git checkout master 2>/dev/null
    git pull --rebase

    # Crear branch
    git checkout -b "$branch_name" 2>/dev/null || {
        log WARN "Branch $branch_name ya existe. Saltando."
        return 1
    }

    # Aplicar patch
    if ! git am "$patch_file"; then
        log ERROR "git am falló para $patch_file. Resolviendo..."
        git am --abort
        git checkout main
        git branch -D "$branch_name"
        return 1
    fi

    # Push
    if ! git push -u origin "$branch_name" 2>/dev/null; then
        # Si no hay fork, crear uno automáticamente
        log INFO "Creando fork..."
        gh repo fork "$repo_full" --clone=false
        sleep 5
        if ! git push -u origin "$branch_name" 2>/dev/null; then
            log ERROR "Push falló. Revisa auth de GitHub."
            return 1
        fi
    fi

    # Crear PR
    local pr_body=""
    if [[ -f "$pr_desc_file" ]]; then
        pr_body=$(cat "$pr_desc_file")
    fi

    local pr_url
    pr_url=$(gh pr create \
        --repo "$repo_full" \
        --head "$branch_name" \
        --title "Fix #$issue_number" \
        --body "$pr_body" \
        2>/dev/null || echo "FAILED")

    if [[ "$pr_url" == "FAILED" ]]; then
        log ERROR "gh pr create falló"
        return 1
    fi

    log OK "✅ PR creado: $pr_url"
    mark_sent "$(basename "$patch_file")" "$pr_url"
    return 0
}

# --- Codeberg PR creation ---
send_codeberg_pr() {
    local patch_file=$1
    local repo_full=$2  # owner/repo
    local issue_number=$3
    local branch_name=$4

    log INFO "Codeberg: enviando $patch_file a $repo_full (issue #$issue_number)"

    if $DRY_RUN; then
        log INFO "[DRY-RUN] No se enviará nada."
        return 0
    fi

    local work_dir="${SCRIPT_DIR}/work/codeberg/${repo_full}"
    mkdir -p "$(dirname "$work_dir")"

    if [[ ! -d "$work_dir" ]]; then
        log INFO "Clonando $repo_full desde codeberg.org..."
        if ! git clone "https://codeberg.org/${repo_full}.git" "$work_dir" --depth 1 2>/dev/null; then
            log ERROR "Clone falló. Verifica CODEBERG_TOKEN en config."
            return 1
        fi
        cd "$work_dir"
        # Configurar remote con token para push
        git remote set-url origin "https://${CODEBERG_USER}:${CODEBERG_TOKEN}@codeberg.org/${repo_full}.git"
    fi

    cd "$work_dir"
    git fetch origin
    git checkout main 2>/dev/null || git checkout master 2>/dev/null
    git pull --rebase

    git checkout -b "$branch_name" 2>/dev/null || {
        log WARN "Branch ya existe. Saltando."
        return 1
    }

    if ! git am "$patch_file"; then
        log ERROR "git am falló para Codeberg $patch_file"
        git am --abort
        git checkout main
        git branch -D "$branch_name"
        return 1
    fi

    if ! git push -u origin "$branch_name"; then
        log ERROR "Push a Codeberg falló"
        return 1
    fi

    # Crear PR via API Codeberg (compatible con Gitea)
    local pr_payload
    pr_payload=$(cat <<EOF
{
    "title": "Fix #$issue_number",
    "head": "$branch_name",
    "base": "main"
}
EOF
)
    local pr_url
    pr_url=$(curl -sS -X POST \
        "https://codeberg.org/api/v1/repos/${repo_full}/pulls" \
        -H "Authorization: token ${CODEBERG_TOKEN}" \
        -H "Content-Type: application/json" \
        -d "$pr_payload" | jq -r .html_url 2>/dev/null || echo "FAILED")

    if [[ "$pr_url" == "FAILED" || -z "$pr_url" ]]; then
        log WARN "PR creation API falló pero branch está pusheada. Crea PR manualmente."
        pr_url="https://codeberg.org/${repo_full}/pulls"
    fi

    log OK "✅ Codeberg PR: $pr_url"
    mark_sent "$(basename "$patch_file")" "$pr_url"
    return 0
}

# --- Cronograma ---
# Define qué patches enviar en qué orden
declare -a GITHUB_QUEUE=(
    "harbour_57_fix_ci_rstest.patch:Ishannaik/harbour:57:fix/57-ci-rstest"
    "saythanks_168_bare_except.patch:BlitzKraft/saythanks.io:168:fix/168-bare-except"
    "icalendar_1921_strenum_get.patch:collective/icalendar:1921:fix/1921-strenum-get"
    "icalendar_1868_suppress_warnings.patch:collective/icalendar:1868:fix/1868-suppress-warnings"
    "vajra_15_eve_parsing_tests.patch:Ergane-Foundation/vajra:15:test/15-eve-parsing"
    "adbt_34_node24_ci.patch:Ergane-Foundation/adbt:34:ci/34-node24"
    "harbour_36_parse_hex_alpha.patch:Ishannaik/harbour:36:feature/36-parse-hex-alpha"
    "pyqtgraph_2373_all_position.patch:pyqtgraph/pyqtgraph:2373:style/2373-all-position"
    "kubearmor_2895_codecov_badge.patch:kubearmor/KubeArmor:2895:fix/2895-codecov-badge"
    "httpexpect_460_test_value_raw.patch:gavv/httpexpect:460:test/460-value-raw"
    "tenv_51_openssf_badge.patch:tofuutils/tenv:51:docs/51-openssf-badge"
    "tenv_302_lockfile_docs.patch:tofuutils/tenv:302:docs/302-lockfile"
    "loki_20673_sync_atomic.patch:grafana/loki:20673:refactor/20673-sync-atomic"
    "minikube_23526_go_version_file.patch:kubernetes/minikube:23526:ci/23526-go-version-file"
    "nushell_19003_mkdir_existing.patch:nushell/nushell:19003:fix/19003-mkdir-existing"
)

declare -a CODEBERG_QUEUE=(
    "siotls_48_indexerror.patch:drlazor8/siotls:48:fix/48-indexerror"
    "golda_53_remove_hugo_refs.patch:PersonalTechHelp/golda:53:refactor/53-remove-hugo-refs"
    "slidcord_47_reactions_history.patch:slidge/slidcord:47:fix/47-reactions-history"
)

# --- Ejecución ---
log INFO "=== Auto PR Sender — $NOW ==="
log INFO "Plataforma: $PLATFORM | Dry run: $DRY_RUN"

github_sent_today=0
codeberg_sent_today=0
MAX_PER_PLATFORM_PER_DAY=2

# Enviar GitHub
if [[ "$PLATFORM" == "all" || "$PLATFORM" == "github" ]]; then
    log INFO "Procesando cola GitHub..."
    for entry in "${GITHUB_QUEUE[@]}"; do
        [[ $github_sent_today -ge $MAX_PER_PLATFORM_PER_DAY ]] && break

        IFS=':' read -r patch_file repo_full issue_num branch <<< "$entry"
        full_patch="$PATCHES_DIR/$patch_file"

        if [[ ! -f "$full_patch" ]]; then
            log WARN "Patch no existe: $patch_file"
            continue
        fi

        if already_sent "$patch_file"; then
            $VERBOSE && log INFO "Ya enviado (skip): $patch_file"
            continue
        fi

        # PR description file (mismo nombre base con .md)
        pr_desc="${PATCHES_DIR}/pr_${patch_file%.patch}.md"
        [[ ! -f "$pr_desc" ]] && pr_desc=""

        if send_github_pr "$full_patch" "$pr_desc" "$repo_full" "$issue_num" "$branch"; then
            ((github_sent_today++))
            sleep 60  # 1 min entre PRs para no spamear
        fi
    done
    log OK "GitHub: $github_sent_today/$MAX_PER_PLATFORM_PER_DAY enviados hoy"
fi

# Enviar Codeberg
if [[ "$PLATFORM" == "all" || "$PLATFORM" == "codeberg" ]]; then
    log INFO "Procesando cola Codeberg..."
    for entry in "${CODEBERG_QUEUE[@]}"; do
        [[ $codeberg_sent_today -ge $MAX_PER_PLATFORM_PER_DAY ]] && break

        IFS=':' read -r patch_file repo_full issue_num branch <<< "$entry"
        full_patch="$PATCHES_DIR/$patch_file"

        if [[ ! -f "$full_patch" ]]; then
            log WARN "Patch no existe: $patch_file"
            continue
        fi

        if already_sent "$patch_file"; then
            $VERBOSE && log INFO "Ya enviado (skip): $patch_file"
            continue
        fi

        if send_codeberg_pr "$full_patch" "$repo_full" "$issue_num" "$branch"; then
            ((codeberg_sent_today++))
            sleep 60
        fi
    done
    log OK "Codeberg: $codeberg_sent_today/$MAX_PER_PLATFORM_PER_DAY enviados hoy"
fi

# GitLab pendiente — requiere MR workflow distinto
if [[ "$PLATFORM" == "all" || "$PLATFORM" == "gitlab" ]]; then
    log WARN "GitLab: pendiente de implementar (MR workflow distinto)"
fi

# Resumen final
log INFO "=== Resumen del día ==="
log INFO "GitHub: $github_sent_today PRs | Codeberg: $codeberg_sent_today PRs"
log INFO "Total enviados históricamente: $(wc -l < "$STATE_FILE")"
log INFO "Próxima corrida: mañana a la misma hora (si cron está activo)"

exit 0
