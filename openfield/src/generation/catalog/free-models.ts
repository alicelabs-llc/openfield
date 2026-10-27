import type { ModelEntry } from "./types";

/* ============================================================================
 * POLLINATIONS — 100% FREE, no signup, no API key, no auth.
 * Anonymous tier works for IMAGE only (5 models). Text/Audio/Video requires
 * a free pollen key (https://enter.pollinations.ai).
 * ==========================================================================*/

const pollinationsFlux: ModelEntry = {
  id: "pollinations-flux",
  surface: "image",
  label: "Flux (Pollinations)",
  blurb: "FLUX.1-dev · 100% free · no key",
  roles: {},
  settings: {
    aspectRatio: { type: "enum", values: ["1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3"], default: "1:1" },
    seed: { type: "range", min: 0, max: 999999, default: 0, step: 1 },
  },
  provider: { provider: "pollinations", model: "flux", needsKey: false },
  free: true,
};

const pollinationsTurbo: ModelEntry = {
  id: "pollinations-turbo",
  surface: "image",
  label: "Turbo (Pollinations)",
  blurb: "Fastest image model · 100% free",
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
  blurb: "Photorealistic · 100% free",
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
  blurb: "Anime / illustration · 100% free",
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
  blurb: "3D-rendered look · 100% free",
  roles: {},
  settings: {
    aspectRatio: { type: "enum", values: ["1:1", "16:9", "9:16", "4:3", "3:4"], default: "1:1" },
    seed: { type: "range", min: 0, max: 999999, default: 0, step: 1 },
  },
  provider: { provider: "pollinations", model: "flux-3d", needsKey: false },
  free: true,
};

/* ============================================================================
 * HUGGINGFACE — free with HF token (signup at huggingface.co/settings/tokens)
 * Free Inference API: ~30 req/hour on classic, $0.10/mo credit on Router.
 * ==========================================================================*/

const hfFluxSchnell: ModelEntry = {
  id: "hf-flux-schnell",
  surface: "image",
  label: "FLUX.1-schnell (HF)",
  blurb: "Apache 2.0 · 4-step · free w/ HF token",
  roles: {},
  settings: {
    aspectRatio: { type: "enum", values: ["1:1", "16:9", "9:16", "4:3", "3:4"], default: "1:1" },
    numInferenceSteps: { type: "range", min: 1, max: 8, default: 4, step: 1 },
    seed: { type: "range", min: 0, max: 999999, default: 0, step: 1 },
  },
  provider: { provider: "huggingface", model: "black-forest-labs/FLUX.1-schnell", needsKey: true, defaultSteps: 4, defaultGuidance: 0 },
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
  provider: { provider: "huggingface", model: "black-forest-labs/FLUX.1-dev", needsKey: true, defaultSteps: 28, defaultGuidance: 3.5 },
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
  provider: { provider: "huggingface", model: "stabilityai/stable-diffusion-xl-base-1.0", needsKey: true, defaultSteps: 25, defaultGuidance: 7.5 },
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
  provider: { provider: "huggingface", model: "runwayml/stable-diffusion-v1-5", needsKey: true, defaultSteps: 20, defaultGuidance: 7.5 },
  free: true,
};

/* ============================================================================
 * FAL.AI — 5 free FLUX 3 Max videos per day (rolling 24h window).
 * Signup: https://fal.ai/dashboard/keys
 * ==========================================================================*/

const falFluxSchnell: ModelEntry = {
  id: "fal-flux-schnell",
  surface: "image",
  label: "FLUX.1-schnell (fal.ai)",
  blurb: "$1 free credit · fastest FLUX",
  roles: {},
  settings: {
    image_size: {
      type: "enum",
      values: ["square_hd", "square", "portrait_4_3", "portrait_16_9", "landscape_4_3", "landscape_16_9"],
      default: "landscape_16_9",
    },
  },
  provider: { provider: "fal", kind: "image", model: "fal-ai/flux/schnell", needsKey: true },
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
  provider: { provider: "fal", kind: "image", model: "fal-ai/flux/dev", needsKey: true },
  free: true,
};

const falFlux3MaxVideo: ModelEntry = {
  id: "fal-flux-3-max-video",
  surface: "video",
  label: "FLUX 3 Max Video (fal.ai)",
  blurb: "5 free videos/day · 720p",
  roles: {},
  settings: {
    duration: { type: "range", min: 5, max: 10, default: 5, step: 5 },
    aspect_ratio: { type: "enum", values: ["16:9", "9:16", "1:1"], default: "16:9" },
  },
  provider: { provider: "fal", kind: "video", model: "fal-ai/flux-3-max/video", needsKey: true },
  free: true,
};

const falKling16: ModelEntry = {
  id: "fal-kling-1.6",
  surface: "video",
  label: "Kling 1.6 Standard (fal.ai)",
  blurb: "$1 free credit · Chinese video model",
  roles: { start: 1, end: 1 },
  settings: {
    duration: { type: "range", min: 5, max: 10, default: 5, step: 5 },
    aspect_ratio: { type: "enum", values: ["16:9", "9:16", "1:1"], default: "16:9" },
  },
  provider: { provider: "fal", kind: "video", model: "fal-ai/kling-video/v1.6/standard/text-to-video", needsKey: true },
  free: true,
};

const falMinimaxHailuo: ModelEntry = {
  id: "fal-minimax-hailuo",
  surface: "video",
  label: "MiniMax Hailuo 02 (fal.ai)",
  blurb: "$1 free credit · Chinese video model",
  roles: {},
  settings: {
    duration: { type: "range", min: 5, max: 10, default: 5, step: 5 },
    aspect_ratio: { type: "enum", values: ["16:9", "9:16", "1:1"], default: "16:9" },
  },
  provider: { provider: "fal", kind: "video", model: "fal-ai/minimax/hailuo-02/standard/text-to-video", needsKey: true },
  free: true,
};

const falVeo3Fast: ModelEntry = {
  id: "fal-veo3-fast",
  surface: "video",
  label: "Veo 3 Fast (fal.ai)",
  blurb: "$1 free credit · Google Veo 3",
  roles: {},
  settings: {
    duration: { type: "range", min: 4, max: 8, default: 4, step: 4 },
    aspect_ratio: { type: "enum", values: ["16:9", "9:16"], default: "16:9" },
  },
  provider: { provider: "fal", kind: "video", model: "fal-ai/veo3/fast", needsKey: true },
  free: true,
};

const falPikaTurbo: ModelEntry = {
  id: "fal-pika-turbo",
  surface: "video",
  label: "Pika v2.2 Turbo (fal.ai)",
  blurb: "$1 free credit · Pika Labs",
  roles: {},
  settings: {
    duration: { type: "range", min: 5, max: 10, default: 5, step: 5 },
    aspect_ratio: { type: "enum", values: ["16:9", "9:16", "1:1"], default: "16:9" },
  },
  provider: { provider: "fal", kind: "video", model: "fal-ai/pika/v2.2/turbo/text-to-video", needsKey: true },
  free: true,
};

/* ============================================================================
 * HUGGINGFACE ROUTER — $0.10 free monthly credit (no PRO needed)
 * Signup: huggingface.co/settings/tokens
 * ==========================================================================*/

const routerFluxSchnell: ModelEntry = {
  id: "router-flux-schnell",
  surface: "image",
  label: "FLUX.1-schnell (HF Router)",
  blurb: "$0.10/mo credit · via fal.ai",
  roles: {},
  settings: { aspectRatio: { type: "enum", values: ["1:1", "16:9", "9:16"], default: "1:1" } },
  provider: { provider: "hf-router", modelId: "black-forest-labs/FLUX.1-schnell", task: "text-to-image", needsKey: true },
  free: true,
};

const routerFluxDev: ModelEntry = {
  id: "router-flux-dev",
  surface: "image",
  label: "FLUX.1-dev (HF Router)",
  blurb: "$0.10/mo credit · via fal.ai",
  roles: {},
  settings: { aspectRatio: { type: "enum", values: ["1:1", "16:9", "9:16"], default: "1:1" } },
  provider: { provider: "hf-router", modelId: "black-forest-labs/FLUX.1-dev", task: "text-to-image", needsKey: true },
  free: true,
};

const routerFluxKontext: ModelEntry = {
  id: "router-flux-kontext",
  surface: "image",
  label: "FLUX.1-Kontext (HF Router)",
  blurb: "Image edit · via fal.ai",
  roles: { reference: 1 },
  settings: { aspectRatio: { type: "enum", values: ["1:1", "16:9", "9:16"], default: "1:1" } },
  provider: { provider: "hf-router", modelId: "black-forest-labs/FLUX.1-Kontext-dev", task: "image-to-image", needsKey: true },
  free: true,
};

const routerLlama8b: ModelEntry = {
  id: "router-llama-8b",
  surface: "text",
  label: "Llama 3.1 8B (HF Router)",
  blurb: "LLM · $0.10/mo credit",
  roles: {},
  settings: {},
  provider: { provider: "hf-router", modelId: "meta-llama/Llama-3.1-8B-Instruct", task: "chat-completions", needsKey: true },
  free: true,
};

const routerQwen4b: ModelEntry = {
  id: "router-qwen-4b",
  surface: "text",
  label: "Qwen3-4B Instruct (HF Router)",
  blurb: "🇨🇳 Chinese LLM · cheapest on market",
  roles: {},
  settings: {},
  provider: { provider: "hf-router", modelId: "Qwen/Qwen3-4B-Instruct-2507", task: "chat-completions", needsKey: true },
  free: true,
};

/* ============================================================================
 * OPENROUTER — Free LLMs (~50 req/day without payment, ~1000/day with $10 top-up)
 * Signup: openrouter.ai/keys
 * ==========================================================================*/

const openrouterLlama4: ModelEntry = {
  id: "openrouter-llama-4-maverick",
  surface: "text",
  label: "Llama 4 Maverick (OpenRouter)",
  blurb: "Free LLM · 400B MoE · multimodal",
  roles: {},
  settings: {},
  provider: { provider: "openrouter", modelId: "meta-llama/llama-4-maverick:free", needsKey: true },
  free: true,
};

const openrouterGemma4: ModelEntry = {
  id: "openrouter-gemma-4",
  surface: "text",
  label: "Gemma 4 27B (OpenRouter)",
  blurb: "Free LLM · Google · multilingual",
  roles: {},
  settings: {},
  provider: { provider: "openrouter", modelId: "google/gemma-4-27b:free", needsKey: true },
  free: true,
};

const openrouterGptOss: ModelEntry = {
  id: "openrouter-gpt-oss-20b",
  surface: "text",
  label: "GPT-OSS 20B (OpenRouter)",
  blurb: "Free LLM · OpenAI · code-focused",
  roles: {},
  settings: {},
  provider: { provider: "openrouter", modelId: "openai/gpt-oss-20b:free", needsKey: true },
  free: true,
};

/* ============================================================================
 * KLING (Web session JWT) — 66 free credits/day
 * Signup: klingai.com (login with Google/email)
 * ==========================================================================*/

const klingFree: ModelEntry = {
  id: "kling-free",
  surface: "video",
  label: "Kling 1.6 (Klingai Web)",
  blurb: "🇨🇳 66 credits/day free · watermarked 720p",
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
 * MINIMAX — 30k initial credits + 5k/day refresh
 * Signup: platform.minimaxi.com (phone verification required)
 * ==========================================================================*/

const minimaxAudio: ModelEntry = {
  id: "minimax-audio-tts",
  surface: "audio",
  label: "MiniMax Speech-02 (TTS)",
  blurb: "🇨🇳 30k initial credits · Chinese TTS",
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
  blurb: "🇨🇳 30k initial credits · video",
  roles: {},
  settings: {
    duration: { type: "range", min: 5, max: 10, default: 5, step: 5 },
    aspect_ratio: { type: "enum", values: ["16:9", "9:16", "1:1", "4:3"], default: "16:9" },
  },
  provider: { provider: "minimax", kind: "video", needsKey: true },
  free: true,
};

/* ============================================================================
 * SUNO (Web session) — 50 free credits/day, ~10 songs/day
 * Signup: suno.com (login with Google/email)
 * ==========================================================================*/

const sunoFree: ModelEntry = {
  id: "suno-free",
  surface: "audio",
  label: "Suno V4 (Music)",
  blurb: "50 credits/day free · web session",
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
  // 5 Pollinations — no key needed
  pollinationsFlux,
  pollinationsTurbo,
  pollinationsFluxRealism,
  pollinationsFluxAnime,
  pollinationsFlux3d,
  // 4 HuggingFace direct — free with HF token
  hfFluxSchnell,
  hfFluxDev,
  hfSdxl,
  hfSd15,
  // 7 fal.ai — 5 free videos/day + $1 credit
  falFluxSchnell,
  falFluxDev,
  falFlux3MaxVideo,
  falKling16,
  falMinimaxHailuo,
  falVeo3Fast,
  falPikaTurbo,
  // 5 HF Router — $0.10/mo credit
  routerFluxSchnell,
  routerFluxDev,
  routerFluxKontext,
  routerLlama8b,
  routerQwen4b,
  // 3 OpenRouter — free LLMs
  openrouterLlama4,
  openrouterGemma4,
  openrouterGptOss,
  // 1 Kling direct
  klingFree,
  // 2 MiniMax direct
  minimaxAudio,
  minimaxVideo,
  // 1 Suno direct
  sunoFree,
];
