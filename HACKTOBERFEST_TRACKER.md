# Hacktoberfest 2026 — Tracker

**Estado al:** 2026-10-13 03:30 UTC
**Cuenta GitHub:** @eddyflores100-lang
**Cuenta GitLab:** @eddyflores100
**Meta:** 4 PRs merged antes del 31 oct 2026

---

## ✅ PRs merged (1)

| # | Plataforma | Proyecto | PR | Issue | Merge date | Lenguaje |
|---|------------|----------|----|-------|------------|----------|
| 1 | GitHub | meetdino/dino | #124 | #106 rust-version | 2026-10-07 | Rust |

**Hacktoberfest cuenta:** 1/4 ✅

## PRs en proceso (5)

| # | Plataforma | Proyecto | MR/PR | Issue | Estado | Lenguaje |
|---|------------|----------|-------|-------|--------|----------|
| 2 | GitLab | OpenMW/openmw | !5667 | #9374 stormDirection | ✅ MERGEABLE. Maintainer Assumeru sugirió migrar a Lua. Respondido + issue follow-up #9394 abierto (2026-10-13). Pipeline MANUAL. | C++ |
| 3 | GitLab | inkscape/extensions | !738 | #634 Tspan | ❌ Cerrado (mi fix estaba mal) | Python |
| 4 | GitLab | inkscape/extensions | !739 | #625 gutter | ✅ Pipeline SUCCESS, NOT_APPROVED. Ping de review publicado (2026-10-13). | Python |
| 5 | GitLab | inkscape/inkscape | !8203 | #5230 Twitter→X | (sin actualizar hoy — Cloudflare bloqueó verificación) | C++ |
| 6 | GitLab | fdroid/fdroidclient | !1786 | #3361 TalkBack | ✅ Rebasing 2026-10-13: 3 commits rehechos sobre master 9bbfa19, force-push OK, pipeline RUNNING con sha 7fe864f9, MERGEABLE sin conflictos. | Kotlin |

**Mergeables ya:** 3 (OpenMW !5667, inkscape !739, fdroidclient !1786) + 1 mergeado (dino #124)

---

## Patches preparados para mañana (3)

| # | Repo | Issue | Lenguaje | Patch | Branch |
|---|------|-------|----------|-------|--------|
| 1 | Ergane-Foundation/vajra | #29 skip Linux installer on macOS | Bash | `/home/z/my-project/download/hacktoberfest-vajra-29.patch` (68 líneas) | fix/29-skip-linux-installer-on-macos |
| 2 | Ishannaik/harbour | #41 filter control chars in push_history | Rust | `/home/z/my-project/download/hacktoberfest-harbour-41.patch` (90 líneas) | fix/41-filter-control-chars-history |
| 3 | NovaCode37/Prism-platform | #388 md5 → sha256 cache filenames | Python | `/home/z/my-project/download/hacktoberfest-prism-388.patch` (66 líneas) | fix/388-md5-to-sha256-cache-filenames |

---

## Otros concursos OSS activos

### MLH Global Hack Week: Hacktoberfest
- **URL:** https://ghw.mlh.io
- **Fechas:** Todo octubre, eventos online
- **Reward:** Stickers + digital badge
- **Acción:** Unirse a eventos. No requiere PRs, solo asistencia y participación.

### 24 Pull Requests (diciembre)
- **URL:** https://24pullrequests.com
- **Fechas:** 1-24 diciembre
- **Reward:** Digital badge + árbol plantado
- **Acción:** 24 PRs en diciembre. Planificamos para diciembre.

### DoraHacks Buidls
- **URL:** https://dorahacks.io
- **Fechas:** Continuo
- **Reward:** Hasta $5,000 USD para top proyectos
- **Acción:** Proponer proyecto OSS propio. Tu repo `alethech-publish-2` califica.

### Global Mesh AI & Swarm Robotics Challenge
- **URL:** https://unstop.com
- **Fechas:** Hasta 5 oct (cierra mañana)
- **Reward:** ₹10,000 cash
- **Acción:** Contribuciones a OSS swarm. Probablemente tarde para este.

### Google Summer of Code 2027
- **URL:** https://summerofcode.withgoogle.com
- **Fechas:** Aplica feb 2027
- **Reward:** $1500-$6000 USD stipend
- **Acción:** Planificar para aplicar en febrero.

### Outreachy
- **URL:** https://outreachy.org
- **Fechas:** Continuo, cohortes mayo y diciembre
- **Reward:** $7000 USD stipend para interns
- **Acción:** Aplicar si calificas (underrepresented in tech).

---

## Plan mañana (miércoles 7 oct, 9am Ecuador)

### Paso 1 — Verificar estado MRs (5 min)

Cuando abras el chat mañana y digas "hacktoberfest", yo ejecuto:

```bash
bash /home/z/my-project/scripts/hacktoberfest_runner.sh
```

Eso verifica estado de los 6 MRs y te lo muestra en pantalla.

### Paso 2 — Responder maintainer dino (5 min)

Ve a https://github.com/meetdino/dino/pull/124 y comenta:

```
Done. Bumped to 1.91.

Thanks for catching the anyllm_translate dep issue — I should have verified the actual MSRV with cargo +1.90 check instead of trusting the value in CONTRIBUTING.md. Good catch on #129 too, the README/CONTRIBUTING alignment makes sense.

Ready to merge whenever you are.
```

### Paso 3 — Enviar 3 PRs nuevos (45 min)

Te paso 3 scripts PowerShell completos para enviar los 3 patches preparados. Uno por uno.

---

## Anti-ban rules

- **1 PR por día por cuenta GitHub** — ya tienes 1 PR (dino #124), mañana mandas 3 más en 3 repos distintos.
- **No tocar mismo repo 2 veces seguidas** sin esperar respuesta maintainer.
- **Cero overlap** con cuenta GitLab — son ecosistemas distintos.
- **Si maintainer responde, atender en <24h.**
