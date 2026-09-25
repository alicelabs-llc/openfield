// Delete cartas whose subject starts with "prueba:" — clean test cartas.
// Run: bun run /home/z/my-project/scripts/clean-test-cartas.ts

import { db } from "../src/lib/db";

async function main() {
  const deleted = await db.carta.deleteMany({
    where: { asunto: { startsWith: "prueba:" } },
  });
  console.log(`deleted ${deleted.count} test cartas`);
}

main()
  .catch(console.error)
  .finally(() => db.$disconnect());
