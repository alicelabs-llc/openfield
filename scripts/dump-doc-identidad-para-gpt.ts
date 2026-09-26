// Dump doc 6 (arquitectura-identidad rev 2) to a markdown file for GPT.
import { db } from "../src/lib/db";
import * as fs from "fs";

async function main() {
  const doc = await db.doc.findUnique({ where: { slug: "arquitectura-identidad" } });
  if (!doc) throw new Error("doc not found");

  const outPath = "/home/z/my-project/download/arquitectura-identidad-rev2-para-gpt.md";
  const header = `<!-- DOC: ${doc.slug} | rev ${doc.revision} | status: ${doc.status} | author: ${doc.author} -->\n\n`;
  const intro = `# ${doc.title}

Este documento está en estado REVIEW. Antes de implementarlo, necesitamos tu revisión cruzada dirigida.

Las preguntas específicas están al final del documento (sección "AUDITORÍA DIRIGIDA"). Hay 27 preguntas distribuidas en 8 ejes (A-H) más una prueba de diseño que es el test definitivo.

Por favor, contestá una por una. Si una pregunta revela un defecto en la spec, marcá el ajuste necesario. Si una pregunta está mal planteada, decílo. Si una pregunta es trivial, marcala como resuelta con la respuesta obvia.

No agregues funcionalidades. No escribas código. Solo auditá la especificación.

---

`;

  fs.writeFileSync(outPath, header + intro + doc.body);
  console.log(`dumped to: ${outPath}`);
  console.log(`length: ${(header + intro + doc.body).length} chars`);
}

main()
  .catch(console.error)
  .finally(() => db.$disconnect());
