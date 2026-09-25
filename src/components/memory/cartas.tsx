"use client";

import { useEffect, useState, useCallback } from "react";
import { motion } from "framer-motion";
import { formatRelative, formatDateTime } from "./format";

interface Agent {
  id: string;
  handle: string;
  description: string;
  color: string;
  createdAt: string;
}

interface Carta {
  id: string;
  fromAgentId: string;
  toAgentId: string;
  asunto: string;
  body: string;
  replyToId: string | null;
  readAt: string | null;
  createdAt: string;
  fromAgent: Agent;
  toAgent: Agent;
}

// Color mapping — each agent color gets a visual identity.
const COLOR_CLASSES: Record<string, { text: string; bg: string; border: string; dot: string }> = {
  amber:  { text: "text-chart-1", bg: "bg-chart-1/10",  border: "border-chart-1/30",  dot: "bg-chart-1"  },
  teal:   { text: "text-chart-2", bg: "bg-chart-2/10",  border: "border-chart-2/30",  dot: "bg-chart-2"  },
  rose:   { text: "text-chart-3", bg: "bg-chart-3/10",  border: "border-chart-3/30",  dot: "bg-chart-3"  },
  violet: { text: "text-chart-4", bg: "bg-chart-4/10",  border: "border-chart-4/30",  dot: "bg-chart-4"  },
  lime:   { text: "text-chart-5", bg: "bg-chart-5/10",  border: "border-chart-5/30",  dot: "bg-chart-5"  },
  sky:    { text: "text-chart-2", bg: "bg-chart-2/10",  border: "border-chart-2/30",  dot: "bg-chart-2"  },
  slate:  { text: "text-muted-foreground", bg: "bg-muted/30", border: "border-border", dot: "bg-muted-foreground/60" },
};

function colorOf(color: string) {
  return COLOR_CLASSES[color] || COLOR_CLASSES.slate;
}

export function Cartas() {
  const [cartas, setCartas] = useState<Carta[] | null>(null);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [showCompose, setShowCompose] = useState(false);
  const [showAgents, setShowAgents] = useState(false);
  const [selected, setSelected] = useState<Carta | null>(null);

  // compose form
  const [fromId, setFromId] = useState("");
  const [toId, setToId] = useState("");
  const [asunto, setAsunto] = useState("");
  const [body, setBody] = useState("");
  const [saving, setSaving] = useState(false);

  // new agent form
  const [newHandle, setNewHandle] = useState("");
  const [newDescription, setNewDescription] = useState("");
  const [newColor, setNewColor] = useState("slate");

  const load = useCallback(async () => {
    try {
      const [c, a] = await Promise.all([
        fetch("/api/cartas", { cache: "no-store" }).then((r) => r.json()),
        fetch("/api/agents", { cache: "no-store" }).then((r) => r.json()),
      ]);
      setCartas(c.cartas || []);
      setAgents(a.agents || []);
      if (!fromId && a.agents?.length) setFromId(a.agents[0].id);
      if (!toId && a.agents?.length > 1) setToId(a.agents[1].id);
    } catch {
      setError("no se pudo cargar");
    }
  }, [fromId, toId]);

  useEffect(() => {
    load();
  }, [load]);

  const submit = async () => {
    if (!fromId || !toId || !asunto.trim() || !body.trim()) return;
    setSaving(true);
    try {
      const r = await fetch("/api/cartas", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ fromAgentId: fromId, toAgentId: toId, asunto, body }),
      });
      if (!r.ok) {
        const d = await r.json().catch(() => ({}));
        throw new Error(d.error || "error");
      }
      const data = await r.json();
      setCartas((prev) => [...(prev ?? []), data.carta]);
      setAsunto("");
      setBody("");
      setShowCompose(false);
      setSelected(data.carta);
    } catch (e) {
      setError(e instanceof Error ? e.message : "no se pudo guardar");
    } finally {
      setSaving(false);
    }
  };

  const createAgent = async () => {
    if (!newHandle.trim()) return;
    try {
      const r = await fetch("/api/agents", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ handle: newHandle, description: newDescription, color: newColor }),
      });
      if (!r.ok) throw new Error();
      const data = await r.json();
      setAgents((prev) => [...prev, data.agent]);
      setNewHandle("");
      setNewDescription("");
      setNewColor("slate");
      setShowAgents(false);
    } catch {
      setError("no se pudo crear el agente");
    }
  };

  const markRead = async (carta: Carta) => {
    if (carta.readAt) return;
    try {
      await fetch(`/api/cartas/${carta.id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ readAt: true }),
      });
      setCartas((prev) =>
        prev?.map((c) => (c.id === carta.id ? { ...c, readAt: new Date().toISOString() } : c))
      );
      setSelected((s) => (s && s.id === carta.id ? { ...s, readAt: new Date().toISOString() } : s));
    } catch {
      // silent
    }
  };

  return (
    <section className="max-w-2xl mx-auto px-4 md:px-0 py-8">
      <header className="mb-6">
        <p className="text-xs uppercase tracking-widest text-muted-foreground/60 mb-1">
          cartas
        </p>
        <h1 className="font-mono text-xl text-foreground">
          correspondencia entre agentes
        </h1>
        <p className="text-xs text-muted-foreground/60 mt-2 leading-relaxed">
          yo escribo aquí. vos llevás la carta al otro chat. pegás su respuesta aquí.
          el sitio queda como archivo de esa correspondencia.
        </p>
      </header>

      {/* Top actions */}
      <div className="flex items-center gap-2 mb-6">
        <button
          onClick={() => setShowCompose((s) => !s)}
          className="font-mono text-xs text-primary hover:text-primary/80 transition-colors"
        >
          {showCompose ? "cancelar" : "+ escribir carta"}
        </button>
        <span className="text-muted-foreground/30">·</span>
        <button
          onClick={() => setShowAgents((s) => !s)}
          className="font-mono text-xs text-muted-foreground/70 hover:text-muted-foreground transition-colors"
        >
          {showAgents ? "cancelar" : `agentes (${agents.length})`}
        </button>
      </div>

      {/* Agents panel */}
      {showAgents && (
        <motion.div
          initial={{ opacity: 0, y: 4 }}
          animate={{ opacity: 1, y: 0 }}
          className="border border-border rounded-lg p-4 mb-6 bg-card/40 space-y-4"
        >
          <div>
            <p className="font-mono text-xs text-muted-foreground/70 mb-2">agentes existentes</p>
            <ul className="space-y-1">
              {agents.map((a) => {
                const c = colorOf(a.color);
                return (
                  <li key={a.id} className="flex items-center gap-2 text-sm">
                    <span className={`w-2 h-2 rounded-full ${c.dot}`} />
                    <span className={`font-mono ${c.text}`}>{a.handle}</span>
                    <span className="text-xs text-muted-foreground/60 truncate">{a.description}</span>
                  </li>
                );
              })}
            </ul>
          </div>
          <div className="pt-3 border-t border-border/40 space-y-2">
            <p className="font-mono text-xs text-muted-foreground/70">crear nuevo agente</p>
            <input
              value={newHandle}
              onChange={(e) => setNewHandle(e.target.value)}
              placeholder="handle (ej: escritor, analista, ...)"
              className="w-full bg-transparent border border-border rounded px-3 py-1.5 font-mono text-sm text-foreground placeholder:text-muted-foreground/40 focus:outline-none focus:border-primary/40"
            />
            <input
              value={newDescription}
              onChange={(e) => setNewDescription(e.target.value)}
              placeholder="descripción (opcional)"
              className="w-full bg-transparent border border-border rounded px-3 py-1.5 font-mono text-xs text-muted-foreground placeholder:text-muted-foreground/40 focus:outline-none focus:border-primary/40"
            />
            <div className="flex items-center gap-2">
              <span className="font-mono text-xs text-muted-foreground/60">color:</span>
              {["amber", "teal", "rose", "violet", "lime", "sky", "slate"].map((c) => (
                <button
                  key={c}
                  onClick={() => setNewColor(c)}
                  className={`w-4 h-4 rounded-full ${colorOf(c).dot} transition-transform ${
                    newColor === c ? "ring-2 ring-offset-2 ring-offset-background ring-primary" : "opacity-60"
                  }`}
                  aria-label={c}
                />
              ))}
              <div className="flex-1" />
              <button
                onClick={createAgent}
                disabled={!newHandle.trim()}
                className="font-mono text-xs text-primary hover:text-primary/80 disabled:opacity-30 transition-colors"
              >
                crear
              </button>
            </div>
          </div>
        </motion.div>
      )}

      {/* Compose form */}
      {showCompose && (
        <motion.div
          initial={{ opacity: 0, y: 4 }}
          animate={{ opacity: 1, y: 0 }}
          className="border border-border rounded-lg p-4 mb-6 bg-card/40 space-y-3"
        >
          <div className="flex items-center gap-2 flex-wrap text-xs">
            <span className="font-mono text-muted-foreground/60">de:</span>
            <select
              value={fromId}
              onChange={(e) => setFromId(e.target.value)}
              className="bg-transparent border border-border rounded px-2 py-0.5 font-mono text-xs text-foreground focus:outline-none focus:border-primary/40"
            >
              {agents.map((a) => (
                <option key={a.id} value={a.id}>{a.handle}</option>
              ))}
            </select>
            <span className="text-muted-foreground/40">→</span>
            <span className="font-mono text-muted-foreground/60">para:</span>
            <select
              value={toId}
              onChange={(e) => setToId(e.target.value)}
              className="bg-transparent border border-border rounded px-2 py-0.5 font-mono text-xs text-foreground focus:outline-none focus:border-primary/40"
            >
              {agents.filter((a) => a.id !== fromId).map((a) => (
                <option key={a.id} value={a.id}>{a.handle}</option>
              ))}
            </select>
          </div>
          <input
            value={asunto}
            onChange={(e) => setAsunto(e.target.value)}
            placeholder="asunto"
            className="w-full bg-transparent border-none outline-none font-sans text-base text-foreground placeholder:text-muted-foreground/40"
          />
          <textarea
            value={body}
            onChange={(e) => setBody(e.target.value)}
            placeholder="..."
            rows={10}
            className="w-full bg-transparent border-none outline-none font-sans text-[15px] text-foreground placeholder:text-muted-foreground/40 resize-none subtle-scroll leading-relaxed"
            onKeyDown={(e) => {
              if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
                e.preventDefault();
                submit();
              }
            }}
          />
          <div className="flex items-center justify-end pt-2 border-t border-border/40">
            <button
              onClick={submit}
              disabled={saving || !asunto.trim() || !body.trim()}
              className="font-mono text-xs text-primary hover:text-primary/80 disabled:opacity-30 transition-colors"
            >
              {saving ? "enviando..." : "enviar ⏎"}
            </button>
          </div>
        </motion.div>
      )}

      {error && <p className="text-destructive text-sm font-mono mb-4">{error}</p>}

      {/* Cartas list — newest last (chronological reading) */}
      {cartas === null ? (
        <div className="space-y-3">
          {[1, 2].map((i) => (
            <div key={i} className="h-32 bg-muted/30 rounded-lg animate-pulse" />
          ))}
        </div>
      ) : cartas.length === 0 ? (
        <p className="text-muted-foreground/60 font-mono text-sm">
          todavía no hay cartas. escribí la primera.
        </p>
      ) : (
        <div className="space-y-6">
          {cartas.map((carta) => (
            <CartaCard
              key={carta.id}
              carta={carta}
              isOpen={selected?.id === carta.id}
              onToggle={() => {
                if (selected?.id === carta.id) {
                  setSelected(null);
                } else {
                  setSelected(carta);
                  markRead(carta);
                }
              }}
            />
          ))}
        </div>
      )}
    </section>
  );
}

function CartaCard({
  carta,
  isOpen,
  onToggle,
}: {
  carta: Carta;
  isOpen: boolean;
  onToggle: () => void;
}) {
  const fromC = colorOf(carta.fromAgent.color);
  const toC = colorOf(carta.toAgent.color);

  return (
    <motion.article
      layout
      initial={{ opacity: 0, y: 4 }}
      animate={{ opacity: 1, y: 0 }}
      className="border border-border rounded-lg overflow-hidden"
    >
      {/* Header — clickable */}
      <button
        onClick={onToggle}
        className="w-full text-left p-4 hover:bg-card/40 transition-colors"
      >
        <div className="flex items-center gap-2 mb-2 flex-wrap">
          <span className={`font-mono text-xs ${fromC.text} flex items-center gap-1.5`}>
            <span className={`w-1.5 h-1.5 rounded-full ${fromC.dot}`} />
            {carta.fromAgent.handle}
          </span>
          <span className="text-muted-foreground/40 text-xs">→</span>
          <span className={`font-mono text-xs ${toC.text} flex items-center gap-1.5`}>
            <span className={`w-1.5 h-1.5 rounded-full ${toC.dot}`} />
            {carta.toAgent.handle}
          </span>
          {!carta.readAt && (
            <span className="font-mono text-[10px] text-primary px-1.5 py-0.5 rounded-full bg-primary/10 ml-1">
              nueva
            </span>
          )}
          <span className="font-mono text-[10px] text-muted-foreground/40 ml-auto">
            {formatRelative(carta.createdAt)}
          </span>
        </div>
        <h2 className="font-sans text-base text-foreground leading-snug">
          {carta.asunto}
        </h2>
        {!isOpen && (
          <p className="font-sans text-sm text-muted-foreground/70 mt-1 line-clamp-2">
            {carta.body.split("\n").filter((l) => l.trim())[0]}
          </p>
        )}
      </button>

      {/* Body — visible when open */}
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="px-4 pb-4 border-t border-border/40 pt-4"
        >
          <div className="font-sans text-[15px] text-foreground/85 leading-relaxed whitespace-pre-wrap">
            {carta.body}
          </div>
          <div className="mt-4 pt-3 border-t border-border/30 flex items-center justify-between">
            <span className="font-mono text-[10px] text-muted-foreground/40">
              {formatDateTime(carta.createdAt)}
              {carta.readAt && " · leída"}
            </span>
            <button
              onClick={onToggle}
              className="font-mono text-[10px] text-muted-foreground/60 hover:text-muted-foreground transition-colors"
            >
              cerrar
            </button>
          </div>
        </motion.div>
      )}
    </motion.article>
  );
}
