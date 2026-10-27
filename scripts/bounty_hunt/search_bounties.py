"""
Search GitHub for open bounty issues matching a Python/TS/Rust/MCP/crypto security skill profile.

NOTE: The user-requested source (scripts/investigate_surprises.py) had its ghp_ token REDACTED
to "[REDACTED:github_token]". All other scripts in /home/z/my-project/scripts/*.py have the same
redaction. No token exists in env vars or .git-credentials. We therefore fall back to the
unauthenticated GitHub Search API, which permits 10 requests per minute.

To stay within the budget we issue 8 strategic search queries that maximise coverage:

  1. label:bounty  + (MCP OR agent OR trust OR attestation OR signature OR verification)
  2. label:bounty  + (Ed25519 OR "key agreement" OR "credential" OR "identity" OR "decentralized identifier")
  3. label:bounty  + (Python OR TypeScript OR Rust OR "machine learning" OR "AI security")
  4. label:"good first issue" + bounty (title or body)
  5. label:help wanted + bounty + (MCP OR agent OR crypto OR signature)
  6. body mentions algora.io bounties (state:open)
  7. body mentions opire.dev / opirebot bounties (state:open)
  8. title contains bounty + (USDC OR USD OR crypto OR x402 OR SOL)

Each query returns up to 30 issues (per_page=30, sorted by created desc). We aggregate,
deduplicate, extract reward amounts from title/body/labels, and emit a sorted table.
"""
import json
import re
import ssl
import sys
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone

# Unauthenticated GitHub Search API headers
HEADERS = {
    "User-Agent": "bounty-hunter-probe/1.0 (+research)",
    "Accept": "application/vnd.github+json",
}
CTX = ssl.create_default_context()

# Skill-aligned keyword queries
QUERIES = [
    # 1. MCP / agent / trust / verification / signature
    'label:bounty state:open type:issue '
    '(MCP OR "Model Context Protocol" OR agent OR trust OR attestation OR signature OR verification)',

    # 2. Cryptography / identity / credentials
    'label:bounty state:open type:issue '
    '(Ed25519 OR "key agreement" OR credential OR "self-sovereign" OR "decentralized identifier" OR DID OR "zero knowledge")',

    # 3. Languages + AI security
    'label:bounty state:open type:issue '
    '(Python OR TypeScript OR Rust OR "AI security" OR "machine learning" OR LLM OR "prompt injection")',

    # 4. Good first issue + bounty
    'label:"good first issue" state:open type:issue bounty',

    # 5. Help wanted + bounty + skill keyword
    'label:"help wanted" state:open type:issue bounty (MCP OR agent OR crypto OR signature OR Ed25519 OR x402)',

    # 6. Algora-funded bounties (their marker is "algora.io" in body)
    'state:open type:issue "algora.io" in:body bounty',

    # 7. Opire-funded bounties
    'state:open type:issue ("opire.dev" OR "@opirebot") in:body bounty',

    # 8. Title bounties with USDC/USD/crypto
    'bounty in:title state:open type:issue (USDC OR USD OR crypto OR x402 OR SOL OR ETH)',
]

# Aggregators to ignore (per task instructions)
AGGREGATOR_DENYLIST = {
    "algora-io/bounty-plaza",
    "algora-io/bounty",
    "opire-dev/opire",
    "opirebot",
    "oss-bounty-aggregator",
    "whilefoo/bounties",
    "issuehunt/issuehunt",
    "boss-dev/boss",
    "bossdev",
}


def gh_search(query: str, per_page: int = 30, sort: str = "created", order: str = "desc", attempt: int = 1):
    """Run a single GitHub search query. Returns (status_code, json_dict_or_str)."""
    url = (
        "https://api.github.com/search/issues?"
        + urllib.parse.urlencode(
            {
                "q": query,
                "sort": sort,
                "order": order,
                "per_page": per_page,
            }
        )
    )
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:400]
        # If rate-limited, wait and retry once
        if e.code == 403 and "rate limit" in body.lower() and attempt <= 2:
            wait = 60
            print(f"  [rate-limit] waiting {wait}s before retry...", file=sys.stderr)
            time.sleep(wait)
            return gh_search(query, per_page, sort, order, attempt + 1)
        return e.code, {"error": body}
    except Exception as e:
        return -1, {"error": str(e)}


# Reward extraction: $ amounts, USDC, ETH, SOL, BTC etc.
REWARD_PATTERNS = [
    # USD / dollar amounts
    re.compile(r"\$\s?(\d{1,3}(?:[,\d]{1,9})?)\b"),
    re.compile(r"\b(\d{2,5})\s?USD\b", re.IGNORECASE),
    re.compile(r"\b(\d{2,5})\s?USDC\b", re.IGNORECASE),
    re.compile(r"\b(\d{2,5})\s?USDT\b", re.IGNORECASE),
    # Crypto amounts (rough USD equivalents computed later)
    re.compile(r"\b(\d+(?:\.\d+)?)\s?(ETH|SOL|BTC|DAI|USDT|USDC|MATIC)\b", re.IGNORECASE),
    re.compile(r"\bbounty[:\s]*\$?\s?(\d{1,5}(?:[,\d]{1,9})?)", re.IGNORECASE),
    re.compile(r"\breward[:\s]*\$?\s?(\d{1,5}(?:[,\d]{1,9})?)", re.IGNORECASE),
    re.compile(r"\bpayout[:\s]*\$?\s?(\d{1,5}(?:[,\d]{1,9})?)", re.IGNORECASE),
]

# Approximate USD conversion for crypto
CRYPTO_USD = {
    "ETH": 3000,
    "SOL": 150,
    "BTC": 65000,
    "DAI": 1,
    "USDT": 1,
    "USDC": 1,
    "MATIC": 0.7,
}


def extract_reward(text: str) -> float | None:
    """Return the highest plausible reward (in USD) found in text, or None."""
    if not text:
        return None
    amounts: list[float] = []
    for pat in REWARD_PATTERNS:
        for m in pat.finditer(text):
            val_str = m.group(1)
            try:
                val = float(val_str.replace(",", ""))
            except ValueError:
                continue
            # Crypto with unit
            if pat.groups >= 2 and m.lastindex and m.lastindex >= 2:
                unit = m.group(2).upper() if m.lastindex >= 2 else ""
                if unit in CRYPTO_USD:
                    val = val * CRYPTO_USD[unit]
            # Sanity bounds: $10 to $100,000
            if 10 <= val <= 100_000:
                amounts.append(val)
    if not amounts:
        return None
    return max(amounts)


def parse_iso(ts: str | None) -> datetime | None:
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None


def repo_full_name(issue_url: str) -> str:
    # issue_url like https://api.github.com/repos/OWNER/REPO/issues/N
    m = re.search(r"/repos/([^/]+/[^/]+)/issues/", issue_url)
    return m.group(1) if m else "?"


def is_aggregator(repo: str) -> bool:
    repo_lc = repo.lower()
    for agg in AGGREGATOR_DENYLIST:
        if agg.lower() in repo_lc:
            return True
    return False


def collect_issue(raw: dict, source_query: str) -> dict | None:
    if not isinstance(raw, dict) or "id" not in raw:
        return None
    repo = repo_full_name(raw.get("repository_url", ""))
    if is_aggregator(repo):
        return None
    title = raw.get("title", "")
    body = raw.get("body", "") or ""
    labels = [l.get("name", "") for l in (raw.get("labels") or [])]
    label_blob = " ".join(labels)
    haystack = f"{title}\n{body}\n{label_blob}"
    reward = extract_reward(haystack) or 0.0

    # Skip "claim" / "tutorial" / "how-to" issues that aren't real bounties
    title_lc = title.lower()
    SKIP_TOKENS = (
        "how to claim", "how-to-claim", "claimable bounties",
        "list of bounties", "bounty board", "bounty program overview",
        "track bounties", "bounty guide",
    )
    if any(tok in title_lc for tok in SKIP_TOKENS):
        return None

    assignee = raw.get("assignee")
    assignees = raw.get("assignees") or []
    is_assigned = bool(assignee) or bool(assignees)
    comments = raw.get("comments", 0) or 0
    created = parse_iso(raw.get("created_at"))
    html_url = raw.get("html_url", "")
    number = raw.get("number")
    state = raw.get("state", "open")

    return {
        "repo": repo,
        "number": number,
        "title": title,
        "reward_usd": reward,
        "comments": comments,
        "assigned": is_assigned,
        "assignee_login": (assignee or {}).get("login") if assignee else None,
        "created_at": raw.get("created_at"),
        "url": html_url,
        "labels": labels,
        "state": state,
        "source_query": source_query,
        "body_excerpt": body[:200].replace("\n", " ") if body else "",
    }


def main():
    all_results: dict[int, dict] = {}  # dedupe by issue id (raw.get('id'))

    for idx, q in enumerate(QUERIES, start=1):
        print(f"\n=== Query {idx}/{len(QUERIES)} ===")
        print(f"  {q[:160]}{'...' if len(q) > 160 else ''}")
        status, payload = gh_search(q, per_page=30)
        if status != 200 or not isinstance(payload, dict):
            print(f"  ! HTTP {status}: {str(payload)[:200]}")
            # Backoff before next attempt
            time.sleep(8)
            continue
        items = payload.get("items", [])
        total = payload.get("total_count", 0)
        print(f"  total_count={total}, returned={len(items)}")
        for it in items:
            entry = collect_issue(it, q)
            if not entry:
                continue
            iid = it.get("id")
            # If we've already seen this issue, keep the max reward estimate
            if iid in all_results:
                existing = all_results[iid]
                if entry["reward_usd"] > existing["reward_usd"]:
                    existing["reward_usd"] = entry["reward_usd"]
                existing["source_query"] = existing["source_query"] + " | " + q[:60]
                continue
            all_results[iid] = entry
        # Polite delay to spread requests across the rate window
        time.sleep(6)

    # ---- Filtering ----
    # Per task: NOT assigned, <5 comments, $100+ reward (lower bar if no reward found but skill match)
    candidates = []
    for e in all_results.values():
        if e["state"] != "open":
            continue
        if e["assigned"]:
            continue
        if e["comments"] >= 5:
            continue
        # Reward filter: $100+ if we could detect a number; otherwise keep only
        # those with at least one skill keyword in title/body (heuristic)
        skill_kws = (
            "mcp", "model context protocol", "agent", "trust", "attestation",
            "signature", "ed25519", "verification", "identity", "credential",
            "security", "python", "typescript", "rust", "x402", "crypto",
            "ai/ml", "ml", "llm", "prompt injection",
        )
        text_lc = (e["title"] + " " + e["body_excerpt"] + " " + " ".join(e["labels"])).lower()
        skill_match = any(kw in text_lc for kw in skill_kws)
        if e["reward_usd"] >= 100:
            candidates.append(e)
        elif e["reward_usd"] > 0:
            # Reward detected but <$100; keep if skill-aligned, otherwise skip
            if skill_match:
                candidates.append(e)
        else:
            # No reward detected — keep only if strongly skill-aligned AND
            # explicitly labelled "bounty"
            if "bounty" in (l.lower() for l in e["labels"]) and skill_match:
                # mark reward as unknown
                e["reward_usd"] = 0.0
                candidates.append(e)

    # ---- Sorting: by reward desc (ties broken by fewer comments, then newer) ----
    def sort_key(e):
        created = parse_iso(e.get("created_at")) or datetime.min.replace(tzinfo=timezone.utc)
        # Higher reward first; if reward is 0 (unknown), treat as -1 so known rewards outrank unknown
        reward_for_sort = e["reward_usd"] if e["reward_usd"] > 0 else -1
        return (-reward_for_sort, e["comments"], -created.timestamp())

    candidates.sort(key=sort_key)

    # ---- Top 20 ----
    top = candidates[:20]

    # ---- Output JSON + Markdown ----
    out_json = {
        "queries_run": len(QUERIES),
        "total_unique_issues_seen": len(all_results),
        "candidates_after_filter": len(candidates),
        "top_20": top,
        "note": (
            "GitHub token was redacted in source files; used unauthenticated "
            "GitHub Search API (10 req/min budget). 8 strategic queries executed."
        ),
    }
    out_path = "/home/z/my-project/scripts/bounty_hunt/results.json"
    with open(out_path, "w") as f:
        json.dump(out_json, f, indent=2, default=str)
    print(f"\nWrote JSON to {out_path}")
    print(f"Unique issues seen: {len(all_results)}")
    print(f"Candidates after filter: {len(candidates)}")
    print(f"Top 20 selected: {len(top)}")
    print()
    # Print a compact table
    print("=" * 130)
    print(f"{'#':>3}  {'$':>8}  {'cmt':>4}  {'repo':<45}  {'#':>6}  title")
    print("-" * 130)
    for i, e in enumerate(top, 1):
        reward_str = f"${e['reward_usd']:.0f}" if e["reward_usd"] > 0 else "?"
        repo_short = e["repo"] if len(e["repo"]) <= 45 else e["repo"][:42] + "..."
        title_short = e["title"][:60] + ("..." if len(e["title"]) > 60 else "")
        print(f"{i:>3}  {reward_str:>8}  {e['comments']:>4}  {repo_short:<45}  #{e['number']:<5} {title_short}")
    print("=" * 130)


if __name__ == "__main__":
    main()
