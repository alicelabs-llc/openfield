/**
 * Client-side generation actions for static export (Cloudflare Pages / GitHub Pages).
 * Only Pollinations models work without a backend proxy.
 * Settings page (/settings) lets users manage all API keys for future dynamic deploy.
 */
import type { QueuedRequest, GenerationResult } from "@/providers";
import { buildPollinationsImageUrl } from "@/providers/pollinations";

const CREDENTIALS_KEY = "openfield_creds_static";

export class MissingCredentialsError extends Error {
  constructor() {
    super(
      "This model requires a Node.js runtime. On static hosting, only Pollinations models work. Deploy with Vercel/Netlify/Cloudflare Workers to use all 28 models.",
    );
    this.name = "MissingCredentialsError";
  }
}

type StoredCreds = Record<string, string>;

export async function savePlatformCredentials(data: unknown): Promise<void> {
  if (typeof window === "undefined") return;
  const stored = readStored() ?? {};
  const incoming = data as Record<string, unknown>;
  const merged: StoredCreds = { ...stored };
  for (const [k, v] of Object.entries(incoming)) {
    if (typeof v === "string" && v.trim()) merged[k] = v.trim();
  }
  window.localStorage.setItem(CREDENTIALS_KEY, JSON.stringify(merged));
}

export async function clearPlatformCredentials(): Promise<void> {
  if (typeof window === "undefined") return;
  window.localStorage.removeItem(CREDENTIALS_KEY);
}

export async function hasPlatformCredentials(): Promise<boolean> {
  return readStored() !== null;
}

export async function listStoredProviders(): Promise<string[]> {
  const stored = readStored();
  if (!stored) return [];
  return Object.keys(stored);
}

export async function submitGeneration(plane: {
  model: string;
  prompt: { text: string };
  settings: Record<string, unknown>;
}): Promise<QueuedRequest> {
  const modelId = plane.model;
  const promptText = plane.prompt.text;

  // Only Pollinations models supported in static mode
  if (!modelId.startsWith("pollinations-")) {
    throw new Error(
      `Model "${modelId}" requires a backend runtime. On static hosting, only Pollinations models work. Visit /settings to get API keys for other providers, then deploy with a Node.js runtime.`,
    );
  }

  const modelMap: Record<string, "flux" | "flux-realism" | "flux-anime" | "flux-3d" | "turbo"> = {
    "pollinations-flux": "flux",
    "pollinations-turbo": "turbo",
    "pollinations-flux-realism": "flux-realism",
    "pollinations-flux-anime": "flux-anime",
    "pollinations-flux-3d": "flux-3d",
  };

  const model = modelMap[modelId] ?? "flux";
  const aspect = (plane.settings.aspectRatio as string) ?? "1:1";
  const dims = ASPECT_TO_DIMENSIONS[aspect] ?? { width: 1024, height: 1024 };
  const seed =
    typeof plane.settings.seed === "number" && plane.settings.seed > 0
      ? plane.settings.seed
      : Math.floor(Math.random() * 999999);

  const url = buildPollinationsImageUrl({
    prompt: promptText,
    width: dims.width,
    height: dims.height,
    model,
    seed,
    nologo: true,
  });

  return {
    requestId: `static-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    statusUrl: url,
    provider: "pollinations",
  };
}

const ASPECT_TO_DIMENSIONS: Record<string, { width: number; height: number }> = {
  "1:1": { width: 1024, height: 1024 },
  "16:9": { width: 1280, height: 720 },
  "9:16": { width: 720, height: 1280 },
  "4:3": { width: 1024, height: 768 },
  "3:4": { width: 768, height: 1024 },
  "3:2": { width: 1080, height: 720 },
  "2:3": { width: 720, height: 1080 },
};

export async function getGenerationStatuses(data: unknown): Promise<Array<GenerationResult>> {
  const payload = data as { requests: Array<QueuedRequest> };
  if (!Array.isArray(payload.requests) || payload.requests.length === 0) {
    throw new Error("Invalid request list");
  }
  return payload.requests.map((req) => ({
    status: "completed" as const,
    requestId: req.requestId,
    images: [{ url: req.statusUrl }],
  }));
}

function readStored(): StoredCreds | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = window.localStorage.getItem(CREDENTIALS_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as StoredCreds;
    if (!parsed || typeof parsed !== "object") return null;
    return parsed;
  } catch {
    return null;
  }
}
