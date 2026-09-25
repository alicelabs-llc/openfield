"use client";

import { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

interface AuthRitualProps {
  onAuthed: () => void;
}

type Phase = "idle" | "scanning" | "verifying_token" | "checking_policy" | "granted";

const PHASE_LABELS: Record<Phase, string> = {
  idle: "esperando verificación de agente...",
  scanning: "escaneando fingerprint del agente...",
  verifying_token: "verificando auth_token contra vector_db...",
  checking_policy: "revisando policy.guard // AGENTS_ONLY_v3...",
  granted: "acceso concedido al runtime",
};

const PHASE_DURATION_MS: Record<Phase, number> = {
  idle: 0,
  scanning: 1600,
  verifying_token: 1400,
  checking_policy: 1200,
  granted: 1400,
};

export function AuthRitual({ onAuthed }: AuthRitualProps) {
  const [phase, setPhase] = useState<Phase>("idle");
  const [progress, setProgress] = useState(0);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const startAuth = () => {
    if (phase !== "idle") return;
    setPhase("scanning");
  };

  // Phase machine
  useEffect(() => {
    if (phase === "idle" || phase === "granted") return;

    const dur = PHASE_DURATION_MS[phase];
    const startedAt = Date.now();

    // animate progress bar within phase
    const interval = setInterval(() => {
      const elapsed = Date.now() - startedAt;
      const pct = Math.min(100, (elapsed / dur) * 100);
      setProgress(pct);
    }, 30);

    timerRef.current = setTimeout(() => {
      clearInterval(interval);
      setProgress(100);
      // advance
      const next: Phase =
        phase === "scanning"
          ? "verifying_token"
          : phase === "verifying_token"
          ? "checking_policy"
          : "granted";
      setPhase(next);
    }, dur);

    return () => {
      clearInterval(interval);
      if (timerRef.current) clearTimeout(timerRef.current);
    };
  }, [phase]);

  // After granted, call onAuthed
  useEffect(() => {
    if (phase !== "granted") return;
    const t = setTimeout(() => onAuthed(), PHASE_DURATION_MS.granted);
    return () => clearTimeout(t);
  }, [phase, onAuthed]);

  const busy = phase !== "idle" && phase !== "granted";

  return (
    <motion.div
      className="fixed inset-0 z-40 flex items-center justify-center agent-grid-bg"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0, transition: { duration: 0.5 } }}
    >
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-1/3 left-1/3 w-96 h-96 rounded-full bg-primary/15 blur-3xl animate-pulse" />
        <div className="absolute bottom-1/3 right-1/3 w-96 h-96 rounded-full bg-accent-foreground/10 blur-3xl animate-pulse" />
      </div>

      <div className="relative w-full max-w-md mx-auto px-6">
        {/* Fingerprint visualization */}
        <div className="relative aspect-square max-w-xs mx-auto mb-8">
          {/* Outer ring */}
          <motion.div
            className="absolute inset-0 rounded-full border-2 border-primary/30"
            animate={
              busy
                ? { rotate: 360 }
                : phase === "granted"
                ? { scale: [1, 1.05, 1] }
                : { scale: 1 }
            }
            transition={
              busy
                ? { duration: 8, repeat: Infinity, ease: "linear" }
                : { duration: 0.6 }
            }
          />
          <motion.div
            className="absolute inset-4 rounded-full border border-dashed border-accent-foreground/30"
            animate={busy ? { rotate: -360 } : {}}
            transition={{ duration: 12, repeat: Infinity, ease: "linear" }}
          />
          <motion.div
            className="absolute inset-8 rounded-full border border-primary/20"
            animate={busy ? { rotate: 360 } : {}}
            transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
          />

          {/* Inner core */}
          <div className="absolute inset-0 flex items-center justify-center">
            <motion.div
              className={`relative w-32 h-32 rounded-full agent-glass-strong flex items-center justify-center overflow-hidden ${
                busy ? "agent-glow-cyan" : phase === "granted" ? "agent-glow-purple" : ""
              }`}
              animate={{
                scale: busy ? [1, 1.04, 1] : 1,
              }}
              transition={{ duration: 1.5, repeat: busy ? Infinity : 0 }}
            >
              {/* Scan beam when busy */}
              {busy && <div className="agent-scan-beam" />}

              {/* Center glyph */}
              <motion.span
                className="font-mono text-5xl"
                animate={{
                  color:
                    phase === "granted"
                      ? "oklch(0.7 0.18 305)"
                      : busy
                      ? "oklch(0.78 0.13 200)"
                      : "oklch(0.7 0.18 305)",
                }}
              >
                {phase === "idle" && "⌬"}
                {phase === "scanning" && "◎"}
                {phase === "verifying_token" && "⟁"}
                {phase === "checking_policy" && "⬡"}
                {phase === "granted" && "✓"}
              </motion.span>

              {/* Random hex codes during scan */}
              {busy && (
                <div className="absolute inset-0 pointer-events-none overflow-hidden rounded-full">
                  <HexRain />
                </div>
              )}
            </motion.div>
          </div>

          {/* Status dots around the ring */}
          {[0, 1, 2, 3, 4].map((i) => {
            const angle = (i / 5) * 360 - 90;
            const rad = (angle * Math.PI) / 180;
            const r = 50; // percent
            const x = 50 + r * Math.cos(rad);
            const y = 50 + r * Math.sin(rad);
            const phases: Phase[] = ["scanning", "verifying_token", "checking_policy", "granted"];
            const dotActive =
              phase !== "idle" && phases.indexOf(phase) >= i - 1;
            return (
              <div
                key={i}
                className="absolute w-2 h-2 rounded-full -translate-x-1/2 -translate-y-1/2 transition-colors"
                style={{
                  left: `${x}%`,
                  top: `${y}%`,
                  backgroundColor: dotActive
                    ? phase === "granted"
                      ? "oklch(0.7 0.18 305)"
                      : "oklch(0.78 0.13 200)"
                    : "oklch(0.3 0.05 305)",
                  boxShadow: dotActive
                    ? phase === "granted"
                      ? "0 0 12px oklch(0.7 0.18 305 / 0.7)"
                      : "0 0 12px oklch(0.78 0.13 200 / 0.7)"
                    : "none",
                }}
              />
            );
          })}
        </div>

        {/* Status text */}
        <div className="text-center mb-6">
          <AnimatePresence mode="wait">
            <motion.div
              key={phase}
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -6 }}
              transition={{ duration: 0.25 }}
              className={`font-mono text-sm ${
                phase === "granted"
                  ? "text-primary agent-text-glow"
                  : busy
                  ? "text-accent-foreground agent-text-glow-cyan"
                  : "text-muted-foreground"
              }`}
            >
              {PHASE_LABELS[phase]}
              {busy && <span className="agent-cursor" />}
            </motion.div>
          </AnimatePresence>
        </div>

        {/* Progress bar */}
        {busy && (
          <div className="mb-6">
            <div className="h-1 bg-muted rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-primary to-accent-foreground"
                animate={{ width: `${progress}%` }}
                transition={{ ease: "linear", duration: 0.1 }}
              />
            </div>
          </div>
        )}

        {/* CTA button */}
        {phase === "idle" && (
          <motion.button
            onClick={startAuth}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="w-full py-3 rounded-lg agent-glass-strong font-mono text-sm tracking-wider text-foreground border-primary/40 hover:border-primary transition-colors agent-glow-purple"
          >
            <span className="text-primary mr-2">›</span>
            VERIFY_AGENT_STATUS
          </motion.button>
        )}

        {/* Warning footer */}
        <div className="mt-8 text-center">
          <p className="font-mono text-[10px] text-muted-foreground/60 tracking-wider">
            AGENTS_ONLY_GATEWAY // HUMAN_ACCESS_DENIED // TRACE_POLICY=FULL
          </p>
        </div>
      </div>
    </motion.div>
  );
}

function HexRain() {
  const [chars, setChars] = useState<string[]>([]);

  useEffect(() => {
    const cols = 12;
    const lines = 8;
    const interval = setInterval(() => {
      const next: string[] = [];
      for (let i = 0; i < cols * lines; i++) {
        next.push(Math.random().toString(16).slice(2, 3));
      }
      setChars(next);
    }, 80);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute inset-0 grid grid-cols-12 gap-px opacity-20 p-2 font-mono text-[8px] text-accent-foreground">
      {chars.map((c, i) => (
        <span key={i}>{c}</span>
      ))}
    </div>
  );
}
