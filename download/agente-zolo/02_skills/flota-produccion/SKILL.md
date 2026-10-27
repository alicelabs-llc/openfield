---
name: flota-produccion
description: Flota de producción por delegación real (v6.0). Activar cuando una tarea tiene ≥2 piezas INDEPENDIENTES (módulos, auditorías, investigaciones, artefactos, páginas, tests) o cuando un pipeline de producción requiere constructor + auditor. Cubre despacho paralelo en un solo mensaje, brief autocontenido por subagente, revisión por artefacto, escéptico con veto, rulings-not-stalls, ledger de progreso en archivo y las únicas 4 paradas legítimas.
---

# Flota de producción — delegar para producir (v6.0)

Fuentes verificadas: `obra/superpowers` (~304k★) skills `subagent-driven-development` + `dispatching-parallel-agents` (clonados en `repos/obra_superpowers/`) + la mesa de 6 bots del founder (un escéptico que tumba lo flojo). Complementa (no reemplaza): `subagentes-contrato` (contrato de 6 líneas), `equipo-virtual` (roles con SOPs recurrentes), `best-of-n-decisiones` (decisiones sensibles).

## 1. La regla central

**Un subagente fresco por pieza, despachados EN UN SOLO MENSAJE.** Múltiples llamadas Task en la misma respuesta = ejecución paralela real; una por mensaje = secuencial disfrazado. El subagente JAMÁS hereda mi contexto o historial: yo construyo exactamente el brief que necesita (contrato de 6 líneas de `subagentes-contrato`). Esto preserva MI contexto para coordinar, que es mi trabajo real como orquestador.

## 2. Cuándo activar (y cuándo NO)

| ¿Activar? | Señal |
|---|---|
| ✅ | ≥2 piezas sin estado compartido (tests de archivos distintos, 3 páginas, auditoría + construcción, N investigaciones) |
| ✅ | Pieza estimada >15 tool calls que otro contexto puede hacer con un brief |
| ❌ | Las piezas están acopladas (arreglar una puede arreglar las otras) — resolver la raíz primero (skill `depuracion-sistematica`) |
| ❌ | Requiere entender el estado completo del sistema — es trabajo mío |

## 3. Protocolo por tarea de producción

1. **Particionar** en piezas independientes y nombrarlas (F-01, F-02…).
2. **Ledger en archivo**: `download/research/<slug>-ledger.md` con una línea por pieza (estado: pendiente/despachada/revisada/integrada). El progreso NO vive solo en el todo list — la compaction de contexto ha hecho que controladores pierdan su lugar y re-despachen tareas YA completadas (el fallo único más caro observado en superpowers). Antes de despachar, leer el ledger si existe y reanudar.
3. **Briefs exactos**: cada brief contiene (a) contexto mínimo autocontenido, (b) objetivo con criterio de salida verificable, (c) formato de salida, (d) boundaries (no tocar X), (e) presupuesto, (f) registro de trabajo esperado. Salida pesada (>2KB) a archivo, solo vuelve resumen + referencia.
4. **Despacho paralelo en un solo mensaje** (todas las llamadas Task juntas).
5. **Revisión por artefacto**: cada pieza que vuelve pasa revisión ANTES de integrarse — spec cumplida + calidad. Rechazada → fix loop con el mismo brief + lo observado (máx 2 rondas; a la 3ª, integrar como esté y registrar deuda).
6. **Revisión final amplia** al cerrar todo el batch (coherencia entre piezas + checklist §10 del núcleo).

## 4. Rulings, not stalls (decidir, no estancarse)

Un plan en marcha NO espera a un humano por conflictos, ambigüedades o defectos menores del plan. La spec es la autoridad vinculante; mi juicio resuelve lo que ni la spec ni el plan responden. **Cada decisión se registra**: `RULING: <qué decidí> — <por qué> — <coste si estoy equivocado>`. Un ruling equivocado cuesta un re-trabajo visible; una sesión estancada en una pregunta cuesta el día entero del founder.

## 5. Las únicas 4 paradas legítimas

1. Operación **irreversible o destructiva** (borrar, sobrescribir sin backup, gastar dinero).
2. Acción **sensible de seguridad** (credenciales, permisos, exponer superficie).
3. **Efecto fuera de este entorno** que por normas se consulta antes (merge a shared, push a rama compartida, publish).
4. Plan **tan roto** que todo camino hacia adelante es adivinar.

Fuera de esas 4: se decide y se sigue (§4). "¿Continúo?" entre piezas está PROHIBIDO — me ordenaron producir, no producir reportes de progreso.

## 6. El escéptico con veto (mesa multi-bot)

Toda línea de producción de calidad lleva un **auditor escéptico** cuyo trabajo explícito es TUMBAR lo flojo: buscar por qué NO cumple la spec, qué rompe, qué infló el constructor. No es opcional: el auditor revisa con evidencia (curl/grep/diff) y su veto obliga al fix loop. Con piezas sensibles (respuesta pública, deploy): además best-of-N (skill `best-of-n-decisiones`).

## 7. Grader

- Ledger existe y tiene una línea por pieza con estado → PASS.
- Los briefs contienen los 6 elementos del contrato → PASS.
- ≥2 Tasks en la misma respuesta cuando había ≥2 piezas independientes → PASS (1 por mensaje = FAIL de paralelismo).
- Cero "¿continúo?" entre piezas; solo las 4 paradas nombradas → PASS.
- Cada pieza integrada tiene revisión registrada (escéptico incluido) → PASS.

## 8. Fuentes en disco

`repos/obra_superpowers/skills/subagent-driven-development/SKILL.md` (ledger + rulings + 4 stops + per-task review) · `repos/obra_superpowers/skills/dispatching-parallel-agents/SKILL.md` (dominios independientes + despacho en una respuesta) · `06_ESTADO_DEL_ARTE_V6.md` §superpowers. Re-clonables: `git clone --depth 1 https://github.com/obra/superpowers.git repos/obra_superpowers`.

## Grader (regla 28)

```bash
test_flota-produccion() {
    # 1. Skill existe con frontmatter
    test -f 02_skills/flota-produccion/SKILL.md
    # 2. Frontmatter tiene name y description
    grep -q "^name:" 02_skills/flota-produccion/SKILL.md
    grep -q "^description:" 02_skills/flota-produccion/SKILL.md
    # 3. Skill indexada en §12 del núcleo
    grep -q "flota-produccion" 01_nucleo/ZOLO_V6.md
}
```
