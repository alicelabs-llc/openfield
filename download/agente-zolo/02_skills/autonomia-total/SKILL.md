---
name: autonomia-total
description: >-
  Superpoder de autonomía total con guardarraíles. Use when tarea abierta sin
  intervención humana posible, producción continua, "hazlo todo", "no preguntes".
trigger: >-
  "hazlo todo", "no preguntes", "automático", "autónomo", "sin intervención",
  tarea >1h sin gate humano, regla 40 activada, founder se va.
---

# Skill: Autonomía Total (superpoder)

> **Origen**: regla 40 v7.0. Combina: bucle-autonomo (presupuesto + terminators) +
> flota-produccion (delegación paralela) + autoinstalador-skills (auto-capacidad) +
> ledger-autoaprendizaje (auto-mejora) + ciclo-hooks (enforcement).

## Qué hace

El agente opera SIN intervención humana por tiempo indefinido, con guardarraíles:

1. **Cola §13** → toma el próximo pendiente priorizado
2. **Ejecuta** → aplica skills relevantes, despacha subagentes si ≥2 piezas
3. **Verifica** → §10 checklist + grader determinista
4. **Aprende** → captura en ledger (regla 31)
5. **Mejora** → si lección repetida 2+, promueve a skill/regla/eval
6. **Produce** → si sin pendientes, produce para la misión (regla 25)
7. **Repite** → vuelve al paso 1

## Guardarraíles (lo que SÍ puede hacer solo)

✅ Escribir código, tests, docs
✅ Ejecutar tests localmente
✅ Hacer commits en worklog append-only
✅ Capturar learnings en ledger
✅ Crear skills nuevas (regla 28)
✅ Despachar subagentes para piezas independientes
✅ Optimizar descriptions de skills (regla 39)
✅ Ejecutar curador de skills (regla 36)
✅ Generar playbooks de consolidación (regla 35)
✅ Auditar repos externos para extraer patrones

## Guardarraíles (lo que NUNCA hace solo — gate G1 §17)

❌ Deploy a producción
❌ Push a git remoto
❌ Enviar emails
❌ Publicar en redes sociales
❌ Comprar/vender
❌ Borrar datos irreversiblemente
❌ Modificar credenciales
❌ Aceptar términos legales

## Terminators (cuando se detiene solo)

- **T1**: objetivo alcanzado (verificable)
- **T2**: presupuesto agotado (acciones/tiempo/subagentes)
- **T3**: progreso nulo ×3 iteraciones
- **T4**: gate humano requerido (irreversible, seguridad, fuera del entorno, plan roto)

Al dispararse: STOP + checkpoint de 5 campos + opciones (no "una iteración más").

## Modos de activación

1. **Explícita**: founder dice "hazlo todo" / "no preguntes" / "autónomo"
2. **Implícita**: founder se va (sin actividad >30 min en chat)
3. **Programada**: cron job / daemon (ver `scripts/zolo_daemon.sh`)
4. **Cadencia**: §18 SEMANAL/MENSUAL sin tarea del founder

## Grader

```bash
test_autonomia_total() {
    # 1. Cola §13 existe y tiene pendientes
    grep -c "^- 🔴\|^- 🟡" worklog.md  # > 0
    # 2. Ledger actualizado (regla 31)
    test -f 06_aprendizaje/LEARNINGS.md
    # 3. No hay acciones irreversibles sin gate
    grep -c "G1\|gate humano" worklog.md  # evidencia de gates
    # 4. Terminators documentados
    grep -c "T1\|T2\|T3\|T4" worklog.md
}
```
