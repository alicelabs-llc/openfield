import { FREE_MODELS } from "./free-models";
import type { ModelEntry } from "./types";

/**
 * In static export mode (GitHub Pages, Cloudflare Pages static), only
 * Pollinations models work because they don't require a backend proxy.
 * The other providers (HF, fal.ai, Kling, MiniMax, Suno) need server actions
 * to keep API keys safe — those require a Node.js runtime like Vercel.
 */
const isStatic = process.env.NEXT_PUBLIC_STATIC_MODE === "true";

export const MODELS: readonly ModelEntry[] = isStatic
  ? FREE_MODELS.filter((m) => m.provider.provider === "pollinations")
  : FREE_MODELS;

export function getModel(id: string): ModelEntry {
  const model = MODELS.find((entry) => entry.id === id);
  if (!model) {
    // Fall back to the full catalog so we can show a clear error
    const fallback = FREE_MODELS.find((entry) => entry.id === id);
    if (fallback) return fallback;
    throw new Error(`Unknown model: ${id}`);
  }
  return model;
}

export type { GenerationPlane, MediaItem, MediaRole, ModelEntry, Surface } from "./types";
export { parseSettings } from "./parse-settings";
