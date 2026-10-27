# Estado del Arte v7.0 — Auditoría de 5 repos (25-oct-2026)

> **Mejoras M22-M30**: extraídas de 5 repos top del ecosistema oct-2026 (ECC 288k★, Hermes 257k★, Obra/superpowers 304k★, Anthropic/skills 184k★, Awesome-Agent-Memory). Auditoría completa en subagent Task 126.

## Mejoras adoptadas (P1-P4, todas HIGH)

### M22 — Skill lifecycle metrics + archive + pin (P1)
- **Origen**: Hermes `agent/curator.py` + ECC `continuous-learning-v2`
- **Mejora**: `06_aprendizaje/SKILL_REGISTRY.json` con use_count/view_count/patch_count + stale_after_days=30 + archive_after_days=60 (NEVER delete) + pinned skills exempt
- **Script**: `scripts/zolo_curador_skills.py`
- **Regla nueva**: 36

### M23 — Per-skill eval harness con baseline + grader/analyzer (P2)
- **Origen**: Anthropic `skill-creator` + Obra `writing-skills` (TDD for skills)
- **Mejora**: skill nueva `evaluador-skills` — RED baseline (subagent sin skill) → GREEN (con skill) → grader/analyzer con roles separados → iteración 5x con train/test split
- **Script**: `scripts/zolo_evaluar_skill.py`
- **Regla nueva**: 37
- **Evals nuevos**: E56-E60

### M24 — Hook layer markdown-native (P3 — CRÍTICO)
- **Origen**: ECC hooks (6 tipos) + Obra SessionStart hook (re-inject después compaction)
- **Mejora**: `01_nucleo/HOOKS.md` — 6 hooks ejecutados por el agente mismo: BOOT, PRE_TOOL, POST_TOOL, **PRE_COMPACT** (crítico: guarda estado antes de compaction), STOP, SESSION_END
- **Skill nueva**: `ciclo-hooks`
- **Regla nueva**: 38
- **Evals nuevos**: E61-E65

### M25 — Description optimization loop + anti-undertriggering (P4)
- **Origen**: Anthropic `improve_description.py` (20 trigger evals, 60/40 split, 5 iteraciones)
- **Mejora**: skill `optimizador-descripciones` — 20 trigger queries por skill (8-10 should-trigger + 8-10 near-miss should-not-trigger), 3x runs cada una, iteración hasta 80% precision en test set
- **Script**: `scripts/zolo_optimizar_descripcion.py`
- **Regla nueva**: 39
- **Evals nuevos**: E66-E70

## Mejoras diferidas (MED, para v7.1)

### M26 — Project-scoped memory tiers + decay (P5)
- **Origen**: ECC unified-memory 3 scopes + PowerMem Ebbinghaus decay
- **Diferido**: toca el contrato alethech v0.9.1 → requiere release v0.10.0 primero

### M27 — "Explain the why" writing philosophy
- **Origen**: Anthropic skill-creator "ALWAYS/NEVER is a yellow flag"
- **Diferido**: refactor completo del núcleo (high effort, degradación temporal del contexto)

### M28 — Memory benchmarks (LOCOMO, MemBench)
- **Origen**: Awesome-Agent-Memory benchmarks section
- **Diferido**: no crítico para operación

### M29 — Footprint ladder (extend → CLI+skill → service → plugin → MCP → core tool)
- **Origen**: Hermes AGENTS.md
- **Diferido**: framework decisional, no protocolo markdown

### M30 — Brainstorming gate before building
- **Origen**: Obra brainstorming skill
- **Diferido**: regla 1 ya cubre respuesta primero para preguntas directas

## Confirmaciones (ZOLO ya está al nivel del estado del arte)

| Área | ZOLO v6.1 | Veredicto auditoría |
|------|-----------|---------------------|
| Memoria integrity | alethech Ed25519 + bi-temporal supersede + fail-closed | ✓ al nivel (ECC unified-memory usa mismo patrón) |
| Self-improvement cadence | §18 4-cadencia | ✓ al nivel (Hermes curator + Anthropic dreaming ya adoptados) |
| Skill fabrication | regla 28 (2x success → skill) | ⚠ base buena pero sin baseline measurement (M23 corrige) |
| Multi-agent | regla 30 flota + rulings-not-stalls | ✓ CANÓNICO (Obra SDD es la fuente, ZOLO ya adoptó) |
| Evals philosophy | regla 21 deterministic grader first | ✓ al nivel (Anthropic grader.md coincide) |
| State machine | §17 con 3 gates HITL | ✓ al nivel (Hermes tiene scheduler similar) |
