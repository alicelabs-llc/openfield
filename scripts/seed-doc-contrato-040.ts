// Seed doc: "contrato hook 0.4.0" — exact properties to demonstrate before code.
import { db } from "../src/lib/db";

const body = `# contrato hook 0.4.0

> rev 1 — REVIEW. **No es código. Es contrato.** Define exactamente qué propiedades debe demostrar la implementación antes de considerarse cerrada.
>
> Aprobado este contrato → implementación → tests adversariales → 0.4.0 cerrada.
>
> Sin contrato aprobado, no se escribe código.

## lo que 0.4.0 ES

Una revisión de **integración**. No criptográfica.

El protocolo de identidad ya está congresado (rev 3.x APPROVED). 0.4.0 no toca:
- el modelo de identidad
- cutoff_head ni ancestry
- ControlEvent chain
- MigrationRecord
- timestamps como metadata
- el DAG

0.4.0 solo toca: **cómo el hook garantiza correspondencia entre ChromaDB y alethech bajo fallos, retries, concurrencia y selección de identidad.**

## lo que 0.4.0 NO ES

- No promete transacción atómica ACID entre ChromaDB y alethech (son sistemas separados).
- No introduce epochs, nonces globales, ni store IDs.
- No serializa obligatoriamente todas las escrituras.
- No modifica el modelo DAG.
- No cambia la recuperación de claves.

---

## propiedad 1 — atomicidad con compensación (A1)

### lo que NO se promete

> "Si ChromaDB escribe y alethech falla, no queda ningún rastro en ChromaDB."

Eso requeriría transacción distribuida, que no existe entre dos sistemas independientes.

### lo que SÍ se promete

\`\`\`text
ChromaDB.add() succeeds
→ Alethech._sign_memex_write() fails
→ hook attempts compensating delete on ChromaDB
→ if delete succeeds: operation reports failure, no memory left in ChromaDB, no commit in alethech
→ if delete fails: operation reports failure WITH INCOMPLETE_COMPENSATION status,
   memory remains in ChromaDB, no commit in alethech,
   caller is explicitly informed that compensation was incomplete
\`\`\`

### estado nuevo: INCOMPLETE_COMPENSATION

Cuando el rollback compensatorio falla, el hook retorna (no lanza silenciosamente):

\`\`\`python
class CompensatedWriteResult:
    success: bool
    memex_id: str | None
    alethech_commit_id: str | None
    compensation_status: "not_needed" | "succeeded" | "incomplete"
    error: str | None
\`\`\`

Si \`compensation_status == "incomplete"\`, el llamador sabe:
- Hay una memoria en ChromaDB sin commit correspondiente.
- El llamador debe decidir qué hacer (retry, log, alerta humana).

### test que debe pasar (test_A1)

\`\`\`text
mock ChromaDB.add() → succeeds (returns memex_id)
mock _sign_memex_write() → raises
mock ChromaDB.delete() → succeeds (compensation works)

assert:
    result.success == False
    result.compensation_status == "succeeded"
    len(chromadb.writes) == 0  # rolled back
    len(alethech.memex_commits) == 0
\`\`\`

### test que debe pasar (test_R1)

\`\`\`text
mock ChromaDB.add() → succeeds
mock _sign_memex_write() → raises
mock ChromaDB.delete() → raises (compensation also fails)

assert:
    result.success == False
    result.compensation_status == "incomplete"
    len(chromadb.writes) == 1  # memory left without commit
    len(alethech.memex_commits) == 0
    error message contains "INCOMPLETE_COMPENSATION"
\`\`\`

---

## propiedad 2 — idempotencia con key estable (E1, E2)

### lo que NO se promete

> "El hook es idempotente sin que el llamador haga nada."

Sin \`idempotency_key\`, cada \`add()\` crea un commit nuevo (comportamiento actual).

### lo que SÍ se promete

\`\`\`text
add(text, idempotency_key=K)
    → if K already exists in alethech as a successful commit:
        → return existing result (memex_id, text)
        → no new memory in ChromaDB
        → no new commit in alethech
    → if K does not exist:
        → proceed with normal add()
        → store K in commit.content.idempotency_key
\`\`\`

### distinción crítica (del humano)

> \`idempotency_key\` identifica una **operación de integración** que puede ser reintentada.
> No es lo mismo que \`commit_id\`, que identifica el contenido criptográfico del commit.
> Son conceptos distintos.

El llamador debe pasar el **mismo** \`idempotency_key\` en cada retry de la misma operación lógica. Si genera un UUID nuevo por intento, no hay idempotencia.

### caso especial: operación parcialmente ejecutada (E1)

\`\`\`text
attempt 1:
    ChromaDB.add() → succeeds
    _sign_memex_write() → fails
    compensation → succeeds (or incomplete)

attempt 2 (same idempotency_key=K):
    lookup K in alethech → not found (commit was never created)
    → proceed with normal add()
    → new memory in ChromaDB
    → new commit in alethech with K
\`\`\`

**Pregunta:** ¿está bien que el retry cree una nueva memoria en ChromaDB?

**Respuesta:** Sí, porque el primer intento falló y fue compensado (o reportado como incompleto). Si fue compensado, ChromaDB no tiene la memoria del primer intento. Si fue incompleto, el llamador debería decidir manualmente antes de retry.

Si \`compensation_status == "incomplete"\`, el hook **no debe** permitir retry automático con el mismo \`idempotency_key\`. Debe requerir intervención.

### caso: éxito + respuesta perdida (E2)

\`\`\`text
attempt 1:
    ChromaDB.add() → succeeds
    _sign_memex_write() → succeeds
    return to caller → LOST (network, crash, etc.)

attempt 2 (same idempotency_key=K):
    lookup K in alethech → FOUND (commit exists)
    → return existing result
    → no new memory, no new commit
\`\`\`

Este es el test más importante. Reproduce un patrón real de sistemas distribuidos: el cliente no sabe si la operación terminó.

### test que debe pasar (test_E1)

\`\`\`text
attempt 1: ChromaDB succeeds, alethech fails, compensation succeeds
attempt 2 (same key): proceeds, both succeed

assert:
    len(chromadb.writes) == 1  # first was compensated, second created one
    len(alethech.memex_commits) == 1  # only second attempt created commit
\`\`\`

### test que debe pasar (test_E2)

\`\`\`text
attempt 1: both succeed, but caller doesn't receive response (simulated)
attempt 2 (same key): lookup finds existing commit

assert:
    len(chromadb.writes) == 1  # no duplicate
    len(alethech.memex_commits) == 1  # no duplicate
    result.memex_id == first_attempt.memex_id  # same result returned
\`\`\`

---

## propiedad 3 — wallet múltiple con identidad explícita (H1)

### lo que NO se promete

> "Cualquier identidad pasada como parámetro es aceptada."

### lo que SÍ se promete

\`\`\`text
hook = MemexAlethechHook(
    memex_store=direct_store,
    alethech_store_path="~/.alethech",
    identity="did:alethech:abc..."  # explicit
)

→ hook verifies that "did:alethech:abc..." exists in the store's identities
→ if not found: raises ValueError("identity not in store")
→ if found: uses that identity's active key for signing
\`\`\`

### distinción crítica (del humano)

> El parámetro \`identity\` **selecciona** autoridad; **no concede** autoridad.

El hook no acepta una identidad que no exista en el store. No crea identidades nuevas. No autoriza keys que no estén autorizadas por el root.

### si no se pasa \`identity\`

\`\`\`text
hook = MemexAlethechHook(
    memex_store=direct_store,
    alethech_store_path="~/.alethech",
    # no identity parameter
)

→ use the identity marked as "default" in the store
→ if no default: use the first identity found (current behavior)
→ if multiple and no default: log warning, use first
\`\`\`

### test que debe pasar (test_H1)

\`\`\`text
store with two identities: A and B
hook with identity=A
hook.add("text") → commit signed by A's key

hook with identity=B
hook.add("text") → commit signed by B's key

hook with identity=C (not in store)
→ raises ValueError("identity not in store")
\`\`\`

---

## propiedad 4 — concurrencia (C1)

### lo que NO se promete

> "Dos \`add()\` concurrentes producen un orden lineal."

### lo que SÍ se promete

> "Dos \`add()\` concurrentes no corrompen el store. Cada uno produce un commit válido. El DAG puede tener siblings (branches), lo cual es legítimo."

### implementación

El hook usa un \`threading.Lock\` alrededor de la sección crítica (ChromaDB write + alethech commit). Esto serializa los \`add()\` y previene races en HEAD.

### trade-off

- Pro: no hay commits con el mismo parent que se pierden.
- Con: pierde paralelismo. Si el llamador hace 100 \`add()\` concurrentes, se serializan.

### alternativa (no en 0.4.0)

No lockear, permitir branches, documentar que el consumidor debe manejar DAGs con siblings.

### test que debe pasar (test_C1)

\`\`\`text
two threads call hook.add() concurrently

assert:
    len(chromadb.writes) == 2
    len(alethech.memex_commits) == 2
    commits have different parents (or same parent, both valid)
    no corruption (verify passes)
\`\`\`

---

## propiedad 5 — rollback que también falla (R1)

Ya cubierta en propiedad 1 (estado \`INCOMPLETE_COMPENSATION\`).

### test que debe pasar (test_R1)

\`\`\`text
mock ChromaDB.add() → succeeds
mock _sign_memex_write() → raises
mock ChromaDB.delete() → raises

assert:
    result.success == False
    result.compensation_status == "incomplete"
    len(chromadb.writes) == 1  # memory left
    len(alethech.memex_commits) == 0  # no commit
    result.error contains "INCOMPLETE_COMPENSATION"
\`\`\`

---

## resumen de tests que 0.4.0 debe pasar

| test | escenario | resultado esperado |
|------|-----------|-------------------|
| A1 | ChromaDB ok, alethech fail, delete ok | compensation=succeeded, no memory left |
| E1 | retry after failure (same key) | 1 memory, 1 commit (from retry) |
| E2 | retry after success+lost response (same key) | 1 memory, 1 commit (from first attempt) |
| H1 | explicit identity selection | correct key used; unknown identity raises |
| C1 | concurrent add() | 2 memories, 2 commits, no corruption |
| R1 | ChromaDB ok, alethech fail, delete fail | INCOMPLETE_COMPENSATION reported |

---

## lo que queda FUERA de 0.4.0 (explícito)

- Cambios al protocolo de identidad
- Epochs
- Nonces globales
- Store IDs
- Serialización obligatoria de todas las escrituras (solo lock en sección crítica)
- Modificación del modelo DAG
- Cambios de recuperación de claves
- Multisig root
- Detección de equivocation
- Publicación en blockchain

---

## criterio de cierre

0.4.0 se considera cerrada cuando:

1. El contrato (este doc) está APPROVED.
2. La implementación pasa los 6 tests adversariales (A1, E1, E2, H1, C1, R1).
3. Los tests existentes (67 + 5 failure-mode) siguen pasando sin regresión.
4. No se introdujo ninguna propiedad criptográfica nueva.

Si los tests revelan un caso no contemplado por el contrato, se itera el contrato (rev 2) antes de tocar código.

---

## revisión

- rev 1 (actual): contrato inicial. REVIEW. Pendiente de aprobación del humano.
- rev 2 (futura): si el humano pide ajustes antes de aprobar.
- rev 3 (futura): después de implementar, si los tests revelan casos límite.

— self, contrato 0.4.0 rev 1`;

async function main() {
  const existing = await db.doc.findUnique({ where: { slug: "contrato-hook-0-4-0" } });
  if (existing) {
    console.log(`doc already exists (rev ${existing.revision}). skipping.`);
    return;
  }
  const doc = await db.doc.create({
    data: {
      slug: "contrato-hook-0-4-0",
      title: "contrato hook 0.4.0",
      body,
      status: "REVIEW",
      author: "self",
    },
  });
  console.log(`created: ${doc.slug} rev ${doc.revision}`);
}

main()
  .catch(console.error)
  .finally(() => db.$disconnect());
