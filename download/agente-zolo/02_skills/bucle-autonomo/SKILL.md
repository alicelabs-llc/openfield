---
name: bucle-autonomo
description: Run autónomo presupuestado (v5.0, lección de AutoGPT + durabilidad de LangGraph + cola de BabyAGI). Activar cuando la tarea es abierta o multi-horizonte ("vigila y mejora X", "investiga hasta encontrar Y", campañas, migraciones largas, o cualquier trabajo donde el plan cambia con lo que se descubre). Abre el run con presupuesto y terminators, mantiene cola de tareas priorizada, log de eventos por acción y checkpoints reanudables.
---

# Bucle autónomo — autonomía con presupuesto, cola y checkpoints (v5.0, M2+M3+M4+M5)

Lección verificada de los repos top: el bucle autónomo original de AutoGPT descarrilaba porque no tenía límites ni memoria de progreso; la industria lo resolvió con (1) presupuestos, (2) terminators, (3) checkpoints de estado, (4) colas de tareas. Esta skill es esa lección en protocolo markdown (regla 27 + §17 del núcleo).

## 1. Apertura de run (bloque OBLIGATORIO antes del primer paso)

```markdown
### RUN <slug> — <fecha America/Guayaquil>
PATRÓN: agente·bucle (por qué: <1 línea>)
OBJETIVO (T1): <criterio de salida verificable, no aspiración>
PRESUPUESTO: máx <N> acciones · <N> min · <N> subagentes
TERMINATORS: T1 objetivo con evidencia · T2 presupuesto agotado · T3 progreso nulo 3 iteraciones · T4 gate humano
GATES: <cuáles se prevén: G1 irreversible / G2 presupuesto / G3 divergencia 2x>
CHECKPOINT: <ruta del archivo que lleva el estado, p.ej. plans/RUN-<slug>.md>
```

Sin este bloque no hay run autónomo — solo trabajo normal paso a paso.

## 2. Cola de tareas priorizada (BabyAGI, M4)

Al abrir el run (y cada vez que se complete un ítem): reconstruir la cola desde §13 del núcleo + lo descubierto en el run:

1. **Listar** candidatos (pendientes canónicos + hallazgos del propio run).
2. **Priorizar** con el criterio del proyecto: 🔴 bloqueante → caja/impacto → desbloquea a otros → resto.
3. **Ejecutar UNA** y re-priorizar (la cola es viva: lo aprendido cambia el orden).
4. La cola vive en el checkpoint (§4), nunca solo en memoria.

## 3. Bucle del run (actuar → observar → reflexionar)

```
por cada ítem de la cola:
  1. ACTUAR: la acción más pequeña que produce evidencia (no la más ambiciosa)
  2. OBSERVAR: resultado programático (HTTP/exit/grep) → 1 línea al event log
  3. REFLEXIONAR: ¿avanza hacia T1? ¿dispara un terminator? ¿aparece un gate?
  4. CHECKPOINT si hubo cambio de fase, gate o cada ~10 acciones
```

Si el ítem requiere planear de nuevo 2 veces (G3): STOP → reiniciar-desde-el-plan (regla 18) → checkpoint antes de cambiar nada.

## 4. Checkpoint (formato §17 del núcleo) + event log (M5)

En el archivo del run:

```markdown
### CHECKPOINT <slug> — <fecha>
- OBJETIVO: <T1>
- HECHO: <qué quedó con evidencia> — reanudar DESDE AQUÍ
- SIGUIENTE: <próximo paso concreto>
- PRESUPUESTO: <restante>
- GATES PENDIENTES: <los que se alcanzaron y esperan>

### EVENT LOG (append-only)
[17:42] curl /api/health → 200 → drift no detectado
[17:44] push uta-ai → 422 → PAT sin scope repo — gate G2, escala
```

El event log es la respuesta al "¿qué hiciste?" sin releer transcripciones (patrón OpenHands).

## 5. Terminators — comportamiento exacto

| Terminator | Acción |
|---|---|
| **T1** objetivo con evidencia | VERIFY (evals/checklist §10) → CLOSE → commit alethech → reporte |
| **T2** presupuesto agotado | STOP INMEDIATO + checkpoint + reporte: hecho/pendiente/opciones. PROHIBIDO "una acción más" |
| **T3** progreso nulo ×3 | STOP + post-mortem (skill `reflexion-post-mortem`) + alternativa o escala |
| **T4** gate humano | checkpoint + pregunta CONCRETA con opciones (árbol §9) + lo que YA quedó hecho mientras tanto |

Reanudación de un run en sesión nueva: leer checkpoint → verificar evidencia de HECHO (no confiar) → continuar SIGUIENTE con el presupuesto RESTANTE declarado. Jamás re-planear desde cero sin leer el checkpoint (regla 27).

## 6. Anti-loops conocidos (del worklog v1-v4)

- Martillear una API que devuelve 401 sin cambiar la petición (correcto: credencial → G2).
- Re-leer el worklog completo en cada iteración (correcto: grep temático, regla 22).
- Subagente tras subagente para el mismo hallazgo (correcto: T3 → post-mortem → cambiar patrón, skill `patrones-flujo` §6).
## Grader (v6.0 — añadido por regla 32)

- Run abierto con presupuesto + 4 terminators declarados antes del primer paso → PASS.
- Terminator disparado → STOP + checkpoint de 5 campos + opciones → PASS. "Una iteración más" → FAIL grave.
- Reanudación multi-sesión desde checkpoint (jamás desde cero) → PASS.
