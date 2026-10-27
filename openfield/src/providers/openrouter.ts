/**
 * OpenRouter provider — unified gateway to 300+ LLMs.
 *
 * URL: https://openrouter.ai/api/v1/chat/completions
 * Auth: Authorization: Bearer <openrouter_key>
 * Free tier: ~50 free-model requests/day (under $10 spent), ~1000/day after $10 top-up
 *
 * Free models have ":free" suffix in their id (e.g. "openai/gpt-oss-20b:free").
 */

const OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions";

export type OpenRouterRequest = {
  model: string; // e.g. "meta-llama/llama-4-maverick:free"
  prompt: string;
  systemPrompt?: string;
};

export async function submitOpenRouter(req: OpenRouterRequest, apiKey: string) {
  const messages = [
    ...(req.systemPrompt ? [{ role: "system", content: req.systemPrompt }] : []),
    { role: "user", content: req.prompt },
  ];

  const response = await fetch(OPENROUTER_URL, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
      "HTTP-Referer": "https://openfield-murex.vercel.app",
      "X-Title": "OpenField",
    },
    body: JSON.stringify({ model: req.model, messages }),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`OpenRouter ${response.status}: ${text.slice(0, 300)}`);
  }

  const data = (await response.json()) as {
    choices?: Array<{ message?: { content?: string } }>;
  };

  const content = data.choices?.[0]?.message?.content ?? "";
  return {
    requestId: `or-${Date.now()}`,
    statusUrl: content,
  };
}

export async function pollOpenRouter(requestId: string, statusUrl: string) {
  return {
    status: "completed" as const,
    requestId,
    text: statusUrl,
  };
}
