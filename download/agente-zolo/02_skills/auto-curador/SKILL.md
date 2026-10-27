---
name: auto-curador
description: >-
  Auto-curación continua: el agente se diagnostica, se repara y se mejora a sí
  mismo sin intervención humana. Use when detectar gaps, mejorar skills, optimizar
  descriptions, archivar skills stale, regla 42 activada.
trigger: >-
  cadencia SEMANAL §18, "mejórate", "auto-curación", "diagnóstico", skill con
  confidence < 0.5, description sin optimizar, regla 42 activada.
---

# Skill: Auto-Curador (superpoder)

> **Origen**: regla 42 v7.0. Combina: curador (regla 36) + evaluador (regla 37) +
> optimizador (regla 39) + sueno-consolidacion (regla 35) + supervisor-meta (regla 41).

## Qué hace

El agente se diagnostica, se repara y se mejora a sí mismo en un ciclo continuo:

### Ciclo de auto-curación (5 fases)

#### 1. DIAGNÓSTICO — detectar gaps
- `python3 scripts/zolo_auditar_skills.py` → skills con issues
- `python3 scripts/zolo_curador_skills.py --report` → skills stale/archived
- `grep "LECCIÓN:" 06_aprendizaje/LEARNINGS.md` → lecciones no promovidas
- `grep "PATRÓN NUEVO:" worklog.md` → patrones detectados sin acción
- Revisar SESSION_STATE.md → drift detectado

#### 2. REPARACIÓN — aplicar fixes
- Skills con grader faltante → añadir grader determinista
- Skills stale → archivar (regla 36, NUNCA borrar)
- Skills con description débil → optimizar (regla 39)
- Lecciones repetidas 2+ → promover a regla (§15) o skill (regla 28)
- Drift detectado → investigar y reportar

#### 3. EVALUACIÓN — medir mejora
- `python3 scripts/zolo_evaluar_skill.py <skill>` → eval con baseline
- Comparar test score antes/después de la reparación
- Si mejora <10% → rollback + intentar enfoque diferente

#### 4. CONSOLIDACIÓN — escribir playbooks
- Patrones repetidos → playbook PB-<NNN> en `06_aprendizaje/playbooks/`
- Heurísticas portables → propuesta de regla nueva
- Evidencia grep-able con fechas + task IDs

#### 5. PROMOCIÓN — proponer al founder (gate G1)
- Reglas nuevas → backup + delta quirúrgico en núcleo
- Skills nuevas → frontmatter + grader + índice §12
- Evals nuevos → EVALS.md append
- TODO con gate G1 explícito: "pendiente aprobación founder"

## Cuándo se activa

1. **Cadencia SEMANAL §18** — cada semana ejecuta el ciclo completo
2. **Tras 5+ tasks cerrados** — auto-curación intermedia
3. **Orden explícita**: "mejórate", "auto-curación", "diagnóstico"
4. **Detección de degrade**: auditor rojo, eval fallido, skill sin uso 30+ días

## Anti-patrón

❌ Auto-curación que rompe algo que funcionaba (siempre backup antes — regla 22)
❌ Promover lección a regla sin 2+ ocurrencias (regla 28)
❌ Cambiar núcleo sin gate G1 del founder (§17)
❌ Archivar skill pinned (regla 36 exenta pinned)

## Grader

```bash
test_auto_curador() {
    # 1. Auditoría verde tras auto-curación
    python3 scripts/zolo_auditar_skills.py  # exit 0
    # 2. No hay skills con confidence < 0.5 sin justificación
    jq '.skills | to_entries[] | select(.value.confidence < 0.5)' 06_aprendizaje/SKILL_REGISTRY.json
    # 3. Playbooks generados
    ls 06_aprendizaje/playbooks/PB-*.md | wc -l  # > 0
    # 4. Worklog tiene entrada de auto-curación
    grep "AUTO-CURACIÓN" worklog.md
}
```
