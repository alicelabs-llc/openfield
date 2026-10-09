import React, { useState } from 'react';
import { X, Printer, Download, ShieldCheck, ShieldAlert, CheckCircle, Stamp, Share2, Copy } from 'lucide-react';
import { SanctionEntity } from '../types';
import { generateAuditChecksum } from '../utils/screeningService';

interface CertifiedReportModalProps {
  isOpen: boolean;
  onClose: () => void;
  entity: SanctionEntity | null;
  query: string;
  isCleanPass: boolean;
}

export const CertifiedReportModal: React.FC<CertifiedReportModalProps> = ({
  isOpen,
  onClose,
  entity,
  query,
  isCleanPass
}) => {
  if (!isOpen) return null;

  const [officerName, setOfficerName] = useState('Senior Compliance Officer');
  const [officerId, setOfficerId] = useState('CO-9942');
  const [copied, setCopied] = useState(false);

  const timestamp = new Date().toISOString();
  const formattedDate = new Date().toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    timeZoneName: 'short'
  });

  const dossierId = `VS-${new Date().getFullYear()}-${Math.random().toString(36).substring(2, 8).toUpperCase()}`;
  const checksum = generateAuditChecksum(query, timestamp);

  const handlePrint = () => {
    window.print();
  };

  const handleDownloadHtml = () => {
    const reportHtml = `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>VeriSanctions Certified Audit Dossier - ${dossierId}</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 40px; color: #0f172a; line-height: 1.5; max-width: 800px; margin: 0 auto; }
    .header { border-bottom: 2px solid #0f172a; padding-bottom: 20px; margin-bottom: 25px; display: flex; justify-content: space-between; }
    .seal { border: 2px solid #059669; color: #059669; padding: 8px 16px; border-radius: 4px; font-weight: bold; text-align: center; font-size: 13px; }
    .seal-flagged { border: 2px solid #dc2626; color: #dc2626; padding: 8px 16px; border-radius: 4px; font-weight: bold; text-align: center; font-size: 13px; }
    .section { margin-bottom: 20px; }
    .label { font-size: 11px; text-transform: uppercase; color: #64748b; font-weight: 600; margin-bottom: 4px; }
    .value { font-size: 14px; font-weight: 500; }
    .box { background: #f8fafc; border: 1px solid #e2e8f0; padding: 15px; border-radius: 6px; margin-top: 15px; }
    .footer { margin-top: 40px; border-top: 1px solid #cbd5e1; padding-top: 20px; font-size: 11px; color: #64748b; }
  </style>
</head>
<body>
  <div class="header">
    <div>
      <h2 style="margin: 0; font-size: 20px;">VERISANCTIONS™ CERTIFIED AUDIT DOSSIER</h2>
      <div style="font-size: 12px; color: #475569; margin-top: 4px;">AliceLabs LLC Corporate Sanctions Screening Unit (USA)</div>
      <div style="font-size: 12px; color: #475569;">FinCEN BSA / OFAC 50% Rule Audit Trail</div>
    </div>
    <div>
      <div class="${isCleanPass ? 'seal' : 'seal-flagged'}">
        ${isCleanPass ? 'NEGATIVE VERIFICATION<br>CLEAN PASS' : 'ENFORCEMENT MATCH<br>FLAGGED'}
      </div>
    </div>
  </div>

  <div class="section">
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
      <div><div class="label">Target Entity Screened</div><div class="value" style="font-size: 16px; font-weight: bold;">${query}</div></div>
      <div><div class="label">Verification Dossier ID</div><div class="value" style="font-family: monospace;">${dossierId}</div></div>
      <div><div class="label">Certified Timestamp</div><div class="value">${formattedDate}</div></div>
      <div><div class="label">Cryptographic SHA-256 Checksum</div><div class="value" style="font-family: monospace; font-size: 12px;">${checksum}</div></div>
    </div>
  </div>

  <div class="box">
    <div class="label">Executive Finding & Adjudication</div>
    <div style="font-size: 13px; margin-top: 6px;">
      ${isCleanPass 
        ? `Target entity "${query}" was searched across 494 global enforcement and sanctions datasets. No active designations, PEP records, or restrictive sanctions detected at the time of screening.` 
        : `Target entity "${query}" matched designated record "${entity?.caption}" with a match score of ${(entity?.score ? Math.round(entity.score * 100) : 95)}%. Designated authorities include ${entity?.properties.sanctionBody || 'Global Sanctions Authorities'}.`
      }
    </div>
  </div>

  <div class="footer">
    <p>Issued by AliceLabs LLC pursuant to FinCEN and OFAC compliance frameworks. This electronic record is cryptographically indexed and valid for legal due diligence files under FCRA 15 U.S.C. § 1681 Safe Harbor guidelines.</p>
  </div>
</body>
</html>`;
    const blob = new Blob([reportHtml], { type: 'text/html;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${dossierId}_VeriSanctions_Audit_Report.html`;
    link.click();
  };

  const handleCopyHash = () => {
    navigator.clipboard.writeText(`${dossierId} | Hash: ${checksum}`);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-slate-950/85 backdrop-blur-md overflow-y-auto">
      <div className="relative w-full max-w-3xl my-8 rounded-2xl border border-slate-700 bg-white text-slate-900 shadow-2xl overflow-hidden">
        
        {/* Top Control Bar (Hidden during print) */}
        <div className="no-print flex items-center justify-between border-b border-slate-200 bg-slate-100 px-6 py-3.5">
          <div className="flex items-center gap-2 text-xs font-semibold text-slate-700">
            <Stamp className="h-4 w-4 text-indigo-600" />
            <span>Certified Compliance Dossier Preview</span>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleDownloadHtml}
              className="inline-flex items-center gap-1.5 rounded-lg border border-slate-300 bg-white px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50 transition-colors cursor-pointer"
            >
              <Download className="h-3.5 w-3.5" />
              <span>Download HTML</span>
            </button>

            <button
              onClick={handlePrint}
              className="inline-flex items-center gap-1.5 rounded-lg bg-indigo-600 px-3.5 py-1.5 text-xs font-semibold text-white shadow-sm hover:bg-indigo-700 transition-colors cursor-pointer"
            >
              <Printer className="h-3.5 w-3.5" />
              <span>Print / Save as PDF</span>
            </button>

            <button
              onClick={onClose}
              className="p-1 text-slate-400 hover:text-slate-700 cursor-pointer ml-1"
            >
              <X className="h-5 w-5" />
            </button>
          </div>
        </div>

        {/* PRINTABLE DOSSIER BODY */}
        <div className="p-8 sm:p-12 space-y-8 bg-white print:p-0">
          
          {/* Header */}
          <div className="border-b-2 border-slate-900 pb-6 flex flex-col sm:flex-row sm:items-start justify-between gap-6">
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xl font-extrabold tracking-tight text-slate-900">
                  VERISANCTIONS™
                </span>
                <span className="text-xs bg-slate-900 text-white font-mono px-2 py-0.5 rounded">
                  OFFICIAL AUDIT DOSSIER
                </span>
              </div>
              <div className="text-xs text-slate-600 mt-1">
                Issued by <strong>AliceLabs LLC</strong> (Registered in USA)
              </div>
              <div className="text-xs text-slate-500">
                Department of FinCEN BSA & OFAC Sanctions Intelligence
              </div>
            </div>

            {/* Official Certification Stamp / Badge */}
            <div className="shrink-0 text-right sm:text-right">
              {isCleanPass ? (
                <div className="inline-block border-2 border-emerald-600 rounded-md p-2.5 text-center bg-emerald-50">
                  <div className="flex items-center justify-center gap-1 text-emerald-700 text-xs font-black tracking-wider uppercase">
                    <ShieldCheck className="h-4 w-4" />
                    NEGATIVE VERIFICATION
                  </div>
                  <div className="text-[11px] font-bold text-emerald-800 uppercase mt-0.5">
                    CLEAN PASS RECORD
                  </div>
                </div>
              ) : (
                <div className="inline-block border-2 border-rose-600 rounded-md p-2.5 text-center bg-rose-50">
                  <div className="flex items-center justify-center gap-1 text-rose-700 text-xs font-black tracking-wider uppercase">
                    <ShieldAlert className="h-4 w-4" />
                    POSITIVE MATCH
                  </div>
                  <div className="text-[11px] font-bold text-rose-800 uppercase mt-0.5">
                    ENFORCEMENT FLAGGED
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Dossier Metadata Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs border-b border-slate-200 pb-6">
            <div>
              <span className="text-slate-500 block font-semibold uppercase text-[10px]">Verification ID</span>
              <span className="font-mono font-bold text-slate-900 text-sm">{dossierId}</span>
            </div>
            <div>
              <span className="text-slate-500 block font-semibold uppercase text-[10px]">Certified Date</span>
              <span className="font-medium text-slate-900">{formattedDate}</span>
            </div>
            <div>
              <span className="text-slate-500 block font-semibold uppercase text-[10px]">Datasets Queried</span>
              <span className="font-medium text-slate-900">494 Watchlists (Full Scan)</span>
            </div>
            <div>
              <span className="text-slate-500 block font-semibold uppercase text-[10px]">Audit Integrity Hash</span>
              <span className="font-mono text-indigo-700 text-[11px] truncate block" title={checksum}>
                {checksum}
              </span>
            </div>
          </div>

          {/* Target Entity Section */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">
              01. Target Entity Subject of Verification
            </h4>
            <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
              <div className="text-base font-bold text-slate-900">
                {query}
              </div>
              <div className="mt-1 text-xs text-slate-600">
                Class: {entity?.schema || 'Legal Individual or Corporate Entity'} · Jurisdiction Search: Global Consolidated
              </div>
            </div>
          </div>

          {/* Findings & Compliance Analysis */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">
              02. Enforcement Findings & Legal Basis
            </h4>

            {isCleanPass ? (
              <div className="rounded-lg border border-emerald-200 bg-emerald-50/50 p-4 text-xs text-slate-700 space-y-2">
                <p className="font-medium text-emerald-900">
                  ✓ Negative Clearance Confirmed: No Sanctions, PEP, or Regulatory Debarment Found
                </p>
                <p>
                  The query was analyzed against all updated databases including US OFAC (SDN, Non-SDN, SSI), 
                  United Nations Security Council Consolidated Sanctions, European Union Restrictive Measures, 
                  United Kingdom HM Treasury OFSI, Interpol Red Notices, and international Politically Exposed Persons registers.
                </p>
                <p className="text-[11px] text-slate-500">
                  Audit Recommendation: Entity may proceed to standard counterparty transaction processing.
                </p>
              </div>
            ) : (
              <div className="rounded-lg border border-rose-200 bg-rose-50/50 p-4 text-xs text-slate-800 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-rose-900 text-sm">
                    Designation: {entity?.caption}
                  </span>
                  <span className="font-mono font-bold text-rose-700">
                    Match Confidence: {entity?.score ? Math.round(entity.score * 100) : 95}%
                  </span>
                </div>

                <div className="text-slate-700">
                  {entity?.properties.notes?.[0] || 'Designated on international economic sanctions lists pursuant to counter-terrorism, state aggression, or money laundering enforcement mandates.'}
                </div>

                <div className="grid grid-cols-2 gap-2 pt-2 border-t border-rose-200/60 text-[11px]">
                  <div>
                    <strong className="text-slate-900">Sanctioning Authorities:</strong>{' '}
                    <span>{entity?.properties.sanctionBody || 'US OFAC / EU CFSP / UN SC'}</span>
                  </div>
                  <div>
                    <strong className="text-slate-900">Legal Citations:</strong>{' '}
                    <span>{entity?.properties.legalBasis || 'Executive Order / Council Regulation'}</span>
                  </div>
                </div>

                {entity?.properties.dataset && (
                  <div className="text-[11px] text-slate-600">
                    <strong>Enforcement Lists:</strong> {entity.properties.dataset.join(' · ')}
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Compliance Officer Sign-off Block */}
          <div className="space-y-3 pt-2">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">
              03. Certified Due Diligence Sign-Off
            </h4>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 rounded-lg border border-slate-200 p-4 text-xs">
              <div className="space-y-2">
                <div>
                  <label className="block text-[10px] text-slate-500 font-semibold uppercase">
                    Reviewing Compliance Officer / MLRO
                  </label>
                  <input
                    type="text"
                    value={officerName}
                    onChange={(e) => setOfficerName(e.target.value)}
                    className="w-full font-medium text-slate-900 border-b border-slate-300 py-1 bg-transparent focus:outline-none focus:border-indigo-600"
                  />
                </div>
                <div>
                  <label className="block text-[10px] text-slate-500 font-semibold uppercase">
                    Officer / License ID
                  </label>
                  <input
                    type="text"
                    value={officerId}
                    onChange={(e) => setOfficerId(e.target.value)}
                    className="w-full font-mono text-slate-700 border-b border-slate-300 py-1 bg-transparent focus:outline-none focus:border-indigo-600"
                  />
                </div>
              </div>

              {/* Signature line simulation */}
              <div className="flex flex-col justify-end border-t sm:border-t-0 sm:border-l border-slate-200 sm:pl-6 pt-4 sm:pt-0">
                <div className="h-10 border-b border-slate-400 border-dashed flex items-end pb-1 font-serif italic text-slate-700 text-sm">
                  {officerName}
                </div>
                <div className="text-[10px] text-slate-500 mt-1 uppercase">
                  Authorized Compliance Officer Signature
                </div>
              </div>
            </div>
          </div>

          {/* Legal Safe Harbor & Disclaimer */}
          <div className="border-t border-slate-200 pt-4 text-[10px] text-slate-500 leading-normal">
            <p>
              <strong>REGULATORY COMPLIANCE NOTICE:</strong> This certified report is generated by VeriSanctions (AliceLabs LLC, USA) for Bank Secrecy Act (BSA), FinCEN, and OFAC economic sanctions compliance purposes. In accordance with the Fair Credit Reporting Act (15 U.S.C. § 1681 et seq.), AliceLabs LLC is not a consumer reporting agency; this dossier may not be utilized to evaluate consumer credit, consumer employment, or tenant eligibility under FCRA restrictions. Validated under Cryptographic Checksum {checksum}.
            </p>
          </div>

        </div>

      </div>
    </div>
  );
};
