/**
 * HuggingFace router provider — the new unified API.
 *
 * Auth: Bearer HF token (free signup at huggingface.co/settings/tokens)
 * Free tier: $2 USD monthly credit on PRO ($9/mo), $0 free for free accounts
 *            but they let you call some models with very tight rate limits.
 *
 * URL pattern (verified by tracing the actual huggingface_hub SDK calls):
 *   POST https://router.huggingface.co/{provider}/v1/models/{provider_id}/predictions
 *
 * Provider IDs are NOT the same as model IDs — they're mapped via:
 *   GET https://huggingface.co/api/models/{model_id}?expand[]=inferenceProviderMapping
 *
 * Providers for image: fal-ai, replicate, wavespeed, nscale
 * Providers for video: fal-ai, replicate
 * Providers for chat (LLM): cerebras, groq, nscale, novita, deepinfra, baseten
 */

const HF_API_BASE = "https://router.huggingface.co";
const HF_HUB_API = "https://huggingface.co/api";

export type HfRouterProvider = "fal-ai" | "replicate" | "wavespeed" | "nscale" | "cerebras" | "groq" | "novita" | "deepinfra";

export type HfRouterRequest = {
  /** Full HF model id, e.g. "black-forest-labs/FLUX.1-schnell" */
  modelId: string;
  /** Provider to route to. If undefined, picks the first available live one. */
  provider?: HfRouterProvider;
  /** Task type determines the endpoint shape */
  task: "text-to-image" | "image-to-image" | "text-to-video" | "chat-completions" | "text-to-speech";
  /** Prompt or inputs depending on task */
  inputs: string;
  /** Per-task parameters */
  parameters?: Record<string, unknown>;
  /** Optional image URL for image-to-image / image-to-video */
  imageUrl?: string;
};

type ProviderMapping = {
  status: string;
  providerId: string;
  task: string;
  isModelAuthor?: boolean;
};

async function resolveProviderId(
  modelId: string,
  preferredProvider: HfRouterProvider | undefined,
): Promise<{ provider: HfRouterProvider; providerId: string; task: string }> {
  // Query HF Hub for the provider mapping
  const response = await fetch(
    `${HF_HUB_API}/models/${modelId}?expand[]=inferenceProviderMapping`,
  );
  if (!response.ok) {
    throw new Error(`HF Hub lookup failed for ${modelId}: ${response.status}`);
  }
  const data = (await response.json()) as {
    inferenceProviderMapping?: Record<HfRouterProvider, ProviderMapping>;
  };

  const mappings = data.inferenceProviderMapping;
  if (!mappings) {
    throw new Error(`Model ${modelId} has no inference provider mapping`);
  }

  const liveProviders = Object.entries(mappings).filter(
    ([_, m]) => m.status === "live",
  );

  if (liveProviders.length === 0) {
    throw new Error(`No live providers for ${modelId}`);
  }

  // Prefer the user-specified one, else pick the first
  const chosen =
    preferredProvider && mappings[preferredProvider]?.status === "live"
      ? ([preferredProvider, mappings[preferredProvider]] as const)
      : (liveProviders[0] as [HfRouterProvider, ProviderMapping]);

  return {
    provider: chosen[0],
    providerId: chosen[1].providerId,
    task: chosen[1].task,
  };
}

/**
 * Submit a generation request to the HF router.
 * Returns a queue-style request id (provider may be sync or async).
 */
export async function submitHfRouter(
  req: HfRouterRequest,
  hfToken: string,
): Promise<{
  requestId: string;
  statusUrl: string;
  provider: HfRouterProvider;
  isAsync: boolean;
}> {
  const { provider, providerId, task } = await resolveProviderId(req.modelId, req.provider);

  // The router URL is /{provider}/v1/models/{provider_id}/predictions
  // For chat-completions, it's /{provider}/v1/chat/completions (OpenAI shape)
  let endpoint: string;
  if (task === "chat-completions") {
    endpoint = `${HF_API_BASE}/${provider}/v1/chat/completions`;
  } else {
    endpoint = `${HF_API_BASE}/${provider}/v1/models/${providerId}/predictions`;
  }

  // Build body per task
  let body: Record<string, unknown>;
  switch (task) {
    case "text-to-image":
      body = {
        inputs: req.inputs,
        parameters: req.parameters ?? {},
      };
      break;
    case "image-to-image":
      body = {
        inputs: req.imageUrl,
        prompt: req.inputs,
        parameters: req.parameters ?? {},
      };
      break;
    case "text-to-video":
      body = {
        prompt: req.inputs,
        parameters: req.parameters ?? {},
      };
      break;
    case "chat-completions":
      body = {
        model: providerId,
        messages: [{ role: "user", content: req.inputs }],
        ...req.parameters,
      };
      break;
    default:
      throw new Error(`Task ${task} not implemented`);
  }

  const response = await fetch(endpoint, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${hfToken}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`HF router ${provider} ${response.status}: ${text.slice(0, 300)}`);
  }

  // Detect response shape (sync returns the result, async returns a job id)
  const contentType = response.headers.get("content-type") ?? "";
  if (contentType.startsWith("image/")) {
    // Synchronous image response — encode as data URL
    const buffer = Buffer.from(await response.arrayBuffer());
    const dataUrl = `data:${contentType};base64,${buffer.toString("base64")}`;
    return {
      requestId: `hf-sync-img-${Date.now()}`,
      statusUrl: dataUrl,
      provider,
      isAsync: false,
    };
  }

  const data = (await response.json()) as Record<string, unknown>;

  // Async prediction: data has id/get_prediction_url
  if (typeof data.id === "string" || typeof data.request_id === "string") {
    const id = (data.id as string) ?? (data.request_id as string);
    const statusUrl = (data.get_prediction_url as string) ?? `${endpoint}/${id}`;
    return {
      requestId: id,
      statusUrl,
      provider,
      isAsync: true,
    };
  }

  // Chat completion sync response
  if (data.choices) {
    const choices = data.choices as Array<{ message?: { content?: string } }>;
    const text = choices[0]?.message?.content ?? "";
    return {
      requestId: `hf-chat-${Date.now()}`,
      statusUrl: text,
      provider,
      isAsync: false,
    };
  }

  // Sync response with image URL (fal-ai shape)
  if (Array.isArray(data.images) && data.images[0]) {
    return {
      requestId: `hf-img-${Date.now()}`,
      statusUrl: (data.images[0] as { url: string }).url,
      provider,
      isAsync: false,
    };
  }

  // Fallback: stringify and store
  return {
    requestId: `hf-${Date.now()}`,
    statusUrl: JSON.stringify(data).slice(0, 5000),
    provider,
    isAsync: false,
  };
}

/**
 * For sync responses, "polling" is just returning the result.
 * For async (Replicate-style), poll the status URL.
 */
export async function pollHfRouterStatus(
  requestId: string,
  statusUrl: string,
  hfToken: string,
  isAsync: boolean,
): Promise<{
  status: string;
  requestId: string;
  images?: Array<{ url: string }>;
  video?: { url: string };
  text?: string;
  error?: string;
}> {
  if (!isAsync) {
    // statusUrl is already the result (data URL or text)
    if (statusUrl.startsWith("data:image/")) {
      return { status: "completed", requestId, images: [{ url: statusUrl }] };
    }
    if (statusUrl.startsWith("http")) {
      // It's an image URL
      return { status: "completed", requestId, images: [{ url: statusUrl }] };
    }
    return { status: "completed", requestId, text: statusUrl };
  }

  const response = await fetch(statusUrl, {
    headers: { Authorization: `Bearer ${hfToken}` },
  });

  if (!response.ok) {
    return { status: "failed", requestId, error: `HF router poll ${response.status}` };
  }

  const data = (await response.json()) as {
    status?: string;
    output?: string | string[];
    error?: string;
    urls?: { output?: string };
  };

  const status = (data.status ?? "processing").toLowerCase();
  if (status === "succeeded" || status === "completed") {
    const output = data.output ?? data.urls?.output;
    if (Array.isArray(output) && output[0]) {
      const url = output[0] as string;
      if (url.startsWith("http")) {
        return { status: "completed", requestId, images: [{ url }] };
      }
      return { status: "completed", requestId, video: { url } };
    }
    if (typeof output === "string") {
      return { status: "completed", requestId, video: { url: output } };
    }
    return { status: "failed", requestId, error: "HF router returned no output" };
  }
  if (status === "failed" || status === "error") {
    return { status: "failed", requestId, error: data.error ?? "HF generation failed" };
  }
  return { status, requestId };
}
