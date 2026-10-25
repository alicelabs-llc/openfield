#!/usr/bin/env bash
# ScamShield Pro — Quick dev launcher
set -e
cd "$(dirname "$0")/.."

if [ ! -d ".venv" ]; then
  bash scripts/install.sh
fi
source .venv/bin/activate

case "${1:-serve}" in
  serve)
    exec scamshield serve --host 0.0.0.0 --port "${2:-8000}" --reload
    ;;
  scan)
    exec scamshield scan "${2:-https://example.com}"
    ;;
  docker)
    docker build -t scamshield-pro .
    docker run -p 8000:8000 --env-file .env scamshield-pro
    ;;
  test)
    pytest -v
    ;;
  *)
    echo "Usage: $0 {serve|scan URL|docker|test}"
    exit 1
    ;;
esac
