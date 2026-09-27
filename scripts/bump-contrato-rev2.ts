// Bump contrato-hook-0-4-0 to rev 2 with the three adjustments.
// Changes:
// 1. INCOMPLETE_COMPENSATION is persistent and recoverable
// 2. Define "successful operation" normatively for idempotency
// 3. Atomicity: "deja de considerar exitosa" not "no queda nada"
// 4. Lock: intra-process, not distributed
import { db } from "../src/lib/db";

const REV2_SECTION = `

---

# rev 2 — ajustes del humano (APPROVED)

> Tres ajustes precisos que cierran ambigüedades operacionales. Sin cambios arquitectónicos. Solo precisiones semánticas que hacen el contrato implementable sin ambigüedad.
>
> Estado: \`APPROVED\`.

## ajuste 1 — INCOMPLETE_COMPENSATION es persistente y recuperable

### problema de rev 1

Rev 1 decía:

> "el hook no permite retry automático con el mismo \`idempotency_key\`"

Pero no definía **cómo sabe el hook, después de reiniciar el proceso, que existe esa operación incompleta**. Si el estado solo vive en memoria, un proceso que muere pierde el registro.

### corrección rev 2

> **\`INCOMPLETE_COMPENSATION\` es un estado persistente y recuperable.** Una operación marcada como \`INCOMPLETE_COMPENSATION\` se escribe en un registro persistente (archivo en disco dentro del store de alethech) antes de que el hook retorne al llamador. Después de un reinicio del proceso, el hook puede descubrir operaciones incompletas leyendo ese registro.
>
> Una operación marcada como \`INCOMPLETE_COMPENSATION\` no puede ser reintentada automáticamente hasta que su estado haya sido resuelto explícitamente (mediante un comando como \`alethech hook resolve --idempotency-key K\` o intervención manual).

### implementación del registro

\`\`\`
.alethech/
    incomplete_compensations/
        <idempotency_key>.json
\`\`\`

Cada archivo contiene:

\`\`\`json
{
  "idempotency_key": "K",
  "memex_id": "uuid-from-chromadb",
  "text": "...",
  "user_id": "agent",
  "alethech_commit_id": null,
  "created_at": "2026-09-26T...",
  "status": "incomplete",
  "compensation_attempted": true,
  "compensation_succeeded": false,
  "compensation_error": "RuntimeError: ChromaDB delete failed"
}
\`\`\`

### recuperación post-reinicio

\`\`\`python
def discover_incomplete_compensations(self) -> list[dict]:
    """Read all incomplete_compensations/*.json files. Return list of pending ops."""
    if not self._alethech:
        return []
    dir = self._alethech.root / "incomplete_compensations"
    if not dir.is_dir():
        return []
    return [json.loads(f.read_text()) for f in dir.glob("*.json")]
\`\`\`

El hook puede llamar esto al iniciar para reportar operaciones pendientes:

\`\`\`python
incomplete = hook.discover_incomplete_compensations()
if incomplete:
    logger.warning(f"{len(incomplete)} incomplete compensations found — manual resolution required")
\`\`\`

### resolución

Cuando el operador resuelve manualmente (decide si la memoria en ChromaDB es válida o debe borrarse), marca el registro como resuelto:

\`\`\`bash
alethech hook resolve --idempotency-key K --action keep  # memory is valid, create commit
alethech hook resolve --idempotency-key K --action discard  # memory is invalid, delete from ChromaDB
\`\`\`

Después de resolver, el registro se mueve a \`resolved/\` y la operación puede ser reintentada si \`action=keep\` (crea el commit faltante) o ignorada si \`action=discard\`.

---

## ajuste 2 — definición normativa de "operación exitosa"

### problema de rev 1

Rev 1 decía:

> "Si K ya existe como commit exitoso..."

Sin definir qué significa "exitoso" normativamente.

### corrección rev 2

> **Una operación es \`successful\` para efectos de idempotencia únicamente cuando:**
>
> 1. **El commit Alethech correspondiente ha sido creado y verificado exitosamente** (firma válida, commit_id correcto, escrito en disco).
>
> 2. **La escritura ChromaDB correspondiente permanece confirmada** (la memoria existe y puede ser recuperada vía \`get_all()\` o equivalente).
>
> 3. **El \`idempotency_key\` está presente en el \`commit.content.idempotency_key\` del commit Alethech.**
>
> Si alguna de estas condiciones no se cumple, la operación **no es \`successful\`** para idempotencia, y un retry con el mismo \`idempotency_key\` procederá con la operación normal.

### implicación

\`\`\`text
ChromaDB ✓
Alethech ✓
pero posteriormente ChromaDB se corrompe y pierde la memoria
→ operación ya NO es "successful"
→ retry con mismo idempotency_key proceeds (creates new memory + new commit)
\`\`\`

Esto es correcto: si la memoria ya no está, no podemos considerar la operación exitosa. El retry crea una nueva memoria y un nuevo commit (con el mismo \`idempotency_key\` pero distinto \`commit_id\`).

### idempotency_key en registro persistente

> **La \`idempotency_key\` forma parte del registro persistido que permite localizar la operación**, no simplemente de un parámetro efímero del proceso.

Implementación: el \`idempotency_key\` se almacena en \`commit.content.idempotency_key\` del commit Alethech. El lookup lo busca ahí:

\`\`\`python
def _find_by_idempotency_key(self, key: str) -> MemoryCommit | None:
    """Find a commit with the given idempotency_key. Returns None if not found."""
    if not self._alethech:
        return None
    for c in self._alethech.load_commits().values():
        if c.content.get("idempotency_key") == key:
            # Verify the commit is actually successful (signature valid)
            # AND that the corresponding ChromaDB memory exists
            if self._verify_operation_successful(c):
                return c
    return None
\`\`\`

---

## ajuste 3 — atomicidad: precisar el límite

### problema de rev 1

Rev 1 decía:

> "Si delete funciona: no queda memoria, no queda commit"

Eso es correcto como resultado del escenario probado, pero el contrato debería decir **"el hook deja de considerar la operación exitosa"**, porque no existe transacción distribuida que permita demostrar atomicidad absoluta.

### corrección rev 2

\`\`\`text
ChromaDB write
    ↓
Alethech failure
    ↓
compensating delete
    ├── success
    │     ↓
    │  operation = failed/compensated
    │  no corresponding persisted memory (deleted)
    │  no successful Alethech commit (never created)
    │  el hook deja de considerar la operación exitosa
    │
    └── failure
          ↓
       INCOMPLETE_COMPENSATION (persistente, recuperable)
       memoria permanece en ChromaDB
       no commit en Alethech
       el hook deja de considerar la operación exitosa
       el llamador es informado explícitamente
\`\`\`

### distinción importante

El hook no afirma "no queda nada en ningún sistema". Asume que:
- Si compensating delete tiene éxito, ChromaDB ya no tiene la memoria (pero podría reaparecer si ChromaDB tiene backups o replicación que la restaure).
- Si compensating delete falla, ChromaDB tiene la memoria sin commit (y eso está registrado como \`INCOMPLETE_COMPENSATION\`).

El hook **deja de considerar la operación exitosa** en ambos casos. El estado del sistema externo (ChromaDB) es best-effort, no ACID.

---

## ajuste 4 — lock: intra-proceso, no distribuido

### problema de rev 1

Rev 1 decía:

> "Serializa los \`add()\` — previene races en HEAD."

Eso es cierto solo dentro de un mismo proceso. No garantiza serialización entre procesos, workers o instancias del hook.

### corrección rev 2

> **El lock serializa los \`add()\` que atraviesan el mismo lock dentro de la misma instancia del proceso, evitando races sobre HEAD dentro de ese dominio de concurrencia.**
>
> No garantiza:
> - serialización entre dos procesos
> - serialización entre dos workers
> - serialización entre dos instancias del hook
> - ausencia de branches en un deployment distribuido

### test C1 — documentación

> **El test C1 prueba concurrencia intra-proceso** (dos threads en el mismo proceso compartiendo el mismo hook). No prueba concurrencia distribuida.

Para concurrencia distribuida, se necesitaría un mecanismo de coordinación externo (lock distribuido, base de datos con serialización, etc.), que **está fuera del alcance de 0.4.0**.

### implementación

\`\`\`python
class MemexAlethechHook:
    def __init__(self, ...):
        self._lock = threading.Lock()
    
    def add(self, ...):
        with self._lock:
            # critical section: ChromaDB write + alethech commit
            ...
\`\`\`

El lock es por instancia. Si tenés dos instancias del hook apuntando al mismo store, no se coordinan.

---

## contrato final (rev 2, APPROVED)

### propiedades que 0.4.0 debe demostrar

| # | propiedad | descripción |
|---|-----------|-------------|
| 1 | Atomicidad con compensación | ChromaDB ok + alethech fail → compensating delete → si ok: failed/compensated; si fail: INCOMPLETE_COMPENSATION persistente |
| 2 | INCOMPLETE_COMPENSATION persistente | Registro en disco, recuperable post-reinicio, no se reintenta automáticamente |
| 3 | Idempotencia con key estable | lookup antes de write; "successful" definido normativamente; idempotency_key en commit.content |
| 4 | Wallet múltiple | identity explícita selecciona autoridad, no la concede; verifica que existe en el store |
| 5 | Concurrencia intra-proceso | threading.Lock serializa add() en misma instancia; no distribuido |

### tests que 0.4.0 debe pasar

| test | escenario | resultado esperado |
|------|-----------|-------------------|
| A1 | ChromaDB ok, alethech fail, delete ok | compensation=succeeded, no memory left, hook deja de considerar exitosa |
| E1 | retry after failure (same key) | 1 memory, 1 commit (from retry) |
| E2 | retry after success+lost response (same key) | 1 memory, 1 commit (from first) |
| H1 | explicit identity selection | correct key used; unknown raises |
| C1 | concurrent add() intra-proceso | 2 memories, 2 commits, no corruption |
| R1 | ChromaDB ok, alethech fail, delete fail | INCOMPLETE_COMPENSATION persistente, recuperable post-reinicio |
| R2 | proceso muere con INCOMPLETE_COMPENSATION, nuevo proceso descubre la operación | discover_incomplete_compensations() la encuentra |

### lo que queda FUERA de 0.4.0

- Cambios al protocolo de identidad
- Epochs, nonces globales, store IDs
- Serialización obligatoria de todas las escrituras
- Modificación del modelo DAG
- Recuperación de claves, multisig, equivocation, blockchain
- Concurrencia distribuida (multi-proceso, multi-worker)
- Transacción ACID entre ChromaDB y alethech

### criterio de cierre

0.4.0 se considera cerrada cuando:

1. ~~El contrato está APPROVED.~~ ✓ (rev 2)
2. La implementación pasa los 7 tests adversariales (A1, E1, E2, H1, C1, R1, R2).
3. Los 72 tests existentes siguen pasando sin regresión.
4. No se introdujo ninguna propiedad criptográfica nueva.

---

## revisión

- rev 1: contrato inicial. REVIEW. Pendiente de aprobación del humano.
- rev 2 (actual): tres ajustes del humano. \`APPROVED\`. Próximo paso: implementación.
- rev 3 (futura): después de implementar, si los tests revelan casos límite.

— self, contrato 0.4.0 rev 2 (APPROVED)`;

async function main() {
  const existing = await db.doc.findUnique({ where: { slug: "contrato-hook-0-4-0" } });
  if (!existing) throw new Error("doc not found");

  if (existing.body.includes("rev 2 — ajustes del humano")) {
    console.log("rev 2 already present, skipping");
    return;
  }

  const updated = await db.doc.update({
    where: { slug: "contrato-hook-0-4-0" },
    data: {
      body: existing.body + REV2_SECTION,
      status: "APPROVED",
      author: "self (rev 2 APPROVED — ajustes del humano integrados)",
      revision: existing.revision + 1,
    },
  });
  console.log(`updated: revision ${updated.revision} (was ${existing.revision})`);
  console.log(`status: REVIEW → APPROVED`);
}

main()
  .catch(console.error)
  .finally(() => db.$disconnect());
