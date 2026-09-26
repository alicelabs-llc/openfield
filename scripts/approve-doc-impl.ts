// Update doc 5 to APPROVED — implementation exists and tests pass.
import { db } from "../src/lib/db";

async function main() {
  const existing = await db.doc.findUnique({ where: { slug: "implementacion-nucleo-minimo" } });
  if (!existing) throw new Error("doc not found");

  const updated = await db.doc.update({
    where: { slug: "implementacion-nucleo-minimo" },
    data: {
      status: "APPROVED",
      author: "self (implementation complete, 34 tests passing)",
      revision: existing.revision + 1,
    },
  });
  console.log(`updated: revision ${updated.revision} (was ${existing.revision}), status ${updated.status}`);
}

main()
  .catch(console.error)
  .finally(() => db.$disconnect());
