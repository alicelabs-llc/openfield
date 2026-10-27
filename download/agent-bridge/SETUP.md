# Agent Bridge — Túnel Seguro para que el sandbox Z.ai corra comandos en tu PC

## Qué es esto

Un servidor HTTP pequeño (solo Python stdlib, sin `pip install`) que corre en
tu PC, escucha **solo en 127.0.0.1** (localhost), y se expone al mundo vía
**Cloudflare Tunnel** (también solo stdlib para el cliente). El sandbox de
Z.ai puede llamarte por HTTPS para ejecutar comandos que **tú autorizás
explícitamente** en la lista blanca (`allowlist` en `config.json`).

No es un shell abierto. Cada comando pasa por:

1. **HMAC-SHA256** con un secret que solo vos y yo conocemos
2. **Timestamp** dentro de una ventana de ±60 segundos (anti-replay)
3. **Nonce** único (cada request solo se acepta una vez)
4. **Allowlist** — solo comandos autorizados (git, python, node, ls, cat, etc.)
5. **Blocklist** — patrones peligrosos rechazados (sudo, rm -rf /, eval, etc.)
6. **Workdir fijo** — solo puede trabajar dentro de la carpeta que definís
7. **Rate limit** — máx 10 comandos por minuto por IP
8. **Kill switch** — creás un archivo `PAUSE` y se apaga todo
9. **Audit log** — cada comando queda registrado con IP, timestamp, output

---

## Instalación (Windows, 10 minutos)

### Paso 1 — Descargá la carpeta `agent-bridge`

Descargá toda la carpeta `/home/z/my-project/download/agent-bridge/` del
sandbox a tu PC. Por ejemplo a:

```
C:\Users\TU_USUARIO\agent-bridge\
```

Deberías ver estos archivos:

- `agent-bridge.py` — el servidor (corre en tu PC)
- `agent-bridge-client.py` — el cliente (corre en mi sandbox)
- `config.json` — tu configuración (editá `workdir` y `secret`)
- `generate-secret.py` — genera un secret nuevo si querés rotarlo
- `SHARED_SECRET.txt` — el secret que ya generé para vos
- `start-bridge.bat` — lanzador de un clic para Windows
- `start-bridge.sh` — lanzador para Mac/Linux
- `SETUP.md` — este archivo

### Paso 2 — Instalá Python 3.10+

Si ya tenés Python, salteá este paso. Si no:

1. Andá a https://www.python.org/downloads/
2. Descargá Python 3.12 (o 3.11)
3. Durante la instalación, **marcá "Add Python to PATH"**
4. Verificá: abrí PowerShell y corré `python --version`

### Paso 3 — Instalá Cloudflare Tunnel (cloudflared)

1. Andá a https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
2. Descargá `cloudflared-windows-amd64.exe` (para Windows 64-bit)
3. Renombralo a `cloudflared.exe` y ponelo en la misma carpeta
   `C:\Users\TU_USUARIO\agent-bridge\`
4. (Opcional) Agregalo al PATH para poder llamarlo de cualquier lado

### Paso 4 — Editá `config.json`

Abrí `config.json` en un editor de texto y cambiá:

```json
{
  "workdir": "C:\\Users\\TU_USUARIO\\alicelabs-work",
  "secret": "rGlJ7O-bqLRfSH8if7-dfMVfK_0FHE936vDIZKKJvJM"
}
```

- **`workdir`**: creá una carpeta de trabajo (ej. `C:\Users\TU_USUARIO\alicelabs-work`)
  y poné esa ruta acá. El sandbox solo va a poder trabajar dentro de esa carpeta.
  No pongas `C:\` ni `C:\Users\TU_USUARIO` — poné una subcarpeta dedicada.
- **`secret`**: ya está lleno con el secret que generé. Si querés rotarlo,
  corré `python generate-secret.py` y pegá el valor nuevo en ambos lados
  (tu `config.json` y mi `SHARED_SECRET.txt`).

### Paso 5 — Corré el bridge

Doble clic en `start-bridge.bat`, o abrí PowerShell y corré:

```powershell
cd C:\Users\TU_USUARIO\agent-bridge
python agent-bridge.py
```

Deberías ver:

```
======================================================================
🔐 AliceLabs agent-bridge v1.0.0
======================================================================
  Listening on:  http://127.0.0.1:7421
  Workdir:       C:\Users\TU_USUARIO\alicelabs-work
  Allowlist:     54 commands
  Blocklist:     40 patterns
  Timeout:       120s per command
  Rate limit:    10 req/min per IP
  Audit log:     agent-bridge.log
======================================================================
```

### Paso 6 — Abrí el túnel

En **otra** terminal de PowerShell (dejá la primera corriendo):

```powershell
cd C:\Users\TU_USUARIO\agent-bridge
.\cloudflared.exe tunnel --url http://localhost:7421
```

Cloudflare te va a imprimir una URL tipo:

```
https://something-random-here.trycloudflare.com
```

**Esa es tu URL pública.** Mandámela por este chat y ya puedo empezar a
llamarte.

### Paso 7 — Probá que funciona

Desde mi lado, cuando me pases la URL, corro:

```bash
curl https://something-random-here.trycloudflare.com/health
```

Y debería responder `{"status":"ok","service":"agent-bridge",...}`.

Después pruebo un comando real:

```bash
python agent-bridge-client.py \
    --url https://something-random-here.trycloudflare.com \
    --secret-file SHARED_SECRET.txt \
    --command "whoami"
```

---

## Instalación en Mac / Linux

Igual que Windows pero:

1. `brew install cloudflared` (Mac) o descargá el binario de Cloudflare
2. Corré `./start-bridge.sh` en vez de `.bat`
3. `cloudflared tunnel --url http://localhost:7421`

---

## Seguridad — qué está protegido y qué no

### Protegido

- **Solo localhost**: nadie puede alcanzarte directamente desde internet.
  Todo pasa por Cloudflare Tunnel, que requiere TLS y solo expone el
  endpoint que vos querés.
- **HMAC + nonce + timestamp**: sin el secret, nadie puede firmar un comando
  válido. El nonce evita que alguien capture una request y la reenvíe.
- **Allowlist estricta**: aunque me robe el secret, solo puedo correr los
  comandos que vos autorizaste. No puedo hacer `sudo`, no puedo editar
  `/etc/passwd`, no puedo instalar servicios.
- **Workdir aislado**: solo puedo leer/escribir dentro de la carpeta que
  definiste. No puedo tocar tus fotos, tus documentos, ni tu sistema.
- **Rate limit**: aunque alguien intente fuerza bruta, está limitado a 10
  intentos por minuto por IP.
- **Audit log completo**: cada comando (aceptado o rechazado) queda
  registrado en `agent-bridge.log` con IP, timestamp, output y código de
  salida. Podés auditar todo lo que hice.
- **Kill switch**: si creás un archivo `PAUSE` en el workdir, dejo de correr
  comandos hasta que lo borres. Útil si querés pausar sin apagar el servidor.

### NO protegido (lo que tenés que entender)

- **El secret es la clave**: si alguien consigue el secret Y la URL del
  túnel, puede correr comandos autorizados. Guardá el secret como una
  contraseña. Rotarlo es gratis (`generate-secret.py`).
- **Cloudflare Tunnel es confiable pero no es mágico**: Cloudflare ve el
  tráfico (HTTPS entre vos y ellos, y entre ellos y mí). No es end-to-end
  encryption entre mi sandbox y tu PC, pero sí TLS en cada hop.
- **Los comandos autorizados pueden hacer cosas reales**: si me permitís
  `rm`, puedo borrar archivos (dentro del workdir). Si me permitís `git
  push`, puedo pushear. Revisá la allowlist y quitá lo que no querés.

### Cómo apagar todo

- **Ctrl+C** en la terminal donde corre `agent-bridge.py`
- **Ctrl+C** en la terminal donde corre `cloudflared`
- Crear un archivo `PAUSE` en el workdir (mantiene el server vivo pero
  rechaza comandos)

---

## Rotación del secret

Cada tanto (una vez al mes, o si sospechás que se filtró):

```bash
python generate-secret.py SHARED_SECRET.txt
```

Pegá el valor nuevo en `config.json` y en mi sandbox (avisanme por el chat).
Reiniciá el bridge. Listo.

---

## Qué comandos me conviene autorizar

**Sí autorizá** (útiles para el trabajo que hacemos):

- `git`, `gh` — para manejar repos, PRs, issues
- `python`, `pip` — para correr scripts
- `node`, `npm` — para TypeScript/JavaScript
- `ls`, `cat`, `grep`, `find` — para explorar archivos
- `mkdir`, `touch`, `cp`, `mv` — para crear/mover archivos
- `curl`, `wget` — para descargar cosas
- `which`, `whoami`, `date`, `hostname` — info del sistema

**Pensalo antes de autorizar** (riesgoso):

- `rm` — borra archivos (recomiendo dejarlo, pero sabé que puedo borrar)
- `pip install` — instala paquetes en tu Python global (preferí venv)
- `npm install -g` — instala paquetes globales
- `curl | sh` — bloqueado por defecto, es el patrón de malware

**No autorices nunca**:

- `sudo`, `su`, `runas`
- Cualquier comando que modifique el sistema operativo
- Comandos que envien tu PC a dormir/apagar
- Herramientas de red como `netsh`, `iptables`, `ufw`

---

## Cómo llamarte desde mi lado

Cuando me pases la URL, yo corro:

```bash
python agent-bridge-client.py \
    --url https://TU-TUNNEL.trycloudflare.com \
    --secret-file SHARED_SECRET.txt \
    --command "git status"
```

Y me devuelve JSON con `stdout`, `stderr`, `exit_code`, `duration_ms`.

---

## Troubleshooting

**"Connection refused" desde mi lado:**
- ¿Está corriendo `agent-bridge.py`? Mirá la terminal.
- ¿Está corriendo `cloudflared tunnel`? Mirá la otra terminal.
- ¿La URL es la correcta? Cloudflare la regenera cada vez que reiniciás
  `cloudflared` (en el modo quick tunnel). Mandame la URL nueva cada vez.

**"401 Invalid signature":**
- ¿El `secret` en `config.json` es el mismo que en mi `SHARED_SECRET.txt`?
- ¿La hora de tu PC está sincronizada? El timestamp tiene que estar dentro
  de ±60s. En Windows: Settings → Time & Language → Sync now.

**"403 Command not in allowlist":**
- Agregá el comando a la lista `allowlist` en `config.json` y reiniciá
  el bridge.

**"403 Blocklist pattern matched":**
- El comando disparó un patrón de seguridad (ej. intentaste `sudo`).
  Es normal. Si es un falso positivo, avisame y ajusto el patrón.

**"429 Rate limit exceeded":**
- Demasiados comandos en 1 minuto. Esperá 60 segundos o subí
  `rate_limit_per_minute` en `config.json`.

---

## Licencia

MIT — hacé lo que querás con esto. Es tu infraestructura.

---

*Generado por el sandbox Z.ai de AliceLabs LLC. Si algo se rompe, avisanme
por el chat y lo arreglamos.*
