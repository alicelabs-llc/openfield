import React, { useState } from 'react';
import { X, Scale, ShieldCheck, FileText, Lock, AlertTriangle } from 'lucide-react';

interface LegalPoliciesModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const LegalPoliciesModal: React.FC<LegalPoliciesModalProps> = ({
  isOpen,
  onClose
}) => {
  if (!isOpen) return null;

  const [activeTab, setActiveTab] = useState<'terms' | 'fcra' | 'privacy' | 'aml'>('terms');

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs overflow-y-auto">
      <div className="relative w-full max-w-3xl my-8 rounded-2xl border border-slate-300 bg-white text-slate-900 shadow-2xl overflow-hidden">
        
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-200 bg-slate-50 px-6 py-4">
          <div className="flex items-center gap-2.5">
            <Scale className="h-5 w-5 text-blue-700" />
            <div>
              <h3 className="text-base font-bold text-slate-900">
                AliceLabs LLC Legal & Regulatory Framework
              </h3>
              <p className="text-xs text-slate-500">
                Governing Law: State of Delaware / United States
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

        {/* Tab Headers */}
        <div className="flex border-b border-slate-200 bg-white px-6 overflow-x-auto">
          <button
            onClick={() => setActiveTab('terms')}
            className={`py-3 px-3 text-xs font-bold border-b-2 whitespace-nowrap transition-colors cursor-pointer ${
              activeTab === 'terms'
                ? 'border-blue-700 text-blue-700'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            Terms of Service
          </button>
          <button
            onClick={() => setActiveTab('fcra')}
            className={`py-3 px-3 text-xs font-bold border-b-2 whitespace-nowrap transition-colors cursor-pointer ${
              activeTab === 'fcra'
                ? 'border-rose-600 text-rose-700'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            FCRA § 1681 Safe Harbor
          </button>
          <button
            onClick={() => setActiveTab('privacy')}
            className={`py-3 px-3 text-xs font-bold border-b-2 whitespace-nowrap transition-colors cursor-pointer ${
              activeTab === 'privacy'
                ? 'border-blue-700 text-blue-700'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            Privacy Policy (GDPR/CCPA)
          </button>
          <button
            onClick={() => setActiveTab('aml')}
            className={`py-3 px-3 text-xs font-bold border-b-2 whitespace-nowrap transition-colors cursor-pointer ${
              activeTab === 'aml'
                ? 'border-blue-700 text-blue-700'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            OFAC & AML Compliance
          </button>
        </div>

        {/* Content body */}
        <div className="p-6 sm:p-8 space-y-4 max-h-[70vh] overflow-y-auto text-xs sm:text-sm text-slate-700 leading-relaxed">
          
          {activeTab === 'terms' && (
            <div className="space-y-4">
              <h4 className="text-base font-bold text-slate-900">AliceLabs LLC — Terms of Service</h4>
              <p className="text-xs text-slate-500">Last Revised: October 2026</p>
              
              <div className="space-y-3">
                <p>
                  <strong>1. Acceptance of Terms:</strong> By accessing VeriSanctions ("Service"), operated by AliceLabs LLC ("Company", "we", "us"), you agree to be bound by these Terms of Service. If you are entering into this agreement on behalf of a financial institution, law firm, or corporate entity, you represent that you possess lawful authority to bind such entity.
                </p>
                <p>
                  <strong>2. Nature of Data & Intelligence:</strong> VeriSanctions compiles and aggregates public and official governmental sanctions lists, including datasets from the US Office of Foreign Assets Control (OFAC), European Union, United Nations Security Council, UK HM Treasury, and OpenSanctions foundation. Company does not author government designations and acts strictly as a technology aggregator and processor.
                </p>
                <p>
                  <strong>3. Permitted Business Use:</strong> The Service is designed exclusively for commercial counterparty vetting, Know Your Customer (KYC), Anti-Money Laundering (AML), and transaction sanction screening. Any unlawful or defamatory use is strictly prohibited.
                </p>
                <p>
                  <strong>4. Limitation of Liability:</strong> Under no circumstances shall AliceLabs LLC, its directors, or affiliates be liable for indirect, punitive, or consequential damages resulting from algorithmic false-positives or screening adjudications.
                </p>
              </div>
            </div>
          )}

          {activeTab === 'fcra' && (
            <div className="space-y-4">
              <div className="flex items-center gap-2 text-rose-700">
                <AlertTriangle className="h-5 w-5 shrink-0" />
                <h4 className="text-base font-bold text-slate-900">Mandatory FCRA Notice (15 U.S.C. § 1681)</h4>
              </div>

              <div className="rounded-xl border border-rose-300 bg-rose-50 p-4 text-xs text-rose-900 space-y-2">
                <p className="font-bold">IMPORTANT REGULATORY NOTICE FOR ALL US USERS:</p>
                <p>
                  VeriSanctions is NOT a "Consumer Reporting Agency" (CRA) under the federal Fair Credit Reporting Act (15 U.S.C. § 1681 et seq.). The reports, matches, and dossiers issued by this platform do not constitute "Consumer Reports."
                </p>
              </div>

              <div className="space-y-3 text-xs text-slate-700">
                <p>
                  <strong>Prohibited Uses:</strong> You expressly certify that you will NOT use any VeriSanctions report, score, or data in whole or in part to determine an individual's eligibility for:
                </p>
                <ul className="list-disc pl-5 space-y-1 text-slate-700">
                  <li>Personal credit, loans, or consumer financing</li>
                  <li>Employment, hiring, promotion, or reassignment decisions</li>
                  <li>Residential tenant leasing or housing eligibility</li>
                  <li>Personal insurance underwriting</li>
                </ul>
                <p>
                  <strong>Authorized Uses:</strong> You may utilize VeriSanctions strictly to verify counterparties, vendors, and transactions for compliance with Bank Secrecy Act (BSA), FinCEN, OFAC economic sanctions, and international anti-terrorism financing laws.
                </p>
              </div>
            </div>
          )}

          {activeTab === 'privacy' && (
            <div className="space-y-4">
              <h4 className="text-base font-bold text-slate-900">Privacy Policy & Data Security</h4>
              <p className="text-xs text-slate-500">GDPR, CCPA & CPRA Compliant Standard</p>

              <div className="space-y-3">
                <p>
                  <strong>1. Search Zero-Logging Option:</strong> For sensitive financial and legal screening queries, AliceLabs LLC provides immediate non-persistent session processing. We do not sell or monetize search queries.
                </p>
                <p>
                  <strong>2. Encryption Standards:</strong> All data in transit is protected via TLS 1.3 encryption with AES-256 bit cipher suites. Audit hash generation utilizes irreversible SHA-256 integrity algorithms.
                </p>
                <p>
                  <strong>3. Payment Information:</strong> Payment processing is handled exclusively by Stripe, Inc. AliceLabs LLC never stores raw payment card numbers or CVVs on its servers.
                </p>
              </div>
            </div>
          )}

          {activeTab === 'aml' && (
            <div className="space-y-4">
              <h4 className="text-base font-bold text-slate-900">AML & OFAC 50% Rule Screening Policy</h4>
              
              <div className="space-y-3 text-xs">
                <p>
                  <strong>OFAC 50% Rule Alignment:</strong> Pursuant to US Department of the Treasury guidance, entities owned 50 percent or more in the aggregate by one or more blocked persons are themselves considered blocked property, regardless of whether the entity is named on the SDN List. VeriSanctions assists compliance officers in detecting parent holding relationships and beneficial ownership ties.
                </p>
                <p>
                  <strong>FATF PEP Definitions:</strong> VeriSanctions indexes Politically Exposed Persons categorized into Tier 1 (Heads of State), Tier 2 (Cabinet Ministers/Supreme Court), Tier 3 (Regional Governors), and Tier 4 (State Enterprise Executives) in accordance with Financial Action Task Force recommendations.
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
            Close
          </button>
        </div>

      </div>
    </div>
  );
};
