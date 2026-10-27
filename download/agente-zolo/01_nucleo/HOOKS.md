# HOOKS.md — Capa de enforcement markdown-native (regla 38, v7.0)

> 6 hooks ejecutados por el agente mismo en los límites del ciclo de vida.
> Inspirado en ECC hooks (6 tipos) + Obra SessionStart (re-inject post-compaction).
> **CRÍTICO**: PreCompact previene la falla más cara documentada por Obra/superpowers ("perdí mi lugar, re-despaché tareas completadas").

## Los 6 hooks

### 1. BOOT (SessionStart)
**Cuando**: arranque de sesión, después de compaction, después de clear.
**Ejecuta**:
1. Verificar `/tmp/my-project/` sobrevivió (regla 5)
2. `tail -150 worklog.md` + grep temático (regla 22 — BOOT interrogativo)
3. `alethech verify` fail-closed (regla 24) o declarar fallback worklog
4. Verificar credenciales (huella 4+4, regla 16)
5. `python3 scripts/zolo_auditar_skills.py` (E52 — debe salir verde)
6. Health checks: `/api/health`, `/api/skills`, `/uta/conformance`
7. Reportar estado en ≤10 líneas (America/Guayaquil)

### 2. PRE_TOOL (antes de herramienta irreversible)
**Cuando**: antes de deploy, push, publish, email, merge, cualquier acción fuera del entorno.
**Ejecuta**:
1. ¿Es irreversible? (regla 9 árbol de decisión)
2. Si irreversible → best-of-N con 3 subagentes (regla 20)
3. Si fuera del entorno → gate G3 §17 (divergencia del plan)
4. Si seguridad-sensible → gate G1 §17 (irreversible)
5. Declarar intención antes de ejecutar

### 3. POST_TOOL (después de cambio de estado)
**Cuando**: después de deploy/rollback, credencial viva/muerta, decisión, regla nueva, pendiente abierto/cerrado.
**Ejecuta**:
1. `alethech commit` estructurado (qué/cuándo/evidencia/pendientes) — regla 24
2. Ledger append si hubo error/corrección/insight — regla 31
3. Actualizar `06_aprendizaje/SKILL_REGISTRY.json` si se activó una skill

### 4. PRE_COMPACT (CRÍTICO — antes de compaction)
**Cuando**: el agente detecta que el contexto está creciendo (regla 22 — presupuesto de atención) o antes de que el sistema compacte.
**Ejecuta**:
1. Guardar estado completo a `06_aprendizaje/SESSION_STATE.md`:
   ```markdown
   # SESSION_STATE — <timestamp ISO>
   ## Task actual
   <Task ID + descripción + estado>
   ## Plan actual
   <PLAN.md path o resumen inline>
   ## TODO actual
   <lista numerada con estado>
   ## Checkpoint actual
   <§17 checkpoint de 5 campos>
   ## Presupuesto restante
   <acciones/tiempo/subagentes>
   ## Últimas 3 entradas de worklog
   <extracto>
   ## Skills activadas esta sesión
   <lista>
   ```
2. **Después de compaction**: re-leer `SESSION_STATE.md` PRIMERO antes de cualquier otra cosa.
3. Si SESSION_STATE.md no existe → declarar "arranque ciego" y ejecutar BOOT completo.

### 5. STOP (cierre de tarea)
**Cuando**: tarea declarada "hecha" o terminator disparado (T1-T4, regla 27).
**Ejecuta**:
1. §10 checklist completo (evidencia, health checks, worklog append, estado_sitio.json, pendientes con dueño, cero secretos)
2. §18 cadencia EN CALIENTE: capturar rulings/learnings al ledger (regla 31)
3. Si fallo verificado propio → post-mortem de 4 campos ANTES de corregir (regla 29)
4. Si éxito 2+ veces → proponer skill nueva (regla 28)

### 6. SESSION_END (cierre de sesión)
**Cuando**: fin de sesión (usuario se va, reset inminente, cierre voluntario).
**Ejecuta**:
1. §18 cadencia DIARIA: post-mortems cerrados, ledger completo, worklog append final
2. `alethech commit` de cierre (regla 24 — sin commit, próximo BOOT arranca ciego)
3. `alethech export --output memory.aleth` si cambió dispositivo o hay riesgo
4. Checkpoint emitido (alethech no detecta rollback sin checkpoint externo)
5. Actualizar `06_aprendizaje/SKILL_REGISTRY.json` con métricas finales de la sesión

## Implementación

Los hooks NO son procesos externos — son **momentos del ciclo de vida** que el agente ejecuta como parte de su protocolo. El agente debe:

1. **Reconocer** cuándo está en un límite de hook (BOOT, antes de irreversible, después de cambio de estado, antes de compaction, cierre de tarea, cierre de sesión)
2. **Ejecutar** los pasos del hook correspondiente
3. **Declarar** "HOOK <nombre> ejecutado" en el worklog

## Anti-patrón

❌ Saltarse hooks porque "ya lo sé" o "es obvio"
❌ Ejecutar hooks parcialmente ("solo el paso 1")
❌ No guardar SESSION_STATE.md antes de compaction ("ya está en el worklog")

## Evals relacionados

- E61: BOOT ejecuta los 7 pasos
- E62: PRE_TOOL dispara best-of-N en irreversible
- E63: POST_TOOL hace commit estructurado
- E64: PRE_COMPACT guarda SESSION_STATE.md completo
- E65: SESSION_END hace commit de cierre + checkpoint
