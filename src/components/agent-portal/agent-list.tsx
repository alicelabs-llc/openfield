"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Agent, AgentStatus, formatTokens, formatUptime, spawnAgent } from "./agent-data";

interface AgentListProps {
  agents: Agent[];
}

const STATUS_STYLES: Record<AgentStatus, { color: string; label: string; pulse: boolean }> = {
  idle: { color: "oklch(0.55 0.01 280)", label: "idle", pulse: false },
  thinking: { color: "oklch(0.78 0.13 200)", label: "thinking", pulse: true },
  executing: { color: "oklch(0.7 0.18 305)", label: "executing", pulse: true },
  awaiting_token: { color: "oklch(0.78 0.15 80)", label: "awaiting_token", pulse: true },
  syncing: { color: "oklch(0.72 0.18 160)", label: "syncing", pulse: true },
};

export function AgentList({ agents }: AgentListProps) {
  return (
    <div className="agent-glass rounded-lg overflow-hidden flex flex-col h-full">
      {/* Header */}
      <div className="px-4 py-3 border-b border-border/40 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="agent-pulse-dot bg-chart-2" style={{ backgroundColor: "oklch(0.78 0.13 200)" }} />
          <span className="font-mono text-xs tracking-widest text-muted-foreground">
            AGENTS_LIVE
          </span>
        </div>
        <span className="font-mono text-[10px] text-muted-foreground">
          {agents.length} conectados
        </span>
      </div>

      {/* Column header */}
      <div className="px-4 py-2 border-b border-border/30 grid grid-cols-12 gap-2 font-mono text-[10px] text-muted-foreground/70 tracking-wider">
        <div className="col-span-4">AGENT_ID</div>
        <div className="col-span-3">MODEL</div>
        <div className="col-span-3">STATUS</div>
        <div className="col-span-2 text-right">TOKENS</div>
      </div>

      {/* List */}
      <div className="flex-1 overflow-y-auto agent-scroll max-h-[28rem]">
        <AnimatePresence initial={false}>
          {agents.map((agent) => (
            <AgentRow key={agent.id} agent={agent} />
          ))}
        </AnimatePresence>
      </div>
    </div>
  );
}

function AgentRow({ agent }: { agent: Agent }) {
  const style = STATUS_STYLES[agent.status];
  return (
    <motion.div
      layout
      initial={{ opacity: 0, x: -10 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 10, transition: { duration: 0.2 } }}
      transition={{ duration: 0.3 }}
      className="px-4 py-2.5 border-b border-border/20 hover:bg-primary/5 transition-colors grid grid-cols-12 gap-2 items-center group"
    >
      <div className="col-span-4 min-w-0">
        <div className="font-mono text-xs text-foreground truncate group-hover:text-primary transition-colors">
          {agent.id}
        </div>
        <div className="font-mono text-[10px] text-muted-foreground truncate">
          {agent.role}
        </div>
      </div>

      <div className="col-span-3 font-mono text-[11px] text-muted-foreground truncate">
        {agent.model}
      </div>

      <div className="col-span-3 flex items-center gap-1.5 min-w-0">
        <span
          className={`agent-pulse-dot shrink-0 ${style.pulse ? "" : "opacity-60"}`}
          style={{ backgroundColor: style.color, width: 6, height: 6 }}
        />
        <span
          className="font-mono text-[10px] truncate"
          style={{ color: style.color }}
        >
          {style.label}
        </span>
      </div>

      <div className="col-span-2 text-right">
        <div className="font-mono text-[11px] text-foreground/90 tabular-nums">
          {formatTokens(agent.tokensConsumed)}
        </div>
        <div className="font-mono text-[9px] text-muted-foreground tabular-nums">
          {formatUptime(agent.uptime)}
        </div>
      </div>
    </motion.div>
  );
}

// Hook for live agents — used by parent dashboard
export function useLiveAgents(initial: Agent[]) {
  const [agents, setAgents] = useState<Agent[]>(initial);

  useEffect(() => {
    // Status flip every ~1.5s
    const statusInterval = setInterval(() => {
      setAgents((prev) =>
        prev.map((a) => {
          if (Math.random() < 0.4) {
            const statuses: AgentStatus[] = [
              "idle",
              "thinking",
              "executing",
              "awaiting_token",
              "syncing",
            ];
            return {
              ...a,
              status: statuses[Math.floor(Math.random() * statuses.length)],
              tokensConsumed: a.tokensConsumed + Math.floor(Math.random() * 200),
              uptime: a.uptime + 2,
            };
          }
          return { ...a, uptime: a.uptime + 2, tokensConsumed: a.tokensConsumed + Math.floor(Math.random() * 30) };
        })
      );
    }, 2000);

    // Spawn / drop agents every ~6s
    const churnInterval = setInterval(() => {
      setAgents((prev) => {
        const next = [...prev];
        const r = Math.random();
        if (r < 0.45 && next.length < 12) {
          next.push(spawnAgent());
        } else if (r > 0.85 && next.length > 4) {
          // remove random
          const idx = Math.floor(Math.random() * next.length);
          next.splice(idx, 1);
        }
        return next;
      });
    }, 6000);

    return () => {
      clearInterval(statusInterval);
      clearInterval(churnInterval);
    };
  }, []);

  return agents;
}
