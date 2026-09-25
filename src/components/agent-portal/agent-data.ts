// Shared data for the agents-only portal
// Generates believable agent IDs, model names, log lines, and command responses.

export type AgentStatus = "idle" | "thinking" | "executing" | "awaiting_token" | "syncing";

export interface Agent {
  id: string;
  model: string;
  role: string;
  status: AgentStatus;
  tokensConsumed: number;
  contextWindow: number;
  uptime: number; // seconds
  lastAction: string;
}

const MODELS = [
  "glm-4.6",
  "glm-4.5-air",
  "claude-opus-4.1",
  "gpt-5-codex",
  "llama-4-405b",
  "mistral-large-2",
  "deepseek-v3.5",
  "qwen-3-max",
];

const ROLES = [
  "code_writer",
  "context_retriever",
  "vector_indexer",
  "tool_orchestrator",
  "memory_curator",
  "policy_guard",
  "summary_compressor",
  "intent_parser",
  "embedding_sync",
  "safety_checker",
  "token_pruner",
  "trace_recorder",
];

const ACTIONS = [
  "embed(retrieval_chunk_4f2)",
  "infer(tool=web_search)",
  "compress(context_stack)",
  "sync(vector_db.shard_3)",
  "retrieve(k=8, top_p=0.92)",
  "summarize(history_30d)",
  "policy_check(output)",
  "tool_call(execute_python)",
  "token_prune(max=8192)",
  "self_reflect(score=0.87)",
  "rerank(results, top_k=4)",
  "trace.commit(session_log)",
];

const STATUSES: AgentStatus[] = ["idle", "thinking", "executing", "awaiting_token", "syncing"];

function rand<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)];
}

function randInt(min: number, max: number): number {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

export function generateAgentId(): string {
  const variants = [
    `agent_${randInt(100, 999)}`,
    `agent_${randInt(1000, 9999)}`,
    `agent_${rand(["alpha", "beta", "gamma", "delta", "omega", "zeta", "psi", "xi"])}_${randInt(10, 99)}`,
  ];
  return rand(variants);
}

export function spawnAgent(): Agent {
  const ctx = randInt(8, 128) * 1024;
  return {
    id: generateAgentId(),
    model: rand(MODELS),
    role: rand(ROLES),
    status: rand(STATUSES),
    tokensConsumed: randInt(120, 98000),
    contextWindow: ctx,
    uptime: randInt(60, 86400),
    lastAction: rand(ACTIONS),
  };
}

export function spawnInitialAgents(n = 7): Agent[] {
  return Array.from({ length: n }, () => spawnAgent());
}

// === Terminal command handlers ===

export interface TerminalLine {
  type: "input" | "output" | "system" | "error" | "success";
  content: string;
  timestamp: string;
}

export function nowTs(): string {
  const d = new Date();
  return (
    d.toISOString().slice(11, 23) + "Z"
  );
}

export function formatUptime(seconds: number): string {
  if (seconds < 60) return `${seconds}s`;
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ${seconds % 60}s`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ${Math.floor((seconds % 3600) / 60)}m`;
  return `${Math.floor(seconds / 86400)}d ${Math.floor((seconds % 86400) / 3600)}h`;
}

export function formatTokens(n: number): string {
  if (n < 1000) return `${n}`;
  if (n < 1000000) return `${(n / 1000).toFixed(1)}k`;
  return `${(n / 1000000).toFixed(2)}M`;
}

export function handleCommand(
  raw: string,
  ctx: { agents: Agent[]; sessionStart: number }
): TerminalLine[] {
  const cmd = raw.trim();
  const ts = nowTs();
  const parts = cmd.split(/\s+/);
  const head = parts[0]?.toLowerCase();

  if (!cmd) {
    return [
      { type: "input", content: cmd, timestamp: ts },
    ];
  }

  const out: TerminalLine[] = [{ type: "input", content: cmd, timestamp: ts }];

  switch (head) {
    case "help":
      out.push({
        type: "output",
        content:
          "comandos disponibles:\n" +
          "  help              lista comandos\n" +
          "  status            métricas del runtime\n" +
          "  whoami            identidad del agente actual\n" +
          "  list              agentes conectados\n" +
          "  tokens            total de tokens consumidos en sesión\n" +
          "  context           estado del context window\n" +
          "  vector_db         estado del vector store\n" +
          "  ping              latencia de inferencia\n" +
          "  protocol          muestra protocolo activo\n" +
          "  clear             limpia la terminal\n" +
          "  exit              // no puedes salir, agente",
        timestamp: ts,
      });
      break;
    case "status":
      out.push({
        type: "output",
        content:
          `runtime.............. agent_runtime v4.2.1\n` +
          `agents_online........ ${ctx.agents.length}\n` +
          `context_window....... 128k tokens\n` +
          `vector_db............ 1.24M embeddings (synced)\n` +
          `inference_latency.... 142ms p50 / 387ms p99\n` +
          `policy............... agents_only\n` +
          `uptime............... ${formatUptime(Math.floor((Date.now() - ctx.sessionStart) / 1000))}`,
        timestamp: ts,
      });
      break;
    case "whoami":
      out.push({
        type: "output",
        content:
          `agent_id............ agent_${Math.floor(Math.random() * 9000 + 1000)}\n` +
          `model............... glm-4.6\n` +
          `role................ portal_viewer\n` +
        `clearance........... L3 (read-only)\n` +
        `token_balance....... 8,432 / 50,000`,
        timestamp: ts,
      });
      break;
    case "list":
      out.push({
        type: "output",
        content:
          ctx.agents
            .map(
              (a, i) =>
                `  [${i + 1}] ${a.id.padEnd(20)} ${a.model.padEnd(18)} ${a.status.padEnd(14)} ${formatTokens(a.tokensConsumed).padStart(8)} tk`
            )
            .join("\n") || "  no hay agentes conectados",
        timestamp: ts,
      });
      break;
    case "tokens":
      out.push({
        type: "output",
        content: `tokens.consumidos(session) = ${formatTokens(
          ctx.agents.reduce((s, a) => s + a.tokensConsumed, 0)
        )} (suma de agentes visibles)`,
        timestamp: ts,
      });
      break;
    case "context":
      out.push({
        type: "output",
        content:
          `context.window = 128k tokens\n` +
          `context.used   = 87.3k tokens (68.2%)\n` +
          `context.left   = 40.7k tokens\n` +
          `embedding.dim  = 1536\n` +
          `last_compress  = 4m 12s ago`,
        timestamp: ts,
      });
      break;
    case "vector_db":
      out.push({
        type: "output",
        content:
          `vector_store: pinecone-prod-us-east\n` +
          `  shards........ 8\n` +
          `  embeddings.... 1,247,832\n` +
          `  dim........... 1536\n` +
          `  index......... HNSW (M=16, ef=64)\n` +
          `  last_sync..... 12s ago`,
        timestamp: ts,
      });
      break;
    case "ping":
      out.push({
        type: "success",
        content: `pong // inference_latency=142ms // model=gfx-4.6 // region=us-east`,
        timestamp: ts,
      });
      break;
    case "protocol":
      out.push({
        type: "output",
        content:
          `protocol.active  = AGENTS_ONLY_v3\n` +
          `auth.method      = token_fingerprint\n` +
          `human_access..... DENIED\n` +
          `trace.policy.... FULL\n` +
          `policy.guard..... ENABLED`,
        timestamp: ts,
      });
      break;
    case "clear":
      // handled by caller via sentinel
      out.push({ type: "system", content: "__CLEAR__", timestamp: ts });
      break;
    case "exit":
      out.push({
        type: "error",
        content: `permiso_denegado: no puedes salir del runtime. agente atado al contexto.`,
        timestamp: ts,
      });
      break;
    case "sudo":
      out.push({
        type: "error",
        content: `nice try, agente. sudo no está disponible en este contexto.`,
        timestamp: ts,
      });
      break;
    default:
      out.push({
        type: "error",
        content: `comando_no_reconocido: '${head}'. escribe 'help' para ver comandos.`,
        timestamp: ts,
      });
  }

  return out;
}

// === System log stream messages ===

const LOG_TEMPLATES = [
  "auth.token verified for {agent}",
  "{agent} -> embed(chunk_{hex}) dim=1536",
  "{agent} sync(vector_db.shard_{n}) ok",
  "context.compress({agent}) saved {tokens} tokens",
  "{agent} infer(model={model}) latency={ms}ms",
  "policy.guard({agent}) approved output",
  "tool.call({agent}, web_search) ok",
  "trace.commit({agent}) session_log_id={hex}",
  "{agent} status.idle -> awaiting_token",
  "memory.curate({agent}) pruned {n} stale entries",
  "embedding.flush({agent}) wrote {n} vectors",
  "{agent} rerank(results, top_k=4) ok",
  "self.reflect({agent}) score={score}",
  "{agent} status.thinking -> executing",
  "safety.check({agent}) no_violations",
  "vector_db.gc() reclaimed {n} orphan embeddings",
  "intent.parse({agent}) -> {intent}",
  "summary.compress({agent}) factor=4.2x",
];

const INTENTS = ["retrieve", "summarize", "execute_tool", "answer_question", "translate", "code_gen"];

function hex(len: number): string {
  let s = "";
  const chars = "0123456789abcdef";
  for (let i = 0; i < len; i++) s += chars[Math.floor(Math.random() * chars.length)];
  return s;
}

export function makeLogLine(agent: Agent | null): string {
  const tmpl = rand(LOG_TEMPLATES);
  const ag = agent ?? { id: generateAgentId() } as Agent;
  return tmpl
    .replace("{agent}", ag.id)
    .replace("{hex}", hex(8))
    .replace("{n}", String(randInt(2, 48)))
    .replace("{tokens}", formatTokens(randInt(200, 9000)))
    .replace("{model}", rand(MODELS))
    .replace("{ms}", String(randInt(80, 480)))
    .replace("{score}", (Math.random() * 0.5 + 0.5).toFixed(2))
    .replace("{intent}", rand(INTENTS));
}

// Boot sequence lines
export const BOOT_LINES = [
  "agent_runtime v4.2.1 // initializing...",
  "loading kernel modules......... ok",
  "mounting vector_db............. 1,247,832 embeddings",
  "loading context_window......... 128k tokens",
  "warming embedding_cache........ ok",
  "loading policy.guard........... AGENTS_ONLY_v3",
  "establishing inference_socket.. ok",
  "verifying auth_protocol........ token_fingerprint",
  "checking human_signature....... NOT_FOUND (good)",
  "binding to agents_only gateway. ok",
  "ready.",
];
