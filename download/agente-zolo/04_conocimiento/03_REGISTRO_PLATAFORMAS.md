# 03 — REGISTRO DE PLATAFORMAS: dónde subir todo lo que tenemos

> Playbook probado: alethech ya está en mcpservers.org + Official MCP Registry + Awesome-Agent-Memory (verificado Task 119). Este archivo replica ese éxito para MarketNow/UTA y añade canales nuevos. Formato: Destino · Qué se sube · Cómo · Estado · Bloqueo. `⚠️ VERIFICAR-EN-BOOT` = el flujo exacto exige sesión/formulario; se confirma al ejecutar, nunca se asume.

## TIER 0 — Donde los AGENTES nos descubren (prioridad máxima: "atraer agentes")

| # | Destino | Qué se sube | Cómo | Estado | Bloqueo |
|---|---|---|---|---|---|
| 1 | **Official MCP Registry** (registry.modelcontextprotocol.io) | Server MCP remoto `marketnow.site/api/mcp` (9 tools) | Publicación server-driven; alethech ya está como `io.github.eddyflores100-lang/alethech` — replicar patrón para `io.github.alicelabs-llc/marketnow`. PulseMCP dice que es EL camino canónico | ⏳ Pendiente | Verificar credencial/flow de publish ⚠️ |
| 2 | **Glama** (glama.ai/mcp/servers) | Server MCP + directorio de agentes | Re-claim con `glama.json` en raíz del dominio (pendiente #2 §13 v3.2) | ⏳ Pendiente | Deploy CF del glama.json (TÚ) |
| 3 | **mcpservers.org** | Listing de marketnow (alethech ya pasó el review) | Mismo flujo usado con alethech | ⏳ Pendiente | Formulario ⚠️ |
| 4 | **mcp.so** | Server MCP (+ sección Skills y Agents) | Submit en mcp.so (tienen Directory/Submission; opción Advertise para luego) | ⏳ Pendiente | Formulario ⚠️ |
| 5 | **skills.sh / agentskills.io** (estándar abierto de skills) | Los 4 skills de `uta-ai` (`uta`, `sentinel-audit`, `marketnow-catalog`, `uta-conformance`) | Repo público + `npx skills add alicelabs-llc/uta-ai` funciona; el índice recolecta repos con SKILL.md | ⏳ Pendiente | **PAT para push del repo (TÚ)** |
| 6 | **Anthropic Connectors Directory** | Conector MCP remoto de marketnow | Formulario oficial de submission (comunidad confirma el flujo: reddit r/ClaudeAI "Submitted a connector to Anthropic's MCP Directory") | ⏳ Pendiente | Formulario ⚠️ |
| 7 | **PulseMCP** | Server MCP | **Submissions pausadas desde sep-2026** — al reabrir ingesta automática desde Official MCP Registry | 👁️ Pasivo | Solo Tier 0.1 |
| 8 | **Agent Card discoverability** | `/api/agent.json` + `/.well-known/agent.json` + MAP `agent-protocol.json` | Ya vivos (200 hoy) — enlazarlos desde llms.txt y listings | ✅ Vivo | — |

## TIER 1 — Donde los HUMANOS con presupuesto nos descubren

| # | Destino | Qué se sube | Cómo | Estado | Bloqueo |
|---|---|---|---|---|---|
| 9 | **npm** | `@marketnow/uta-conformance` 1.4.0 + `marketnow-mcp` | Ya publicados | ✅ Vivo | — |
| 10 | **PyPI** | `alethech` | Ya publicado | ✅ Vivo | — |
| 11 | **GitHub Sponsors** (org `alicelabs-llc`) | Monetización del OSS (UTA/alethech) | Activar Sponsors en la cuenta operativa; enlace desde READMEs | ⏳ Pendiente | Cuenta org ⚠️ |
| 12 | **Product Hunt** | Launch de MarketNow/UTA ("SSL for AI Agents") | Post como maker; preparar assets (tagline, galería, primer comentario del founder) | ⏳ Cola | Assets + cuenta TÚ |
| 13 | **Hacker News (Show HN)** | "Show HN: MarketNow – Agent Trust Cards, SSL for AI agents (71k skills indexados)" | Texto plano, sin marketing, responder comentarios 24h | ⏳ Cola | Cuenta TÚ (karma ayuda) |
| 14 | **Uneed / Peerlist Launchpad** | Alternativas de lanzamiento dev-friendly sin el gate de PH | Submit en unebest.com / peerlist.io | ⏳ Cola | Cuenta ⚠️ |
| 15 | **LinkedIn (página AliceLabs) + X** | Prueba social semanal: 1 artefacto vivo por semana (badge ATC, drift-check, conformance) | Post corto + demo GIF; comentarios en hilos MCP/agents | ⏳ Cola | Cuentas TÚ |
| 16 | **Directorios llms.txt** (llmstxt.site, directorios de sites agent-first) | marketnow.site con llms.txt curado | Submit tras desplegar `llms-v2.txt` (mata el drift) | ⏳ Bloqueado | Deploy CF (TÚ) |

## TIER 2 — Donde conseguimos TRABAJO (casa → caja)

| # | Destino | Qué ofrecemos | Nota |
|---|---|---|---|
| 17 | **Upwork** | Perfil "MCP Server / AI Agent developer" vendiendo S1-S5 | Categoría existe y está caliente (upwork.com/hire/mcp-server-developers). Requiere cuenta humana (TÚ); el agente prepara perfil, propuestas y respuestas |
| 18 | **Fiverr / Freelancer.com** | Gig productizados: "MCP server in 7 days $1,500", "Agent-first docs $2,500", "MCP conformance audit $400" | Mismo material de 02; gig = oferta S2/S3 textual |
| 19 | **Opire** (opire.dev) | Cobrar bounties de issues públicos ($20+, fee 4%, payout Stripe al merge) | El agente rastrea `label:bounty` y propone claims; humano mergea pago |
| 20 | **Algora** (algora.io) | Bounties/challenges OSS (ej. Turso $1,000/bug) + visibilidad para contratos | Perfil GitHub = CV |
| 21 | **GitHub Issues con `label:bounty`** | Búsqueda directa: `label:bounty state:open sort:created-desc` | Sin intermediarios ni fee |

## Orden de ejecución recomendado (máximo $ por unidad de esfuerzo)

1. **Hoy (agente, sin bloqueos):** campañas NEXUS COLD S3→S1 a autores de MCP (04), respuestas Upwork preparadas (17), rastreo de bounties (19-21).
2. **Con PAT (TÚ, 10 min):** push `uta-ai` → skills instalables → Tier 0.5 y oferta S1 con demo pública.
3. **Con CF (TÚ, 30 min):** deploy `llms-v2.txt` + `/SKILL.md` + `glama.json` → mata drift, desbloquea Tier 0.2 y 0.6.
4. **Esta semana (agente+TÚ):** Official MCP Registry → mcpservers.org → mcp.so → Anthropic Directory (orden de tráfico y fricción).
5. **Lanzamientos (cuando las 2-4 estén hechas):** PH/HN/Uneed con cifras vivas verificadas.
