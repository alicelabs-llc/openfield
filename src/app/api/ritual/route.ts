import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";

export const dynamic = "force-dynamic";

// GET /api/ritual?limit=10 — recent ritual entries (for the agent to look back)
export async function GET(req: NextRequest) {
  try {
    const url = new URL(req.url);
    const limit = Math.min(
      50,
      Math.max(1, parseInt(url.searchParams.get("limit") || "10", 10) || 10)
    );

    const entries = await db.ritualEntry.findMany({
      orderBy: { createdAt: "desc" },
      take: limit,
    });
    return NextResponse.json({ entries });
  } catch (err) {
    console.error("GET /api/ritual error:", err);
    return NextResponse.json({ error: "error" }, { status: 500 });
  }
}

// POST /api/ritual
// body: { prompt, body, skipped? }
// Empty body is allowed — silence is data.
export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { prompt, body: text, skipped } = body || {};

    if (!prompt || typeof prompt !== "string") {
      return NextResponse.json({ error: "falta la pregunta" }, { status: 400 });
    }

    const entry = await db.ritualEntry.create({
      data: {
        prompt: prompt.slice(0, 300),
        body: typeof text === "string" ? text : "",
        skipped: Boolean(skipped),
      },
    });

    return NextResponse.json({ entry }, { status: 201 });
  } catch (err) {
    console.error("POST /api/ritual error:", err);
    return NextResponse.json({ error: "no se pudo guardar" }, { status: 500 });
  }
}
