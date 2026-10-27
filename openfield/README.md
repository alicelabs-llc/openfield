# OpenField — 100% Free Open-Source AI Studio

> Forked from `wide-trace/open-higgsfield`, rewritten to use only free APIs.
> No Higgsfield API key required. No subscription. No $5 topup.

## 🌐 What this fork changes

The original `open-higgsfield` repo is a beautiful Next.js 16 frontend that proxies to the **paid** Higgsfield Cloud API (`api.higgsfield.ai`). It calls itself free because the studio UI is free, but every generation costs real money against your prepaid Higgsfield balance ($5 minimum).

OpenField rewrites the backend to call **actually free APIs** instead:

| Provider | Free tier | Key required | Models |
|---|---|---|---|
| **Pollinations.ai** | 100% free, no rate limit (soft) | ❌ None | Flux, Turbo, Flux Realism, Flux Anime, Flux 3D |
| **HuggingFace Inference** | ~30 req/hour on free tier | ✅ Free HF token | FLUX.1-schnell, FLUX.1-dev, SDXL 1.0, SD 1.5 |

That's **9 image models, 100% free**. The trade-off:

- **No video generation** (yet) — none of the free providers offer a usable free video API. Kling, Seedance, Veo are all paid and proprietary. Adding free video is on the roadmap.
- **Lower quality on HF free tier** — rate-limited, but works.
- **No batch, no per-model tuning** beyond what each free API exposes.

## 🚀 Run it locally

```bash
git clone https://github.com/alicelabs-llc/openfield.git
cd openfield
pnpm install
pnpm dev   # http://localhost:3000
```

Open the studio. Pick any **Pollinations** model — it just works, no setup.

For **HuggingFace** models, click the key icon and paste a free token from
[huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) (sign up free, generate a "Read" token, paste it).

## 🔑 Environment variables

```bash
# Required for Vercel Blob (file uploads). Get one free at vercel.com
OPEN_HIGGSFIELD_READ_WRITE_TOKEN=

# Optional: site URL for OG tags
NEXT_PUBLIC_SITE_URL=https://your-domain.com
```

No `HF_API_BASE_URL` needed anymore — each provider knows its own base URL.

## 📦 Deploy to Vercel

1. Push this repo to GitHub
2. Import it on [vercel.com](https://vercel.com)
3. Add the env vars above
4. Deploy

The studio is fully static-friendly except for the server actions that call the providers, which run on the Edge or Node runtime.

## 🗺️ Roadmap — what's missing

| Feature | Status | Why |
|---|---|---|
| Pollinations image (5 models) | ✅ Done | 100% free, no key |
| HuggingFace image (4 models) | ✅ Done | Free with HF token |
| Pollinations video | 🚧 Pending | API announced, not stable yet |
| Replicate free-tier image | 📋 Planned | Need signup flow |
| fal.ai free tier | 📋 Planned | $1 free credit on signup |
| Modal free tier | 📋 Planned | $30 free credits monthly |
| Local ComfyUI bridge | 💭 Idea | Run your own GPU, fully free |
| Direct Gradio/Spaces | 💭 Idea | HuggingFace Spaces are free but slow |

## 🔬 Architecture

```
Browser → Next.js server action → Provider dispatcher
                                  ├─ Pollinations API (no key)
                                  ├─ HuggingFace Inference API (HF token)
                                  └─ [future] Replicate / fal.ai / Modal
```

Each model in `src/generation/catalog/free-models.ts` declares which provider
it uses. Adding a new model is one entry — no UI changes needed.

## ⚖️ License & attribution

- Original code: © 2026 wide-trace (GitHub) — MIT-style, source available on GitHub
- OpenField modifications: © 2026 AliceLabs LLC — MIT

The original UI, design system, and architecture are kept intact. Only the
backend provider layer is rewritten.

## ⚠️ Honest limitations

1. **Pollinations sometimes returns 502/503** under load — retry with a different seed
2. **HuggingFace rate-limits aggressively** — 30 req/hour is the soft cap, you may hit 429
3. **No video generation** — the most-requested feature, blocked by lack of free video APIs
4. **No persistence across devices** — IndexedDB only, no account sync
5. **Result URLs from Pollinations expire** — they're cached on their CDN, not yours

If you need paid features (Kling 3, Seedance 2.5, etc.), use the original
`open-higgsfield` repo with a Higgsfield Cloud API account.
