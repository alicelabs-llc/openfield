#!/bin/bash
# Submit multiple agents to mcpservers.org via Agent Bridge

# Define agents with their details
declare -A AGENTS=(
  ["recall-mcp"]="Long-term memory for AI agents|Memory|https://github.com/eddyflores100-lang/recall-mcp|io.github.eddyflores100-lang/recall-mcp"
  ["context-pruner-mcp"]="Save 50-80% on token costs by intercepting tool outputs before they reach the LLM|Development|https://github.com/eddyflores100-lang/context-pruner-mcp|io.github.eddyflores100-lang/context-pruner-mcp"
  ["mcp-suite"]="229 modern MCP servers for AI agents (1035 tools, 30 categories)|Development|https://github.com/eddyflores100-lang/mcp-suite|io.github.eddyflores100-lang/mcp-suite"
  ["mermail-escrow-agent"]="Peer-to-peer deal escrow coordinated entirely over a Mermail email thread|Finance|https://github.com/eddyflores100-lang/mermail-escrow-agent|io.github.eddyflores100-lang/mermail-escrow-agent"
  ["mcp-vault-server"]="High-security MCP server for secret management on Google Cloud (NIST/OWASP standards)|Cloud Service|https://github.com/alicelabs-llc/mcp-vault-server|io.github.alicelabs-llc/mcp-vault-server"
  ["universal-trust-adapter"]="Translate between ALL trust credential formats used by AI agents via canonical Universal Trust Schema|Communication|https://github.com/alicelabs-llc/universal-trust-adapter|io.github.alicelabs-llc/universal-trust-adapter"
  ["marketnow-agent"]="Universal agent plugin (Claude Code, Cursor, Gemini, Grok, Qwen, Codex) for MarketNow trust layer|Security|https://github.com/alicelabs-llc/marketnow-agent|io.github.alicelabs-llc/marketnow-agent"
)

for agent_name in "${!AGENTS[@]}"; do
  IFS='|' read -r description category url registry <<< "${AGENTS[$agent_name]}"
  echo "Submitting $agent_name to mcpservers.org..."
  echo "  name: $agent_name"
  echo "  description: ${description:0:60}..."
  echo "  category: $category"
  echo "  url: $url"
  echo "  registry: $registry"
  echo
  
  # Navigate to submit page (only once, then fill+submit+repeat)
  python3 /home/z/my-project/scripts/agent_bridge_cli.py open "https://mcpservers.org/submit" 2>&1 | tail -1
  sleep 3
  
  # Fill the form
  python3 /home/z/my-project/scripts/agent_bridge_cli.py fill "#server-name" "$agent_name" 2>&1 | tail -1
  python3 /home/z/my-project/scripts/agent_bridge_cli.py fill "#server-description" "$description" 2>&1 | tail -1
  python3 /home/z/my-project/scripts/agent_bridge_cli.py fill "#server-url" "$url" 2>&1 | tail -1
  python3 /home/z/my-project/scripts/agent_bridge_cli.py fill "#registry-name" "$registry" 2>&1 | tail -1
  python3 /home/z/my-project/scripts/agent_bridge_cli.py fill "#contact-email" "eddyflores100@gmail.com" 2>&1 | tail -1
  
  # Set category via direct selector (less brittle than option:contains)
  # Find the option value by category name
  CATEGORY_VALUE=$(echo "$category" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
  python3 /home/z/my-project/scripts/agent_bridge_cli.py click "select#server-category" 2>&1 | tail -1
  python3 /home/z/my-project/scripts/agent_bridge_cli.py click "option[value='$category']" 2>&1 | tail -1
  
  # Click submit button
  python3 /home/z/my-project/scripts/agent_bridge_cli.py click "button[type=submit]" 2>&1 | tail -1
  sleep 3
  
  # Verify success
  python3 /home/z/my-project/scripts/agent_bridge_cli.py gettext "h1" 2>&1 | tail -1
  echo "Done with $agent_name"
  echo "----"
done
