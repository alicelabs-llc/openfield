# CONOCIMIENTO — Empresa y superficie viva (canon 21-oct-2026)

> Datos, no reglas. Regla de frescura: en un pitch, toda cifra se re-verifica en vivo antes de usarse (cifra >7 días = prohibida). Este archivo se actualiza en cada BOOT de ventas.

## 1. Empresa

| Campo | Valor |
|---|---|
| Entidad | AliceLabs LLC — Wyoming, USA (puede facturar; pagos objetivo: USDC/Stripe/wire) |
| Founder | Edison Flores (Ecuador; timezone America/Guayaquil — todas las fechas del agente) |
| Producto principal | **MarketNow** — marketnow.site — "the first agent-first marketplace": agentes descubren, evalúan, compran e instalan MCP skills autónomamente |
| Infra | Cloudflare Pages + R2 + Workers MCP (proyecto Vercel residual `marketnow-uta`; Hostinger CONGELADO por decisión del founder — no re-suscitar) |
| Cuentas | GitHub: `alicelabs-llc` (canon, appeal sin respuesta), `eddyflores100-lang` (operativa, PAT Task 98), `edgarfloresguerra2011-a11y` (flaggeada) · npm `@marketnow` · PyPI `alethech` |
| Canales de entrada | `support@alicelabs.energy` (forwarder activo, verificado Task 91) · alias From `contacto@alicelabs.site` vía Gmail SMTP · Gmail inbox = OTRO agente (este agente no toca la bandeja) |
| Herramienta propia de outbound | **NEXUS COLD** (cold email mejorada, declarada por el founder; documentación pendiente — registro en 04 §4.1) |

## 2. Superficie VIVA verificada (curl 21-oct-2026, HTTP codes reales)

| Endpoint | Estado | Contenido clave |
|---|---|---|
| `/api/health` | 200 | **v4.2.0** · features: `sentinel-l1`, `leaderboard`, `arena`, `quests`, **`agent-hire`**, `submit`, **`m2m-checkout`**, `agent-rep`, `agent-referral` |
| `/api/skills` | 200 | **71,198 skills indexadas** (paginado; `/api/categories.json`; páginas `/s/<slug>`; badge SVG por skill) |
| `/agents` | 200 | Registro & descubrimiento de agentes; flujo de 6 pasos: manifest → search → trust-score → certificado firmado → install (`npx -y marketnow-mcp`) → … |
| `/api/trust` | 200 (Task 118) | UTA: verify / translate / issue / bridge — pipeline fail-closed de 12 etapas, 9 formatos de credenciales (`UNKNOWN = DENY`) |
| `/api/mcp` | 200 | 9 tools MCP remotas (search_skills, verify_trust, translate_credential, list_formats, get_pipeline, check_domain, check_revocation, fingerprint_tool, submit_skill) |
| `/agent-protocol.json` | 200 | **MAP v1.1.0** (MarketNow Agent Protocol) — descubre/evalúa/compra/instala; commerce marcado "planned, gate C1" |
| `/atc` | 200 | **ATC — Agent Trust Card** ("SSL for AI Agents") |
| `/api/agent.json` + `/.well-known/agent.json` | 200 | Agent Card v4.0.0 |
| `/llms.txt` · `/llms-full.txt` | 200 | Docs agent-first — **DEUDA: cifra muerta 68,388 vs vivo 71,198**; fix listo en `uta-ai/site-agent-first/llms-v2.txt` (requiere deploy CF) |
| `/SKILL.md` | **404** | Artefacto listo para deploy (misma carpeta) — desplegar |
| `/handshake` | **404** | Referenciado pero muerto — eliminar de docs o implementar |

npm: `@marketnow/uta-conformance@1.4.0` (latest) · `marketnow-mcp` (instalación autónoma por agentes).

## 3. Repos propios

| Repo | Rol | Estado |
|---|---|---|
| `alicelabs-llc/universal-trust-adapter` | UTA canon (AL-1.0 source-available) | vivo |
| `eddyflores100-lang/uta` | publicador duplicado residual (workflow desactivado) | archivar — decisión del usuario |
| `eddyflores100-lang/alethech` v0.9.1 | memoria con cadena de custodia (9 comandos CLI, `.aleth` scrypt+AES-256-GCM, DR 42s medidos, 84+ commits) | listado en mcpservers.org + Official MCP Registry (`io.github.eddyflores100-lang/alethech`) + Awesome-Agent-Memory |
| `uta-ai` (local `download/uta-ai/`) | réplica del patrón taiko-ai: 4 skills + 2 subagentes + MCP servers spec + plugin Claude Code + CI drift-check | **push pendiente de PAT** |
| Kit agente v3.3 (este paquete) | definición completa del agente (25 reglas, 12 skills, 33 evals) | este bundle |

## 4. Deudas de credibilidad (arreglar antes de campañas grandes)

1. Drift de cifra en `/llms.txt` (68,388 → 71,198): deploy `llms-v2.txt` — CF.
2. `/SKILL.md` 404: deploy del artefacto — CF.
3. `/handshake` 404: eliminar o implementar.
4. Glama re-claim: `glama.json` en la RAÍZ (corrección Task 117-c).
5. Push de `uta-ai` (PAT): sin él, la oferta S1 no tiene demo pública ni skills instalables.
6. NEXUS COLD sin documentar: bloquea campañas email.

## 5. Posicionamiento (una línea)

> "Convertimos tu producto en algo que los AGENTES descubren, confían y pagan — skills + MCP + docs agent-first + conformance auditable + Agent Trust Card. Ya lo vive nuestra propia infraestructura (71,198 skills, v4.2.0); lo instalamos en la tuya en 7 días."
