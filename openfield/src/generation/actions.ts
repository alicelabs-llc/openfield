/**
 * Client-side generation actions — for static export (GitHub Pages, Cloudflare Pages static).
 *
 * In static mode, we can only use providers that:
 * 1. Don't require server-side API keys (no HF, fal.ai, Kling, MiniMax, Suno)
 * 2. Allow CORS from the browser (Pollinations does — the URL IS the image)
 *
 * For non-Pollinations models, we throw a clear error explaining why.
 */

import type { QueuedRequest, GenerationResult } from "@/providers";
import { buildPollinationsImageUrl } from "@/providers/pollinations";

const CREDENTIALS_KEY = "openfield_creds_static";

type StoredCreds = {
  hfToken?: string;
  falKey?: string;
  klingJwt?: string;
  minimaxKey?: string;
  sunoToken?: string;
};

export class MissingCredentialsError extends Error {
  constructor() {
    super(
      "This model requires a Node.js runtime (HuggingFace, fal.ai, Kling, MiniMax, Suno). On static hosting (GitHub Pages), only Pollinations models work without a backend.",
    );
    this.name = "MissingCredentialsError";
  }
}

export async function savePlatformCredentials(data: unknown): Promise<void> {
  if (typeof window === "undefined") return;
  const stored = readStored() ?? {};
  const incoming = data as Record<string, unknown>;
  const merged: StoredCreds = { ...stored };
  for (const key of ["hfToken", "falKey", "klingJwt", "minimaxKey", "sunoToken"] as const) {
    const v = incoming[key] ?? incoming[key.toLowerCase()];
    if (typeof v === "string" && v.trim()) {
      merged[key] = v.trim();
    }
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

/**
 * In static mode, only Pollinations can be called directly from the browser
 * (the URL itself returns the image bytes). All other providers require a
 * backend proxy to keep API keys safe.
 */
export async function submitGeneration(plane: {
  model: string;
  prompt: { text: string };
  settings: Record<string, unknown>;
}): Promise<QueuedRequest> {
  const modelId = plane.model;
  const promptText = plane.prompt.text;

  // Only Pollinations models are supported in static mode
  if (!modelId.startsWith("pollinations-")) {
    throw new Error(
      `Model "${modelId}" requires a backend runtime. On static hosting, only Pollinations models work. ` +
        `Deploy with a Node.js runtime (Vercel/Netlify/Cloudflare Workers) to use this model.`,
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

/**
 * In static mode, results are immediately "completed" because the statusUrl
 * IS the image URL — the browser fetches it on render.
 */
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
