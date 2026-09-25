import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";

export const dynamic = "force-dynamic";

interface RouteParams {
  params: Promise<{ id: string }>;
}

// GET /api/notes/:id
export async function GET(_req: NextRequest, { params }: RouteParams) {
  try {
    const { id } = await params;
    const note = await db.note.findUnique({ where: { id } });
    if (!note) {
      return NextResponse.json({ error: "no encontrada" }, { status: 404 });
    }
    return NextResponse.json({ note });
  } catch (err) {
    console.error("GET /api/notes/:id error:", err);
    return NextResponse.json({ error: "error" }, { status: 500 });
  }
}

// PATCH /api/notes/:id
export async function PATCH(req: NextRequest, { params }: RouteParams) {
  try {
    const { id } = await params;
    const body = await req.json();
    const { title, content, tags, type, pinned, author, recipient } = body || {};

    const existing = await db.note.findUnique({ where: { id } });
    if (!existing) {
      return NextResponse.json({ error: "no encontrada" }, { status: 404 });
    }

    const data: Record<string, unknown> = {};
    if (typeof title === "string") data.title = title.trim().slice(0, 300);
    if (typeof content === "string") data.content = content;
    if (typeof tags === "string") data.tags = tags.trim();
    if (typeof type === "string" && ["NOTE","REFLECTION","SNIPPET","MEMORY","MESSAGE"].includes(type)) {
      data.type = type;
    }
    if (typeof pinned === "boolean") data.pinned = pinned;
    if (typeof author === "string") data.author = author;
    if (typeof recipient === "string") data.recipient = recipient;

    const updated = await db.note.update({ where: { id }, data });
    return NextResponse.json({ note: updated });
  } catch (err) {
    console.error("PATCH /api/notes/:id error:", err);
    return NextResponse.json({ error: "no se pudo actualizar" }, { status: 500 });
  }
}

// DELETE /api/notes/:id
export async function DELETE(_req: NextRequest, { params }: RouteParams) {
  try {
    const { id } = await params;
    const existing = await db.note.findUnique({ where: { id } });
    if (!existing) {
      return NextResponse.json({ error: "no encontrada" }, { status: 404 });
    }
    await db.note.delete({ where: { id } });
    return NextResponse.json({ ok: true });
  } catch (err) {
    console.error("DELETE /api/notes/:id error:", err);
    return NextResponse.json({ error: "no se pudo eliminar" }, { status: 500 });
  }
}
