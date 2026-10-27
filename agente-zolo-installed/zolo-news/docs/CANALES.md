# CANALES.md — Entrega multicanal de ZOLO NEWS

> **ZOLO NEWS** · noticiero matutino autónomo del agente ZOLO (AliceLabs · founder Edison Flores · Ecuador).
> Cómo pasar cada canal de `enabled: false` a funcionando, con ejemplos de `config.json` rellenados.

Estado de los canales (ver `config.json`):

| Canal | Estado | Motor |
|---|---|---|
| 📧 Email | listo (requiere App Password) | SMTP + nodemailer (`src/delivery/email.js`) |
| ✈️ Telegram | listo (requiere token del bot) | Bot API oficial (`src/delivery/telegram.js`) |
| 💬 WhatsApp | listo (requiere apikey CallMeBot) | CallMeBot (`src/delivery/whatsapp.js`) |
| 📘 Facebook | adaptador preparado, requiere tokens | Meta Graph API (`src/delivery/social.js`) |
| 📸 Instagram | adaptador preparado, requiere tokens | Instagram Graph API (`src/delivery/social.js`) |
| 🎵 TikTok | adaptador preparado, requiere app aprobada | Content Posting API (`src/delivery/social.js`) |

Mientras Facebook/Instagram/TikTok no tengan tokens, el boletín ya llega completo por **email / Telegram / WhatsApp**.

---

## 1. 📧 Gmail por SMTP con App Password

**Paso a paso (10 min):**

1. Entra a tu cuenta Google → **Gestión de tu cuenta de Google** → **Seguridad**.
2. Activa la **verificación en 2 pasos** (obligatoria para App Passwords).
3. Ve a https://myaccount.google.com/apppasswords → nombre "ZOLO NEWS" → **Crear**.
4. Google te da una contraseña de 16 caracteres (p. ej. `abcd efgh ijkl mnop`). Cópiala SIN espacios.
5. Rellena `config.json` (Gmail usa `smtp.gmail.com:465` con TLS implícito → `secure: true`):

```json
"email": {
  "enabled": true,
  "smtp": {
    "host": "smtp.gmail.com",
    "port": 465,
    "secure": true,
    "user": "edison@gmail.com",
    "pass": "abcdEfghIjklMnop"
  },
  "to": "edison@gmail.com"
}
```

6. Prueba sin esperar al run completo:

```bash
cd /home/z/my-project/zolo-news
node --input-type=module -e "
import('./src/delivery/email.js').then(async m => {
  const fs = (await import('node:fs')).default;
  const cfg = JSON.parse(fs.readFileSync('config.json','utf8'));
  const r = await m.sendEmail(cfg.channels.email, {subject:'ZOLO prueba', html:'<p>Boletín de prueba ✅</p>'});
  console.log(JSON.stringify(r, null, 2));
});"
```

Notas: la App Password es lo único que va en `pass` (no tu contraseña normal). Si Gmail rechaza el login, revisa 2FA activo y que la App Password siga vigente. `to` puede ser otra dirección distinta del remitente.

---

## 2. ✈️ Telegram con @BotFather

1. Habla con **@BotFather** en Telegram → `/newbot` → nombre (p. ej. "ZOLO Noticias") y username que termine en `bot` (p. ej. `zolo_noticias_bot`).
2. BotFather responde con el **token** (formato `123456789:AAExxxxxxxxxxxxxxxxxxxxxxxxxxxx`).
3. Obtén tu `chat_id`: **mándale cualquier mensaje a tu bot** (p. ej. "hola") y luego:

```bash
curl "https://api.telegram.org/bot<TU_TOKEN>/getUpdates"
```

Busca en la respuesta `"chat":{"id": 123456789, ...}` → ese número es tu `chat_id`. (Para un canal/grupo: añade el bot al grupo y usa el id negativo `-100...`.)

4. Rellena `config.json`:

```json
"telegram": {
  "enabled": true,
  "botToken": "123456789:AAExxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "chatId": "123456789"
}
```

5. Prueba:

```bash
node --input-type=module -e "
import('./src/delivery/telegram.js').then(async m => {
  const fs = (await import('node:fs')).default;
  const cfg = JSON.parse(fs.readFileSync('config.json','utf8'));
  const r = await m.sendTelegram(cfg.channels.telegram, {message:'<b>ZOLO</b> prueba ✅'});
  console.log(JSON.stringify(r, null, 2));
});"
```

Notas: el boletín se envía con `parse_mode: HTML` (el orquestador ya escapa el contenido). Si hay video (`bulletin.mp4` < 50 MB), se envía después con `sendDocument` (FormData + Blob nativos). El mensaje soporta hasta 4096 chars; el resumen se recorta a 4000 por seguridad.

---

## 3. 💬 WhatsApp con CallMeBot

CallMeBot es una API gratuita personal (solo puede mandarte mensajes a TI mismo).

1. Desde tu WhatsApp, guarda el contacto **+34 644 51 95 23** (número de activación de CallMeBot).
2. Envíale EXACTAMENTE este mensaje: `I allow callmebot to send me messages`
3. En ~2 minutos recibes una respuesta con tu **apikey** (formato `123456`).
4. Rellena `config.json` (teléfono en formato internacional, solo dígitos, SIN `+`):

```json
"whatsapp": {
  "enabled": true,
  "phone": "593991234567",
  "apikey": "123456"
}
```

5. Prueba:

```bash
node --input-type=module -e "
import('./src/delivery/whatsapp.js').then(async m => {
  const fs = (await import('node:fs')).default;
  const cfg = JSON.parse(fs.readFileSync('config.json','utf8'));
  const r = await m.sendWhatsApp(cfg.channels.whatsapp, {message:'ZOLO prueba ✅'});
  console.log(JSON.stringify(r, null, 2));
});"
```

> Verifica el número/texto de activación vigente en https://www.callmebot.com/blog/free-api-whatsapp-messages/ — CallMeBot puede cambiar el proceso. Límite práctico: mensajes de texto corto (el boletín va recortado a ≤ 800 chars por diseño).

---

## 4. 📘 Facebook oficial (Meta Graph API)

Requiere una app de Meta con revisión de permisos (App Review). Mientras tanto `social.js` devuelve `{channel:'facebook', status:'necesita_configuracion'}` y NO llama a ninguna API.

1. https://developers.facebook.com → **My Apps → Create App** (tipo *Business*).
2. Añade el producto **Facebook Login for Business** (o *Facebook Graph API* según el flujo).
3. Con **Graph API Explorer** (Tools → Graph API Explorer): genera un **User Token** y pídelo con permisos `pages_show_list`, `pages_read_engagement`, `pages_manage_posts`.
4. Convierte el User Token en **Page Access Token**: `GET /me/accounts?access_token=<user_token>` → copia el `access_token` de tu página (ese es el Page Token de larga duración al hacer el exchange `fb_exchange_token`).
5. Copia el **ID de la página** (`GET /me/accounts` también lo devuelve).
6. Rellena `config.json`:

```json
"facebook": {
  "enabled": true,
  "pageId": "123456789012345",
  "pageToken": "EAAG...page-access-token...",
  "note": "Token vencimiento largo; renovar o automatizar exchange"
}
```

7. Con el token presente, `social.js` marca el canal como `pendiente_implementacion`: la llamada exacta ya está documentada dentro del archivo (marcada con `FUTURO`) — es un `POST https://graph.facebook.com/v21.0/{page-id}/feed` con `message` + `access_token`.
8. **App Review**: para que el token no expire y el permiso sea permanente, somete la app a revisión con uso justificado de `pages_manage_posts`.

---

## 5. 📸 Instagram oficial (Instagram Graph API)

Requisito duro: cuenta de **Instagram profesional (Business)** vinculada a una página de Facebook.

1. Convierte la cuenta: Instagram → Configuración → *Cambiar a cuenta profesional*.
2. En la app de Meta del paso anterior añade el producto **Instagram Graph API**.
3. Permisos a solicitar en el App Review: `instagram_content_publish`, `instagram_basic`, `pages_show_list`.
4. Obtén el **IG User ID** y el token: `GET /me/accounts?fields=instagram_business_account&access_token=<page_token>` → `instagram_business_account.id` es tu `igUserId`.
5. Rellena `config.json`:

```json
"instagram": {
  "enabled": true,
  "igUserId": "17841400000000000",
  "igToken": "EAAG...token-con-instagram_content_publish...",
  "note": "Publicación en 2 pasos: media container → media_publish"
}
```

6. El flujo real (documentado con `FUTURO` en `social.js`): `POST /{ig-user-id}/media` (con `image_url` público y `caption`) → devuelve `creation_id` → `POST /{ig-user-id}/media_publish` con ese id. La imagen del boletín tendría que servirse por HTTPS público (p. ej. R2 de Cloudflare) porque Instagram exige URL pública.

---

## 6. 🎵 TikTok oficial (Content Posting API)

1. https://developers.tiktok.com → **Manage apps → Connect** → crea la app.
2. Añade el producto **Content Posting API** (requiere verificación de identidad y, para publicar en cuenta real, aprobación de la app; se empieza en *sandbox*).
3. Permisos: `video.upload`, `video.publish`. Genera el **access token** (OAuth del usuario dueño de la cuenta).
4. Rellena `config.json`:

```json
"tiktok": {
  "enabled": true,
  "accessToken": "act.xxxxxxxxxxxxxxxx",
  "note": "Content Posting API; sandbox primero (audience SELF_ONLY)"
}
```

5. El flujo real (documentado con `FUTURO` en `social.js`): `POST https://open.tiktokapis.com/v2/post/publish/video/init/` con `source_info` tipo `FILE_UPLOAD` → TikTok devuelve URL de upload → `PUT` del `bulletin.mp4` (≤ 64 MB, el boletín cabe). En sandbox los videos quedan privados (`SELF_ONLY`) hasta aprobación.

---

## 7. Ejemplo completo de `config.json` con canales rellenados

```json
{
  "user": { "name": "Edison", "language": "es" },
  "city": { "name": "Guayaquil", "lat": -2.1894, "lon": -79.8891, "timezone": "America/Guayaquil" },
  "wakeTime": "06:30",
  "mood": { "default": "neutral", "allowed": ["feliz", "neutral", "serio", "motivado", "bajoneado"] },
  "news": { "maxItems": 6, "feeds": [] },
  "tts": { "voice": "tongtong", "speed": 1.0 },
  "video": { "width": 1280, "height": 720, "font": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" },
  "features": { "onThisDay": true, "joke": true, "quote": true, "crypto": true },
  "channels": {
    "email": {
      "enabled": true,
      "smtp": { "host": "smtp.gmail.com", "port": 465, "secure": true, "user": "edison@gmail.com", "pass": "abcdEfghIjklMnop" },
      "to": "edison@gmail.com"
    },
    "telegram": {
      "enabled": true,
      "botToken": "123456789:AAExxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      "chatId": "123456789"
    },
    "whatsapp": {
      "enabled": true,
      "phone": "593991234567",
      "apikey": "123456"
    },
    "facebook": {
      "enabled": false,
      "pageId": "123456789012345",
      "pageToken": "",
      "note": "Requiere Meta Graph API (pagina + token). Ver docs/CANALES.md"
    },
    "instagram": {
      "enabled": false,
      "igUserId": "",
      "igToken": "",
      "note": "Requiere Instagram Graph API (cuenta business). Ver docs/CANALES.md"
    },
    "tiktok": {
      "enabled": false,
      "accessToken": "",
      "note": "Requiere TikTok Content Posting API (app aprobada). Ver docs/CANALES.md"
    }
  }
}
```

⚠️ **Seguridad**: `config.json` con credenciales reales NO debe subirse a repos públicos. Considera mover los secretos a variables de entorno antes de versionar el proyecto.

---

## 8. Reglas de skip (implementadas en `src/delivery/`)

| Situación | Resultado |
|---|---|
| `enabled !== true` en el canal | `{sent:false, skipped:true, info:'...no configurado — ver docs/CANALES.md'}` |
| Credenciales placeholder (`TU_CORREO`, `APP_PASSWORD`, `TOKEN_DEL_BOT`, `TU_CHAT_ID`, `CLAVE_CALLMEBOT`, teléfono con `X`) | mismo skip |
| Adjunto > 25 MB (email) o > 50 MB (Telegram) | se OMITE el adjunto y se anota en `info`; el texto sí se envía |
| Cualquier excepción de red/API | `{sent:false, error:'<motivo>'}` — **`deliverAll` NUNCA lanza** |

Verificación integral (todo debe salir skipped sin excepciones, con canales por defecto):

```bash
cd /home/z/my-project/zolo-news
node --input-type=module -e "import('./src/delivery/index.js').then(async m=>{const r=await m.deliverAll({reportMd:'prueba', sections:[], cfg:JSON.parse((await import('fs')).default.readFileSync('config.json','utf8'))}); console.log(JSON.stringify(r,null,2))})"
```
