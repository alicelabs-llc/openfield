#!/usr/bin/env python3
"""
agent-bridge.py — Secure agent bridge for AliceLabs LLC.

Listens on 127.0.0.1:7421 and executes a RESTRICTED set of commands
when called via HTTPS through a Cloudflare Tunnel (or any reverse
proxy). Designed to be used by Edison Flores Guerra to let the
AliceLabs sandbox (Z.ai agent) run specific commands on this PC
without exposing a raw shell to the internet.

Security model:
  1. Binds to 127.0.0.1 ONLY — no direct internet exposure.
  2. Exposed via `cloudflared tunnel --url http://localhost:7421`.
  3. Every request must carry:
       - X-Bridge-Timestamp: ISO 8601 UTC, valid within ±60s window
       - X-Bridge-Nonce:     unique UUID4, tracked for 5 min (anti-replay)
       - X-Bridge-Signature: HMAC-SHA256(secret, timestamp + nonce + body)
  4. Command allowlist: only the first token of the command is matched
     against the allowlist in config.json. Anything else is refused.
  5. Blocklist: regex patterns that refuse dangerous constructs even
     if the first token is allowlisted (rm -rf /, sudo, eval, etc.).
  6. Working directory: fixed to WORKDIR in config.json. Commands run
     inside it. Absolute paths outside WORKDIR are refused by default
     (unless ALLOW_ABSOLUTE_PATHS is true).
  7. Timeout: max 300 seconds per command (configurable).
  8. Output size: max 1 MB (truncated).
  9. Rate limit: max MAX_REQUESTS_PER_MINUTE per source IP.
  10. Audit log: JSON lines to agent-bridge.log. Every request is
      logged — even rejected ones — with source IP, command, and
      reason for refusal.
  11. Kill switch: if a file named PAUSE exists in the working
      directory, all commands are refused until it is removed.

Run:
    python agent-bridge.py            # loads config.json from same dir
    python agent-bridge.py --config /path/to/config.json

Then, in a second terminal, expose it via Cloudflare Tunnel:
    cloudflared tunnel --url http://localhost:7421

The tunnel prints a URL like https://xyz.trycloudflare.com — send that
URL to Edison so he can call it from the Z.ai sandbox.

Requires: Python 3.10+ (stdlib only — no pip installs needed).
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import logging
import os
import re
import socket
import subprocess
import sys
import threading
import time
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_PORT = 7421
DEFAULT_CONFIG_PATH = Path(__file__).parent / "config.json"
MAX_BODY_BYTES = 1 * 1024 * 1024          # 1 MB request body
MAX_OUTPUT_BYTES = 1 * 1024 * 1024        # 1 MB response output
TIMESTAMP_WINDOW_SECONDS = 60             # request clock skew allowed
NONCE_TTL_SECONDS = 300                   # 5 min nonce memory
DEFAULT_TIMEOUT_SECONDS = 120
MAX_TIMEOUT_SECONDS = 300
DEFAULT_RATE_LIMIT = 10                   # commands per minute per IP

LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"

# Patterns that, if found anywhere in the command string, cause refusal.
DEFAULT_BLOCKLIST_PATTERNS: list[str] = [
    r"\bsudo\b",
    r"\bsu\s+-\b",
    r"\beval\b",
    r"\bexec\s*\(",
    r"rm\s+-rf\s+[~/]",
    r"rm\s+-rf\s+/",
    r"rm\s+-rf\s+\*",
    r":\(\)\s*\{\s*:\|:&\s*\};:",
    r"\bmkfs\b",
    r"\bdd\s+if=",
    r"\bformat\s+[A-Z]:",
    r"\bdel\s+/[fsq]",
    r"\brd\s+/s\b",
    r"\bshutdown\b",
    r"\breboot\b",
    r"\bpoweroff\b",
    r"\bhalt\b",
    r"\bpasswd\b",
    r"\buseradd\b",
    r"\buserdel\b",
    r"\busermod\b",
    r"\bchown\b",
    r"chmod\s+777\s+/",
    r"\bkillall\b",
    r"\bpkill\b",
    r"taskkill\s+/f",
    r"curl[^|]*\|\s*(ba)?sh",
    r"wget[^|]*\|\s*(ba)?sh",
    r"curl[^|]*-o\s*/etc",
    r"/etc/(passwd|shadow|sudoers)",
    r"\bssh-keygen\b",
    r"\bssh-copy-id\b",
    r"\bnc\s+-l\b",
    r"\bnetcat\b",
    r"\bnslookup\b.*-type=any",
    r"\biptables\b",
    r"\bufw\b",
    r"\bnetsh\b",
    r"\breg\s+add\b",
    r"\bschtasks\b",
    r"\bcrontab\b",
    r"\bat\s+\d",
    r"\bsystemctl\s+(start|stop|restart|enable|disable)",
    r"\bservice\s+(start|stop|restart)",
    # Git destructive
    r"git\s+push\s+.*--force",
    r"git\s+push\s+-f\b",
    r"git\s+reset\s+--hard\s+origin",
    r"git\s+clean\s+-fdx",
    r"git\s+filter-branch",
    r"git\s+branch\s+-D\b",
    r"git\s+remote\s+remove",
]

# Default command allowlist (first token). Override in config.json.
DEFAULT_ALLOWLIST: list[str] = [
    # Source control
    "git", "gh", "glab",
    # Interpreters
    "python", "python3", "pip", "pip3", "node", "npm", "npx", "pnpm", "yarn", "bun",
    "deno", "tsx", "ts-node",
    # Filesystem read
    "ls", "dir", "cat", "type", "head", "tail", "grep", "find", "rg", "fd",
    "wc", "sort", "uniq", "stat", "file", "du", "df",
    # Filesystem write (safe operations only)
    "mkdir", "touch", "cp", "copy", "mv", "move", "rm", "del",
    # Archive
    "tar", "zip", "unzip", "7z",
    # Network
    "curl", "wget", "ping", "nslookup", "traceroute", "tracert",
    # System info (read-only)
    "which", "where", "whoami", "hostname", "date", "uname", "systeminfo",
    "tasklist", "ps", "top", "uptime", "env", "printenv",
    # Text processing
    "awk", "sed", "cut", "tr", "tee", "jq", "yq",
    # Build tools
    "make", "cmake", "cargo", "go", "rustc", "javac", "java", "dotnet",
]


# ---------------------------------------------------------------------------
# Audit log
# ---------------------------------------------------------------------------

class AuditLogger:
    """JSON-lines audit logger. Writes one JSON object per line."""

    def __init__(self, log_path: Path):
        self.log_path = log_path
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def write(self, event: dict[str, Any]) -> None:
        event["ts"] = datetime.now(timezone.utc).isoformat()
        line = json.dumps(event, ensure_ascii=False, default=str)
        with self._lock:
            with self.log_path.open("a", encoding="utf-8") as f:
                f.write(line + "\n")


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

class Config:
    """Loads and validates config.json."""

    def __init__(self, config_path: Path):
        if not config_path.exists():
            raise FileNotFoundError(
                f"Config not found: {config_path}\n"
                "Create a config.json next to agent-bridge.py. "
                "See SETUP.md for a template."
            )
        raw = json.loads(config_path.read_text(encoding="utf-8"))

        self.secret_b64 = raw.get("secret")
        if not self.secret_b64:
            raise ValueError(
                "Missing 'secret' in config.json. "
                "Generate one with: python generate-secret.py"
            )
        # Accept both raw base64url (no padding) and padded
        padded = self.secret_b64 + "=" * (-len(self.secret_b64) % 4)
        self.secret = base64.urlsafe_b64decode(padded.encode())

        self.port = int(raw.get("port", DEFAULT_PORT))
        self.host = raw.get("host", "127.0.0.1")  # only 127.0.0.1 is safe
        if self.host not in ("127.0.0.1", "localhost"):
            raise ValueError(
                f"Refusing to bind to {self.host}. "
                "agent-bridge must only listen on 127.0.0.1 — "
                "use Cloudflare Tunnel for internet exposure."
            )

        workdir = Path(raw.get("workdir", Path.cwd())).expanduser().resolve()
        if not workdir.exists():
            raise FileNotFoundError(f"workdir does not exist: {workdir}")
        self.workdir = workdir

        self.allowlist = set(raw.get("allowlist", DEFAULT_ALLOWLIST))
        self.blocklist = [
            re.compile(p, re.IGNORECASE)
            for p in raw.get("blocklist", DEFAULT_BLOCKLIST_PATTERNS)
        ]
        self.allow_absolute_paths = bool(raw.get("allow_absolute_paths", False))
        self.allow_outside_workdir = bool(raw.get("allow_outside_workdir", False))
        self.default_timeout = min(
            int(raw.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS)),
            MAX_TIMEOUT_SECONDS,
        )
        self.rate_limit_per_minute = int(
            raw.get("rate_limit_per_minute", DEFAULT_RATE_LIMIT)
        )
        self.max_output_bytes = int(raw.get("max_output_bytes", MAX_OUTPUT_BYTES))
        self.log_path = Path(
            raw.get("log_path", Path(__file__).parent / "agent-bridge.log")
        )


# ---------------------------------------------------------------------------
# Security helpers
# ---------------------------------------------------------------------------

class RateLimiter:
    """Sliding-window rate limiter keyed by source IP."""

    def __init__(self, limit_per_minute: int):
        self.limit = limit_per_minute
        self.requests: dict[str, list[float]] = {}
        self._lock = threading.Lock()

    def allow(self, ip: str) -> bool:
        now = time.time()
        with self._lock:
            window = self.requests.setdefault(ip, [])
            # Drop entries older than 60s
            window[:] = [t for t in window if now - t < 60]
            if len(window) >= self.limit:
                return False
            window.append(now)
            return True


class NonceStore:
    """Tracks recently seen nonces to prevent replay attacks."""

    def __init__(self, ttl_seconds: int):
        self.ttl = ttl_seconds
        self.seen: dict[str, float] = {}
        self._lock = threading.Lock()

    def is_fresh(self, nonce: str) -> bool:
        now = time.time()
        with self._lock:
            # Purge expired
            self.seen = {n: t for n, t in self.seen.items() if now - t < self.ttl}
            if nonce in self.seen:
                return False
            self.seen[nonce] = now
            return True


def verify_signature(secret: bytes, timestamp: str, nonce: str,
                     body: bytes, signature: str) -> bool:
    """Verify HMAC-SHA256(secret, timestamp + '.' + nonce + '.' + body)."""
    payload = timestamp.encode("utf-8") + b"." + nonce.encode("utf-8") + b"." + body
    expected = hmac.new(secret, payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def parse_timestamp(ts: str) -> datetime | None:
    """Parse ISO 8601 UTC timestamp. Returns None on failure."""
    try:
        # Handle both 'Z' suffix and explicit offset
        if ts.endswith("Z"):
            ts = ts[:-1] + "+00:00"
        dt = datetime.fromisoformat(ts)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (ValueError, AttributeError):
        return None


def is_timestamp_fresh(dt: datetime, window_seconds: int) -> bool:
    """Check that the timestamp is within ±window_seconds of now."""
    now = datetime.now(timezone.utc)
    delta = abs((now - dt).total_seconds())
    return delta <= window_seconds


def check_path_safety(command: str, workdir: Path,
                      allow_outside: bool) -> tuple[bool, str]:
    """Refuse absolute paths outside WORKDIR if not explicitly allowed."""
    if allow_outside:
        return True, ""
    # Look for absolute paths (Unix: /foo, Windows: C:\foo or C:/foo)
    abs_paths = re.findall(r'(?<!\w)(/[A-Za-z0-9_\-\.][^\s"\';&|]*)', command)
    win_paths = re.findall(r'(?<!\w)([A-Z]:\\[^\s"\';&|]*)', command)
    all_paths = abs_paths + win_paths
    for p in all_paths:
        try:
            resolved = Path(p).resolve()
            # Allow paths inside workdir
            resolved.relative_to(workdir)
        except (ValueError, OSError):
            return False, f"Path outside workdir refused: {p}"
    return True, ""


def check_blocklist(command: str, patterns: list[re.Pattern]) -> tuple[bool, str]:
    """Refuse if any blocklist pattern matches the command string."""
    for pattern in patterns:
        m = pattern.search(command)
        if m:
            return False, f"Blocklist pattern matched: {pattern.pattern}"
    return True, ""


def check_allowlist(command: str, allowlist: set[str]) -> tuple[bool, str]:
    """Refuse if the first token is not in the allowlist."""
    tokens = command.strip().split()
    if not tokens:
        return False, "Empty command"
    first = tokens[0].lower()
    # Strip path prefix (e.g. /usr/bin/git -> git)
    first = first.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
    # Strip Windows .exe suffix
    if first.endswith(".exe"):
        first = first[:-4]
    if first not in allowlist:
        return False, f"Command '{first}' not in allowlist"
    return True, ""


# ---------------------------------------------------------------------------
# Command execution
# ---------------------------------------------------------------------------

def execute_command(command: str, cfg: Config) -> dict[str, Any]:
    """Run a command in cfg.workdir, with timeout, and capture output."""
    # Safety checks
    ok, reason = check_allowlist(command, cfg.allowlist)
    if not ok:
        return {"allowed": False, "reason": reason}

    ok, reason = check_blocklist(command, cfg.blocklist)
    if not ok:
        return {"allowed": False, "reason": reason}

    ok, reason = check_path_safety(command, cfg.workdir,
                                    cfg.allow_outside_workdir)
    if not ok:
        return {"allowed": False, "reason": reason}

    # Kill switch
    pause_file = cfg.workdir / "PAUSE"
    if pause_file.exists():
        return {
            "allowed": False,
            "reason": f"Kill switch active: {pause_file} exists. "
                      "Remove it to resume command execution."
        }

    # Execute
    started = time.monotonic()
    try:
        proc = subprocess.run(
            command,
            shell=True,  # allowlist + blocklist are our defense; cwd is fixed
            cwd=cfg.workdir,
            timeout=cfg.default_timeout,
            capture_output=True,
            text=True,
            env={**os.environ, "BRIDGE": "1"},  # mark subprocesses
        )
        duration_ms = int((time.monotonic() - started) * 1000)

        stdout = proc.stdout or ""
        stderr = proc.stderr or ""
        if len(stdout.encode("utf-8", errors="replace")) > cfg.max_output_bytes:
            stdout = stdout[:cfg.max_output_bytes // 4] + "\n... [TRUNCATED]"
        if len(stderr.encode("utf-8", errors="replace")) > cfg.max_output_bytes:
            stderr = stderr[:cfg.max_output_bytes // 4] + "\n... [TRUNCATED]"

        return {
            "allowed": True,
            "exit_code": proc.returncode,
            "stdout": stdout,
            "stderr": stderr,
            "duration_ms": duration_ms,
            "cwd": str(cfg.workdir),
        }
    except subprocess.TimeoutExpired:
        duration_ms = int((time.monotonic() - started) * 1000)
        return {
            "allowed": True,
            "exit_code": -1,
            "stdout": "",
            "stderr": f"Command timed out after {cfg.default_timeout}s",
            "duration_ms": duration_ms,
            "cwd": str(cfg.workdir),
        }
    except Exception as e:
        duration_ms = int((time.monotonic() - started) * 1000)
        return {
            "allowed": True,
            "exit_code": -1,
            "stdout": "",
            "stderr": f"Execution error: {type(e).__name__}: {e}",
            "duration_ms": duration_ms,
            "cwd": str(cfg.workdir),
        }


# ---------------------------------------------------------------------------
# HTTP handler
# ---------------------------------------------------------------------------

class BridgeHandler(BaseHTTPRequestHandler):
    """Handles POST /run and GET /health."""

    # These are set by the server factory
    cfg: Config = None
    audit: AuditLogger = None
    rate_limiter: RateLimiter = None
    nonce_store: NonceStore = None

    def log_message(self, format: str, *args) -> None:
        """Suppress default stderr logging — we use our audit logger."""
        pass

    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _client_ip(self) -> str:
        # Behind Cloudflare Tunnel, the real IP is in CF-Connecting-IP.
        # Fall back to X-Forwarded-For, then remote address.
        cf = self.headers.get("CF-Connecting-IP")
        if cf:
            return cf.strip()
        xff = self.headers.get("X-Forwarded-For")
        if xff:
            return xff.split(",")[0].strip()
        return self.client_address[0] if self.client_address else "unknown"

    def do_GET(self) -> None:
        """GET /health — no auth, returns status only."""
        if self.path == "/health":
            self._send_json(200, {
                "status": "ok",
                "service": "agent-bridge",
                "version": "1.0.0",
                "workdir": str(self.cfg.workdir),
                "time": datetime.now(timezone.utc).isoformat(),
            })
        else:
            self._send_json(404, {"error": "Not found"})

    def do_POST(self) -> None:
        """POST /run — authenticated command execution."""
        ip = self._client_ip()

        if self.path != "/run":
            self.audit.write({"ip": ip, "path": self.path,
                              "action": "rejected", "reason": "unknown_path"})
            self._send_json(404, {"error": "Only POST /run is supported"})
            return

        # --- Rate limit ---
        if not self.rate_limiter.allow(ip):
            self.audit.write({"ip": ip, "action": "rejected",
                              "reason": "rate_limit"})
            self._send_json(429, {"error": "Rate limit exceeded"})
            return

        # --- Read body ---
        try:
            content_length = int(self.headers.get("Content-Length", 0))
        except (ValueError, TypeError):
            content_length = 0
        if content_length <= 0 or content_length > MAX_BODY_BYTES:
            self.audit.write({"ip": ip, "action": "rejected",
                              "reason": "invalid_body_size",
                              "content_length": content_length})
            self._send_json(400, {"error": "Invalid Content-Length"})
            return

        body = self.rfile.read(content_length)

        # --- Parse JSON body ---
        try:
            payload = json.loads(body.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            self.audit.write({"ip": ip, "action": "rejected",
                              "reason": "invalid_json", "error": str(e)})
            self._send_json(400, {"error": "Invalid JSON body"})
            return

        command = payload.get("command", "")
        if not command or not isinstance(command, str):
            self.audit.write({"ip": ip, "action": "rejected",
                              "reason": "missing_command"})
            self._send_json(400, {"error": "Missing 'command' in body"})
            return

        # --- Auth headers ---
        timestamp = self.headers.get("X-Bridge-Timestamp", "")
        nonce = self.headers.get("X-Bridge-Nonce", "")
        signature = self.headers.get("X-Bridge-Signature", "")

        if not all([timestamp, nonce, signature]):
            self.audit.write({"ip": ip, "action": "rejected",
                              "reason": "missing_auth_headers",
                              "command": command[:200]})
            self._send_json(401, {"error": "Missing auth headers"})
            return

        # --- Timestamp freshness ---
        dt = parse_timestamp(timestamp)
        if dt is None or not is_timestamp_fresh(dt, TIMESTAMP_WINDOW_SECONDS):
            self.audit.write({"ip": ip, "action": "rejected",
                              "reason": "timestamp_out_of_window",
                              "command": command[:200]})
            self._send_json(401, {"error": "Timestamp out of window"})
            return

        # --- Nonce freshness (anti-replay) ---
        if not self.nonce_store.is_fresh(nonce):
            self.audit.write({"ip": ip, "action": "rejected",
                              "reason": "nonce_replay",
                              "command": command[:200]})
            self._send_json(401, {"error": "Nonce already used (replay)"})
            return

        # --- Signature ---
        if not verify_signature(self.cfg.secret, timestamp, nonce,
                                 body, signature):
            self.audit.write({"ip": ip, "action": "rejected",
                              "reason": "invalid_signature",
                              "command": command[:200]})
            self._send_json(401, {"error": "Invalid signature"})
            return

        # --- Execute ---
        result = execute_command(command, self.cfg)

        # --- Audit ---
        self.audit.write({
            "ip": ip,
            "action": "executed" if result["allowed"] else "rejected",
            "command": command,
            "reason": result.get("reason", ""),
            "exit_code": result.get("exit_code"),
            "duration_ms": result.get("duration_ms"),
            "stdout_bytes": len(result.get("stdout", "").encode("utf-8", errors="replace")),
            "stderr_bytes": len(result.get("stderr", "").encode("utf-8", errors="replace")),
        })

        # --- Respond ---
        if result["allowed"]:
            self._send_json(200, result)
        else:
            self._send_json(403, result)


# ---------------------------------------------------------------------------
# Server factory
# ---------------------------------------------------------------------------

def make_server(cfg: Config) -> ThreadingHTTPServer:
    audit = AuditLogger(cfg.log_path)
    rate_limiter = RateLimiter(cfg.rate_limit_per_minute)
    nonce_store = NonceStore(NONCE_TTL_SECONDS)

    class BoundHandler(BridgeHandler):
        pass

    BoundHandler.cfg = cfg
    BoundHandler.audit = audit
    BoundHandler.rate_limiter = rate_limiter
    BoundHandler.nonce_store = nonce_store

    server = ThreadingHTTPServer((cfg.host, cfg.port), BoundHandler)
    server.daemon_threads = True
    return server


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="AliceLabs agent-bridge — secure local command executor"
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH,
                        help="Path to config.json")
    args = parser.parse_args()

    try:
        cfg = Config(args.config)
    except (FileNotFoundError, ValueError) as e:
        print(f"❌ Configuration error:\n{e}", file=sys.stderr)
        return 1

    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    log = logging.getLogger("agent-bridge")

    # Print startup banner
    print("=" * 72)
    print("🔐 AliceLabs agent-bridge v1.0.0")
    print("=" * 72)
    print(f"  Listening on:  http://{cfg.host}:{cfg.port}")
    print(f"  Workdir:       {cfg.workdir}")
    print(f"  Allowlist:     {len(cfg.allowlist)} commands")
    print(f"  Blocklist:     {len(cfg.blocklist)} patterns")
    print(f"  Timeout:       {cfg.default_timeout}s per command")
    print(f"  Rate limit:    {cfg.rate_limit_per_minute} req/min per IP")
    print(f"  Audit log:     {cfg.log_path}")
    print()
    print("  Next step — open a second terminal and run:")
    print(f"    cloudflared tunnel --url http://localhost:{cfg.port}")
    print()
    print("  Cloudflare will print a URL like https://xyz.trycloudflare.com.")
    print("  Send that URL to Edison so the Z.ai sandbox can reach you.")
    print()
    print("  Kill switch: create a file named PAUSE in the workdir to stop")
    print("  command execution. Delete it to resume.")
    print("=" * 72)
    print()

    server = make_server(cfg)
    try:
        server.serve_forever(poll_interval=0.5)
    except KeyboardInterrupt:
        log.info("Shutting down (Ctrl+C)")
        server.shutdown()
        return 0
    except Exception as e:
        log.error(f"Server crashed: {type(e).__name__}: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
