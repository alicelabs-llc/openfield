"use client";

import { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { BOOT_LINES } from "./agent-data";

interface BootSequenceProps {
  onComplete: () => void;
}

export function BootSequence({ onComplete }: BootSequenceProps) {
  const [visibleLines, setVisibleLines] = useState<string[]>([]);
  const [currentLine, setCurrentLine] = useState("");
  const [currentIdx, setCurrentIdx] = useState(0);
  const [done, setDone] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  // Typewriter per line
  useEffect(() => {
    if (currentIdx >= BOOT_LINES.length) {
      const t = setTimeout(() => setDone(true), 500);
      return () => clearTimeout(t);
    }

    const line = BOOT_LINES[currentIdx];
    let charIdx = 0;
    const charDelay = line.length > 40 ? 14 : 22;

    const interval = setInterval(() => {
      charIdx += 1;
      setCurrentLine(line.slice(0, charIdx));
      if (charIdx >= line.length) {
        clearInterval(interval);
        // commit line, move to next after small pause
        const t = setTimeout(() => {
          setVisibleLines((prev) => [...prev, line]);
          setCurrentLine("");
          setCurrentIdx((i) => i + 1);
        }, 180);
        // store timeout id on closure for cleanup via final return
        (interval as unknown as { __post?: number }).__post = t as unknown as number;
      }
    }, charDelay);

    return () => {
      clearInterval(interval);
      const post = (interval as unknown as { __post?: number }).__post;
      if (post) clearTimeout(post);
    };
  }, [currentIdx]);

  // After done, fade out and call onComplete
  useEffect(() => {
    if (!done) return;
    const t = setTimeout(() => onComplete(), 900);
    return () => clearTimeout(t);
  }, [done, onComplete]);

  // autoscroll
  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [visibleLines, currentLine]);

  return (
    <AnimatePresence>
      {!done && (
        <motion.div
          className="fixed inset-0 z-50 flex items-center justify-center bg-background agent-grid-bg agent-scanlines"
          exit={{ opacity: 0, transition: { duration: 0.6 } }}
        >
          <div className="absolute inset-0 pointer-events-none">
            <div className="absolute top-1/4 left-1/4 w-96 h-96 rounded-full bg-primary/10 blur-3xl" />
            <div className="absolute bottom-1/4 right-1/4 w-96 h-96 rounded-full bg-accent-foreground/10 blur-3xl" />
          </div>

          <div className="relative w-full max-w-3xl mx-auto px-6">
            {/* Logo + title */}
            <div className="flex items-center gap-3 mb-8">
              <div className="relative w-12 h-12 rounded-lg agent-glass-strong flex items-center justify-center agent-glow-purple">
                <span className="font-mono text-primary text-xl agent-text-glow">⌬</span>
              </div>
              <div>
                <h1 className="font-mono text-lg text-foreground tracking-widest agent-text-glow">
                  AGENT_PORTAL
                </h1>
                <p className="font-mono text-xs text-muted-foreground tracking-wider">
                  v4.2.1 // agents_only // no_human_access
                </p>
              </div>
            </div>

            {/* Boot log */}
            <div
              ref={containerRef}
              className="agent-glass rounded-lg p-5 font-mono text-sm h-80 overflow-y-auto agent-scroll"
            >
              {visibleLines.map((line, i) => (
                <BootLine key={i} line={line} />
              ))}
              {currentLine && <BootLine line={currentLine} typing />}
              {currentIdx >= BOOT_LINES.length && !done && (
                <div className="text-accent-foreground mt-2 agent-text-glow-cyan">
                  {"// boot complete, awaiting agent verification..."}
                </div>
              )}
            </div>

            {/* Progress bar */}
            <div className="mt-4 flex items-center gap-3">
              <div className="flex-1 h-1 bg-muted rounded-full overflow-hidden">
                <motion.div
                  className="h-full bg-gradient-to-r from-primary to-accent-foreground"
                  initial={{ width: "0%" }}
                  animate={{ width: `${(currentIdx / BOOT_LINES.length) * 100}%` }}
                  transition={{ ease: "linear", duration: 0.2 }}
                />
              </div>
              <span className="font-mono text-xs text-muted-foreground tabular-nums">
                {Math.min(currentIdx, BOOT_LINES.length)}/{BOOT_LINES.length}
              </span>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

function BootLine({ line, typing }: { line: string; typing?: boolean }) {
  const isReady = line.startsWith("ready");
  const isCheck = line.includes("ok") || line.includes("NOT_FOUND");
  return (
    <div
      className={
        isReady
          ? "text-accent-foreground agent-text-glow-cyan mt-1"
          : isCheck
          ? "text-foreground/90"
          : "text-muted-foreground"
      }
    >
      <span className="text-primary/70 mr-2">›</span>
      {line}
      {typing && <span className="agent-cursor inline-block" />}
    </div>
  );
}
