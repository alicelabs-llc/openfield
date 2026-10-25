"""Bulk scan a list of URLs from a CSV.

CSV format:
    url,expected_safe
    https://example.com,1
    https://suspicious-site.xyz,0

Outputs a JSON report + writes results to bulk_report.json.
"""
import asyncio
import csv
import json
import sys
from pathlib import Path

from scamshield.core.models import ScanRequest
from scamshield.scanner import Scanner


async def main(csv_path: str):
    p = Path(csv_path)
    if not p.exists():
        print(f"File not found: {csv_path}", file=sys.stderr)
        sys.exit(1)

    rows = list(csv.DictReader(p.open()))
    if not rows:
        print("CSV is empty", file=sys.stderr)
        sys.exit(1)

    scanner = Scanner(parallel=False)
    results = []
    for i, row in enumerate(rows, 1):
        url = row.get("url", "").strip()
        if not url:
            continue
        print(f"[{i}/{len(rows)}] Scanning {url} ...")
        try:
            r = await scanner.scan(ScanRequest(url=url))
            results.append({
                "url": url,
                "expected_safe": row.get("expected_safe"),
                "score": r.trust_score.value,
                "verdict": r.trust_score.verdict.value,
                "duration_ms": r.duration_ms,
            })
            print(f"  → {r.trust_score.verdict.emoji} {r.trust_score.value}/100")
        except Exception as e:
            print(f"  ✗ Error: {e}")

    # Write report
    out = Path("bulk_report.json")
    out.write_text(json.dumps(results, indent=2))
    print(f"\nReport saved to {out.resolve()}")

    # Summary
    total = len(results)
    safe = sum(1 for r in results if r["score"] >= 61)
    unsafe = sum(1 for r in results if r["score"] < 41)
    mid = total - safe - unsafe
    print(f"\nSummary: {total} scanned — {safe} safe, {mid} caution, {unsafe} unsafe")


if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "urls.csv"
    asyncio.run(main(csv_path))
