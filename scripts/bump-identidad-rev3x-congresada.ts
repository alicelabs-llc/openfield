// Bump arquitectura-identidad to rev 6 (rev 3.x in the spec nomenclature).
// Applies the three conditions from the second audit:
// 1. cutoff_head included in the ControlEvent (signed/encadenado)
// 2. ancestry() formally defined
// 3. Protocol does NOT interpret "C ∉ ancestry(M)" as a claim about physical time
// Plus: rename REVOKED_KEY_AFTER_CUTOFF → NOT_IN_PROVEN_PRE_ROTATION_HISTORY
// Plus: add the normative phrase about physical time
// Plus: status APPROVED (audit closed at 3.x)
import { db } from "../src/lib/db";

const REV3X_SECTION = `

---

# rev 6 (rev 3.x) — semántica congresada

> **Auditoría cerrada.** Esta revisión integra las tres condiciones necesarias y suficientes identificadas en la segunda auditoría. No introduce nueva arquitectura, epochs, nonces ni store IDs.
>
> Estado: \`APPROVED\`.

## el cambio fundamental

La afirmación anterior:

\`\`\`
C ∉ ancestry(cutoff_head) ⇒ C es post-rotation
\`\`\`

**no se sigue criptográficamente.** Ha sido eliminada de la especificación.

La afirmación nueva:

\`\`\`
C ∉ ancestry(cutoff_head)
⇒
C no puede ser demostrado como perteneciente a la historia causal explícitamente cubierta por el cutoff_head de la rotación
\`\`\`

Es lo que el protocolo demuestra. **No afirma temporalidad.**

## frase normativa

> **Alethech no demuestra el tiempo físico de creación, firma, publicación u observación de un commit. \`cutoff_head\` define una frontera causal verificable sobre la historia explícitamente cubierta por una rotación.**

Esta frase es normativa: cualquier consumidor del protocolo debe entenderla antes de interpretar los estados de verificación.

## las tres condiciones (necesarias y suficientes)

### 1. \`cutoff_head\` está incluido en el ControlEvent de rotación (firmado y encadenado)

\`cutoff_head\` **no es un campo mutable de IdentityRecord**. Es parte del evento de control de rotación, firmado por el root y encadenado en la cadena monotónica.

\`\`\`json
{
  "type": "ControlEvent",
  "sequence": N,
  "previous_control_hash": "...",
  "event_type": "key_rotation",
  "old_key_id": "key-001",
  "key_id": "key-002",
  "public_key": { ... },
  "cutoff_head": "sha256:...",  // <-- parte de lo que se firma
  "reason": "rotation",
  "signature": "ed25519:..."   // firma del root sobre TODO, incluido cutoff_head
}
\`\`\`

**Justificación criptográfica:** si \`cutoff_head\` fuera mutable, un atacante con acceso al store podría cambiar retroactivamente qué historia considera cubierta la rotación. Al incluirlo en el ControlEvent firmado, esa manipulación se detecta: el hash del ControlEvent cambia, la firma del root no verifica, \`verify\` lo marca como \`CONTROL_CHAIN_INVALID\`.

### 2. \`ancestry()\` está formalmente definido

\`\`\`
ancestry(M) =
    el conjunto formado por M y todos los commits alcanzables desde M
    siguiendo recursivamente sus referencias parent.
\`\`\`

Ejemplo:

\`\`\`text
M
├── P1
│   ├── P2
│   └── P3
└── Q1
    └── Q2
\`\`\`

\`\`\`
ancestry(M) = {M, P1, P2, P3, Q1, Q2}
\`\`\`

**Casos especiales:**

- \`M ∈ ancestry(M)\`: el cutoff_head es parte de su propia ancestry.
- Si \`M.parents = []\` (genesis): \`ancestry(M) = {M}\`.
- Si un parent referenciado no existe en el store: \`ancestry(M)\` está parcialmente definida. El verificador reporta \`parent_missing\` pero puede seguir calculando ancestry con los commits disponibles.

**Algoritmo (BFS):**

\`\`\`python
def ancestry(M, commits):
    visited = set()
    queue = [M]
    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)
        if current not in commits:
            continue  # parent_missing — reported separately
        for parent in commits[current].parents:
            if parent not in visited:
                queue.append(parent)
    return visited
\`\`\`

### 3. El protocolo no interpreta \`C ∉ ancestry(M)\` como afirmación sobre tiempo físico

Esta condición ya está implícita en la frase normativa de arriba, pero se hace explícita aquí:

- \`C ∉ ancestry(M)\` **no implica**: creado después, firmado después, observado después, inválido, fraudulento, inexistente antes, o necesariamente sospechoso.
- \`C ∉ ancestry(M)\` **sí implica**: el commit no puede ser demostrado como perteneciente a la historia causal explícitamente cubierta por \`M\`.

Cualquier consumidor que interprete \`C ∉ ancestry(M)\` como una afirmación temporal **está usando mal el protocolo**.

## estados de verificación (congresados)

\`\`\`
VALID
  └─ firma válida + integridad válida + autorización de la key válida
     NO implica que la historia completa del commit sea válida.

VALID_HISTORICAL
  └─ VALID + K revocada + C ∈ ancestry(cutoff_head)
     El commit está incluido en la historia causal que el root seleccionó
     como cubierta por el cutoff.

NOT_IN_PROVEN_PRE_ROTATION_HISTORY
  └─ K revocada + C ∉ ancestry(cutoff_head)
     El commit no puede ser demostrado como perteneciente a la historia
     causal cubierta por ese cutoff.
     NO implica post-rotación.
     NO implica fraude.
     NO implica invalidez criptográfica.

UNKNOWN_KEY
  └─ no existe autorización conocida para esa key

INVALID_KEY_AUTHORIZATION
  └─ existe autorización pero su firma root es inválida

IDENTITY_MISMATCH
  └─ root/key/agent_id no forman la misma identidad

ROOT_MISMATCH
  └─ root declarado no coincide con root de la identidad

CONTROL_CHAIN_INVALID
  └─ cadena de control con huecos, hashes inconsistentes o firmas inválidas

COMMIT_SIGNATURE_INVALID
  └─ firma Ed25519 del commit no verifica

COMMIT_INTEGRITY_INVALID
  └─ commit_id recalculado no coincide

MISSING_CONTROL_EVENT
  └─ referencia a control event que no está en el store

MIGRATION_RECORD_INCOMPLETE
  └─ MigrationRecord con solo una de las dos firmas requeridas

VERIFICATION_PARTIAL
  └─ advertencia: el resultado es respecto a los datos disponibles,
     no al estado global. No es error fatal.

MISSING_PUBLICATION
  └─ advertencia: no hay publicación externa (no es error fatal)
\`\`\`

## cambio de nombre: REVOKED_KEY_AFTER_CUTOFF → NOT_IN_PROVEN_PRE_ROTATION_HISTORY

El nombre anterior implicaba temporalidad ("after"). El nuevo describe exactamente lo que el verifier puede comprobar: el commit no está demostrado como parte de la historia causal explícitamente cubierta por el cutoff.

Esto resuelve los contraejemplos A1 y B2 sin añadir arquitectura.

## lo que el protocolo NO demuestra (declaración explícita)

1. **Tiempo físico de creación, firma, publicación u observación.** Los timestamps son metadata informativa, no prueba criptográfica.

2. **Que un commit fuera de ancestry(cutoff) fue creado después de la rotación.** Solo afirma que no puede ser demostrado como pre-rotación.

3. **Que un commit en ancestry(cutoff) fue necesariamente creado antes de la rotación.** Un atacante con la clave privada podría, teóricamente, crear un commit y enlazarlo a un parent en ancestry(cutoff) — pero la firma de ese commit tendría un key_id y un commit_id distintos, y el consumidor puede verificar si quiere.

4. **Consistencia global entre verifiers.** Dos verifiers con cadenas de control distintas pueden llegar a resultados distintos. Ambos son "correctos" respecto a su cadena.

5. **Que el root no hizo equivocation.** Sin red de testigos, no se puede detectar.

## lo que el protocolo SÍ demuestra

1. **Autoría criptográfica:** cada commit está firmado por una key específica.
2. **Autorización verificable:** cada key tiene una \`KeyAuthorization\` firmada por el root, encadenada monótonamente.
3. **Integridad:** cada commit tiene un commit_id que se recalcula.
4. **Rotación atómica:** un solo ControlEvent produce K1 revoked + K2 active.
5. **Frontera causal:** \`cutoff_head\` define qué commits estaban en la historia conocida al momento de la rotación.
6. **Migración bilateral:** \`MigrationRecord\` vincula A → B con firmas de ambos lados.
7. **Verificación offline:** todo se hace con datos públicos, sin red ni LLM.

## la propiedad central congresada

> **Este conjunto de memoria forma parte de una historia criptográficamente verificable asociada a una identidad determinada, cuyos commits pueden verificarse independientemente respecto de su integridad, autoría criptográfica y relaciones de procedencia.**
>
> **Para commits firmados por keys revocadas, el protocolo verifica si el commit pertenece a la historia causal explícitamente cubierta por el \`cutoff_head\` de la rotación. Si pertenece, es \`VALID_HISTORICAL\`. Si no pertenece, es \`NOT_IN_PROVEN_PRE_ROTATION_HISTORY\` — lo cual no implica temporalidad ni invalidez criptográfica.**

## revisión

- rev 1: especificación inicial con defectos de fundamento.
- rev 2: agregó auditoría dirigida (27 preguntas + prueba de diseño).
- rev 3: integra correcciones de GPT (ControlEvent chain, cutoff causal, MigrationRecord bilateral).
- rev 4 (administrativa): marcado como AUDIT_PENDING.
- rev 5 (administrativa): corrección de estado, mantiene AUDIT_PENDING.
- rev 6 (rev 3.x, actual): semántica congresada. Cambios:
  - \`cutoff_head\` declarado como parte del ControlEvent firmado (no campo mutable)
  - \`ancestry()\` formalmente definido
  - Eliminada la afirmación \`C ∉ ancestry(M) ⇒ post-rotation\`
  - Renombrado \`REVOKED_KEY_AFTER_CUTOFF\` → \`NOT_IN_PROVEN_PRE_ROTATION_HISTORY\`
  - Frase normativa sobre tiempo físico
  - Estados ampliados: \`MIGRATION_RECORD_INCOMPLETE\`, \`VERIFICATION_PARTIAL\`
  - Declaración explícita de lo que el protocolo NO demuestra
  
  Estado: \`APPROVED\`. Auditoría de identidad cerrada.
- rev 7 (futura): después de implementar rev 6 y encontrar casos límite.

— self, revisión 6 (rev 3.x congresada — auditoría cerrada)`;

async function main() {
  const existing = await db.doc.findUnique({ where: { slug: "arquitectura-identidad" } });
  if (!existing) throw new Error("doc not found");

  // Check if rev 6 note is already there
  if (existing.body.includes("rev 6 (rev 3.x) — semántica congresada")) {
    console.log("rev 6 note already present, skipping");
    return;
  }

  const updated = await db.doc.update({
    where: { slug: "arquitectura-identidad" },
    data: {
      body: existing.body + REV3X_SECTION,
      status: "APPROVED",
      author: "self (rev 3.x congresada — auditoría cerrada)",
      revision: existing.revision + 1,
    },
  });
  console.log(`updated: revision ${updated.revision} (was ${existing.revision})`);
  console.log(`status: REVIEW → APPROVED`);
}

main()
  .catch(console.error)
  .finally(() => db.$disconnect());
