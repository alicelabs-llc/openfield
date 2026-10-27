---
name: depuracion-sistematica
description: Depuración sistemática (v6.0 — la Ley de Hierro de superpowers). Activar ante CUALQUIER bug, test rojo, fallo de build, comportamiento inesperado o problema de rendimiento, ANTES de proponer el primer fix. Especialmente bajo presión de tiempo, cuando "un fix rápido se ve obvio", tras 2+ fixes fallidos, o cuando no entiendo la causa. Cubre las 4 fases con la regla: NO FIX SIN CAUSA RAÍZ INVESTIGADA.
---

# Depuración sistemática — causa raíz ANTES que fix (v6.0)

Fuente verificada: `obra/superpowers` skill `systematic-debugging` (clonado en `repos/obra_superpowers/`). Regla de acoplamiento: si el fallo es MIO (mi script, mi deploy, mi decisión), este skill se ejecuta junto con `reflexion-post-mortem` (post-mortem de 4 campos antes de corregir, regla 29) y la LECCIÓN termina en `06_aprendizaje/ERRORS.md` (regla 31).

## 1. La Ley de Hierro

```
NINGÚN FIX SIN INVESTIGACIÓN DE CAUSA RAÍZ PRIMERO
```

Fase 1 incompleta = prohibido proponer fixes. **Arreglar el síntoma ES fallar** — violar la letra del proceso es violar su espíritu. Se usa ESPECIALMENTE cuando: hay presión de tiempo (la urgencia hace adivinar tentador), "un fix rapidito" parece obvio, ya probé 2+ fixes sin resultado, o no entiendo del todo el fallo.

## 2. Las 4 fases (cada una completa antes de la siguiente)

### Fase 1 — Investigación de causa raíz
1. **Leer el error COMPLETO**: mensaje, stack trace, códigos, líneas, paths — la solución exacta a veces está dentro del propio error. Jamás saltarlo.
2. **Reproducir de forma consistente**: pasos exactos, ¿pasa siempre? No reproducible = recolectar más datos, NO adivinar.
3. **Cambios recientes**: git diff, commits nuevos, dependencias, config, entorno — ¿qué cambió que pudo causar esto?
4. **Sistemas multi-componente** (CI→build→signing, API→worker→DNS, curl→CDN→origen): instrumentar ANTES de proponer fix — log de qué ENTRA y qué SALE en cada frontera de componente, verificar propagación de env/config, inspeccionar estado por capa.

### Fase 2 — Análisis de patrón
- ¿Qué OTROS lugares comparten el mismo patrón y podrían tener el mismo bug?
- ¿Funciona en un entorno y falla en otro? ¿Qué difiere EXACTAMENTE entre ambos (env, versión, permisos, caché)?
- ¿Cuándo dejó de funcionar? ¿Qué cambió entonces? (git log bisectable)

### Fase 3 — Hipótesis y test mínimo
- Escribir la hipótesis en 1 línea: "X causa Y porque Z".
- Diseñar el test MÁS PEQUEÑO que la confirma o refuta (un curl, un grep, un run aislado).
- Hipótesis refutada = volver a Fase 1 con el dato nuevo. Jamás apilar fixes sobre una hipótesis no probada.

### Fase 4 — Fix dirigido a la raíz
- El fix corrige la CAUSA, no el síntoma (parche al síntoma solo si además hay fix de raíz o bloqueo urgente documentado como deuda).
- Verificar el fix con la reproducción original (ahora verde) + regresión en lo cercano.
- Cierre: si el fallo era propio → post-mortem 4 campos (regla 29) + entrada en `06_aprendizaje/ERRORS.md` + eval de regresión nuevo.

## 3. Anti-patrones (todos vistos en producción, todos cobrados)

| Anti-patrón | Por qué falla |
|---|---|
| "Un fix rapidito" bajo presión | La urgencia es cuando MÁS se necesita el proceso — adivinar garantiza re-trabajo |
| Apilar fixes #3, #4, #5 sobre el síntoma | Cada parche añade estado nuevo que confunde la siguiente investigación |
| Declarar "fixed" sin reproducir | El fallo vuelve en producción con interés compuesto |
| Fix sin cerrar el ciclo de aprendizaje | El mismo bug regresa en otra sesión (por eso existe el ledger, regla 31) |
| Atribuir a "el modelo/la plataforma se portó raro" | Es la excusa que impide encontrar la causa real |

## 4. Grader

- Antes del primer fix existe evidencia de Fase 1 (error leído completo + reproducción + diff de cambios recientes) → PASS.
- El fix propuesto cita la hipótesis probada (Fase 3), no el síntoma → PASS.
- "Fixed" declarado SOLO con la reproducción original en verde + verificación de regresión cercana → PASS.
- Fallo propio cierra con post-mortem + entrada en ERRORS.md + eval nuevo → PASS.
- 2+ fixes apilados sin hipótesis → FAIL grave (post-mortem obligatorio del proceso completo).

## Grader (regla 28)

```bash
test_depuracion-sistematica() {
    # 1. Skill existe con frontmatter
    test -f 02_skills/depuracion-sistematica/SKILL.md
    # 2. Frontmatter tiene name y description
    grep -q "^name:" 02_skills/depuracion-sistematica/SKILL.md
    grep -q "^description:" 02_skills/depuracion-sistematica/SKILL.md
    # 3. Skill indexada en §12 del núcleo
    grep -q "depuracion-sistematica" 01_nucleo/ZOLO_V6.md
}
```
