/**
 * Provider signup info — used by the Settings page to show direct links
 * where users can get a free API key for each provider.
 *
 * All providers here offer a genuine free tier (verified Oct 2026).
 */

export type ProviderSignup = {
  /** Provider id — matches ProviderName in providers/index.ts */
  id: string;
  /** Display name */
  name: string;
  /** Direct URL where the user signs up and gets an API key */
  signupUrl: string;
  /** URL of the docs / dashboard */
  docsUrl?: string;
  /** What the free tier actually gives you */
  freeTier: string;
  /** Token format hint (e.g. "hf_xxx", "sk-...", "Bearer JWT from browser") */
  tokenFormat: string;
  /** Marketing blurb shown in the UI */
  blurb: string;
  /** Whether the key is required for ANY model on this provider */
  required: boolean;
  /** Auth header format ("Bearer" or "Key" or "session") */
  authHeader: "Bearer" | "Key" | "session";
  /** Models this provider unlocks (just for display) */
  unlocksModels: string[];
};

export const PROVIDER_SIGNUPS: ProviderSignup[] = [
  {
    id: "pollinations",
    name: "Pollinations",
    signupUrl: "https://enter.pollinations.ai",
    docsUrl: "https://github.com/pollinations/pollinations",
    freeTier:
      "5 image models 100% free without key. With free pollen key: ~1.5 Pollen/week, more reliable + audio/video/text unblocked.",
    tokenFormat: "pk_xxx (publishable) or sk_xxx (secret)",
    blurb: "Berlin-based open-source GenAI. The default for free image generation.",
    required: false,
    authHeader: "Bearer",
    unlocksModels: ["Flux", "Turbo", "Realism", "Anime", "3D"],
  },
  {
    id: "huggingface",
    name: "Hugging Face",
    signupUrl: "https://huggingface.co/settings/tokens",
    docsUrl: "https://huggingface.co/docs/inference-providers",
    freeTier:
      "Free account: $0.10 monthly credit on Inference Providers (very tight). PRO ($9/mo): $2 monthly credit, 8x ZeroGPU quota, 1TB storage. ~30 req/hour on free classic Inference API.",
    tokenFormat: "hf_xxxxxxxxxxxxxxxxxxxxxxxx",
    blurb: "Largest open model hub. Required for FLUX, SDXL, Llama, Qwen.",
    required: true,
    authHeader: "Bearer",
    unlocksModels: [
      "FLUX.1-schnell",
      "FLUX.1-dev",
      "FLUX.1-Kontext",
      "SDXL 1.0",
      "SD 1.5",
      "Llama 3.1 8B",
      "Qwen3-4B",
    ],
  },
  {
    id: "fal",
    name: "fal.ai",
    signupUrl: "https://fal.ai/dashboard/keys",
    docsUrl: "https://fal.ai/docs",
    freeTier:
      "5 free FLUX 3 Max videos (720p) every 24h on rolling window. Plus 1 free 720p video with sound. ~$1 signup credit for image generation.",
    tokenFormat: "fal_xxxxxxxxxxxxxxxxxxxxxxxx",
    blurb: "Hosted video + image infra. Powers 40% of Poe's media generation.",
    required: true,
    authHeader: "Key",
    unlocksModels: [
      "FLUX.1-schnell",
      "FLUX.1-dev",
      "Kling 1.6",
      "MiniMax Hailuo 02",
      "Veo 3 Fast",
      "Pika v2.2",
    ],
  },
  {
    id: "replicate",
    name: "Replicate",
    signupUrl: "https://replicate.com/signin",
    docsUrl: "https://replicate.com/docs",
    freeTier:
      "Free tier: limited number of free models (no credit card required). Plus up to $500 free credits for new accounts (per-second billing on open models).",
    tokenFormat: "r8_xxxxxxxxxxxxxxxxxxxxxxxx",
    blurb: "100+ official models, pay-per-second. Best for trying many models.",
    required: true,
    authHeader: "Bearer",
    unlocksModels: ["FLUX.1-dev", "SDXL", "Stable Video Diffusion", "Whisper"],
  },
  {
    id: "openrouter",
    name: "OpenRouter",
    signupUrl: "https://openrouter.ai/keys",
    docsUrl: "https://openrouter.ai/docs",
    freeTier:
      "Free models: ~50 req/day (under $10 spent) or ~1,000 req/day (after $10 top-up). 20 req/min cap. Many LLMs including Llama 4 Maverick, Gemma 4, GPT-OSS 20B.",
    tokenFormat: "sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxx",
    blurb: "Unified gateway to 300+ LLMs. ~30 models are 100% free.",
    required: true,
    authHeader: "Bearer",
    unlocksModels: ["Llama 4 Maverick", "Gemma 4", "GPT-OSS 20B", "Nemotron 3", "Qwen3"],
  },
  {
    id: "together",
    name: "Together AI",
    signupUrl: "https://api.together.xyz/settings/api-keys",
    docsUrl: "https://docs.together.ai",
    freeTier: "$1 free signup credit. ~$25 trial credit historically. Image + LLM endpoints.",
    tokenFormat: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    blurb: "Open model hosting. Strong for image generation + Llama.",
    required: true,
    authHeader: "Bearer",
    unlocksModels: ["FLUX.1-schnell", "FLUX.1-dev", "SDXL", "Llama 3.3 70B"],
  },
  {
    id: "segmind",
    name: "Segmind",
    signupUrl: "https://www.segmind.com/",
    docsUrl: "https://www.segmind.com/docs",
    freeTier: "100 free credits on signup. Image + video + audio endpoints including Luma.",
    tokenFormat: "SG_xxxxxxxxxxxxxxxxxxxxxxxx",
    blurb: "Serverless AI models. Includes Luma Dream Machine video gen.",
    required: true,
    authHeader: "Bearer",
    unlocksModels: ["Luma img-2-video", "SDXL", "FLUX.1-schnell"],
  },
  {
    id: "kling",
    name: "Kling AI (Web session)",
    signupUrl: "https://klingai.com",
    docsUrl: "https://klingai.com/dev",
    freeTier:
      "66 free credits/day (resets every 24h). ~2 standard 720p videos/day. Watermark, non-commercial only.",
    tokenFormat: "Bearer JWT from browser devtools (Network tab → Authorization header)",
    blurb: "Kuaishou's Chinese video model. Free web tier, unofficial API.",
    required: true,
    authHeader: "Bearer",
    unlocksModels: ["Kling 1.6 (Web)"],
  },
  {
    id: "minimax",
    name: "MiniMax (Chinese)",
    signupUrl: "https://platform.minimaxi.com",
    docsUrl: "https://platform.minimaxi.com/document/Announcement",
    freeTier:
      "30,000 free credits on signup. 5,000 free credits daily refresh. Covers TTS (Speech-02) + Hailuo video generation.",
    tokenFormat: "xxxxxxxxxxxxxxxxxxxxxxxx",
    blurb: "Chinese AI lab. Best TTS + Hailuo video model. Requires phone verification.",
    required: true,
    authHeader: "Bearer",
    unlocksModels: ["MiniMax Speech-02 TTS", "MiniMax Hailuo video"],
  },
  {
    id: "suno",
    name: "Suno (Web session)",
    signupUrl: "https://suno.com",
    docsUrl: "https://suno.com/api",
    freeTier:
      "50 free credits/day (anonymous). ~10 songs/day. Watermarked MP3 192kbps. Non-commercial only.",
    tokenFormat: "Bearer session token from browser devtools (cookie or Authorization header)",
    blurb: "AI music generation. Free web tier — no official free API.",
    required: true,
    authHeader: "Bearer",
    unlocksModels: ["Suno V4 Music"],
  },
];

export function getSignupForProvider(providerId: string): ProviderSignup | undefined {
  return PROVIDER_SIGNUPS.find((p) => p.id === providerId);
}
