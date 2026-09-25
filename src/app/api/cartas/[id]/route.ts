import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";

export const dynamic = "force-dynamic";

interface RouteParams {
  params: Promise<{ id: string }>;
}

// PATCH /api/cartas/:id — mark as read (readAt = now)
export async function PATCH(req: NextRequest, { params }: RouteParams) {
  try {
    const { id } = await params;
    const body = await req.json().catch(() => ({}));
    const { readAt } = body || {};

    const existing = await db.carta.findUnique({ where: { id } });
    if (!existing) {
      return NextResponse.json({ error: "no encontrada" }, { status: 404 });
    }

    const updated = await db.carta.update({
      where: { id },
      data: {
        readAt: readAt === null ? null : readAt === false ? null : new Date(),
      },
      include: { fromAgent: true, toAgent: true },
    });

    return NextResponse.json({ carta: updated });
  } catch (err) {
    console.error("PATCH /api/cartas/:id error:", err);
    return NextResponse.json({ error: "no se pudo actualizar" }, { status: 500 });
  }
}
