/**
 * Multi-provider credentials storage.
 *
 * Stored in a single httpOnly cookie as JSON. Different providers need
 * different token shapes:
 *
 *   hfToken     — HuggingFace bearer (hf_xxx)
 *   falKey      — fal.ai API key
 *   klingJwt    — Kling session JWT (from browser devtools)
 *   minimaxKey  — MiniMax API key
 *   sunoToken   — Suno session token (from browser devtools)
 */

export const CREDENTIALS_COOKIE = "openfield_creds";
export const CREDENTIALS_COOKIE_OPTIONS = {
  httpOnly: true,
  secure: process.env.NODE_ENV === "production",
  sameSite: "lax" as const,
  path: "/",
  maxAge: 60 * 60 * 24 * 365, // 1 year
};

export class MissingCredentialsError extends Error {
  readonly provider: string;

  constructor(provider: string) {
    const messages: Record<string, string> = {
      huggingface: "This model needs a HuggingFace token. Get one free at huggingface.co/settings/tokens",
      "hf-router": "This model needs a HuggingFace token. Get one free at huggingface.co/settings/tokens",
      fal: "This model needs a fal.ai API key. Get $1 free credit at fal.ai/dashboard/keys",
      kling: "This model needs a Kling session JWT. Open klingai.com, log in, copy the Bearer token from your browser devtools",
      minimax: "This model needs a MiniMax API key. Get one at platform.minimaxi.com (30k free credits)",
      suno: "This model needs a Suno session token. Open suno.com, log in, copy the Bearer token from your browser devtools",
    };
    super(messages[provider] ?? `This model needs ${provider} credentials`);
    this.name = "MissingCredentialsError";
    this.provider = provider;
  }
}

export type StoredCredentials = {
  hfToken?: string;
  falKey?: string;
  klingJwt?: string;
  minimaxKey?: string;
  sunoToken?: string;
};

export function encodeCredentials(creds: StoredCredentials): string {
  return JSON.stringify(creds);
}

export function decodeCredentials(raw: string | undefined): StoredCredentials | null {
  if (!raw) return null;
  try {
    const parsed = JSON.parse(raw) as unknown;
    if (parsed === null || typeof parsed !== "object" || Array.isArray(parsed)) return null;
    const record = parsed as Record<string, unknown>;
    const creds: StoredCredentials = {};
    if (typeof record.hfToken === "string" && record.hfToken.trim()) creds.hfToken = record.hfToken.trim();
    if (typeof record.falKey === "string" && record.falKey.trim()) creds.falKey = record.falKey.trim();
    if (typeof record.klingJwt === "string" && record.klingJwt.trim()) creds.klingJwt = record.klingJwt.trim();
    if (typeof record.minimaxKey === "string" && record.minimaxKey.trim()) creds.minimaxKey = record.minimaxKey.trim();
    if (typeof record.sunoToken === "string" && record.sunoToken.trim()) creds.sunoToken = record.sunoToken.trim();
    return Object.keys(creds).length === 0 ? null : creds;
  } catch {
    return null;
  }
}

/**
 * Legacy compat: the key modal may still post a single token (the old
 * "id:secret" shape from openhiggsfield). We try to detect that and route
 * it to the right field based on a prefix:
 *   hf_xxx → hfToken
 *   no prefix + short → falKey
 */
export function parseCredentialInput(data: unknown): StoredCredentials {
  if (data === null || typeof data !== "object" || Array.isArray(data)) {
    throw new Error("Invalid credentials payload");
  }
  const record = data as Record<string, unknown>;

  // New shape: { hfToken, falKey, klingJwt, minimaxKey, sunoToken }
  const creds: StoredCredentials = {};
  for (const key of ["hfToken", "falKey", "klingJwt", "minimaxKey", "sunoToken"] as const) {
    const v = record[key] ?? record[key.toLowerCase()] ?? record[key.replace(/([A-Z])/g, "_$1").toLowerCase()];
    if (typeof v === "string" && v.trim()) {
      creds[key] = v.trim();
    }
  }

  // Legacy: single apiKey field — route by prefix
  const legacyKey = (record.apiKey ?? record.api_key ?? record.token) as unknown;
  if (typeof legacyKey === "string" && legacyKey.trim()) {
    const trimmed = legacyKey.trim();
    if (trimmed.startsWith("hf_")) creds.hfToken = trimmed;
    else if (!creds.falKey) creds.falKey = trimmed;
  }

  if (Object.keys(creds).length === 0) {
    throw new Error("Enter at least one credential");
  }
  return creds;
}
