#!/bin/bash
set -e

# Extract token from git config without printing it
TOKEN=$(python3 -c "
import re
with open('/home/z/my-project/hacktoberfest-candidates/vajra/.git/config') as f:
    content = f.read()
m = re.search(r'https://[^:]+:([^@]+)@github\.com', content)
print(m.group(1) if m else '')
")

if [ -z "$TOKEN" ]; then
    echo "ERROR: Could not extract token"
    exit 1
fi

# Verify token works (don't print it)
AUTH_OK=$(curl -sS --max-time 15 -H "Authorization: token $TOKEN" -H "User-Agent: Mozilla/5.0" \
  "https://api.github.com/user" 2>&1 | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(d.get('login','') if 'login' in d else 'ERR:'+str(d)[:200])
")
echo "Auth as: $AUTH_OK"

if [ "$AUTH_OK" = "ERR:"* ] || [ -z "$AUTH_OK" ]; then
    echo "Token invalid"
    exit 1
fi
