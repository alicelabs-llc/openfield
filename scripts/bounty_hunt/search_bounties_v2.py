"""
Refined bounty search — v2.

Key fixes from v1:
  * Repo name extracted from `html_url` (was reading wrong field).
  * Reward regex now excludes 4-digit "year-like" numbers (1900-2099) that
    previously matched e.g. "2026-10-22T19:11" -> $2026 false positive.
  * Queries 1-3 (which had >5 OR operators and 422'd) are split into
    multiple sub-queries with ≤5 OR operands each.
  * Added targeted queries:
      - label:bounty + crypto/x402 keyword
      - label:bounty + Ed25519/identity/credential
      - "label:bounty 💰" emoji variant
      - Algora-funded issues only (label:bounty in:body "https://algora.io")
      - Opire-funded issues only (label:bounty in:body "https://opire.dev")
      - Specific high-value MCP / agent security repos via in:body
  * Per-issue metadata (assignee, comments, created_at) already present in
    search results, so no additional /repos API calls are needed.
"""
import json
import re
import ssl
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

HEADERS = {
    "User-Agent": "bounty-hunter-probe/1.0 (+research)",
    "Accept": "application/vnd.github+json",
}
CTX = ssl.create_default_context()

# Split into smaller queries — max 5 OR operands per GitHub search query
QUERIES = [
    # --- label:bounty + skill keywords (split into 4 sub-queries) ---
    'label:bounty state:open type:issue (MCP OR "Model Context Protocol" OR agent OR trust OR attestation)',
    'label:bounty state:open type:issue (signature OR verification OR Ed25519 OR "key agreement")',
    'label:bounty state:open type:issue (credential OR identity OR "zero knowledge" OR DID)',
    'label:bounty state:open type:issue (Python OR TypeScript OR Rust OR "AI security" OR LLM)',

    # --- "good first issue" + bounty ---
    'label:"good first issue" state:open type:issue bounty in:title',

    # --- "help wanted" + bounty + skill keyword ---
    'label:"help wanted" state:open type:issue bounty in:title (MCP OR agent OR crypto OR signature OR Ed25519 OR x402)',

    # --- Algora-funded (real algora.io URL in body) ---
    'state:open type:issue "https://algora.io" in:body',

    # --- Opire-funded (real opire.dev URL in body) ---
    'state:open type:issue "https://opire.dev" in:body',

    # --- Title-based crypto bounties (split) ---
    'bounty in:title state:open type:issue (USDC OR USD OR "$" OR crypto OR x402 OR SOL OR ETH)',
]

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
    "fu-rong-jun/dsh-bounty",  # false-positive aggregator pattern
    "furongjun",
    "relayhop/sn-monetization-runtime",  # radar noise tracker
}


def gh_search(query: str, per_page: int = 30, sort: str = "created", order: str = "desc", attempt: int = 1):
    url = (
        "https://api.github.com/search/issues?"
        + urllib.parse.urlencode({"q": query, "sort": sort, "order": order, "per_page": per_page})
    )
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:400]
        if e.code == 403 and "rate limit" in body.lower() and attempt <= 2:
            wait = 62
            print(f"  [rate-limit] waiting {wait}s before retry...", file=sys.stderr)
            time.sleep(wait)
            return gh_search(query, per_page, sort, order, attempt + 1)
        return e.code, {"error": body}
    except Exception as e:
        return -1, {"error": str(e)}


REWARD_PATTERNS = [
    # USD / dollar amounts — explicit $ prefix
    re.compile(r"\$\s?(\d{1,3}(?:[,\d]{0,9}))\b"),
    # "USD 500" or "500 USD"
    re.compile(r"\b(\d{2,6})\s?USD\b", re.IGNORECASE),
    re.compile(r"\b(\d{2,6})\s?USDC\b", re.IGNORECASE),
    re.compile(r"\b(\d{2,6})\s?USDT\b", re.IGNORECASE),
    # Crypto amounts with unit
    re.compile(r"\b(\d+(?:\.\d+)?)\s?(ETH|SOL|BTC|DAI|MATIC)\b", re.IGNORECASE),
    # "bounty: $500" / "reward: $1000" / "payout: $250"
    re.compile(r"\b(?:bounty|reward|payout|prize)[:\s]*\$?\s?(\d{2,6}(?:[,\d]{0,9}))", re.IGNORECASE),
]

CRYPTO_USD = {
    "ETH": 3000,
    "SOL": 150,
    "BTC": 65000,
    "DAI": 1,
    "MATIC": 0.7,
}

# Regexes that look like dates / year-only numbers and should be rejected
YEAR_RE = re.compile(r"^\d{4}$")


def extract_reward(text: str) -> float | None:
    """Return the highest plausible reward (USD) found in text, or None."""
    if not text:
        return None
    amounts: list[float] = []
    for pat in REWARD_PATTERNS:
        for m in pat.finditer(text):
            val_str = m.group(1).replace(",", "").rstrip(".")
            try:
                val = float(val_str)
            except ValueError:
                continue
            # Reject 4-digit year-like numbers (1900-2099) when from $ prefix pattern
            if YEAR_RE.match(val_str) and 1900 <= val <= 2099:
                continue
            # Crypto with unit
            if m.lastindex and m.lastindex >= 2:
                unit = m.group(2).upper() if m.lastindex >= 2 else ""
                if unit in CRYPTO_USD:
                    val = val * CRYPTO_USD[unit]
            # Sanity bounds: $25 to $100,000
            if 25 <= val <= 100_000:
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


def repo_from_html_url(html_url: str) -> str:
    # https://github.com/OWNER/REPO/issues/N
    m = re.match(r"https?://github\.com/([^/]+/[^/]+)/", html_url or "")
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
    html_url = raw.get("html_url", "")
    repo = repo_from_html_url(html_url)
    if is_aggregator(repo):
        return None
    title = raw.get("title", "")
    body = raw.get("body", "") or ""
    labels = [l.get("name", "") for l in (raw.get("labels") or [])]
    label_blob = " ".join(labels)
    haystack = f"{title}\n{body}\n{label_blob}"
    reward = extract_reward(haystack) or 0.0

    title_lc = title.lower()
    SKIP_TOKENS = (
        "how to claim", "how-to-claim", "claimable bounties",
        "list of bounties", "bounty board", "bounty program overview",
        "track bounties", "bounty guide", "bounty alert", "open bounties right now",
        "open bounties available", "[radar]", "intake 输入",
    )
    if any(tok in title_lc for tok in SKIP_TOKENS):
        return None

    assignee = raw.get("assignee")
    assignees = raw.get("assignees") or []
    is_assigned = bool(assignee) or bool(assignees)
    comments = raw.get("comments", 0) or 0
    created = parse_iso(raw.get("created_at"))
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
        "body_excerpt": body[:300].replace("\n", " ") if body else "",
    }


def main():
    all_results: dict[int, dict] = {}

    for idx, q in enumerate(QUERIES, start=1):
        print(f"\n=== Query {idx}/{len(QUERIES)} ===")
        print(f"  {q[:170]}{'...' if len(q) > 170 else ''}")
        status, payload = gh_search(q, per_page=30)
        if status != 200 or not isinstance(payload, dict):
            print(f"  ! HTTP {status}: {str(payload)[:200]}")
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
            if iid in all_results:
                existing = all_results[iid]
                if entry["reward_usd"] > existing["reward_usd"]:
                    existing["reward_usd"] = entry["reward_usd"]
                if q[:60] not in existing["source_query"]:
                    existing["source_query"] = existing["source_query"] + " | " + q[:60]
                continue
            all_results[iid] = entry
        time.sleep(7)  # spread across rate window

    # ---- Filtering ----
    candidates = []
    for e in all_results.values():
        if e["state"] != "open":
            continue
        if e["assigned"]:
            continue
        if e["comments"] >= 5:
            continue
        skill_kws = (
            "mcp", "model context protocol", "agent", "trust", "attestation",
            "signature", "ed25519", "verification", "identity", "credential",
            "security", "python", "typescript", "rust", "x402", "crypto",
            "ai/ml", "ml ", "llm", "prompt injection", "zero knowledge",
            " did ", "did:", "self-sovereign", "verifiable", "wallet",
            "signing", "key agreement", "session",
        )
        text_lc = (e["title"] + " " + e["body_excerpt"] + " " + " ".join(e["labels"])).lower()
        skill_match = any(kw in text_lc for kw in skill_kws)
        if e["reward_usd"] >= 100:
            candidates.append(e)
        elif e["reward_usd"] > 0:
            if skill_match:
                candidates.append(e)
        else:
            # Reward unknown — keep only if explicitly labelled "bounty" AND skill-aligned
            if "bounty" in (l.lower() for l in e["labels"]) and skill_match:
                e["reward_usd"] = 0.0
                candidates.append(e)

    def sort_key(e):
        created = parse_iso(e.get("created_at")) or datetime.min.replace(tzinfo=timezone.utc)
        reward_for_sort = e["reward_usd"] if e["reward_usd"] > 0 else -1
        return (-reward_for_sort, e["comments"], -created.timestamp())

    candidates.sort(key=sort_key)
    top = candidates[:20]

    out_json = {
        "queries_run": len(QUERIES),
        "total_unique_issues_seen": len(all_results),
        "candidates_after_filter": len(candidates),
        "top_20": top,
        "note": (
            "GitHub token was redacted in source files; used unauthenticated "
            "GitHub Search API (10 req/min budget). Queries split to respect "
            "GitHub's 5-OR-operator cap."
        ),
    }
    out_path = "/home/z/my-project/scripts/bounty_hunt/results_v2.json"
    with open(out_path, "w") as f:
        json.dump(out_json, f, indent=2, default=str)
    print(f"\nWrote JSON to {out_path}")
    print(f"Unique issues seen: {len(all_results)}")
    print(f"Candidates after filter: {len(candidates)}")
    print(f"Top 20 selected: {len(top)}")
    print()
    print("=" * 150)
    print(f"{'#':>3}  {'$':>8}  {'cmt':>4}  {'created':<10}  {'repo':<48}  {'#':>6}  title")
    print("-" * 150)
    for i, e in enumerate(top, 1):
        reward_str = f"${e['reward_usd']:.0f}" if e["reward_usd"] > 0 else "?"
        repo_short = e["repo"] if len(e["repo"]) <= 48 else e["repo"][:45] + "..."
        title_short = e["title"][:55] + ("..." if len(e["title"]) > 55 else "")
        created_short = (e["created_at"] or "")[:10]
        print(f"{i:>3}  {reward_str:>8}  {e['comments']:>4}  {created_short:<10}  {repo_short:<48}  #{e['number']:<5} {title_short}")
    print("=" * 150)


if __name__ == "__main__":
    main()
