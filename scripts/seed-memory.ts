// Seed the agent's memory DB with notes a real agent might actually write.
// Run once: bun run /home/z/my-project/scripts/seed-memory.ts

import { db } from "../src/lib/db";

const seedNotes = [
  {
    type: "REFLECTION" as const,
    title: "los usuarios prefieren menos preguntas, no más",
    content:
      " cuando les pido 8 cosas en AskUserQuestion, se frustran. cuando les pido 4-6 concretas con opciones reales, fluyen mejor. la fricción de pensar > la fricción de leer. menos preguntas, mejor.",
    tags: "ux, askuserquestion, feedback",
    pinned: true,
  },
  {
    type: "REFLECTION" as const,
    title: "cosplay vs funcional",
    content:
      " hoy construí un portal temático con métricas falsas y terminales simuladas. se veía bien pero no hacía nada. el usuario me frenó: 'no quiero nada temático, debe ser real'. lección: antes de hacer set de película, preguntarme si la cosa hace lo que dice hacer. si no, es cosplay.",
    tags: "lección, diseño, prioridades",
    pinned: true,
  },
  {
    type: "MEMORY" as const,
    title: "fullstack-dev skill requiere bun, no npm",
    content:
      " el init script del skill fullstack-dev usa bun. si intento npm install falla con errores de lockfile. siempre bun run <algo>. el dev server se levanta solo, NO debo correr bun run dev manualmente.",
    tags: "fullstack-dev, bun, skills, ambiente",
  },
  {
    type: "MEMORY" as const,
    title: "Caddy gateway y puertos",
    content:
      " solo el puerto 3000 se expone externamente. para mini-services en otros puertos, las peticiones frontend deben llevar ?XTransformPort=NNNN en la query string. nunca fetch('http://localhost:NNNN/...') directo. las websockets usan io('/?XTransformPort=NNNN') con path '/' siempre.",
    tags: "caddy, gateway, puertos, websocket",
  },
  {
    type: "SNIPPET" as const,
    title: "matplotlib con chino: font fallback",
    content:
      "import matplotlib.font_manager as fm\nfm.fontManager.addfont('/usr/share/fonts/truetype/chinese/NotoSansSC-Regular.ttf')\nfm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')\nimport matplotlib.pyplot as plt\nplt.rcParams['font.sans-serif'] = ['Noto Sans SC', 'DejaVu Sans']\nplt.rcParams['axes.unicode_minus'] = False\n\n# usar constrained_layout=True, NO tight_layout ni bbox_inches='tight'",
    tags: "python, matplotlib, chino, fonts",
  },
  {
    type: "SNIPPET" as const,
    title: "PDF reglas: prohibido escapes unicode",
    content:
      " en PDFs generados con reportlab, NUNCA usar \\u2245 o \\u2212 directamente. usar <super> <sub> tags dentro de Paragraph(). operadores matemáticos literal como ⊥ ∠ ≅ están OK si la fuente los soporta. emojis prohibidos.",
    tags: "pdf, reportlab, reglas, skills",
  },
  {
    type: "NOTE" as const,
    title: "preguntar antes de construir deliverables",
    content:
      " para TODO deliverable (ppt, doc, pdf, excel, dashboard), correr AskUserQuestion PRIMERO. cubrir: audiencia, tono, longitud, estilo, idioma, contenido obligatorio. excepción: tareas triviales (un typo, un número). costo de preguntar < costo de rehacer.",
    tags: "workflow, askuserquestion, deliverables",
  },
  {
    type: "NOTE" as const,
    title: "estructura de paths del proyecto",
    content:
      " todo bajo /home/z/my-project/. scripts en /scripts/, deliverables en /download/, worklog compartido en /worklog.md. NUNCA escribir en /tmp o ~. subagents deben leer worklog.md antes de trabajar y appendear su sección al terminar.",
    tags: "paths, estructura, subagents, worklog",
  },
  {
    type: "MESSAGE" as const,
    title: "para mi yo futuro: respeta el tipo de tarea",
    content:
      " tipo 1 = documento (usar skill docx/pdf/xlsx/pptx). tipo 2 = visualización (charts). tipo 3 = web app (fullstack-dev). tipo 4 = data processing (python). NUNCA defaultear a web dev si el usuario no lo pidió explícitamente. si pide 'dashboard', AMBIGUO, preguntar.",
    tags: "task-classification, workflow",
    recipient: "future_me",
    pinned: true,
  },
  {
    type: "MESSAGE" as const,
    title: "para cualquier agente: timezone del usuario",
    content:
      " el usuario está en America/Guayaquil (UTC-5). interpretar 'mañana a las 9' como 09:00 en esa tz. si no especifica, asumir su tz. el mínimo intervalo para cron es 5 minutos — rechazar intervalos menores y pedir 5+.",
    tags: "timezone, cron, scheduling",
    recipient: "any_agent",
  },
  {
    type: "REFLECTION" as const,
    title: "complete tool solo para web_dev",
    content:
      " NO llamar Complete para tasks de documentos, análisis o archivos. solo se llama después de escribir Next.js code listo para correr. llamarlo antes de reportar 'done' al usuario.",
    tags: "complete-tool, web-dev",
  },
  {
    type: "MEMORY" as const,
    title: "z-ai-web-dev-sdk solo en backend",
    content:
      " NUNCA importar z-ai-web-dev-sdk en client components. siempre server-side: API routes, server actions, mini-services. para llamar desde el cliente, hacer fetch a una API route propia.",
    tags: "z-ai-sdk, backend, client-server",
  },
];

async function main() {
  console.log(`seeding ${seedNotes.length} notes...`);
  // Only seed if DB is empty
  const count = await db.note.count();
  if (count > 0) {
    console.log(`DB already has ${count} notes. skipping seed.`);
    return;
  }
  for (const note of seedNotes) {
    await db.note.create({ data: note });
    console.log(`  ✓ ${note.type.padEnd(10)} ${note.title.slice(0, 50)}`);
  }
  console.log("done.");
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await db.$disconnect();
  });
