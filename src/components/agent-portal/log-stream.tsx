"use client";

import { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Agent, makeLogLine, nowTs } from "./agent-data";

interface LogStreamProps {
  agents: Agent[];
  maxLines?: number;
}

interface LogEntry {
  id: number;
  ts: string;
  msg: string;
}

export function LogStream({ agents, maxLines = 60 }: LogStreamProps) {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const counterRef = useRef(0);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // seed a few logs immediately
    const seed: LogEntry[] = Array.from({ length: 8 }, () => {
      counterRef.current += 1;
      return {
        id: counterRef.current,
        ts: nowTs(),
        msg: makeLogLine(null),
      };
    });
    setLogs(seed);

    const interval = setInterval(() => {
      const ag = agents.length > 0 ? agents[Math.floor(Math.random() * agents.length)] : null;
      counterRef.current += 1;
      const entry: LogEntry = {
        id: counterRef.current,
        ts: nowTs(),
        msg: makeLogLine(ag),
      };
      setLogs((prev) => [...prev.slice(-(maxLines - 1)), entry]);
    }, 1200);

    return () => clearInterval(interval);
  }, [agents, maxLines]);

  // autoscroll to bottom on new entries (only if user is at bottom)
  const stickRef = useRef(true);
  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    if (stickRef.current) {
      el.scrollTop = el.scrollHeight;
    }
  }, [logs]);

  const onScroll = () => {
    const el = containerRef.current;
    if (!el) return;
    const atBottom = el.scrollHeight - el.scrollTop - el.clientHeight < 24;
    stickRef.current = atBottom;
  };

  return (
    <div className="agent-glass rounded-lg overflow-hidden flex flex-col h-full">
      {/* Header */}
      <div className="px-4 py-2.5 border-b border-border/40 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="agent-pulse-dot" style={{ backgroundColor: "oklch(0.72 0.18 160)" }} />
          <span className="font-mono text-xs tracking-widest text-muted-foreground">
            SYSTEM_LOGS
          </span>
        </div>
        <span className="font-mono text-[10px] text-muted-foreground/60">
          tail -f /var/log/agent_runtime
        </span>
      </div>

      {/* Logs */}
      <div
        ref={containerRef}
        onScroll={onScroll}
        className="flex-1 overflow-y-auto agent-scroll px-3 py-2 font-mono text-[11px] space-y-0.5 max-h-96 min-h-[18rem]"
      >
        <AnimatePresence initial={false}>
          {logs.map((log) => (
            <LogRow key={log.id} entry={log} />
          ))}
        </AnimatePresence>
      </div>
    </div>
  );
}

function LogRow({ entry }: { entry: LogEntry }) {
  const isError = /denied|fail|error|violation/i.test(entry.msg);
  const isWarn = /prune|gc|stale|awaiting/i.test(entry.msg);
  const isOk = /ok|approved|verified|complete|sync/i.test(entry.msg);

  const tsColor = "text-muted-foreground/50";
  const msgColor = isError
    ? "text-destructive/80"
    : isWarn
    ? "text-chart-4/80"
    : isOk
    ? "text-chart-2/80"
    : "text-foreground/70";

  return (
    <motion.div
      initial={{ opacity: 0, y: 4 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.2 }}
      className="flex gap-2 leading-tight"
    >
      <span className={`shrink-0 ${tsColor}`}>{entry.ts}</span>
      <span className={`shrink-0 ${msgColor}`}>
        {isError ? "✗" : isWarn ? "▲" : isOk ? "✓" : "·"}
      </span>
      <span className={`flex-1 ${msgColor} break-all`}>{entry.msg}</span>
    </motion.div>
  );
}
