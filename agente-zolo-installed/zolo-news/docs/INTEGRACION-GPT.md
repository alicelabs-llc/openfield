# INTEGRACIÓN-GPT.md — Complemento MCP de ZOLO NEWS para GPT o cualquier IA

> **ZOLO NEWS** · noticiero matutino autónomo del agente ZOLO (ecosistema AliceLabs, founder Edison Flores, Ecuador).
> Este documento explica cómo conectar el complemento MCP a Claude Desktop, Cursor, cualquier cliente MCP y (honradamente) a ChatGPT.

---

## 1. Qué es este complemento

Un **servidor MCP estándar sobre stdio** (`@modelcontextprotocol/sdk`), sin HTTP, sin puertos, sin bin entry: se ejecuta con Node.

```bash
cd /home/z/my-project/zolo-news
node src/mcp/server.js          # arranca el servidor (npm run mcp hace lo mismo)
node src/mcp/selftest.js        # prueba de protocolo: debe imprimir "MCP SELFTEST OK"
```

Requisito: **Node ≥ 20** (probado con Node v24). No necesita API keys ni credenciales: lee `config.json` del proyecto y los módulos del núcleo (`src/news.js`, `src/weather.js`, `src/mood.js`, `src/scriptWriter.js`).

### Herramientas (tools) que expone

| Tool | Parámetros | Qué devuelve |
|---|---|---|
| `zolo_get_news` | `limit?: number (1-20, default 6)` · `topic?: string` | Noticias frescas ahora mismo (RSS: Google News Ecuador, BBC Mundo, Infobae, El Universo, El Comercio) en markdown con titular, fuente, fecha y link |
| `zolo_get_weather` | `city?: string` | Clima actual de la ciudad configurada (Guayaquil): temperatura, sensación, condición, máx/mín, lluvia y consejo |
| `zolo_get_bulletin` | `mood?: string` | El boletín completo de HOY: si el agente ya corrió devuelve `output/<fecha>/report.md`; si no, genera uno al vuelo (noticias + clima + curiosidades + guion) |
| `zolo_set_mood` | `mood: string` (requerido) | Configura el tono del boletín de mañana. Valores: `feliz`, `neutral`, `serio`, `motivado`, `bajoneado` |

Todas las respuestas llegan **en español y en markdown**. Si el núcleo aún no está disponible, la tool responde un error útil: `ERROR: núcleo no disponible: <motivo>` (nunca cuelga la sesión del cliente).

---

## 2. (a) Claude Desktop

1. Edita (o crea) el archivo de configuración:
   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
2. Añade el servidor con la **ruta absoluta** de `src/mcp/server.js`:

```json
{
  "mcpServers": {
    "zolo-news": {
      "command": "node",
      "args": ["/home/z/my-project/zolo-news/src/mcp/server.js"]
    }
  }
}
```

3. Reinicia Claude Desktop. Deberías ver el icono de herramientas (martillo 🔨) y dentro del chat el servidor **zolo-news** con sus 4 tools.
4. Pruébale: *"¿Qué noticias frescas hay ahora mismo?"*, *"clima en Guayaquil"*, *"dame el boletín de hoy con humor motivado"*, *"pon el humor en feliz para mañana"*.

> Nota Linux: Claude Desktop oficial no tiene build nativo para Linux; se usa la versión de claude.ai en navegador o un cliente MCP alternativo (Cursor, Zed, Cline…). El fragmento de configuración es idéntico donde exista.

---

## 3. (b) Cursor y cualquier cliente MCP

**Cursor** — crea `.cursor/mcp.json` (global: `~/.cursor/mcp.json`) con el mismo bloque:

```json
{
  "mcpServers": {
    "zolo-news": {
      "command": "node",
      "args": ["/home/z/my-project/zolo-news/src/mcp/server.js"]
    }
  }
}
```

Luego: `Ctrl+Shift+J` → MCP & Integrations → verifica que **zolo-news** aparece habilitado (el Circulito verde).

**Otros clientes MCP stdio** (mismo patrón: `command: node` + `args: [ruta absoluta]`):

| Cliente | Archivo de configuración |
|---|---|
| Windsurf | `~/.codeium/windsurf/mcp_config.json` (bloque `mcpServers`) |
| Zed | `~/.config/zed/settings.json` (clave `context_servers`, con `command`/`args`) |
| VS Code (Copilot agent mode) | `.vscode/mcp.json` (clave `servers`, tipo `stdio`) |
| Cline / Roo Code | settings del plugin → MCP Servers → Add Server (stdio, mismo command/args) |
| Gemini CLI | `~/.gemini/settings.json` (clave `mcpServers`) |

Consejo universal: usa siempre **ruta absoluta** al `server.js` y verifica primero con el selftest:

```bash
cd /home/z/my-project/zolo-news && node src/mcp/selftest.js
```

---

## 4. (c) ChatGPT — explicación honesta

**ChatGPT hoy NO consume MCP de forma nativa para GPTs personalizados.** Lo que ChatGPT soporta son **Actions**: un endpoint **HTTPS** + un **esquema OpenAPI** que defines en el creador de GPTs. Es decir: mientras este servidor MCP viva solo en tu máquina por stdio, ChatGPT no puede llamarlo directamente.

El camino soportado es:

1. **Exponer un adaptador HTTP→MCP detrás de HTTPS.** Opciones (de más simple a más permanente):
   - **ngrok** (para probar 10 minutos): `ngrok http 8787`
   - **Cloudflare Tunnel** (gratis y estable): `cloudflared tunnel --url http://localhost:8787`
   - **VPS + Caddy** (producción): Caddy te da HTTPS automático con 3 líneas de Caddyfile.
2. El adaptador mapea los 4 endpoints HTTP a las 4 tools MCP (mismo contrato; en el futuro es un archivo de ~100 líneas con `@modelcontextprotocol/sdk/client` que habla con `src/mcp/server.js` vía stdio y expone Express/Hono). Endpoints equivalentes: `GET /news`, `GET /weather`, `GET /bulletin`, `POST /mood`.
3. Pegar el esquema OpenAPI de abajo en el GPT Action.

### Esquema OpenAPI 3.1 (copiable en el creador de GPTs → Actions → Schema)

```yaml
openapi: 3.1.0
info:
  title: ZOLO NEWS API
  version: 1.0.0
  description: >
    Noticiero matutino autónomo ZOLO NEWS (agente ZOLO, AliceLabs).
    Noticias frescas, clima de Guayaquil, boletín completo y configuración de tono.
servers:
  - url: https://TU-DOMINIO-O-TUNNEL.example
paths:
  /news:
    get:
      operationId: getNews
      summary: Noticias frescas ahora mismo
      parameters:
        - name: limit
          in: query
          required: false
          schema: { type: integer, minimum: 1, maximum: 20, default: 6 }
        - name: topic
          in: query
          required: false
          schema: { type: string }
      responses:
        '200':
          description: Lista de noticias en markdown con titular, fuente, fecha y link
          content:
            text/markdown:
              schema: { type: string }
  /weather:
    get:
      operationId: getWeather
      summary: Clima actual de la ciudad configurada (Guayaquil)
      parameters:
        - name: city
          in: query
          required: false
          schema: { type: string }
      responses:
        '200':
          description: Clima actual en markdown (temp, condición, máx/mín, lluvia, consejo)
          content:
            text/markdown:
              schema: { type: string }
  /bulletin:
    get:
      operationId: getBulletin
      summary: Boletín completo de hoy del noticiero ZOLO
      parameters:
        - name: mood
          in: query
          required: false
          schema:
            type: string
            enum: [feliz, neutral, serio, motivado, bajoneado]
      responses:
        '200':
          description: Boletín completo en markdown
          content:
            text/markdown:
              schema: { type: string }
  /mood:
    post:
      operationId: setMood
      summary: Configura el tono del boletín de mañana
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [mood]
              properties:
                mood:
                  type: string
                  enum: [feliz, neutral, serio, motivado, bajoneado]
      responses:
        '200':
          description: Confirmación en markdown
          content:
            text/markdown:
              schema: { type: string }
```

> Cuando se despliegue el adaptador, reemplaza `TU-DOMINIO-O-TUNNEL.example` por la URL real. Si se añade autenticación, definir `components.securitySchemes` (API key en header) y configurarla en la sección de Actions del GPT.

---

## 5. (d) Tabla: ¿qué IA soporta MCP hoy?

| Cliente / IA | MCP stdio (este complemento) | Nota |
|---|---|---|
| Claude Desktop (macOS/Windows) | ✅ nativo | `claude_desktop_config.json` (§2) |
| Cursor | ✅ nativo | `.cursor/mcp.json` (§3) |
| Windsurf | ✅ nativo | `mcp_config.json` (§3) |
| Zed | ✅ nativo | `context_servers` (§3) |
| VS Code (Copilot, agent mode) | ✅ nativo | `.vscode/mcp.json` (§3) |
| Cline / Roo Code (VS Code) | ✅ nativo | panel MCP Servers (§3) |
| Gemini CLI | ✅ nativo | `settings.json` (§3) |
| ChatGPT (GPTs/Actions) | ❌ hoy no | Solo Actions HTTP + OpenAPI (§4); revisar anuncios de OpenAI por soporte futuro |
| Cualquier cliente MCP-1.0 | ✅ | Es un servidor stdio estándar (JSON-RPC 2.0) |

*(Estado verificado a la fecha de este documento; los soportes cambian rápido — confirma en la documentación de cada cliente.)*

---

## 6. Solución de problemas

| Síntoma | Causa / solución |
|---|---|
| `ERROR: núcleo no disponible: no se pudo importar ../news.js …` | El núcleo no está construido o falla al cargar. Ejecuta `npm start` (corrida del agente) y reintenta. |
| Las tools tardan ~10 s | Normal: 5 feeds RSS en paralelo con timeout de 10 s; clima consulta Open-Meteo. |
| El boletín dice "generado al vuelo" | Aún no ha corrido la corrida programada de hoy (`npm start` o `npm run schedule`). |
| El cliente no muestra las tools | Verifica ruta absoluta a `server.js`, que `node` esté en PATH, y corre `node src/mcp/selftest.js`. |
| Ruido en la salida | Todo log del servidor va a **stderr**; stdout es exclusivo del protocolo JSON-RPC. |
