/**
 * Encrypted credentials storage.
 *
 * - In the browser: AES-GCM encrypted blob stored in localStorage, decrypted
 *   with a user-provided passphrase.
 * - On the server: httpOnly cookie set via the Settings page action.
 *
 * The passphrase never leaves the browser. If the user loses the passphrase,
 * the credentials are unrecoverable.
 *
 * Storage shape:
 *   localStorage["openfield.creds.v1"] = "<base64(salt|iv|ciphertext)>"
 */

const STORAGE_KEY = "openfield.creds.v1";
const SALT_BYTES = 16;
const IV_BYTES = 12;
const KEY_BITS = 256;

export type StoredCredentials = {
  pollinations?: string;
  huggingface?: string;
  fal?: string;
  replicate?: string;
  openrouter?: string;
  together?: string;
  segmind?: string;
  kling?: string;
  minimax?: string;
  suno?: string;
};

/* ---------- crypto helpers ---------- */

async function deriveKey(passphrase: string, salt: Uint8Array): Promise<CryptoKey> {
  const enc = new TextEncoder();
  const baseKey = await crypto.subtle.importKey(
    "raw",
    enc.encode(passphrase) as BufferSource,
    { name: "PBKDF2" },
    false,
    ["deriveKey"],
  );
  return crypto.subtle.deriveKey(
    { name: "PBKDF2", salt: salt as BufferSource, iterations: 200_000, hash: "SHA-256" },
    baseKey,
    { name: "AES-GCM", length: KEY_BITS },
    false,
    ["encrypt", "decrypt"],
  );
}

function bytesToBase64(bytes: Uint8Array): string {
  let binary = "";
  for (let i = 0; i < bytes.length; i++) {
    binary += String.fromCharCode(bytes[i]!);
  }
  return btoa(binary);
}

function base64ToBytes(b64: string): Uint8Array {
  const binary = atob(b64);
  const out = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    out[i] = binary.charCodeAt(i);
  }
  return out;
}

/* ---------- public API ---------- */

export async function encryptCredentials(
  creds: StoredCredentials,
  passphrase: string,
): Promise<string> {
  const salt = crypto.getRandomValues(new Uint8Array(SALT_BYTES));
  const iv = crypto.getRandomValues(new Uint8Array(IV_BYTES));
  const key = await deriveKey(passphrase, salt);
  const enc = new TextEncoder();
  const plaintext = enc.encode(JSON.stringify(creds));
  const ciphertext = await crypto.subtle.encrypt({ name: "AES-GCM", iv: iv as BufferSource }, key, plaintext as BufferSource);
  const combined = new Uint8Array(salt.length + iv.length + ciphertext.byteLength);
  combined.set(salt, 0);
  combined.set(iv, salt.length);
  combined.set(new Uint8Array(ciphertext), salt.length + iv.length);
  return bytesToBase64(combined);
}

export async function decryptCredentials(
  blob: string,
  passphrase: string,
): Promise<StoredCredentials> {
  const combined = base64ToBytes(blob);
  const salt = combined.slice(0, SALT_BYTES);
  const iv = combined.slice(SALT_BYTES, SALT_BYTES + IV_BYTES);
  const ciphertext = combined.slice(SALT_BYTES + IV_BYTES);
  const key = await deriveKey(passphrase, salt);
  try {
    const plaintext = await crypto.subtle.decrypt({ name: "AES-GCM", iv: iv as BufferSource }, key, ciphertext as BufferSource);
    const dec = new TextDecoder();
    return JSON.parse(dec.decode(plaintext)) as StoredCredentials;
  } catch {
    throw new Error(
      "Could not decrypt credentials. Wrong passphrase, or the data was corrupted.",
    );
  }
}

export function loadEncryptedBlob(): string | null {
  if (typeof window === "undefined") return null;
  try {
    return window.localStorage.getItem(STORAGE_KEY);
  } catch {
    return null;
  }
}

export function saveEncryptedBlob(blob: string): void {
  if (typeof window === "undefined") return;
  try {
    window.localStorage.setItem(STORAGE_KEY, blob);
  } catch (e) {
    console.error("Failed to save credentials blob", e);
  }
}

export function clearEncryptedBlob(): void {
  if (typeof window === "undefined") return;
  try {
    window.localStorage.removeItem(STORAGE_KEY);
  } catch {
    /* ignore */
  }
}

/**
 * Export credentials as a .env file (plaintext). Used by the "Download .env"
 * button in Settings. The user is warned that this file contains secrets.
 */
export function exportAsEnvFile(creds: StoredCredentials): string {
  const lines: string[] = [
    "# OpenField credentials — generated on " + new Date().toISOString(),
    "# ⚠️  This file contains secrets. Do NOT commit to git. Do NOT share.",
    "",
  ];
  const mapping: Array<[keyof StoredCredentials, string]> = [
    ["pollinations", "POLLINATIONS_TOKEN"],
    ["huggingface", "HF_TOKEN"],
    ["fal", "FAL_KEY"],
    ["replicate", "REPLICATE_API_TOKEN"],
    ["openrouter", "OPENROUTER_API_KEY"],
    ["together", "TOGETHER_API_KEY"],
    ["segmind", "SEGMIND_API_KEY"],
    ["kling", "KLING_JWT"],
    ["minimax", "MINIMAX_API_KEY"],
    ["suno", "SUNO_SESSION_TOKEN"],
  ];
  for (const [field, envVar] of mapping) {
    const val = creds[field];
    if (val) {
      lines.push(`${envVar}=${val}`);
    }
  }
  return lines.join("\n");
}

/**
 * Import credentials from a .env file (plaintext or base64-encrypted).
 * Returns parsed credentials. Only known env vars are recognized.
 */
export function parseEnvFile(contents: string): StoredCredentials {
  const creds: StoredCredentials = {};
  const mapping: Record<string, keyof StoredCredentials> = {
    POLLINATIONS_TOKEN: "pollinations",
    HF_TOKEN: "huggingface",
    HUGGINGFACE_TOKEN: "huggingface",
    FAL_KEY: "fal",
    FALAI_KEY: "fal",
    REPLICATE_API_TOKEN: "replicate",
    REPLICATE_API_KEY: "replicate",
    OPENROUTER_API_KEY: "openrouter",
    OPENROUTER_KEY: "openrouter",
    TOGETHER_API_KEY: "together",
    TOGETHERAI_API_KEY: "together",
    SEGMIND_API_KEY: "segmind",
    KLING_JWT: "kling",
    KLING_TOKEN: "kling",
    MINIMAX_API_KEY: "minimax",
    MINIMAX_KEY: "minimax",
    SUNO_SESSION_TOKEN: "suno",
    SUNO_TOKEN: "suno",
  };
  for (const line of contents.split("\n")) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const eqIdx = trimmed.indexOf("=");
    if (eqIdx <= 0) continue;
    const key = trimmed.slice(0, eqIdx).trim();
    const value = trimmed.slice(eqIdx + 1).trim().replace(/^["']|["']$/g, "");
    const field = mapping[key];
    if (field && value) {
      creds[field] = value;
    }
  }
  return creds;
}
