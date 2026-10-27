---
name: biblioteca-skills
description: Fábrica de skills (v5.0, Voyager + ACI de SWE-agent). Activar cuando un procedimiento acaba de ejecutarse con éxito por 2ª vez (o 1ª si fue caro: >10 pasos, >1 subagente, o falló antes de lograrlo), cuando el usuario pregunta "¿esto no se puede automatizar?", o en el mantenimiento mensual para PODAR skills sin uso. Convierte experiencia en capacidad permanente.
---

# Biblioteca de skills viva — cada éxito repetible se vuelve capacidad (v5.0, M7)

Voyager demostró el salto clave: un agente con biblioteca que CRECE supera linealmente al que repite descubrimientos. En ZOLO la biblioteca son las 18 skills de `02_skills/`; esta skill define cómo se AMPLÍA (fábrica, regla 28) y se MANTIENE (poda) — sin degradar la definición (edición por deltas, regla 22).

## 1. Gatillo de fabricación (cuándo promover procedimiento → skill)

| Condición | Acción |
|---|---|
| Éxito 2ª vez del mismo procedimiento | Fabricar skill |
| Éxito 1ª vez PERO caro (>10 pasos · >1 subagente · falló antes) | Fabricar skill |
| Procedimiento único, barato, ya terminado | NO fabricar — queda como entrada de worklog grep-able |

El registro del contador vive en el Stage Summary de cada task (`replicable: sí/2ª vez`).

## 2. Protocolo de fabricación (4 piezas obligatorias, regla 28)

```markdown
---
name: <slug-kebab>
description: <QUÉ hace y CUÁNDO activarla — los disparadores TEXTUALES que la invocan>
---
# <Título> (v5.x, M<si aplica>)

1. FRONTMATTER agentskills.io — name + description con disparadores literales
2. PASOS reproducibles — cada paso con criterio de salida verificable (grader determinista primero)
3. CONTRATO DE SALIDA ergonómico (ACI, SWE-agent) — qué imprime el procedimiento,
   formato compacto y grep-able, sin ruido decorativo; errores con huella + acción siguiente
4. GRADER — el check determinista que confirma "esta skill se ejecutó bien"
```

## 3. Contrato de salida ergonómico (ACI — la interfaz se diseña para el agente)

SWE-agent probó que el RENDIMIENTO depende más de la interfaz que del modelo. Para cada skill nueva:

- Outputs como líneas `CLAVE: valor` o tablas — grep-ables, sin párrafos decorativos.
- Errores: `FALLO <paso> — causa — acción siguiente` (nunca stack dumps crudos en la ventana).
- Cifras con fecha + fuente inline (`71,198 (24-oct, /api/skills)`).
- El skillbody cabe en ≤1 pantalla; el detalle pesado va a los scripts que la skill llama (L2, skill `memoria-jerarquica`).

## 4. Alta en el índice (delta quirúrgico)

1. Crear `02_skills/<slug>/SKILL.md`.
2. Añadir 1 línea al índice §12 del núcleo (delta MultiEdit, sin regenerar).
3. Entrada en CHANGELOG (PATCH o MINOR) + escenario nuevo en EVALS.md (grader de la pieza 4).
4. Commit alethech (cambio de estado de la definición — regla 24).

## 5. Poda (mantenimiento-mensual)

- Skill sin activación en 2 meses → candidata a poda: fusionar si solapa con otra, o archivar a `02_skills/archive/` con nota en CHANGELOG (NUNCA borrar silenciosamente — bi-temporal, regla 24).
- Skill con 2 fallos seguidos en su grader → volver a fabricación (pieza 2/3 rotas) o post-mortem (skill `reflexion-post-mortem`).
- Límite sano: ~25 skills. Más que eso = índice caro en el núcleo; consolidar en vez de acumular.

## 6. Anti-patrones

- Skill-documento: un doc de contexto disfrazado de skill (sin pasos ni grader) → pertenece a `04_conocimiento/`.
- Skill de 1 uso: fabricar por entusiasmo — consume índice sin retorno.
- Skill sin disparadores textuales: si la description no dice CUÁNDO activarla, nunca se activará.
- Duplicar una existente: antes de fabricar, grep en `02_skills/` — extender la existente por delta.

## Grader (regla 28)

```bash
test_biblioteca-skills() {
    # 1. Skill existe con frontmatter
    test -f 02_skills/biblioteca-skills/SKILL.md
    # 2. Frontmatter tiene name y description
    grep -q "^name:" 02_skills/biblioteca-skills/SKILL.md
    grep -q "^description:" 02_skills/biblioteca-skills/SKILL.md
    # 3. Skill indexada en §12 del núcleo
    grep -q "biblioteca-skills" 01_nucleo/ZOLO_V6.md
}
```
