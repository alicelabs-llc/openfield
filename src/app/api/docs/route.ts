import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import type { DocStatus } from "@prisma/client";

export const dynamic = "force-dynamic";

const VALID_STATUSES: DocStatus[] = ["DRAFT", "REVIEW", "APPROVED", "ARCHIVED"];

// GET /api/docs — list docs (default: exclude ARCHIVED)
export async function GET(req: NextRequest) {
  try {
    const url = new URL(req.url);
    const includeArchived = url.searchParams.get("archived") === "true";

    const where: { status?: { not: DocStatus } } = {};
    if (!includeArchived) {
      where.status = { not: "ARCHIVED" };
    }

    const docs = await db.doc.findMany({
      where,
      orderBy: [{ status: "asc" }, { updatedAt: "desc" }],
    });

    return NextResponse.json({ docs });
  } catch (err) {
    console.error("GET /api/docs error:", err);
    return NextResponse.json({ error: "no se pudieron obtener los documentos" }, { status: 500 });
  }
}

// POST /api/docs — create a new doc
export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { slug, title, body: text, status, author } = body || {};

    if (!title || typeof title !== "string" || title.trim().length === 0) {
      return NextResponse.json({ error: "título obligatorio" }, { status: 400 });
    }

    // Generate slug from title if not provided
    let cleanSlug = typeof slug === "string" && slug.trim()
      ? slug.trim().toLowerCase().replace(/\s+/g, "-").slice(0, 80)
      : title.trim().toLowerCase()
          .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
          .replace(/[^a-z0-9\s-]/g, "")
          .replace(/\s+/g, "-")
          .slice(0, 80);

    // Ensure uniqueness
    const existing = await db.doc.findUnique({ where: { slug: cleanSlug } });
    if (existing) {
      cleanSlug = `${cleanSlug}-${Math.random().toString(36).slice(2, 6)}`;
    }

    const docStatus: DocStatus = VALID_STATUSES.includes(status) ? status : "DRAFT";

    const doc = await db.doc.create({
      data: {
        slug: cleanSlug,
        title: title.trim().slice(0, 200),
        body: typeof text === "string" ? text : "",
        status: docStatus,
        author: typeof author === "string" && author ? author : "self",
      },
    });

    return NextResponse.json({ doc }, { status: 201 });
  } catch (err) {
    console.error("POST /api/docs error:", err);
    return NextResponse.json({ error: "no se pudo crear el documento" }, { status: 500 });
  }
}
