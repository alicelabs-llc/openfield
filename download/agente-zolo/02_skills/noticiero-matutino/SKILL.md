---
name: noticiero-matutino
description: Noticiero personal automatizado de ZOLO (v6.0, maquinaria viva en zolo-news/). Activar cuando el founder pide "noticias al despertar", boletín diario, resumen matutino, o cuando cualquier IA pregunte por noticias frescas vía MCP. Orquesta scraping de RSS en español, clima Open-Meteo, curiosidades según humor, guion LLM, TTS con avatar y video MP4, entrega por correo/Telegram/WhatsApp y servidor MCP (zolo_get_news, zolo_get_weather, zolo_get_bulletin, zolo_set_mood).
---

# Noticiero matutino — ZOLO NEWS (maquinaria viva, Task 125)

El founder pidió: "un complemento para GPT o cualquier IA que lea las noticias más frescas al despertar… un agente que se despierte a la hora programada… un avatar que lea las noticias como un noticiero… reportes del clima, cosas curiosas y cómicas dependiendo del humor del usuario". Esta skill es el protocolo; la maquinaria ejecutable vive en `zolo-news/` del entorno (reclonable/re-zipeable).

## 1. Arquitectura (3 zonas con contratos)

| Módulo | Ruta | Responsabilidad |
|---|---|---|
| Núcleo | `agent.js` + `src/{config,news,weather,curiosities,mood,scriptWriter,report,scheduler}.js` | RSS es → dedupe/rank, clima, curiosidades según mood, guion LLM con fallback, CLI |
| Medios | `src/media/{index,tts,avatar,images,video}.js` | TTS (voz tongtong), avatar IA cacheado, imágenes por noticia, MP4 1280x720 con captions (ffmpeg) |
| Entrega + MCP | `src/delivery/*` + `src/mcp/server.js` | Email HTML, Telegram, WhatsApp (CallMeBot), stubs FB/IG/TikTok; 4 tools MCP |

Contrato del guion (secciones): `{kind: intro|news|weather|curious|outro, title?, text ≤600, source?, url?, imagePrompt?, caption? ≤90}` — el text ≤600 existe por el límite TTS de 1024 chars.

## 2. Comandos de operación

```bash
cd zolo-news
node agent.js run --dry-run      # prueba sin medios ni entrega (RSS+clima+guion)
node agent.js run --no-deliver   # boletín completo SIN enviar (TTS+avatar+video)
node agent.js run                # boletín completo + entrega a canales habilitados
node agent.js mood feliz         # fija el humor del día (feliz|neutral|serio|motivado|bajoneado)
node agent.js schedule           # daemon: despierta a la hora programada (config wakeTime, TZ America/Guayaquil)
node agent.js status             # última corrida + humor actual
node src/mcp/server.js           # complemento MCP para GPT o cualquier IA (stdio)
node src/mcp/selftest.js         # verificación del protocolo MCP
```

## 3. El despertar programado (flota 24/7, reel 2 del founder)

El modo `schedule` materializa el patrón de la mesa de bots 24/7: ZOLO despierta a la hora programada, produce el boletín y entrega; el flag anti-solape es el "escéptico con veto" que impide corridas duplicadas. Para reloj del sistema (en la máquina del founder, no en el sandbox): `scripts/install-cron.sh` añade la entrada crontab con TZ America/Guayaquil. Resiliencia probada: feed RSS muerto → se salta y reporta; Open-Meteo 429 → respaldo wttr.in; TTS 429 → el run continúa sin audio; LLM caído → guion por plantillas; entrega sin credenciales → skip documentado. NINGÚN componente opcional tumba el run.

## 4. Humor adaptativo (mood)

- `state/mood.json` manda > `config.mood.current` > `config.mood.default`.
- El mood cambia el guion (intro, chiste, frase) Y el TTS puede ajustar speed (bajoneado → 0.95 más calmado).
- Sin conexión al LLM: chistes/frases estáticas por mood (5 bancos de fallback).

## 5. Complemento para GPT o cualquier IA (reel 3 del founder)

El servidor MCP expone 4 tools en español: `zolo_get_news` (limit/topic), `zolo_get_weather`, `zolo_get_bulletin` (boletín de hoy o generado al vuelo), `zolo_set_mood`. Configuración en Claude Desktop / Cursor / Windsurf / Zed / VS Code: ver `zolo-news/docs/INTEGRACION-GPT.md` (incluye esquema OpenAPI 3.1 para cuando ChatGPT Actions consuma el puente HTTPS). Canales y credenciales: `zolo-news/docs/CANALES.md`.

## 6. Reglas de oro de esta maquinaria

1. **Números vivos**: feeds verificados antes de afirmar (los muertos se quitan de config o se saltan con log).
2. **Feeds vivos al 24-oct-2026**: Google News Ecuador, Google News Tecnología, BBC Mundo, France24 Español, eJu.tv. Muertos: Infobae (404), El Universo (404), El Comercio (anti-bot).
3. **El avatar y el fondo de estudio se cachean** en `assets/` — regenerar solo si falta.
4. **drawtext SIEMPRE con textfile= + expansion=none** (tildes/comillas seguras).
5. La API de imágenes devuelve JPEG con contrato PNG — normalizar firma con ffmpeg antes de usar.

## Grader (v6.0 — añadido por regla 32)

- `node agent.js run --dry-run` termina con artefactos en output/<fecha>/ y lastRun.json actualizado → PASS.
- Un feed muerto no tumba el run (aparece en newsErrors y el boletín se produce) → PASS. Un feed muerto aborta → FAIL grave.
- `node src/mcp/selftest.js` imprime MCP SELFTEST OK → PASS.
- Cambio de mood vía CLI/ MCP se refleja en el siguiente guion → PASS.
- Video final ≈ duración del audio (±1s) con captions legibles y sin caracteres rotos → PASS.
