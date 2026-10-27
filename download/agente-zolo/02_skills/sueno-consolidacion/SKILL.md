---
name: sueno-consolidacion
description: >-
  Cross-session pattern extraction and playbook generation. Inspired by
  Anthropic's "dreaming" feature (May 2026 Code with Claude). Reviews past
  worklog entries and ledger (LEARNINGS/ERRORS/FEATURE_REQUESTS) to identify
  recurring patterns across sessions and write them back as structured
  playbooks that future sessions reference. Markdown-native: no model weights
  changed, all output is inspectable by humans.
trigger: >-
  Cualquiera de: cadencia SEMANAL del ciclo §18 (planificada), después de
  cerrar 5+ tasks consecutivos, cuando LEARNINGS.md supera 50 entradas, cuando
  ERRORS.md repite el mismo patrón 3+ veces, o cuando el founder pide
  "consolida", "resume lo aprendido", "qué patrón has visto".
---

# Skill: Sueño-Consolidación (Dreaming cross-sesión)

> **Origen**: Anthropic "dreaming" feature (Code with Claude, May 2026). Harvey
> reportó 6x task completion rate tras activarlo. Adaptación markdown-native
> para ZOLO: todo el output es texto plano auditable por humanos, sin tocar
> pesos del modelo ni dependencias externas.

## Cuándo activar

- **Cadencia SEMANAL §18**: domingo o primer BOOT de la semana (recomendado)
- **Trigger por umbral**: LEARNINGS.md > 50 entradas o ERRORS.md con mismo patrón 3+ veces
- **Cierre de sprint**: después de 5+ tasks consecutivos cerrados con `alethech commit`
- **Orden explícita del founder**: "consolida", "resume lo aprendido", "qué patrón has visto"

## Lo que hace

1. **Lee** el worklog (últimas N entradas, default 20) + `06_aprendizaje/LEARNINGS.md` + `06_aprendizaje/ERRORS.md` + `06_aprendizaje/FEATURE_REQUESTS.md`
2. **Identifica patrones** que se repiten 2+ veces:
   - Errores con la misma causa raíz
   - Soluciones exitosas usadas múltiples veces
   - Decisiones del founder que aparecen 2+ veces
   - Skills activadas con el mismo trigger
3. **Escribe playbooks** en `06_aprendizaje/playbooks/` (uno por patrón):
   ```markdown
   # Playbook: <nombre-del-patrón>
   
   ## Patrón detectado
   <descripción grep-able, 1 línea>
   
   ## Evidencia (N ocurrencias)
   - <fecha> — <task_id> — <extracto de 1 línea>
   - <fecha> — <task_id> — <extracto de 1 línea>
   - ...
   
   ## Heurística portable
   <regla o procedimiento que futuras sesiones deben aplicar>
   
   ## Acción de promoción
   - [ ] Promover a regla del núcleo ZOLO_V<N+1>.md
   - [ ] Promover a skill nueva (02_skills/)
   - [ ] Promover a eval nuevo (EVALS.md)
   - [ ] Solo playbook (mantener como referencia)
   ```
4. **Promueve** los patrones más repetidos:
   - Si 5+ ocurrencias → propone regla nueva al núcleo (§15 fricción → regla)
   - Si 3+ ocurrencias con procedimiento claro → propone skill nueva (regla 28)
   - Si 2+ ocurrencias con caso de test → propone eval nuevo (regla 12)
5. **Reporta** al founder con resumen grep-able en worklog:
   ```
   ### RADAR <fecha> — sesión de sueño
   - PATRONES DETECTADOS: <N>
   - PLAYBOOKS CREADOS: <N> en 06_aprendizaje/playbooks/
   - PROMOCIONES PROPUESTAS: <N> (X reglas, Y skills, Z evals)
   - ACCIÓN: <esperar founder | aplicar auto si regla 33 activa>
   ```

## Diferencias vs Anthropic dreaming

| Aspecto | Anthropic | ZOLO |
|---------|-----------|------|
| Plataforma | Claude Managed Agents (cerrada) | Markdown + filesystem (auditable) |
| Pesos del modelo | No modifica (correcto) | No modifica (igual) |
| Output | Notes + playbooks en memoria interna | Playbooks markdown en `06_aprendizaje/playbooks/` |
| Inspección humana | Requiere dev console | `cat 06_aprendizaje/playbooks/*.md` |
| Cross-agent | Sí (multi-agente managed) | Sí (multi-task via worklog compartido) |
| Trigger | Manual desde console | Cadencia §18 + umbral + orden founder |
| Promoción | Auto a memory store | Propuesta al founder (gate HITL §17 G1) |

## Lo que NO hace (guardarraíles)

- ❌ No modifica `ZOLO_V<N>.md` sin aprobación del founder (gate G1 §17)
- ❌ No elimina entradas del ledger (append-only, regla 9)
- ❌ No "olvida" lecciones — solo consolida y promueve
- ❌ No inventa patrones sin evidencia (mínimo 2 ocurrencias con cita)
- ❌ No ejecuta promociones automáticas salvo regla 33 explícita del founder

## Contrato de salida (regla 7)

```
INPUT: worklog + 06_aprendizaje/{LEARNINGS,ERRORS,FEATURE_REQUESTS}.md
OUTPUT:
  - 06_aprendizaje/playbooks/PB-<NNN>-<nombre>.md (1+ archivos nuevos)
  - worklog append: entrada ### RADAR <fecha> con conteo + rutas
  - Si promociones propuestas: FEATURE_REQUESTS.md append con IDs PB-<NNN>
BOUNDARIES:
  - Solo lee, no ejecuta código externo
  - Solo escribe en 06_aprendizaje/playbooks/ y worklog.md (append)
  - No toca 01_nucleo/ sin gate G1 explícito del founder
PRESUPUESTO:
  - <10 min de wallclock (no es un bucle autónomo, es una pasada)
  - Si >30 patrones detectados, muestrea los 10 más repetidos
```

## Grader (regla 28)

```bash
# Verificar que la skill produce lo que dice
test_sueno_consolidacion() {
    # 1. Trigger: simular 5 entradas de worklog + 3 LEARNINGS repetidos
    # 2. Ejecutar skill
    # 3. Verificar output
    ls 06_aprendizaje/playbooks/PB-*.md | wc -l  # >= 1 playbook creado
    grep -l "Patrón detectado" 06_aprendizaje/playbooks/*.md  # tiene sección
    grep -c "Evidencia" 06_aprendizaje/playbooks/*.md  # cita entradas reales
    # 4. Worklog tiene entrada RADAR
    grep "PATRONES DETECTADOS" worklog.md  # al menos 1
    # Exit 0 si todo pasa
}
```

## Implementación técnica (cuando se active)

El agente debe:
1. `tail -200 /home/z/my-project/worklog.md` + leer los 3 archivos del ledger
2. `grep -E "^### |^- CONTEXTO:|^- LECCIÓN:" worklog.md 06_aprendizaje/*.md` para extraer patrones
3. Agrupar por similitud textual (no semántica — mantener determinista)
4. Para cada grupo con 2+ entradas, generar playbook
5. Listar promociones propuestas con IDs PB-<NNN>
6. Append worklog con resumen grep-able

## Historial

- **2026-10-25 (Task 125)**: skill creada tras detectar patrón "Anthropic dreaming" en radar semanal. Inspiración: Harvey 6x task completion rate. Implementación markdown-native (sin deps externas).
