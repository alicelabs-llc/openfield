import React from 'react';
import { ArrowDown, CheckCircle2, FileCheck2, Database, ShieldCheck, Building2, Search, ArrowRight } from 'lucide-react';

interface HeroProps {
  onStartSearch: () => void;
  onExplorePricing: () => void;
}

export const Hero: React.FC<HeroProps> = ({ onStartSearch, onExplorePricing }) => {
  return (
    <section className="relative border-b border-slate-200 bg-white pt-12 pb-16 lg:pt-16 lg:pb-20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        
        {/* Top Header Badge */}
        <div className="flex flex-col items-center text-center max-w-4xl mx-auto">
          <div className="inline-flex items-center gap-2 rounded-full border border-blue-200 bg-blue-50/80 px-3.5 py-1 text-xs font-semibold text-blue-800 mb-6">
            <Building2 className="h-3.5 w-3.5 text-blue-700" />
            <span>AliceLabs LLC Institutional Suite</span>
            <span aria-hidden="true">·</span>
            <span>FinCEN & OFAC Safe Harbor Compliant</span>
          </div>

          {/* Main Headline */}
          <h1 className="text-3xl font-extrabold tracking-tight text-slate-900 sm:text-5xl lg:text-6xl text-balance leading-tight">
            Automated Sanctions, PEP & Adverse Media Screening
          </h1>

          {/* Subtitle */}
          <p className="mt-5 text-base sm:text-lg leading-relaxed text-slate-600 max-w-3xl">
            Screen individuals and corporate entities against <strong>494 official global enforcement lists</strong> in real time. 
            Built on OpenSanctions data with sub-350ms response latency, cryptographic PDF audit dossiers, 
            and official US LLC invoicing for title companies, law firms, and fintechs.
          </p>

          {/* Call to Actions */}
          <div className="mt-8 flex flex-wrap items-center justify-center gap-4">
            <button
              onClick={onStartSearch}
              className="inline-flex items-center justify-center rounded-lg bg-blue-700 px-6 py-3.5 text-sm font-semibold text-white shadow-xs transition-colors hover:bg-blue-800 focus-visible:outline-2 focus-visible:outline-blue-600 cursor-pointer"
            >
              <Search className="mr-2 h-4 w-4" />
              <span>Launch Live Screener Below</span>
            </button>

            <button
              onClick={onExplorePricing}
              className="inline-flex items-center justify-center rounded-lg border border-slate-300 bg-white px-6 py-3.5 text-sm font-semibold text-slate-700 transition-colors hover:bg-slate-50 hover:text-slate-900 shadow-xs cursor-pointer"
            >
              <span>Compare Plans & Pricing</span>
              <ArrowRight className="ml-2 h-4 w-4 text-slate-400" />
            </button>
          </div>

          {/* Key Trust Checkmarks */}
          <div className="mt-8 flex flex-wrap items-center justify-center gap-x-8 gap-y-3 text-xs sm:text-sm font-medium text-slate-600">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-emerald-600 shrink-0" />
              <span>US OFAC (SDN & Non-SDN)</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-emerald-600 shrink-0" />
              <span>EU, UN & UK Sanctions</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-emerald-600 shrink-0" />
              <span>Certified Court-Ready PDF Dossiers</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-emerald-600 shrink-0" />
              <span>70% Lower Cost than Legacy Vendors</span>
            </div>
          </div>
        </div>

        {/* 4-Stat High-Trust Institutional Strip */}
        <div className="mt-14 grid grid-cols-2 gap-4 rounded-xl border border-slate-200 bg-slate-50 p-6 sm:grid-cols-4 sm:gap-6">
          <div className="border-r border-slate-200 pr-4">
            <div className="flex items-center gap-2 text-slate-500 text-xs font-semibold">
              <Database className="h-4 w-4 text-blue-700" />
              <span>Watchlist Sources</span>
            </div>
            <div className="mt-1.5 text-2xl sm:text-3xl font-extrabold text-slate-900 font-mono tabular-nums">494+</div>
            <div className="mt-0.5 text-xs text-slate-500">Updated every 6 hours</div>
          </div>

          <div className="border-r border-slate-200 pr-4">
            <div className="flex items-center gap-2 text-slate-500 text-xs font-semibold">
              <ShieldCheck className="h-4 w-4 text-emerald-600" />
              <span>API Latency</span>
            </div>
            <div className="mt-1.5 text-2xl sm:text-3xl font-extrabold text-emerald-600 font-mono tabular-nums">&lt; 350ms</div>
            <div className="mt-0.5 text-xs text-slate-500">Live edge query time</div>
          </div>

          <div className="border-r border-slate-200 pr-4">
            <div className="flex items-center gap-2 text-slate-500 text-xs font-semibold">
              <FileCheck2 className="h-4 w-4 text-blue-700" />
              <span>Audit Dossiers</span>
            </div>
            <div className="mt-1.5 text-2xl sm:text-3xl font-extrabold text-slate-900 font-mono tabular-nums">100%</div>
            <div className="mt-0.5 text-xs text-slate-500">SHA-256 sealed PDF & HTML</div>
          </div>

          <div>
            <div className="flex items-center gap-2 text-slate-500 text-xs font-semibold">
              <Building2 className="h-4 w-4 text-blue-700" />
              <span>LLC Invoicing</span>
            </div>
            <div className="mt-1.5 text-2xl sm:text-3xl font-extrabold text-slate-900 font-mono">USA</div>
            <div className="mt-0.5 text-xs text-slate-500">AliceLabs LLC W-9 deductibility</div>
          </div>
        </div>

      </div>
    </section>
  );
};
