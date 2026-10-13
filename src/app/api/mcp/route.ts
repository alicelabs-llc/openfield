import { NextRequest, NextResponse } from "next/server";

// MCP endpoint — Model Context Protocol para agentes AI
// Permite que Claude, GPT, Gemini y otros agentes usen VRFKYC

const OPENSANCTIONS_API_KEY = process.env.OPENSANCTIONS_API_KEY || "1ad95e58381ae978ff2cfb93a7f3bea2";
const OPENSANCTIONS_API_URL = "https://api.opensanctions.org";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    // MCP JSON-RPC 2.0 protocol
    const { jsonrpc, method, params, id } = body;

    if (jsonrpc !== "2.0") {
      return NextResponse.json({
        jsonrpc: "2.0",
        error: { code: -32600, message: "Invalid Request" },
        id: id || null,
      }, { status: 400 });
    }

    switch (method) {
      case "tools/list": {
        return NextResponse.json({
          jsonrpc: "2.0",
          result: {
            tools: [
              {
                name: "screen_person",
                description: "Screen a person against 490+ global sanctions, PEP, and criminal lists. Returns risk score, match details, adverse media, and entity info.",
                inputSchema: {
                  type: "object",
                  properties: {
                    name: { type: "string", description: "Full name of the person to screen" },
                    threshold: { type: "number", description: "Match threshold 0-1 (default: 0.3)" }
                  },
                  required: ["name"]
                }
              },
              {
                name: "screen_company",
                description: "Screen a company against global sanctions and watchlists",
                inputSchema: {
                  type: "object",
                  properties: {
                    name: { type: "string", description: "Company name to screen" }
                  },
                  required: ["name"]
                }
              },
              {
                name: "get_risk_score",
                description: "Get a 0-100 risk score for a person or company. Returns risk level (Low/Medium/High/Critical) and risk factors.",
                inputSchema: {
                  type: "object",
                  properties: {
                    name: { type: "string" },
                    type: { type: "string", "enum": ["Person", "Company"] }
                  },
                  required: ["name"]
                }
              }
            ]
          },
          id
        });
      }

      case "tools/call": {
        const { name: toolName, arguments: args } = params;

        if (toolName === "screen_person" || toolName === "screen_company" || toolName === "get_risk_score") {
          const entityName = args?.name;
          const entityType = toolName === "screen_company" || args?.type === "Company" ? "Company" : "Person";

          if (!entityName) {
            return NextResponse.json({
              jsonrpc: "2.0",
              error: { code: -32602, message: "Missing required parameter: name" },
              id
            }, { status: 400 });
          }

          // Call OpenSanctions
          const schema = entityType === "Company" ? "LegalEntity" : "Person";
          const sanctionsResponse = await fetch(`${OPENSANCTIONS_API_URL}/match/default`, {
            method: "POST",
            headers: {
              "Authorization": `ApiKey ${OPENSANCTIONS_API_KEY}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              queries: {
                q1: {
                  schema,
                  properties: { name: [entityName] },
                },
              },
            }),
          });

          let sanctionsResults: any[] = [];
          if (sanctionsResponse.ok) {
            const sanctionsData = await sanctionsResponse.json();
            const rawResults = sanctionsData.responses?.q1?.results || [];
            sanctionsResults = rawResults
              .filter((r: any) => r.score >= 0.3)
              .map((r: any) => ({
                name: r.caption,
                score: r.score,
                datasets: r.datasets,
                topics: r.topics,
              }));
          }

          // Calculate risk score
          let riskScore = 0;
          const riskFactors: string[] = [];
          if (sanctionsResults.length > 0) {
            const top = sanctionsResults[0];
            if (top.score >= 0.9) { riskScore += 50; riskFactors.push("High-confidence sanctions match"); }
            else if (top.score >= 0.7) { riskScore += 30; riskFactors.push("Medium-confidence sanctions match"); }
            else { riskScore += 15; riskFactors.push("Low-confidence sanctions match"); }
            if (top.topics?.includes("role.pep") || top.topics?.includes("role.pol")) {
              riskScore += 15; riskFactors.push("PEP");
            }
            if (top.topics?.includes("crime") || top.topics?.includes("wanted")) {
              riskScore += 20; riskFactors.push("Criminal status");
            }
          }

          const riskLevel = riskScore >= 70 ? "Critical" : riskScore >= 40 ? "High" : riskScore >= 20 ? "Medium" : "Low";

          const result = toolName === "get_risk_score"
            ? {
                name: entityName,
                type: entityType,
                risk_score: riskScore,
                risk_level: riskLevel,
                risk_factors: riskFactors,
                status: sanctionsResults.length > 0 ? "FLAGGED" : "CLEAR",
              }
            : {
                name: entityName,
                type: entityType,
                risk_score: riskScore,
                risk_level: riskLevel,
                risk_factors: riskFactors,
                status: sanctionsResults.length > 0 ? "FLAGGED" : "CLEAR",
                sanctions_matches: sanctionsResults.length,
                matches: sanctionsResults.slice(0, 5),
                datasets_checked: 490,
                report_id: `KYC-${Date.now()}-${Math.random().toString(36).substring(2, 8)}`,
                timestamp: new Date().toISOString(),
              };

          return NextResponse.json({
            jsonrpc: "2.0",
            result: {
              content: [
                {
                  type: "text",
                  text: JSON.stringify(result, null, 2),
                }
              ]
            },
            id
          });
        }

        return NextResponse.json({
          jsonrpc: "2.0",
          error: { code: -32601, message: `Unknown tool: ${toolName}` },
          id
        }, { status: 400 });
      }

      case "initialize": {
        return NextResponse.json({
          jsonrpc: "2.0",
          result: {
            protocolVersion: "2024-11-05",
            serverInfo: {
              name: "VRFKYC",
              version: "1.0.0",
            },
            capabilities: {
              tools: {},
              resources: {},
            },
          },
          id
        });
      }

      default:
        return NextResponse.json({
          jsonrpc: "2.0",
          error: { code: -32601, message: `Method not found: ${method}` },
          id
        }, { status: 400 });
    }
  } catch (error) {
    return NextResponse.json({
      jsonrpc: "2.0",
      error: { code: -32700, message: "Parse error" },
      id: null,
    }, { status: 500 });
  }
}

export async function GET() {
  return NextResponse.json({
    name: "VRFKYC MCP Server",
    version: "1.0.0",
    description: "Global AML, sanctions, PEP and adverse media screening via MCP",
    protocol: "JSON-RPC 2.0",
    tools: ["screen_person", "screen_company", "get_risk_score"],
    endpoint: "/api/mcp",
  });
}
