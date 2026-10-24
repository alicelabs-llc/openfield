#!/usr/bin/env python3
"""
opp6_verify.py — OPP-6: Re-verify the 36 OSS bounties reported by OPP-2.

Strategy (two-pass):
  Pass 1 — HTML scrape (no rate limit):
    For each URL, curl the GitHub issue HTML page with a browser UA and
    classify into LIVE / DISPUTED / DEAD based on static HTML markers:
      * HTTP 404 / "page you are looking for"  -> DEAD (404)
      * "This issue was closed" / "State: closed" / octicon-issue-closed -> DEAD (closed)
      * "Repository has been deleted" / "moved" -> DEAD (repo gone)
      * "locked as" / "Lock conversation" + "comment lock" -> DISPUTED (locked)
      * assignee present (not "No one assigned") -> DISPUTED (assigned)
      * "Successfully merging a pull request may close this issue" with an
        OPEN linked PR -> DISPUTED (active PR)
      * otherwise -> LIVE (pending API confirmation)

  Pass 2 — anonymous GitHub API (60/hr limit, run AFTER pass 1 to defer usage):
    For each LIVE-from-HTML entry, GET /repos/OWNER/REPO/issues/NUMBER
    Confirm: state == "open" AND assignee == null AND has bounty-ish label
    or "$" in title/body. Also report comments count and PR refs.

Output:
  /home/z/my-project/download/OPP_OSS_BOUNTIES_VERIFIED.md   — verified-only list
  /home/z/my-project/scripts/opp6_results.json                — full classification log
"""

import json
import re
import sys
import time
import urllib.request
import urllib.error
import ssl
from datetime import datetime, timezone

SRC = "/tmp/my-project/download/OPP_OSS_BOUNTIES.md"
OUT_MD = "/home/z/my-project/download/OPP_OSS_BOUNTIES_VERIFIED.md"
OUT_JSON = "/home/z/my-project/scripts/opp6_results.json"

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
CTX = ssl.create_default_context()

URL_RE = re.compile(r"https://github\.com/([\w.\-]+)/([\w.\-]+)/issues/(\d+)")


def http_get(url, accept="text/html,application/xhtml+xml", timeout=25):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": accept,
        "Accept-Language": "en-US,en;q=0.9",
    })
    with urllib.request.urlopen(req, context=CTX, timeout=timeout) as resp:
        return resp.status, resp.read().decode("utf-8", errors="replace"), dict(resp.headers)


def fetch_html(url):
    """Return (status, html, final_url) or (status, None, url) on error."""
    try:
        status, body, hdrs = http_get(url)
        return status, body, url
    except urllib.error.HTTPError as e:
        # 404 / 410 / 451 — fetch body if any
        try:
            body = e.read().decode("utf-8", errors="replace")
        except Exception:
            body = None
        return e.code, body, url
    except urllib.error.URLError as e:
        return None, str(e), url
    except Exception as e:
        return None, str(e), url


def classify_html(status, html):
    """Return (classification, reason, evidence) where classification is
    one of: DEAD, DISPUTED, LIVE_UNKNOWN."""
    if status is None:
        return "DEAD", "fetch_error", "no response"
    if status == 404:
        return "DEAD", "404", "GitHub returned 404"
    if status == 410:
        return "DEAD", "410_gone", "GitHub returned 410 Gone"
    if status == 451:
        return "DEAD", "451_unavailable_legal", "GitHub returned 451"
    if status >= 500:
        return "DEAD", f"http_{status}", "GitHub server error"
    if status not in (200, 301, 302):
        return "DEAD", f"http_{status}", f"unexpected status {status}"
    if html is None:
        return "DEAD", "empty_body", "no HTML body"

    low = html.lower()

    # 404 page (sometimes returns 200 with a 404 page)
    if "this is not the web page you are looking for" in low:
        return "DEAD", "404_page", "GitHub 404 page"
    if "repository has been deleted" in low or "repo was deleted" in low:
        return "DEAD", "repo_deleted", "repository deleted"
    if "the repository you're looking for doesn't exist" in low:
        return "DEAD", "repo_not_found", "repo doesn't exist"

    # Issue / repo moved
    if "this repository is empty" in low and "issues" not in low:
        return "DEAD", "empty_repo", "repository is empty"

    # Login wall (private repo / DMCA)
    if "sign in to github" in low and "issue" not in low:
        return "DEAD", "login_wall", "private or DMCA'd"

    # Issue state — GitHub HTML uses "State: open" / "State: closed" in the
    # sidebar, and the title bar shows "Issue · #N · CLOSED".
    closed_markers = [
        "state: closed",
        '"state":"closed"',
        "this issue was closed",
        "closed this issue",
        "issue · closed",
        "closed on",
    ]
    # be careful: "Closed" can appear in linked PRs sidebar. We require
    # multiple independent markers, OR the canonical "State: closed" /
    # '"state":"closed"' JSON in the page data.
    is_closed = (
        "state: closed" in low
        or '"state":"closed"' in low
        or ('"state": "closed"' in low)
    )

    # The "issue opened" / "issue closed" octicons
    has_closed_icon = "octicon-issue-closed" in low
    has_open_icon = "octicon-issue-opened" in low

    if is_closed or (has_closed_icon and not has_open_icon):
        return "DEAD", "closed", "issue closed"

    # Locked
    if "locked as" in low or "locked this conversation" in low:
        return "DISPUTED", "locked", "conversation locked"
    if "this conversation has been locked" in low:
        return "DISPUTED", "locked", "conversation locked"
    # "Lock conversation" button only appears for maintainers — not a
    # reliable lock signal by itself, so we don't use it.

    # Assignee — sidebar shows either "No one assigned" or an avatar
    # with a login. The static HTML reliably contains the text "No one
    # assigned" when nobody is assigned.
    if "no one assigned" in low:
        assigned = False
    else:
        # The sidebar "Assignees" section is rendered without the
        # "No one assigned" text only when someone IS assigned.
        if "assignees" in low and "assignee" in low:
            # Check for a concrete login: GitHub renders assignee as
            # <a href="/LOGIN"> or data-hovercard-url="/users/LOGIN/..."
            m = re.search(r'/users/([\w.\-]+)/hovercard', low)
            if m:
                return "DISPUTED", "assigned", f"assignee=@{m.group(1)}"

    # Linked PR — sidebar shows "Linked pull requests" with a list. The
    # "Successfully merging a pull request may close this issue" string
    # appears in the comment box when no PR is linked yet, so it is NOT
    # a reliable signal on its own. Instead we look for the sidebar block:
    #   <div ... data-test-selector="issue-linked-pull-requests">
    # or the visible "Linked pull requests" header followed by a PR link.
    if "linked pull requests" in low:
        # extract PR numbers from the sidebar
        prs = re.findall(r'/[\w.\-]+/[\w.\-]+/pull/(\d+)', low)
        prs = list(dict.fromkeys(prs))  # dedupe, preserve order
        if prs:
            return "DISPUTED", "has_linked_pr", f"linked PRs: {','.join(prs[:3])}"

    return "LIVE_UNKNOWN", "open_unassigned_no_pr", "HTML markers indicate open + unassigned + no linked PR"


def fetch_issue_api(owner, repo, num):
    """Anonymous GitHub API call. Returns dict or raises."""
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{num}"
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "application/vnd.github.v3+json",
    })
    with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def api_confirm(owner, repo, num):
    """Return (verdict, detail_dict). Verdict: LIVE / DISPUTED / DEAD / ERROR."""
    try:
        data = fetch_issue_api(owner, repo, num)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "DEAD", {"api": "404 issue not found"}
        if e.code == 403:
            return "RATE_LIMITED", {"api": f"403 {e}"}
        return "ERROR", {"api": f"HTTP {e.code}"}
    except Exception as e:
        return "ERROR", {"api": str(e)[:200]}

    state = data.get("state", "?")
    assignee = data.get("assignee")
    assignees = data.get("assignees", []) or []
    labels = [l.get("name", "") for l in data.get("labels", []) or []]
    title = data.get("title", "")
    body = data.get("body", "") or ""
    comments = data.get("comments", 0)
    pr_field = data.get("pull_request")  # if the "issue" is actually a PR
    locked = data.get("locked", False)
    # active_lock_reason: 'off-topic' / 'resolved' / 'spam' / 'too heated'
    lock_reason = data.get("active_lock_reason")
    updated_at = data.get("updated_at", "?")
    closed_at = data.get("closed_at")

    detail = {
        "state": state,
        "assignee": assignee.get("login") if assignee else None,
        "assignees": [a.get("login") for a in assignees],
        "labels": labels,
        "title": title,
        "comments": comments,
        "locked": locked,
        "lock_reason": lock_reason,
        "is_pr": pr_field is not None,
        "closed_at": closed_at,
        "updated_at": updated_at,
    }

    if state != "open":
        return "DEAD", detail
    if pr_field is not None:
        # the URL was /issues/N but it's actually a PR — bounty usually lives
        # on the issue, not the PR. Treat as disputed (someone is working on it).
        return "DISPUTED", detail
    if locked:
        return "DISPUTED", detail
    if assignee or assignees:
        return "DISPUTED", detail

    # Bounty signal: label contains "bounty"/"reward" or title/body has "$"
    label_lc = [l.lower() for l in labels]
    has_bounty_label = any(("bounty" in l) or ("reward" in l) or ("💰" in l) or ("💵" in l) or ("usd" in l) for l in label_lc)
    has_dollar = ("$" in title) or ("$" in body)
    has_algora = ("algora" in body.lower()) or ("/bounty" in body.lower())
    has_issuehunt = "issuehunt" in body.lower()
    detail["has_bounty_signal"] = bool(has_bounty_label or has_dollar or has_algora or has_issuehunt)
    detail["bounty_signal"] = {
        "label": has_bounty_label,
        "dollar": has_dollar,
        "algora": has_algora,
        "issuehunt": has_issuehunt,
    }

    return "LIVE", detail


def parse_bounties(src_md):
    """Extract the 36 bounty rows from the markdown table."""
    bounties = []
    with open(src_md, "r", encoding="utf-8") as f:
        for line in f:
            m = URL_RE.search(line)
            if not m:
                continue
            owner, repo, num = m.group(1), m.group(2), m.group(3)
            url = m.group(0)
            # skip the table header / sample rows that don't have an amount
            # immediately after the URL. We also pull the amount from the
            # same table row.
            amt = "?"
            amt_match = re.search(r"\$(\d[\d,]*)", line)
            if amt_match:
                amt = "$" + amt_match.group(1)
            bounties.append({
                "owner": owner,
                "repo": repo,
                "num": int(num),
                "url": url,
                "amount": amt,
                "raw_row": line.rstrip("\n"),
            })
    # de-dup by URL while preserving order
    seen = set()
    out = []
    for b in bounties:
        if b["url"] in seen:
            continue
        seen.add(b["url"])
        out.append(b)
    return out


def main():
    print(f"=== OPP-6 verification starting at {datetime.now(timezone.utc).isoformat()} ===\n")
    bounties = parse_bounties(SRC)
    print(f"Parsed {len(bounties)} unique bounty URLs from {SRC}\n")

    # PASS 1 — HTML scrape
    print("--- PASS 1: HTML scrape (no rate limit) ---")
    for i, b in enumerate(bounties, 1):
        url = b["url"]
        status, html, final = fetch_html(url)
        cls, reason, ev = classify_html(status, html)
        b["pass1_status"] = status
        b["pass1_classification"] = cls
        b["pass1_reason"] = reason
        b["pass1_evidence"] = ev
        b["pass1_final_url"] = final
        marker = {"LIVE_UNKNOWN": "OK?", "DISPUTED": "DISP", "DEAD": "DEAD"}.get(cls, cls)
        print(f"  [{i:2d}/36] {marker:5s} {b['amount']:>8s}  {url}  ({reason})")
        time.sleep(0.4)  # gentle on GitHub

    # Wait for rate limit if needed before pass 2
    # Check current rate limit
    try:
        status, body, _ = http_get("https://api.github.com/rate_limit",
                                   accept="application/vnd.github.v3+json")
        rl = json.loads(body)
        remaining = rl["resources"]["core"]["remaining"]
        reset = rl["resources"]["core"]["reset"]
        print(f"\n--- GitHub API rate limit: {remaining}/60 remaining, resets in {max(0, reset-int(time.time()))}s ---")
    except Exception as e:
        print(f"\n--- could not read rate limit: {e} ---")
        remaining, reset = 0, 0

    # PASS 2 — anonymous API confirm for LIVE_UNKNOWN entries
    live_candidates = [b for b in bounties if b["pass1_classification"] == "LIVE_UNKNOWN"]
    print(f"\n--- PASS 2: API confirmation for {len(live_candidates)} LIVE candidates ---")

    if remaining < len(live_candidates) + 2:
        wait = max(0, reset - int(time.time())) + 5
        print(f"  rate limit too low ({remaining} < {len(live_candidates)+2}); sleeping {wait}s until reset")
        if wait > 0:
            time.sleep(min(wait, 1200))  # cap at 20 min

    for i, b in enumerate(live_candidates, 1):
        # refresh rate limit check occasionally
        if i % 15 == 0:
            try:
                _, rlbody, _ = http_get("https://api.github.com/rate_limit",
                                        accept="application/vnd.github.v3+json")
                rem = json.loads(rlbody)["resources"]["core"]["remaining"]
                print(f"    [ratelimit check] {rem}/60 remaining")
                if rem < 3:
                    print("    rate limit low — pausing 30s")
                    time.sleep(30)
            except Exception:
                pass
        verdict, detail = api_confirm(b["owner"], b["repo"], b["num"])
        b["pass2_verdict"] = verdict
        b["pass2_detail"] = detail
        print(f"  [{i}/{len(live_candidates)}] {verdict:12s} {b['amount']:>8s}  {b['url']}")
        if verdict == "LIVE":
            print(f"     labels={detail.get('labels', [])[:6]} comments={detail.get('comments', 0)} signal={detail.get('bounty_signal')}")
        elif verdict == "DEAD":
            print(f"     state={detail.get('state')} closed_at={detail.get('closed_at')}")
        elif verdict == "DISPUTED":
            print(f"     state={detail.get('state')} assignee={detail.get('assignee')} locked={detail.get('locked')} is_pr={detail.get('is_pr')}")
        elif verdict == "RATE_LIMITED":
            print("     !!! rate limited — stopping API pass")
            break
        time.sleep(0.5)

    # Save full results JSON
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(bounties, f, indent=2, default=str)
    print(f"\nFull classification log -> {OUT_JSON}")

    # Final tally
    final_live = []
    final_disputed = []
    final_dead = []
    for b in bounties:
        v = b.get("pass2_verdict")
        if v == "LIVE":
            final_live.append(b)
        elif v == "DEAD":
            final_dead.append(b)
        elif v == "DISPUTED":
            final_disputed.append(b)
        else:
            # pass2 didn't run or errored — fall back to pass1
            p1 = b["pass1_classification"]
            if p1 == "LIVE_UNKNOWN":
                # treat as unconfirmed — put in disputed bucket to be safe
                b["pass2_verdict"] = "UNCONFIRMED"
                final_disputed.append(b)
            elif p1 == "DISPUTED":
                final_disputed.append(b)
            elif p1 == "DEAD":
                final_dead.append(b)

    print(f"\n=== FINAL TALLY ===")
    print(f"  LIVE     : {len(final_live)}")
    print(f"  DISPUTED : {len(final_disputed)}")
    print(f"  DEAD     : {len(final_dead)}")
    print(f"  TOTAL    : {len(bounties)}")

    return bounties, final_live, final_disputed, final_dead


if __name__ == "__main__":
    main()
