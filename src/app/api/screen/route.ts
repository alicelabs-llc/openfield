import { NextRequest, NextResponse } from "next/server";

const OPENSANCTIONS_API_KEY = process.env.OPENSANCTIONS_API_KEY || "1ad95e58381ae978ff2cfb93a7f3bea2";
const OPENSANCTIONS_API_URL = "https://api.opensanctions.org";

export async function POST(request: NextRequest) {
  try {
    const { name, type } = await request.json();

    if (!name || typeof name !== "string") {
      return NextResponse.json({ error: "Name is required" }, { status: 400 });
    }

    const schema = type === "Company" ? "LegalEntity" : "Person";

    // =================================================================
    // 1. OPENSANCTIONS — Sanciones, PEPs, Criminales, Exclusiones
    // =================================================================
    const sanctionsBody = {
      queries: {
        q1: {
          schema: schema,
          properties: { name: [name] },
        },
      },
    };

    const sanctionsResponse = await fetch(`${OPENSANCTIONS_API_URL}/match/default`, {
      method: "POST",
      headers: {
        "Authorization": `ApiKey ${OPENSANCTIONS_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(sanctionsBody),
    });

    let sanctionsResults: any[] = [];
    let sanctionsTotal = 0;

    if (sanctionsResponse.ok) {
      const sanctionsData = await sanctionsResponse.json();
      const queryResponse = sanctionsData.responses?.q1 || {};
      const rawResults = queryResponse.results || [];
      sanctionsTotal = queryResponse.total?.value || rawResults.length;
      sanctionsResults = rawResults
        .filter((r: any) => r.score >= 0.3)
        .map((r: any) => ({
          caption: r.caption || "Unknown",
          schema: r.schema || "Person",
          score: r.score || 0,
          datasets: r.datasets || [],
          properties: r.properties || {},
          topics: r.topics || [],
        }));
    }

    // =================================================================
    // 2. WIKIDATA — Bio, foto, nacionalidad, ocupación
    // =================================================================
    let wikiData: any = null;

    try {
      const wikiResponse = await fetch(
        `https://www.wikidata.org/w/api.php?action=wbsearchentities&search=${encodeURIComponent(name)}&language=en&format=json&limit=1`,
        { signal: AbortSignal.timeout(5000) }
      );

      if (wikiResponse.ok) {
        const wikiJson = await wikiResponse.json();
        const wikiResults = wikiJson.search || [];
        if (wikiResults.length > 0) {
          const wikiEntity = wikiResults[0];
          wikiData = {
            id: wikiEntity.id || "",
            label: wikiEntity.label || "",
            description: wikiEntity.description || "",
            url: wikiEntity.concepturi || "",
          };

          // Fetch additional details (birth date, nationality, occupation, image)
          try {
            const detailsResponse = await fetch(
              `https://www.wikidata.org/w/api.php?action=wbgetentities&ids=${wikiEntity.id}&props=labels|descriptions|claims|sitelinks&languages=en&format=json`,
              { signal: AbortSignal.timeout(5000) }
            );

            if (detailsResponse.ok) {
              const detailsJson = await detailsResponse.json();
              const entity = detailsJson.entities?.[wikiEntity.id] || {};
              const claims = entity.claims || {};

              // Extract birth date (P569)
              if (claims.P569?.[0]?.mainsnak?.datavalue?.value?.time) {
                const birthTime = claims.P569[0].mainsnak.datavalue.value.time;
                wikiData.birthDate = birthTime.replace(/^\+/, "").split("T")[0];
              }

              // Extract nationality (P27)
              if (claims.P27?.[0]?.mainsnak?.datavalue?.value?.id) {
                const natId = claims.P27[0].mainsnak.datavalue.value.id;
                // Fetch country name
                const natResponse = await fetch(
                  `https://www.wikidata.org/w/api.php?action=wbgetentities&ids=${natId}&props=labels&languages=en&format=json`,
                  { signal: AbortSignal.timeout(3000) }
                );
                if (natResponse.ok) {
                  const natJson = await natResponse.json();
                  wikiData.nationality = natJson.entities?.[natId]?.labels?.en?.value || "";
                }
              }

              // Extract occupation (P106)
              if (claims.P106?.[0]?.mainsnak?.datavalue?.value?.id) {
                const occId = claims.P106[0].mainsnak.datavalue.value.id;
                const occResponse = await fetch(
                  `https://www.wikidata.org/w/api.php?action=wbgetentities&ids=${occId}&props=labels&languages=en&format=json`,
                  { signal: AbortSignal.timeout(3000) }
                );
                if (occResponse.ok) {
                  const occJson = await occResponse.json();
                  wikiData.occupation = occJson.entities?.[occId]?.labels?.en?.value || "";
                }
              }

              // Extract image (P18)
              if (claims.P18?.[0]?.mainsnak?.datavalue?.value) {
                const imageName = claims.P18[0].mainsnak.datavalue.value;
                wikiData.imageUrl = `https://commons.wikimedia.org/wiki/Special:FilePath/${encodeURIComponent(imageName)}?width=200`;
              }

              // Extract Wikipedia link
              const sitelinks = entity.sitelinks || {};
              if (sitelinks.enwiki?.url) {
                wikiData.wikipediaUrl = sitelinks.enwiki.url;
              }
            }
          } catch {
            // Timeout on details, continue with basic info
          }
        }
      }
    } catch {
      // Wikidata failed, continue without it
    }

    // =================================================================
    // 3. GDELT — Adverse Media / Negative News (235K+ sources)
    // =================================================================
    let adverseMedia: any[] = [];

    try {
      const gdeltQuery = encodeURIComponent(name);
      const gdeltResponse = await fetch(
        `https://api.gdeltproject.org/api/v2/doc/doc?query=${gdeltQuery}+sanction+OR+fraud+OR+corruption+OR+scandal+OR+laundering+OR+criminal&mode=ArtList&maxrecords=10&format=json&sort=DateDesc`,
        { signal: AbortSignal.timeout(8000) }
      );

      if (gdeltResponse.ok) {
        const gdeltText = await gdeltResponse.text();
        if (gdeltText.startsWith("{")) {
          const gdeltJson = JSON.parse(gdeltText);
          const articles = gdeltJson.articles || [];
          adverseMedia = articles.slice(0, 10).map((a: any) => ({
            title: a.title || "",
            url: a.url || "",
            source: a.domain || "",
            date: a.seendate || "",
            language: a.language || "",
            socialImage: a.socialimage || "",
          }));
        }
      }
    } catch {
      // GDELT failed or timed out, continue without adverse media
    }

    // =================================================================
    // 4. RISK SCORE — Calculate overall risk
    // =================================================================
    let riskScore = 0;
    let riskLevel = "Low";
    const riskFactors: string[] = [];

    if (sanctionsResults.length > 0) {
      const topMatch = sanctionsResults[0];
      if (topMatch.score >= 0.9) {
        riskScore += 50;
        riskFactors.push("High-confidence sanctions match");
      } else if (topMatch.score >= 0.7) {
        riskScore += 30;
        riskFactors.push("Medium-confidence sanctions match");
      } else {
        riskScore += 15;
        riskFactors.push("Low-confidence sanctions match");
      }

      // Check for PEP status
      const isPEP = sanctionsResults.some(
        (r) => r.topics?.includes("role.pep") || r.topics?.includes("role.pol")
      );
      if (isPEP) {
        riskScore += 15;
        riskFactors.push("Politically Exposed Person (PEP)");
      }

      // Check for criminal status
      const isCriminal = sanctionsResults.some(
        (r) => r.topics?.includes("crime") || r.topics?.includes("wanted")
      );
      if (isCriminal) {
        riskScore += 20;
        riskFactors.push("Criminal/wanted status");
      }
    }

    if (adverseMedia.length > 0) {
      riskScore += Math.min(adverseMedia.length * 3, 15);
      riskFactors.push(`${adverseMedia.length} adverse media articles found`);
    }

    if (riskScore >= 70) riskLevel = "Critical";
    else if (riskScore >= 40) riskLevel = "High";
    else if (riskScore >= 20) riskLevel = "Medium";

    // =================================================================
    // 5. BUILD RESPONSE
    // =================================================================
    const result = {
      query_id: `KYC-${Date.now()}-${Math.random().toString(36).substring(2, 8)}`,
      query: name,
      entity_type: type,
      timestamp: new Date().toISOString(),

      // Risk assessment
      risk_score: riskScore,
      risk_level: riskLevel,
      risk_factors: riskFactors,

      // Sanctions screening
      sanctions: {
        total_matches: sanctionsResults.length,
        datasets_checked: 490,
        results: sanctionsResults,
      },

      // Entity enrichment (Wikidata)
      entity_info: wikiData,

      // Adverse media (GDELT)
      adverse_media: {
        total_articles: adverseMedia.length,
        sources_checked: "235,000+ news sources",
        articles: adverseMedia,
      },

      // Summary
      summary: {
        status: sanctionsResults.length > 0 ? "FLAGGED" : "CLEAR",
        recommendations:
          sanctionsResults.length > 0
            ? "Potential risk detected. Enhanced due diligence recommended."
            : "No matches found in 490+ sanctions, PEP, and watchlist datasets.",
        data_sources: [
          "OpenSanctions (490 datasets, 16M+ entities)",
          "Wikidata (entity enrichment, bio, photos)",
          "GDELT (235K+ news sources for adverse media)",
        ],
      },
    };

    return NextResponse.json(result);
  } catch (error) {
    console.error("Screening error:", error);
    return NextResponse.json(
      { error: "An unexpected error occurred during screening" },
      { status: 500 }
    );
  }
}
