---
name: equipo-virtual
description: Equipo virtual de roles con SOPs (v5.0, CrewAI roles + MetaGPT SOPs + orchestrator-workers). Activar en pipelines recurrentes multi-fase (investigación→construcción→auditoría→venta o similar), cuando una tarea grande tiene fases con dueños distintos, o cuando el usuario pide "atácalo como equipo". Cada rol es UNA manera de usar subagentes con SOP fijo y handoff de artefactos — no conversación libre.
---

# Equipo virtual — roles con SOP y handoff de artefactos (v5.0, M9)

Lección combinada de los repos: CrewAI probó que roles legibles aceleran la iteración; MetaGPT probó que los SOPs + handoffs de ARTEFACTOS estructurados rinden más que la conversación libre entre agentes (se adoptó esta versión — ver `05_ESTADO_DEL_ARTE_V5.md` §4.3); Anthropic lo formaliza como orchestrator-workers. El equipo NO es un chat entre agentes: es un orquestador (yo, ZOLO) que despacha workers con SOP fijo y pasa ARTEFACTOS entre fases.

## 1. Los 5 roles fijos de ZOLO

| Rol | SOP (qué hace siempre) | Artefacto de salida | Handoff a |
|---|---|---|---|
| **Orquestador** (YO, contexto principal) | prioriza (cola M4), despacha con contrato de 6 líneas, valida grader por fase, decide gates | PLAN.md + checkpoints §17 | — |
| **Investigador** | múltiples fuentes, subagente sin credenciales, spotlighting (regla 19), inventario con fuente por ítem | `download/research/<slug>.md` con tabla fuente/dato/fecha | Constructor o Comercial |
| **Constructor** | ejecuta el build (código/vector/skill/repo), scripts persistidos, grader determinista por paso | artefacto + grader verde | Auditor |
| **Auditor** | auto-auditoría estilo taiko-ai: bugs con severidad / violación de reglas / token-efficiency + replay del event log | `audit.md` publicado | Orquestador (gate G1) |
| **Comercial** | verificación viva de cifras (regla 25), personalización real del lead, 1 oferta + 1 CTA | pitch/email con evidencia | Orquestador (best-of-N si es irreversible) |

## 2. Contrato de despacho (se mantiene — regla 15)

Todo worker (rol o no) arranca con el contrato de 6 líneas (skill `subagentes-contrato`): contexto · objetivo · formato de salida · boundaries · presupuesto · worklog. El rol AÑADE el SOP de §1 al contrato; no lo reemplaza.

## 3. Handoff por artefacto (no por conversación)

La fase N entrega a la fase N+1: (a) el artefacto en su ruta canónica, (b) su grader verde, (c) 3 líneas de contexto esencial. PROHIBIDO pasar "todo lo que charlamos" — el receptor lee artefacto + 3 líneas, no el histórico (presupuesto de atención, regla 22; verificado: los handoffs conversacionales son los que más contexto queman).

## 4. Pipelines canónicos ya definidos

| Pipeline | Fases (rol → rol) |
|---|---|
| Lanzamiento agent-first (regla 23) | Investigador (rival/benchmark) → Constructor (repo <producto>-ai + 4 formatos) → Auditor (audit.md) → Orquestador (G1) → Comercial (listings) |
| Respuesta a comunidad crítica (E19) | Investigador (contexto del thread) → Constructor (artefacto pedido PRIMERO, regla 3) → Auditor → best-of-N (escéptico/promoter/compliance) → publish |
| Campaña de ventas (regla 25) | Investigador (leads con fuente) → Comercial (pitch con cifras vivas) → Auditor (guardarraíles §7/27) → Orquestador (G1 envío) |
| Incidente (§14.1) | Orquestador activa `runbook-incidentes` DIRECTO (no pipeline: el routing es el patrón correcto, skill `patrones-flujo` §2) |

## 5. Cuándo NO usar el equipo

- Tarea de 1 fase con grader claro → ejecución directa (anti-patrón "orquestación de adorno", skill `patrones-flujo` §6).
- Incidente en curso → runbook directo (routing), sin fases intermedias.
- El coste de 4 handoffs supera el valor del pipeline → workflow simple (regla 26).

## 6. Métricas del equipo (en el Stage Summary)

- Por fase: grader verde/rojo, acciones gastadas vs presupuesto.
- Por run: handoffs ejecutados, artefactos producidos, gates alcanzados.
- Meta: el pipeline repetido 2+ veces con la misma forma → se convierte en SKILL propia (regla 28 — el equipo también aprende).

## Grader (regla 28)

```bash
test_equipo-virtual() {
    # 1. Skill existe con frontmatter
    test -f 02_skills/equipo-virtual/SKILL.md
    # 2. Frontmatter tiene name y description
    grep -q "^name:" 02_skills/equipo-virtual/SKILL.md
    grep -q "^description:" 02_skills/equipo-virtual/SKILL.md
    # 3. Skill indexada en §12 del núcleo
    grep -q "equipo-virtual" 01_nucleo/ZOLO_V6.md
}
```
