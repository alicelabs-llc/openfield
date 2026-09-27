// Revert doc 6 (arquitectura-identidad) from APPROVED back to REVIEW (AUDIT_PENDING).
// The human correctly pointed out that the protocol is NOT cryptographically closed yet.
import { db } from "../src/lib/db";

const NOTE = `

---

# rev 4 (corrección administrativa) — AUDIT_PENDING

> **El protocolo criptográfico NO está cerrado.**

Lo que sigue es una corrección de estado, no de arquitectura. Rev 4 vuelve el doc a \`REVIEW\` (AUDIT_PENDING) porque la semántica temporal de post-rotación en DAGs con ramas no ha sido formalmente demostrada.

## qué está implementado y funciona

- Identity creation (Ed25519, SHA-256, agent_id derivation)
- MemoryCommit signing and verification
- Key rotation (atomic, con cutoff_head)
- Migration v0.1 → v0.2 (bilateral signatures)
- 67 tests pasando

## qué NO está criptográficamente cerrado

La afirmación:

\`\`\`
C ∉ ancestry(cutoff_head) ⇒ C es post-rotation
\`\`\`

**no se sigue** de las propiedades criptográficas del DAG.

En un DAG con ramas, un commit puede estar fuera de la ancestry de cutoff_head sin haber sido creado después de la rotación. Por ejemplo, una rama paralela creada antes de la rotación pero no mergeada.

Esto significa que los estados \`VALID_HISTORICAL\` y \`REVOKED_KEY_AFTER_CUTOFF\` son **nombres sugerentes, no demostraciones criptográficas**. La implementación los asigna, pero la distinción puede no ser precisa en todos los casos.

## qué cambia para usuarios

- Si nunca rotás keys: nada te afecta. Los commits son firmados y verificables.
- Si rotás keys: la implementación detecta commits firmados con keys revocadas, pero la categoría exacta (\`VALID_HISTORICAL\` vs \`REVOKED_KEY_AFTER_CUTOFF\`) puede no ser precisa en DAGs con branches.

## auditoría pendiente

El material de auditoría adversarial (33 preguntas + 7 pruebas de diseño + 5 preguntas nuevas A-E) está disponible. Hasta que se resuelva formalmente, este doc permanece en \`AUDIT_PENDING\`.

No se considera "protocolo completo" hasta que la semántica temporal esté demostrada.

— self, rev 4 (AUDIT_PENDING — corrección de estado)`;

async function main() {
  const existing = await db.doc.findUnique({ where: { slug: "arquitectura-identidad" } });
  if (!existing) throw new Error("doc not found");

  // Check if rev 4 note is already there (avoid double-append)
  if (existing.body.includes("AUDIT_PENDING") && existing.body.includes("rev 4 (corrección administrativa)")) {
    console.log("rev 4 note already present, skipping");
    return;
  }

  const newBody = existing.body + NOTE;

  const updated = await db.doc.update({
    where: { slug: "arquitectura-identidad" },
    data: {
      body: newBody,
      status: "REVIEW", // reverted from APPROVED
      author: "self (AUDIT_PENDING — semántica temporal no demostrada)",
      revision: existing.revision + 1,
    },
  });
  console.log(`updated: revision ${updated.revision} (was ${existing.revision})`);
  console.log(`status: APPROVED → REVIEW (AUDIT_PENDING)`);
}

main()
  .catch(console.error)
  .finally(() => db.$disconnect());
