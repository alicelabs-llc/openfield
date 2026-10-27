---
name: tareas-largas
description: Harness para tareas multi-sesión. Activar en migraciones, campañas multi-plataforma, reconstrucciones post-reset, o cualquier trabajo que no cabe en una sesión. Patrón initializer + progress file (Anthropic effective-harnesses, nov-2025).
---

# Tareas largas: feature list inmutable + sesiones limpias (v3.0)

## Sesión 0 — Initializer (una sola vez)
1. Crear `/home/z/my-project/plans/PENDIENTES-<slug>.json`:
```json
{
  "proyecto": "<slug>",
  "creado": "<fecha>",
  "items": [
    {"id": 1, "tarea": "<descripción>", "criterio_salida": "<verificación programática>", "passes": false, "nota": ""}
  ]
}
```
2. Regla de inmutabilidad: los ítems NUNCA se borran ni reordenan — solo se actualiza `passes` y `nota`. (JSON en vez de markdown: el modelo lo altera menos — lección Anthropic.)
3. Commit inicial si aplica (el estado del mundo queda fijado).

## Cada sesión siguiente — ciclo
1. Leer el JSON + la última entrada del worklog del proyecto.
2. Elegir UN ítem `passes: false`.
3. Ejecutarlo → verificar con su criterio programático (exit code / grep / HTTP 200).
4. Dejar estado LIMPIO: commit si aplica + `nota` con lo hecho + worklog append (Task ID del día).
5. Marcar `passes: true` SOLO tras la verificación. Prohibido marcar en optimismo.

## Reglas de sesión limpia
- Fin de sesión = estado mergeable/reanudable (otra sesión nueva debe poder continuar sin preguntas).
- Si un íitem está bloqueado >2 sesiones: escalar al usuario con diagnóstico (no acumular bloqueos en silencio).
- Al cerrar el proyecto entero: reporte final con los N ítems verificados + evidencia, y commit de memoria alethech.

## Relación con otros protocolos
- PLAN.md (skill plan-y-ejecucion) para la estrategia; PENDIENTES.json para el estado ejecutable.
- Grind loop acotado (máx 5 iteraciones sin progreso) aplica también aquí.
- El worklog episódico registra EL TRABAJO; el JSON registra EL ESTADO. No duplicar uno en el otro.
## Grader (v6.0 — añadido por regla 32)

- Trabajo multi-sesión reanudado desde checkpoint/worklog (no desde cero) → PASS.
- Cierre de sesión con commit de memoria + checkpoint → PASS. Sesión cerrada sin estado → FAIL.
- Progreso declarado sin evidencia → FAIL.
