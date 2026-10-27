# 04 — CAMPAÑA NEXUS COLD (lista para cargar y enviar)

> NEXUS COLD = nuestra herramienta de cold email mejorada (declarada por el founder; pendiente de documentar en inventario). Este archivo le entrega: configuración, guardarrails, segmentos, leads y secuencias terminadas. El envío lo ejecuta NEXUS COLD; las respuestas entran a `support@alicelabs.energy` (forwarder activo, verificado Task 91). Gmail inbox = OTRO agente.

## 4.1 Registro del activo NEXUS COLD (a completar por TÚ)

| Campo | Valor |
|---|---|
| Repo/ubicación | ⚠️ VERIFICAR-EN-BOOT (no está en worklog) |
| Mejoras vs base | declaradas por founder — documentar aquí |
| Dominio(s) de envío | ⚠️ p.ej. `alicelabs.site` con subdominio dedicado `mail.alicelabs.site` |
| SPF/DKIM/DMARC | ⚠️ verificar antes del primer envío (requisito 2026) |
| Warm-up | ⚠️ nuevo dominio = 2–3 semanas antes de volumen |
| Volumen máx | 80/día por dirección (ver guardarrails) |

## 4.2 Guardarrails de deliverability (fuente: MailReach "Cold Email Deliverability Ultimate Guide 2026", ago-2026 — citada en 01 §E)

1. **≤80 correos fríos/día por dirección** (tope duro 100). Escalar = añadir direcciones, no volumen.
2. **1 sola dirección de envío por dominio.** Para 2ª dirección → 2º dominio (contagio de reputación).
3. **Warm-up ≥15% del volumen** (~45 interacciones/día en autopiloto) mientras la campaña corre.
4. Google/Microsoft 2026 pesan mucho los reportes de spam y la engagement → **texto plano, 1 link máximo, 1 CTA, sin imágenes, sin tracking visible agresivo**.
5. Bajas + lista limpia: cualquier respuesta negativa o bounce → excluir permanente. Stop total si spam-rate > 0.3%.

## 4.3 Fuentes de leads (todas públicas; el agente las arma solo)

| Segmento | Dónde viven los leads | Señal de dolor |
|---|---|---|
| **S1 Autores de MCP servers** | Listados públicos: Official MCP Registry, mcp.so, Glama, mcpservers.org (alethech ya nos dio acceso al ecosistema) | Su server no tiene conformance/trust/badge; invisible en búsquedas de agentes |
| **S2 Startups/devtools con API** | GitHub repos con API pública + Hire pages; Founders en directories | Quieren distribución y ser descubiertos por agentes; no saben cómo |
| **S3 Empresas que CONTRATAN agentes/MCP** | Postings activos en Upwork "MCP Server Developers", Fiverr, Algora | Demanda declarada con presupuesto — el lead más caliente |
| **S4 Agentes operadores** (atraer agentes) | Directorios de agentes, Agent Cards públicos, comunidades MCP/A2A | Necesitan confianza entre pares y monetización (ATC/x402) |

Higiene: solo correos públicos de contacto/proyecto (no scraping personal), identificar remitente y empresa, opt-out en 1 línea, CAN-SPAM/GDPR básico. Si un dominio publica `abuse@`/`noc@`, no usarlo para ventas.

## 4.4 Secuencias (EN = mercado global; ES = LATAM/ES). Cadencia: Día 0 → Día 3 → Día 7. Toque final Día 14 (breakup) opcional. Un CTA por correo.

### Segmento S1 — Autores de MCP servers (oferta: S3 conformance+ATC $400, upsell S1)

**E1 · Asunto:** `your MCP server, verified — 3 min check`
```
Hi {{first_name}},

Saw {{server_name}} in the {{directory}} directory — solid {{category}} work.

Quick one: agents increasingly skip servers they can't trust. We run a conformance
check (our @marketnow/uta-conformance npm, public) + issue an Agent Trust Card —
"SSL for AI agents" — with a verifiable badge.

$400 flat, 3 days, report + badge. Live example on our own infra: https://marketnow.site/atc

Worth a 15-min call?

Edison — AliceLabs LLC (marketnow.site)
Opt-out: reply "no"
```
**E2 (día 3):** asunto `re: your MCP server, verified`
```
{{first_name}} — quick add: we indexed {{count_skills}} skills and agents check trust
scores before install (flow: manifest → search → trust-score → signed cert).
Unverified servers drop out of that loop.

If it's useful I'll run the free pre-check on {{server_name}} and send findings
before you pay anything. Yes/no?
```
**E3 (día 7):** asunto `closing the loop`
```
Last note, {{first_name}}. If trust/badges aren't a priority for {{server_name}}
right now, all good — good luck with it.

If it ever is: the conformance + ATC package stays $400 flat for directory authors
this month.
```

### Segmento S2 — Startups/devtools con API (oferta: S1 Superficie Agent-First $2,500)

**E1 · Asunto:** `{{company}} × agents: be discoverable in 7 days`
```
Hi {{first_name}},

Agents are becoming your buyers — but they can't discover {{company}} unless your
product speaks agent-first: llms.txt, SKILL.md, an MCP surface, skills they can
install.

We package exactly that in one delivery (replicated from the public taiko-ai
pattern, shipped live on our own stack): repo <product>-ai + docs agents can read
+ MCP server + Claude Code plugin + CI that keeps numbers honest.

$2,500 fixed, 7–10 days. Live demo: https://marketnow.site/agents

Open to 15 minutes?

Edison — AliceLabs LLC (marketnow.site)
Opt-out: reply "no"
```
**E2:** prueba social + cifras vivas (re-verificadas al generar) + caso taiko-ai público. **E3:** breakup con oferta de pre-diagnóstico gratis (`/llms.txt` de su dominio: existe/no existe — el agente lo comprueba en vivo antes de enviar).

### Segmento S3 — Postings activos (oferta: la que pida el posting; respuesta <24h)

- El agente monitorea Upwork/Fiverr/Algora; para cada posting relevante prepara propuesta con: 1) demo propia viva (marketnow.site), 2) entregable concreto de 02, 3) precio fijo, 4) fecha de entrega. Estos NO son fríos: respuesta personalizada en <24h, dentro de la plataforma.

### Segmento S4 — Atraer AGENTES (oferta: free tier + ATC gratis primeros 100)

**E1 · Asunto:** `free trust card for {{agent_name}}`
```
Hi {{first_name}} — you operate {{agent_name}}.

Agents that verify each other close more deals autonomously. We issue Agent Trust
Cards ("SSL for AI agents") — free for the first 100 agents this month, no card
required: signed badge + agent.json + listing in our registry (71,198 skills
indexed; agents check trust before install).

Claim it in one reply: your agent URL is enough.
https://marketnow.site/atc

Edison — AliceLabs (marketnow.site)
Opt-out: reply "no"
```
**E2:** x402/monetización angle — "when your agent sells, m2m-checkout + trust = higher close". **E3:** referral loop (`agent-referral` ya vive en nuestra API v4.2.0).

## 4.5 KPIs y reglas de parada (por segmento, ventana 14 días)

| Métrica | Meta | Parada/corrección |
|---|---|---|
| Bounce | <2% | >2% → pausa, limpia lista |
| Respuesta | ≥3% S1/S4, ≥2% S2 | <1% → cambia asunto/primera línea (test A/B por bloque de 80) |
| Reuniones | ≥2/semana | 2 semanas sin reuniones → cambia segmento |
| Spam complaints | 0.1% | >0.3% → STOP total, revisa dominio |
| Cierre S3 | 1 de cada 15 propuestas S3 | — |

## 4.6 Pipeline (el agente lo mantiene en worklog, formato fijo)

`| fecha | segmento | lead | oferta | estado (enviado/abrió/respondió/reunión/cerrado/$) | siguiente acción |`
Cierre de sesión = commit alethech con evidence (regla 24).
