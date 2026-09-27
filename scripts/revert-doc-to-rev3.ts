// Revert doc to clean rev 3 — strip the AUDIT_PENDING note + propuesta regla central.
// Move those to a separate file outside the doc.
import { db } from "../src/lib/db";

const AUDIT_PENDING_MARKER = "\n\n---\n\n# rev 3.1 — estado: auditoría adversarial pendiente";

async function main() {
  const existing = await db.doc.findUnique({ where: { slug: "arquitectura-identidad" } });
  if (!existing) throw new Error("doc not found");

  const body = existing.body;
  const idx = body.indexOf(AUDIT_PENDING_MARKER);
  if (idx === -1) {
    console.log("marker not found, nothing to strip");
    return;
  }

  const cleanBody = body.slice(0, idx);

  // Save the stripped content to a separate file for reference
  const fs = await import("fs");
  const auditContent = body.slice(idx);
  fs.writeFileSync("/home/z/my-project/download/audit-pending-removed.md", auditContent);
  console.log(`stripped ${auditContent.length} chars to /home/z/my-project/download/audit-pending-removed.md`);

  // Revert doc to clean rev 3
  const updated = await db.doc.update({
    where: { slug: "arquitectura-identidad" },
    data: {
      body: cleanBody,
      // keep revision 4 because we did change the doc — but mark it as the clean rev 3 state
      // actually, let's revert to rev 3 entirely by setting revision back
      revision: 3, // revert
      author: "self (integra auditoría GPT)",
      status: "REVIEW",
    },
  });
  console.log(`reverted: revision ${updated.revision} (was ${existing.revision})`);
  console.log(`body length: ${existing.body.length} → ${updated.body.length} chars`);
}

main()
  .catch(console.error)
  .finally(() => db.$disconnect());
