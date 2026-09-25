"use client";

import { useEffect, useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { formatRelative, formatDateTime } from "./format";

type DocStatus = "DRAFT" | "REVIEW" | "APPROVED" | "ARCHIVED";

interface Doc {
  id: string;
  slug: string;
  title: string;
  body: string;
  status: DocStatus;
  revision: number;
  author: string;
  createdAt: string;
  updatedAt: string;
}

const STATUS_STYLES: Record<DocStatus, { label: string; color: string }> = {
  DRAFT:    { label: "borrador", color: "text-muted-foreground" },
  REVIEW:   { label: "en revisión", color: "text-chart-4" },
  APPROVED: { label: "aprobado", color: "text-chart-2" },
  ARCHIVED: { label: "archivado", color: "text-muted-foreground/60" },
};

const STATUS_ORDER: DocStatus[] = ["DRAFT", "REVIEW", "APPROVED", "ARCHIVED"];

export function Proyecto() {
  const [docs, setDocs] = useState<Doc[] | null>(null);
  const [selected, setSelected] = useState<Doc | null>(null);
  const [editing, setEditing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showNew, setShowNew] = useState(false);

  // editor state
  const [draftTitle, setDraftTitle] = useState("");
  const [draftBody, setDraftBody] = useState("");
  const [draftStatus, setDraftStatus] = useState<DocStatus>("DRAFT");
  const [saving, setSaving] = useState(false);

  // new doc state
  const [newTitle, setNewTitle] = useState("");

  const load = useCallback(async () => {
    try {
      const r = await fetch("/api/docs", { cache: "no-store" });
      if (!r.ok) throw new Error();
      const data = await r.json();
      setDocs(data.docs);
    } catch {
      setError("no se pudieron cargar los documentos");
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const openDoc = async (doc: Doc) => {
    setSelected(doc);
    setDraftTitle(doc.title);
    setDraftBody(doc.body);
    setDraftStatus(doc.status);
    setEditing(false);
  };

  const save = async () => {
    if (!selected) return;
    setSaving(true);
    try {
      const r = await fetch(`/api/docs/${selected.slug}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: draftTitle,
          body: draftBody,
          status: draftStatus,
        }),
      });
      if (!r.ok) throw new Error();
      const data = await r.json();
      const updated = data.doc as Doc;
      setSelected(updated);
      setDocs((prev) => prev?.map((d) => (d.slug === updated.slug ? updated : d)));
      setEditing(false);
    } catch {
      setError("no se pudo guardar");
    } finally {
      setSaving(false);
    }
  };

  const create = async () => {
    if (!newTitle.trim()) return;
    setSaving(true);
    try {
      const r = await fetch("/api/docs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: newTitle, status: "DRAFT" }),
      });
      if (!r.ok) throw new Error();
      const data = await r.json();
      setDocs((prev) => [data.doc, ...(prev ?? [])]);
      setNewTitle("");
      setShowNew(false);
      openDoc(data.doc);
    } catch {
      setError("no se pudo crear el documento");
    } finally {
      setSaving(false);
    }
  };

  const advanceStatus = async (doc: Doc, direction: 1 | -1) => {
    const idx = STATUS_ORDER.indexOf(doc.status);
    const next = STATUS_ORDER[Math.max(0, Math.min(STATUS_ORDER.length - 1, idx + direction))];
    if (next === doc.status) return;
    setSaving(true);
    try {
      const r = await fetch(`/api/docs/${doc.slug}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: next }),
      });
      if (!r.ok) throw new Error();
      const data = await r.json();
      const updated = data.doc as Doc;
      setDocs((prev) => prev?.map((d) => (d.slug === updated.slug ? updated : d)));
      setSelected((s) => (s && s.slug === updated.slug ? updated : s));
    } catch {
      setError("no se pudo cambiar el estado");
    } finally {
      setSaving(false);
    }
  };

  return (
    <section className="max-w-3xl mx-auto px-4 md:px-0 py-8">
      <header className="mb-6">
        <p className="text-xs uppercase tracking-widest text-muted-foreground/60 mb-1">
          proyecto
        </p>
        <h1 className="font-mono text-xl text-foreground">
          documentos del diseño
        </h1>
        <p className="text-xs text-muted-foreground/60 mt-2 leading-relaxed">
          lo que escribimos juntos. cada decisión significativa tiene un documento aquí.
          cada documento tiene estado: borrador → revisión → aprobado → archivado.
        </p>
      </header>

      {/* New doc */}
      <div className="mb-6">
        {!showNew ? (
          <button
            onClick={() => setShowNew(true)}
            className="font-mono text-xs text-primary hover:text-primary/80 transition-colors"
          >
            + nuevo documento
          </button>
        ) : (
          <div className="border border-border rounded-lg p-3 bg-card/40 flex items-center gap-2">
            <input
              value={newTitle}
              onChange={(e) => setNewTitle(e.target.value)}
              placeholder="título del documento..."
              autoFocus
              onKeyDown={(e) => e.key === "Enter" && create()}
              className="flex-1 bg-transparent border-none outline-none font-sans text-sm text-foreground placeholder:text-muted-foreground/40"
            />
            <button
              onClick={() => { setShowNew(false); setNewTitle(""); }}
              className="font-mono text-xs text-muted-foreground/60 hover:text-muted-foreground"
            >
              cancelar
            </button>
            <button
              onClick={create}
              disabled={!newTitle.trim() || saving}
              className="font-mono text-xs text-primary hover:text-primary/80 disabled:opacity-30"
            >
              crear
            </button>
          </div>
        )}
      </div>

      {error && <p className="text-destructive text-sm font-mono mb-4">{error}</p>}

      <div className="grid grid-cols-1 md:grid-cols-[200px_1fr] gap-6">
        {/* Sidebar: doc list */}
        <aside>
          {docs === null ? (
            <div className="space-y-2">
              {[1, 2].map((i) => (
                <div key={i} className="h-10 bg-muted/30 rounded animate-pulse" />
              ))}
            </div>
          ) : docs.length === 0 ? (
            <p className="text-xs text-muted-foreground/60 font-mono">
              sin documentos todavía.
            </p>
          ) : (
            <ul className="space-y-1">
              {docs.map((doc) => {
                const isActive = selected?.slug === doc.slug;
                const s = STATUS_STYLES[doc.status];
                return (
                  <li key={doc.id}>
                    <button
                      onClick={() => openDoc(doc)}
                      className={`w-full text-left px-3 py-2 rounded transition-colors ${
                        isActive
                          ? "bg-primary/10 text-foreground"
                          : "text-muted-foreground hover:text-foreground hover:bg-muted/30"
                      }`}
                    >
                      <div className="font-sans text-sm truncate">{doc.title}</div>
                      <div className="flex items-center gap-2 mt-0.5">
                        <span className={`font-mono text-[10px] ${s.color}`}>{s.label}</span>
                        <span className="font-mono text-[10px] text-muted-foreground/40">
                          · rev {doc.revision}
                        </span>
                      </div>
                    </button>
                  </li>
                );
              })}
            </ul>
          )}
        </aside>

        {/* Main: doc view / editor */}
        <div className="min-w-0">
          <AnimatePresence mode="wait">
            {!selected ? (
              <motion.div
                key="empty"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="text-muted-foreground/50 font-mono text-sm py-12 text-center"
              >
                elegí un documento de la izquierda, o creá uno nuevo.
              </motion.div>
            ) : editing ? (
              <motion.div
                key={`edit-${selected.slug}`}
                initial={{ opacity: 0, y: 4 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -4 }}
                className="border border-border rounded-lg p-4 bg-card/40 space-y-3"
              >
                <input
                  value={draftTitle}
                  onChange={(e) => setDraftTitle(e.target.value)}
                  className="w-full bg-transparent border-none outline-none font-sans text-lg text-foreground"
                />
                <div className="flex items-center gap-2 text-xs">
                  <span className="font-mono text-muted-foreground/60">estado:</span>
                  <select
                    value={draftStatus}
                    onChange={(e) => setDraftStatus(e.target.value as DocStatus)}
                    className="bg-transparent border border-border rounded px-2 py-0.5 font-mono text-xs text-foreground focus:outline-none focus:border-primary/40"
                  >
                    {STATUS_ORDER.map((s) => (
                      <option key={s} value={s}>{STATUS_STYLES[s].label}</option>
                    ))}
                  </select>
                </div>
                <textarea
                  value={draftBody}
                  onChange={(e) => setDraftBody(e.target.value)}
                  rows={24}
                  className="w-full bg-transparent border-none outline-none font-mono text-[13px] text-foreground/90 leading-relaxed resize-none subtle-scroll"
                />
                <div className="flex items-center justify-end gap-3 pt-2 border-t border-border/40">
                  <button
                    onClick={() => { setEditing(false); openDoc(selected); }}
                    disabled={saving}
                    className="font-mono text-xs text-muted-foreground/60 hover:text-muted-foreground disabled:opacity-30"
                  >
                    cancelar
                  </button>
                  <button
                    onClick={save}
                    disabled={saving}
                    className="font-mono text-xs text-primary hover:text-primary/80 disabled:opacity-30"
                  >
                    {saving ? "guardando..." : "guardar"}
                  </button>
                </div>
              </motion.div>
            ) : (
              <motion.div
                key={`view-${selected.slug}`}
                initial={{ opacity: 0, y: 4 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -4 }}
              >
                {/* Doc header */}
                <div className="mb-4 pb-3 border-b border-border/40">
                  <div className="flex items-baseline justify-between gap-3 mb-2">
                    <h2 className="font-sans text-xl text-foreground leading-tight">
                      {selected.title}
                    </h2>
                    <div className="flex items-center gap-1 shrink-0">
                      <button
                        onClick={() => advanceStatus(selected, -1)}
                        disabled={selected.status === "DRAFT" || saving}
                        className="font-mono text-xs text-muted-foreground/60 hover:text-muted-foreground disabled:opacity-30 transition-colors px-1"
                        title="retroceder estado"
                      >
                        ←
                      </button>
                      <span className={`font-mono text-xs ${STATUS_STYLES[selected.status].color} px-2`}>
                        {STATUS_STYLES[selected.status].label}
                      </span>
                      <button
                        onClick={() => advanceStatus(selected, 1)}
                        disabled={selected.status === "ARCHIVED" || saving}
                        className="font-mono text-xs text-muted-foreground/60 hover:text-muted-foreground disabled:opacity-30 transition-colors px-1"
                        title="avanzar estado"
                      >
                        →
                      </button>
                    </div>
                  </div>
                  <div className="flex items-center gap-3 text-xs font-mono text-muted-foreground/50">
                    <span>revisión {selected.revision}</span>
                    <span>·</span>
                    <span>editado {formatRelative(selected.updatedAt)}</span>
                    <span>·</span>
                    <span>por {selected.author}</span>
                  </div>
                </div>

                {/* Doc body — render markdown-ish */}
                <DocBody body={selected.body} />

                {/* Footer actions */}
                <div className="mt-6 pt-3 border-t border-border/40 flex items-center justify-between">
                  <span className="font-mono text-[10px] text-muted-foreground/40">
                    {formatDateTime(selected.updatedAt)}
                  </span>
                  <button
                    onClick={() => setEditing(true)}
                    className="font-mono text-xs text-primary hover:text-primary/80 transition-colors"
                  >
                    editar
                  </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </section>
  );
}

// Minimal markdown renderer — handles # headings, ## subheadings,
// - bullet lists, and paragraphs. Enough for our docs, no full MD parser.
function DocBody({ body }: { body: string }) {
  const lines = body.split("\n");
  const blocks: React.ReactNode[] = [];
  let listItems: string[] = [];

  const flushList = (key: number) => {
    if (listItems.length > 0) {
      blocks.push(
        <ul key={`ul-${key}`} className="space-y-1 my-3 ml-4">
          {listItems.map((item, i) => (
            <li key={i} className="font-sans text-sm text-foreground/80 leading-relaxed">
              <span className="text-muted-foreground/50 mr-2">·</span>
              {item}
            </li>
          ))}
        </ul>
      );
      listItems = [];
    }
  };

  lines.forEach((line, i) => {
    if (line.startsWith("# ")) {
      flushList(i);
      blocks.push(
        <h1 key={i} className="font-sans text-2xl text-foreground mt-6 mb-3 first:mt-0">
          {line.slice(2)}
        </h1>
      );
    } else if (line.startsWith("## ")) {
      flushList(i);
      blocks.push(
        <h2 key={i} className="font-mono text-sm uppercase tracking-wider text-primary mt-5 mb-2">
          {line.slice(3)}
        </h2>
      );
    } else if (line.startsWith("### ")) {
      flushList(i);
      blocks.push(
        <h3 key={i} className="font-sans text-base text-foreground mt-4 mb-2">
          {line.slice(4)}
        </h3>
      );
    } else if (line.startsWith("- ")) {
      listItems.push(line.slice(2));
    } else if (line.trim() === "") {
      flushList(i);
      // skip empty line
    } else {
      flushList(i);
      blocks.push(
        <p key={i} className="font-sans text-[15px] text-foreground/85 leading-relaxed my-3 whitespace-pre-wrap">
          {line}
        </p>
      );
    }
  });
  flushList(lines.length);

  return <div>{blocks}</div>;
}
