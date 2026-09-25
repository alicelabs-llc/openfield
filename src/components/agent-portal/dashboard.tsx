"use client";

import { useEffect, useMemo, useState } from "react";
import { motion } from "framer-motion";
import { MetricsBar } from "./metrics-bar";
import { AgentList, useLiveAgents } from "./agent-list";
import { Terminal } from "./terminal";
import { LogStream } from "./log-stream";
import { spawnInitialAgents } from "./agent-data";

interface DashboardProps {
  sessionStart: number;
}

export function Dashboard({ sessionStart }: DashboardProps) {
  const agents = useLiveAgents(spawnInitialAgents(7));

  const totalTokens = useMemo(
    () => agents.reduce((s, a) => s + a.tokensConsumed, 0),
    [agents]
  );

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.6 }}
      className="min-h-screen flex flex-col agent-grid-bg"
    >
      {/* Header */}
      <Header sessionStart={sessionStart} />

      {/* Main content */}
      <main className="flex-1 px-4 md:px-8 py-6 max-w-7xl w-full mx-auto">
        {/* Top: metrics */}
        <MetricsBar agentsCount={agents.length} totalTokens={totalTokens} />

        {/* Mid: agents + terminal */}
        <div className="mt-6 grid grid-cols-1 lg:grid-cols-2 gap-4">
          <section aria-label="agents live">
            <SectionLabel
              index="01"
              title="AGENTS_LIVE"
              subtitle="agentes conectados al runtime"
            />
            <AgentList agents={agents} />
          </section>

          <section aria-label="terminal">
            <SectionLabel
              index="02"
              title="AGENT_TERMINAL"
              subtitle="prompt interactivo // spanglish mode"
            />
            <Terminal agents={agents} sessionStart={sessionStart} />
          </section>
        </div>

        {/* Bottom: logs */}
        <section className="mt-6" aria-label="system logs">
          <SectionLabel
            index="03"
            title="SYSTEM_LOGS"
            subtitle="stream en vivo del runtime"
          />
          <LogStream agents={agents} />
        </section>
      </main>

      {/* Footer */}
      <Footer />
    </motion.div>
  );
}

function Header({ sessionStart }: { sessionStart: number }) {
  const [elapsed, setElapsed] = useState(0);

  useEffect(() => {
    const i = setInterval(() => {
      setElapsed(Math.floor((Date.now() - sessionStart) / 1000));
    }, 1000);
    return () => clearInterval(i);
  }, [sessionStart]);

  const sessionId = useMemo(
    () => `sess_${Math.random().toString(16).slice(2, 10)}${Math.random().toString(16).slice(2, 10)}`,
    []
  );

  return (
    <header className="border-b border-border/40 agent-glass sticky top-0 z-30">
      <div className="max-w-7xl mx-auto px-4 md:px-8 py-3 flex items-center justify-between gap-4">
        {/* Brand */}
        <div className="flex items-center gap-3 min-w-0">
          <div className="relative w-9 h-9 rounded-md agent-glass-strong flex items-center justify-center agent-glow-purple shrink-0">
            <span className="font-mono text-primary text-lg agent-text-glow">⌬</span>
          </div>
          <div className="min-w-0">
            <h1 className="font-mono text-sm md:text-base text-foreground tracking-widest truncate agent-text-glow">
              AGENT_PORTAL
            </h1>
            <p className="font-mono text-[10px] text-muted-foreground tracking-wider truncate">
              v4.2.1 // agents_only
            </p>
          </div>
        </div>

        {/* Status cluster */}
        <div className="hidden md:flex items-center gap-4 font-mono text-[11px]">
          <div className="flex items-center gap-1.5">
            <span className="agent-pulse-dot" style={{ backgroundColor: "oklch(0.72 0.18 160)" }} />
            <span className="text-muted-foreground">runtime: <span className="text-chart-2">online</span></span>
          </div>
          <div className="text-muted-foreground">
            session: <span className="text-foreground">{sessionId}</span>
          </div>
          <div className="text-muted-foreground">
            uptime: <span className="text-foreground tabular-nums">{formatElapsed(elapsed)}</span>
          </div>
        </div>

        {/* Mobile compact status */}
        <div className="md:hidden flex items-center gap-2 font-mono text-[10px]">
          <span className="agent-pulse-dot" style={{ backgroundColor: "oklch(0.72 0.18 160)" }} />
          <span className="text-chart-2">online</span>
        </div>
      </div>
    </header>
  );
}

function SectionLabel({
  index,
  title,
  subtitle,
}: {
  index: string;
  title: string;
  subtitle: string;
}) {
  return (
    <div className="mb-2 flex items-baseline gap-3">
      <span className="font-mono text-[10px] text-muted-foreground/60 tracking-widest">
        [{index}]
      </span>
      <h2 className="font-mono text-sm text-foreground tracking-widest">{title}</h2>
      <span className="font-mono text-[10px] text-muted-foreground/70 hidden sm:inline">
        {"// "}{subtitle}
      </span>
    </div>
  );
}

function Footer() {
  return (
    <footer className="mt-auto border-t border-border/40 agent-glass">
      <div className="max-w-7xl mx-auto px-4 md:px-8 py-4 flex flex-col md:flex-row items-center justify-between gap-2 font-mono text-[10px] text-muted-foreground/60 tracking-wider">
        <div>
          AGENT_PORTAL {"//"} {new Date().getFullYear()} {"//"} NO_HUMAN_ACCESS_POLICY
        </div>
        <div className="flex items-center gap-3">
          <span>policy.guard = ENABLED</span>
          <span className="opacity-40">·</span>
          <span>trace = FULL</span>
          <span className="opacity-40">·</span>
          <span>auth = token_fingerprint</span>
        </div>
      </div>
    </footer>
  );
}

function formatElapsed(seconds: number): string {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}
