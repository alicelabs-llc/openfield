# Hacktoberfest 2026 — Plan de batalla

**Objetivo:** 4 PRs merged antes del 31 de octubre 2026 para completar Hacktoberfest.

**Estado actual:**
- 6 PRs activos en GitLab/GitHub
- 1 aprobado (dino #124) pendiente de tu respuesta
- 5 esperando review

**Faltan:** 3 PRs merged más.

---

## Concursos OSS activos (octubre-noviembre 2026)

| Concurso | Fechas | Reward | Cómo participar |
|----------|--------|--------|----------------|
| **Hacktoberfest 2026** | 1-31 octubre | Swag kit (camiseta + stickers) | 4 PRs merged a repos con tag "hacktoberfest" |
| **MLH Global Hack Week: Hacktoberfest** | Online, octubre | Stickers + digital badge | Unirte a eventos en majorleaguehacking.io |
| **24 Pull Requests** | 1-24 diciembre | Digital badge + árbol plantado | 24 PRs en diciembre |
| **DoraHacks Buidls** | Continuo | Hasta $5,000 USD | Proponer proyecto open source |
| **Global Mesh AI & Swarm Robotics Challenge** | Hasta 5 oct | ₹10,000 cash | Contribuciones a OSS swarm |

---

## Candidatos para mañana (miércoles 7 oct, 9am Ecuador)

### Prioridad alta — bugs reales (no "add example")

#### Python (5 candidatos)

1. **Ergane-Foundation/vajra #29** — "Skip the Linux installer when starting on macOS"
   - 0 comments, fresh issue
   - URL: https://github.com/Ergane-Foundation/vajra/issues/29
   - Probablemente 1 if-statement

2. **Ergane-Foundation/vajra #26** — "Remove the broken duplicate get_gnn_fingerprint_predictions"
   - 0 comments
   - URL: https://github.com/Ergane-Foundation/vajra/issues/26
   - Borrar función duplicada

3. **Ergane-Foundation/vajra #21** — "Create the logs directory before log files are opened at import time"
   - 0 comments
   - URL: https://github.com/Ergane-Foundation/vajra/issues/21
   - os.makedirs(exist_ok=True) en __init__

4. **NovaCode37/Prism-platform #388** — "Hash cache filenames with sha256 instead of MD5"
   - 1 comment
   - URL: https://github.com/NovaCode37/Prism-platform/issues/388
   - Cambiar hashlib.md5 a hashlib.sha256

5. **NovaCode37/Prism-platform #411** — "Fix the React Compiler lint errors that Next 16 surfaces"
   - 2 comments
   - URL: https://github.com/NovaCode37/Prism-platform/issues/411
   - Más complejo, TS/React

#### Rust (2 candidatos)

6. **Ishannaik/harbour #41** — "persist: filter control characters and newlines in push_history"
   - URL: https://github.com/Ishannaik/harbour/issues/41
   - Sanitización de input

#### TypeScript (3 candidatos)

7. **reticlehq/reticle #1412** — "`press` never fires `keypress`"
   - URL: https://github.com/reticlehq/reticle/issues/1412
   - Bug real de evento

8. **libredb/libredb-studio #1260** — "docs/editor/query-optimization.md: count Neo4j and Db2"
   - URL: https://github.com/libredb/libredb-studio/issues/1260
   - Docs

9. **libredb/libredb-studio #1259** — "provider-docs-monitoring-citations.test.ts"
   - URL: https://github.com/libredb/libredb-studio/issues/1259
   - Test fix

---

## Plan de ejecución mañana (miércoles 7 oct)

### Hora de inicio: 9:00am hora Ecuador (14:00 UTC)

| Hora (Ecuador) | Tarea |
|-----------------|-------|
| 09:00 | Verificar estado de los 5 MRs actuales (¿alguno merged?) |
| 09:15 | Responder al maintainer de dino PR #124 (texto ya preparado) |
| 09:30 | Clonar vajra, hacer fix issue #29 (skip Linux installer en macOS) |
| 10:00 | Crear PR #1 del día a vajra |
| 10:15 | Clonar harbour, hacer fix issue #41 (filter control chars) |
| 10:45 | Crear PR #2 del día a harbour |
| 11:00 | Clonar Prism-platform, hacer fix issue #388 (md5 → sha256) |
| 11:30 | Crear PR #3 del día a Prism-platform |
| 11:45 | Pausa, monitorear MRs anteriores |
| 14:00 | Si respondió maintainer de cualquier MR, atender |
| 14:30 | Buscar 2 issues más para el jueves |
| 16:00 | Cierre del día |

**Meta del día:** 3 PRs nuevos enviados → total 9 PRs en proceso.

---

## Anti-ban (importante)

| Límite | Máximo |
|--------|--------|
| PRs por día por cuenta GitHub | 2-3 |
| Cuenta disponible | @eddyflores100-lang (ya tiene 8 PRs) |
| Estrategia | 1 PR por repo distinto, no spam |
| Esperar respuesta | Sí, antes de abrir otro en mismo repo |

---

## Cómo usar este plan

1. Hoy (martes 23:11 Ecuador): Descansa.
2. Mañana (miércoles 9am): Vuelve y trabajamos los 3 PRs del día.
3. Jueves: Si mergearon algunos, seguimos con otros. Si no, esperamos.
4. Viernes: Repaso semanal.

**Para completar Hacktoberfest necesitas 4 PRs merged. Tienes 6 en proceso. Si 4 se merguean, completas el reto.**

---

## Concursos adicionales a explorar

- **MLH Global Hack Week**: https://ghw.mlh.io (eventos online todo octubre)
- **DEV Challenges**: https://dev.to/challenges (challenges mensuales con prizes)
- **Codebeam**: https://codebeam.dev (Erlang/Elixir community)
- **Google Summer of Code 2027**: opens February 2027 (no aplica ahora pero planifica)
- **Outreachy**: https://outreachy.org (internships OSS para underrepresented groups)
