#!/usr/bin/env python3
"""
opp6_pass2_api.py — OPP-6 Pass 2: confirm the 19 LIVE_UNKNOWN bounties from
pass 1 via the anonymous GitHub API.

Pass 1 (HTML scrape) finished at ~01:25 UTC. Pass 2 needs the anonymous rate
limit (60/hr) to reset; reset was at 01:38:31 UTC. This script polls the
rate-limit endpoint, waits if needed, then issues 19 API calls and saves
results to opp6_results_full.json + writes the final markdown.
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error
import ssl
from datetime import datetime, timezone

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
CTX = ssl.create_default_context()

OUT_JSON = "/home/z/my-project/scripts/opp6_results_full.json"
PASS1_JSON = "/home/z/my-project/scripts/opp6_pass1.json"

# The 19 LIVE_UNKNOWN from pass 1 (in original table order)
LIVE_CANDIDATES = [
    # (idx, owner, repo, num, amount_str, original_url)
    (2,  "commaai",                "opendbc",                              2017, "$3,000",  "https://github.com/commaai/opendbc/issues/2017"),
    (3,  "osmesirius-ship-it",     "daxda-next-gen",                       39,   "$5,000",  "https://github.com/osmesirius-ship-it/daxda-next-gen/issues/39"),
    (4,  "tursodatabase",          "turso",                                3830, "$1,500",  "https://github.com/tursodatabase/turso/issues/3830"),
    (5,  "tursodatabase",          "turso",                                5092, "$2,500",  "https://github.com/tursodatabase/turso/issues/5092"),
    (7,  "Sifchain",               "sifnode",                              503,  "$1,000",  "https://github.com/Sifchain/sifnode/issues/503"),
    (8,  "Sifchain",               "sifnode",                              524,  "$1,000",  "https://github.com/Sifchain/sifnode/issues/524"),
    (9,  "teamleaderleo",          "bot-observatory",                      45,   "$1,000",  "https://github.com/teamleaderleo/bot-observatory/issues/45"),
    (10, "commaai",                "opendbc",                              1175, "$1,000",  "https://github.com/commaai/opendbc/issues/1175"),
    (11, "commaai",                "opendbc",                              1833, "$1,000",  "https://github.com/commaai/opendbc/issues/1833"),
    (12, "tursodatabase",          "turso",                                4493, "$800",    "https://github.com/tursodatabase/turso/issues/4493"),
    (14, "tursodatabase",          "turso",                                4879, "$1,000",  "https://github.com/tursodatabase/turso/issues/4879"),
    (15, "tursodatabase",          "turso",                                6626, "$1,000",  "https://github.com/tursodatabase/turso/issues/6626"),
    (16, "tursodatabase",          "turso",                                3436, "$500",    "https://github.com/tursodatabase/turso/issues/3436"),
    (17, "tursodatabase",          "turso",                                2049, "$500",    "https://github.com/tursodatabase/turso/issues/2049"),
    (20, "perria080925-bot",       "agente-bountie",                       1,    "$500",    "https://github.com/perria080925-bot/agente-bountie/issues/1"),
    (21, "NEXAITECHAU",            "gh-disc-54891-tenstorrent-tt-metal",   1,    "$2,000",  "https://github.com/NEXAITECHAU/gh-disc-54891-tenstorrent-tt-metal/issues/1"),
    (22, "Senthemodder",           "aquarium-of-gullibles",                1,    "$1,250",  "https://github.com/Senthemodder/aquarium-of-gullibles/issues/1"),
    (24, "tursodatabase",          "turso",                                6583, "$200",    "https://github.com/tursodatabase/turso/issues/6583"),
    (28, "flowdriveai",            "flowpilot",                            46,   "$100",    "https://github.com/flowdriveai/flowpilot/issues/46"),
]


def api_call(url, accept="application/vnd.github.v3+json", timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
    with urllib.request.urlopen(req, context=CTX, timeout=timeout) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))


def check_rate_limit():
    try:
        _, rl = api_call("https://api.github.com/rate_limit")
        return rl["resources"]["core"]["remaining"], rl["resources"]["core"]["reset"]
    except Exception as e:
        print(f"  [ratelimit check failed] {e}")
        return None, None


def wait_for_reset():
    """Block (polling every 30s) until core rate limit >= 25."""
    while True:
        rem, reset = check_rate_limit()
        now = int(time.time())
        if rem is None:
            print("  ratelimit endpoint failed — sleeping 30s and retrying")
            time.sleep(30)
            continue
        if rem >= 25:
            print(f"  OK: {rem}/60 remaining — proceeding")
            return
        wait = max(5, reset - now + 3)
        print(f"  ratelimit {rem}/60 — need to wait ~{wait}s until reset at {datetime.fromtimestamp(reset, tz=timezone.utc).isoformat()}")
        # cap each sleep at 90s so we can be interrupted
        time.sleep(min(wait, 90))


def confirm_issue(owner, repo, num):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{num}"
    try:
        _, data = api_call(url)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "DEAD", {"api_404": True}
        if e.code == 403:
            return "RATE_LIMITED", {"api_403": str(e)[:120]}
        return "ERROR", {"api_http": e.code}
    except Exception as e:
        return "ERROR", {"api_err": str(e)[:200]}

    state = data.get("state", "?")
    assignee = data.get("assignee")
    assignees = data.get("assignees", []) or []
    labels = [l.get("name", "") for l in (data.get("labels") or [])]
    title = data.get("title", "") or ""
    body = data.get("body", "") or ""
    comments = data.get("comments", 0)
    pr_field = data.get("pull_request")
    locked = data.get("locked", False)
    lock_reason = data.get("active_lock_reason")
    updated_at = data.get("updated_at", "?")
    closed_at = data.get("closed_at")
    created_at = data.get("created_at", "?")

    detail = {
        "state": state, "assignee": assignee.get("login") if assignee else None,
        "assignees": [a.get("login") for a in assignees],
        "labels": labels, "title": title, "comments": comments,
        "locked": locked, "lock_reason": lock_reason,
        "is_pr": pr_field is not None, "closed_at": closed_at,
        "updated_at": updated_at, "created_at": created_at,
    }
    label_lc = [l.lower() for l in labels]
    has_bounty_label = any(
        ("bounty" in l) or ("reward" in l) or ("💰" in l) or ("💵" in l) or ("usd" in l)
        for l in label_lc
    )
    has_dollar = ("$" in title) or ("$" in body)
    has_algora = ("algora" in body.lower()) or ("/bounty" in body.lower())
    has_issuehunt = "issuehunt" in body.lower()
    detail["bounty_signal"] = {
        "label": has_bounty_label, "dollar": has_dollar,
        "algora": has_algora, "issuehunt": has_issuehunt,
    }
    detail["has_any_signal"] = bool(has_bounty_label or has_dollar or has_algora or has_issuehunt)

    if state != "open":
        detail["why_dead"] = f"state={state}"
        return "DEAD", detail
    if pr_field is not None:
        detail["why_disputed"] = "URL is a PR not an issue"
        return "DISPUTED", detail
    if locked:
        detail["why_disputed"] = f"locked ({lock_reason})"
        return "DISPUTED", detail
    if assignee or assignees:
        detail["why_disputed"] = f"assignee={assignee.get('login') if assignee else assignees}"
        return "DISPUTED", detail
    return "LIVE", detail


def main():
    print(f"=== OPP-6 Pass 2 starting at {datetime.now(timezone.utc).isoformat()} ===")
    print(f"Confirming {len(LIVE_CANDIDATES)} LIVE_UNKNOWN bounties via anonymous GitHub API\n")

    print("Waiting for anonymous rate limit (need >=25 free slots)...")
    wait_for_reset()
    print()

    results = []
    for i, (idx, owner, repo, num, amount, url) in enumerate(LIVE_CANDIDATES, 1):
        # refresh ratelimit check every 8 calls
        if i % 8 == 0:
            rem, _ = check_rate_limit()
            print(f"  [ratelimit] {rem}/60 remaining")
            if rem is not None and rem < 5:
                print("  low — pausing 60s")
                time.sleep(60)
        verdict, detail = confirm_issue(owner, repo, num)
        rec = {
            "table_idx": idx, "owner": owner, "repo": repo, "num": num,
            "amount": amount, "url": url,
            "pass2_verdict": verdict, "pass2_detail": detail,
        }
        results.append(rec)
        print(f"  [{i:2d}/{len(LIVE_CANDIDATES)}] {verdict:12s} {amount:>8s}  {url}")
        if verdict == "LIVE":
            print(f"     title: {detail['title'][:90]}")
            print(f"     labels: {detail['labels'][:8]}  comments: {detail['comments']}  signal: {detail['bounty_signal']}")
            print(f"     updated: {detail['updated_at']}")
        elif verdict == "DEAD":
            print(f"     state={detail.get('state')} closed_at={detail.get('closed_at')}")
        elif verdict == "DISPUTED":
            print(f"     state={detail.get('state')} assignee={detail.get('assignee')} locked={detail.get('locked')}({detail.get('lock_reason')}) is_pr={detail.get('is_pr')}")
            print(f"     why: {detail.get('why_disputed', detail.get('why_dead'))}")
        elif verdict == "RATE_LIMITED":
            print("  !!! rate limited mid-pass — aborting")
            break
        time.sleep(0.6)

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nFull pass 2 results -> {OUT_JSON}")

    live = [r for r in results if r["pass2_verdict"] == "LIVE"]
    disp = [r for r in results if r["pass2_verdict"] == "DISPUTED"]
    dead = [r for r in results if r["pass2_verdict"] == "DEAD"]
    err  = [r for r in results if r["pass2_verdict"] in ("ERROR", "RATE_LIMITED")]
    print(f"\n=== PASS 2 TALLY (out of {len(LIVE_CANDIDATES)} LIVE_UNKNOWN from pass 1) ===")
    print(f"  LIVE     : {len(live)}")
    print(f"  DISPUTED : {len(disp)}")
    print(f"  DEAD     : {len(dead)}")
    print(f"  ERROR    : {len(err)}")


if __name__ == "__main__":
    main()
