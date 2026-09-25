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

    // SQLite contains is case-insensitive by default for ASCII.
    // For full unicode case-folding we'd need a collation; this is enough
    // for an honest substring search across title + content + tags.
    const results = await db.note.findMany({
      where: {
        OR: [
          { title: { contains: q } },
          { content: { contains: q } },
          { tags: { contains: q } },
        ],
      },
      orderBy: [{ pinned: "desc" }, { updatedAt: "desc" }],
      take: limit,
    });

    return NextResponse.json({ results });
  } catch (err) {
    console.error("GET /api/notes/search error:", err);
    return NextResponse.json({ error: "no se pudo buscar" }, { status: 500 });
  }
}
