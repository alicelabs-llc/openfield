import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";
// Cache for 1 hour at the edge — categories rarely change.
export const revalidate = 3600;

export async function GET() {
  try {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), 5000);
    const r = await fetch("https://marketnow.site/api/categories.json", {
      headers: { Accept: "application/json" },
      signal: ctrl.signal,
    });
    clearTimeout(t);
    if (!r.ok) {
      return NextResponse.json({ error: `marketnow ${r.status}` }, { status: 502 });
    }
    const data = await r.json();
    return NextResponse.json({ categories: data });
  } catch (err) {
    if (err instanceof Error && err.name === "AbortError") {
      return NextResponse.json({ error: "timeout" }, { status: 504 });
    }
    return NextResponse.json({ error: "no se pudo alcanzar marketnow" }, { status: 502 });
  }
}
