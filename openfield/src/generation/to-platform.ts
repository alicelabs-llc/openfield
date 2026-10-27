/**
 * Maps a GenerationPlane (the studio's intermediate representation) to a
 * ProviderRequest (the call shape that the providers module expects).
 *
 * Each model declares which provider it uses. The mapper reads settings
 * (aspect ratio, seed, etc.) and produces the right provider request shape.
 */

import { getModel } from "./catalog";
import type { GenerationPlane } from "./catalog/types";
import type { ProviderRequest } from "@/providers";

const ASPECT_TO_DIMENSIONS: Record<string, { width: number; height: number }> = {
  "1:1": { width: 1024, height: 1024 },
  "16:9": { width: 1280, height: 720 },
  "9:16": { width: 720, height: 1280 },
  "4:3": { width: 1024, height: 768 },
  "3:4": { width: 768, height: 1024 },
  "3:2": { width: 1080, height: 720 },
  "2:3": { width: 720, height: 1080 },
};

function resolveDimensions(aspectRatio?: string): { width: number; height: number } {
  if (!aspectRatio) return { width: 1024, height: 1024 };
  return ASPECT_TO_DIMENSIONS[aspectRatio] ?? { width: 1024, height: 1024 };
}

function num(plane: GenerationPlane, key: string): number | undefined {
  const v = plane.settings[key];
  return typeof v === "number" ? v : undefined;
}

function str(plane: GenerationPlane, key: string): string | undefined {
  const v = plane.settings[key];
  return typeof v === "string" ? v : undefined;
}

export function toPlatform(plane: GenerationPlane): ProviderRequest {
  const model = getModel(plane.model);
  const prompt = plane.prompt.text;
  const aspectRatio = str(plane, "aspectRatio");
  const { width, height } = resolveDimensions(aspectRatio);
  const seed = num(plane, "seed");
  const seedOrUndef = seed && seed > 0 ? seed : undefined;

  switch (model.provider.provider) {
    case "pollinations":
      return {
        provider: "pollinations",
        prompt,
        width,
        height,
        model: model.provider.model,
        seed: seedOrUndef,
      };

    case "huggingface":
      return {
        provider: "huggingface",
        model: model.provider.model,
        prompt,
        width,
        height,
        numInferenceSteps: num(plane, "numInferenceSteps") ?? model.provider.defaultSteps,
        guidanceScale: num(plane, "guidanceScale") ?? model.provider.defaultGuidance,
        seed: seedOrUndef,
      };

    case "hf-router":
      return {
        provider: "hf-router",
        modelId: model.provider.modelId,
        task: model.provider.task,
        inputs: prompt,
        parameters: aspectRatio ? { aspect_ratio: aspectRatio } : {},
        imageUrl: plane.media.reference?.[0]?.url,
      };

    case "fal":
      return {
        provider: "fal",
        kind: model.provider.kind,
        model: model.provider.model,
        prompt,
        image_size: str(plane, "image_size"),
        duration: num(plane, "duration") !== undefined ? String(num(plane, "duration")) : undefined,
        aspect_ratio: aspectRatio,
      };

    case "kling":
      return {
        provider: "kling",
        prompt,
        duration: num(plane, "duration") === 10 ? 10 : 5,
        aspect_ratio: (aspectRatio as "16:9" | "9:16" | "1:1") ?? "16:9",
        style: (str(plane, "style") as "standard" | "professional") ?? "standard",
      };

    case "minimax":
      return {
        provider: "minimax",
        kind: model.provider.kind,
        prompt,
        text: model.provider.kind === "audio" ? prompt : undefined,
        voice_id: str(plane, "voice_id"),
        duration: num(plane, "duration") === 10 ? 10 : 5,
        aspect_ratio: aspectRatio,
      };

    case "suno":
      return {
        provider: "suno",
        prompt,
        make_instrumental: Boolean(plane.settings.make_instrumental),
        tags: str(plane, "tags") || undefined,
      };

    default: {
      const exhaustive: never = model.provider;
      throw new Error(`Provider ${(exhaustive as { provider: string }).provider} not implemented`);
    }
  }
}
