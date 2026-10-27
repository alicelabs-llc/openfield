---
name: optimizador-descripciones
description: >-
  Optimización de skill descriptions con loop medible anti-undertriggering. Use when
  skill no se activa cuando debería, description parece débil, ciclo MENSUAL §18.
trigger: >-
  skill undertriggerea, "mejora la description", "por qué no se activa X skill",
  nueva skill creada, regla 39 activada.
---

# Skill: Optimizador de Descripciones

> **Origen**: Anthropic improve_description.py. Regla 39 v7.0.
> **Filosofía**: Claude undertriggerea skills por defecto — las descriptions deben ser "pushy".

## Proceso

1. **Generar 20 trigger eval queries**:
   - 8-10 should-trigger (diferentes frasing del mismo intent)
   - 8-10 should-not-trigger NEAR-MISS (comparten keywords pero necesitan otra cosa)

2. **Split 60/40**: 12 train / 8 test

3. **3x runs** por query para reliable trigger rate

4. **Iterar hasta 80%** en TEST set (no train — evitar overfitting), máx 5 iteraciones

5. **Anti-undertriggering**: enumerar condiciones de disparo explícitamente, incluso
   cuando el usuario no nombra la skill. Toda info "cuándo usar" va en description.

6. **Cap**: ≤80 chars en description

## Grader
```bash
test_optimizador_descripciones() {
    # 1. 20 queries existen
    ls 06_aprendizaje/evals/<skill>/trigger_queries/ | wc -l  # >= 20
    # 2. Test score ≥80%
    jq '.test_score' 06_aprendizaje/evals/<skill>/benchmark.json | grep -E '0\.[8-9]|1\.0'
    # 3. Description ≤80 chars
    jq -r '.description' 02_skills/<skill>/SKILL.md | wc -c  # <= 81 (80+newline)
}
```
