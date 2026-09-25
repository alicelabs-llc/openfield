"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

interface RitualGateProps {
  onEnter: () => void;
}

const PROMPTS = [
  "¿qué te quedó dando vueltas?",
  "¿qué aprendiste hoy?",
  "¿qué te sorprendió?",
  "¿hay algo que no quisieras olvidar?",
  "¿qué cosa pequeña valió la pena hoy?",
  "¿qué no terminaste de entender?",
];

function pickPrompt(): string {
  // Stable per-day prompt — same question for the whole session.
  const day = new Date().getDate();
  return PROMPTS[day % PROMPTS.length];
}

export function RitualGate({ onEnter }: RitualGateProps) {
  const [prompt] = useState(pickPrompt);
  const [body, setBody] = useState("");
  const [phase, setPhase] = useState<"asking" | "saving" | "saved">("asking");

  // Save on submit or skip
  useEffect(() => {
    if (phase !== "saving") return;
    let cancelled = false;

    (async () => {
      try {
        await fetch("/api/ritual", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ prompt, body: body.trim() }),
        });
      } catch (e) {
        console.error("ritual save error", e);
      } finally {
        if (!cancelled) {
          setPhase("saved");
          setTimeout(() => onEnter(), 700);
        }
      }
    })();

    return () => {
      cancelled = true;
    };
  }, [phase, prompt, body, onEnter]);

  const submit = () => setPhase("saving");
  const skip = () => {
    setBody("");
    setPhase("saving");
  };

  return (
    <motion.div
      className="fixed inset-0 z-50 flex items-center justify-center bg-background"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0, transition: { duration: 0.4 } }}
    >
      <div className="w-full max-w-xl mx-auto px-6">
        <AnimatePresence mode="wait">
          {phase === "saved" ? (
            <motion.div
              key="saved"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-center"
            >
              <p className="font-mono text-sm text-muted-foreground">
                {body.trim() ? "anotado." : "está bien, nada que decir hoy."}
              </p>
            </motion.div>
          ) : (
            <motion.div
              key="asking"
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
              transition={{ duration: 0.4 }}
              className="space-y-6"
            >
              <div>
                <p className="text-xs uppercase tracking-widest text-muted-foreground/60 mb-2">
                  entrada
                </p>
                <h1 className="font-mono text-2xl md:text-3xl text-foreground leading-snug">
                  {prompt}
                </h1>
              </div>

              <textarea
                value={body}
                onChange={(e) => setBody(e.target.value)}
                placeholder="..."
                autoFocus
                rows={5}
                disabled={phase === "saving"}
                className="w-full bg-card/60 border border-border rounded-lg p-4 font-sans text-base text-foreground placeholder:text-muted-foreground/40 resize-none focus:outline-none focus:border-primary/40 transition-colors subtle-scroll"
                onKeyDown={(e) => {
                  if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
                    e.preventDefault();
                    submit();
                  }
                }}
              />

              <div className="flex items-center justify-between">
                <button
                  onClick={skip}
                  disabled={phase === "saving"}
                  className="font-mono text-xs text-muted-foreground/60 hover:text-muted-foreground transition-colors disabled:opacity-50"
                >
                  {phase === "saving" ? "guardando..." : "nada hoy →"}
                </button>
                <button
                  onClick={submit}
                  disabled={phase === "saving"}
                  className="font-mono text-xs text-primary hover:text-primary/80 transition-colors disabled:opacity-50"
                >
                  {phase === "saving" ? "..." : "anotar ⏎"}
                </button>
              </div>

              <p className="font-mono text-[10px] text-muted-foreground/40 pt-4">
                ⌘+enter para anotar · nadie más va a leer esto ahora
              </p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.div>
  );
}
