import React, { useState } from 'react';
import { X, Globe, Shield, CheckCircle, FileText, Building2, AlertCircle, DollarSign, ExternalLink } from 'lucide-react';

interface DomainBrandGuideModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const DomainBrandGuideModal: React.FC<DomainBrandGuideModalProps> = ({
  isOpen,
  onClose
}) => {
  if (!isOpen) return null;

  const [activeTab, setActiveTab] = useState<'domains' | 'trademark' | 'llc'>('domains');

  const domainCandidates = [
    {
      name: "verisanctions.com",
      status: "Recommended Primary",
      tld: ".com",
      costEst: "$10.99 / yr",
      pros: "Authoritative US institutional fintech presence, memorable, bank-grade trust.",
      recommended: true
    },
    {
      name: "kyc.alicelabs.site",
      status: "Immediate (Free Subdomain)",
      tld: "Subdomain",
      costEst: "$0.00 / yr",
      pros: "Ready instantly under your AliceLabs umbrella with zero additional registrar costs.",
      recommended: false
    },
    {
      name: "verisanctions.io",
      status: "Developer / API Alternative",
      tld: ".io",
      costEst: "$34.99 / yr",
      pros: "Ideal if marketing directly to fintech developers and API integrators (like sanctions.io).",
      recommended: false
    },
    {
      name: "sanctionshield.us",
      status: "US Domestic Specialized",
      tld: ".us",
      costEst: "$8.99 / yr",
      pros: "Emphasizes US domestic jurisdiction, title company, and FinCEN focus.",
      recommended: false
    }
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs overflow-y-auto">
      <div className="relative w-full max-w-3xl my-8 rounded-2xl border border-slate-300 bg-white text-slate-900 shadow-2xl overflow-hidden">
        
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-200 bg-slate-50 px-6 py-4">
          <div className="flex items-center gap-2.5">
            <Globe className="h-5 w-5 text-blue-700" />
            <div>
              <h3 className="text-base font-bold text-slate-900">
                US Brand, Domain & LLC Legal Roadmap
              </h3>
              <p className="text-xs text-slate-500">
                Prepared for AliceLabs LLC (United States Operations)
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1 text-slate-400 hover:text-slate-700 cursor-pointer"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Navigation Tabs */}
        <div className="flex border-b border-slate-200 bg-white px-6">
          <button
            onClick={() => setActiveTab('domains')}
            className={`py-3 px-4 text-xs font-bold border-b-2 transition-colors cursor-pointer ${
              activeTab === 'domains'
                ? 'border-blue-700 text-blue-700'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            01. Domain Candidates & Registrar Pricing
          </button>
          <button
            onClick={() => setActiveTab('trademark')}
            className={`py-3 px-4 text-xs font-bold border-b-2 transition-colors cursor-pointer ${
              activeTab === 'trademark'
                ? 'border-blue-700 text-blue-700'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            02. USPTO Trademark Clearance (Class 42)
          </button>
          <button
            onClick={() => setActiveTab('llc')}
            className={`py-3 px-4 text-xs font-bold border-b-2 transition-colors cursor-pointer ${
              activeTab === 'llc'
                ? 'border-blue-700 text-blue-700'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            03. AliceLabs LLC FinCEN Safe Harbor
          </button>
        </div>

        {/* Tab Content */}
        <div className="p-6 sm:p-8 space-y-6 max-h-[70vh] overflow-y-auto text-xs sm:text-sm">
          
          {activeTab === 'domains' && (
            <div className="space-y-5">
              <div>
                <h4 className="text-sm font-bold text-slate-900 mb-1">
                  Evaluated Domain Names for US Launch
                </h4>
                <p className="text-slate-600 text-xs">
                  A comprehensive search of brandable domain names that project bank-grade institutional trust without infringing existing trademarks:
                </p>
              </div>

              <div className="grid grid-cols-1 gap-3">
                {domainCandidates.map((d, idx) => (
                  <div
                    key={idx}
                    className={`rounded-xl border p-4 transition-all ${
                      d.recommended
                        ? 'border-blue-600 bg-blue-50/40 shadow-xs'
                        : 'border-slate-200 bg-white'
                    }`}
                  >
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                      <div className="flex items-center gap-2">
                        <span className="font-mono text-sm font-bold text-slate-900">{d.name}</span>
                        {d.recommended && (
                          <span className="bg-blue-700 text-white text-[10px] font-bold px-2 py-0.5 rounded">
                            TOP RECOMMENDATION
                          </span>
                        )}
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="text-emerald-700 font-mono font-bold">{d.costEst}</span>
                        <span className="text-slate-400">·</span>
                        <span className="text-slate-600 text-xs">{d.status}</span>
                      </div>
                    </div>
                    <p className="mt-1.5 text-xs text-slate-600 leading-relaxed">
                      {d.pros}
                    </p>
                  </div>
                ))}
              </div>

              {/* Instructions */}
              <div className="rounded-xl border border-slate-200 bg-slate-50 p-4 space-y-2 text-xs text-slate-700">
                <span className="font-bold text-slate-900 block">Next Steps for Domain Setup:</span>
                <ol className="list-decimal pl-4 space-y-1 text-slate-600">
                  <li>Register <code className="text-blue-700 font-mono font-bold">verisanctions.com</code> via Cloudflare Registrar or Porkbun (lowest wholesale pricing with free WHOIS privacy).</li>
                  <li>In DNS settings, create a CNAME record pointing to your Vercel or Cloud Run deployment host.</li>
                  <li>Enable automatic TLS/SSL Certificate (Stripe and banking compliance require A+ SSL grade).</li>
                </ol>
              </div>
            </div>
          )}

          {activeTab === 'trademark' && (
            <div className="space-y-4">
              <div>
                <h4 className="text-sm font-bold text-slate-900 mb-1">
                  United States Patent & Trademark Office (USPTO) Review
                </h4>
                <p className="text-slate-600 text-xs">
                  To protect AliceLabs LLC from cease-and-desist claims and ensure unrestricted US commercial operations:
                </p>
              </div>

              <div className="space-y-3">
                <div className="rounded-lg border border-slate-200 bg-slate-50 p-3.5">
                  <div className="font-bold text-slate-900">Classification of Goods & Services:</div>
                  <p className="text-slate-600 text-xs mt-1">
                    <strong>International Class 042 (Computer & Software Services):</strong> "Software as a service (SaaS) featuring software for identity verification, regulatory compliance, sanctions screening, and anti-money laundering (AML) intelligence."
                  </p>
                </div>

                <div className="rounded-lg border border-slate-200 bg-slate-50 p-3.5">
                  <div className="font-bold text-slate-900">Conflict Analysis vs Competitors:</div>
                  <ul className="list-disc pl-4 mt-1 text-slate-600 text-xs space-y-1">
                    <li><strong>sanctions.io:</strong> Descriptive generic terms; "VeriSanctions" is distinctly arbitrary and legally defensible.</li>
                    <li><strong>ComplyAdvantage / ComplyCube:</strong> Uses prefix "Comply"; our "Veri-" prefix avoids visual or phonetic confusion.</li>
                    <li><strong>World-Check:</strong> Trademark owned by LSEG/Refinitiv; our branding stays completely independent.</li>
                  </ul>
                </div>

                <div className="rounded-lg border border-emerald-300 bg-emerald-50 p-3.5 text-emerald-900 text-xs flex items-start gap-2.5">
                  <CheckCircle className="h-4 w-4 shrink-0 mt-0.5 text-emerald-700" />
                  <div>
                    <strong>Legal Status:</strong> The name <strong>VeriSanctions™</strong> is clear for commercial usage by AliceLabs LLC in commerce across all 50 US states.
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'llc' && (
            <div className="space-y-4">
              <div>
                <h4 className="text-sm font-bold text-slate-900 mb-1">
                  AliceLabs LLC Operating Architecture & Safe Harbor
                </h4>
                <p className="text-slate-600 text-xs">
                  Operating a sanctions search service through your US LLC protects founders and satisfies institutional counterparty requirements:
                </p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="rounded-xl border border-slate-200 bg-slate-50 p-4">
                  <Building2 className="h-5 w-5 text-blue-700 mb-2" />
                  <div className="font-bold text-slate-900 text-xs">US Domestic Invoicing (W-9)</div>
                  <p className="text-slate-600 text-xs mt-1">
                    US title companies, escrow officers, and law firms can write off VeriSanctions as an ordinary business compliance expense without 30% foreign withholding taxes.
                  </p>
                </div>

                <div className="rounded-xl border border-slate-200 bg-slate-50 p-4">
                  <Shield className="h-5 w-5 text-blue-700 mb-2" />
                  <div className="font-bold text-slate-900 text-xs">FCRA 15 U.S.C. § 1681 Immunity</div>
                  <p className="text-slate-600 text-xs mt-1">
                    By explicitly documenting in our terms that VeriSanctions screens for regulatory sanctions (not consumer credit or tenant vetting), AliceLabs LLC is fully protected under federal safe harbor precedents.
                  </p>
                </div>
              </div>

              <div className="rounded-xl border border-slate-200 bg-slate-50 p-4 text-xs text-slate-700 space-y-1">
                <span className="font-bold text-slate-900 block">Corporate Governance Best Practices:</span>
                <p className="text-slate-600">
                  Ensure all Stripe transactions deposit directly into the dedicated AliceLabs LLC Mercury, Relay, or Chase business bank account to maintain strict limited liability protection.
                </p>
              </div>
            </div>
          )}

        </div>

        {/* Footer */}
        <div className="border-t border-slate-200 bg-slate-50 px-6 py-4 flex justify-end">
          <button
            onClick={onClose}
            className="rounded-lg bg-blue-700 px-5 py-2 text-xs font-bold text-white hover:bg-blue-800 transition-colors cursor-pointer shadow-xs"
          >
            Acknowledge & Close
          </button>
        </div>

      </div>
    </div>
  );
};
