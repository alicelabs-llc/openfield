/**
 * Kling AI provider — uses the public Klingai web API (no official dev API
 * access required). Free tier: 66 credits per day per account, refresh every
 * 24 hours. Watermarked 720p output, no commercial use.
 *
 * Auth: Bearer JWT from klingai.com session (paste from browser devtools)
 *
 * Flow:
 *   1. POST https://klingai.com/api/v1/text2video — create task
 *   2. GET  https://klingai.com/api/v1/text2video/{task_id} — poll until done
 *
 * This is the unofficial API path; if Kling changes it, this provider breaks.
 * For official API access, see https://klingai.com/dev — requires credit pack.
 */

const KLING_API = "https://klingai.kuaishou.com/api/v1";

export type KlingVideoRequest = {
  prompt: string;
  duration?: 5 | 10;
  aspect_ratio?: "16:9" | "9:16" | "1:1";
  style?: "standard" | "professional";
};

export async function submitKlingVideo(
  req: KlingVideoRequest,
  jwt: string,
): Promise<{ requestId: string; statusUrl: string }> {
  const response = await fetch(`${KLING_API}/text2video`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${jwt}`,
      "Content-Type": "application/json",
      Origin: "https://klingai.com",
      Referer: "https://klingai.com/",
    },
    body: JSON.stringify({
      prompt: req.prompt,
      duration: req.duration ?? 5,
      ratio: req.aspect_ratio ?? "16:9",
      mode: req.style ?? "standard",
      model_version: "1.6",
      callback_url: "",
    }),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Kling submit ${response.status}: ${text.slice(0, 300)}`);
  }

  const data = (await response.json()) as {
    code: number;
    data: { task_id: string };
  };

  if (data.code !== 0 || !data.data?.task_id) {
    throw new Error(`Kling rejected request: ${JSON.stringify(data).slice(0, 300)}`);
  }

  const taskId = data.data.task_id;
  return {
    requestId: taskId,
    statusUrl: `${KLING_API}/text2video/${taskId}`,
  };
}

export async function pollKlingStatus(
  requestId: string,
  _statusUrl: string,
  jwt: string,
): Promise<{
  status: string;
  requestId: string;
  video?: { url: string };
  error?: string;
}> {
  const response = await fetch(`${KLING_API}/text2video/${requestId}`, {
    headers: {
      Authorization: `Bearer ${jwt}`,
      Origin: "https://klingai.com",
      Referer: "https://klingai.com/",
    },
  });

  if (!response.ok) {
    return { status: "failed", requestId, error: `Kling poll ${response.status}` };
  }

  const data = (await response.json()) as {
    code: number;
    data: {
      task_status: "processing" | "success" | "failed";
      task_result?: { videos?: Array<{ url: string }> };
      task_info?: { errmsg?: string };
    };
  };

  if (data.code !== 0) {
    return { status: "failed", requestId, error: `Kling code ${data.code}` };
  }

  const status = data.data?.task_status;
  if (status === "success") {
    const videoUrl = data.data?.task_result?.videos?.[0]?.url;
    if (!videoUrl) {
      return { status: "failed", requestId, error: "Kling returned no video URL" };
    }
    return { status: "completed", requestId, video: { url: videoUrl } };
  }
  if (status === "failed") {
    return {
      status: "failed",
      requestId,
      error: data.data?.task_info?.errmsg ?? "Kling generation failed",
    };
  }
  return { status: "processing", requestId };
}
