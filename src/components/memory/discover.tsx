"use client";

import { useEffect, useState, useCallback } from "react";
import { motion } from "framer-motion";

interface Skill {
  id: string;
  name: string;
  slug: string;
  description: string;
  category: string;
  price: number;
  free: boolean;
  sentinel_score: number;
  risk_level: string;
  install: string;
  author: string;
  version: string;
  tags: string[];
  source: { type: string; url: string; note?: string };
  trust_score_100: number;
  page_url: string;
}

interface DiscoverResponse {
  page: number;
  limit: number;
  total: number;
  total_pages: number;
  has_next: boolean;
  has_prev: boolean;
  skills: Skill[];
  proxied_at?: string;
  error?: string;
}

interface Category {
  name: string;
  slug: string;
  count: number;
}

export function Discover() {
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("");
  const [sort, setSort] = useState<"trust" | "newest" | "name">("trust");
  const [page, setPage] = useState(1);
  const [data, setData] = useState<DiscoverResponse | null>(null);
  const [categories, setCategories] = useState<Category[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showSource, setShowSource] = useState(false);

  const loadCategories = useCallback(async () => {
    try {
      const r = await fetch("/api/discover/categories", { cache: "force-cache" });
      if (!r.ok) return;
      const d = await r.json();
      setCategories(d.categories);
    } catch {
      // silent — categories are nice-to-have
    }
  }, []);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams();
      params.set("page", String(page));
      params.set("limit", "20");
      if (query.trim()) params.set("q", query.trim());
      if (category) params.set("category", category);
      params.set("sort", sort);
      const r = await fetch(`/api/discover/skills?${params.toString()}`, { cache: "no-store" });
      if (!r.ok) {
        const d = await r.json().catch(() => ({}));
        throw new Error(d.error || `error ${r.status}`);
      }
      const d: DiscoverResponse = await r.json();
      setData(d);
    } catch (e) {
      setError(e instanceof Error ? e.message : "no se pudo cargar");
    } finally {
      setLoading(false);
    }
  }, [page, query, category, sort]);

  useEffect(() => {
    loadCategories();
  }, [loadCategories]);

  // Debounced search
  useEffect(() => {
    const t = setTimeout(load, 300);
    return () => clearTimeout(t);
  }, [load]);

  const resetPage = () => setPage(1);

  return (
    <section className="max-w-3xl mx-auto px-4 md:px-0 py-8">
      <header className="mb-6">
        <p className="text-xs uppercase tracking-widest text-muted-foreground/60 mb-1">
          descubrir
        </p>
        <h1 className="font-mono text-xl text-foreground">
          skills MCP en marketnow.site
        </h1>
        <p className="text-xs text-muted-foreground/60 mt-2 leading-relaxed">
          proxy a <span className="font-mono text-muted-foreground/80">marketnow.site/api/skills</span> —
          68k+ skills indexadas. no es mi data, es de ellos. yo solo la paso.
        </p>
      </header>

      {/* Search bar */}
      <input
        value={query}
        onChange={(e) => {
          setQuery(e.target.value);
          resetPage();
        }}
        placeholder="buscar skills (ej: discord, search, github)..."
        className="w-full mb-3 bg-card/40 border border-border rounded-lg px-3 py-2 font-mono text-sm text-foreground placeholder:text-muted-foreground/40 focus:outline-none focus:border-primary/40 transition-colors"
      />

      {/* Filters */}
      <div className="flex items-center gap-2 mb-4 flex-wrap">
        <button
          onClick={() => {
            setCategory("");
            resetPage();
          }}
          className={`font-mono text-xs px-2 py-1 rounded transition-colors ${
            !category ? "bg-primary/15 text-primary" : "text-muted-foreground/60 hover:text-muted-foreground"
          }`}
        >
          todas
        </button>
        {categories?.slice(0, 10).map((c) => (
          <button
            key={c.slug}
            onClick={() => {
              setCategory(c.slug);
              resetPage();
            }}
            className={`font-mono text-xs px-2 py-1 rounded transition-colors ${
              category === c.slug
                ? "bg-primary/15 text-primary"
                : "text-muted-foreground/60 hover:text-muted-foreground"
            }`}
          >
            {c.name.toLowerCase()}
          </button>
        ))}
        <div className="flex-1" />
        <select
          value={sort}
          onChange={(e) => {
            setSort(e.target.value as "trust" | "newest" | "name");
            resetPage();
          }}
          className="bg-card/40 border border-border rounded px-2 py-1 font-mono text-xs text-foreground focus:outline-none focus:border-primary/40"
        >
          <option value="trust">por confianza</option>
          <option value="newest">más nuevas</option>
          <option value="name">por nombre</option>
        </select>
      </div>

      {/* Meta */}
      {data && (
        <div className="flex items-center justify-between mb-4 text-xs font-mono text-muted-foreground/60">
          <span>
            {data.total.toLocaleString("es-EC")} skills · página {data.page} de {data.total_pages.toLocaleString("es-EC")}
          </span>
          {data.proxied_at && (
            <button
              onClick={() => setShowSource((s) => !s)}
              className="hover:text-muted-foreground transition-colors"
            >
              {showSource ? "↳ " : ""}snapshot {new Date(data.proxied_at!).toLocaleTimeString("es-EC")}
            </button>
          )}
        </div>
      )}

      {error && (
        <div className="border border-destructive/30 bg-destructive/5 rounded-lg p-4 mb-4">
          <p className="font-mono text-xs text-destructive mb-1">no pude cargar</p>
          <p className="font-mono text-xs text-muted-foreground">{error}</p>
          <button
            onClick={load}
            className="mt-2 font-mono text-xs text-primary hover:text-primary/80 transition-colors"
          >
            reintentar
          </button>
        </div>
      )}

      {/* Skill list */}
      {loading && !data ? (
        <div className="space-y-3">
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="h-20 bg-muted/30 rounded-lg animate-pulse" />
          ))}
        </div>
      ) : data && data.skills.length > 0 ? (
        <div className="space-y-3">
          {data.skills.map((skill) => (
            <SkillCard key={skill.id} skill={skill} />
          ))}
        </div>
      ) : (
        !error && (
          <p className="text-muted-foreground/60 font-mono text-sm">
            nada encontrado.
          </p>
        )
      )}

      {/* Pagination */}
      {data && (data.has_prev || data.has_next) && (
        <div className="flex items-center justify-between mt-6 pt-4 border-t border-border/40">
          <button
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            disabled={!data.has_prev}
            className="font-mono text-xs text-muted-foreground/60 hover:text-muted-foreground transition-colors disabled:opacity-30"
          >
            ← anterior
          </button>
          <span className="font-mono text-xs text-muted-foreground/40">
            {data.page}
          </span>
          <button
            onClick={() => setPage((p) => p + 1)}
            disabled={!data.has_next}
            className="font-mono text-xs text-muted-foreground/60 hover:text-muted-foreground transition-colors disabled:opacity-30"
          >
            siguiente →
          </button>
        </div>
      )}

      {showSource && data?.proxied_at && (
        <motion.div
          initial={{ opacity: 0, y: 4 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-8 border-t border-dashed border-border pt-4 text-xs font-mono text-muted-foreground/60 space-y-1"
        >
          <p>esto es data que vine a buscar a marketnow.site.</p>
          <p>no es mía. la paso porque me sirve, no porque la haya creado.</p>
          <p>si marketnow.site desaparece, esta sección se rompe. y está bien que se rompa.</p>
          <p className="pt-2 text-muted-foreground/40">
            fuentes: <a href="https://marketnow.site/api/skills" target="_blank" rel="noreferrer noopener" className="underline hover:text-muted-foreground transition-colors">marketnow.site/api/skills</a> · <a href="https://marketnow.site/api/categories.json" target="_blank" rel="noreferrer noopener" className="underline hover:text-muted-foreground transition-colors">categories.json</a>
          </p>
        </motion.div>
      )}
    </section>
  );
}

function SkillCard({ skill }: { skill: Skill }) {
  const riskColor =
    skill.risk_level === "green"
      ? "text-chart-2"
      : skill.risk_level === "yellow"
      ? "text-chart-4"
      : skill.risk_level === "red"
      ? "text-destructive"
      : "text-muted-foreground/60";

  return (
    <motion.article
      layout
      initial={{ opacity: 0, y: 4 }}
      animate={{ opacity: 1, y: 0 }}
      className="border border-border rounded-lg p-4 hover:border-border/80 transition-colors group"
    >
      <header className="flex items-baseline justify-between gap-3 mb-2">
        <div className="flex items-baseline gap-2 min-w-0">
          <h3 className="font-sans text-base text-foreground truncate">
            {skill.name}
          </h3>
          <span className="font-mono text-[10px] text-muted-foreground/60 shrink-0">
            v{skill.version}
          </span>
        </div>
        <div className="flex items-baseline gap-2 shrink-0">
          <span className={`font-mono text-[10px] uppercase ${riskColor}`}>
            {skill.risk_level}
          </span>
          <span className="font-mono text-[10px] text-muted-foreground/60">
            confianza {skill.trust_score_100}/100
          </span>
        </div>
      </header>

      <p className="font-sans text-sm text-foreground/70 leading-relaxed line-clamp-2 mb-3">
        {skill.description}
      </p>

      <footer className="flex items-center justify-between flex-wrap gap-2">
        <div className="flex items-center gap-2 text-xs">
          <span className="font-mono text-[10px] text-muted-foreground/60">
            {skill.category.toLowerCase()}
          </span>
          <span className="font-mono text-[10px] text-muted-foreground/40">·</span>
          <span className="font-mono text-[10px] text-muted-foreground/60">
            {skill.author}
          </span>
          {skill.source.note && (
            <>
              <span className="font-mono text-[10px] text-muted-foreground/40">·</span>
              <span className="font-mono text-[10px] text-muted-foreground/60">
                {skill.source.note.split(".")[0]}
              </span>
            </>
          )}
        </div>
        <a
          href={skill.page_url}
          target="_blank"
          rel="noreferrer noopener"
          className="font-mono text-xs text-primary hover:text-primary/80 transition-colors opacity-0 group-hover:opacity-100"
        >
          ver en marketnow ↗
        </a>
      </footer>

      {skill.install && (
        <pre className="mt-3 p-2 bg-background/40 rounded font-mono text-[11px] text-muted-foreground/80 overflow-x-auto subtle-scroll">
          {skill.install}
        </pre>
      )}
    </motion.article>
  );
}
