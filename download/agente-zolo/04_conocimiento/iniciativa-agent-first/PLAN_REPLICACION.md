# Plan de réplica — "iniciativa Taiko" para AliceLabs/MarketNow/UTA

Cada fila mapea el movimiento verificado de Taiko (CASO_ESTUDIO_TAIKO.md) a su equivalente nuestro, con estado al 21-oct-2026 (America/Guayaquil). Formato de respuesta §8 aplicado: YO = hecho por el agente aquí; TÚ/PRÓXIMO BOOT = requiere cuenta o credencial.

| # | Movimiento Taiko (verificado) | Equivalente AliceLabs | Estado |
|---|---|---|---|
| 1 | Repo `taiko-ai` con 4 skills agentskills.io | **`uta-ai`** con 4 skills: `uta` · `sentinel-audit` · `marketnow-catalog` · `uta-conformance` | ✅ YO — `download/uta-ai/skills/` (frontmatter validado por script, 4/4 OK) |
| 2 | 4 subagentes `agents/*.md` (frontmatter tools/mcpServers/skills) | 2 subagentes: `uta-developer` · `sentinel-auditor` | ✅ YO — `download/uta-ai/agents/` |
| 3 | `.claude-plugin/` marketplace (4 plugins) + plugin.json | `alicelabs-llc` marketplace con 4 plugins (security/discovery/development) | ✅ YO — JSON validado |
| 4 | 4 MCP servers (41 tools) + cliente API + CLI `taiko --json` schema fijo | SPEC.md de 2 servers (`uta-local` 8 tools, `catalog-cache` 3 tools) + **scaffold v0.1** `catalog-mcp` (build pendiente — sin npm en este entorno) | ⚠️ YO (spec+scaffold) → completar en próximo BOOT |
| 5 | `audit.md` — auto-auditoría de PRs (bugs/reglas/token-efficiency) | `audit.md` con plantilla + primer registro aplicado al PR de creación | ✅ YO |
| 6 | Distribución triple: `npx skills add` · `/plugin marketplace add` · MCP config | Idéntica, con `alicelabs-llc/uta-ai` | ✅ YO (instrucciones en README) — el push del repo necesita PAT (TÚ) |
| 7 | CI + releases | `ci.yml` (JSON+frontmatter+secretos+scaffold) + **`drift-check.yml`** (cifra viva vs citada, diario 08:00 Guayaquil) — mejora propia sobre el patrón | ✅ YO |
| 8 | `/llms.txt` | Ya existe (200) → **v2 generada** con superficies nuevas + cifras vivas fechadas | ✅ YO propuesta (`llms-v2.txt`) → deploy TÚ |
| 9 | `/llms-full.txt` | Ya existe (200) | ✅ no requiere acción |
| 10 | `/SKILL.md` del sitio | **404 hoy** → archivo completo escrito (endpoints, 9 tools MCP, pipeline, conducta) | ✅ YO contenido → deploy a la raíz del sitio (TÚ/CF) |
| 11 | `/<path>.md` por página | 404 hoy (`/uta.md`) | ⏳ PRÓXIMO BOOT con credenciales CF (Worker/Pages function) |
| 12 | Browser tests de metadata SEO | Sin evidencia en nuestro repo del sitio | ⏳ PRÓXIMO BOOT (Playwright e2e en `alicelabs-llc/marketnow`) |
| 13 | Agente como contribuidor (dantaik + claude) | Commits del agente con co-author en `uta-ai` | ⏳ necesita PAT vivo (pedir al usuario) |
| 14 | Drift de cifras detectado (llms.txt 68,388 vs vivo 71,198) | Reportado en GAPS.md; drift-check lo automatiza | ✅ YO (detección) → corrección con deploy |

## Fases de ejecución

- **Fase 0 (hecha hoy, sin credenciales)**: repo réplica completo + artefactos del sitio + caso de estudio + regla 23 en la definición del agente.
- **Fase 1 (próximo BOOT con PAT GitHub)**: push `alicelabs-llc/uta-ai` · co-author del agente · release v1.0.0 · activar workflows.
- **Fase 2 (con credenciales CF)**: desplegar `/SKILL.md` + `llms.txt` v2 · implementar rutas `.md` · actualizar `estado_sitio.json`.
- **Fase 3 (con npm + acceso registry)**: completar `catalog-mcp` build + tests · quitar `continue-on-error` del CI · entrada en audit.md.
- **Fase 4 (distribución)**: someter los 4 skills a skills.sh · `npx skills add alicelabs-llc/uta-ai` verificado end-to-end · anuncio con la metodología (outreach anti-ban §7: 1 link máximo, disclosure).

## Métrica de éxito de la réplica

Un agente externo (Claude/Cursor/Cline) sin contexto nuestro puede: (a) instalar la superficie con 1 comando, (b) verificar una credencial ATC con `marketnow_verify_trust`, (c) citar el total del catálogo con fecha, (d) leer `/SKILL.md` del sitio y operar sin preguntarnos nada. Ese es el estándar taiko — y nuestra barrera de salida.
