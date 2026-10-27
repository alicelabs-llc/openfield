---
name: ciclo-hooks
description: >-
  6 hooks markdown-native ejecutados en límites del ciclo de vida. Use when arrancar
  sesión, antes de acción irreversible, después de cambio de estado, antes de compaction,
  cierre de tarea, cierre de sesión.
trigger: >-
  arranque de sesión, antes de deploy/push/publish/email, después de cambio de estado,
  contexto creciendo (pre-compaction), tarea declarada "hecha", fin de sesión.
---

# Skill: Ciclo de Hooks (markdown-native)

> **Origen**: ECC hooks 6-tipos + Obra SessionStart. Regla 38 v7.0.
> **CRÍTICO**: PreCompact previene la falla más cara ("perdí mi lugar, re-despaché tareas completadas").

## Los 6 hooks

1. **BOOT** → §1 completo (worklog + alethech + creds + audit + health)
2. **PRE_TOOL** → antes de irreversible (best-of-N + árbol decisión)
3. **POST_TOOL** → después de cambio estado (commit + ledger)
4. **PRE_COMPACT** → guardar SESSION_STATE.md (task/plan/todo/checkpoint/presupuesto)
5. **STOP** → §10 checklist + §18 en caliente
6. **SESSION_END** → §18 diaria + commit de cierre + checkpoint

Detalle completo: `01_nucleo/HOOKS.md`

## Grader
```bash
test_ciclo_hooks() {
    # 1. SESSION_STATE.md existe (PreCompact ejecutado)
    test -f 06_aprendizaje/SESSION_STATE.md
    # 2. HOOKS.md existe
    test -f 01_nucleo/HOOKS.md
    # 3. Worklog tiene "HOOK" entries
    grep -c "HOOK" worklog.md
}
```
