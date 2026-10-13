import { NextRequest, NextResponse } from "next/server";

// MCP Server Manifest — descubre el servicio para agentes AI
export async function GET(request: NextRequest) {
  const baseUrl = request.nextUrl.origin;

  const manifest = {
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": "VRFKYC",
    "description": "Global AML, sanctions, PEP and adverse media screening API. Screen any person or company against 490+ datasets in seconds. Risk scoring, PDF reports, entity enrichment.",
    "url": baseUrl,
    "applicationCategory": "BusinessApplication",
    "operatingSystem": "Web",
    "offers": {
      "@type": "Offer",
      "price": "0",
      "priceCurrency": "USD",
      "description": "Free tier: 5 screenings/month. Pro: $99/mo. Business: $299/mo."
    },
    "provider": {
      "@type": "Organization",
      "name": "AliceLabs LLC",
      "url": "https://github.com/eddyflores100-lang",
      "email": "eddyflores100@gmail.com",
      "address": {
        "@type": "PostalAddress",
        "addressCountry": "US"
      }
    },
    "apiEndpoint": `${baseUrl}/api/screen`,
    "capabilities": [
      "sanctions-screening",
      "pep-check",
      "adverse-media-screening",
      "risk-scoring",
      "entity-enrichment",
      "pdf-report-generation",
      "batch-screening"
    ],
    "dataSources": [
      "OpenSanctions (490 datasets, 16M+ entities)",
      "Wikidata (entity enrichment, bio, photos)",
      "GDELT (235K+ news sources for adverse media)"
    ],
    "mcp": {
      "version": "1.0",
      "transport": "http",
      "endpoint": `${baseUrl}/api/mcp`,
      "tools": [
        {
          "name": "screen_person",
          "description": "Screen a person against 490+ global sanctions, PEP, and criminal lists",
          "inputSchema": {
            "type": "object",
            "properties": {
              "name": { "type": "string", "description": "Full name of the person to screen" },
              "country": { "type": "string", "description": "ISO country code (optional)" },
              "threshold": { "type": "number", "description": "Match threshold 0-1 (default: 0.3)" }
            },
            "required": ["name"]
          }
        },
        {
          "name": "screen_company",
          "description": "Screen a company against global sanctions and watchlists",
          "inputSchema": {
            "type": "object",
            "properties": {
              "name": { "type": "string", "description": "Company name to screen" },
              "country": { "type": "string", "description": "ISO country code (optional)" }
            },
            "required": ["name"]
          }
        },
        {
          "name": "get_risk_score",
          "description": "Get a 0-100 risk score for a person or company",
          "inputSchema": {
            "type": "object",
            "properties": {
              "name": { "type": "string" },
              "type": { "type": "string", "enum": ["Person", "Company"] }
            },
            "required": ["name"]
          }
        },
        {
          "name": "generate_report",
          "description": "Generate a PDF screening report for compliance purposes",
          "inputSchema": {
            "type": "object",
            "properties": {
              "name": { "type": "string" },
              "type": { "type": "string", "enum": ["Person", "Company"] },
              "format": { "type": "string", "enum": ["pdf", "html", "json"], "default": "pdf" }
            },
            "required": ["name"]
          }
        }
      ]
    },
    "openapi": {
      "openapi": "3.0.0",
      "info": {
        "title": "VRFKYC API",
        "version": "1.0.0",
        "description": "Global AML, sanctions, PEP and adverse media screening API"
      },
      "servers": [{ "url": baseUrl }],
      "paths": {
        "/api/screen": {
          "post": {
            "summary": "Screen a person or company",
            "requestBody": {
              "content": {
                "application/json": {
                  "schema": {
                    "type": "object",
                    "properties": {
                      "name": { "type": "string" },
                      "type": { "type": "string", "enum": ["Person", "Company"] }
                    }
                  }
                }
              }
            }
          }
        },
        "/api/report": {
          "post": {
            "summary": "Generate PDF report",
            "requestBody": {
              "content": {
                "application/json": {
                  "schema": { "type": "object" }
                }
              }
            }
          }
        }
      }
    }
  };

  return NextResponse.json(manifest, {
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type, Authorization",
    }
  });
}
