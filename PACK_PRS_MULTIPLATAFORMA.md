# 📦 PACK MAESTRO DE PRs — GitHub + GitLab + Codeberg

**Fecha de generación:** 2026-10-25
**Objetivo:** 2 PRs por día en cada plataforma (GitHub, GitLab, Codeberg) = 6 PRs/día
**Total de patches preparados:** 14 listos para enviar

---

## 🐙 GITHUB — 11 patches preparados

### Patches ya preparados (revisión anterior, 5 + 1 fix)
1. **collective/icalendar #1921** — StrEnum.get() classmethod → `icalendar_1921_strenum_get.patch`
2. **collective/icalendar #1868** — Suppress pytest warnings → `icalendar_1868_suppress_warnings.patch`
3. **Ergane-Foundation/vajra #15** — Tests eve.json parsing → `vajra_15_eve_parsing_tests.patch`
4. **Ergane-Foundation/adbt #34** — Bump GH Actions Node 24 → `adbt_34_node24_ci.patch`
5. **Ishannaik/harbour #36** — parse_hex 4/8-digit alpha → `harbour_36_parse_hex_alpha.patch`
6. **Ishannaik/harbour #57** — Fix CI rstest version ⚡ URGENTE → `harbour_57_fix_ci_rstest.patch`

### Patches NUEVOS (esta sesión, +5)
7. **BlitzKraft/saythanks.io #168** — Fix bare `except` statements → `saythanks_168_bare_except.patch`
   - Python, 1,315 stars, 4 comments
   - Reemplaza 2 bare except en `saythanks/storage.py` con `URLError` y `JSONDecodeError`

8. **tofuutils/tenv #51** — Add OpenSSF badges → `tenv_51_openssf_badge.patch`
   - Go, 1,457 stars, **0 comments** (zero competition)
   - Agrega badge OpenSSF Best Practices al README

9. **tofuutils/tenv #302** — Lockfile docs → `tenv_302_lockfile_docs.patch`
   - Go, 1,457 stars, **0 comments**
   - Documenta cómo tenv maneja lockfiles en runs paralelos

10. **pyqtgraph/pyqtgraph #2373** — Move `__all__` to top → `pyqtgraph_2373_all_position.patch`
    - Python, 4,432 stars, 3 comments
    - Mechanical refactor: mueve `__all__` al inicio del módulo (PEP 8)

11. **kubearmor/KubeArmor #2895** — Fix Codecov badge 0% → `kubearmor_2895_codecov_badge.patch`
    - Go, 2,631 stars, 3 comments
    - Fix de URL del badge Codecov que mostraba 0%

### Patches NUEVOS adicionales (más profundos, +3)
12. **gavv/httpexpect #460** — Add TestValue_Raw test → `httpexpect_460_test_value_raw.patch`
    - Go, 2,723 stars, **1 comment**
    - Table-driven test con 9 casos cubriendo nil/bool/int/float/string/object/array/nested

13. **grafana/loki #20673** — Replace go.uber.org/atomic with sync/atomic → `loki_20673_sync_atomic.patch`
    - Go, 29,054 stars, 7 comments
    - Mechanical refactor: standard library en Go 1.19+ ya tiene typed atomics

14. **kubernetes/minikube #23526** — Use go-version-file in CI → `minikube_23526_go_version_file.patch`
    - Go, 32,207 stars, 4 comments
    - Reemplaza versiones hardcoded de Go con `go-version-file: 'go.mod'`

15. **nushell/nushell #19003** — Error on existing directory in mkdir → `nushell_19003_mkdir_existing.patch`
    - Rust, 40,719 stars, 2 comments
    - Alinea comportamiento con POSIX `mkdir` + agrega flag `--verbose`

---

## 🦊 CODEBERG — 3 patches preparados

### Patches preparados
16. **drlazor8/siotls #48** — Fix IndexError in BadCertificate → `siotls_48_indexerror.patch`
    - **Python**, pure-Python TLS 1.3 library
    - Guard `alert_data[0]` con check de empty list

17. **PersonalTechHelp/golda #53** — Remove leftover Hugo references → `golda_53_remove_hugo_refs.patch`
    - **Go**, CLI tool
    - Renombra `hugoTemplate` → `docTemplate`, `hugoRender` → `render`

18. **slidge/slidcord #47** — Emoji reactions in channel history → `slidcord_47_reactions_history.patch`
    - **Python**, Discord→XMPP bridge
    - Agrega `with_reactions: True` al fetch de historial

### Otros candidatos de Codeberg pendientes de patch (3 más)
- **rimu/pyfedi #1931** — Preserve selected community when changing post type (Python)
- **SupermarketTapir/tapir #917** — Formatting of balance (Python)
- **core-lang/core #110** — Design function/method reference syntax (Rust)

---

## 🦊 GITLAB — Sin patches nuevos (problemas de acceso)

GitLab.com requiere auth para listar issues via WebFetch. Sin embargo, los candidatos verificados previamente siguen disponibles:

### Candidatos verificados anteriormente (sin patch aún)
- **gitlab-org/gitlab-foss** — No hay "good first issue" label abiertas (verificado vía WebFetch)
- **GNOME Pika** — Política anti-AI (rechazado anteriormente)
- **fdroid/fdroidclient !1786** — Tu MR sigue abierto, requiere AI declaration

### Estrategia GitLab
GitLab tiene barreras más altas que GitHub/Codeberg:
1. **DCO (Developer Certificate of Origin)** obligatorio en muchos proyectos
2. **CLA** en proyectos enterprise (gitlab-org/*)
3. **Políticas anti-AI** en algunos proyectos (GNOME, Forgejo old)
4. **Mejor enfoque**: contribuir a través de community forks (https://gitlab.com/gitlab-community)

### Pendiente GitLab (siguiente sesión)
Buscar en:
- invent.kde.org (KDE GitLab)
- gitlab.freedesktop.org
- gitlab.gnome.org (solo si no hay anti-AI policy)

---

## 📊 Plan de ejecución — 2 PRs/día × 3 plataformas = 6 PRs/día

### DÍA 1 (hoy) — GitHub + Codeberg
**GitHub (2 PRs):**
- ⚡ Push `harbour_57_fix_ci_rstest.patch` (URGENTE, desbloquea PR existente)
- Enviar `saythanks_168_bare_except.patch` (trivial Python)

**Codeberg (2 PRs):**
- Enviar `siotls_48_indexerror.patch` (Python TLS fix)
- Enviar `golda_53_remove_hugo_refs.patch` (Go cleanup)

### DÍA 2 — GitHub × 4
- Enviar `icalendar_1921_strenum_get.patch`
- Enviar `icalendar_1868_suppress_warnings.patch`
- Enviar `tenv_51_openssf_badge.patch`
- Enviar `tenv_302_lockfile_docs.patch`

### DÍA 3 — GitHub + Codeberg
**GitHub (2 PRs):**
- Enviar `vajra_15_eve_parsing_tests.patch`
- Enviar `adbt_34_node24_ci.patch`

**Codeberg (2 PRs):**
- Enviar `slidcord_47_reactions_history.patch`
- (Crear patch para `pyfedi #1931` o `tapir #917`)

### DÍA 4 — GitHub × 4
- Enviar `harbour_36_parse_hex_alpha.patch` (después de que #57 merge)
- Enviar `pyqtgraph_2373_all_position.patch`
- Enviar `kubearmor_2895_codecov_badge.patch`
- Enviar `httpexpect_460_test_value_raw.patch`

### DÍA 5 — GitHub + GitLab research
**GitHub (2 PRs):**
- Enviar `loki_20673_sync_atomic.patch`
- Enviar `minikube_23526_go_version_file.patch`

**GitLab (research + 1 PR):**
- Buscar issues en invent.kde.org
- Enviar 1 MR a GitLab (TBD)

### DÍA 6 — GitHub × 1 + Codeberg × 2 + GitLab × 1
- Enviar `nushell_19003_mkdir_existing.patch`
- Crear + enviar patch para `core-lang/core #110` (Rust, Codeberg)
- Crear + enviar patch para `SupermarketTapir/tapir #917` (Python, Codeberg)
- Enviar 1 MR a GitLab (TBD)

---

## 📈 Proyección total

| Métrica | Valor |
|---------|-------|
| PRs merged actuales | 3 |
| PRs open esperando merge | 4 |
| **Patches preparados** | **14** |
| Plataformas cubiertas | GitHub + Codeberg (GitLab pendiente research) |
| Proyección si 60% merge rate | 3 + 4 + (14 × 0.6) = **15 PRs merged** |
| Proyección si 80% merge rate | 3 + 4 + (14 × 0.8) = **18 PRs merged** |

---

## ⚠️ Reglas anti-spam (CRÍTICAS)

1. **No más de 2 PRs por día por plataforma** (límite anti-spam de GitHub/Codeberg)
2. **No tocar mismo repo 2 veces seguidas** sin esperar respuesta del maintainer
3. **Comment-claim el issue primero** antes de empezar (24h de espera)
4. **Incluir tests siempre** (aumenta merge rate)
5. **Polite nudge después de 7 días** (no spamear)
6. **Si CI falla, fix inmediato** (harbour #57 lesson)

---

## 🎯 Candidatos adicionales NO preparados (para próximas sesiones)

Estos 20 candidatos fueron identificados por el subagent pero no se preparó patch (queda para siguientes sesiones):

### Trivial (10)
- kubearmor/KubeArmor #2884 — Fix setup script Ubuntu 18.04
- tofuutils/tenv #419 — Add terramate to Nix/Choco/Brew
- kubernetes/minikube #23581 — Fix cri-dockerd updater
- gavv/httpexpect #455 — Add gzip decompress helpers
- tofuutils/tenv #158 — Portage package manager support
- tofuutils/tenv #56 — Add MSI installer support
- rust-lang/rust-clippy #17913 — False positive unnecessary_to_owned
- rimu/pyfedi #1931 — Preserve community on post type change
- SupermarketTapir/tapir #917 — Formatting of balance
- core-lang/core #110 — Design method reference syntax

### Medium (5)
- oven-sh/bun #17855 — Fish completions directory
- rust-lang/rustfmt #6539 — Off-by-one return type wrap
- home-assistant/core #185133 — Roborock map "NO MAP"
- BlitzKraft/saythanks.io #352 — Align Flask/Jinja best practices
- collective/icalendar #1802, #1840, #1784 (3 más del mismo repo)

---

## 📂 Archivos en `/home/z/my-project/download/`

```
Patches GitHub (11):
├── icalendar_1921_strenum_get.patch
├── icalendar_1868_suppress_warnings.patch
├── vajra_15_eve_parsing_tests.patch
├── adbt_34_node24_ci.patch
├── harbour_36_parse_hex_alpha.patch
├── harbour_57_fix_ci_rstest.patch    ⚡ URGENTE
├── saythanks_168_bare_except.patch
├── tenv_51_openssf_badge.patch
├── tenv_302_lockfile_docs.patch
├── pyqtgraph_2373_all_position.patch
├── kubearmor_2895_codecov_badge.patch
├── httpexpect_460_test_value_raw.patch
├── loki_20673_sync_atomic.patch
├── minikube_23526_go_version_file.patch
└── nushell_19003_mkdir_existing.patch

Patches Codeberg (3):
├── siotls_48_indexerror.patch
├── golda_53_remove_hugo_refs.patch
└── slidcord_47_reactions_history.patch

PR descriptions (6):
├── pr_icalendar_1921.md
├── pr_icalendar_1868.md
├── pr_vajra_15.md
├── pr_adbt_34.md
├── pr_harbour_36.md
└── pr_harbour_57_fix_ci.md
```

---

**Próxima sesión:** Crear patches para los 10 candidatos adicionales pendientes + buscar en GitLab/invent.kde.org.

© 2026 Eddy Flores. Pack de PRs multi-plataforma.
