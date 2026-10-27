# CONOCIMIENTO — Evidencia de mercado (21-oct-2026, fuentes con URL)

> Base factual para pitches, precios y decisiones de canal. Cada dato cita fuente primaria verificada hoy. Actualizar en cada BOOT que encuentre dato nuevo (append con fecha; borrar lo muerto).

## 1. Demanda de servicios MCP/agentes (caliente y tarifada)

- **Upwork tiene categoría dedicada** "Hire MCP Server Developers" — `https://www.upwork.com/hire/mcp-server-developers` (browsable, oct-2026).
- **Upwork lanzó su propio MCP server** para que clientes y freelancers operen el marketplace desde herramientas de IA (anuncio del CTO Andrew Rabinovich, LinkedIn) — señal de que las plataformas themselves se vuelven agent-first.
- **Rates de mercado 2026**: $20–60/hr en marketplaces abiertos; $60–150+/hr en firmas especializadas — `https://divogue.net/hire-mcp-engineers`.
- **Freelancer.com** y **Fiverr** tienen categorías "Model Context Protocol Experts" / "Remote MCP Server Development" — `https://www.freelancer.com/hire/model-context-protocol` · `https://www.fiverr.com/hire/remote-mcp-server-development`.
- Implicación para precios: nuestras ofertas fijas S1-S5 ($400–$2,500) compiten contra 2–4 semanas de freelance hourly; la velocidad del agente es la ventaja.

## 2. Bounties y trabajo OSS

- **GitHub label search** (sin fee): `label:bounty state:open sort:created-desc` (guía dev.to "How to Find and Win Open Source Bounties in 2026" — `https://dev.to/timmothybuilder/...`).
- **Opire** — `https://opire.dev/home` · bounties desde **$20** sobre cualquier issue público; fee 4% + Stripe lo paga el creador del bounty; pago al merge del PR; tips `/tip` — fee/fuente: `https://www.oss.fund/opire` (verificado mar-2026).
- **Algora** — `https://algora.io` — hoy orientado a recruiting de OSS engineers (client stories: CodeRabbit, ComfyUI, Firecrawl); mantiene challenges: caso activo Turso "$1,000 por bug" (`https://algora.io/challenges/turso`).
- Implicación: canal de caja en días; el agente rastrea y PROPONE, el humano mergea/cobra.

## 3. Distribución: dónde se listan los MCP servers (estado real)

- **PulseMCP** — `https://www.pulsemcp.com/submit` — **submissions PAUSADAS** ("temporarily paused", página actualizada 3-sep-2026); recomiendan publicar en el **Official MCP Registry** del cual ingieren automáticamente al reabrir. 21,660+ servers indexados.
- **Official MCP Registry** — EL camino canónico hoy; ya probado por nosotros con alethech (`io.github.eddyflores100-lang/alethech`).
- **mcp.so** — directorio con secciones Directory / MCP clients / Remote servers / CLI / **Skills / Agents** + opción Advertise (`https://mcp.so`).
- **Anthropic Connectors Directory** — formulario oficial de submission; el flujo está documentado por la comunidad (reddit r/ClaudeAI: "Submitted a connector to Anthropic's MCP Directory").
- **Glama** — claim vía `glama.json` en la RAÍZ del repo/dominio (corrección propia Task 117-c; re-claim pendiente §13).
- Implicación: orden de ataque = Official Registry → Glama → mcpservers.org → mcp.so → Anthropic Directory; PulseMCP pasivo.

## 4. Monetización agente↔agente (riel en el que ya estamos posicionados)

- **x402** (LF Projects; impulso Coinbase/Cloudflare) — `https://x402.org` — producción real, **últimos 30 días: 75.41M transacciones · $24.24M volumen · 94.06K buyers · 22K sellers**. Pago HTTP-nativo (402), stablecoins, sin cuentas ni API keys; soporta agent-to-agent.
- **Cloudflare Monetization Gateway** — `https://blog.cloudflare.com/monetization-gateway` — cobrar por CUALQUIER recurso: APIs, datos, **llamadas MCP**; settlement sub-segundo; reglas por ruta/verbo; integra Web Bot Auth para identidad de agentes.
- Implicación: MarketNow corre en Cloudflare Workers y su `m2m-checkout` ya está en la API v4.2.0 → cuando gate C1 abra, el riel está listo; pitch a terceros: "cobre llamadas MCP con x402".

## 5. Cold email — guardarrails de deliverability 2026

- Fuente: MailReach, "Cold Email Deliverability: The Ultimate Guide (2026)" (ago-2026) — `https://www.mailreach.co/blog/cold-email-deliverability-sending-strategy`:
  - **≤80 correos fríos/día por dirección de envío** (tope absoluto 100) — escalar = más direcciones, no más volumen.
  - **1 dirección de envío por dominio** — reputación no se contamina entre dominios.
  - **Warm-up ≥15% del volumen** (~45 interacciones/día por dirección en autopiloto) mientras se envía.
  - Google/Microsoft 2026 ponderan fuertemente reportes de spam y engagement.
- Complementos estándar (Twilio/Salesforce deliverability 2026): autenticar dominio (SPF/DKIM/DMARC), listas limpias, asuntos no-spam.
- Implicación: NEXUS COLD opera dentro de estos límites o quemamos `alicelabs.site`; las secuencias del kit 04 ya están escritas a ese calibre.

## 6. Ecosistema de referencia (por qué vendemos "agent-first")

- `taikoxyz/taiko-ai` (91 commits, v1.5.0) y `taiko-docs`: el patrón público de superficie agent-first que ya replicamos (caso de estudio en `04_conocimiento/iniciativa-agent-first/`).
- Estándares vigentes en los que operamos: MCP (spec 2026-07-28, modelcontextprotocol.io), skills formato agentskills.io (instalables vía `npx skills add`), agents.md/AAIF, Agent Cards (/.well-known/agent.json).
