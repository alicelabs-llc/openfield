export type Surface = "image" | "video" | "audio" | "text";
export type MediaRole = "start" | "end" | "reference" | "video" | "audio";

export type MediaItem = {
  id: string;
  url: string;
  role: MediaRole;
};

export type SettingField =
  | { type: "enum"; values: readonly string[]; default: string }
  | { type: "range"; min: number; max: number; default: number; step?: number }
  | { type: "boolean"; default: boolean };

export type ProviderConfig =
  | {
      provider: "pollinations";
      model: "flux" | "flux-realism" | "flux-anime" | "flux-3d" | "flux-cablyai" | "turbo";
      needsKey: false;
    }
  | {
      provider: "huggingface";
      model: string;
      needsKey: true;
      defaultSteps?: number;
      defaultGuidance?: number;
    }
  | {
      provider: "hf-router";
      modelId: string;
      task: "text-to-image" | "image-to-image" | "text-to-video" | "chat-completions";
      needsKey: true;
    }
  | {
      provider: "fal";
      kind: "image" | "video";
      model: string;
      needsKey: true;
    }
  | {
      provider: "kling";
      needsKey: true;
    }
  | {
      provider: "minimax";
      kind: "audio" | "video";
      needsKey: true;
    }
  | {
      provider: "suno";
      needsKey: true;
    };

export type ModelEntry = {
  id: string;
  surface: Surface;
  label: string;
  roles: Partial<Record<MediaRole, number>>;
  settings: Record<string, SettingField>;
  provider: ProviderConfig;
  free: boolean;
  /** Optional marketing blurb shown in the model picker */
  blurb?: string;
};

export type GenerationPlane = {
  model: string;
  prompt: { text: string };
  media: Partial<Record<MediaRole, MediaItem[]>>;
  settings: Record<string, unknown>;
};
