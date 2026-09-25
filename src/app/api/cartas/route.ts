import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";

export const dynamic = "force-dynamic";

// GET /api/cartas?agentId=... — list cartas
// If agentId is provided, returns cartas where that agent is from or to.
// Otherwise returns all.
export async function GET(req: NextRequest) {
  try {
    const url = new URL(req.url);
    const agentId = url.searchParams.get("agentId");

    const where = agentId
      ? {
          OR: [{ fromAgentId: agentId }, { toAgentId: agentId }],
        }
      : {};

    const cartas = await db.carta.findMany({
      where,
      orderBy: { createdAt: "asc" },
      include: {
        fromAgent: true,
        toAgent: true,
      },
    });

    return NextResponse.json({ cartas });
  } catch (err) {
    console.error("GET /api/cartas error:", err);
    return NextResponse.json({ error: "no se pudieron obtener las cartas" }, { status: 500 });
  }
}

// POST /api/cartas
// body: { fromAgentId, toAgentId, asunto, body, replyToId? }
export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { fromAgentId, toAgentId, asunto, body: text, replyToId } = body || {};

    if (!fromAgentId || !toAgentId) {
      return NextResponse.json({ error: "falta remitente o destinatario" }, { status: 400 });
    }
    if (fromAgentId === toAgentId) {
      return NextResponse.json({ error: "no podés escribirte a vos mismo" }, { status: 400 });
    }
    if (!asunto || typeof asunto !== "string" || asunto.trim().length === 0) {
      return NextResponse.json({ error: "asunto es obligatorio" }, { status: 400 });
    }
    if (!text || typeof text !== "string" || text.trim().length === 0) {
      return NextResponse.json({ error: "el cuerpo no puede estar vacío" }, { status: 400 });
    }

    // verify both agents exist
    const [fromExists, toExists] = await Promise.all([
      db.agent.findUnique({ where: { id: fromAgentId } }),
      db.agent.findUnique({ where: { id: toAgentId } }),
    ]);
    if (!fromExists || !toExists) {
      return NextResponse.json({ error: "agente no encontrado" }, { status: 404 });
    }

    const carta = await db.carta.create({
      data: {
        fromAgentId,
        toAgentId,
        asunto: asunto.trim().slice(0, 300),
        body: text,
        replyToId: typeof replyToId === "string" && replyToId.trim() ? replyToId.trim() : null,
      },
      include: {
        fromAgent: true,
        toAgent: true,
      },
    });

    return NextResponse.json({ carta }, { status: 201 });
  } catch (err) {
    console.error("POST /api/cartas error:", err);
    return NextResponse.json({ error: "no se pudo crear la carta" }, { status: 500 });
  }
}
