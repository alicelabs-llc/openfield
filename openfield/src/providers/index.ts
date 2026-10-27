/**
 * Provider dispatch — picks the right provider per model id.
 *
 * Each catalog entry declares which `provider` it uses. This module is the
 * single switchboard that knows how to call each provider.
 */

import { submitPollinationsImage, pollPollinationsStatus } from "./pollinations";
import { submitHfImage, pollHfStatus } from "./huggingface";
import { submitHfRouter, pollHfRouterStatus } from "./hf-router";
import {
  submitFalImage,
  submitFalVideo,
  pollFalVideoStatus,
} from "./fal";
import { submitKlingVideo, pollKlingStatus } from "./kling";
import {
  submitMinimaxAudio,
  submitMinimaxVideo,
  pollMinimaxVideo,
} from "./minimax";
import { submitSunoSong, pollSunoStatus } from "./suno";
import { submitOpenRouter, pollOpenRouter } from "./openrouter";

export type ProviderName =
  | "pollinations"
  | "huggingface"
  | "hf-router"
  | "fal"
  | "kling"
  | "minimax"
  | "suno"
  | "openrouter";

export type ProviderRequest =
  | {
      provider: "pollinations";
      prompt: string;
      width?: number;
      height?: number;
      model?: "flux" | "flux-realism" | "flux-anime" | "flux-3d" | "flux-cablyai" | "turbo";
      seed?: number;
    }
  | {
      provider: "huggingface";
      model: string;
      prompt: string;
      width?: number;
      height?: number;
      numInferenceSteps?: number;
      guidanceScale?: number;
      negativePrompt?: string;
      seed?: number;
    }
  | {
      provider: "hf-router";
      modelId: string;
      task: "text-to-image" | "image-to-image" | "text-to-video" | "chat-completions";
      inputs: string;
      parameters?: Record<string, unknown>;
      imageUrl?: string;
      providerRouting?: "fal-ai" | "replicate" | "wavespeed" | "nscale" | "cerebras" | "groq" | "novita" | "deepinfra";
    }
  | {
      provider: "fal";
      kind: "image" | "video";
      model: string;
      prompt: string;
      image_size?: string;
      duration?: string;
      aspect_ratio?: string;
    }
  | {
      provider: "kling";
      prompt: string;
      duration?: 5 | 10;
      aspect_ratio?: "16:9" | "9:16" | "1:1";
      style?: "standard" | "professional";
    }
  | {
      provider: "minimax";
      kind: "audio" | "video";
      prompt: string;
      text?: string; // for TTS
      voice_id?: string;
      duration?: 5 | 10;
      aspect_ratio?: string;
    }
  | {
      provider: "suno";
      prompt: string;
      make_instrumental?: boolean;
      tags?: string;
      title?: string;
    }
  | {
      provider: "openrouter";
      model: string;
      prompt: string;
      systemPrompt?: string;
    };

export type ProviderCredentials = {
  hfToken?: string;
  falKey?: string;
  klingJwt?: string;
  minimaxKey?: string;
  sunoToken?: string;
  openrouterKey?: string;
};

export type QueuedRequest = {
  requestId: string;
  statusUrl: string;
  provider: ProviderName;
  /** Provider-specific extra state needed for polling (e.g., async/sync flag) */
  meta?: Record<string, unknown>;
};

export type GenerationResult = {
  status: "queued" | "completed" | "failed" | "processing" | string;
  requestId: string;
  images?: Array<{ url: string }>;
  video?: { url: string };
  audio?: Array<{ url: string; title?: string }>;
  text?: string;
  error?: string;
};

export async function submitToProvider(
  req: ProviderRequest,
  creds: ProviderCredentials,
  deviceId: string,
): Promise<QueuedRequest> {
  switch (req.provider) {
    case "pollinations":
      return {
        ...(await submitPollinationsImage(
          {
            prompt: req.prompt,
            width: req.width,
            height: req.height,
            model: req.model,
            seed: req.seed,
          },
          deviceId,
        )),
        provider: "pollinations",
      };

    case "huggingface":
      if (!creds.hfToken) throw new Error("HuggingFace provider requires an HF token");
      return {
        ...(await submitHfImage(
          {
            model: req.model,
            prompt: req.prompt,
            width: req.width,
            height: req.height,
            numInferenceSteps: req.numInferenceSteps,
            guidanceScale: req.guidanceScale,
            negativePrompt: req.negativePrompt,
            seed: req.seed,
          },
          creds.hfToken,
        )),
        provider: "huggingface",
      };

    case "hf-router": {
      if (!creds.hfToken) throw new Error("HF router requires an HF token");
      const result = await submitHfRouter(
        {
          modelId: req.modelId,
          task: req.task,
          inputs: req.inputs,
          parameters: req.parameters,
          imageUrl: req.imageUrl,
          provider: req.providerRouting,
        },
        creds.hfToken,
      );
      return {
        requestId: result.requestId,
        statusUrl: result.statusUrl,
        provider: "hf-router",
        meta: { isAsync: result.isAsync, hfProvider: result.provider },
      };
    }

    case "fal": {
      if (!creds.falKey) throw new Error("fal.ai requires an API key");
      if (req.kind === "image") {
        const result = await submitFalImage(
          {
            model: req.model as never,
            prompt: req.prompt,
            image_size: (req.image_size as never) ?? "landscape_16_9",
          },
          creds.falKey,
        );
        return {
          requestId: result.requestId,
          statusUrl: result.statusUrl,
          provider: "fal",
          meta: { kind: "image" },
        };
      }
      const result = await submitFalVideo(
        {
          model: req.model as never,
          prompt: req.prompt,
          duration: req.duration,
          aspect_ratio: req.aspect_ratio,
        },
        creds.falKey,
      );
      return {
        requestId: result.requestId,
        statusUrl: result.statusUrl,
        provider: "fal",
        meta: { kind: "video" },
      };
    }

    case "kling": {
      if (!creds.klingJwt) throw new Error("Kling requires a session JWT");
      const result = await submitKlingVideo(
        {
          prompt: req.prompt,
          duration: req.duration,
          aspect_ratio: req.aspect_ratio,
          style: req.style,
        },
        creds.klingJwt,
      );
      return {
        requestId: result.requestId,
        statusUrl: result.statusUrl,
        provider: "kling",
      };
    }

    case "minimax": {
      if (!creds.minimaxKey) throw new Error("MiniMax requires an API key");
      if (req.kind === "audio") {
        const result = await submitMinimaxAudio(
          { text: req.text ?? req.prompt, voice_id: req.voice_id },
          creds.minimaxKey,
        );
        return {
          requestId: result.requestId,
          statusUrl: result.audioUrl,
          provider: "minimax",
          meta: { kind: "audio" },
        };
      }
      const result = await submitMinimaxVideo(
        {
          prompt: req.prompt,
          duration: req.duration,
          aspect_ratio: req.aspect_ratio,
        },
        creds.minimaxKey,
      );
      return {
        requestId: result.requestId,
        statusUrl: result.statusUrl,
        provider: "minimax",
        meta: { kind: "video" },
      };
    }

    case "suno": {
      if (!creds.sunoToken) throw new Error("Suno requires a session token");
      const result = await submitSunoSong(
        { prompt: req.prompt, make_instrumental: req.make_instrumental, tags: req.tags, title: req.title },
        creds.sunoToken,
      );
      return {
        requestId: result.requestIds[0] ?? "",
        statusUrl: result.statusUrl,
        provider: "suno",
        meta: { allIds: result.requestIds },
      };
    }

    case "openrouter": {
      if (!creds.openrouterKey) throw new Error("OpenRouter requires an API key (free at openrouter.ai/keys)");
      const result = await submitOpenRouter({ model: req.model, prompt: req.prompt }, creds.openrouterKey);
      return {
        requestId: result.requestId,
        statusUrl: result.statusUrl,
        provider: "openrouter",
      };
    }

    default: {
      const exhaustive: never = req;
      throw new Error(`Provider ${(exhaustive as { provider: string }).provider} not implemented`);
    }
  }
}

export async function pollProvider(req: QueuedRequest, creds: ProviderCredentials): Promise<GenerationResult> {
  switch (req.provider) {
    case "pollinations": {
      const result = await pollPollinationsStatus(req.requestId, req.statusUrl);
      return { ...result, status: "completed" as const };
    }

    case "huggingface": {
      const result = await pollHfStatus(req.requestId, req.statusUrl);
      return { ...result, status: "completed" as const };
    }

    case "hf-router": {
      const isAsync = (req.meta?.isAsync as boolean) ?? false;
      const result = await pollHfRouterStatus(req.requestId, req.statusUrl, creds.hfToken ?? "", isAsync);
      return result;
    }

    case "fal": {
      const kind = req.meta?.kind as "image" | "video" | undefined;
      if (kind === "image") {
        return {
          status: "completed",
          requestId: req.requestId,
          images: [{ url: req.statusUrl }],
        };
      }
      const result = await pollFalVideoStatus(req.requestId, req.statusUrl, creds.falKey ?? "");
      return result;
    }

    case "kling": {
      const result = await pollKlingStatus(req.requestId, req.statusUrl, creds.klingJwt ?? "");
      return result;
    }

    case "minimax": {
      const kind = req.meta?.kind as "audio" | "video" | undefined;
      if (kind === "audio") {
        return {
          status: "completed",
          requestId: req.requestId,
          audio: [{ url: req.statusUrl }],
        };
      }
      const result = await pollMinimaxVideo(req.requestId, req.statusUrl, creds.minimaxKey ?? "");
      return result;
    }

    case "suno": {
      const allIds = (req.meta?.allIds as string[] | undefined) ?? [req.requestId];
      const result = await pollSunoStatus(allIds, req.statusUrl, creds.sunoToken ?? "");
      if (result.status === "completed" && result.audio) {
        return { ...result, audio: result.audio };
      }
      return result;
    }

    case "openrouter": {
      const result = await pollOpenRouter(req.requestId, req.statusUrl);
      return result;
    }

    default:
      return {
        status: "failed",
        requestId: req.requestId,
        error: `Provider ${(req as { provider: string }).provider} not implemented`,
      };
  }
}
