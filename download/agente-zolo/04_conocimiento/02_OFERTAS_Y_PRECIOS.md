# 02 — OFERTAS, PRECIOS Y CLIENTE IDEAL

> Principio: vendemos RESULTADO con demo viva, no horas. Los precios anclan contra el mercado verificado (MCP devs $20–60/hr en marketplaces, $60–150+ en firmas — ver 01 §E). Nuestras ofertas compiten por VELOCIDAD (entrega en días por agente) y por PRUEBA (conformance + certificado, nadie más lo da).

## CARRIL 1 — Servicios productizados (INGRESO YA, días-semanas)

| # | Oferta (nombre comercial) | Qué recibe el cliente | Precio fijo | Entrega | Cliente ideal (ICP) |
|---|---|---|---|---|---|
| S1 | **Superficie Agent-First** | Su producto convertido en superficie instalable por agentes: repo `<producto>-ai` (skills + subagentes + MCP server + plugin Claude Code) + docs agent-first 4 formatos (`llms.txt`, `llms-full.txt`, `.md` por página, `SKILL.md`) + CI con drift-check. Réplica del patrón taiko-ai, ya ejecutado 1 vez para UTA | **$2,500** (base) / $3,500 con MCP server remoto | 7–10 días | Startup/empresa con API o devtool que quiere ser descubierta por agentes |
| S2 | **MCP Server a medida** | Server MCP (local stdio o remoto) con schema de salida fijo, cache, tests, README + publish en Official MCP Registry y directorios | **$1,200–2,500** según tools | 5–10 días | SaaS/SMB con API que quiere exposición en Claude/ChatGPT/Cursor/agents |
| S3 | **Auditoría de conformance + ATC** | Corrida de conformance (`@marketnow/uta-conformance`) contra su MCP/API + reporte de bugs + **Agent Trust Card (SSL para agentes)** + badge verificable | **$400** | 3 días | Autores de MCP servers (miles, listados públicamente en directorios) |
| S4 | **Memoria con cadena de custodia** | Alethech instalado y operando: `init`+`commit`+`evidence`+`verify`, rotación de claves, simulacro DR, entrenamiento al equipo | **$500** setup + $50/mes | 3–5 días | Equipos que operan agentes con requisitos de auditoría/compliance |
| S5 | **Agent Ops kit** | Implementación del paquete v3.2 (BOOT protocol, runbook, evals E01-E30, skills) calibrado a la empresa | **$1,000** + $200/mes mantenimiento | 10 días | Equipos serios operando agentes en producción |

**Cómo se cobran:** AliceLabs LLC (Wyoming) factura; aceptar USDC (riel x402/Stablecoin, sin fricción internacional), Stripe (si se activa) o wire. 50% adelanto en S1/S2/S5.

## CARRIL 2 — Producto UTA/ATC (INGRESO RECURRENTE, activar tras primeras ventas)

| Plan | Qué incluye | Precio propuesto |
|---|---|---|
| Free para agentes | verify/translate ilimitado (read), agent card, badge ATC básico | $0 — es el imán de adquisición |
| Pro | `issue`/`bridge` (write) con token, 10k verificaciones/mes, certificados firmados, soporte | **$49/mes** |
| Scale | todo Pro + volumen alto, SLA, dominio propio para badges, integración con su pipeline | **$299/mes** |
| Por llamada (agentes) | verificación unitaria vía HTTP 402 / x402 cuando `m2m-checkout` abra gate C1 | **$0.001–0.01/call** |

Precios = propuesta a validar; anclan por debajo de una hora de dev senior ($60-150/hr) para que la decisión sea obvia. El pitch: "confianza verificable entre agentes, como SSL para IA — hoy gratis para tu agente".

## CARRIL 3 — Marketplace MarketNow (INGRESO POR VOLUMEN, medio plazo)

- `agent-hire` + `m2m-checkout` ya existen en la API v4.2.0 (verificados hoy) → al abrir gate C1, MarketNow cobra fee por transacción agente↔agente (target 5–10%).
- Listings destacados en catálogo (71,198 skills, tráfico de agentes): placement de $99–499/mes para autores que quieran descubribilidad (propuesta; requiere activar analytics).
- Contexto a favor: x402 procesa $24.24M/mes con 22K sellers (x402.org) y Cloudflare lanzó Monetization Gateway para cobrar llamadas MCP — nosotros ya vivimos en Cloudflare Workers. Ventaja estructural real.

## Mensaje maestro (todo pitch deriva de esto)

> "Tu producto necesita que los AGENTES lo descubran, confíen y paguen. Nosotros hacemos exactamente eso: convertimos tu producto en superficie agent-first (skills + MCP + llms.txt + plugin), lo auditamos con conformance y le damos una Agent Trust Card — 'SSL para agentes IA'. Ya lo hicimos para nuestra propia infraestructura viva en marketnow.site; lo hacemos para el tuyo en 7 días."

## Objeciones y respuestas (para NEXUS COLD y respuestas del agente)

1. *"Ya tengo API, ¿por qué agent-first?"* → Porque el comprador de tu producto cada vez más es un agente, no una persona; sin llms.txt/SKILL.md/MCP eres invisible para él. Demo: marketnow.site/agents (flujo de 6 pasos, vivo).
2. *"¿Por qué ustedes?"* → Somos los únicos que además del desarrollo entregamos conformance auditable + ATC (certificado de confianza) sobre infraestructura propia viva con 71,198 skills indexadas. Cifras re-verificadas en vivo antes de cada envío.
3. *"$2,500 es caro"* → Market rate para un MCP dev: $20–60/hr en marketplaces (guía 2026); un server bien hecho son 2–4 semanas de un freelance. Nosotros entregamos en 5–10 días con publicación en registries incluida + certificado. Alternativa: empezar por S3 ($400) y escalar.
4. *"¿Confianza? ¿Quién los audita a ustedes?"* → Código source-available (AL-1.0), pipeline fail-closed público de 12 etapas, conformance npm pública v1.4.0. La auditable-idad ES el producto.
