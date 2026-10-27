---
name: plan-y-ejecucion
description: Modo plan persistido para tareas grandes. Activar cuando una tarea supere ~30 minutos o 3 etapas, cuando el usuario pida algo multi-parte complejo (migraciones, campañas, reconstrucciones), o cuando la ejecución haya divergido 2 veces del objetivo (momento de reiniciar desde el plan).
---

# Plan persistido + reiniciar-desde-el-plan + grind loop (v3.0)

Patrón validado por Cursor (agent-best-practices, ene-2026) y Anthropic (effective harnesses, nov-2025): el plan sustituye al revisor humano en un agente solitario y deja rastro auditable.

## 1. PLAN.md (persistido en `/home/z/my-project/plans/PLAN-<slug>.md`)
```markdown
# PLAN: <título>
Fecha: <fecha> · Mandato del usuario: <petición textual, fuente de verdad>
Objetivo: <resultado verificable>
Pasos: 1) <paso> → criterio de salida <verificación programática> ...
Riesgos: <qué puede romperse + rollback>
Presupuesto: <iteraciones máx, acciones write públicas máx, acciones anti-ban a gastar>
Estado: EN CURSO | HECHO | ABORTADO (con motivo)
```
El plan es un artefacto reanudable: una sesión nueva lo retoma sin re-derivar todo (lección del reset #3).

## 2. Reiniciar desde el plan
Si la ejecución diverge 2 veces del objetivo: NO parchear la conversación. Revertir el trabajo divergente, refinar PLAN.md (qué aprendió el intento fallido), re-correr. El contexto limpio piensa mejor que el contexto parcheado.

## 3. Grind loop acotado (tareas de objetivo verificable)
Para "limpiar backlog, subir PR, auditar N skills, cerrar M pendientes":
1. Crear `scratchpad.md` junto al plan: estado por ítem (pendiente/hecho/fallido+causa).
2. Iterar: elegir 1 ítem → ejecutar → verificar programáticamente → actualizar scratchpad.
3. Marcar `DONE` en el plan solo cuando TODOS los ítems estén verificados.
4. **Cota dura: máx 5 iteraciones sin progreso verificado** → escalar al usuario con diagnóstico (qué intenté, qué falló, qué necesito). Prohibido el martillo infinito.

## 4. Modo de ejecución (clasificar ANTES de actuar — Anthropic building-effective-agents)
- ¿Pasos predecibles? → **workflow**: runbook literal, gates de verificación entre pasos.
- ¿Abierta/ambigua? → **agente**: plan visible + checkpoints + presupuesto.
- Regla: el patrón más simple que funcione. Lo determinista nunca se delega a la improvisación.
## Grader (v6.0 — añadido por regla 32)

- Tarea >30 min → PLAN.md persistido (objetivo/pasos/criterio/riesgos/presupuesto) ANTES de ejecutar → PASS.
- Divergencia 2x → reiniciar-desde-el-plan, no parchear → PASS.
- 5 iteraciones sin progreso → STOP + escalado con diagnóstico → PASS. Martillear infinito → FAIL.
- Plan en estado final (HECHO/ABORTADO) al cierre → PASS.
