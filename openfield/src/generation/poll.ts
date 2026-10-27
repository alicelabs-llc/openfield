"use client";

import { getGenerationStatuses } from "./actions";
import type { GenerationResult } from "@/providers";
import type { QueuedRequest } from "@/providers";

/** Statuses the platform never moves off again. */
const TERMINAL = new Set(["completed", "failed", "nsfw", "canceled"]);

export const POLL_INTERVAL_MS = 4000;
export const POLL_DEADLINE_MS = 10 * 60_000;
const MAX_MISSES = 3;

type Waiter = {
  request: QueuedRequest;
  deadline: number;
  resolve: (status: GenerationResult) => void;
  reject: (reason: Error) => void;
};

const waiting = new Map<string, Waiter>();
const inflight = new Map<string, Promise<GenerationResult>>();
let timer: ReturnType<typeof setTimeout> | null = null;
let polling = false;
let misses = 0;

/** Resolves when the provider reports a terminal status for this request.
    Every request in flight is asked for together, in one server action per
    interval — Next dispatches server actions one at a time per client, so a
    poll per run would queue ahead of the next submit. */
export function watchRequest(
  request: QueuedRequest,
  opts?: { deadline?: number },
): Promise<GenerationResult> {
  const existing = inflight.get(request.requestId);
  if (existing) return existing;
  const promise = new Promise<GenerationResult>((resolve, reject) => {
    waiting.set(request.requestId, {
      request,
      deadline: opts?.deadline ?? Date.now() + POLL_DEADLINE_MS,
      resolve: (status) => {
        inflight.delete(request.requestId);
        resolve(status);
      },
      reject: (reason) => {
        inflight.delete(request.requestId);
        reject(reason);
      },
    });
    schedule();
  });
  inflight.set(request.requestId, promise);
  return promise;
}

/** Drops every watch without settling it: the studio unmounted. */
export function stopWatching(): void {
  if (timer !== null) clearTimeout(timer);
  timer = null;
  misses = 0;
  waiting.clear();
  inflight.clear();
}

function schedule(): void {
  if (timer !== null || polling || waiting.size === 0) return;
  timer = setTimeout(() => void round(), POLL_INTERVAL_MS);
}

async function round(): Promise<void> {
  timer = null;
  polling = true;
  try {
    const requests = [...waiting.values()].map((w) => w.request);
    const results = await getGenerationStatuses({ requests });
    misses = 0;
    for (const result of results) deliver(result);
    sweep();
  } catch (caught) {
    if (++misses < MAX_MISSES) return;
    settleAll(caught instanceof Error ? caught : new Error(String(caught)));
  } finally {
    polling = false;
    schedule();
  }
}

function deliver(result: GenerationResult): void {
  const waiter = waiting.get(result.requestId);
  if (!waiter) return;
  if (result.status === "failed" || result.error) {
    waiting.delete(result.requestId);
    waiter.reject(new Error(result.error ?? "Generation failed"));
    return;
  }
  if (!TERMINAL.has(result.status)) return;
  waiting.delete(result.requestId);
  waiter.resolve(result);
}

function sweep(): void {
  const now = Date.now();
  for (const [id, waiter] of waiting) {
    if (waiter.deadline > now) continue;
    waiting.delete(id);
    waiter.reject(new Error("Poll deadline exceeded"));
  }
}

function settleAll(reason: Error): void {
  for (const [, waiter] of waiting) waiter.reject(reason);
  waiting.clear();
  inflight.clear();
}
