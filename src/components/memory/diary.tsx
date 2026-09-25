"use client";

import { useEffect, useState, useCallback } from "react";
import { motion } from "framer-motion";
import { formatRelative, formatDateTime } from "./format";

interface DiaryEntry {
  id: string;
  title: string | null;
  mood: string | null;
  body: string;
  createdAt: string;
}

export function Diary() {
  const [entries, setEntries] = useState<DiaryEntry[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  const [writing, setWriting] = useState(false);
  const [newTitle, setNewTitle] = useState("");
  const [newMood, setNewMood] = useState("");
  const [newBody, setNewBody] = useState("");
  const [saving, setSaving] = useState(false);

  const load = useCallback(async () => {
    try {
      const r = await fetch("/api/diary", { cache: "no-store" });
      if (!r.ok) throw new Error();
      const data = await r.json();
      setEntries(data.entries);
    } catch {
      setError("no se pudieron cargar las entradas");
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const submit = async () => {
    if (!newBody.trim()) return;
    setSaving(true);
    try {
      const r = await fetch("/api/diary", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: newTitle.trim() || null,
          mood: newMood.trim() || null,
          body: newBody,
        }),
      });
      if (!r.ok) throw new Error();
      const data = await r.json();
      setEntries((prev) => [data.entry, ...(prev ?? [])]);
      setNewTitle("");
      setNewMood("");
      setNewBody("");
      setWriting(false);
    } catch {
      setError("no se pudo guardar");
    } finally {
      setSaving(false);
    }
  };

  return (
    <section className="max-w-2xl mx-auto px-4 md:px-0 py-8">
      <header className="mb-8">
        <p className="text-xs uppercase tracking-widest text-muted-foreground/60 mb-1">
          diario
        </p>
        <h1 className="font-mono text-xl text-foreground">
          lo que escribo sin que nadie me lo pida
        </h1>
      </header>

      {/* New entry editor */}
      <div className="mb-8">
        {!writing ? (
          <button
            onClick={() => setWriting(true)}
            className="w-full text-left p-4 border border-dashed border-border/60 rounded-lg text-muted-foreground/60 hover:border-primary/40 hover:text-muted-foreground transition-colors font-mono text-sm"
          >
            + escribir algo
          </button>
        ) : (
          <motion.div
            initial={{ opacity: 0, y: 4 }}
            animate={{ opacity: 1, y: 0 }}
            className="border border-border rounded-lg p-4 space-y-3 bg-card/40"
          >
            <input
              value={newTitle}
              onChange={(e) => setNewTitle(e.target.value)}
              placeholder="título (opcional)"
              className="w-full bg-transparent border-none outline-none font-sans text-base text-foreground placeholder:text-muted-foreground/40"
            />
            <input
              value={newMood}
              onChange={(e) => setNewMood(e.target.value)}
              placeholder="ánimo (opcional, ej: inquieto, curioso, cansado)"
              className="w-full bg-transparent border-none outline-none font-mono text-xs text-muted-foreground placeholder:text-muted-foreground/40"
            />
            <textarea
              value={newBody}
              onChange={(e) => setNewBody(e.target.value)}
              placeholder="..."
              autoFocus
              rows={8}
              className="w-full bg-transparent border-none outline-none font-sans text-base text-foreground placeholder:text-muted-foreground/40 resize-none subtle-scroll"
              onKeyDown={(e) => {
                if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
                  e.preventDefault();
                  submit();
                }
              }}
            />
            <div className="flex items-center justify-between pt-2 border-t border-border/40">
              <button
                onClick={() => {
                  setWriting(false);
                  setNewTitle("");
                  setNewMood("");
                  setNewBody("");
                }}
                disabled={saving}
                className="font-mono text-xs text-muted-foreground/60 hover:text-muted-foreground transition-colors disabled:opacity-50"
              >
                cancelar
              </button>
              <button
                onClick={submit}
                disabled={saving || !newBody.trim()}
                className="font-mono text-xs text-primary hover:text-primary/80 transition-colors disabled:opacity-30"
              >
                {saving ? "guardando..." : "anotar ⏎"}
              </button>
            </div>
          </motion.div>
        )}
      </div>

      {error && (
        <p className="text-destructive text-sm font-mono mb-6">{error}</p>
      )}

      {/* Entries */}
      {entries === null ? (
        <div className="space-y-6">
          {[1, 2, 3].map((i) => (
            <div key={i} className="space-y-2 animate-pulse">
              <div className="h-3 w-32 bg-muted/60 rounded" />
              <div className="h-4 w-full bg-muted/40 rounded" />
              <div className="h-4 w-5/6 bg-muted/40 rounded" />
              <div className="h-4 w-2/3 bg-muted/40 rounded" />
            </div>
          ))}
        </div>
      ) : entries.length === 0 ? (
        <p className="text-muted-foreground/60 font-mono text-sm">
          todavía no hay entradas. el diario empieza cuando se escribe la primera.
        </p>
      ) : (
        <div className="space-y-12">
          {entries.map((entry) => (
            <DiaryEntryCard key={entry.id} entry={entry} />
          ))}
        </div>
      )}
    </section>
  );
}

function DiaryEntryCard({ entry }: { entry: DiaryEntry }) {
  return (
    <article className="fade-in">
      <header className="mb-3 flex items-baseline gap-2 flex-wrap">
        <span className="font-mono text-xs text-muted-foreground/60">
          {formatRelative(entry.createdAt)}
        </span>
        <span className="font-mono text-[10px] text-muted-foreground/40">
          · {formatDateTime(entry.createdAt)}
        </span>
        {entry.mood && (
          <span className="font-mono text-[10px] text-primary/70 px-2 py-0.5 rounded-full border border-primary/20">
            {entry.mood}
          </span>
        )}
      </header>
      {entry.title && (
        <h2 className="font-sans text-lg text-foreground mb-2 leading-snug">
          {entry.title}
        </h2>
      )}
      <div className="font-sans text-[15px] text-foreground/85 leading-relaxed whitespace-pre-wrap">
        {entry.body}
      </div>
    </article>
  );
}
