"""
Refined bounty search — v3.

Adds targeted follow-up queries based on v2 findings:
  * Split crypto/title queries to respect 5-OR cap
  * Specifically scan algora.io bounties for skill matches
  * Search for x402 / crypto payment bounties
  * Look for high-reward ($500+) bounties in title

Also: don't filter out algora bounties just for lacking skill keywords in
their issue body — if the algora funding is set and reward >= $100, keep it.
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

# Load v2 results so we can merge
V2_PATH = "/home/z/my-project/scripts/bounty_hunt/results_v2.json"
OUT_PATH = "/home/z/my-project/scripts/bounty_hunt/results_v3.json"

# Additional queries — each respects 5-OR cap
EXTRA_QUERIES = [
    # Crypto title bounties, split (≤5 OR each)
    'bounty in:title state:open type:issue (USDC OR USD OR "$")',
    'bounty in:title state:open type:issue (crypto OR x402 OR SOL OR ETH)',
    # Algora-funded with skill keywords
    'state:open type:issue "https://algora.io" in:body (MCP OR agent OR security OR Python OR Rust)',
    # x402-specific
    'state:open type:issue x402 in:title,body',
    # High-reward bounties
    'state:open type:issue label:bounty "$500" OR "$1000" OR "$2000" OR "$5000"',
    # Updated-most-recently skill bounties (sort:updated not allowed on search/issues;
    # use created desc as proxy)
    'state:open type:issue label:bounty (MCP OR agent OR trust OR Ed25519) sort:created',
]

AGGREGATOR_DENYLIST = {
    "algora-io/bounty-plaza",
    "zhangjiayang6835-cyber/bounty-plaza",  # mirror of bounty-plaza
    "furongjun",
    "fu-rong-jun/dsh-bounty",
    "relayhop/sn-monetization-runtime",
    "whilefoo/bounties",
    "issuehunt",
    "boss-dev/boss",
    "bossdev",
    "opire-dev/opire",
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
    re.compile(r"\$\s?(\d{1,3}(?:[,\d]{0,9}))\b"),
    re.compile(r"\b(\d{2,6})\s?USD\b", re.IGNORECASE),
    re.compile(r"\b(\d{2,6})\s?USDC\b", re.IGNORECASE),
    re.compile(r"\b(\d{2,6})\s?USDT\b", re.IGNORECASE),
    re.compile(r"\b(\d+(?:\.\d+)?)\s?(ETH|SOL|BTC|DAI|MATIC)\b", re.IGNORECASE),
    re.compile(r"\b(?:bounty|reward|payout|prize)[:\s]*\$?\s?(\d{2,6}(?:[,\d]{0,9}))", re.IGNORECASE),
]

CRYPTO_USD = {
    "ETH": 3000, "SOL": 150, "BTC": 65000, "DAI": 1, "MATIC": 0.7,
}

YEAR_RE = re.compile(r"^\d{4}$")


def extract_reward(text: str) -> float | None:
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
            if YEAR_RE.match(val_str) and 1900 <= val <= 2099:
                continue
            if m.lastindex and m.lastindex >= 2:
                unit = m.group(2).upper() if m.lastindex >= 2 else ""
                if unit in CRYPTO_USD:
                    val = val * CRYPTO_USD[unit]
            if 25 <= val <= 100_000:
                amounts.append(val)
    return max(amounts) if amounts else None


def parse_iso(ts: str | None) -> datetime | None:
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None


def repo_from_html_url(html_url: str) -> str:
    m = re.match(r"https?://github\.com/([^/]+/[^/]+)/", html_url or "")
    return m.group(1) if m else "?"


def is_aggregator(repo: str) -> bool:
    repo_lc = repo.lower()
    for agg in AGGREGATOR_DENYLIST:
        if agg.lower() in repo_lc:
            return True
    return False


SKIP_TOKENS = (
    "how to claim", "how-to-claim", "claimable bounties",
    "list of bounties", "bounty board", "bounty program overview",
    "track bounties", "bounty guide", "bounty alert",
    "open bounties right now", "open bounties available",
    "[radar]", "intake 输入",
)


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
    if any(tok in title_lc for tok in SKIP_TOKENS):
        return None

    assignee = raw.get("assignee")
    assignees = raw.get("assignees") or []
    is_assigned = bool(assignee) or bool(assignees)
    comments = raw.get("comments", 0) or 0
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
        "body_excerpt": body[:400].replace("\n", " ") if body else "",
    }


def main():
    # Load v2 baseline
    try:
        with open(V2_PATH) as f:
            v2_data = json.load(f)
        all_results = {e["url"]: e for e in v2_data.get("top_20", [])}
        # v2 only stored top 20, so we have a partial set. Also keep their
        # candidate pool by re-collecting from the search.
        print(f"Loaded {len(all_results)} entries from v2 baseline")
    except FileNotFoundError:
        all_results = {}

    # Re-run all queries (v2's 9 + v3's 6 extra) — but we've already used
    # v2's searches, so we don't re-run those. Just do EXTRA_QUERIES.
    new_count = 0
    for idx, q in enumerate(EXTRA_QUERIES, start=1):
        print(f"\n=== Extra Query {idx}/{len(EXTRA_QUERIES)} ===")
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
            url = entry["url"]
            if url in all_results:
                existing = all_results[url]
                if entry["reward_usd"] > existing["reward_usd"]:
                    existing["reward_usd"] = entry["reward_usd"]
                if q[:60] not in existing["source_query"]:
                    existing["source_query"] = existing["source_query"] + " | " + q[:60]
                continue
            all_results[url] = entry
            new_count += 1
        time.sleep(7)

    print(f"\nNew entries added by extra queries: {new_count}")
    print(f"Total unique entries: {len(all_results)}")

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
            "signing", "key agreement", "usdc", "stellar", "ethereum",
            "solana", "kernel", "cve", "threat", "bm25", "idf", "retrieval",
            "moe", "tensor", "autonomous", "swarm",
        )
        text_lc = (e["title"] + " " + e["body_excerpt"] + " " + " ".join(e["labels"])).lower()
        skill_match = any(kw in text_lc for kw in skill_kws)
        if e["reward_usd"] >= 100:
            candidates.append(e)
        elif e["reward_usd"] > 0:
            if skill_match:
                candidates.append(e)
        else:
            # Reward unknown — keep if labelled bounty AND skill-aligned
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
        "queries_run_v2": 9,
        "queries_run_v3_extra": len(EXTRA_QUERIES),
        "total_unique_issues_seen": len(all_results),
        "candidates_after_filter": len(candidates),
        "top_20": top,
        "note": (
            "GitHub token was redacted in source files; used unauthenticated "
            "GitHub Search API (10 req/min budget). v2 ran 9 queries (3 of "
            "which 422'd due to >5 OR operands). v3 ran 6 additional targeted "
            "queries and merged results."
        ),
    }
    with open(OUT_PATH, "w") as f:
        json.dump(out_json, f, indent=2, default=str)
    print(f"\nWrote JSON to {OUT_PATH}")
    print(f"Unique issues seen: {len(all_results)}")
    print(f"Candidates after filter: {len(candidates)}")
    print(f"Top 20 selected: {len(top)}")
    print()
    print("=" * 160)
    print(f"{'#':>3}  {'$':>8}  {'cmt':>4}  {'created':<10}  {'repo':<48}  {'#':>6}  title")
    print("-" * 160)
    for i, e in enumerate(top, 1):
        reward_str = f"${e['reward_usd']:.0f}" if e["reward_usd"] > 0 else "?"
        repo_short = e["repo"] if len(e["repo"]) <= 48 else e["repo"][:45] + "..."
        title_short = e["title"][:55] + ("..." if len(e["title"]) > 55 else "")
        created_short = (e["created_at"] or "")[:10]
        print(f"{i:>3}  {reward_str:>8}  {e['comments']:>4}  {created_short:<10}  {repo_short:<48}  #{e['number']:<5} {title_short}")
    print("=" * 160)


if __name__ == "__main__":
    main()
