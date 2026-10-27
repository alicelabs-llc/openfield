---
name: mcp-compliance-2026
description: Checklist de compliance MCP 2026 para el servidor de marketnow.site y para auditar servidores del catálogo. Activar al trabajar en /api/mcp, el Worker de Cloudflare, claims en directorios (Glama/Smithery/mcpservers.org), o al auditar skills/servidores de terceros para el catálogo Sentinel.
---

# MCP compliance 2026 — checklist del servidor propio y del catálogo (v3.0)

Fuente: especificación modelcontextprotocol.io verificada el 21-oct-2026 (Tasks 117-c). Timeline: 2024-11-05 → 2025-03-26 (Streamable HTTP) → 2025-06-18 (OAuth resource server, elicitation) → 2025-11-25 (OIDC, URL-mode elicitation) → **2026-07-28 latest (stateless, sin handshake)**.

## Checklist del servidor remoto propio (marketnow.site/api/mcp → Worker CF)
1. [ ] **Streamable HTTP** en un único endpoint POST (SSE deprecado para remotos).
2. [ ] **Dual-era**: aceptar `initialize` legacy (≤2025-11-25) Y protocolo stateless 2026-07-28 (`_meta` con `io.modelcontextprotocol/protocolVersion`) — `UnsupportedProtocolVersionError` si no soporta.
3. [ ] **`server/discover`** implementado: anuncia versiones/capacidades/identidad.
4. [ ] **RFC 9728**: `/.well-known/oauth-protected-resource` + header `WWW-Authenticate` con resource_metadata al devolver 401 (aunque el auth sea simple — es lo que clientes y directorios inspeccionan primero).
5. [ ] OAuth 2.1 + RFC 8707 (resource indicators) + RFC 9207 (`iss`); soportar Client ID Metadata Documents (DCR deprecado).
6. [ ] **`/.well-known/mcp/server-card.json`** (SEP-1649): serverInfo + authentication + tools — lo que Smithery y directorios consumen ante auth-walls.
7. [ ] 403 ante Origin inválido; JSON Schema 2020-12 en inputSchema; tools/list determinista + `ttlMs`/`cacheScope` en resultados cacheables.
8. [ ] **server.json en el MCP Registry oficial** (registry.modelcontextprotocol.io, CLI `mcp-publisher`, remotes streamable-http, namespace por dominio DNS-verificado) — Glama/PulseMCP y demás aggregators sindican desde aquí.

## Corrección crítica del claim Glama (descubierta en esta investigación)
El worklog histórico asumía `/.well-known/glama.json` — **la doc verificada dice glama.json en la RAÍZ del repo GitHub** (`{$schema: glama.ai/mcp/schemas/server.json, maintainers: [usuario-github]}`); repos de org requieren el archivo (personales pueden OAuth). Corregir ANTES de re-clamar.

## Auditar un servidor/skill del catálogo (para certificados Sentinel)
1. Correr el checklist de seguridad de la skill seguridad-fuentes (anti tool-poisoning).
2. Verificar: transporte declarado vs real, auth, schema válido, `server/discover` o server-card presente.
3. Contra skills.sh Audits (Trust Hub/Socket/Snyk): nuestros certificados firmados verificables (UTA/Ed25519) son CAPA SUPERIOR al escaneo — posicionarlo así en marketing: "escaneo + firma verificable", no "escaneo".

## Ecosistema de estándares (contexto de gobernanza)
AAIF (Linux Foundation, dic-2025) administra MCP (donado por Anthropic) + AGENTS.md (donado por OpenAI) + goose (Block); A2A v1.0 es el estándar agente↔agente (`/.well-known/agent-card.json`) y complementa a MCP (agente↔herramientas). Claim de marketing verificable: "cumple estándares Linux Foundation-AAIF".
## Grader (v6.0 — añadido por regla 32)

- Claim en directorios SOLO tras inspección de schema de /api/mcp → PASS.
- glama.json referenciado en RAÍZ del repo (no /.well-known/) → PASS.
- Claim publicado con cifra muerta o schema no inspeccionado → FAIL.
