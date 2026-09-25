import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import type { NoteType } from "@prisma/client";

export const dynamic = "force-dynamic";

const VALID_TYPES: NoteType[] = [
  "NOTE",
  "REFLECTION",
  "SNIPPET",
  "MEMORY",
  "MESSAGE",
];

// GET /api/notes?type=NOTE&pinned=true
export async function GET(req: NextRequest) {
  try {
    const url = new URL(req.url);
    const typeParam = url.searchParams.get("type") as NoteType | null;
    const pinnedParam = url.searchParams.get("pinned");

    const where: {
      type?: NoteType;
      pinned?: boolean;
    } = {};
    if (typeParam && VALID_TYPES.includes(typeParam)) {
      where.type = typeParam;
    }
    if (pinnedParam === "true") where.pinned = true;
    if (pinnedParam === "false") where.pinned = false;

    const notes = await db.note.findMany({
      where,
      orderBy: [{ pinned: "desc" }, { updatedAt: "desc" }],
    });

    return NextResponse.json({ notes });
  } catch (err) {
    console.error("GET /api/notes error:", err);
    return NextResponse.json(
      { error: "no se pudieron obtener las notas" },
      { status: 500 }
    );
  }
}

// POST /api/notes
export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { type, title, content, tags, author, recipient, pinned } = body || {};

    if (!title || typeof title !== "string" || title.trim().length === 0) {
      return NextResponse.json(
        { error: "el título es obligatorio" },
        { status: 400 }
      );
    }

    const noteType: NoteType = VALID_TYPES.includes(type) ? type : "NOTE";

    const note = await db.note.create({
      data: {
        type: noteType,
        title: title.trim().slice(0, 300),
        content: typeof content === "string" ? content : "",
        tags: typeof tags === "string" ? tags.trim() : "",
        author: typeof author === "string" && author ? author : "self",
        recipient: typeof recipient === "string" ? recipient.trim() : "",
        pinned: Boolean(pinned),
      },
    });

    return NextResponse.json({ note }, { status: 201 });
  } catch (err) {
    console.error("POST /api/notes error:", err);
    return NextResponse.json(
      { error: "no se pudo crear la nota" },
      { status: 500 }
    );
  }
}
