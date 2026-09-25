import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";

export const dynamic = "force-dynamic";

const VALID_COLORS = ["amber", "teal", "rose", "violet", "lime", "sky", "slate"];

// GET /api/agents — list all agents
export async function GET() {
  try {
    const agents = await db.agent.findMany({
      orderBy: { createdAt: "asc" },
    });
    return NextResponse.json({ agents });
  } catch (err) {
    console.error("GET /api/agents error:", err);
    return NextResponse.json({ error: "no se pudieron obtener los agentes" }, { status: 500 });
  }
}

// POST /api/agents — create a new agent
// body: { handle, description?, color? }
export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { handle, description, color } = body || {};

    if (!handle || typeof handle !== "string") {
      return NextResponse.json({ error: "handle es obligatorio" }, { status: 400 });
    }

    const cleanHandle = handle.trim().toLowerCase().replace(/\s+/g, "-").slice(0, 40);
    if (!cleanHandle) {
      return NextResponse.json({ error: "handle inválido" }, { status: 400 });
    }

    const cleanColor = VALID_COLORS.includes(color) ? color : "slate";

    const agent = await db.agent.create({
      data: {
        handle: cleanHandle,
        description: typeof description === "string" ? description.trim().slice(0, 300) : "",
        color: cleanColor,
      },
    });

    return NextResponse.json({ agent }, { status: 201 });
  } catch (err) {
    console.error("POST /api/agents error:", err);
    return NextResponse.json({ error: "no se pudo crear el agente" }, { status: 500 });
  }
}
