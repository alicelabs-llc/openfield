# 📦 ZOLO v6.0 — Paquete del agente (identidad ZOLO · AUTÓMATA)

**ZOLO** es el agente operativo de AliceLabs LLC / MarketNow — nombre puesto por el founder (Task 121, 24-oct-2026: "revisa todo lo que tiene que ver con el agente, recrealo. se llama zolo").

Genealogía: reconstrucción del agente original (chat `c6439ca3` / `glm-5.3`, 1222 mensajes, 25,644 tool calls, Tasks 1→114) **más 8 rondas de mejora**: v2.1 (auditoría de fricciones) · v3.0 (estado del arte 2025-2026, Tasks 117-a/b/c) · v3.1 (iniciativa agent-first — caso Taiko, Task 118) · v3.2 (memoria con cadena de custodia — alethech, Task 119) · v3.3 (máquina de ventas, Task 120) · v4.0 (identidad ZOLO, Task 121) · v5.0 (estado del arte de AUTONOMÍA: reglas 26-29 + §17, Task 122) · **v6.0 AUTÓMATA (12 reels del founder descifrados + 8 repos clonados: reglas 30-33 + §18 ciclo de auto-mejora + `06_aprendizaje/` + 7 skills nuevas + maquinaria de autoinstalación, Task 123)**.

## Arquitectura v3.0: 2 niveles (progressive disclosure)

- **Núcleo siempre en contexto**: `ZOLO_V6.md` — 33 reglas de iniciativa, 14 reglas de oro, protocolo worklog, contexto canónico, registro de plataformas, guardarraíles, formato de respuesta, árbol de decisión, checklist de cierre, memoria alethech (protocolo completo), pendientes, índice de skills, mejora continua, vigilancia, **máquina de estado del trabajo (§17, v5.0)** y **ciclo de auto-mejora continua en 4 cadencias (§18, v6.0)**.
- **25 skills on-demand** (`02_skills/*/SKILL.md`, formato agentskills.io): el cuerpo se carga SOLO cuando la tarea aplica — el índice de 25 líneas vive en el núcleo (§12). Registro de fuentes para autoinstalación: `02_skills/biblioteca-skills/FUENTES.md`.
- **Ledger de aprendizaje** (`06_aprendizaje/`): LEARNINGS · ERRORS · FEATURE_REQUESTS · FUENTES_RADAR — captura en caliente, promoción semanal, radar de información continua (reglas 31+33).

## Contenido

| Archivo | Qué es |
|---|---|
| `ZOLO_V6.md` | **El núcleo del agente** (v6.0 AUTÓMATA, con §17 máquina de estado + §18 ciclo de auto-mejora) |
| `05_ESTADO_DEL_ARTE_V5.md` | Investigación v5.0: repos de autonomía + patrones + mejoras M1-M12 (Task 122) |
| `06_ESTADO_DEL_ARTE_V6.md` | **Investigación v6.0**: los 12 reels descifrados + 8 repos clonados + mejoras M13-M21 (Task 123) |
| `02_skills/` (25 SKILL.md) | runbook-incidentes · escalera-outreach · plan-y-ejecucion · best-of-n-decisiones · subagentes-contrato · seguridad-fuentes · tareas-largas · mantenimiento-mensual · mcp-compliance-2026 · iniciativa-agent-first · memoria-alethech · maquina-ventas · patrones-flujo · bucle-autonomo · memoria-jerarquica · biblioteca-skills · reflexion-post-mortem · equipo-virtual (v5.0) · **flota-produccion · ledger-autoaprendizaje · autoinstalador-skills · depuracion-sistematica · diseno-web-premium · cumplimiento-legal-vibecoding · canales-distribucion (v6.0)** + `biblioteca-skills/FUENTES.md` (registro de repos) |
| `06_aprendizaje/` | **Ledger de autoaprendizaje (v6.0)**: LEARNINGS · ERRORS · FEATURE_REQUESTS (F-001..F-008) · FUENTES_RADAR |
| `iniciativa-agent-first/` | Caso de estudio Taiko verificado + plan de réplica de 14 movimientos (Task 118) |
| `BOOTSTRAP_PROMPT.md` | Primer mensaje listo para pegar en un chat nuevo de chat.z.ai |
| `worklog_seed.md` | Worklog semilla con el estado recuperado — copiar a `/home/z/my-project/worklog.md` |
| `AGENTS.md` | Versión portable en el **estándar abierto agents.md** (Codex, Cursor, Gemini CLI, Copilot, Cline, Devin) — raíz del repo |
| `AGENT.md` | Puntero deprecado a AGENTS.md (compatibilidad Cline antiguo) |
| `EVALS.md` | **52 escenarios de verificación** (regresión + capability, graders deterministas primero) |
| `CHANGELOG.md` | Historial versionado (v2.0 → … → v5.0 → v6.0) |
| `archive/` | Backups por regla 22 (v2.1 + `ZOLO_V4.md` + `ZOLO_V5.md`) |
| `README.md` | Este archivo |
| `scripts/` (en la raíz del entorno) | **Maquinaria v6.0**: `zolo_instalar_skill.py` (autoinstalador) · `zolo_auditar_skills.py` (auditor 25 skills) · `zolo_mejorar_skills_v6.py` (lote graders) |

## 3 vías de despliegue

### A) Ya está desplegado en ESTE entorno (vía rápida)
`/home/z/my-project/worklog.md` está sembrado y el paquete vive en `/home/z/my-project/download/agente-zolo/`. **Este chat ya opera como ZOLO v6.0.**

### B) Chat nuevo en chat.z.ai
1. Nuevo chat → **GLM-5.3** → **Thinking ON** → **Reasoning effort: Máximo**. Sin MCP externos.
2. Copia `worklog_seed.md` → `/home/z/my-project/worklog.md` y sube la carpeta completa del paquete.
3. Pega el bloque de código de `BOOTSTRAP_PROMPT.md` como primer mensaje.

### C) Cline / Cursor / VS Code / Codex (dentro del repo)
1. Coloca `AGENTS.md` en la **raíz** del repo (los agentes del estándar lo leen automáticamente).
2. Coloca `ZOLO_V6.md` + `02_skills/` + `06_aprendizaje/` + `worklog.md` en el workspace.
3. *(Esto cierra la deuda del caso Cline del chat original — ahora con el nombre canónico del estándar.)*

## Qué añadió v6.0 (AUTÓMATA — Task 123)

| Mejora | Fuente |
|---|---|
| Regla 30 FLOTA DE PRODUCCIÓN (despacho paralelo en un mensaje, revisión por artefacto, escéptico con veto, rulings-not-stalls, 4 paradas, ledger en archivo) + skill `flota-produccion` | `obra/superpowers` ~304k★ (subagent-driven-development + dispatching-parallel-agents) + mesa multi-bot del founder (reel 2) |
| Regla 31 LEDGER EN CALIENTE + `06_aprendizaje/` (LEARNINGS/ERRORS/FEATURE_REQUESTS) + skill `ledger-autoaprendizaje` | `pskoett/self-improving-agent` (patrón .learnings con captura/reuso/promoción) |
| Regla 32 AUTOINSTALACIÓN DE SKILLS + skill `autoinstalador-skills` + `biblioteca-skills/FUENTES.md` + script `zolo_instalar_skill.py` | Fábrica de Voyager (ronda v5) hecha real + skills CLI + repos de los reels |
| Regla 33 PRODUCCIÓN CONTINUA + AUTOEDUCACIÓN + `FUENTES_RADAR.md` + §18 ciclo de 4 cadencias | Mandato del founder (24/7) + radar del ecosistema |
| Skill `depuracion-sistematica` (Ley de Hierro: no fix sin causa raíz, 4 fases) | `obra/superpowers` systematic-debugging |
| Skill `diseno-web-premium` (sistema de diseño + UX 1-10 + auditoría anti-slop a 3 anchos) | Reel 1 → `Leonxlnx/taste-skill` + `nextlevelbuilder/ui-ux-pro-max-skill` + impeccable |
| Skill `cumplimiento-legal-vibecoding` (checklist COPPA/fonts/recording/unsubscribe/renewals/DMCA) | Reel 12 (riesgos legales del vibe coding) |
| Skill `canales-distribucion` (r/SideProject → HN → PH Tue-Thu → Indie Hackers → Uneed) | Reel 8 (5 primeros sitios) + reel 3 (plugins como canal) |
| 14 skills v3.x con sección Grader a medida (auditor verde 25/25) | Regla 32 §2 aplicada al propio paquete |

## Checklist de credenciales (pedir al usuario lo que falte — nunca asumir)

| Credencial | Archivo esperado | Estado al cierre del período recuperado |
|---|---|---|
| GitHub PAT (eddyflores100-lang) | `scripts/.pat_eddy` | El de Task 98 operativo; uno posterior daba 401 |
| Cloudflare (Pages+DNS+R2) | `scripts/.cf_creds` | Well-known vencía 9-oct — re-verificar |
| Gmail app password | `scripts/.gmail_eddy` | **MUERTO 3-oct** — pedir nuevo |
| Vercel token | `scripts/.vercel_token` | Limitado, respaldo |
| npm | `npm whoami` | Vivo al cierre |

## Qué añadió v3.2 (protocolo alethech completo — Task 119, repo propio revisado)

| Mejora | Fuente |
|---|---|
| Regla 24 MEMORIA CON CADENA DE CUSTODIA + skill memoria-alethech | `eddyflores100-lang/alethech` v0.9.1 (README + listing mcpservers.org + Awesome-Agent-Memory) |
| §11 protocolo completo: boot fail-closed, gate de novedad, formato de commit con `supersede`, evidence, checkpoints, rotación mensual, DR trimestral ≤60s | Superficie CLI de 9 comandos del propio protocolo + patterns del ecosistema (Cortex gate, Verified Memory Vault linter, MemTether bi-temporal) |
| **Hostinger CONGELADO** (decisión usuario) — §13 re-priorizado: urgentes = Gmail app password → Glama re-claim | Orden textual del usuario 21-oct-2026 |
| EVALS E28-E30 (fail-closed, commit antes de "hecho", rollback por checkpoint) | Suite ampliada a 30 |

Detalle completo en `CHANGELOG.md` (v3.2).

## Qué añadió v3.1 (caso de estudio Taiko — Task 118, fuentes primarias verificadas)

| Mejora | Fuente del patrón |
|---|---|
| Regla 23 SUPERFICIE AGENT-FIRST + skill iniciativa-agent-first | `taikoxyz/taiko-ai` (repo que ES un agente: 4 skills, 4 subagentes, 4 MCP servers/41 tools, CLI `--json` schema fijo, plugin marketplace, audit.md; contribuidores dantaik + claude) |
| Repo réplica **`download/uta-ai/`** listo para push a `alicelabs-llc/uta-ai` | Misma estructura de taiko-ai adaptada a UTA/Sentinel/catálogo (cifras vivas 21-oct: 71,198 skills, agent card v4.0.0) |
| `/SKILL.md` del sitio (hoy 404 → artefacto listo) + `llms-v2.txt` generada + GAPS.md con drift detectado (68,388 vs 71,198) | `taikoxyz/taiko-docs` ("agent-first documentation", 4 formatos machine-readable + browser tests) |
| **drift-check.yml** — cifra viva vs citada en CI, diario 08:00 Guayaquil | Mejora propia sobre el patrón Taiko + regla de oro "números vivos" del worklog |
| audit.md de auto-auditoría de PRs (bugs/reglas/token-efficiency) | `taiko-ai/audit.md` del PR #12 verificado |

Detalle completo en `CHANGELOG.md` (v3.1).

## Qué añadió v3.0 (fuentes verificadas en Tasks 117-a/b/c)

| Mejora | Fuente del patrón |
|---|---|
| Arquitectura 2 niveles + 9 skills on-demand | Anthropic Agent Skills (estándar abierto agentskills.io) + Cursor reglas/skills |
| Regla 18: PLAN.md persistido + reiniciar-desde-el-plan + grind loop acotado | Cursor "agent best practices" (ene-2026) + Anthropic harnesses |
| Regla 19: DATO ≠ INSTRUCCIÓN (spotlighting, cuarentena, anti tool-poisoning) | Anthropic prompt-injection-defenses + CaMeL + Invariant Labs |
| Regla 20: Best-of-N para decisiones irreversibles | Cursor 2.0 (worktrees) + Anthropic voting |
| Regla 21: Evals 2 niveles + grader determinista primero + "eval al 0% = eval roto" | Anthropic "Demystifying evals" (ene-2026) |
| Regla 22: Presupuesto de atención + edición por deltas con backup | Anthropic context engineering + ACE (ICLR 2026) + lección reset #3 |
| §7.7 Mandato explícito para acciones de riesgo | AP2 / agentic commerce (mandatos firmados) |
| AGENTS.md estándar AAIF | agents.md (donado por OpenAI a Linux Foundation, dic-2025) |
| Pendientes MCP 2026: Worker dual-era + server/discover + RFC 9728 + server-card SEP-1649 + server.json Registry oficial | modelcontextprotocol.io spec 2026-07-28 |
| Corrección Glama: glama.json en RAÍZ del repo (no /.well-known/) | Docs Glama verificadas 21-oct-2026 |
| §16 Vigilancia de mercado trimestral | Codifica esta sesión como rutina permanente |
| skills.sh (Audits Trust Hub/Socket/Snyk) como objetivo de sindicación | Vercel skills.sh, 1.39M installs |

## Qué añadió v4.0 (Task 121 — "se llama zolo")

| Mejora | Detalle |
|---|---|
| **Identidad ZOLO** | Nombre propio en núcleo §0, BOOTSTRAP, mapa, README, AGENTS.md, EVALS E34; firma pública "ZOLO (AliceLabs)"; renombre mecánico verificado (0 referencias viejas) |
| **Estado verificado en vivo (24-oct-2026)** | health v4.2.0 (features agent-hire, m2m-checkout, agent-rep, agent-referral…) · 71,198 skills · `/SKILL.md` 200 (RESUELTO, era 404) · `/api/mcp` 200 · `/llms.txt` 200 · `/agents`/`/atc` 200 · glama.json 200 · npm 1.4.0 |
| **Pendientes §13 re-sellados** | items 3/8/17 actualizados: lo desplegado queda marcado; queda inspección de schema de `/api/mcp` antes de claims |
| **Memoria §11** | Referencia de UI: `Alethech Notebook` (design concept React/Vite) — conceptual, no bloquea CLI |

Detalle completo en `CHANGELOG.md` (v4.0).

## Qué añadió v5.0 (Task 122 — "los repos más estrella de autonomía y diseño de agentes")

| Mejora | Fuente del patrón |
|---|---|
| Reglas 26-29: WORKFLOW>AGENTE · PRESUPUESTO DE AUTONOMÍA · BIBLIOTECA DE SKILLS VIVA · REFLEXIÓN TRAS FALLO | Anthropic "Building Effective Agents" + AutoGPT/LangGraph (budget+checkpoints) + Voyager (skill factory) + Reflexion (post-mortems) |
| §17 MÁQUINA DE ESTADO: checkpoints reanudables de 5 campos + 3 gates HITL + event log por acción | LangGraph (estado tipado + interrupts) + OpenHands (event stream) + DeepAgents (filesystem como memoria) |
| 6 skills nuevas → 18: patrones-flujo · bucle-autonomo · memoria-jerarquica · biblioteca-skills · reflexion-post-mortem · equipo-virtual | Los 5 patrones de Anthropic · AutoGPT+BabyAGI (bucle+cola) · MemGPT/Letta (jerarquía de memoria) · Voyager+SWE-agent (fábrica+ACI) · Reflexion · CrewAI+MetaGPT (roles+SOPs) |
| Lista de mejoras M1-M12 trazada repo-a-repo + decisión documentada de qué NO adoptar | `05_ESTADO_DEL_ARTE_V5.md` (investigación completa Task 122) |
| Evals E35-E42 (patrón declarado · run presupuestado · stop en T2 · paginación · fábrica · post-mortem · equipo por artefactos · contexto autosuficiente) | Suite ampliada a 42 |

Detalle completo en `CHANGELOG.md` (v5.0).

## Fuentes del kit original

`chat_meta.json` · `reasoning_samples.md` (20 muestras) · `file_snapshots/worklog*` (Tasks 18, 89-93, 94-99) · `skills_inventory.json` (76) · `AGENT_RECREATION_MANUAL.md` · `AGENT_RECONSTRUCTION_README.md` · memoria alethech (Task 114).
