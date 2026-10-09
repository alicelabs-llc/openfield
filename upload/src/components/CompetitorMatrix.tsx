import React from 'react';
import { Check, X, Shield, Award, Sparkles, ExternalLink, ArrowRight } from 'lucide-react';

export const CompetitorMatrix: React.FC = () => {
  const competitors = [
    {
      name: "VeriSanctions (AliceLabs)",
      isUs: true,
      price: "$0 free / $99/mo Pro",
      datasets: "494+ Lists (OFAC, EU, UN, UK)",
      pdfReports: "Court-Ready Cryptographic PDF & HTML",
      batchScreening: "Included (CSV / Bulk)",
      usLlcInvoicing: "Delaware US LLC (W-9 Deductible)",
      apiResponseTime: "< 350ms",
      badge: "OUR SERVICE"
    },
    {
      name: "sanctions.io",
      isUs: false,
      price: "$19 - $99/mo",
      datasets: "~200 Sanctions lists",
      pdfReports: "No official audit PDF",
      batchScreening: "Higher tier only ($299+)",
      usLlcInvoicing: "EU Entity (No domestic US LLC)",
      apiResponseTime: "~350ms",
      badge: "Competitor"
    },
    {
      name: "Dilisense",
      isUs: false,
      price: "100 free, then usage-based",
      datasets: "Aggregated web lists",
      pdfReports: "No certified PDF stamps",
      batchScreening: "Pay-per-row credit model",
      usLlcInvoicing: "Foreign entity",
      apiResponseTime: "~150ms",
      badge: "Competitor"
    },
    {
      name: "ComplyAdvantage",
      isUs: false,
      price: "$99.99/mo starter (up to $500+)",
      datasets: "~500 lists + proprietary",
      pdfReports: "Requires enterprise add-on",
      batchScreening: "Enterprise contract",
      usLlcInvoicing: "Enterprise only",
      apiResponseTime: "~1 sec",
      badge: "Competitor"
    },
    {
      name: "ComplyCube",
      isUs: false,
      price: "$99/mo + usage fees",
      datasets: "Global Watchlists",
      pdfReports: "Standard portal reports",
      batchScreening: "Additional API fee",
      usLlcInvoicing: "UK / Global entity",
      apiResponseTime: "~1.2 sec",
      badge: "Competitor"
    },
    {
      name: "LSEG World-Check One",
      isUs: false,
      price: "$500 - $2,000/mo (Annual Lock)",
      datasets: "Proprietary database",
      pdfReports: "Full dossier",
      batchScreening: "Complex legacy integration",
      usLlcInvoicing: "Enterprise sales cycle",
      apiResponseTime: "Legacy batch / slow",
      badge: "Legacy Terminal"
    }
  ];

  return (
    <section id="competitors" className="py-16 border-b border-slate-200 bg-slate-50">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        
        {/* Header */}
        <div className="max-w-3xl mb-8">
          <div className="text-xs font-bold uppercase tracking-wider text-blue-700 mb-1">
            Competitive Benchmark
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            How VeriSanctions Outperforms the Top 5 Screening Providers
          </h2>
          <p className="mt-2 text-sm text-slate-600">
            We analyzed the top screening tools in the market. VeriSanctions provides identical comprehensive data coverage at 70% lower cost, backed by certified PDF dossiers and domestic US LLC invoicing.
          </p>
        </div>

        {/* Feature comparison table */}
        <div className="overflow-hidden rounded-xl border border-slate-300 bg-white shadow-xs">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs sm:text-sm">
              <thead className="border-b border-slate-200 bg-slate-100/80 text-slate-700 font-bold">
                <tr>
                  <th className="py-3.5 px-4 sm:px-6">Provider</th>
                  <th className="py-3.5 px-4">Starting Price</th>
                  <th className="py-3.5 px-4">Datasets</th>
                  <th className="py-3.5 px-4">Certified PDF Reports</th>
                  <th className="py-3.5 px-4">Batch CSV</th>
                  <th className="py-3.5 px-4">US LLC Invoicing</th>
                  <th className="py-3.5 px-4">Speed</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200">
                {competitors.map((item, idx) => (
                  <tr 
                    key={idx}
                    className={item.isUs ? "bg-blue-50/60 font-medium" : "hover:bg-slate-50 text-slate-700"}
                  >
                    <td className="py-3.5 px-4 sm:px-6">
                      <div className="flex items-center gap-2">
                        {item.isUs && <Shield className="h-4 w-4 text-blue-700 shrink-0" />}
                        <span className={item.isUs ? "font-bold text-slate-900" : "text-slate-800"}>
                          {item.name}
                        </span>
                      </div>
                      {item.isUs && (
                        <span className="text-[11px] text-blue-700 font-semibold block mt-0.5">
                          AliceLabs LLC Platform Guarantee
                        </span>
                      )}
                    </td>

                    <td className="py-3.5 px-4 font-mono font-bold">
                      <span className={item.isUs ? "text-emerald-700" : "text-slate-700"}>
                        {item.price}
                      </span>
                    </td>

                    <td className="py-3.5 px-4 text-slate-700">
                      {item.datasets}
                    </td>

                    <td className="py-3.5 px-4">
                      {item.isUs ? (
                        <span className="inline-flex items-center gap-1.5 text-emerald-700 font-bold">
                          <Check className="h-4 w-4" />
                          <span>Included (SHA-256)</span>
                        </span>
                      ) : (
                        <span className="text-slate-500">{item.pdfReports}</span>
                      )}
                    </td>

                    <td className="py-3.5 px-4">
                      {item.isUs ? (
                        <span className="inline-flex items-center gap-1.5 text-emerald-700 font-bold">
                          <Check className="h-4 w-4" />
                          <span>Web Table & CSV</span>
                        </span>
                      ) : (
                        <span className="text-slate-500">{item.batchScreening}</span>
                      )}
                    </td>

                    <td className="py-3.5 px-4">
                      {item.isUs ? (
                        <span className="inline-flex items-center gap-1.5 text-emerald-700 font-bold">
                          <Check className="h-4 w-4" />
                          <span>W-9 & Domestic EIN</span>
                        </span>
                      ) : (
                        <span className="text-slate-500">{item.usLlcInvoicing}</span>
                      )}
                    </td>

                    <td className="py-3.5 px-4 font-mono text-slate-700 font-semibold">
                      {item.apiResponseTime}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* 3 Core Value Pillars */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-5">
          <div className="rounded-xl border border-slate-300 bg-white p-5 shadow-xs">
            <div className="text-xs font-bold text-blue-700 mb-1">ADVANTAGE 01</div>
            <h4 className="text-base font-bold text-slate-900 mb-1.5">Court & Audit-Ready PDF Dossiers</h4>
            <p className="text-xs text-slate-600 leading-relaxed">
              Neither sanctions.io nor Dilisense provides formal audit PDF certificates. VeriSanctions generates legally formatted dossiers with SHA-256 cryptographic hashes and compliance officer sign-off lines in one click.
            </p>
          </div>

          <div className="rounded-xl border border-slate-300 bg-white p-5 shadow-xs">
            <div className="text-xs font-bold text-blue-700 mb-1">ADVANTAGE 02</div>
            <h4 className="text-base font-bold text-slate-900 mb-1.5">70% Lower Cost than Legacy Vendors</h4>
            <p className="text-xs text-slate-600 leading-relaxed">
              ComplyAdvantage and LexisNexis require $500–$2,000/month annual vendor commitments. Our plans start at $0 free, with unlimited manual screening for just $99/month on Stripe.
            </p>
          </div>

          <div className="rounded-xl border border-slate-300 bg-white p-5 shadow-xs">
            <div className="text-xs font-bold text-blue-700 mb-1">ADVANTAGE 03</div>
            <h4 className="text-base font-bold text-slate-900 mb-1.5">US LLC Domestic Compliance</h4>
            <p className="text-xs text-slate-600 leading-relaxed">
              US title companies, escrow officers, and law firms require an official W-9 and domestic corporate invoicing. AliceLabs LLC provides direct US domestic compliance receipts without international tax friction.
            </p>
          </div>
        </div>

      </div>
    </section>
  );
};
