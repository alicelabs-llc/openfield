#!/bin/bash
# Outreachy setup script - identifica communities Outreachy Dic 2026 y busca issues viables

set -u
DATE=$(date -u +%Y-%m-%dT%H:%M:%SZ)
LOG="/home/z/my-project/outreachy_setup_$(date +%Y%m%d_%H%M).log"

echo "=== Outreachy setup — $DATE ===" | tee "$LOG"
echo "" | tee -a "$LOG"

# 1. Fetch lista de communities participating
echo "=== Communities Outreachy Dic 2026 ===" | tee -a "$LOG"
sleep 2
curl -sS --max-time 15 "https://www.outreachy.org/communities/cfp/" 2>&1 | python3 -c "
import sys, re
html = sys.stdin.read()
html = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)
html = re.sub(r'<style.*?</style>', '', html, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', '\n', html)
text = re.sub(r'\n+', '\n', text)
# Buscar nombres de communities
lines = text.split('\n')
for i, line in enumerate(lines):
    line = line.strip()
    if line and len(line) > 3 and len(line) < 80 and not line.startswith(('Outreachy', 'Menu', 'Search', 'Skip', 'Applicant', 'Internship', 'Community', 'Volunteering', 'Mentor', 'Donor', 'Sponsor', 'About', 'Contact', 'Promote', 'Blog', 'FAQ')):
        if any(c.isalpha() for c in line) and not any(c in line for c in ['<', '>', '{', '}', '=']):
            print(f'  {line}')
" | head -40 | tee -a "$LOG"

echo "" | tee -a "$LOG"
echo "=== Repos GitHub con label 'outreachy' ===" | tee -a "$LOG"
sleep 3
curl -sS --max-time 10 "https://api.github.com/search/repositories?q=topic:outreachy+stars:>50&per_page=15&sort=stars&order=desc" 2>&1 | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    items = data.get('items', [])
    for r in items[:15]:
        print(f\"  {r['full_name']:50} stars={r['stargazers_count']:>5} lang={r.get('language','?')[:15]}\")
except: print('  rate limit hit')
" | tee -a "$LOG"

echo "" | tee -a "$LOG"
echo "=== Plan recomendado ===" | tee -a "$LOG"
cat <<'PLAN' | tee -a "$LOG"

1. NO aplicar a Outreachy Dic 2026 (deadline ya pasó 11 sept 2026)
2. SI prepararse para Mayo 2027:
   - Initial application abre feb 2027
   - Eligibility: ser 18+, full-time availability 13 semanas, underrepresented
3. Acción octubre-noviembre:
   - Elegir 1 community focus (sugerido: GNOME o Wikimedia)
   - Hacer 3-5 contribuciones durante Hacktoberfest
   - Conectar con mentors en Matrix/IRC
4. Acción diciembre:
   - 24 Pull Requests challenge (24pr.com) al mismo community
5. Acción enero-febrero 2027:
   - Apply a Outreachy Mayo 2027 cohorte

Ver OUTREACHY_PLAN.md para detalles completos.

PLAN
