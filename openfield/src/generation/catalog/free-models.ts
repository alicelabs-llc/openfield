import type { ModelEntry } from "./types";

/* ============================================================================
 * POLLINATIONS — 100% free, no API key, no signup
 * ==========================================================================*/

const pollinationsFlux: ModelEntry = {
  id: "pollinations-flux",
  surface: "image",
  label: "Flux (Pollinations)",
  blurb: "FLUX.1-dev · free · no key",
  roles: {},
  settings: {
    aspectRatio: {
      type: "enum",
      values: ["1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3"],
      default: "1:1",
    },
    seed: { type: "range", min: 0, max: 999999, default: 0, step: 1 },
  },
  provider: { provider: "pollinations", model: "flux", needsKey: false },
  free: true,
};

const pollinationsTurbo: ModelEntry = {
  id: "pollinations-turbo",
  surface: "image",
  label: "Turbo (Pollinations)",
  blurb: "Fastest · free · no key",
  roles: {},
  settings: {
    aspectRatio: { type: "enum", values: ["1:1", "16:9", "9:16", "4:3", "3:4"], default: "1:1" },
    seed: { type: "range", min: 0, max: 999999, default: 0, step: 1 },
  },
  provider: { provider: "pollinations", model: "turbo", needsKey: false },
  free: true,
};

const pollinationsFluxRealism: ModelEntry = {
  id: "pollinations-flux-realism",
  surface: "image",
  label: "Flux Realism (Pollinations)",
  blurb: "Photorealistic · free",
  roles: {},
  settings: {
    aspectRatio: { type: "enum", values: ["1:1", "16:9", "9:16", "4:3", "3:4"], default: "1:1" },
    seed: { type: "range", min: 0, max: 999999, default: 0, step: 1 },
  },
  provider: { provider: "pollinations", model: "flux-realism", needsKey: false },
  free: true,
};

const pollinationsFluxAnime: ModelEntry = {
  id: "pollinations-flux-anime",
  surface: "image",
  label: "Flux Anime (Pollinations)",
  blurb: "Anime style · free",
  roles: {},
  settings: {
    aspectRatio: { type: "enum", values: ["1:1", "16:9", "9:16", "4:3", "3:4"], default: "1:1" },
    seed: { type: "range", min: 0, max: 999999, default: 0, step: 1 },
  },
  provider: { provider: "pollinations", model: "flux-anime", needsKey: false },
  free: true,
};

const pollinationsFlux3d: ModelEntry = {
  id: "pollinations-flux-3d",
  surface: "image",
  label: "Flux 3D (Pollinations)",
  blurb: "3D rendered look · free",
  roles: {},
  settings: {
    aspectRatio: { type: "enum", values: ["1:1", "16:9", "9:16", "4:3", "3:4"], default: "1:1" },
    seed: { type: "range", min: 0, max: 999999, default: 0, step: 1 },
  },
  provider: { provider: "pollinations", model: "flux-3d", needsKey: false },
  free: true,
};

/* ============================================================================
 * HUGGINGFACE INFERENCE API — free with HF token (rate limited)
 * ==========================================================================*/

const hfFluxSchnell: ModelEntry = {
  id: "hf-flux-schnell",
  surface: "image",
  label: "FLUX.1-schnell (HF)",
  blurb: "Apache 2.0 · 4-step distilled · free w/ HF token",
  roles: {},
  settings: {
    aspectRatio: { type: "enum", values: ["1:1", "16:9", "9:16", "4:3", "3:4"], default: "1:1" },
    numInferenceSteps: { type: "range", min: 1, max: 8, default: 4, step: 1 },
    seed: { type: "range", min: 0, max: 999999, default: 0, step: 1 },
  },
  provider: {
    provider: "huggingface",
    model: "black-forest-labs/FLUX.1-schnell",
    needsKey: true,
    defaultSteps: 4,
    defaultGuidance: 0,
  },
  free: true,
};

const hfFluxDev: ModelEntry = {
  id: "hf-flux-dev",
  surface: "image",
  label: "FLUX.1-dev (HF)",
  blurb: "Full FLUX · free w/ HF token",
  roles: {},
  settings: {
    aspectRatio: { type: "enum", values: ["1:1", "16:9", "9:16", "4:3", "3:4"], default: "1:1" },
    numInferenceSteps: { type: "range", min: 10, max: 50, default: 28, step: 1 },
    guidanceScale: { type: "range", min: 1, max: 10, default: 3.5, step: 0.1 },
    seed: { type: "range", min: 0, max: 999999, default: 0, step: 1 },
  },
  provider: {
    provider: "huggingface",
    model: "black-forest-labs/FLUX.1-dev",
    needsKey: true,
    defaultSteps: 28,
    defaultGuidance: 3.5,
  },
  free: true,
};

const hfSdxl: ModelEntry = {
  id: "hf-sdxl",
  surface: "image",
  label: "SDXL 1.0 (HF)",
  blurb: "Stability AI XL · free w/ HF token",
  roles: {},
  settings: {
    aspectRatio: { type: "enum", values: ["1:1", "16:9", "9:16", "4:3", "3:4"], default: "1:1" },
    numInferenceSteps: { type: "range", min: 10, max: 50, default: 25, step: 1 },
    guidanceScale: { type: "range", min: 1, max: 20, default: 7.5, step: 0.5 },
    seed: { type: "range", min: 0, max: 999999, default: 0, step: 1 },
  },
  provider: {
    provider: "huggingface",
    model: "stabilityai/stable-diffusion-xl-base-1.0",
    needsKey: true,
    defaultSteps: 25,
    defaultGuidance: 7.5,
  },
  free: true,
};

const hfSd15: ModelEntry = {
  id: "hf-sd-1-5",
  surface: "image",
  label: "SD 1.5 (HF)",
  blurb: "Fast · lightweight · free w/ HF token",
  roles: {},
  settings: {
    aspectRatio: { type: "enum", values: ["1:1", "16:9", "9:16", "4:3", "3:4"], default: "1:1" },
    numInferenceSteps: { type: "range", min: 10, max: 50, default: 20, step: 1 },
    guidanceScale: { type: "range", min: 1, max: 20, default: 7.5, step: 0.5 },
    seed: { type: "range", min: 0, max: 999999, default: 0, step: 1 },
  },
  provider: {
    provider: "huggingface",
    model: "runwayml/stable-diffusion-v1-5",
    needsKey: true,
    defaultSteps: 20,
    defaultGuidance: 7.5,
  },
  free: true,
};

/* ============================================================================
 * HUGGINGFACE ROUTER (Inference Providers) — paid but with $2/mo free credit
 * Routes through fal-ai / replicate / wavespeed / nscale
 * ==========================================================================*/

const routerFluxSchnellFal: ModelEntry = {
  id: "router-flux-schnell-fal",
  surface: "image",
  label: "FLUX.1-schnell (HF Router)",
  blurb: "Via fal.ai · $2/mo free credit",
  roles: {},
  settings: {
    aspectRatio: { type: "enum", values: ["1:1", "16:9", "9:16"], default: "1:1" },
  },
  provider: {
    provider: "hf-router",
    modelId: "black-forest-labs/FLUX.1-schnell",
    task: "text-to-image",
    needsKey: true,
  },
  free: true,
};

const routerFluxDev: ModelEntry = {
  id: "router-flux-dev",
  surface: "image",
  label: "FLUX.1-dev (HF Router)",
  blurb: "Via fal.ai · $2/mo free credit",
  roles: {},
  settings: {
    aspectRatio: { type: "enum", values: ["1:1", "16:9", "9:16"], default: "1:1" },
  },
  provider: {
    provider: "hf-router",
    modelId: "black-forest-labs/FLUX.1-dev",
    task: "text-to-image",
    needsKey: true,
  },
  free: true,
};

const routerFluxKontext: ModelEntry = {
  id: "router-flux-kontext",
  surface: "image",
  label: "FLUX.1-Kontext (HF Router)",
  blurb: "Image edit · Via fal.ai",
  roles: { reference: 1 },
  settings: {
    aspectRatio: { type: "enum", values: ["1:1", "16:9", "9:16"], default: "1:1" },
  },
  provider: {
    provider: "hf-router",
    modelId: "black-forest-labs/FLUX.1-Kontext-dev",
    task: "image-to-image",
    needsKey: true,
  },
  free: true,
};

const routerSdxl: ModelEntry = {
  id: "router-sdxl",
  surface: "image",
  label: "SDXL 1.0 (HF Router)",
  blurb: "Via fal.ai · fast-sdxl",
  roles: {},
  settings: {
    aspectRatio: { type: "enum", values: ["1:1", "16:9", "9:16"], default: "1:1" },
  },
  provider: {
    provider: "hf-router",
    modelId: "stabilityai/stable-diffusion-xl-base-1.0",
    task: "text-to-image",
    needsKey: true,
  },
  free: true,
};

const routerLlama8b: ModelEntry = {
  id: "router-llama-8b",
  surface: "text",
  label: "Llama 3.1 8B (HF Router)",
  blurb: "LLM · via novita · cheap",
  roles: {},
  settings: {},
  provider: {
    provider: "hf-router",
    modelId: "meta-llama/Llama-3.1-8B-Instruct",
    task: "chat-completions",
    needsKey: true,
  },
  free: true,
};

const routerQwen4b: ModelEntry = {
  id: "router-qwen-4b",
  surface: "text",
  label: "Qwen3-4B Instruct (HF Router)",
  blurb: "Cheapest LLM · nscale · $0.01/1M tok",
  roles: {},
  settings: {},
  provider: {
    provider: "hf-router",
    modelId: "Qwen/Qwen3-4B-Instruct-2507",
    task: "chat-completions",
    needsKey: true,
  },
  free: true,
};

/* ============================================================================
 * FAL.AI — paid but with $1 credit on signup
 * ==========================================================================*/

const falFluxSchnell: ModelEntry = {
  id: "fal-flux-schnell",
  surface: "image",
  label: "FLUX.1-schnell (fal.ai)",
  blurb: "$1 free credit · fast",
  roles: {},
  settings: {
    image_size: {
      type: "enum",
      values: ["square_hd", "square", "portrait_4_3", "portrait_16_9", "landscape_4_3", "landscape_16_9"],
      default: "landscape_16_9",
    },
  },
  provider: {
    provider: "fal",
    kind: "image",
    model: "fal-ai/flux/schnell",
    needsKey: true,
  },
  free: true,
};

const falFluxDev: ModelEntry = {
  id: "fal-flux-dev",
  surface: "image",
  label: "FLUX.1-dev (fal.ai)",
  blurb: "$1 free credit · full quality",
  roles: {},
  settings: {
    image_size: {
      type: "enum",
      values: ["square_hd", "square", "portrait_4_3", "portrait_16_9", "landscape_4_3", "landscape_16_9"],
      default: "landscape_16_9",
    },
  },
  provider: {
    provider: "fal",
    kind: "image",
    model: "fal-ai/flux/dev",
    needsKey: true,
  },
  free: true,
};

const falKling16: ModelEntry = {
  id: "fal-kling-1.6",
  surface: "video",
  label: "Kling 1.6 Standard (fal.ai)",
  blurb: "Video · $1 free credit",
  roles: { start: 1, end: 1 },
  settings: {
    duration: { type: "range", min: 5, max: 10, default: 5, step: 5 },
    aspect_ratio: { type: "enum", values: ["16:9", "9:16", "1:1"], default: "16:9" },
  },
  provider: {
    provider: "fal",
    kind: "video",
    model: "fal-ai/kling-video/v1.6/standard/text-to-video",
    needsKey: true,
  },
  free: true,
};

const falMinimaxHailuo: ModelEntry = {
  id: "fal-minimax-hailuo",
  surface: "video",
  label: "MiniMax Hailuo 02 (fal.ai)",
  blurb: "Chinese video model · $1 free",
  roles: {},
  settings: {
    duration: { type: "range", min: 5, max: 10, default: 5, step: 5 },
    aspect_ratio: { type: "enum", values: ["16:9", "9:16", "1:1"], default: "16:9" },
  },
  provider: {
    provider: "fal",
    kind: "video",
    model: "fal-ai/minimax/hailuo-02/standard/text-to-video",
    needsKey: true,
  },
  free: true,
};

const falVeo3Fast: ModelEntry = {
  id: "fal-veo3-fast",
  surface: "video",
  label: "Veo 3 Fast (fal.ai)",
  blurb: "Google Veo 3 · $1 free credit",
  roles: {},
  settings: {
    duration: { type: "range", min: 4, max: 8, default: 4, step: 4 },
    aspect_ratio: { type: "enum", values: ["16:9", "9:16"], default: "16:9" },
  },
  provider: {
    provider: "fal",
    kind: "video",
    model: "fal-ai/veo3/fast",
    needsKey: true,
  },
  free: true,
};

const falPikaTurbo: ModelEntry = {
  id: "fal-pika-turbo",
  surface: "video",
  label: "Pika v2.2 Turbo (fal.ai)",
  blurb: "Pika Labs · $1 free credit",
  roles: {},
  settings: {
    duration: { type: "range", min: 5, max: 10, default: 5, step: 5 },
    aspect_ratio: { type: "enum", values: ["16:9", "9:16", "1:1"], default: "16:9" },
  },
  provider: {
    provider: "fal",
    kind: "video",
    model: "fal-ai/pika/v2.2/turbo/text-to-video",
    needsKey: true,
  },
  free: true,
};

/* ============================================================================
 * KLING — direct web API (66 free credits/day with session JWT)
 * ==========================================================================*/

const klingFree: ModelEntry = {
  id: "kling-free",
  surface: "video",
  label: "Kling 1.6 (Klingai Web)",
  blurb: "66 credits/day · free web API",
  roles: {},
  settings: {
    duration: { type: "range", min: 5, max: 10, default: 5, step: 5 },
    aspect_ratio: { type: "enum", values: ["16:9", "9:16", "1:1"], default: "16:9" },
    style: { type: "enum", values: ["standard", "professional"], default: "standard" },
  },
  provider: { provider: "kling", needsKey: true },
  free: true,
};

/* ============================================================================
 * MINIMAX — official API (30k initial credits, 5k/day)
 * ==========================================================================*/

const minimaxAudio: ModelEntry = {
  id: "minimax-audio-tts",
  surface: "audio",
  label: "MiniMax Speech-02 (TTS)",
  blurb: "Chinese TTS · 30k initial credits",
  roles: {},
  settings: {
    voice_id: {
      type: "enum",
      values: ["male-qn-qingse", "female-shaonv", "male-qn-jingying", "female-yujie", "male-qn-badao"],
      default: "male-qn-qingse",
    },
    speed: { type: "range", min: 0.5, max: 2.0, default: 1.0, step: 0.1 },
    pitch: { type: "range", min: -12, max: 12, default: 0, step: 1 },
  },
  provider: { provider: "minimax", kind: "audio", needsKey: true },
  free: true,
};

const minimaxVideo: ModelEntry = {
  id: "minimax-video",
  surface: "video",
  label: "MiniMax Hailuo (Direct)",
  blurb: "Video · 30k initial credits",
  roles: {},
  settings: {
    duration: { type: "range", min: 5, max: 10, default: 5, step: 5 },
    aspect_ratio: { type: "enum", values: ["16:9", "9:16", "1:1", "4:3"], default: "16:9" },
  },
  provider: { provider: "minimax", kind: "video", needsKey: true },
  free: true,
};

/* ============================================================================
 * SUNO — unofficial web API (50 credits/day)
 * ==========================================================================*/

const sunoFree: ModelEntry = {
  id: "suno-free",
  surface: "audio",
  label: "Suno V4 (Music)",
  blurb: "50 credits/day · web session",
  roles: {},
  settings: {
    make_instrumental: { type: "boolean", default: false },
    tags: {
      type: "enum",
      values: ["", "pop", "rock", "hip hop", "electronic", "classical", "jazz", "ambient", "lo-fi", "metal"],
      default: "",
    },
  },
  provider: { provider: "suno", needsKey: true },
  free: true,
};

export const FREE_MODELS: ModelEntry[] = [
  // Pollinations — no key needed
  pollinationsFlux,
  pollinationsTurbo,
  pollinationsFluxRealism,
  pollinationsFluxAnime,
  pollinationsFlux3d,
  // HuggingFace direct (free with token, rate-limited)
  hfFluxSchnell,
  hfFluxDev,
  hfSdxl,
  hfSd15,
  // HuggingFace router ($2/mo free)
  routerFluxSchnellFal,
  routerFluxDev,
  routerFluxKontext,
  routerSdxl,
  routerLlama8b,
  routerQwen4b,
  // fal.ai ($1 free signup credit)
  falFluxSchnell,
  falFluxDev,
  falKling16,
  falMinimaxHailuo,
  falVeo3Fast,
  falPikaTurbo,
  // Kling (66 credits/day free)
  klingFree,
  // MiniMax (30k initial + 5k/day free)
  minimaxAudio,
  minimaxVideo,
  // Suno (50 credits/day free)
  sunoFree,
];
