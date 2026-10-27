---
name: supervisor-meta
description: >-
  Supervisor meta-cognitivo que monitorea al agente y redirige cuando está stalled.
  Use when bucle autónomo sin progreso, agente repite mismo error, contexto degradado.
trigger: >-
  T3 progreso nulo ×3, mismo error repetido, contexto >50k tokens, "estás atascado",
  "no avanzas", regla 41 activada.
---

# Skill: Supervisor Meta (superpoder)

> **Origen**: NVIDIA AVO (100% ARC-AGI-3) — "supervisor that redirects a stalled agent".
> Regla 41 v7.0.

## Qué hace

El supervisor es una capa meta-cognitiva que MONITOREA al agente principal y
INTERVIENE cuando detecta patrones de estancamiento:

### Detección de stall (6 patrones)

1. **Loop de herramientas**: mismo tool call 3+ veces sin cambio de output
2. **Error repetido**: mismo error capturado 2+ veces en ledger (regla 31)
3. **Contexto saturado**: >50k tokens consumidos sin checkpoint
4. **Progreso nulo**: T3 disparado (3 iteraciones sin progreso verificable)
5. **Divergencia**: plan actual difiere 2x del original
6. **Racionalización**: agent justifica no ejecutar en vez de ejecutar

### Intervenciones (escaladas)

1. **GENTLE**: "Detecté que repetiste X. ¿Hay un enfoque diferente?"
2. **REDIRECT**: "Pausa. Resume el objetivo. Verifica el estado del mundo. Cambia enfoque."
3. **COMPACT**: "Contexto saturado. Ejecuta PRE_COMPACT hook. Re-leer SESSION_STATE.md."
4. **ESCALATE**: "Esto necesita gate humano. STOP + checkpoint + reportar al founder."
5. **RESET**: "Plan roto. Volver al último checkpoint. Refinar el plan. Reiniciar."

### Implementación markdown-native

El supervisor es el AGENTE MISMO en modo meta-cognitivo, no un agente separado:
- Antes de cada acción: revisar si patrón de stall detectado
- Si detectado: ejecutar intervención escalada correspondiente
- Registrar intervención en worklog: `### SUPERVISOR <timestamp> — <patrón> — <intervención>`

## Grader

```bash
test_supervisor_meta() {
    # 1. Worklog tiene entradas de supervisor
    grep -c "SUPERVISOR" worklog.md
    # 2. Intervenciones documentadas con patrón
    grep -E "loop|error repetido|contexto saturado|progreso nulo|divergencia" worklog.md
    # 3. No más de 3 loops del mismo tool
    # (verificación dinámica — el supervisor previene esto)
}
```
