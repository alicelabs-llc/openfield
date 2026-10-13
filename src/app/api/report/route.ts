import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const data = await request.json();

    // Generate a professional HTML report that can be converted to PDF
    const {
      query_id,
      query,
      entity_type,
      total_matches,
      results,
      timestamp,
    } = data;

    const date = new Date(timestamp).toLocaleString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      timeZone: "UTC",
    });

    const html = `
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>KYC Screening Report - ${query}</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Helvetica Neue', Arial, sans-serif; color: #1a202c; background: #fff; }
  .header { background: linear-gradient(135deg, #064e3b 0%, #047857 100%); color: white; padding: 40px 60px; }
  .header h1 { font-size: 28px; margin-bottom: 8px; }
  .header .subtitle { font-size: 14px; opacity: 0.9; }
  .header .logo { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }
  .header .logo-icon { width: 40px; height: 40px; background: white; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 24px; }
  .content { padding: 40px 60px; }
  .section { margin-bottom: 32px; }
  .section h2 { font-size: 18px; color: #064e3b; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; margin-bottom: 16px; }
  .info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  .info-item { background: #f7fafc; padding: 12px 16px; border-radius: 8px; }
  .info-label { font-size: 12px; color: #718096; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
  .info-value { font-size: 15px; font-weight: 600; color: #1a202c; }
  .result-banner { padding: 20px 24px; border-radius: 12px; margin-bottom: 24px; }
  .result-clear { background: #f0fdf4; border: 1px solid #86efac; }
  .result-flag { background: #fef2f2; border: 1px solid #fca5a5; }
  .result-banner h3 { font-size: 20px; margin-bottom: 4px; }
  .result-clear h3 { color: #166534; }
  .result-flag h3 { color: #991b1b; }
  .match-card { border: 1px solid #e2e8f0; border-left: 4px solid #ef4444; border-radius: 8px; padding: 16px 20px; margin-bottom: 16px; }
  .match-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
  .match-name { font-size: 16px; font-weight: 700; color: #1a202c; }
  .match-score { font-size: 14px; font-weight: 600; padding: 4px 12px; border-radius: 6px; }
  .score-high { background: #fef2f2; color: #991b1b; }
  .score-medium { background: #fffbeb; color: #92400e; }
  .match-details { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 13px; }
  .match-detail-label { color: #718096; }
  .match-detail-value { font-weight: 500; color: #1a202c; }
  .datasets { margin-top: 12px; display: flex; flex-wrap: wrap; gap: 4px; }
  .dataset-tag { background: #e2e8f0; color: #475569; padding: 2px 8px; border-radius: 4px; font-size: 11px; }
  .footer { border-top: 1px solid #e2e8f0; padding: 24px 60px; background: #f7fafc; }
  .footer p { font-size: 12px; color: #718096; margin-bottom: 4px; }
  .footer .disclaimer { font-size: 11px; color: #a0aec0; margin-top: 12px; line-height: 1.5; }
  .page-break { page-break-before: always; }
</style>
</head>
<body>
  <div class="header">
    <div class="logo">
      <div class="logo-icon">🛡️</div>
      <div>
        <h1>VerifyKYC</h1>
        <div class="subtitle">by AliceLabs LLC · Sanctions &amp; KYC Screening Report</div>
      </div>
    </div>
    <div style="font-size: 13px; opacity: 0.85;">
      Report ID: ${query_id}<br>
      Generated: ${date} UTC<br>
      Datasets checked: 490+ sources across 30+ jurisdictions
    </div>
  </div>

  <div class="content">
    <div class="section">
      <h2>Screening Details</h2>
      <div class="info-grid">
        <div class="info-item">
          <div class="info-label">Search Query</div>
          <div class="info-value">${escapeHtml(query)}</div>
        </div>
        <div class="info-item">
          <div class="info-label">Entity Type</div>
          <div class="info-value">${entity_type}</div>
        </div>
        <div class="info-item">
          <div class="info-label">Report Date</div>
          <div class="info-value">${date} UTC</div>
        </div>
        <div class="info-item">
          <div class="info-label">Report ID</div>
          <div class="info-value">${query_id}</div>
        </div>
      </div>
    </div>

    <div class="section">
      <h2>Screening Result</h2>
      ${total_matches > 0
        ? `<div class="result-banner result-flag">
            <h3>⚠️ ${total_matches} Match${total_matches > 1 ? "es" : ""} Found</h3>
            <p style="font-size: 14px; color: #991b1b;">Potential risk detected. Further due diligence is recommended.</p>
          </div>`
        : `<div class="result-banner result-clear">
            <h3>✅ No Matches Found</h3>
            <p style="font-size: 14px; color: #166534;">The screened entity does not appear in any of the 490+ sanctions, PEP, or watchlist datasets.</p>
          </div>`}
      ${results.map((match: any) => `
        <div class="match-card">
          <div class="match-header">
            <div class="match-name">${escapeHtml(match.caption)}</div>
            <div class="match-score ${match.score >= 0.9 ? "score-high" : "score-medium"}">
              ${(match.score * 100).toFixed(1)}% match
            </div>
          </div>
          <div class="match-details">
            <div>
              <span class="match-detail-label">Type:</span>
              <span class="match-detail-value">${match.schema}</span>
            </div>
            ${match.properties?.birthDate?.[0] ? `<div><span class="match-detail-label">Birth Date:</span> <span class="match-detail-value">${match.properties.birthDate[0]}</span></div>` : ""}
            ${match.properties?.nationality?.[0] ? `<div><span class="match-detail-label">Nationality:</span> <span class="match-detail-value">${match.properties.nationality[0]}</span></div>` : ""}
            ${match.properties?.country?.[0] ? `<div><span class="match-detail-label">Country:</span> <span class="match-detail-value">${match.properties.country[0]}</span></div>` : ""}
          </div>
          <div class="datasets">
            ${match.datasets.map((ds: string) => `<span class="dataset-tag">${ds}</span>`).join("")}
          </div>
        </div>
      `).join("")}
    </div>
  </div>

  <div class="footer">
    <p><strong>VerifyKYC</strong> by AliceLabs LLC</p>
    <p>Contact: eddyflores100@gmail.com · LLC registered in USA</p>
    <p>Data provided by OpenSanctions (opensanctions.org) · 490 datasets · 30+ jurisdictions</p>
    <div class="disclaimer">
      This report is generated automatically from publicly available sanctions, PEP, and watchlist data.
      It is provided for informational purposes only and does not constitute legal advice.
      AliceLabs LLC is not liable for decisions made based on this report.
      Matches should be reviewed by a qualified compliance professional before taking action.
    </div>
  </div>
</body>
</html>`;

    // Return as downloadable HTML (browser can print to PDF)
    return new NextResponse(html, {
      headers: {
        "Content-Type": "text/html",
        "Content-Disposition": `attachment; filename="KYC_Report_${query.replace(/\s+/g, "_")}.html"`,
      },
    });
  } catch (error) {
    console.error("Report generation error:", error);
    return NextResponse.json(
      { error: "Failed to generate report" },
      { status: 500 }
    );
  }
}

function escapeHtml(text: string): string {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
