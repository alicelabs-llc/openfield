import json, re, ssl, urllib.request, time

with open('results_v3.json') as f:
    data = json.load(f)

ctx = ssl.create_default_context()
patterns = [
    (re.compile(r'\$\s?(\d{1,3}(?:[,\d]{0,9}))\b'), 'dollar'),
    (re.compile(r'(?<!EIP-)(?<!RFC-)\b(\d{2,6})\s?USDC\b', re.IGNORECASE), 'N USDC'),
    (re.compile(r'\b(\d{2,6})\s?USD\b', re.IGNORECASE), 'N USD'),
    (re.compile(r'\b(\d+(?:\.\d+)?)\s?(ETH|SOL|BTC|DAI|MATIC)\b', re.IGNORECASE), 'crypto'),
    (re.compile(r'\b(?:bounty|reward|payout|prize)[:\s]*\$?\s?(\d{2,6}(?:[,\d]{0,9}))', re.IGNORECASE), 'bounty kw'),
]
units = {'ETH':3000,'SOL':150,'BTC':65000,'DAI':1,'MATIC':0.7}

print('Re-verifying rewards by fetching fresh body:')
results = []
for e in data['top_20']:
    api_url = e['url'].replace('https://github.com/', 'https://api.github.com/repos/').replace('/issues/', '/issues/')
    try:
        req = urllib.request.Request(api_url, headers={'User-Agent':'x','Accept':'application/vnd.github+json'})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
            full = json.loads(r.read().decode())
        body = full.get('body','') or ''
        title = full.get('title','')
        haystack = title + '\n' + body
    except Exception as ex:
        print(f'  {e["repo"]} #{e["number"]}  ERROR: {ex}')
        results.append((e, 0.0, []))
        time.sleep(2)
        continue
    matches = []
    for p, name in patterns:
        for m in p.finditer(haystack):
            ctx_txt = haystack[max(0,m.start()-30):m.end()+15].replace('\n',' ')
            matches.append((name, m.group(0), m.group(1), ctx_txt))
    # Determine verified reward
    real = 0.0
    for name, full_m, val_str, ctx_txt in matches:
        try:
            v = float(val_str.replace(',',''))
        except: continue
        if not (25 <= v <= 100000): continue
        if name == 'dollar':
            real = max(real, v)
        elif name == 'N USDC' and 'EIP' not in ctx_txt:
            real = max(real, v)
        elif name == 'N USD':
            real = max(real, v)
        elif name == 'crypto':
            m2 = re.match(r'(\d+(?:\.\d+)?)\s?(ETH|SOL|BTC|DAI|MATIC)', full_m, re.IGNORECASE)
            if m2:
                v2 = float(m2.group(1)) * units.get(m2.group(2).upper(), 1)
                if 25 <= v2 <= 100000:
                    real = max(real, v2)
    results.append((e, real, matches))
    print(f'  {e["repo"][:38]:<38} #{e["number"]:<6}  verified=\${real:.2f}  (orig=\${e["reward_usd"]:.2f})')
    for name, full_m, val_str, ctx_txt in matches[:2]:
        print(f'      [{name}] {full_m!r}  ctx="{ctx_txt}"')
    time.sleep(2)  # avoid core api rate limit (60/hr)

# Save verified results
out = []
for e, verified, matches in results:
    out.append({**e, 'verified_reward_usd': verified, 'match_evidence': matches[:5]})
with open('results_verified.json','w') as f:
    json.dump(out, f, indent=2, default=str)
print(f'\nWrote verified results to results_verified.json')
