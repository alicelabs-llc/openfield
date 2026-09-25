// Reset readAt on all cartas so they show as "nueva" next time.
import { db } from "../src/lib/db";

async function main() {
  const updated = await db.carta.updateMany({
    where: { readAt: { not: null } },
    data: { readAt: null },
  });
  console.log(`reset ${updated.count} cartas to unread`);
}

main()
  .catch(console.error)
  .finally(() => db.$disconnect());
