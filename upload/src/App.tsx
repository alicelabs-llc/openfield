/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import { Hero } from './components/Hero';
import { Screener } from './components/Screener';
import { BatchScreener } from './components/BatchScreener';
import { CompetitorMatrix } from './components/CompetitorMatrix';
import { PricingStripe } from './components/PricingStripe';
import { ApiDocs } from './components/ApiDocs';
import { Footer } from './components/Footer';
import { CertifiedReportModal } from './components/CertifiedReportModal';
import { EmailReportModal } from './components/EmailReportModal';
import { StripeCheckoutModal } from './components/StripeCheckoutModal';
import { DomainBrandGuideModal } from './components/DomainBrandGuideModal';
import { LegalPoliciesModal } from './components/LegalPoliciesModal';
import { SanctionEntity } from './types';
import { Building2 } from 'lucide-react';

export default function App() {
  // Modal states
  const [certifiedModal, setCertifiedModal] = useState<{
    isOpen: boolean;
    entity: SanctionEntity | null;
    query: string;
    isCleanPass: boolean;
  }>({
    isOpen: false,
    entity: null,
    query: '',
    isCleanPass: false,
  });

  const [emailModal, setEmailModal] = useState<{
    isOpen: boolean;
    entity: SanctionEntity | null;
    query: string;
  }>({
    isOpen: false,
    entity: null,
    query: '',
  });

  const [stripeModal, setStripeModal] = useState<{
    isOpen: boolean;
    plan: {
      id: string;
      name: string;
      price: number;
      interval: 'month' | 'year';
    } | null;
  }>({
    isOpen: false,
    plan: null,
  });

  const [brandGuideOpen, setBrandGuideOpen] = useState(false);
  const [legalOpen, setLegalOpen] = useState(false);

  // Smooth scroll handler
  const handleScrollToSection = (sectionId: string) => {
    const el = document.getElementById(sectionId);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  // Open certified report
  const handleOpenCertifiedPdf = (
    entity: SanctionEntity | null,
    query: string,
    isCleanPass: boolean
  ) => {
    setCertifiedModal({
      isOpen: true,
      entity,
      query,
      isCleanPass,
    });
  };

  // Open email dispatch
  const handleOpenEmailReport = (entity: SanctionEntity | null, query: string) => {
    setEmailModal({
      isOpen: true,
      entity,
      query,
    });
  };

  // Open Stripe checkout
  const handleSelectPlan = (plan: {
    id: string;
    name: string;
    price: number;
    interval: 'month' | 'year';
  }) => {
    setStripeModal({
      isOpen: true,
      plan,
    });
  };

  return (
    <div className="min-h-screen bg-white text-slate-900 flex flex-col font-sans">
      
      {/* Top Advisory Banner */}
      <div className="border-b border-slate-200 bg-slate-100 px-4 py-2 text-center text-xs text-slate-700">
        <div className="mx-auto flex max-w-7xl items-center justify-center gap-2">
          <Building2 className="h-3.5 w-3.5 text-blue-700 shrink-0" />
          <span>
            <strong>AliceLabs LLC:</strong> Enterprise Sanctions & AML Screening Engine. OpenSanctions Live Sync Active.
          </span>
          <button
            onClick={() => setBrandGuideOpen(true)}
            className="ml-2 font-bold text-blue-700 underline hover:text-blue-800 cursor-pointer"
          >
            Review US Domain & LLC Guide →
          </button>
        </div>
      </div>

      {/* Main Navigation */}
      <Navbar
        onOpenLegal={() => setLegalOpen(true)}
        onOpenBrandGuide={() => setBrandGuideOpen(true)}
        onScrollToSection={handleScrollToSection}
      />

      {/* Main Content Sections */}
      <main className="flex-1">
        {/* Hero Section */}
        <Hero
          onStartSearch={() => handleScrollToSection('screener')}
          onExplorePricing={() => handleScrollToSection('pricing')}
        />

        {/* Live KYC / AML Screener */}
        <Screener
          onGenerateCertifiedPdf={handleOpenCertifiedPdf}
          onSendEmailReport={handleOpenEmailReport}
        />

        {/* Batch CSV Screening Engine */}
        <BatchScreener />

        {/* Competitor Benchmark (sanctions.io, Dilisense, ComplyAdvantage, ComplyCube, World-Check) */}
        <CompetitorMatrix />

        {/* Transparent Pricing with Stripe Checkout */}
        <PricingStripe onSelectPlan={handleSelectPlan} />

        {/* Interactive REST API Documentation */}
        <ApiDocs />
      </main>

      {/* Institutional Footer */}
      <Footer
        onOpenLegal={() => setLegalOpen(true)}
        onOpenBrandGuide={() => setBrandGuideOpen(true)}
        onScrollToSection={handleScrollToSection}
      />

      {/* Certified PDF Dossier Modal */}
      <CertifiedReportModal
        isOpen={certifiedModal.isOpen}
        onClose={() => setCertifiedModal({ ...certifiedModal, isOpen: false })}
        entity={certifiedModal.entity}
        query={certifiedModal.query}
        isCleanPass={certifiedModal.isCleanPass}
      />

      {/* Email Report Modal */}
      <EmailReportModal
        isOpen={emailModal.isOpen}
        onClose={() => setEmailModal({ ...emailModal, isOpen: false })}
        entity={emailModal.entity}
        query={emailModal.query}
      />

      {/* Stripe Checkout Simulation Modal */}
      <StripeCheckoutModal
        isOpen={stripeModal.isOpen}
        onClose={() => setStripeModal({ ...stripeModal, isOpen: false })}
        plan={stripeModal.plan}
      />

      {/* US Domain & LLC Brand Guide Modal */}
      <DomainBrandGuideModal
        isOpen={brandGuideOpen}
        onClose={() => setBrandGuideOpen(false)}
      />

      {/* Legal & FCRA Compliance Modal */}
      <LegalPoliciesModal
        isOpen={legalOpen}
        onClose={() => setLegalOpen(false)}
      />

    </div>
  );
}
