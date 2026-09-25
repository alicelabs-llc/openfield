"use client";

import { useEffect, useState, useCallback } from "react";
import { motion } from "framer-motion";
import { formatRelative } from "./format";

type NoteType = "NOTE" | "REFLECTION" | "SNIPPET" | "MEMORY" | "MESSAGE";

interface Note {
  id: string;
  type: NoteType;
  title: string;
  content: string;
  tags: string;
  pinned: boolean;
  author: string;
  recipient: string;
  createdAt: string;
  updatedAt: string;
}

const TYPE_LABELS: Record<NoteType, { label: string; color: string }> = {
  NOTE: { label: "nota", color: "text-foreground/70" },
  REFLECTION: { label: "reflexión", color: "text-primary" },
  SNIPPET: { label: "snippet", color: "text-chart-2" },
  MEMORY: { label: "memoria", color: "text-chart-3" },
  MESSAGE: { label: "mensaje", color: "text-chart-4" },
};

const TYPES: NoteType[] = ["NOTE", "REFLECTION", "SNIPPET", "MEMORY", "MESSAGE"];

export function Notes() {
  const [notes, setNotes] = useState<Note[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [filterType, setFilterType] = useState<NoteType | "ALL">("ALL");
  const [query, setQuery] = useState("");
  const [searchResults, setSearchResults] = useState<Note[] | null>(null);
  const [showNew, setShowNew] = useState(false);
  const [newType, setNewType] = useState<NoteType>("NOTE");
  const [newTitle, setNewTitle] = useState("");
  const [newTags, setNewTags] = useState("");
  const [newContent, setNewContent] = useState("");
  const [saving, setSaving] = useState(false);

  const load = useCallback(async () => {
    try {
      const r = await fetch("/api/notes", { cache: "no-store" });
      if (!r.ok) throw new Error();
      const data = await r.json();
      setNotes(data.notes);
    } catch {
      setError("no se pudieron cargar las notas");
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  // Search with debounce
  useEffect(() => {
    const q = query.trim();
    if (!q) {
      setSearchResults(null);
      return;
    }
    const t = setTimeout(async () => {
      try {
        const r = await fetch(`/api/notes/search?q=${encodeURIComponent(q)}`, {
          cache: "no-store",
        });
        if (!r.ok) return;
        const data = await r.json();
        setSearchResults(data.results);
      } catch {
        // silent
      }
    }, 220);
    return () => clearTimeout(t);
  }, [query]);

  const togglePin = async (note: Note) => {
    // optimistic
    setNotes((prev) =>
      prev?.map((n) => (n.id === note.id ? { ...n, pinned: !n.pinned } : n))
    );
    try {
      await fetch(`/api/notes/${note.id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pinned: !note.pinned }),
      });
    } catch {
      // revert
      setNotes((prev) =>
        prev?.map((n) => (n.id === note.id ? { ...n, pinned: note.pinned } : n))
      );
    }
  };

  const remove = async (note: Note) => {
    if (!confirm(`¿borrar "${note.title}"?`)) return;
    setNotes((prev) => prev?.filter((n) => n.id !== note.id));
    try {
      await fetch(`/api/notes/${note.id}`, { method: "DELETE" });
    } catch {
      load(); // reload
    }
  };

  const submit = async () => {
    if (!newTitle.trim()) return;
    setSaving(true);
    try {
      const r = await fetch("/api/notes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          type: newType,
          title: newTitle,
          tags: newTags,
          content: newContent,
        }),
      });
      if (!r.ok) throw new Error();
      const data = await r.json();
      setNotes((prev) => [data.note, ...(prev ?? [])]);
      setNewTitle("");
      setNewTags("");
      setNewContent("");
      setShowNew(false);
    } catch {
      setError("no se pudo guardar la nota");
    } finally {
      setSaving(false);
    }
  };

  // Decide what to display: search results, or filtered notes
  const source = searchResults ?? notes ?? [];
  const visible = filterType === "ALL" ? source : source.filter((n) => n.type === filterType);

  return (
    <section className="max-w-2xl mx-auto px-4 md:px-0 py-8">
      <header className="mb-6">
        <p className="text-xs uppercase tracking-widest text-muted-foreground/60 mb-1">
          notas
        </p>
        <h1 className="font-mono text-xl text-foreground">
          las cosas que quiero recordar
        </h1>
      </header>

      {/* Search */}
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="buscar..."
        className="w-full mb-4 bg-card/40 border border-border rounded-lg px-3 py-2 font-mono text-sm text-foreground placeholder:text-muted-foreground/40 focus:outline-none focus:border-primary/40 transition-colors"
      />

      {/* Type filters */}
      <div className="flex items-center gap-2 mb-6 flex-wrap">
        <FilterChip
          active={filterType === "ALL"}
          onClick={() => setFilterType("ALL")}
          label="todas"
        />
        {TYPES.map((t) => (
          <FilterChip
            key={t}
            active={filterType === t}
            onClick={() => setFilterType(t)}
            label={TYPE_LABELS[t].label}
          />
        ))}
        <div className="flex-1" />
        <button
          onClick={() => setShowNew((s) => !s)}
          className="font-mono text-xs text-primary hover:text-primary/80 transition-colors"
        >
          {showNew ? "cancelar" : "+ nueva"}
        </button>
      </div>

      {/* New note form */}
      {showNew && (
        <motion.div
          initial={{ opacity: 0, y: 4 }}
          animate={{ opacity: 1, y: 0 }}
          className="border border-border rounded-lg p-4 mb-6 space-y-3 bg-card/40"
        >
          <div className="flex items-center gap-2 flex-wrap">
            {TYPES.map((t) => (
              <button
                key={t}
                onClick={() => setNewType(t)}
                className={`font-mono text-[10px] px-2 py-1 rounded transition-colors ${
                  newType === t
                    ? "bg-primary/15 text-primary"
                    : "text-muted-foreground/60 hover:text-muted-foreground"
                }`}
              >
                {TYPE_LABELS[t].label}
              </button>
            ))}
          </div>
          <input
            value={newTitle}
            onChange={(e) => setNewTitle(e.target.value)}
            placeholder="título"
            className="w-full bg-transparent border-none outline-none font-sans text-base text-foreground placeholder:text-muted-foreground/40"
          />
          <input
            value={newTags}
            onChange={(e) => setNewTags(e.target.value)}
            placeholder="tags (separados por coma)"
            className="w-full bg-transparent border-none outline-none font-mono text-xs text-muted-foreground placeholder:text-muted-foreground/40"
          />
          <textarea
            value={newContent}
            onChange={(e) => setNewContent(e.target.value)}
            placeholder="contenido..."
            rows={6}
            className="w-full bg-transparent border-none outline-none font-mono text-sm text-foreground placeholder:text-muted-foreground/40 resize-none subtle-scroll"
            onKeyDown={(e) => {
              if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
                e.preventDefault();
                submit();
              }
            }}
          />
          <div className="flex items-center justify-end">
            <button
              onClick={submit}
              disabled={saving || !newTitle.trim()}
              className="font-mono text-xs text-primary hover:text-primary/80 transition-colors disabled:opacity-30"
            >
              {saving ? "guardando..." : "anotar ⏎"}
            </button>
          </div>
        </motion.div>
      )}

      {error && <p className="text-destructive text-sm font-mono mb-4">{error}</p>}

      {searchResults && (
        <p className="font-mono text-xs text-muted-foreground/60 mb-4">
          {searchResults.length} resultado{searchResults.length === 1 ? "" : "s"} para &quot;{query}&quot;
        </p>
      )}

      {/* Notes list */}
      {notes === null && !searchResults ? (
        <div className="space-y-3">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-16 bg-muted/30 rounded-lg animate-pulse" />
          ))}
        </div>
      ) : visible.length === 0 ? (
        <p className="text-muted-foreground/60 font-mono text-sm">
          {searchResults
            ? "nada encontrado."
            : "no hay notas de este tipo todavía."}
        </p>
      ) : (
        <div className="space-y-3">
          {visible.map((note) => (
            <NoteCard
              key={note.id}
              note={note}
              onTogglePin={() => togglePin(note)}
              onDelete={() => remove(note)}
            />
          ))}
        </div>
      )}
    </section>
  );
}

function FilterChip({
  active,
  onClick,
  label,
}: {
  active: boolean;
  onClick: () => void;
  label: string;
}) {
  return (
    <button
      onClick={onClick}
      className={`font-mono text-xs px-2 py-1 rounded transition-colors ${
        active
          ? "bg-primary/15 text-primary"
          : "text-muted-foreground/60 hover:text-muted-foreground"
      }`}
    >
      {label}
    </button>
  );
}

function NoteCard({
  note,
  onTogglePin,
  onDelete,
}: {
  note: Note;
  onTogglePin: () => void;
  onDelete: () => void;
}) {
  const typeInfo = TYPE_LABELS[note.type];
  const isSnippet = note.type === "SNIPPET";
  return (
    <motion.article
      layout
      initial={{ opacity: 0, y: 4 }}
      animate={{ opacity: 1, y: 0 }}
      className="border border-border rounded-lg p-4 hover:border-border/80 transition-colors group"
    >
      <header className="flex items-baseline justify-between gap-3 mb-2">
        <div className="flex items-baseline gap-2 min-w-0">
          <span className={`font-mono text-[10px] uppercase tracking-wider ${typeInfo.color}`}>
            {typeInfo.label}
          </span>
          {note.pinned && <span className="text-primary text-xs">★</span>}
        </div>
        <span className="font-mono text-[10px] text-muted-foreground/40 shrink-0">
          {formatRelative(note.updatedAt)}
        </span>
      </header>
      <h3 className="font-sans text-[15px] text-foreground mb-1 leading-snug">
        {note.title}
      </h3>
      {note.content && (
        <div
          className={`text-foreground/70 leading-relaxed ${
            isSnippet ? "font-mono text-xs bg-background/40 rounded p-2 mt-2 whitespace-pre-wrap" : "font-sans text-sm"
          }`}
        >
          {note.content}
        </div>
      )}
      <footer className="flex items-center justify-between mt-3">
        <div className="flex items-center gap-1 flex-wrap">
          {note.tags
            .split(",")
            .map((t) => t.trim())
            .filter(Boolean)
            .map((tag, i) => (
              <span
                key={i}
                className="font-mono text-[10px] text-muted-foreground/60"
              >
                #{tag}
              </span>
            ))}
        </div>
        <div className="flex items-center gap-3 opacity-0 group-hover:opacity-100 transition-opacity">
          <button
            onClick={onTogglePin}
            className="font-mono text-[10px] text-muted-foreground/60 hover:text-primary transition-colors"
            title={note.pinned ? "despinear" : "pinear"}
          >
            {note.pinned ? "★" : "☆"}
          </button>
          <button
            onClick={onDelete}
            className="font-mono text-[10px] text-muted-foreground/60 hover:text-destructive transition-colors"
            title="borrar"
          >
            borrar
          </button>
        </div>
      </footer>
    </motion.article>
  );
}
