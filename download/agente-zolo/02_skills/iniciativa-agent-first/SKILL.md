---
name: iniciativa-agent-first
description: Protocolo para que CUALQUIER producto de AliceLabs tenga superficie de agente de primera clase (skills + subagentes + MCP servers + plugin + docs agent-first + auto-auditoría), replicando el patrón verificado de taikoxyz/taiko-ai y taiko-docs. Activar al lanzar un producto nuevo, al abrir un repo público nuevo, o cuando el usuario diga "replica la iniciativa", "hazlo agent-first", "como taiko".
---

# Iniciativa agent-first — el patrón Taiko como procedimiento (v3.1)

Origen: Task 118 (21-oct-2026) — caso de estudio `taikoxyz/taiko-ai` + `taikoxyz/taiko-docs` verificado en fuentes primarias. Análisis completo: `iniciativa-agent-first/CASO_ESTUDIO_TAIKO.md` · Réplica aplicada a UTA: `download/uta-ai/` + `PLAN_REPLICACION.md`.

## Los 7 componentes obligatorios (checklist de lanzamiento)

1. **Repo `<producto>-ai`** con: `skills/*/SKILL.md` (frontmatter agentskills.io: name slug + description ≤1024 con triggers "Use when..." y routing "For X use skill Y instead") · `agents/*.md` (frontmatter: tools, mcpServers, color, memory, skills) · `.claude-plugin/marketplace.json` + `plugin.json` · `audit.md` · README con instalación triple.
2. **Instalación en 1 comando por los 3 canales**: `npx skills add <org>/<repo>` · `/plugin marketplace add <org>/<repo>` · config MCP.
3. **MCP servers con schema de salida fijo**: toda tool/CLI devuelve `{ schema_version, command, status, network, data, errors, warnings, metrics }` — jamás texto solo-humano. Write tools tras env vars + confirmación.
4. **Docs agent-first (4 formatos)**: `/llms.txt` (índice con descripciones) · `/llms-full.txt` · `/<path>.md` por página · **`/SKILL.md` en la raíz del dominio** (referencia de agente: cómo operar el producto sin preguntar).
5. **`audit.md` público**: cada PR importante del agente lleva auditoría posterior en 3 categorías — Bugs (con severidad) · Violaciones de reglas · Token efficiency (payloads inflados, sin paginar, filtrado client-side). Publicar ANTES del merge.
6. **Agente como contribuidor** con identidad propia (co-author) — como dantaik + claude en taiko-ai.
7. **CI con drift-check**: workflow diario que compara cifras vivas (APIs) vs cifras citadas en docs — build rojo = cifra muerta = actualizar con fecha nueva. (Mejora propia sobre el patrón Taiko.)

## Reglas de calidad heredadas del caso Taiko

- Skills con **triggers explícitos** en description (el routing entre skills se hace en texto, no en código).
- Troubleshooting tabulado en toda skill (síntoma → solución).
- **Token efficiency es categoría de auditoría de primera clase**: ABIs completos vs firmas truncadas, resultados sin paginación, filtrado que pertenece al servidor.
- La metadata para agentes **se testea** (browser tests), no se espera.
- Claims de marketing no verificables = violación auditada (así lo castiga el propio audit.md de Taiko).

## Cómo aplicarlo a un producto NUEVO (procedimiento)

1. Inventario de superficie viva del producto (curl de APIs, sitemap, agent.json si existe) — cifras con fecha+fuente.
2. Reducir a 3-5 skills por dominio (no 1 skill monolítica) + 1-3 subagentes con frontmatter completo.
3. Escribir los 7 componentes con las plantillas de `download/uta-ai/` (es el scaffold de referencia — copiar estructura, adaptar contenido).
4. Validar: `python3 scripts/validate_skills.py` (frontmatter ≤1024) · `python3 -m json.tool` en los plugin JSON.
5. Si el producto ya tiene llms.txt: NO reemplazar a ciegas — generar propuesta v2 (script `generate_llms_txt.py` como modelo) y comparar drift de cifras primero (GAPS.md como modelo).
6. Registrar en el worklog qué quedó YO vs TÚ (push/deploy requieren credenciales) — regla 2, nunca degradar a borrador.

## Detección de oportunidad (cuándo proponerlo sin que lo pidan)

- Producto nuevo sin skills/MCP → proponer el repo `<producto>-ai` en el mismo task de lanzamiento.
- Repo público nuestro cuyo README no menciona agentes → proponer instalación triple.
- `/SKILL.md` 404 en cualquier dominio nuestro → artefacto + pasos de deploy (YOTO).
- Cifras distintas entre superficies (llms.txt vs API vs agent.json) → incidente de drift → GAPS.md + drift-check.
## Grader (v6.0 — añadido por regla 32)

- Lanzamiento de producto incluye superficie agent-first en el MISMO task (repo <producto>-ai, 4 formatos de docs, MCP con schema fijo, audit.md) → PASS.
- audit.md escrito antes del merge de PR importante → PASS.
- Lanzamiento sin /SKILL.md en la raíz del dominio → FAIL.
