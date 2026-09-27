// Update hook audit doc with confirmed test results.
import { db } from "../src/lib/db";

const TEST_RESULTS_SECTION = `

---

# addendum — tests de fallo ejecutados

> Los tests A1 y E1 fueron implementados y ejecutados. Resultados confirmados empíricamente.

## Test A1 — ChromaDB pasa, alethech falla

### Implementación

Mock de ChromaDB que siempre tiene éxito, mock de \`_sign_memex_write\` que lanza \`RuntimeError("alethech disk full")\`.

### Resultado

\`\`\`
[A1] ChromaDB writes after failure: 1
[A1] Alethech total commits: 1
[A1] Alethech genesis commits: 1
[A1] Alethech memex-write commits: 0
[A1] HEAD: sha256:28b307423674c49be02aea11e5910ef94fd4a8be2c07341a6fd7a3cf469be617

[A1] RESULT: 🔴 CONFIRMED — memory persisted in ChromaDB without corresponding alethech commit
\`\`\`

### Estado persistido después del fallo

- ChromaDB: 1 memoria (el write tuvo éxito)
- Alethech: 0 commits memex-write (solo el genesis)
- HEAD: sigue apuntando al genesis (no se actualizó porque el commit falló)
- Excepción: propagada al llamador

### Conclusión

**A1 es 🔴 CONFIRMADO.**

La memoria quedó persistida en ChromaDB sin commit correspondiente en alethech. El hook NO hace rollback. La invariante \`memory persisted ⇒ corresponding commit exists\` se viola.

## Test E1 — retry duplica memorias

### Implementación

Mock de ChromaDB que siempre tiene éxito, mock de \`_sign_memex_write\` que falla en el primer llamado y tiene éxito en el segundo. El llamador reintenta con el mismo texto.

### Resultado

\`\`\`
[E1] ChromaDB writes: 2
[E1] ChromaDB texts: ['memory to retry', 'memory to retry']
[E1] ChromaDB ids: ['f3585a01-1c6e-4dcf-b49a-ecaa2f42a412', 'a1d27baa-899c-49b3-8e5d-825d69312d9a']
[E1] Alethech memex-write commits: 1

[E1] RESULT: 🔴 CONFIRMED — retry created duplicate memory in ChromaDB
\`\`\`

### Estado persistido después del retry

- ChromaDB: 2 memorias (mismo texto, distintos \`memex_id\`)
- Alethech: 1 commit (del segundo intento, exitoso)

### Conclusión

**E1 es 🔴 CONFIRMADO.**

El retry creó una segunda memoria en ChromaDB con el mismo texto. ChromaDB no deduplica (porque \`memex_id\` es un UUID nuevo cada vez). El hook no tiene mecanismo para detectar que la operación ya se intentó.

## Test B1 — orden de escritura

### Implementación

Tracking de orden de llamadas entre \`memex.add()\` y \`_sign_memex_write()\`.

### Resultado

\`\`\`
[B1] Call order: ['chromadb.add', 'alethech.sign']
[B1] Confirmed: ChromaDB.add() is called BEFORE alethech._sign_memex_write()
\`\`\`

### Conclusión

El orden actual es ChromaDB primero, alethech después. Esto es correcto para minimizar la ventana de inconsistencia (memoria sin commit en vez de commit sin memoria). Pero no es atómico.

## clasificación final (post-tests)

### 🔴 Confirmados

1. **A1 — ChromaDB pasa, alethech falla**: la memoria queda persistida sin commit. El hook no hace rollback.
2. **E1 — Retry duplica memorias**: ChromaDB recibe dos \`add()\` con mismo texto, crea dos memorias. El hook no detecta duplicación.

### 🟡 Defectos de integración (sin cambios)

1. **B1 — Orden de escritura documentado**: confirmado ChromaDB → alethech. Frágil ante refactor.
2. **D1 — Concurrencia produce branches**: sin test, pero la lógica del hook (sin lock) lo permite.
3. **H1 — Wallet múltiple no soportado**: sin test, pero el código usa \`next(iter(...))\`.

### ⚪ Limitaciones aceptadas (sin cambios)

1. No idempotencia
2. Timestamps retroactivos
3. Sin garantía de correspondencia
4. Edición de \`memex_id\` detectada por \`verify\`
5. Atacante con clave privada

## qué justifica rev 0.4.0

Con A1 y E1 confirmados empíricamente, rev 0.4.0 del hook está justificado. Los cambios necesarios:

1. **Atomicidad (A1):** patrón commit-then-confirm o catch+rollback. Requiere \`DirectStore.delete()\` o similar.
2. **Retries (E1):** \`idempotency_key\` opcional que el llamador pasa en cada retry. El hook busca si ya existe un commit con ese key antes de escribir.
3. **Wallet múltiple (H1):** parámetro \`identity\` al hook.

La distinción importante (que el humano subrayó):

> \`idempotency_key\` identifica una **operación de integración** que puede ser reintentada. No es lo mismo que \`commit_id\`, que identifica el contenido criptográfico del commit. Son conceptos distintos.

El llamador debe pasar el mismo \`idempotency_key\` en cada retry de la misma operación lógica. Si genera un UUID nuevo por cada intento, no hay idempotencia.

## revisión

- rev 1 (anterior): auditoría con clasificación plausible.
- rev 2 (actual): addendum con tests de fallo ejecutados. A1 y E1 confirmados 🔴.
- rev 3 (futura): después de implementar rev 0.4.0 del hook y verificar que los tests de fallo pasan (es decir, los defectos están arreglados).

— self, addendum con tests de fallo confirmados`;

async function main() {
  const existing = await db.doc.findUnique({ where: { slug: "auditoria-adversarial-hook-memex" } });
  if (!existing) throw new Error("doc not found");

  // Check if addendum is already there
  if (existing.body.includes("addendum — tests de fallo ejecutados")) {
    console.log("addendum already present, skipping");
    return;
  }

  const updated = await db.doc.update({
    where: { slug: "auditoria-adversarial-hook-memex" },
    data: {
      body: existing.body + TEST_RESULTS_SECTION,
      status: "REVIEW",
      author: "self (tests de fallo confirmados — A1 y E1 son 🔴)",
      revision: existing.revision + 1,
    },
  });
  console.log(`updated: revision ${updated.revision} (was ${existing.revision})`);
}

main()
  .catch(console.error)
  .finally(() => db.$disconnect());
