/**
 * HuggingFace provider — free Inference API with rate limits.
 *
 * Requires HF_API_KEY env var (free signup at huggingface.co/settings/tokens).
 * Free tier: ~30 requests/hour per model on most models.
 *
 * Image models: black-forest-labs/FLUX.1-schnell, stabilityai/stable-diffusion-xl-base-1.0, etc.
 *
 * API shape (v0):
 *   POST https://api-inference.huggingface.co/models/{model_id}
 *   Headers: Authorization: Bearer {token}
 *   Body: { inputs: "prompt", parameters: { width, height, num_inference_steps } }
 *   Response: image bytes (image/png)
 */

const HF_API_BASE = "https://api-inference.huggingface.co/models";

export type HfImageRequest = {
  model: string; // e.g. "black-forest-labs/FLUX.1-schnell"
  prompt: string;
  width?: number;
  height?: number;
  numInferenceSteps?: number;
  guidanceScale?: number;
  negativePrompt?: string;
  seed?: number;
};

export async function submitHfImage(
  req: HfImageRequest,
  apiKey: string,
): Promise<{ requestId: string; statusUrl: string }> {
  // HF Inference API is synchronous — call it, store the bytes, return a URL.
  // We use a small in-memory cache for the polling loop to pick up.
  const response = await fetch(`${HF_API_BASE}/${req.model}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
      "x-wait-for-model": "true",
    },
    body: JSON.stringify({
      inputs: req.prompt,
      parameters: {
        width: req.width ?? 1024,
        height: req.height ?? 1024,
        num_inference_steps: req.numInferenceSteps ?? 4,
        guidance_scale: req.guidanceScale ?? 7.5,
        ...(req.negativePrompt ? { negative_prompt: req.negativePrompt } : {}),
        ...(typeof req.seed === "number" ? { seed: req.seed } : {}),
      },
      options: {
        wait_for_model: true,
      },
    }),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`HF API ${response.status}: ${text.slice(0, 200)}`);
  }

  // The response body is the image bytes.
  const buffer = Buffer.from(await response.arrayBuffer());
  const dataUrl = `data:image/png;base64,${buffer.toString("base64")}`;

  return {
    requestId: `hf-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    statusUrl: dataUrl,
  };
}

export async function pollHfStatus(
  requestId: string,
  statusUrl: string,
): Promise<{
  status: "completed";
  requestId: string;
  images: Array<{ url: string }>;
}> {
  // For v0 we treat the synchronous fetch as immediate completion.
  return {
    status: "completed",
    requestId,
    images: [{ url: statusUrl }],
  };
}
