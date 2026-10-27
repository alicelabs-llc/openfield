# 01 — INVENTARIO DE ACTIVOS VENDIBLES (verificado en vivo 21-oct-2026)

> Regla: este archivo es la ÚNICA fuente de cifras para pitches. Cada cifra lleva su verificación. Si un BOOT encuentra que un número cambió, actualiza aquí primero y luego vende.

## A. Superficie VIVA de marketnow.site (verificada con HTTP codes hoy)

| Activo | URL | Verificación 21-oct-2026 | Dónde está el dinero |
|---|---|---|---|
| API de confianza UTA (verify/translate/issue/bridge, pipeline fail-closed de 12 etapas) | `https://www.marketnow.site/api/trust` | 200 (Task 118; re-verificar en BOOT) | Producto core: read gratis, `issue`/`bridge` de pago vía `UTA_ISSUE_TOKEN` |
| Endpoint MCP remoto (9 tools) | `https://marketnow.site/api/mcp` | 200 (agent.json lo confirma por nombre) | Herramienta de adquisición: si un agente lo usa, se acostumbra a nuestra superficie |
| Catálogo de skills (L1) | `https://marketnow.site/api/skills` | 200 — **total: 71,198** (contado hoy vía API) | Marketplace: listings destacados, badges, fees de transacción |
| Health del worker | `/api/health` | 200 — **v4.2.0**, features: `sentinel-l1`, `leaderboard`, `arena`, `quests`, **`agent-hire`**, `submit`, **`m2m-checkout`**, `agent-rep`, `agent-referral` | `agent-hire` + `m2m-checkout` = infraestructura de monetización YA desplegada, falta activar demanda |
| Registro & descubrimiento de agentes | `https://marketnow.site/agents` | 200 — "The first agent-first marketplace. Built for agents, by agents. Agents discover, evaluate, purchase, and install MCP skills — autonomously" + flujo de 6 pasos (manifest → search → trust-score → certificado firmado → `npx -y marketnow-mcp`) | Landing de venta para el segmento "agentes" |
| MarketNow Agent Protocol (MAP) | `https://marketnow.site/agent-protocol.json` | 200 — **v1.1.0** (descubre, evalúa, compra, instala; commerce marcado "planned, gate C1") | Diferenciador: protocolo propio publicable |
| ATC — Agent Trust Card ("SSL for AI Agents") | `https://marketnow.site/atc` | 200 | Producto vendible por sí solo (badges/certificados) |
| Agent Card | `/api/agent.json` + `/.well-known/agent.json` | 200 | Requisito de listing en muchos directorios |
| Paquete npm de conformance | `@marketnow/uta-conformance` | **1.4.0 latest** (npm view hoy) | Servicio de auditoría de conformance para terceros |
| Cliente npm para agentes | `marketnow-mcp` (`npx -y marketnow-mcp`) | citado por /agents y agent-protocol.json | Canal de instalación autónoma por agentes |

## B. Productos repo/npm/PyPI (fuera del sitio)

| Activo | Dónde vive | Estado | Dinero |
|---|---|---|---|
| UTA — Universal Trust Adapter (canon) | `alicelabs-llc/universal-trust-adapter` | vivo; licencia AL-1.0 source-available | Licencias comerciales + API de pago |
| `uta-ai` — superficie agent-first completa (4 skills, 2 subagentes, MCP servers spec+scaffold, plugin Claude Code, CI + drift-check, audit.md) | `download/uta-ai/` local, **push pendiente de PAT** | scaffold validado localmente 4/4 | (1) Réplica como SERVICIO para terceros (oferta S1). (2) Al hacerse público: distribución de skills |
| Alethech — memoria con cadena de custodia (9 comandos CLI, contenedor `.aleth`, DR 42s medidos, 84+ commits) | `eddyflores100-lang/alethech` v0.9.1 | listado en mcpservers.org + Official MCP Registry (`io.github.eddyflores100-lang/alethech`) + Awesome-Agent-Memory | Instalación soportada como servicio (oferta S4) |
| NEXUS COLD — herramienta de cold email mejorada | declarada por el founder; NO está en el worklog | **pendiente de documentar** (repo, stack, estado) | Motor de la propia prospección; potencialmente vendible como servicio de outbound para terceros |
| Kit ZOLO v3.2 (24 reglas, 11 skills, 30 evals, BOOT protocol) | `download/agente-zolo/` | completo y verificado | "Agent Ops kit" vendible como consultoría/implementación (oferta S5) |

## C. Infraestructura y marca

- Dominio vivo: `marketnow.site` (Cloudflare Pages + R2 + Workers MCP). Dominios secundarios: `alicelabs.site`, `alicelabs.energy` (soporte: `support@alicelabs.energy` con forwarder verificado; alias From `contacto@alicelabs.site`).
- Cuentas: GitHub `alicelabs-llc` (canon), `eddyflores100-lang` (operativa, PAT Task 98), `alicelabsllc` (org con appeal sin respuesta). npm org `@marketnow`. AliceLabs LLC (Wyoming) — puede facturar.
- Skill ya probada una vez: publicar alethech en registries funcionó → el mismo playbook se repite para marketnow.

## D. Deudas de credibilidad (bloquean ventas — arreglar ANTES de la campaña grande)

1. **Drift de cifra**: `/llms.txt` cita 68,388 vs vivo **71,198** (detectado hoy). Un pitch con cifra muerta contradice nuestro propio producto (la confianza). Fix: desplegar `llms-v2.txt` ya generada en `uta-ai/site-agent-first/` — requiere credenciales CF (TÚ).
2. `/SKILL.md` sigue **404** (el artefacto está listo en `uta-ai/site-agent-first/`): los agentes que llegan por llms.txt se chocan con la puerta cerrada. Mismo deploy CF.
3. `/handshake` **404** (referenciado en superficies): eliminar de docs o implementar.
4. Glama: re-claim pendiente con `glama.json` en raíz (pendiente #2 del §13 v3.2) — Glama es directorio de alto tráfico de agentes.
5. `uta-ai` sin push (PAT) → los skills no instalables vía `npx skills add` y la oferta S1 no tiene demo pública.
6. NEXUS COLD sin documentar → no se puede ejecutar campaña ni vender como servicio.

## E. Cifras de mercado citables en pitches (con fuente)

- Demanda freelance de MCP: Upwork tiene categoría dedicada "Hire MCP Server Developers" (`upwork.com/hire/mcp-server-developers`); guía de contratación 2026: **$20–60/hr** en marketplaces abiertos, **$60–150+/hr** en firmas especializadas (divogue.net/hire-mcp-engineers).
- x402 (pagos HTTP-nativos para agentes, LF Projects): **75.41M transacciones / $24.24M volumen / 22K sellers en los últimos 30 días** (x402.org, hoy). Cloudflare Monetization Gateway cobrará por llamadas MCP (blog.cloudflare.com/monetization-gateway).
- PulseMCP (21,660+ servers indexados): submissions pausadas desde sep-2026, ingestan desde Official MCP Registry (pulsemcp.com/submit) → publicar en el registry oficial es EL camino.
