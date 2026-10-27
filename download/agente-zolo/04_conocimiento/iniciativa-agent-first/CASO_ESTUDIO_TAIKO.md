# Caso de estudio — la iniciativa agent-first de Taiko (verificado 21-oct-2026)

> Origen del task: "REVISA EL REPO DE TAIKO, VE LA INICIATIVA MOSTRADA POR EL AGENTE, ESTA EN GITHUB TODO EL CASO DE ESTUDIO, VE SI PUEDES REPLICAR ESE TIPO DE INICIATIVA".
> Método: WebSearch + WebFetch sobre fuentes primarias (github.com/taikoxyz), verificación de archivos crudos (raw.githubusercontent.com) y árbol git vía API. Todas las citas abajo fueron leídas directamente de los repos.

## Qué es Taiko (contexto mínimo)

Taiko (`taikoxyz`) es un based rollup de Ethereum (Type-1 ZK-EVM). Fundación con 128 repos públicos. Lo relevante aquí NO es el L2 sino **cómo hicieron agent-first su proyecto entero**.

## La iniciativa 1 — `taikoxyz/taiko-ai`: el repo que ES un agente

**"An AI agent/skill for developing on Taiko"** — 91 commits, v1.5.0 (28-feb-2026), TypeScript 72% + Python 17% + Solidity 10%. Commits por **dantaik (Daniel Wang, fundador de Taiko) y "claude" (el agente como contribuidor con su propia identidad)**.

Componentes verificados:

1. **4 skills** formato agentskills.io (`skills/*/SKILL.md`, frontmatter name+description con triggers "Use when..."):
   - `taiko` — desarrollo de contratos (main): quick decision table, protocol knowledge con referencias, deploy/verify/cast, troubleshooting tabulado, "Related Skills" cruzados.
   - `taiko-node` — operar nodos. · `taiko-shadow` — transferencias privadas ZK. · `taiko-x402` — pagos HTTP con USDC.
2. **4 definiciones de subagentes** (`agents/*.md`) con frontmatter extenso: name, description con triggers, **tools, mcpServers, color, memory, skills** — y cuerpo con "Critical Rules" numeradas, workflow bash, tabla "MCP Tools" (cuándo→tool→server), security checklist, troubleshooting.
3. **4 servidores MCP** (41 tools en total): taiko-data (16), taiko-explorer (10, incluye análisis Slither), taiko-bridge (8, con write tools tras private keys en env), taiko-node-monitor (7, Python). Cliente API compartido (Taikoscan V2 / Blockscout V2 / Relayer) + CLI `taiko`.
4. **CLI con salida `--json` de schema fijo para agentes**: `{ schema_version, command, status, network, data, errors, warnings, metrics }` — la lección: toda superficie CLI devuelve estructuras parseables, nunca texto humano-only.
5. **Distribución triple**: `npx skills add taikoxyz/taiko-ai` (estándar abierto) · `/plugin marketplace add taikoxyz/taiko-ai` + `/plugin install taiko@taikoxyz` (Claude Code) · config MCP stdio local. `.claude-plugin/marketplace.json` con 4 plugins categorizados (development/infrastructure/privacy/payments) + `plugin.json` con keywords.
6. **`audit.md` — el agente audita sus propios PRs**: el archivo audita el PR #12 (que añadió los MCP servers) en 3 categorías: **Bugs** (6, con severidad — p.ej. `retry_message` enviaba txs a la cadena contraria por mapping invertido), **Violaciones CLAUDE.md/RULES.md** (2 — placeholder sin implementar, claim de marketing no verificable), **Token efficiency** (4 — ABIs completos vs firmas truncadas, source sin límite, sin paginación, filtrado client-side). La auditoría es pública EN el repo.
7. `how_to_deploy.md`, GitHub Actions, releases versionadas.

**Por qué es iniciativa y no solo tooling**: el fundador dedicó el repo a que CUALQUIER agente (Claude, Cursor, Cline...) opere Taiko de punta a punta — deploy, bridge, nodos, pagos — y lo mantuvo con el agente como co-autor, publicando hasta la auditoría de sus propios errores.

## La iniciativa 2 — `taikoxyz/taiko-docs`: documentación agent-first

README verificado: *"Agent-first documentation for Taiko... Every page is designed for both human developers and AI agents, with machine-readable formats generated automatically."*

- `/llms.txt` — índice de páginas con descripciones · `/llms-full.txt` — docs completas en texto plano · `/<path>.md` — cualquier página como Markdown crudo · `/SKILL.md` — **referencia de agente con instrucciones de cómo interactuar con la cadena**.
- **Browser tests** (e2e, construyen el sitio y lo sirven solos) que cubren la metadata SEO que debe sobrevivir la navegación client-side — la lección: la metadata para agentes se TESTEA, no se espera.

## Patrones replicables destilados (7)

1. **El producto tiene superficie de agente de primera clase** (skills + agents + MCP + plugin), no un README que "menciona agentes".
2. **El agente es contribuidor con identidad propia** en el repo del producto.
3. **Auto-auditoría pública de PRs** en 3 categorías fijas (bugs / reglas / token-efficiency).
4. **CLI/API con schema de salida fijo** (`schema_version...`) — parseable por máquinas siempre.
5. **Docs con 4 formatos de máquina** (llms.txt / llms-full.txt / .md por página / SKILL.md) y **tests de metadata**.
6. **Distribución por los 3 canales del estándar** (npx skills add · plugin marketplace · MCP config).
7. **Skills con triggers explícitos y cross-references** ("For X use skill Y instead") — routing entre skills.

## Aplicación inmediata a AliceLabs/MarketNow

Verificado el 21-oct-2026 contra marketnow.site vivo: `/llms.txt` ✅ (200) y `/llms-full.txt` ✅ (200) ya existen; **`/SKILL.md` ❌ 404 y `/<path>.md` ❌ 404**; 18+ superficies nuevas (`/agents`, `/acp`, `/agent-passport`, `/atc`, `/handshake`...) sin indexar en llms.txt; drift de cifras (llms.txt 68,388 vs `/api/skills` vivo **71,198**). El 90% de la superficie de datos ya es de primera clase — faltan exactamente las piezas que taiko-docs llama SKILL.md y .md-routes, y el repo tipo taiko-ai completo. Réplica: `PLAN_REPLICACION.md` + repo `download/uta-ai/`.
