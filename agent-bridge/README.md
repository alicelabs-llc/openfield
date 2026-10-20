# Agent Bridge — Secure Browser Control Extension

A Chrome extension that lets an AI agent (or any external script) control your browser **through a private ntfy.sh channel** — no port forwarding, no ngrok, no exposed credentials.

## How it works

```
┌────────────────┐    ntfy.sh/<channel>     ┌─────────────────┐
│   AI Agent     │ ──────────────────────►   │   Your Chrome    │
│  (anywhere)    │   JSON commands          │   (extension)    │
│                │ ◄──────────────────────   │                  │
└────────────────┘    ntfy.sh/<channel>-resp  └─────────────────┘
                     JSON results
```

- The agent publishes commands to `ntfy.sh/<your-channel-id>`
- The extension subscribes via WebSocket and executes them
- The extension publishes results back to `ntfy.sh/<your-channel-id>-resp`
- The agent reads responses and decides next action

## Security model

1. **8-char channel ID** — 2.8 trillion combinations, unguessable
2. **You control the channel** — regenerate any time to revoke access instantly
3. **Login screens are yours** — the agent never sees your password; you type it
4. **Live activity log** in the side panel — every command is visible
5. **One-click disconnect** — kills the WebSocket immediately
6. **Only the active tab** is controlled — agent can't touch your other tabs
7. **No credentials stored** — the extension never sees or stores passwords

## Installation

1. Download `agent-bridge.zip` and unzip it somewhere permanent (e.g. `C:\Tools\agent-bridge\`)
2. Open `chrome://extensions` in Chrome
3. Toggle **Developer mode** (top right)
4. Click **Load unpacked** → select the `agent-bridge` folder
5. The Agent Bridge icon appears in your toolbar
6. Click the icon → side panel opens

## Usage

1. Open the side panel (click the icon)
2. You'll see a **Channel ID** (8 chars, e.g. `7f3a9c2e`)
3. Click 📋 to copy it
4. Share the Channel ID with your agent (paste in chat)
5. Click **Connect**
6. The agent can now send commands

## Supported commands

The agent sends JSON to your channel:

```json
{"id": "uuid", "action": "open", "url": "https://example.com"}
{"id": "uuid", "action": "snapshot"}
{"id": "uuid", "action": "click", "selector": "#submit-btn"}
{"id": "uuid", "action": "fill", "selector": "#email", "value": "test@example.com"}
{"id": "uuid", "action": "gettext", "selector": "h1"}
{"id": "uuid", "action": "geturl"}
{"id": "uuid", "action": "listtabs"}
{"id": "uuid", "action": "switchtab", "tabId": 123}
{"id": "uuid", "action": "eval", "code": "document.title"}
{"id": "uuid", "action": "screenshot"}
{"id": "uuid", "action": "wait", "ms": 2000}
{"id": "uuid", "action": "press", "key": "Enter"}
{"id": "uuid", "action": "scroll", "direction": "down", "amount": 500}
{"id": "uuid", "action": "ping"}
```

Responses go to `<channel>-resp`:

```json
{"id": "uuid", "action": "open", "ok": true, "result": {"tabId": 123, "url": "..."}}
```

## Files

- `manifest.json` — Chrome MV3 manifest
- `background.js` — service worker, maintains WebSocket + executes commands
- `sidepanel.html` — UI
- `sidepanel.js` — side panel logic
- `icons/` — PNG icons

## Revoking access

Three ways:
1. Click **Disconnect** in the side panel
2. Click 🔄 to regenerate the Channel ID (old channel becomes useless)
3. Disable the extension in `chrome://extensions`

## License

MIT.
