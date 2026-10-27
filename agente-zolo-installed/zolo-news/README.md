# 📰 ZOLO NEWS — noticiero matutino autónomo del agente ZOLO

> "Un complemento para GPT o cualquier IA que lea las noticias más frescas al despertar… un avatar que lea las noticias como un noticiero… reportes del clima, cosas curiosas y cómicas dependiendo del humor del usuario." — founder, Task 125

ZOLO NEWS despierta a la hora programada, scrapea la red (RSS en español), consulta el clima, busca curiosidades adaptadas a tu humor, escribe el guion con un LLM, lo locuta con voz, genera las imágenes de cada noticia, ensambla un **video MP4 con avatar presentador** y lo entrega por **correo, Telegram y WhatsApp**. Además expone un **servidor MCP** para que GPT, Claude, Cursor o cualquier IA pregunte por noticias frescas.

## Arquitectura (3 módulos con contratos)

```
zolo-news/
├── agent.js                  ← CLI del agente (run / mood / schedule / status)
├── config.json               ← usuario, ciudad, hora de despertar, feeds, canales
├── src/
│   ├── config.js  news.js  weather.js  curiosities.js  mood.js
│   ├── scriptWriter.js  report.js  scheduler.js      ← NÚCLEO (125-A)
│   ├── media/  index.js tts.js avatar.js images.js video.js  ← MEDIOS (125-B)
│   ├── delivery/ index.js email.js telegram.js whatsapp.js social.js ← ENTREGA (125-C)
│   └── mcp/ server.js selftest.js                     ← COMPLEMENTO GPT/CUALQUIER IA
├── templates/email-template.js   ← HTML del correo (CSS inline)
├── docs/INTEGRACION-GPT.md       ← Claude Desktop, Cursor, ChatGPT Actions (OpenAPI 3.1)
├── docs/CANALES.md               ← Gmail, Telegram, WhatsApp, FB/IG/TikTok paso a paso
├── scripts/install-cron.sh       ← despertar programado con crontab (TZ America/Guayaquil)
├── scripts/ensamblar.mjs         ← ensamblaje por etapas (audio/images/video)
├── assets/                       ← avatar.png + background-studio.png (cacheados)
├── state/                        ← lastRun.json + mood.json (humor persistente)
└── output/<YYYY-MM-DD>/          ← script.json, script.md, report.md, audio/, images/, bulletin.mp4
```

## Uso diario

```bash
cd zolo-news
node agent.js run --dry-run        # prueba rápida: noticias+clima+guion (sin medios)
node agent.js run                  # boletín completo + entrega a canales habilitados
node agent.js mood feliz           # humor del día: feliz|neutral|serio|motivado|bajoneado
node agent.js schedule             # daemon: se despierta solo a wakeTime (config.json)
bash scripts/install-cron.sh       # alternativa: crontab en tu máquina (06:30 por defecto)
node agent.js status               # estado: última corrida, humor, próxima alarma
```

## Complemento para GPT o cualquier IA (MCP)

```bash
node src/mcp/server.js             # servidor MCP stdio
node src/mcp/selftest.js           # verificación del protocolo
```

4 tools en español: `zolo_get_news` (limit/topic) · `zolo_get_weather` · `zolo_get_bulletin` (boletín de hoy o al vuelo) · `zolo_set_mood`. Conéctalo a Claude Desktop, Cursor, Windsurf, Zed o VS Code — instrucciones exactas en `docs/INTEGRACION-GPT.md` (incluye el esquema OpenAPI 3.1 para exponerlo como GPT Action vía HTTPS).

## Canales de entrega

| Canal | Estado | Para activar |
|---|---|---|
| Email (HTML + video adjunto) | ✅ implementado | `docs/CANALES.md` — Gmail App Password |
| Telegram (mensaje + video) | ✅ implementado | `docs/CANALES.md` — @BotFather + chat_id |
| WhatsApp (resumen texto) | ✅ implementado | CallMeBot |
| Facebook / Instagram | 🔜 adaptador listo | Meta Graph API + app review |
| TikTok | 🔜 adaptador listo | Content Posting API + app aprobada |

Edita `config.json → channels` y pon `enabled: true` con tus credenciales.

## Resiliencia (probada con fallos reales)

- Feed RSS muerto → se salta, se reporta en `newsErrors` y el boletín se produce igual.
- Open-Meteo 429 → respaldo wttr.in automático.
- TTS 429 / LLM caído → el run continúa (guion por plantillas de respaldo, medios omitidos con aviso).
- Entrega sin credenciales → skip documentado; NINGÚN canal tumba el run.
- Video final siempre ≈ duración del audio (±0.1s, verificado con ffprobe).

## Ecosistema ZOLO

- Skill instalada en el paquete del agente: `download/agente-zolo/02_skills/noticiero-matutino/SKILL.md`
- Ledger: `download/agente-zolo/06_aprendizaje/FEATURE_REQUESTS.md` → F-009
- Worklog canónico: `/home/z/my-project/worklog.md` → Task 125
- API de imágenes: devuelve JPEG — se normaliza a PNG con ffmpeg (ver skill §6.5)
- drawtext SIEMPRE con `textfile=` + `expansion=none` (tildes y comillas seguras)
