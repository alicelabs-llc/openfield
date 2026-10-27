# 🤖 AUTO PR SYSTEM — Sistema automático de PRs

> **Envía 2 PRs por día automáticamente** en GitHub + Codeberg + GitLab
> mientras tu PC está prendida. Cero intervención manual.

---

## ⚡ Estado actual (2026-10-25)

### ❌ Lo que NO se ha hecho hoy
- **No se han enviado PRs todavía** — solo están los patches preparados
- Mi sandbox no es tu PC: necesitas ejecutar el install en tu máquina

### ✅ Lo que SÍ está listo
- **26 patches preparados** (15 GitHub + 3 Codeberg + 8 previos)
- **6 PR descriptions** (markdown listos para el body del PR)
- **Sistema completo de automatización** creado:
  - `auto_pr_sender.sh` — envía 2 PRs/día por plataforma
  - `pr_monitor.py` — revisa estado y genera reporte diario
  - `setup_cron.sh` — instala cron jobs
  - `install.sh` — instalación one-shot

---

## 🚀 Cómo instalar (3 minutos en tu PC)

### Requisitos previos
- Linux o macOS (Windows usa WSL2)
- `git`, `gh` (GitHub CLI), `jq`, `curl`, `python3`
- Cuenta GitHub logueada en `gh`

### Paso 1: Descargar el sistema
```bash
# Baja el ZIP auto_pr_system/ a tu PC y descomprime
cd ~/auto_pr_system
```

### Paso 2: Instalar
```bash
bash install.sh
```
Esto:
1. Verifica que tengas git, gh, jq, curl
2. Te hace login en GitHub CLI si no lo estás
3. Crea `~/.auto-pr-config.env` con template
4. Abre el config para que pegues tus tokens
5. Prueba con `--dry-run`
6. Pregunta si quieres instalar el cron job

### Paso 3: Configurar tokens
Edita `~/.auto-pr-config.env`:
```bash
GITHUB_TOKEN=ghp_tu_token_de_github
CODEBERG_TOKEN=tu_token_de_codeberg
MAX_PER_PLATFORM_PER_DAY=2
```

### Paso 4: Probar manualmente (opcional)
```bash
bash scripts/auto_pr_sender.sh --dry-run --verbose
# Simula todo sin enviar nada
```

### Paso 5: Activar cron
```bash
bash scripts/setup_cron.sh
# Te pregunta a qué hora correr (default 9 AM)
```

---

## 📅 Cronograma automático (2 PRs/día × 3 plataformas)

### Día 1 (hoy si activas ya)
**GitHub:**
1. `harbour_57_fix_ci_rstest.patch` ⚡ (desbloquea PR existente)
2. `saythanks_168_bare_except.patch` (trivial Python)

**Codeberg:**
3. `siotls_48_indexerror.patch` (Python TLS fix)
4. `golda_53_remove_hugo_refs.patch` (Go cleanup)

### Día 2
**GitHub:**
5. `icalendar_1921_strenum_get.patch`
6. `icalendar_1868_suppress_warnings.patch`

**Codeberg:**
7. `slidcord_47_reactions_history.patch`

### Día 3
8. `vajra_15_eve_parsing_tests.patch`
9. `adbt_34_node24_ci.patch`

### Día 4
10. `harbour_36_parse_hex_alpha.patch`
11. `pyqtgraph_2373_all_position.patch`

### Día 5
12. `kubearmor_2895_codecov_badge.patch`
13. `httpexpect_460_test_value_raw.patch`

### Día 6
14. `tenv_51_openssf_badge.patch` (0 competencia!)
15. `tenv_302_lockfile_docs.patch` (0 competencia!)

### Día 7
16. `loki_20673_sync_atomic.patch`
17. `minikube_23526_go_version_file.patch`

### Día 8
18. `nushell_19003_mkdir_existing.patch`

**Total: 18 PRs en 8 días** → si 60% merge rate = **11 PRs merged** para portfolio

---

## 📊 Cómo funciona el cron

```
9:00 AM  →  auto_pr_sender.sh
            - Lee .state (qué ya se envió)
            - Selecciona próximos 2 patches de GitHub
            - Selecciona próximos 2 patches de Codeberg
            - Para cada uno:
              git clone → crear branch → git am → push → gh pr create
            - Actualiza .state
            - Log en logs/YYYY-MM-DD.log

10:00 AM →  pr_monitor.py
            - Lee .state
            - Consulta estado real de cada PR via API
            - Genera logs/daily_report_YYYY-MM-DD.md
            - Identifica PRs que necesitan nudge (>7 días sin actividad)
```

---

## 🛠️ Comandos útiles

### Ejecutar manualmente (sin esperar al cron)
```bash
bash scripts/auto_pr_sender.sh --verbose
```

### Solo GitHub hoy
```bash
bash scripts/auto_pr_sender.sh github --verbose
```

### Solo Codeberg
```bash
bash scripts/auto_pr_sender.sh codeberg --verbose
```

### Ver estado de todos los PRs enviados
```bash
python3 scripts/pr_monitor.py
```

### Ver logs del día
```bash
cat logs/$(date +%Y-%m-%d).log
```

### Ver cronograma planificado
```bash
cat PACK_PRS_MULTIPLATAFORMA.md
```

### Pausar el cron (temporal)
```bash
crontab -l | sed 's|^\(.*auto-pr-sender\)|#\1|' | crontab -
```

### Desinstalar cron completamente
```bash
crontab -l | grep -v "auto-pr-sender" | crontab -
```

---

## ⚠️ Reglas anti-ban (CRÍTICAS)

1. **Máximo 2 PRs por día por plataforma** (hardcoded en el script)
2. **60 segundos entre PRs** (anti-spam)
3. **No tocar mismo repo 2 veces seguidas** (validado por script)
4. **Si git am falla, aborta automáticamente** (no deja branch rota)
5. **Si maintainer marca como spam, pausa el sistema**

---

## 📂 Estructura del sistema

```
auto_pr_system/
├── README.md                          ← Este archivo
├── install.sh                          ← Setup one-shot
├── patches/                           ← 26 patches + 6 PR descriptions
│   ├── icalendar_1921_strenum_get.patch
│   ├── icalendar_1868_suppress_warnings.patch
│   ├── vajra_15_eve_parsing_tests.patch
│   ├── adbt_34_node24_ci.patch
│   ├── harbour_36_parse_hex_alpha.patch
│   ├── harbour_57_fix_ci_rstest.patch ⚡
│   ├── saythanks_168_bare_except.patch
│   ├── tenv_51_openssf_badge.patch
│   ├── tenv_302_lockfile_docs.patch
│   ├── pyqtgraph_2373_all_position.patch
│   ├── kubearmor_2895_codecov_badge.patch
│   ├── httpexpect_460_test_value_raw.patch
│   ├── loki_20673_sync_atomic.patch
│   ├── minikube_23526_go_version_file.patch
│   ├── nushell_19003_mkdir_existing.patch
│   ├── siotls_48_indexerror.patch       (Codeberg)
│   ├── golda_53_remove_hugo_refs.patch  (Codeberg)
│   ├── slidcord_47_reactions_history.patch (Codeberg)
│   ├── pr_icalendar_1921.md
│   ├── pr_icalendar_1868.md
│   ├── pr_vajra_15.md
│   ├── pr_adbt_34.md
│   ├── pr_harbour_36.md
│   └── pr_harbour_57_fix_ci.md
├── scripts/
│   ├── auto_pr_sender.sh              ← Envía 2 PRs/día
│   ├── pr_monitor.py                  ← Revisa estado de PRs
│   ├── setup_cron.sh                  ← Instala cron jobs
│   └── config.example.env             ← Template de config
├── logs/                              ← Logs diarios
│   ├── 2026-10-25.log
│   └── daily_report_2026-10-25.md
├── work/                              ← Clones temporales de repos
│   └── Ishannaik/harbour/...
└── .state                             ← Track de qué se envió
```

---

## 🔒 Seguridad

- **Tokens en `~/.auto-pr-config.env`** con permisos `600` (solo tu usuario lee)
- **NUNCA subas este archivo a git**
- El `.gitignore` del sistema excluye `.state`, `logs/`, `work/`, `*.env`
- Tokens NO se loggean (están en variables de entorno)

---

## ❓ Troubleshooting

### "gh: command not found"
Instala GitHub CLI:
```bash
# macOS
brew install gh
# Ubuntu/Debian
sudo apt install gh
# Otras: https://cli.github.com/
```

### "gh auth status: not logged in"
```bash
gh auth login
# Elige: GitHub.com → HTTPS → Yes → Login with a web browser
```

### "git am failed"
El patch no aplica limpiamente (el repo cambió desde que lo generé).
Soluciones:
1. Re-clonar el repo
2. Aplicar el patch manualmente: `git apply --3way patch.patch`
3. Reportarlo y te genero un nuevo patch

### "Push rejected (permission denied)"
No tienes fork del repo. El script intenta crear fork automáticamente con `gh repo fork`. Si falla, créalo manualmente:
```bash
gh repo fork owner/repo --clone=false
```

### Cron no corre
Verifica:
```bash
# 1. Cron service activo
systemctl status cron  # Linux
brew services list | grep cron  # macOS (cron via launchd)

# 2. Permisos de scripts
chmod +x scripts/*.sh

# 3. Rutas absolutas en crontab
crontab -l
# Debe mostrar rutas absolutas (/home/user/auto_pr_system/scripts/...)
```

---

## 📈 Proyección

Con 18 patches preparados y 60% merge rate:

| Semana | PRs merged acumulados |
|--------|----------------------|
| 1 | 5-7 |
| 2 | 9-12 |
| 3 | 12-15 |
| 4 | 14-18 |

**Meta realista: 12-15 PRs merged para fin de noviembre 2026.**

Portfolio respetable para Outreachy/DoraHacks/GSoC 2027.

---

## 🆘 Soporte

Si algo se rompe:
1. Revisa `logs/YYYY-MM-DD.log`
2. Revisa `logs/daily_report_YYYY-MM-DD.md`
3. Ejecuta `python3 scripts/pr_monitor.py` para ver estado real
4. Si un PR falla, márcalo como sent en `.state` para saltarlo y seguir con los demás

---

© 2026 Eddy Flores. Sistema automático de contribuciones OSS.
