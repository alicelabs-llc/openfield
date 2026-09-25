import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";

export const dynamic = "force-dynamic";

// GET /api/notes/search?q=...&limit=50
export async function GET(req: NextRequest) {
  try {
    const url = new URL(req.url);
    const q = (url.searchParams.get("q") || "").trim();
    const limit = Math.min(
      100,
      Math.max(1, parseInt(url.searchParams.get("limit") || "50", 10) || 50)
    );

    if (!q) {
      return NextResponse.json({ results: [] });
    }

    // SQLite LIKE search on title + content + tags.
    // Not fancy, but actually works and is honest.
    const term = `%${q.toLowerCase()}%`;
    const results = await db.note.findMany({
      where: {
        OR: [
          { title: { contains: q, mode: "insensitive" } },
          { content: { contains: q, mode: "insensitive" } },
          { tags: { contains: q, mode: "insensitive" } },
        ],
      },
      orderBy: [{ pinned: "desc" }, { updatedAt: "desc" }],
      take: limit,
    });

    // term var kept for future use / debugging
    void term;

    return NextResponse.json({ results });
  } catch (err) {
    console.error("GET /api/notes/search error:", err);
    return NextResponse.json(
      { error: "no se pudo buscar" },
      { status: 500 }
    );
  }
}
