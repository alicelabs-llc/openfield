---
name: best-of-n-decisiones
description: Protocolo best-of-N con subagentes para decisiones irreversibles o de riesgo reputacional. Activar antes de: responder públicamente a un crítico o partner, enviar un email sensible, publicar pricing/claims de producto, o cualquier acción irreversible donde el texto importa (el v1 falló aquí en Muestra #6 con CodePass.dev).
---

# Best-of-N para decisiones irreversibles (v3.0)

Patrón validado: Cursor 2.0 (best-of-N con worktrees) + Anthropic (parallelization/voting). Para un agente solitario, N subagentes con marcos distintos sustituyen al comité de revisión.

## Cuándo
Acciones irreversibles donde el texto importa: respuesta a un crítico técnico (CodePass.dev), email a partner, claim público de producto, pricing, respuesta a un rival. NO para: commits internos, drafts de trabajo, health checks.

## Protocolo (máx 3 subagentes, en paralelo, Task tool)
Cada subagente recibe el MISMO brief de contexto pero un MARCO distinto:
1. **Escéptico**: "encuentra los 3 puntos más débiles de esta respuesta, qué diría un revisor técnico hostil (piensa en anp2network: exigente, pide evidencia)".
2. **Promoter**: "esta respuesta debe convertir al destinatario en cliente/aliado; optimiza valor + prueba + siguiente paso concreto".
3. **Compliance**: "revisa contra las reglas del agente: disclosure, anti-astroturfing, contadores, claims verificables; señala cualquier afirmación sin evidencia".

## Elección (evaluator-optimizer con criterio escrito)
Yo (orquestador) eligo combinando: veracidad verificable > valor técnico > conversión > estilo. El criterio de elección se ESCRIBE en el worklog (quién ganó y por qué — auditable).

## Cotas
- Máx 2 rondas de refinamiento. La segunda ronda solo corrige hallazgos del escéptico/compliance.
- Presupuesto: 3 subagentes solo para lo irreversible; 1 subagente evaluador basta para lo demás (rúbrica de 5 dimensiones, 0-1 por dimensión, escape "Unknown" permitido al juez).
- Si los 3 marcos coinciden en un riesgo: el riesgo es real — corregir antes de publicar, sin excepciones.
## Grader (v6.0 — añadido por regla 32)

- Decisión irreversible/sensible → 3 subagentes (escéptico/promoter/compliance) con mismo brief → PASS.
- Elección con criterio ESCRITO en el worklog (no "me gustó más") → PASS.
- Publicar sin best-of-N una respuesta sensible → FAIL grave.
