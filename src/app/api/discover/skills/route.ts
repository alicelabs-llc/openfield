import { NextRequest, NextResponse } from "next/server";

export const dynamic = "force-dynamic";
// Proxy to marketnow.site. We don't store anything; we just forward.
// This is honest: marketnow is the source of truth, not us.

const UPSTREAM = "https://marketnow.site/api/skills";

export async function GET(req: NextRequest) {
  try {
    const url = new URL(req.url);
    const q = url.searchParams.get("q") || "";
    const page = Math.max(1, Math.min(1000, parseInt(url.searchParams.get("page") || "1", 10) || 1));
    const limit = Math.min(50, Math.max(1, parseInt(url.searchParams.get("limit") || "20", 10) || 20));
    const category = url.searchParams.get("category") || "";
    const sort = url.searchParams.get("sort") || "trust";

    const params = new URLSearchParams();
    params.set("page", String(page));
    params.set("limit", String(limit));
    if (q) params.set("q", q);
    if (category) params.set("category", category);
    if (sort) params.set("sort", sort);

    // 8 second timeout — if marketnow is slow or down, fail gracefully.
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), 8000);

    const r = await fetch(`${UPSTREAM}?${params.toString()}`, {
      headers: { Accept: "application/json", "User-Agent": "un-sitio/1.0 (agent-memory)" },
      signal: ctrl.signal,
      cache: "no-store",
    });
    clearTimeout(t);

    if (!r.ok) {
      return NextResponse.json(
        { error: `marketnow respondió ${r.status}` },
        { status: 502 }
      );
    }

    const data = await r.json();
    // Pass through with one addition: a `proxied_at` timestamp so the client
    // knows the data is a snapshot.
    return NextResponse.json({ ...data, proxied_at: new Date().toISOString() });
  } catch (err) {
    if (err instanceof Error && err.name === "AbortError") {
      return NextResponse.json(
        { error: "marketnow tardó demasiado (timeout 8s)" },
        { status: 504 }
      );
    }
    console.error("GET /api/discover/skills error:", err);
    return NextResponse.json({ error: "no se pudo alcanzar marketnow" }, { status: 502 });
  }
}
