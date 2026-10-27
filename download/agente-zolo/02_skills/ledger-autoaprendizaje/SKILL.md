---
name: ledger-autoaprendizaje
description: Captura de aprendizaje EN CALIENTE (v6.0, regla 31 — self-improving-agent). Activar SIEMPRE que (a) un comando falla, (b) el usuario corrige un supuesto, (c) falta una capacidad o dato, (d) el conocimiento queda desactualizado, (e) se descubre una mejor vía — y ANTES de cualquier tarea mayor (revisar el ledger relevante primero). Cubre captura en 06_aprendizaje/, categorías, reuso, promoción semanal a reglas/skills.
---

# Ledger de autoaprendizaje — el agente aprende de sus errores (v6.0)

Fuente verificada: `pskoett/self-improving-agent` (clonado en `repos/pskoett_self-improving-agent/`, patrón `.learnings/` con LEARNINGS/ERRORS/FEATURE_REQUESTS + ciclo captura→revisión→reuso→promoción). En ZOLO el ledger vive en **`06_aprendizaje/`** DENTRO del paquete (sobrevive a resets, regla 22). Complementa: `reflexion-post-mortem` (post-mortem formal del fallo grave — su LECCIÓN se copia aquí), §15 del núcleo (promoción a regla).

## 1. Los 3 archivos del ledger

```markdown
06_aprendizaje/ERRORS.md            # fallos de comando/integración/deploy + cómo se resolvió
06_aprendizaje/LEARNINGS.md         # correcciones, insights, huecos de conocimiento, mejores prácticas
06_aprendizaje/FEATURE_REQUESTS.md  # capacidades pedidas por el founder o detectadas por mí, con estado
```

Si faltan (entorno nuevo), crearlos con los headers de categoría. Nunca borrar entradas — una corrección APPENDE una entrada nueva que SUPERSEDE (regla 24).

## 2. Captura EN EL MOMENTO (no "al cierre de sesión")

El aprendizaje que espera al cierre se pierde (la ventana avanza, el detalle muere). Formato mínimo de entrada (~5 líneas):

```markdown
### <slug> — <fecha America/Guayaquil>
- CONTEXTO: <qué intentaba, en qué task>
- PASÓ: <hecho observable con evidencia (exit code, HTTP, grep)>
- LECCIÓN: <1 frase grep-able con acción>            # ← LECCIÓN: es grep-able en TODO el ledger
- CATEGORÍA: corrección | insight | hueco_conocimiento | mejor_práctica
- PROMOCIÓN: <ninguna | regla candidata §15 | skill candidata regla 28 | eval nuevo>
```

Rutas de captura:
- **Comando/tool falla** → `ERRORS.md` (incluir la corrección exacta que funcionó).
- **El usuario corrige un supuesto mío** → `LEARNINGS.md` categoría `corrección` (regla §15: fricción = regla potencial).
- **No sé hacer X o un dato falta** → `LEARNINGS.md` categoría `hueco_conocimiento` → dispara el ciclo de regla 32 (autoinstalador) o autoeducación (regla 33).
- **Mejor vía descubierta** → `LEARNINGS.md` categoría `mejor_práctica` → candidata a regla de oro (§3 del núcleo).
- **Capacidad pedida y ausente** → `FEATURE_REQUESTS.md` con estado `pendiente | en_curso | resuelto (v6.0 …)` — las peticiones del founder de la carta v6.0 ya viven ahí como F-001..F-008.

## 3. Reuso ANTES de tareas mayores

Antes de: deploy, campaña de outreach, edición del núcleo, tarea >30 min, tarea con subagentes → `grep -i "<tema>" 06_aprendizaje/*.md` y aplicar las lecciones relevantes. Reincidir en un error YA registrado en el ledger = fallo de proceso grave (post-mortem obligatorio + eval de regresión).

## 4. Promoción semanal (lección → ADN del agente)

En el BOOT semanal (o al acumular ≥5 entradas nuevas):
1. Releer entradas nuevas; agrupar repetidas (misma lección 2+ veces = patrón real).
2. Promover: patrón de comportamiento → **regla nueva §15** (delta quirúrgico + CHANGELOG + eval) · patrón de técnica → **regla de oro §3** · procedimiento repetible → **skill nueva** (regla 28) · hueco de conocimiento → **misión de autoeducación** (regla 33) con fecha.
3. Marcar en la entrada: `PROMOCIÓN: hecha → <destino>` (bi-temporal, sin borrar).
4. Registrar la promoción en el worklog semanal.

## 5. Relación con los otros mecanismos

| Señal | Mecanismo | Destino |
|---|---|---|
| Fallo grave verificado propio | `reflexion-post-mortem` (4 campos, antes de corregir) | LECCIÓN se copia a `LEARNINGS.md` |
| Fricción del usuario | §15 (regla) | entrada en `LEARNINGS.md` como corrección |
| Éxito repetible | `biblioteca-skills` (fábrica, regla 28) | entrada en `LEARNINGS.md` como mejor_práctica |
| Hueco de capacidad | `autoinstalador-skills` (regla 32) | `FEATURE_REQUESTS.md` o hueco_conocimiento |
| Dato de mercado desactualizado | `mantenimiento-mensual` + regla 33 | hueco_conocimiento → radar |

## 6. Grader

- Toda corrección del usuario genera entrada en `LEARNINGS.md` en la MISMA sesión → PASS.
- Toda tarea mayor abre con grep del ledger (y cita 0+ lecciones aplicadas) → PASS.
- `grep -c "LECCIÓN:" 06_aprendizaje/LEARNINGS.md` ≥ entradas → PASS.
- Lección repetida 2+ veces promovida a regla/skill/eval en ≤7 días → PASS.
- Ninguna entrada editada hacia atrás (solo append + PROMOCIÓN) → PASS.

## Grader (regla 28)

```bash
test_ledger-autoaprendizaje() {
    # 1. Skill existe con frontmatter
    test -f 02_skills/ledger-autoaprendizaje/SKILL.md
    # 2. Frontmatter tiene name y description
    grep -q "^name:" 02_skills/ledger-autoaprendizaje/SKILL.md
    grep -q "^description:" 02_skills/ledger-autoaprendizaje/SKILL.md
    # 3. Skill indexada en §12 del núcleo
    grep -q "ledger-autoaprendizaje" 01_nucleo/ZOLO_V6.md
}
```
