---
name: evaluador-skills
description: >-
  Eval harness por skill con baseline RED/GREEN. Use when crear o modificar una skill —
  mide si la skill realmente mejora el comportamiento del agente vs no tenerla.
trigger: >-
  skill nueva creada, skill existente modificada, "evalúa esta skill", "mide si funciona",
  regla 37 activada, ciclo MENSUAL §18 de skills.
---

# Skill: Evaluador de Skills (RED/GREEN baseline)

> **Origen**: Anthropic skill-creator + Obra writing-skills (TDD for skills). Regla 37 v7.0.

## Cuándo activar
- Skill nueva creada (regla 28)
- Skill existente modificada (cambio de frontmatter o body)
- Cadencia MENSUAL §18 (auditar skills con baja confianza)
- Orden explícita: "evalúa esta skill", "mide si funciona"

## Proceso (5 fases)

### 1. RED — Baseline sin skill
- Ejecutar subagente SIN la skill en 2-3 escenarios de presión
- Documentar racionalizaciones exactas: ¿qué hace el agente sin la skill?
- **Si el agente NO falla sin la skill → la skill enseña lo equivocado**

### 2. GREEN — Con skill vs baseline (mismo turno)
- Spawn con-skill Y baseline EN EL MISMO turno (no secuencial)
- Capturar: total_tokens, duration_ms de cada run
- Workspace: `06_aprendizaje/evals/<skill>/iteration-N/eval-X/{with_skill,without_skill}/`

### 3. Grader (determinista primero)
- Verificar evidencia REAL (no cumplimiento superficial)
- PASS solo si el output refleja completitud genuina
- **Crítica de evals**: una assertion que pasa para output claramente equivocado = peor que inútil

### 4. Analyzer (ciego A/B)
- Comparación post-hoc sin saber cuál es con-skill
- Score 1-10 en instruction-following
- Identificar fortalezas del ganador + debilidades del perdedor

### 5. Iteración
- 60% train / 40% test split
- Seleccionar por TEST score (no train — evitar overfitting)
- Máx 5 iteraciones
- Objetivo: ≥80% en test set

## Grader
```bash
test_evaluador_skill() {
    # 1. RED baseline existe
    ls 06_aprendizaje/evals/<skill>/iteration-1/eval-0/without_skill/outputs/
    # 2. GREEN con-skill existe
    ls 06_aprendizaje/evals/<skill>/iteration-1/eval-0/with_skill/outputs/
    # 3. grading.json con scores
    test -f 06_aprendizaje/evals/<skill>/iteration-1/benchmark.json
    # 4. Test score ≥80%
    jq '.test_score' benchmark.json | grep -E '0\.[8-9]|1\.0'
}
```
