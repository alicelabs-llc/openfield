/**
 * MiniMax provider — supports audio (TTS Speech-02) and video (Hailuo).
 *
 * Auth: Bearer token from https://platform.minimaxi.com
 * Free tier: 30k credits initial, 5k daily refresh
 *
 * Audio endpoint:
 *   POST https://api.minimax.chat/v1/t2a_v2
 *
 * Video endpoint:
 *   POST https://api.minimax.chat/v1/video_generation
 */

const MINIMAX_API = "https://api.minimax.chat/v1";

export type MinimaxAudioRequest = {
  text: string;
  voice_id?: string;
  model?: "speech-02-hd" | "speech-02-turbo" | "speech-01-hd" | "speech-01-turbo";
  speed?: number; // 0.5 to 2.0
  vol?: number; // 0.5 to 2.0
  pitch?: number; // -12 to 12
  audio_format?: "mp3" | "wav" | "flac";
  sample_rate?: 16000 | 22050 | 24000 | 32000 | 44100;
};

export type MinimaxVideoRequest = {
  prompt: string;
  duration?: 5 | 10;
  aspect_ratio?: string;
  model?: "video-01" | "video-01-live2d" | "T2V-01D" | "T2V-01";
};

export async function submitMinimaxAudio(
  req: MinimaxAudioRequest,
  apiKey: string,
): Promise<{ requestId: string; audioUrl: string }> {
  const response = await fetch(`${MINIMAX_API}/t2a_v2`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: req.model ?? "speech-02-turbo",
      text: req.text,
      voice_setting: {
        voice_id: req.voice_id ?? "male-qn-qingse",
        speed: req.speed ?? 1.0,
        vol: req.vol ?? 1.0,
        pitch: req.pitch ?? 0,
      },
      audio_setting: {
        sample_rate: req.sample_rate ?? 24000,
        bitrate: 128000,
        format: req.audio_format ?? "mp3",
      },
    }),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`MiniMax audio ${response.status}: ${text.slice(0, 300)}`);
  }

  const data = (await response.json()) as {
    base_resp: { status_code: number; status_msg: string };
    data?: { audio?: string; status?: number };
    extra_info?: { audio_length?: number };
  };

  if (data.base_resp.status_code !== 0) {
    throw new Error(`MiniMax error: ${data.base_resp.status_msg}`);
  }

  const audioBase64 = data.data?.audio;
  if (!audioBase64) throw new Error("MiniMax returned no audio");

  return {
    requestId: `minimax-audio-${Date.now()}`,
    audioUrl: `data:audio/mp3;base64,${audioBase64}`,
  };
}

export async function submitMinimaxVideo(
  req: MinimaxVideoRequest,
  apiKey: string,
): Promise<{ requestId: string; statusUrl: string }> {
  const response = await fetch(`${MINIMAX_API}/video_generation`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: req.model ?? "T2V-01",
      prompt: req.prompt,
      duration: req.duration ?? 5,
      aspect_ratio: req.aspect_ratio ?? "16:9",
    }),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`MiniMax video submit ${response.status}: ${text.slice(0, 300)}`);
  }

  const data = (await response.json()) as {
    base_resp: { status_code: number; status_msg: string };
    task_id?: string;
    file_id?: string;
  };

  if (data.base_resp.status_code !== 0 || !data.task_id) {
    throw new Error(`MiniMax error: ${data.base_resp.status_msg}`);
  }

  return {
    requestId: data.task_id,
    statusUrl: `${MINIMAX_API}/query/video_generation?task_id=${data.task_id}`,
  };
}

export async function pollMinimaxVideo(
  requestId: string,
  statusUrl: string,
  apiKey: string,
): Promise<{
  status: string;
  requestId: string;
  video?: { url: string };
  error?: string;
}> {
  const response = await fetch(statusUrl, {
    headers: { Authorization: `Bearer ${apiKey}` },
  });

  if (!response.ok) {
    return { status: "failed", requestId, error: `MiniMax poll ${response.status}` };
  }

  const data = (await response.json()) as {
    base_resp: { status_code: number };
    status: "Queueing" | "Preparing" | "Generating" | "Success" | "Failed";
    file_id?: string;
    video_url?: string;
  };

  if (data.status === "Success") {
    if (!data.video_url) {
      return { status: "failed", requestId, error: "MiniMax returned no video URL" };
    }
    return { status: "completed", requestId, video: { url: data.video_url } };
  }
  if (data.status === "Failed") {
    return { status: "failed", requestId, error: "MiniMax generation failed" };
  }
  return { status: "processing", requestId };
}
