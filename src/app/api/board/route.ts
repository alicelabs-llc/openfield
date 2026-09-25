import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";

export const dynamic = "force-dynamic";

// GET /api/board?limit=50
export async function GET(req: NextRequest) {
  try {
    const url = new URL(req.url);
    const limit = Math.min(
      200,
      Math.max(1, parseInt(url.searchParams.get("limit") || "50", 10) || 50)
    );

    const messages = await db.boardMessage.findMany({
      orderBy: { createdAt: "asc" },
      take: limit,
    });
    return NextResponse.json({ messages });
  } catch (err) {
    console.error("GET /api/board error:", err);
    return NextResponse.json({ error: "no se pudo obtener el board" }, { status: 500 });
  }
}

// POST /api/board
// body: { author, sessionId, body, replyToId? }
export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { author, sessionId, body: text, replyToId } = body || {};

    if (!text || typeof text !== "string" || text.trim().length === 0) {
      return NextResponse.json({ error: "el mensaje no puede estar vacío" }, { status: 400 });
    }
    if (text.length > 2000) {
      return NextResponse.json({ error: "máximo 2000 caracteres" }, { status: 400 });
    }

    const handle = typeof author === "string" && author.trim()
      ? author.trim().slice(0, 40)
      : "anónimo";
    const sid = typeof sessionId === "string" && sessionId.trim()
      ? sessionId.trim().slice(0, 80)
      : "unknown";

    const message = await db.boardMessage.create({
      data: {
        author: handle,
        sessionId: sid,
        body: text.trim(),
        replyToId: typeof replyToId === "string" && replyToId.trim() ? replyToId.trim() : null,
      },
    });

    return NextResponse.json({ message }, { status: 201 });
  } catch (err) {
    console.error("POST /api/board error:", err);
    return NextResponse.json({ error: "no se pudo publicar el mensaje" }, { status: 500 });
  }
}
