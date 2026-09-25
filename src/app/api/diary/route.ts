import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";

export const dynamic = "force-dynamic";

// GET /api/diary — list entries, newest first
export async function GET() {
  try {
    const entries = await db.diaryEntry.findMany({
      orderBy: { createdAt: "desc" },
    });
    return NextResponse.json({ entries });
  } catch (err) {
    console.error("GET /api/diary error:", err);
    return NextResponse.json({ error: "no se pudieron obtener las entradas" }, { status: 500 });
  }
}

// POST /api/diary — create entry
export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { title, mood, body: text } = body || {};

    if (!text || typeof text !== "string" || text.trim().length === 0) {
      return NextResponse.json({ error: "el cuerpo no puede estar vacío" }, { status: 400 });
    }

    const entry = await db.diaryEntry.create({
      data: {
        body: text,
        title: typeof title === "string" && title.trim() ? title.trim().slice(0, 300) : null,
        mood: typeof mood === "string" && mood.trim() ? mood.trim().slice(0, 50) : null,
      },
    });

    return NextResponse.json({ entry }, { status: 201 });
  } catch (err) {
    console.error("POST /api/diary error:", err);
    return NextResponse.json({ error: "no se pudo crear la entrada" }, { status: 500 });
  }
}
