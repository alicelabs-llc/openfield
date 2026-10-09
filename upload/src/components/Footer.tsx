import React from 'react';
import { Shield, Lock, FileText, Scale } from 'lucide-react';

interface FooterProps {
  onOpenLegal: () => void;
  onOpenBrandGuide: () => void;
  onScrollToSection: (sectionId: string) => void;
}

export const Footer: React.FC<FooterProps> = ({
  onOpenLegal,
  onOpenBrandGuide,
  onScrollToSection
}) => {
  return (
    <footer className="border-t border-slate-800 bg-slate-950 text-slate-400 py-12 lg:py-16">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-10">
          
          {/* Brand Col */}
          <div className="space-y-3 md:col-span-1">
            <div className="flex items-center gap-2 text-white font-bold text-base">
              <div className="flex h-7 w-7 items-center justify-center rounded bg-blue-700 text-white">
                <Shield className="h-4 w-4" />
              </div>
              <span>VeriSanctions</span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Global sanctions, PEP & adverse media screening platform operated by <strong>AliceLabs LLC</strong> (USA).
            </p>
            <div className="text-[11px] text-slate-500 font-mono">
              FinCEN BSA · OFAC 50% Rule · OpenSanctions Data
            </div>
          </div>

          {/* Navigation */}
          <div className="space-y-2 text-xs">
            <div className="font-bold text-white uppercase tracking-wider text-[11px] mb-3">
              Platform
            </div>
            <div>
              <button 
                onClick={() => onScrollToSection('screener')} 
                className="hover:text-white transition-colors cursor-pointer"
              >
                Live Sanctions Terminal
              </button>
            </div>
            <div>
              <button 
                onClick={() => onScrollToSection('competitors')} 
                className="hover:text-white transition-colors cursor-pointer"
              >
                vs Top 5 Competitors
              </button>
            </div>
            <div>
              <button 
                onClick={() => onScrollToSection('pricing')} 
                className="hover:text-white transition-colors cursor-pointer"
              >
                Pricing & Stripe Billing
              </button>
            </div>
            <div>
              <button 
                onClick={() => onScrollToSection('api-docs')} 
                className="hover:text-white transition-colors cursor-pointer"
              >
                Developer REST API
              </button>
            </div>
          </div>

          {/* Regulatory & Corporate */}
          <div className="space-y-2 text-xs">
            <div className="font-bold text-white uppercase tracking-wider text-[11px] mb-3">
              US LLC Governance
            </div>
            <div>
              <button 
                onClick={onOpenBrandGuide} 
                className="hover:text-white transition-colors cursor-pointer text-blue-400 font-semibold"
              >
                US Brand & Domain Blueprint
              </button>
            </div>
            <div>
              <button 
                onClick={onOpenLegal} 
                className="hover:text-white transition-colors cursor-pointer"
              >
                Terms of Service (Delaware LLC)
              </button>
            </div>
            <div>
              <button 
                onClick={onOpenLegal} 
                className="hover:text-white transition-colors cursor-pointer"
              >
                FCRA 15 U.S.C. § 1681 Safe Harbor
              </button>
            </div>
            <div>
              <button 
                onClick={onOpenLegal} 
                className="hover:text-white transition-colors cursor-pointer"
              >
                OFAC 50% Rule & AML Policy
              </button>
            </div>
          </div>

          {/* Compliance & Security */}
          <div className="space-y-3 text-xs">
            <div className="font-bold text-white uppercase tracking-wider text-[11px] mb-2">
              Verified Security
            </div>
            <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-3 text-[11px] text-slate-400 space-y-1.5">
              <div className="flex items-center gap-1.5 text-emerald-400 font-medium">
                <Lock className="h-3.5 w-3.5" />
                <span>Stripe 256-bit Encrypted</span>
              </div>
              <p>
                Invoicing and payments processed securely via Stripe. Domestic US EIN tax receipts.
              </p>
            </div>
          </div>

        </div>

        {/* Regulatory disclaimer */}
        <div className="border-t border-slate-800 pt-6 text-[11px] text-slate-500 leading-relaxed">
          <p>
            DISCLAIMER: VeriSanctions is a business-to-business regulatory intelligence platform provided by AliceLabs LLC. It is not a consumer reporting agency as defined under the Fair Credit Reporting Act (FCRA, 15 U.S.C. § 1681 et seq.). Information obtained through VeriSanctions may not be used to establish an individual's eligibility for consumer credit, tenant leasing, employment, or personal insurance. All data is synchronized from authoritative global public and governmental sanction releases, including OpenSanctions, US Treasury OFAC, the European External Action Service, and the UN Security Council.
          </p>
          <div className="mt-4 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-slate-600">
            <span>© {new Date().getFullYear()} AliceLabs LLC. All rights reserved. Registered in the United States.</span>
            <span>VeriSanctions™ is a trademark of AliceLabs LLC.</span>
          </div>
        </div>

      </div>
    </footer>
  );
};
