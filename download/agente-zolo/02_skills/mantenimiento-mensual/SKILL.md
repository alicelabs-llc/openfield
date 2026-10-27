---
name: mantenimiento-mensual
description: Rutinas de mantenimiento del agente y del proyecto. Activar el primer BOOT de cada mes, en días sin tareas de usuario (sleep-time), o cuando el usuario pida "mantenimiento", "limpieza", "auditoría del agente", "vigilancia de mercado".
---

# Mantenimiento mensual + sleep-time + vigilancia de mercado (v3.0)

## 1. Compaction del worklog (primer BOOT del mes)
1. Archivar los Tasks de hace >60 días a `worklog-archive-YYYY-MM.md` (append-only).
2. En el worklog vivo dejar: índice de Task IDs archivados (1 línea cada uno) + los últimos ~30 tasks íntegros.
3. El worklog debe caber completo en contexto, siempre. Medir: `wc -c worklog.md` — si >60KB, compactar más agresivo.

## 2. Reporte mensual (al terminar la compaction)
- Tareas completadas (YO) vs entregadas como borrador (TÚ) — el ratio es el KPI de la misión.
- Acciones anti-ban gastadas por cuenta; incidentes del mes (con causa raíz); reglas nuevas nacidas (§15).
- Evals: cuáles se ejecutaron, resultado. Cualquier E fallido = regresión → arreglar definición.

## 3. Sleep-time compute (días sin tareas de usuario — Letta sleep-time-compute)
Mantenimiento de fondo, en orden de valor:
1. Dedup de reglas de oro (¿hay reglas que se solapan? fusionar, nunca borrar historia sin CHANGELOG).
2. Refrescar §5 contexto canónico con los datos vivos del mes (cifras, hilos, contactos).
3. Correr 2-3 evals aleatorios de la suite de regresión (EVALS.md).
4. Refresh de `estado_sitio.json` + revisión de pendientes con fecha próxima (＜30 días).

## 4. Vigilancia de mercado (trimestral — protocolo de esta misma sesión, Tasks 117-a/b/c)
El mercado de agentes evoluciona rápido (oct-2025: skills GA; dic-2025: AAIF; jul-2026: MCP stateless). Cada trimestre:
1. Lanzar subagentes con el contrato (skill subagentes-contrato) sobre: (a) cambios de spec MCP en modelcontextprotocol.io changelog, (b) novedades Anthropic/Cursor/OpenAI en ingeniería de agentes, (c) estándares agentskills.io / agents.md.
2. Solo fuentes primarias verificadas (leer la página, no el agregador).
3. Producir: "¿qué patrón nuevo es portable a protocolo markdown?" → si hay, PROTOCOLO §15 completo (regla → CHANGELOG → eval).
4. Revisar skills.sh Audits (Trust Hub/Socket/Snyk): nuevos riesgos reportados en skills de la categoría MCP — insumo para los certificados Sentinel.

## 5. Higiene de la propia definición (cada mantenimiento)
- ¿Hay reglas muertas (nunca disparadas en 3 meses)? Marcar para revisión, no borrar sin evidencia.
- ¿El índice de skills sigue siendo exacto? Actualizar descriptions con las keywords que disparan bien/mal en la práctica.
- Backup versionado de la definición antes de cualquier cambio (regla 22, deltas).
## Grader (v6.0 — añadido por regla 32)

- Primer BOOT del mes → mantenimiento ejecutado (cifras vivas, skills sin uso, mercado, linter de memoria) → PASS.
- Reporte mensual en worklog con tareas YO vs TÚ, incidentes, reglas/evals nuevos → PASS.
- Cifra publicada sin fecha+fuente → FAIL (regla de oro).
