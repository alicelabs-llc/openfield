import React, { useState } from 'react';
import { Check, Shield, Zap, CreditCard, Lock, Building, FileText, CheckCircle2 } from 'lucide-react';

interface PricingStripeProps {
  onSelectPlan: (plan: { id: string; name: string; price: number; interval: 'month' | 'year' }) => void;
}

export const PricingStripe: React.FC<PricingStripeProps> = ({ onSelectPlan }) => {
  const [interval, setInterval] = useState<'month' | 'year'>('month');

  const plans = [
    {
      id: 'starter',
      name: 'Free Starter',
      description: 'Ideal for independent legal counsel and testing sanctions coverage.',
      monthlyPrice: 0,
      annualPrice: 0,
      highlight: false,
      features: [
        '5 Live Watchlist checks per month',
        'Direct OpenSanctions cloud access',
        'OFAC SDN, EU, UN, & UK lists',
        'Web search console access',
        'Standard HTML export',
        'No credit card required'
      ],
      cta: 'Start Free'
    },
    {
      id: 'pro',
      name: 'Professional Compliance',
      description: 'Built for compliance officers, title companies, and fintech onboarding.',
      monthlyPrice: 99,
      annualPrice: 79,
      highlight: true,
      badge: 'MOST POPULAR',
      features: [
        'Unlimited manual screenings',
        '1,000 Automated API calls / month',
        'Certified Cryptographic PDF Dossiers',
        'Batch CSV Screening (500 entities / run)',
        'Politically Exposed Persons (PEP Tiers 1-4)',
        'Adverse Media & Law Enforcement alerts',
        'AliceLabs LLC US Corporate W-9 Invoice',
        'False-Positive Adjudication log'
      ],
      cta: 'Subscribe via Stripe'
    },
    {
      id: 'business',
      name: 'Business Enterprise',
      description: 'For commercial banks, high-volume payment rails, and enterprise AML desks.',
      monthlyPrice: 299,
      annualPrice: 239,
      highlight: false,
      features: [
        '50,000 Automated API calls / month',
        'Sub-300ms Dedicated Edge Cluster',
        'Unlimited Batch CSV Screening',
        'Webhooks for Ongoing Sanctions Monitoring',
        'Up to 15 Compliance Officer seats',
        'Custom Risk Weighting & Whitelisting',
        '99.99% Guaranteed SLA by AliceLabs LLC',
        'Priority Phone & Dedicated Compliance Desk'
      ],
      cta: 'Subscribe via Stripe'
    }
  ];

  return (
    <section id="pricing" className="py-16 sm:py-20 border-b border-slate-200 bg-white">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto">
          <div className="text-xs font-bold uppercase tracking-wider text-blue-700 mb-1">
            Transparent Pricing & Stripe Gateway
          </div>
          <h2 className="text-2xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
            Simple, predictable compliance billing
          </h2>
          <p className="mt-2 text-sm sm:text-base text-slate-600">
            No sales calls or hidden enterprise lock-in. Instant activation via Stripe with verified US LLC corporate billing.
          </p>

          {/* Billing Interval Toggle */}
          <div className="mt-6 inline-flex items-center rounded-lg border border-slate-300 bg-slate-100 p-1">
            <button
              onClick={() => setInterval('month')}
              className={`rounded-md px-4 py-1.5 text-xs font-bold transition-all cursor-pointer ${
                interval === 'month'
                  ? 'bg-white text-slate-900 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Monthly Billing
            </button>
            <button
              onClick={() => setInterval('year')}
              className={`flex items-center gap-1.5 rounded-md px-4 py-1.5 text-xs font-bold transition-all cursor-pointer ${
                interval === 'year'
                  ? 'bg-white text-slate-900 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <span>Annual Billing</span>
              <span className="text-[10px] text-emerald-800 font-bold bg-emerald-100 px-1.5 py-0.5 rounded border border-emerald-300">
                Save 20%
              </span>
            </button>
          </div>
        </div>

        {/* Pricing Cards Grid */}
        <div className="mt-12 grid grid-cols-1 gap-6 lg:grid-cols-3 lg:items-stretch">
          {plans.map((p) => {
            const price = interval === 'year' ? p.annualPrice : p.monthlyPrice;

            return (
              <div
                key={p.id}
                className={`relative flex flex-col justify-between rounded-xl border p-7 transition-all ${
                  p.highlight
                    ? 'border-blue-600 bg-blue-50/20 shadow-md ring-2 ring-blue-600'
                    : 'border-slate-300 bg-white hover:border-slate-400 shadow-xs'
                }`}
              >
                {/* Optional highlight badge */}
                {p.badge && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                    <span className="inline-flex items-center rounded-full bg-blue-700 px-3 py-0.5 text-[11px] font-bold uppercase tracking-wider text-white shadow-xs">
                      {p.badge}
                    </span>
                  </div>
                )}

                <div>
                  <h3 className="text-xl font-bold text-slate-900">{p.name}</h3>
                  <p className="mt-1.5 text-xs text-slate-600 min-h-[36px]">{p.description}</p>

                  {/* Price */}
                  <div className="mt-5 flex items-baseline gap-1">
                    <span className="text-4xl font-extrabold text-slate-900 font-mono tabular-nums">
                      ${price}
                    </span>
                    <span className="text-xs text-slate-500 font-medium">
                      / month {interval === 'year' && price > 0 ? '(billed annually)' : ''}
                    </span>
                  </div>

                  {/* Features List */}
                  <div className="mt-6 space-y-2.5">
                    <div className="text-xs font-bold uppercase tracking-wider text-slate-700">
                      Included Capabilities
                    </div>
                    {p.features.map((feat, fIdx) => (
                      <div key={fIdx} className="flex items-start gap-2 text-xs text-slate-700">
                        <Check className="h-4 w-4 text-emerald-600 shrink-0 mt-0.5" />
                        <span>{feat}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Card CTA */}
                <div className="mt-8 pt-5 border-t border-slate-200">
                  <button
                    onClick={() => onSelectPlan({ id: p.id, name: p.name, price, interval })}
                    className={`w-full rounded-lg py-2.5 text-xs font-bold transition-all cursor-pointer flex items-center justify-center gap-2 shadow-xs ${
                      p.highlight
                        ? 'bg-blue-700 text-white hover:bg-blue-800 focus-visible:outline-2 focus-visible:outline-blue-600'
                        : 'bg-slate-900 text-white hover:bg-slate-800'
                    }`}
                  >
                    <CreditCard className="h-3.5 w-3.5" />
                    <span>{p.cta}</span>
                  </button>

                  <div className="mt-2.5 flex items-center justify-center gap-1.5 text-[11px] text-slate-500 font-medium">
                    <Lock className="h-3 w-3 text-slate-400" />
                    <span>Secured by Stripe · Instant receipt</span>
                  </div>
                </div>

              </div>
            );
          })}
        </div>

        {/* Corporate Billing Notice by AliceLabs LLC */}
        <div className="mt-10 rounded-xl border border-slate-200 bg-slate-50 p-5 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <Building className="h-5 w-5 text-blue-700 shrink-0" />
            <div className="text-xs text-slate-700">
              <strong className="text-slate-900">Need an official US W-9 or ACH Wire invoicing?</strong>{' '}
              AliceLabs LLC provides direct corporate invoicing for US title companies and law firms with Net-30 terms available.
            </div>
          </div>
          <div className="shrink-0 flex items-center gap-2">
            <span className="font-mono text-xs text-slate-700 font-bold bg-white px-2.5 py-1 rounded border border-slate-300">
              EIN Available on Request
            </span>
          </div>
        </div>

      </div>
    </section>
  );
};
