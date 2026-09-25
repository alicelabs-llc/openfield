import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import type { DocStatus } from "@prisma/client";

export const dynamic = "force-dynamic";

const VALID_STATUSES: DocStatus[] = ["DRAFT", "REVIEW", "APPROVED", "ARCHIVED"];

interface RouteParams {
  params: Promise<{ slug: string }>;
}

// GET /api/docs/[slug]
export async function GET(_req: NextRequest, { params }: RouteParams) {
  try {
    const { slug } = await params;
    const doc = await db.doc.findUnique({ where: { slug } });
    if (!doc) {
      return NextResponse.json({ error: "no encontrado" }, { status: 404 });
    }
    return NextResponse.json({ doc });
  } catch (err) {
    console.error("GET /api/docs/[slug] error:", err);
    return NextResponse.json({ error: "error" }, { status: 500 });
  }
}

// PATCH /api/docs/[slug] — update body, status, bump revision
export async function PATCH(req: NextRequest, { params }: RouteParams) {
  try {
    const { slug } = await params;
    const body = await req.json();
    const { title, body: text, status, author, bumpRevision } = body || {};

    const existing = await db.doc.findUnique({ where: { slug } });
    if (!existing) {
      return NextResponse.json({ error: "no encontrado" }, { status: 404 });
    }

    const data: Record<string, unknown> = {};
    if (typeof title === "string") data.title = title.trim().slice(0, 200);
    if (typeof text === "string") data.body = text;
    if (typeof status === "string" && VALID_STATUSES.includes(status as DocStatus)) {
      data.status = status;
    }
    if (typeof author === "string" && author) data.author = author;

    // bump revision when explicitly requested OR when body/title meaningfully changes
    const bodyChanged = typeof text === "string" && text !== existing.body;
    const titleChanged = typeof title === "string" && title.trim() !== existing.title;
    if (bumpRevision || bodyChanged || titleChanged) {
      data.revision = existing.revision + 1;
    }

    const updated = await db.doc.update({ where: { slug }, data });
    return NextResponse.json({ doc: updated });
  } catch (err) {
    console.error("PATCH /api/docs/[slug] error:", err);
    return NextResponse.json({ error: "no se pudo actualizar" }, { status: 500 });
  }
}
