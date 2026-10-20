#!/usr/bin/env python3
"""Agent Bridge CLI — sends commands via GitHub, reads responses via webhook.site.

Usage:
    python3 agent_bridge_cli.py ping
    python3 agent_bridge_cli.py open "https://example.com"
    python3 agent_bridge_cli.py snapshot
    python3 agent_bridge_cli.py click "#submit-btn"
    python3 agent_bridge_cli.py fill "#email" "test@example.com"
    python3 agent_bridge_cli.py geturl
    python3 agent_bridge_cli.py screenshot out.png
    python3 agent_bridge_cli.py --repl

Architecture:
    This CLI writes commands to a GitHub repo file (command.json) via the
    Contents API. The Chrome extension polls that file every 2s, executes
    the command, and POSTs the response to a webhook.site URL. This CLI
    then reads the response from webhook.site.

    No ntfy.sh, no port forwarding, no tokens in the extension.
"""
import base64
import json
import sys
import time
import uuid
import urllib.request
import urllib.parse
import urllib.error
import ssl
import argparse

# ── Config ──────────────────────────────────────────────────────────────────
GITHUB_TOKEN = "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"
GITHUB_OWNER = "eddyflores100-lang"
GITHUB_REPO = "agent-bridge-relay"
GITHUB_BRANCH = "main"
COMMAND_FILE = "command.json"

# Webhook.site URL for responses (created once, reused)
WEBHOOK_UUID = "bc53085a-10ce-41e7-8c4d-120f043c2ad0"
WEBHOOK_URL = f"https://webhook.site/{WEBHOOK_UUID}"
WEBHOOK_API = f"https://webhook.site/token/{WEBHOOK_UUID}/requests"

# Polling
RESPONSE_TIMEOUT = 30  # seconds
RESPONSE_POLL_INTERVAL = 1  # seconds

_ctx = ssl.create_default_context()
_cmd_seq = 0
_file_sha = None


def gh_api(method, path, data=None):
    """Call GitHub API."""
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/{path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    body = json.dumps(data).encode() if data else None
    if body:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, context=_ctx, timeout=15) as resp:
        return resp.status, json.loads(resp.read().decode())


def get_file_sha():
    """Get the current SHA of command.json (needed for updates)."""
    status, data = gh_api("GET", f"contents/{COMMAND_FILE}")
    return data.get("sha")


def get_command_state():
    """Read the current command sequence + file SHA from GitHub."""
    status, data = gh_api("GET", f"contents/{COMMAND_FILE}")
    content = base64.b64decode(data["content"]).decode()
    cmd = json.loads(content)
    return cmd.get("cmd_seq", 0), data.get("sha")


def send_command(action, **args):
    """Write a command to the GitHub repo file. The extension polls and executes."""
    global _cmd_seq, _file_sha

    # Always read the current state from GitHub to avoid sequence conflicts
    if _file_sha is None:
        _cmd_seq, _file_sha = get_command_state()

    _cmd_seq += 1
    cmd = {
        "cmd_seq": _cmd_seq,
        "action": action,
        "args": args,
        "resp_url": WEBHOOK_URL,
    }

    content_b64 = base64.b64encode(
        json.dumps(cmd, indent=2).encode()
    ).decode()

    # Always get the latest SHA before writing (avoids 409 conflict)
    try:
        _, latest = gh_api("GET", f"contents/{COMMAND_FILE}")
        _file_sha = latest.get("sha", _file_sha)
    except Exception:
        pass

    status, resp = gh_api("PUT", f"contents/{COMMAND_FILE}", {
        "message": f"cmd #{_cmd_seq}: {action}",
        "content": content_b64,
        "sha": _file_sha,
        "branch": GITHUB_BRANCH,
    })

    if status not in (200, 201):
        print(f"  ✗ GitHub API error: {status}", file=sys.stderr)
        return None

    _file_sha = resp["content"]["sha"]

    print(f"→ #{_cmd_seq} {action}" + (f" {args}" if args else ""))
    return wait_for_response(_cmd_seq)


def wait_for_response(cmd_seq, timeout=RESPONSE_TIMEOUT):
    """Poll GitHub response.json for the response with matching id.

    The extension writes responses to response.json in the same repo.
    We poll the GitHub API (no cache) every 1.5s until we find our response.
    """
    deadline = time.time() + timeout

    while time.time() < deadline:
        try:
            status, data = gh_api("GET", "contents/response.json")
            if status != 200:
                time.sleep(1.5)
                continue

            content = base64.b64decode(data["content"]).decode()
            body = json.loads(content)

            if body.get("id") == cmd_seq:
                if body.get("ok"):
                    result = body.get("result")
                    if isinstance(result, (dict, list)):
                        print(f"✓ {json.dumps(result, indent=2)[:600]}")
                    else:
                        print(f"✓ {result}")
                else:
                    print(f"✗ error: {body.get('error', 'unknown')}")
                return body
        except Exception as e:
            pass  # response.json might not exist yet

        time.sleep(1.5)

    print("  ⏱ no response (timeout)")
    return None


def repl():
    """Interactive REPL mode."""
    print("Agent Bridge REPL")
    print("Commands: open <url>, snapshot, click <sel>, fill <sel> <val>,")
    print("          gettext <sel>, geturl, listtabs, switchtab <id>,")
    print("          eval <code>, screenshot <file>, wait <ms>, press <key>,")
    print("          scroll <dir> <amount>, ping, quit")
    print()
    while True:
        try:
            line = input("agent> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nbye")
            break
        if not line:
            continue
        if line in ("quit", "exit", "q"):
            break

        parts = line.split(maxsplit=1)
        action = parts[0]
        rest = parts[1] if len(parts) > 1 else ""
        args = {}

        if action == "open":
            args["url"] = rest
        elif action == "click":
            args["selector"] = rest
        elif action == "fill":
            sub = rest.split(maxsplit=1)
            if len(sub) == 2:
                args["selector"] = sub[0]
                args["value"] = sub[1]
            else:
                print("  usage: fill <selector> <value>")
                continue
        elif action == "gettext":
            args["selector"] = rest
        elif action == "switchtab":
            try:
                args["tabId"] = int(rest)
            except ValueError:
                print("  usage: switchtab <id>")
                continue
        elif action == "eval":
            args["code"] = rest
        elif action == "screenshot":
            args["_saveTo"] = rest or "screenshot.png"
        elif action == "wait":
            try:
                args["ms"] = int(rest) if rest else 1000
            except ValueError:
                args["ms"] = 1000
        elif action == "press":
            args["key"] = rest or "Enter"
        elif action == "scroll":
            sub = rest.split()
            args["direction"] = sub[0] if sub else "down"
            args["amount"] = int(sub[1]) if len(sub) > 1 else 500
        elif action in ("ping", "snapshot", "geturl", "listtabs"):
            pass
        else:
            print(f"  unknown: {action}")
            continue

        save_to = args.pop("_saveTo", None)
        resp = send_command(action, **args)
        if action == "screenshot" and resp and resp.get("ok"):
            result = resp.get("result", {})
            data_url = result.get("dataUrl", "")
            if data_url.startswith("data:image/png;base64,"):
                with open(save_to, "wb") as f:
                    f.write(base64.b64decode(data_url[len("data:image/png;base64,"):]))
                print(f"  💾 saved to {save_to}")


def main():
    parser = argparse.ArgumentParser(description="Agent Bridge CLI")
    parser.add_argument("action", nargs="?", help="command to send")
    parser.add_argument("args", nargs="*", help="positional args")
    parser.add_argument("--repl", action="store_true", help="interactive mode")
    a = parser.parse_args()

    if a.repl or not a.action:
        repl()
        return

    action = a.action
    args = {}
    if action == "open" and a.args:
        args["url"] = a.args[0]
    elif action == "click" and a.args:
        args["selector"] = a.args[0]
    elif action == "fill" and len(a.args) >= 2:
        args["selector"] = a.args[0]
        args["value"] = a.args[1]
    elif action == "gettext" and a.args:
        args["selector"] = a.args[0]
    elif action == "eval" and a.args:
        args["code"] = a.args[0]
    elif action == "wait" and a.args:
        args["ms"] = int(a.args[0])
    elif action == "press" and a.args:
        args["key"] = a.args[0]
    elif action == "scroll" and a.args:
        args["direction"] = a.args[0]
        if len(a.args) > 1:
            args["amount"] = int(a.args[1])

    send_command(action, **args)


if __name__ == "__main__":
    main()
