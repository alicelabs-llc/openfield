# 06 — OPORTUNIDADES INMEDIATAS (trabajo YA, verificadas 21-oct-2026)

> Ordenadas por velocidad de caja. Fuente de cada afirmación citada. El agente revisa esta página al inicio de cada BOOT y actualiza hallazgos nuevos abajo.

## Canal A — Demanda declarada con presupuesto (la más caliente)

1. **Upwork — categoría "MCP Server Developers"**: existe como categoría de contratación dedicada (upwork.com/hire/mcp-server-developers) y Upwork mismo lanzó su propio MCP server para que clientes/freelancers operen desde herramientas de IA (anuncio LinkedIn Andrew Rabinovich, CTO Upwork). Mercado tarificado: $20–60/hr marketplaces abiertos, $60–150+ firmas (divogue.net/hire-mcp-engineers). **Acción:** cuenta TÚ + perfil prepado por agente (título: "MCP & AI Agent infrastructure — I run a live agent marketplace"; portafolio: marketnow.site + uta-ai + alethech). El agente redacta propuestas por posting.
2. **Fiverr / Freelancer.com**: categorías "Remote MCP Server Development" y "Model Context Protocol Experts" activas (fiverr.com/hire/remote-mcp-server-development; freelancer.com/hire/model-context-protocol). **Acción:** 3 gigs desde 02 (S1/S2/S3) con precios fijos.
3. **Postings de empleo de agentes** (señal de presupuesto): empresas contratan "AI agent engineers" — ofrecer el mismo entregable como servicio fijo cuesta 10x menos que un hire.

## Canal B — Bounties OSS (caja en días-semanas, además construye reputación)

4. **Búsqueda directa GitHub**: `label:bounty state:open sort:created-desc` — sin fee, sin intermediario (guía dev.to "How to Find and Win Open Source Bounties in 2026").
5. **Opire** (opire.dev): bounties desde $20 sobre cualquier issue público; fee 4% + Stripe lo paga el creador; payout al merge (oss.fund/opire, verificado mar-2026). **Acción:** el agente filtra issues de repos MCP/agentes TypeScript/Python donde tenemos ventaja demostrable.
6. **Algora** (algora.io): hoy orientado a recruiting, pero mantiene challenges con premios fuertes — caso activo citado: Turso "$1,000 por bug de corrupción de datos" (algora.io/challenges/turso). **Acción:** monitorear challenges Rust/SQLite/DST solo si el margen justifica; prioridad baja.
7. **Programas específicos**: AsyncAPI rounds trimestrales, repos de tooling AI con bounties para plugins/integraciones (dev.to, misma guía).

## Canal C — Vender a los que YA construyen agentes (nuestro ICP natural)

8. **Autores de MCP servers**: miles de servers listados públicamente (PulseMCP 21,660+ indexados aunque pausado; mcp.so con secciones Servers/Skills/Agents) → lista de leads S1 ya enumerable. Oferta de entrada: conformance+ATC $400 (04 §4.4).
9. **Agentes operadores**: Agent Cards públicos + directorios → S4 free ATC para primeros 100 (loop de viralidad con `agent-referral` ya vivo en nuestra API).

## Canal D — Infraestructura de monetización nativa (medio plazo, alinear con roadmap propio)

10. **x402** (x402.org, LF Projects): producción real — 75.41M transacciones, $24.24M volumen, 22K sellers en 30 días. Cobrar por llamada HTTP (402) encaja con `m2m-checkout` (ya en nuestra API v4.2.0) cuando abra gate C1.
11. **Cloudflare Monetization Gateway** (blog.cloudflare.com/monetization-gateway): cobrar por cualquier recurso — APIs, datos, **llamadas MCP** — con settlement sub-segundo. Nosotros ya corremos en Cloudflare Workers → ventaja estructural. **Acción:** seguir el GA y ser día-1 (pitch: "MarketNow cobra llamadas MCP con x402").

## Hallazgos nuevos (el agente añade con fecha; borrar lo muerto)

- (Task 120, 21-oct-2026) Seed inicial: los canales A/B arriba verificados hoy. NEXUS COLD sin configuración conocida = bloqueo #1 del Canal C.
