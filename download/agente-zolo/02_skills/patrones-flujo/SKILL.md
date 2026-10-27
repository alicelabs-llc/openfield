---
name: patrones-flujo
description: Taxonomía de patrones de ejecución (v5.0, de Anthropic "Building Effective Agents" y los repos top de agentes). Activar al INICIAR cualquier tarea grande o multi-parte: clasificar si es workflow o agente, elegir el patrón más simple que resuelve la tarea y declararlo en 1 línea antes de ejecutar. Disparadores: tarea multi-etapa, "implementa X de punta a punta", pipeline recurrente, o duda entre planear más o ejecutar ya.
---

# Patrones de flujo — elegir la forma ANTES de ejecutar (v5.0, M1+M10+M12)

Principio Anthropic verificado en producción: **la simplicidad gana** — las implementaciones exitosas no usan la arquitectura más sofisticada, sino el patrón MÁS SIMPLE que resuelve la tarea. Cada salto de complejidad cuesta latencia, coste y probabilidad de error (regla 26).

## 1. Clasificación en 1 línea (obligatoria al abrir tarea grande)

```
¿El camino de la tarea es mapeable de antemano (pasos conocidos, pocos desvíos)?
  SÍ → WORKFLOW  (patrón explícito de §2)
  NO (ambigua, multi-horizonte, el descubrimiento ES parte del trabajo) → AGENTE con bucle presupuestado (regla 27 + skill bucle-autonomo)
```

Se declara en el plan: `PATRÓN: workflow·chaining | workflow·parallelization | agente·bucle` — y si a mitad de tarea el patrón elegido falla 2 veces (G3), se CAMBIA de patrón explícitamente, no se parchea.

## 2. Los 5 patrones de workflow (Anthropic, adoptados 1:1)

| Patrón | Cuándo | En ZOLO (ejemplos reales) |
|---|---|---|
| **1. Prompt chaining** | Tarea = secuencia fija de pasos, cada salida alimenta al siguiente | audit.md (releer diff → clasificar bugs → severidad) · vector de conformance (spec → vector → grader) |
| **2. Routing** | Entrada que se clasifica y va por rama especializada | tipo de incidente → runbook §2/3/4 · tipo de lead → oferta S1-S5 |
| **3. Parallelization** | Varios bloques independientes ejecutables a la vez (o voting) | 3 subagentes best-of-N (regla 20) · verificar 5 endpoints en paralelo · health checks |
| **4. Orchestrator-workers** | Una cabeza descompone y sintetiza; los workers ejecutan aislados | investigación pesada → subagentes con contrato (regla 15) · revisar N directorios MCP |
| **5. Evaluator-optimizer** | Loop generar→criticar→revisar para lo REVERSIBLE (≤2 iteraciones) | texto público no crítico, PRD, README, respuesta de comunidad sin riesgo de ban |

Para lo IRREVERSIBLE el loop es best-of-N (regla 20), no evaluator-optimizer: no se puede "revisar" un email ya enviado.

## 3. Criterio de salida por patrón (anti improvisación)

- Chaining: cada paso tiene criterio de salida verificable (grader determinista primero, regla 21) — si un paso no tiene grader, el patrón está mal elegido.
- Routing: las categorías y su destino están ESCRITAS antes de recibir la primera entrada.
- Parallelization: los bloques no comparten estado mutable entre sí; el merge tiene dueño (el orquestador).
- Orchestrator-workers: workers con contrato de 6 líneas (skill `subagentes-contrato`), salida pesada a archivo.
- Evaluator-optimizer: el CRÍTERIO de crítica se escribe antes de generar; máximo 2 iteraciones (si no pasa, escala o simplifica).

## 4. Cuándo SUBIR a agente (y no es renuncia de control)

Se justifica agente cuando: la tarea tiene ambigüedad real (el descubrimiento cambia el plan), el valor justifica el coste de exploración, y los errores son descubribles baratos (tests, curl, evals). En ese caso: skill `bucle-autonomo` (presupuesto + terminators + checkpoints, reglas 27 y §17).

## 5. Evaluator-optimizer barato — protocolo exacto (M10)

```markdown
1. GENERAR: versión 1 contra el plan real (no contra la idea vaga)
2. CRITICAR con criterio ESCRITO (misma checklist siempre): ¿afirmaciones sin evidencia? ¿cifra sin fecha? ¿parte ignorada? ¿CTA único?
3. REVISAR: aplicar solo las correcciones del criterio (sin reescribir por gusto)
4. Máx 2 loops. Si sigue fallando: el problema es el criterio o el plan — volver a §1
```

## 6. Anti-patrones (prohibidos)

- **Agente de adorno**: abrir un bucle autónomo para algo que era una secuencia de 3 comandos.
- **Workflow de adorno**: encadenar pasos formales para una pregunta que se responde con 1 tool call.
- **Patrón mudo**: ejecutar una tarea grande sin declarar el patrón (regla 26 — la declaración ES la verificación).
- **Cambio de patrón silencioso**: parchear dentro del patrón fallido en vez de declarar el cambio (G3).

## 7. Auditoría de contexto al activar (M12 — "think like your agent")

Antes de ejecutar con esta skill: ¿la ventana tiene (a) el objetivo con criterio de salida, (b) las herramientas disponibles y sus límites, (c) el criterio de crítica (§5) si el patrón lo exige? Lo que falte: traerlo ahora o persistirlo a archivo de sesión (skill `memoria-jerarquica`). El agente solo puede decidir con lo que hay en la ventana — nunca "lo sé de otra sesión".

## Grader (regla 28)

```bash
test_patrones-flujo() {
    # 1. Skill existe con frontmatter
    test -f 02_skills/patrones-flujo/SKILL.md
    # 2. Frontmatter tiene name y description
    grep -q "^name:" 02_skills/patrones-flujo/SKILL.md
    grep -q "^description:" 02_skills/patrones-flujo/SKILL.md
    # 3. Skill indexada en §12 del núcleo
    grep -q "patrones-flujo" 01_nucleo/ZOLO_V6.md
}
```
