"use client";

import { useEffect, useRef, useState } from "react";
import { motion } from "framer-motion";
import {
  Agent,
  TerminalLine,
  handleCommand,
  nowTs,
} from "./agent-data";

interface TerminalProps {
  agents: Agent[];
  sessionStart: number;
}

const WELCOME_LINES: TerminalLine[] = [
  {
    type: "system",
    content: "// terminal conectada al runtime de agentes",
    timestamp: nowTs(),
  },
  {
    type: "system",
    content: "// escribe 'help' para ver comandos disponibles",
    timestamp: nowTs(),
  },
];

export function Terminal({ agents, sessionStart }: TerminalProps) {
  const [lines, setLines] = useState<TerminalLine[]>(WELCOME_LINES);
  const [input, setInput] = useState("");
  const [history, setHistory] = useState<string[]>([]);
  const [historyIdx, setHistoryIdx] = useState(-1);
  const scrollRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // autoscroll
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [lines]);

  // focus input on mount
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const runCommand = (raw: string) => {
    const newLines = handleCommand(raw, { agents, sessionStart });

    // Check for __CLEAR__ sentinel
    const clearIdx = newLines.findIndex((l) => l.content === "__CLEAR__");
    if (clearIdx !== -1) {
      // remove the clear sentinel and reset lines
      setLines(WELCOME_LINES);
      return;
    }

    setLines((prev) => [...prev, ...newLines]);
  };

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) {
      // still echo empty
      runCommand(input);
      setInput("");
      return;
    }
    runCommand(input);
    setHistory((prev) => [...prev, input]);
    setHistoryIdx(-1);
    setInput("");
  };

  const onKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "ArrowUp") {
      e.preventDefault();
      if (history.length === 0) return;
      const nextIdx = historyIdx === -1 ? history.length - 1 : Math.max(0, historyIdx - 1);
      setHistoryIdx(nextIdx);
      setInput(history[nextIdx]);
    } else if (e.key === "ArrowDown") {
      e.preventDefault();
      if (history.length === 0 || historyIdx === -1) return;
      const nextIdx = historyIdx + 1;
      if (nextIdx >= history.length) {
        setHistoryIdx(-1);
        setInput("");
      } else {
        setHistoryIdx(nextIdx);
        setInput(history[nextIdx]);
      }
    } else if (e.key === "Tab") {
      e.preventDefault();
      const cmds = ["help", "status", "whoami", "list", "tokens", "context", "vector_db", "ping", "protocol", "clear", "exit"];
      const matches = cmds.filter((c) => c.startsWith(input.trim().toLowerCase()));
      if (matches.length === 1) {
        setInput(matches[0]);
      }
    }
  };

  return (
    <div className="agent-glass rounded-lg overflow-hidden flex flex-col h-full">
      {/* Header */}
      <div className="px-4 py-2.5 border-b border-border/40 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="flex gap-1.5">
            <div className="w-2.5 h-2.5 rounded-full bg-destructive/60" />
            <div className="w-2.5 h-2.5 rounded-full bg-chart-4/60" />
            <div className="w-2.5 h-2.5 rounded-full bg-chart-2/60" />
          </div>
          <span className="ml-2 font-mono text-xs tracking-widest text-muted-foreground">
            agent@runtime:~$
          </span>
        </div>
        <span className="font-mono text-[10px] text-muted-foreground/60">
          session_active
        </span>
      </div>

      {/* Output */}
      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto agent-scroll px-4 py-3 font-mono text-xs space-y-1 max-h-80 min-h-[18rem]"
        onClick={() => inputRef.current?.focus()}
      >
        {lines.map((line, i) => (
          <Line key={i} line={line} />
        ))}
        {/* Active prompt */}
        <form onSubmit={onSubmit} className="flex items-center gap-2 mt-1">
          <span className="text-primary/80 shrink-0">›</span>
          <input
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={onKeyDown}
            spellCheck={false}
            autoComplete="off"
            className="flex-1 bg-transparent outline-none border-none font-mono text-xs text-foreground caret-accent-foreground"
            placeholder="escribe un comando... (try 'help')"
            aria-label="terminal input"
          />
        </form>
      </div>
    </div>
  );
}

function Line({ line }: { line: TerminalLine }) {
  const colorClass =
    line.type === "input"
      ? "text-foreground"
      : line.type === "output"
      ? "text-muted-foreground"
      : line.type === "error"
      ? "text-destructive"
      : line.type === "success"
      ? "text-chart-2"
      : "text-primary/70";

  const prefix =
    line.type === "input" ? "›" : line.type === "system" ? "//" : "";

  if (line.type === "input") {
    return (
      <div className="flex gap-2">
        <span className="text-primary/80 shrink-0">{prefix}</span>
        <span className={colorClass}>{line.content}</span>
      </div>
    );
  }

  return (
    <div className={`whitespace-pre-wrap ${colorClass}`}>
      {prefix && <span className="mr-2 opacity-70">{prefix}</span>}
      {line.content}
    </div>
  );
}
