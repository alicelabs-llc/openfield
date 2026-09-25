"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { formatTokens } from "./agent-data";

interface MetricsBarProps {
  agentsCount: number;
  totalTokens: number;
}

interface Metric {
  label: string;
  value: string;
  delta?: string;
  trend?: "up" | "down" | "flat";
  accent: "purple" | "cyan" | "amber" | "green";
}

export function MetricsBar({ agentsCount, totalTokens }: MetricsBarProps) {
  const [latency, setLatency] = useState(142);
  const [contextUtil, setContextUtil] = useState(68.2);

  useEffect(() => {
    const i = setInterval(() => {
      setLatency((l) => Math.max(80, Math.min(420, l + (Math.random() - 0.5) * 30)));
      setContextUtil((c) =>
        Math.max(20, Math.min(95, c + (Math.random() - 0.5) * 4))
      );
    }, 2000);
    return () => clearInterval(i);
  }, []);

  const metrics: Metric[] = [
    {
      label: "AGENTS_ONLINE",
      value: String(agentsCount),
      delta: "+1",
      trend: "up",
      accent: "purple",
    },
    {
      label: "TOKENS_CONSUMED",
      value: formatTokens(totalTokens),
      delta: "+2.3k",
      trend: "up",
      accent: "cyan",
    },
    {
      label: "CONTEXT_UTIL",
      value: `${contextUtil.toFixed(1)}%`,
      delta: contextUtil > 70 ? "high" : "ok",
      trend: contextUtil > 70 ? "up" : "flat",
      accent: "amber",
    },
    {
      label: "INFERENCE_LATENCY",
      value: `${Math.round(latency)}ms`,
      delta: latency < 200 ? "p50" : "p99",
      trend: latency < 200 ? "down" : "up",
      accent: "green",
    },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
      {metrics.map((m, i) => (
        <MetricCard key={m.label} metric={m} index={i} />
      ))}
    </div>
  );
}

function MetricCard({ metric, index }: { metric: Metric; index: number }) {
  const accentColor =
    metric.accent === "purple"
      ? "text-primary"
      : metric.accent === "cyan"
      ? "text-accent-foreground"
      : metric.accent === "amber"
      ? "text-chart-4"
      : "text-chart-4";

  const glowClass =
    metric.accent === "purple"
      ? "agent-glow-purple"
      : metric.accent === "cyan"
      ? "agent-glow-cyan"
      : "";

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.08, duration: 0.4 }}
      className={`agent-glass rounded-lg p-4 relative overflow-hidden ${glowClass}`}
    >
      {/* Subtle bg gradient */}
      <div
        className="absolute -top-12 -right-12 w-32 h-32 rounded-full blur-2xl opacity-20"
        style={{
          background:
            metric.accent === "purple"
              ? "oklch(0.7 0.18 305)"
              : metric.accent === "cyan"
              ? "oklch(0.78 0.13 200)"
              : metric.accent === "amber"
              ? "oklch(0.78 0.15 80)"
              : "oklch(0.72 0.18 160)",
        }}
      />

      <div className="relative">
        <div className="flex items-center justify-between mb-2">
          <span className="font-mono text-[10px] tracking-widest text-muted-foreground">
            {metric.label}
          </span>
          {metric.trend === "up" && (
            <span className="font-mono text-[10px] text-chart-4">▲</span>
          )}
          {metric.trend === "down" && (
            <span className="font-mono text-[10px] text-chart-2">▼</span>
          )}
          {metric.trend === "flat" && (
            <span className="font-mono text-[10px] text-muted-foreground">▬</span>
          )}
        </div>
        <div className={`font-mono text-2xl font-semibold tabular-nums ${accentColor}`}>
          {metric.value}
        </div>
        {metric.delta && (
          <div className="mt-1 font-mono text-[10px] text-muted-foreground">
            {metric.delta}
          </div>
        )}
      </div>
    </motion.div>
  );
}
