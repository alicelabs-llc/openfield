#!/usr/bin/env python3
"""
Consolidate Reddit DDG results + oembed enrichment + date estimate into scored leads.
Inputs:
  - reddit/ddg_reddit_all.json   (dict of query -> [{title,url,snippet}])
  - reddit/q3_freelance_v3.json  (same format)
  - reddit/enriched.json         (list of {url, author, title, subreddit, ok})
Output:
  - reddit/scored.json           (sorted scored leads)
"""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from score_leads import score_lead, is_warm
sys.path.insert(0, os.path.dirname(__file__))
from reddit_date import pid_to_approx_year_month

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)

def extract_pid(url):
    """Extract post ID (e.g. '1bmz5ej') from reddit URL."""
    m = re.search(r'/comments/([a-z0-9]{5,8})/', url)
    return m.group(1) if m else None

def main():
    # 1. Load all DDG results
    ddg_results = {}
    for fname in ['reddit/ddg_reddit_all.json', 'reddit/q3_freelance_v3.json']:
        d = load_json(fname)
        for q, results in d.items():
            if not results or 'error' in results[0]:
                continue
            ddg_results[q] = results
    # 2. Load oembed enrichment
    enriched = {r['url']: r for r in load_json('reddit/enriched.json') if r.get('ok')}
    # 3. Combine
    leads = []
    seen_urls = set()
    for q, results in ddg_results.items():
        for r in results:
            url = r.get('url','')
            if url in seen_urls or not url:
                continue
            seen_urls.add(url)
            e = enriched.get(url, {})
            pid = extract_pid(url)
            date_est = pid_to_approx_year_month(pid) if pid else "unknown"
            lead = {
                "query": q,
                "url": url,
                "ddg_title": r.get('title',''),
                "snippet": r.get('snippet',''),
                "subreddit": e.get('subreddit',''),
                "author": e.get('author',''),
                "post_title": e.get('title',''),
                "date_estimated": date_est,
                "post_id": pid,
            }
            text = " ".join(filter(None, [lead['ddg_title'], lead['snippet'], lead['post_title']]))
            s = score_lead(text)
            lead['matches'] = s['matches']
            lead['score'] = s['score']
            warm, why = is_warm(text)
            lead['warm'] = warm
            if warm:
                lead['warm_marker'] = why
            leads.append(lead)
    # 4. Sort by score desc, then warm first
    leads.sort(key=lambda x: (-x['score'], -int(x['warm'])))
    out_path = 'reddit/scored.json'
    with open(out_path, 'w') as f:
        json.dump(leads, f, ensure_ascii=False, indent=2)
    print(f"[consolidate] {len(leads)} leads -> {out_path}", file=sys.stderr)
    # Top 12 summary
    print("\n=== TOP 12 REDDIT LEADS ===", file=sys.stderr)
    for l in leads[:12]:
        warm_tag = "🔥WARM" if l.get('warm') else "    "
        print(f"{l['score']}★ {warm_tag} | r/{l['subreddit']:12s} | {l['author'][:18]:18s} | {l['post_title'][:60]}", file=sys.stderr)
        print(f"     date~{l['date_estimated']:18s} | {l['url']}", file=sys.stderr)
        print(f"     matches: {','.join(l['matches'])}", file=sys.stderr)

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')
    main()
