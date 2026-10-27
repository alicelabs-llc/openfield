#!/usr/bin/env bash
# start-bridge.sh — One-click launcher for AliceLabs agent-bridge on Mac/Linux
# Run: chmod +x start-bridge.sh && ./start-bridge.sh

set -e
cd "$(dirname "$0")"

echo ""
echo "==============================================="
echo "  AliceLabs agent-bridge - starting..."
echo "==============================================="
echo ""

# Check Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ python3 is not installed or not in PATH."
    echo "   Install with: brew install python3  (Mac)"
    echo "   Or:            apt install python3  (Ubuntu/Debian)"
    exit 1
fi

# Check config.json exists
if [ ! -f "config.json" ]; then
    echo "❌ config.json not found in $(pwd)"
    exit 1
fi

echo "🚀 Starting agent-bridge on http://127.0.0.1:7421"
echo ""
echo "   Leave this terminal open. Open another to run cloudflared:"
echo "     cloudflared tunnel --url http://localhost:7421"
echo ""
echo "   Press Ctrl+C to stop."
echo ""

exec python3 agent-bridge.py
