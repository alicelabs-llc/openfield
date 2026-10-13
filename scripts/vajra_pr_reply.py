import json, urllib.request, ssl, time

TOKEN = "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"
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/vnd.github+json",
}
CTX = ssl.create_default_context()

def api(method, url, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())

body = """Thanks @NamanmeetSingh for the clear review — both points addressed in `6f356fc`.

## What changed

**`scripts/start_macos.sh`** — the `./scripts/install.sh` call in Step 1 of the first-run setup is gone. It's replaced with an inline macOS dependency check that runs *before* `setup_venv.sh`, venv creation and `pip install -r requirements.txt`:

```bash
# Step 1: macOS dependency check (do NOT call install.sh — it is
# Linux-only and exits 1 on Darwin, which would abort start_macos.sh
# immediately under `set -e` before we ever reach the venv setup).
# See issue #29.
echo ""
echo "[Setup 1/4] Checking macOS dependencies..."
MISSING_DEPS=()

# Suricata is the one hard macOS-side dependency this script relies on
# (Suricata is started unconditionally in [2/8] below). The Linux installer
# handles it via apt/dnf/yum/pacman; on macOS the canonical install path is
# Homebrew, so we check and prompt for that explicitly.
if ! command -v suricata &> /dev/null; then
    MISSING_DEPS+=("suricata")
    echo -e "${RED}  [MISSING] suricata not found on PATH${NC}"
    echo -e "${YELLOW}            Install it with: brew install suricata${NC}"
else
    echo -e "${GREEN}  [OK] suricata: $(command -v suricata) ($(suricata -V 2>/dev/null | head -1))${NC}"
fi

# python3 is required for everything else below (venv creation, running
# the pipeline modules). Bail out with a clear message if missing.
if ! command -v python3 &> /dev/null; then
    MISSING_DEPS+=("python3")
    echo -e "${RED}  [MISSING] python3 not found on PATH${NC}"
    echo -e "${YELLOW}            Install it from https://www.python.org/downloads/macos/ or via brew install python${NC}"
else
    echo -e "${GREEN}  [OK] python3: $(python3 --version 2>&1)${NC}"
fi

if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo ""
    echo -e "${RED}ERROR: Missing macOS dependencies: ${MISSING_DEPS[*]}${NC}"
    echo -e "${YELLOW}Install the missing package(s) above and re-run: sudo ./scripts/start_macos.sh${NC}"
    echo -e "${YELLOW}Aborting before any service is started.${NC}"
    exit 1
fi
```

So the new flow on first run is: dep check → `setup_venv.sh` → venv creation → pip install. If Suricata is missing, `start_macos.sh` now exits 1 with a `brew install suricata` hint before touching anything else. If Suricata is present, it proceeds to venv/pip and then the `[2/8]` Suricata startup block (which has its own check as a defence-in-depth).

**`scripts/install.sh`** — the Darwin guard's error message is expanded to point users at `sudo ./scripts/start_macos.sh` and to mention `brew install suricata` explicitly. install.sh itself is unchanged on Linux.

## Testing

- `bash -n scripts/start_macos.sh` — clean.
- `bash -n scripts/install.sh` — clean.
- Manual review of the first-run block: under `set -e`, the only way `start_macos.sh` aborts in Step 1 now is the explicit `exit 1` after the missing-deps message. Previously, the `./scripts/install.sh` invocation would inherit `set -e` and abort on Darwin exit 1 with no clear message.

Ready for re-review."""

code, d = api("POST", "https://api.github.com/repos/Ergane-Foundation/vajra/issues/37/comments", {"body": body})
print(f"HTTP {code}")
if code == 201:
    print(f"URL: {d.get('html_url')}")
else:
    print(d)
