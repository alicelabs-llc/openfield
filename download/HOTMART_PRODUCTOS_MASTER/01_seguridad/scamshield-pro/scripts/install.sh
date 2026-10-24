#!/usr/bin/env bash
# ScamShield Pro — Quick installer for Linux/macOS
set -e

echo "🛡️  ScamShield Pro — Installer"
echo "==============================="

# 1. Check Python
if ! command -v python3 &>/dev/null; then
  echo "✗ Python 3.10+ required. Install with: apt install python3 python3-venv"
  exit 1
fi
PY_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "✓ Python $PY_VER found"

# 2. Virtualenv
if [ ! -d ".venv" ]; then
  echo "→ Creating virtualenv .venv ..."
  python3 -m venv .venv
fi
source .venv/bin/activate

# 3. Install deps
echo "→ Installing dependencies ..."
pip install --upgrade pip wheel
pip install -r requirements.txt
pip install -e .

# 4. Env file
if [ ! -f ".env" ]; then
  echo "→ Creating .env from template ..."
  cp .env.example .env
  # Generate random API key
  NEW_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
  sed -i.bak "s/changeme-please-replace-this/$NEW_KEY/g" .env
  rm -f .env.bak
  echo "✓ Generated API key: $NEW_KEY"
  echo "  (saved in .env — keep this private)"
fi

echo ""
echo "==============================="
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "  1. Start the API server:    scamshield serve"
echo "  2. Open dashboard:          http://localhost:8000/dashboard"
echo "  3. Scan from CLI:            scamshield scan https://example.com"
echo "  4. Read the docs:            cat README.md"
echo ""
echo "Need help? eddyflores100@gmail.com"
