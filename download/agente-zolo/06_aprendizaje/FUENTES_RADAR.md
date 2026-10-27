# RADAR — fuentes de información continua (regla 33, v6.0)

El agente se mantiene AL DÍA con cadencia fija. Cada fuente declara QUÉ vigilar y QUÉ.extraer (solo patrones portables a protocolo markdown — jamás adoptar frameworks). Protocolo: **semanal ≥30 min** (1 patrón portable mínimo como criterio de éxito) · **mensual**: verificación de estrellas/patrones del estado del arte (§16 núcleo).

## 1. Fuentes técnicas (ingeniería de agentes y autonomía)

| Fuente | Qué vigilar | Cadencia |
|---|---|---|
| GitHub Trending (topics: agent-skills, claude-skills, ai-agents, mcp) | repos que explotan → ¿patrón portable? | semanal |
| `anthropics/skills` (releases + discussions) | skills oficiales nuevas + spec agentskills.io | semanal |
| `obra/superpowers` (releases) | disciplina de skills (v7: skills que sobreviven compaction) | semanal |
| `VoltAgent/awesome-agent-skills` (nuevas entradas) | el mapa de 1000+ skills — capacidad que me falta (regla 32) | semanal |
| Anthropic Engineering blog + "Building Effective Agents" | patrones de orquestación oficiales | mensual |
| modelcontextprotocol.io changelog + agentskills.io + agents.md | cambios de estándar (LF-AAIF) | mensual |
| HN (front page + Show HN top) | señal de mercado + lanzamientos de competencia | semanal |

## 2. Fuentes de comunidad

| Fuente | Qué vigilar | Cadencia |
|---|---|---|
| r/claudeskills, r/SideProject, r/LocalLLaMA | qué skills/methods pide la gente (FEATURE_REQUESTS candidatos) | semanal |
| Dev.to / Medium topics agentes | contenido que citan nuestros leads (material de outreach) | semanal |
| Hilos propios (llama_index#23122, langchain#40158, mcp#540, cline#13652, autogen#8139) | respuestas pendientes — implementar antes que responder (regla 3) | en cada BOOT |
| dev.to anp2network + comunidad conocida | pedidos de artefactos (regla 3) | en cada BOOT |

## 3. Fuentes del founder (jerarquía máxima — se procesan primero)

| Tipo | Protocolo |
|---|---|
| **Reels/links/canales que el founder mande** (ej. los 12 reels de Task 123) | descifrar contenido → clasificar: herramienta instalable (regla 32) / patrón / conocimiento / oportunidad de negocio (regla 25) / solo-FYI → captura en ledger → respuesta con lo EJECUTADO (regla 2) |
| Correcciones y fricciones | regla 31 (captura en caliente) + §15 (promoción a regla) |
| "Mejora el agente" / "auditoría de definición" | §15.5: fricciones + worklog + evals + este radar → propuesta con evidencia |

## 4. Salida del radar (obligatoria, grep-able)

Cada sesión de radar cierra con entrada en worklog:

```markdown
### RADAR <fecha> — <n> fuentes revisadas
- PATRÓN NUEVO: <1 línea portable o "ninguno esta semana">
- ACCIÓN: <instalada skill X (regla 32) | actualizada fuente Y | hueco anotado en FEATURE_REQUESTS | ninguno>
```

`grep "PATRÓN NUEVO" worklog.md` = historial de vigilancia. Radar con 2 semanas seguidas sin ningún patrón/acción = radar pasivo (FAIL) — subir profundidad o cambiar fuentes.

## 5. Descubrimientos ya procesados (historial vivo)

- **Task 123 (24-oct-2026)**: 12 reels descifrados → 8 repos clonados (superpowers ~304k★, anthropics/skills ~183k★, ui-ux-pro-max, taste-skill, self-improving-agent, awesome-agent-skills, awesome-workflow-templates, unlazy) → reglas 30-33 + 7 skills v6.0. Detalle: `06_ESTADO_DEL_ARTE_V6.md`.
- **Task 122 (24-oct-2026)**: 15 repos de autonomía (AutoGPT, LangChain, MetaGPT…) → reglas 26-29 + §17. Detalle: `05_ESTADO_DEL_ARTE_V5.md`.
- **Task 126 (25-oct-2026)**: PRIMER RADAR SEMANAL DEL CICLO AUTÓMATA — 3 fuentes (GitHub trending oct-2026 vía curadurías Techninjaah/DataAIHub, changelog MCP spec 2026-07-28 en modelcontextprotocol.io, front page HN 23-oct). Hallazgos: (1) MCP 2026-07-28 = núcleo STATELESS (adiós initialize/sesiones; server/discover + headers Mcp-Method/Mcp-Name + MRTR + Tasks) — valida el diseño dual-era de mcp-compliance-2026 y el MCP de zolo-news; (2) el ecosistema dejó de construir "más agentes" y construye ALREDEDOR: memoria, routing de modelos (magpie 15.4k★), rails, dashboards; (3) herramientas locales se AUTO-EXPONEN como MCP (jub0t/Concat 8.6k★ con `concat --mcp`) — el patrón que zolo-news ya implementa; (4) browser agents sin screenshots (jev-ultrafast 23.2k★: elementos numerados, "estructura, no píxeles"). Drift detectado en propia superficie: llms.txt 68,388 vs API viva 71,198 (−2,810).
