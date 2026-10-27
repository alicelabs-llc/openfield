/**
 * Legacy compat layer — kept because poll.ts and other modules import these
 * types. In OpenField, the actual provider dispatch lives in @/providers.
 */

export type QueuedGeneration = {
  status: string;
  requestId: string;
  statusUrl: string;
  cancelUrl: string;
};

export type GenerationStatus = {
  status: string;
  requestId: string;
  images?: Array<{ url: string }>;
  video?: { url: string };
  error?: unknown;
};

export type StatusResult =
  | { requestId: string; status: GenerationStatus }
  | { requestId: string; error: string };

export type PlatformClientOptions = {
  apiKey: string;
  baseUrl: string;
  fetch?: typeof fetch;
};

export class PlatformError extends Error {
  readonly status: number;
  readonly body: unknown;

  constructor(status: number, body: unknown) {
    super(messageFromBody(status, body));
    this.name = "PlatformError";
    this.status = status;
    this.body = body;
  }
}

export function isModelId(model: string): boolean {
  return /^[a-z0-9][a-z0-9._/-]*$/i.test(model) && !model.includes("..");
}

function messageFromBody(status: number, body: unknown): string {
  if (body !== null && typeof body === "object" && !Array.isArray(body)) {
    const detail = (body as Record<string, unknown>).detail;
    if (typeof detail === "string" && detail) return detail;
  }
  return `Platform request failed (${status})`;
}
