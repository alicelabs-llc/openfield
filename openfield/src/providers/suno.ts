/**
 * Suno AI provider — unofficial API for music generation.
 *
 * Auth: Bearer session token from suno.com (paste from browser devtools)
 * Free tier: 50 credits/day (~10 songs)
 *
 * Flow (uses the unofficial suno.com/api endpoint):
 *   1. POST /api/generate/v2/ — start generation, returns clip ids
 *   2. GET  /api/feed/?ids=xxx — poll until clips are ready
 *
 * Note: Suno's official API requires paid subscription ($30+/mo).
 * This provider uses the web session API that backs the suno.com web app.
 * It can break any time Suno changes their backend.
 *
 * For commercial/stable use, get the official API at https://suno.com/api
 */

const SUNO_API = "https://studio-api.suno.ai/api";

export type SunoSongRequest = {
  prompt: string;
  make_instrumental?: boolean;
  wait_audio?: boolean;
  model?: "chirp-v4" | "chirp-v3.5" | "chirp-v4.5";
  tags?: string; // genre tags
  title?: string;
  negative_tags?: string;
};

export async function submitSunoSong(
  req: SunoSongRequest,
  sessionToken: string,
): Promise<{ requestIds: string[]; statusUrl: string }> {
  const response = await fetch(`${SUNO_API}/generate/v2/`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${sessionToken}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      gpt_description_prompt: req.prompt,
      make_instrumental: req.make_instrumental ?? false,
      mv: req.model ?? "chirp-v4",
      title: req.title ?? "",
      tags: req.tags ?? "",
      negative_tags: req.negative_tags ?? "",
      wait_audio: false,
    }),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Suno submit ${response.status}: ${text.slice(0, 300)}`);
  }

  const data = (await response.json()) as Array<{
    id: string;
    audio_url?: string;
    status?: string;
  }>;

  if (!Array.isArray(data) || data.length === 0) {
    throw new Error("Suno returned no clips");
  }

  const ids = data.map((clip) => clip.id);
  return {
    requestIds: ids,
    statusUrl: `${SUNO_API}/feed/?ids=${ids.join(",")}`,
  };
}

export async function pollSunoStatus(
  requestIds: string[],
  statusUrl: string,
  sessionToken: string,
): Promise<{
  status: string;
  requestId: string;
  audio?: Array<{ url: string; title?: string }>;
  error?: string;
}> {
  const response = await fetch(statusUrl, {
    headers: { Authorization: `Bearer ${sessionToken}` },
  });

  if (!response.ok) {
    return {
      status: "failed",
      requestId: requestIds[0] ?? "unknown",
      error: `Suno poll ${response.status}`,
    };
  }

  const data = (await response.json()) as Array<{
    id: string;
    status: "queued" | "loading" | "complete" | "error";
    audio_url?: string;
    title?: string;
    error_message?: string;
  }>;

  if (!Array.isArray(data)) {
    return {
      status: "failed",
      requestId: requestIds[0] ?? "unknown",
      error: "Suno returned unexpected shape",
    };
  }

  const allComplete = data.every((clip) => clip.status === "complete");
  const anyError = data.some((clip) => clip.status === "error");

  if (anyError) {
    const errClip = data.find((clip) => clip.status === "error");
    return {
      status: "failed",
      requestId: requestIds[0] ?? "unknown",
      error: errClip?.error_message ?? "Suno generation failed",
    };
  }

  if (allComplete) {
    return {
      status: "completed",
      requestId: requestIds[0] ?? "unknown",
      audio: data
        .filter((clip) => clip.audio_url)
        .map((clip) => ({ url: clip.audio_url!, title: clip.title })),
    };
  }

  return { status: "processing", requestId: requestIds[0] ?? "unknown" };
}
