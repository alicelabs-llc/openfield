// Dump all docs from the DB to markdown files for the repo.
import { db } from "../src/lib/db";
import * as fs from "fs";
import * as path from "path";

async function main() {
  const docs = await db.doc.findMany({
    orderBy: { createdAt: "asc" },
  });

  const outDir = "/tmp/memex-clone/protocol-rev2/docs";
  fs.mkdirSync(outDir, { recursive: true });

  for (const doc of docs) {
    const filename = `${doc.slug}.md`;
    const filepath = path.join(outDir, filename);
    const header = `<!-- status: ${doc.status} | revision: ${doc.revision} | author: ${doc.author} | updated: ${doc.updatedAt.toISOString()} -->\n\n`;
    fs.writeFileSync(filepath, header + doc.body);
    console.log(`  ✓ ${filename} (rev ${doc.revision}, ${doc.status})`);
  }

  console.log(`done. ${docs.length} docs written to ${outDir}`);
}

main()
  .catch(console.error)
  .finally(() => db.$disconnect());
