/**
 * fal.ai provider — supports image and video models.
 *
 * Auth: Bearer token (FAL_KEY env var or key modal input)
 * Free tier: $1 credit on signup (https://fal.ai/dashboard/keys)
 *
 * Image endpoint:
 *   POST https://fal.run/fal-ai/flux/schnell
 *   POST https://fal.run/fal-ai/flux/dev
 *   POST https://fal.run/fal-ai/fast-sdxl
 *
 * Video endpoint (async):
 *   POST https://fal.run/fal-ai/kling-video/v1.6/standard/text-to-video
 *   GET  https://queue.fal.run/fal-ai/kling-video/requests/{id}/status
 */

const FAL_RUN_BASE = "https://fal.run";
const FAL_QUEUE_BASE = "https://queue.fal.run";

export type FalImageModel =
  | "fal-ai/flux/schnell"
  | "fal-ai/flux/dev"
  | "fal-ai/fast-sdxl"
  | "fal-ai/recraft-v3"
  | "fal-ai/ideogram/v2";

export type FalVideoModel =
  | "fal-ai/kling-video/v1.6/standard/text-to-video"
  | "fal-ai/kling-video/v1.6/pro/text-to-video"
  | "fal-ai/minimax/hailuo-02/standard/text-to-video"
  | "fal-ai/veo3/fast"
  | "fal-ai/pika/v2.2/turbo/text-to-video";

export type FalImageRequest = {
  model: FalImageModel;
  prompt: string;
  image_size?: "square_hd" | "square" | "portrait_4_3" | "portrait_16_9" | "landscape_4_3" | "landscape_16_9";
  num_inference_steps?: number;
  guidance_scale?: number;
  num_images?: number;
  enable_safety_checker?: boolean;
  seed?: number;
};

export type FalVideoRequest = {
  model: FalVideoModel;
  prompt: string;
  duration?: string; // "5" or "10"
  aspect_ratio?: string; // "16:9" | "9:16" | "1:1"
  negative_prompt?: string;
};

export async function submitFalImage(req: FalImageRequest, apiKey: string) {
  const response = await fetch(`${FAL_RUN_BASE}/${req.model}`, {
    method: "POST",
    headers: {
      Authorization: `Key ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      prompt: req.prompt,
      image_size: req.image_size ?? "landscape_16_9",
      num_inference_steps: req.num_inference_steps ?? 4,
      num_images: req.num_images ?? 1,
      enable_safety_checker: req.enable_safety_checker ?? false,
      ...(typeof req.seed === "number" ? { seed: req.seed } : {}),
    }),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`fal.ai ${response.status}: ${text.slice(0, 300)}`);
  }

  const data = (await response.json()) as { images?: Array<{ url: string }>; image?: { url: string } };
  const urls =
    data.images?.map((i) => i.url) ?? (data.image ? [data.image.url] : []);

  if (urls.length === 0) throw new Error("fal.ai returned no images");

  return {
    requestId: `fal-img-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    statusUrl: urls[0]!,
    images: urls,
  };
}

export async function submitFalVideo(req: FalVideoRequest, apiKey: string) {
  // Submit to queue
  const response = await fetch(`${FAL_QUEUE_BASE}/${req.model}`, {
    method: "POST",
    headers: {
      Authorization: `Key ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      prompt: req.prompt,
      duration: req.duration ?? "5",
      aspect_ratio: req.aspect_ratio ?? "16:9",
      ...(req.negative_prompt ? { negative_prompt: req.negative_prompt } : {}),
    }),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`fal.ai video submit ${response.status}: ${text.slice(0, 300)}`);
  }

  const data = (await response.json()) as {
    request_id: string;
    status_url: string;
  };

  return {
    requestId: data.request_id,
    statusUrl: data.status_url,
  };
}

export async function pollFalVideoStatus(
  requestId: string,
  statusUrl: string,
  apiKey: string,
): Promise<{
  status: string;
  requestId: string;
  video?: { url: string };
  error?: string;
}> {
  const response = await fetch(statusUrl, {
    headers: { Authorization: `Key ${apiKey}` },
  });

  if (!response.ok) {
    return {
      status: "failed",
      requestId,
      error: `fal.ai poll ${response.status}`,
    };
  }

  const data = (await response.json()) as {
    status: string;
    video?: { url: string };
    logs?: Array<{ message: string }>;
    error?: string;
  };

  if (data.status === "COMPLETED" && data.video?.url) {
    return { status: "completed", requestId, video: data.video };
  }
  if (data.status === "FAILED") {
    return { status: "failed", requestId, error: data.error ?? "Generation failed" };
  }
  return { status: data.status.toLowerCase(), requestId };
}
