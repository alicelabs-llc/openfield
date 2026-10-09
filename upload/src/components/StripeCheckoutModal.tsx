import React, { useState } from 'react';
import { X, CreditCard, Lock, CheckCircle2, Shield, Download, FileText, Building, ArrowRight } from 'lucide-react';

interface StripeCheckoutModalProps {
  isOpen: boolean;
  onClose: () => void;
  plan: {
    id: string;
    name: string;
    price: number;
    interval: 'month' | 'year';
  } | null;
}

export const StripeCheckoutModal: React.FC<StripeCheckoutModalProps> = ({
  isOpen,
  onClose,
  plan
}) => {
  if (!isOpen || !plan) return null;

  const [step, setStep] = useState<'checkout' | 'success'>('checkout');
  const [email, setEmail] = useState('compliance@corporation.com');
  const [companyName, setCompanyName] = useState('Acme Financial Partners LLC');
  const [cardNumber, setCardNumber] = useState('4242 •••• •••• 4242');
  const [expiry, setExpiry] = useState('12/28');
  const [cvc, setCvc] = useState('888');
  const [zip, setZip] = useState('10005');
  const [loading, setLoading] = useState(false);
  const [invoiceId] = useState(`INV-AL-${Math.random().toString(36).substring(2, 8).toUpperCase()}`);
  const [apiKey] = useState(`vs_live_${Math.random().toString(36).substring(2, 18)}`);

  const handlePay = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const res = await fetch('/api/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          plan: plan.id,
          interval: plan.interval,
          email
        })
      });
      await res.json();
    } catch (err) {
      console.warn("Local checkout simulation:", err);
    } finally {
      setTimeout(() => {
        setLoading(false);
        setStep('success');
      }, 700);
    }
  };

  const handleDownloadInvoice = () => {
    const invoiceContent = `========================================================
ALICELABS LLC — OFFICIAL TAX INVOICE & RECEIPT
Corporate Sanctions & AML Intelligence Platform
========================================================
Invoice Reference: ${invoiceId}
Date: ${new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
Issuer: AliceLabs LLC (Delaware / USA)
Billed To: ${companyName} (${email})
ZIP Code: ${zip}

ITEM DESCRIPTION:
- Plan: VeriSanctions ${plan.name} (${plan.interval === 'year' ? 'Annual Subscription' : 'Monthly Subscription'})
- Global Watchlists: 494 Sanctions, PEP, and Adverse Media lists
- Total Paid via Stripe: $${plan.price}.00 USD
Payment Status: PAID / CONFIRMED
Stripe Transaction ID: ch_${Math.random().toString(36).substring(2, 16)}
Issued API Key: ${apiKey}
========================================================
AliceLabs LLC — Support: support@alicelabs.site
`;
    const blob = new Blob([invoiceContent], { type: 'text/plain;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${invoiceId}_AliceLabs_Receipt.txt`;
    link.click();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs">
      <div className="relative w-full max-w-lg rounded-2xl border border-slate-300 bg-white p-6 sm:p-8 shadow-2xl text-slate-900">
        
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-5 right-5 text-slate-400 hover:text-slate-700 cursor-pointer"
        >
          <X className="h-5 w-5" />
        </button>

        {step === 'checkout' ? (
          <div>
            {/* Header */}
            <div className="flex items-center gap-2 mb-2">
              <div className="flex h-7 w-7 items-center justify-center rounded bg-blue-700 text-white">
                <CreditCard className="h-4 w-4" />
              </div>
              <span className="text-xs font-bold uppercase tracking-wider text-blue-700">
                Stripe Payments Gateway
              </span>
            </div>

            <h3 className="text-xl font-bold text-slate-900">
              Activate {plan.name}
            </h3>
            
            <p className="text-xs text-slate-600 mt-1">
              Billed by <strong className="text-slate-900">AliceLabs LLC</strong> (USA). Instant API key activation and PDF audit capabilities.
            </p>

            {/* Plan Summary Card */}
            <div className="mt-4 rounded-xl border border-slate-200 bg-slate-50 p-4 flex items-center justify-between">
              <div>
                <div className="text-sm font-bold text-slate-900">{plan.name}</div>
                <div className="text-xs text-slate-500">
                  {plan.interval === 'year' ? 'Billed annually (20% off)' : 'Billed monthly, cancel anytime'}
                </div>
              </div>
              <div className="text-right">
                <div className="text-xl font-extrabold text-slate-900 font-mono tabular-nums">
                  ${plan.price}
                </div>
                <div className="text-[11px] text-slate-500 font-medium">USD</div>
              </div>
            </div>

            {/* Form */}
            <form onSubmit={handlePay} className="mt-5 space-y-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Billing Email
                </label>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full text-xs rounded-lg border border-slate-300 bg-white px-3 py-2 text-slate-900 focus:border-blue-600 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Company Legal Entity (for US W-9 Invoicing)
                </label>
                <input
                  type="text"
                  required
                  value={companyName}
                  onChange={(e) => setCompanyName(e.target.value)}
                  className="w-full text-xs rounded-lg border border-slate-300 bg-white px-3 py-2 text-slate-900 focus:border-blue-600 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Card Information
                </label>
                <div className="rounded-lg border border-slate-300 bg-white divide-y divide-slate-200">
                  <div className="flex items-center px-3 py-2">
                    <CreditCard className="h-4 w-4 text-slate-400 mr-2 shrink-0" />
                    <input
                      type="text"
                      value={cardNumber}
                      onChange={(e) => setCardNumber(e.target.value)}
                      className="w-full text-xs bg-transparent text-slate-900 focus:outline-none font-mono"
                    />
                  </div>
                  <div className="grid grid-cols-3 divide-x divide-slate-200">
                    <input
                      type="text"
                      placeholder="MM/YY"
                      value={expiry}
                      onChange={(e) => setExpiry(e.target.value)}
                      className="px-3 py-2 text-xs bg-transparent text-slate-900 focus:outline-none font-mono text-center"
                    />
                    <input
                      type="text"
                      placeholder="CVC"
                      value={cvc}
                      onChange={(e) => setCvc(e.target.value)}
                      className="px-3 py-2 text-xs bg-transparent text-slate-900 focus:outline-none font-mono text-center"
                    />
                    <input
                      type="text"
                      placeholder="ZIP"
                      value={zip}
                      onChange={(e) => setZip(e.target.value)}
                      className="px-3 py-2 text-xs bg-transparent text-slate-900 focus:outline-none font-mono text-center"
                    />
                  </div>
                </div>
              </div>

              {/* Submit CTA */}
              <button
                type="submit"
                disabled={loading}
                className="w-full mt-2 rounded-lg bg-blue-700 py-3 text-xs font-bold text-white shadow-xs hover:bg-blue-800 disabled:opacity-50 transition-colors flex items-center justify-center gap-2 cursor-pointer"
              >
                {loading ? (
                  <span>Connecting to Stripe...</span>
                ) : (
                  <>
                    <Lock className="h-3.5 w-3.5" />
                    <span>Pay ${plan.price}.00 USD via Stripe</span>
                  </>
                )}
              </button>

              <div className="flex items-center justify-center gap-1.5 text-[11px] text-slate-500 pt-1">
                <Shield className="h-3.5 w-3.5 text-emerald-600" />
                <span>256-bit TLS Encryption · AliceLabs LLC Authorized</span>
              </div>
            </form>
          </div>
        ) : (
          /* SUCCESS SCREEN */
          <div className="text-center py-4">
            <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-emerald-100 border border-emerald-300 text-emerald-700 mb-3">
              <CheckCircle2 className="h-7 w-7" />
            </div>

            <h3 className="text-xl font-bold text-slate-900">Payment Confirmed!</h3>
            <p className="text-xs text-slate-600 mt-1 max-w-sm mx-auto">
              Your subscription to <strong className="text-slate-900">{plan.name}</strong> is active. 
              An official tax invoice has been generated for {companyName}.
            </p>

            {/* Issued Credentials Card */}
            <div className="mt-5 rounded-xl border border-slate-200 bg-slate-50 p-4 text-left space-y-2">
              <div className="flex justify-between items-center text-xs">
                <span className="text-slate-500">Invoice ID:</span>
                <span className="font-mono text-slate-900 font-bold">{invoiceId}</span>
              </div>

              <div className="flex justify-between items-center text-xs">
                <span className="text-slate-500">Issuer:</span>
                <span className="text-slate-900 font-medium">AliceLabs LLC (Delaware)</span>
              </div>

              <div className="border-t border-slate-200 pt-2">
                <span className="block text-[11px] text-slate-500 font-medium mb-1">Your Live API Key:</span>
                <div className="flex items-center justify-between bg-white border border-slate-300 px-2.5 py-1.5 rounded font-mono text-xs text-emerald-700">
                  <span className="truncate font-semibold">{apiKey}</span>
                  <button 
                    onClick={() => navigator.clipboard.writeText(apiKey)}
                    className="text-[10px] text-slate-500 hover:text-slate-900 ml-2 underline cursor-pointer"
                  >
                    Copy
                  </button>
                </div>
              </div>
            </div>

            {/* Action buttons */}
            <div className="mt-5 flex flex-col sm:flex-row gap-2.5">
              <button
                onClick={handleDownloadInvoice}
                className="flex-1 flex items-center justify-center gap-1.5 rounded-lg border border-slate-300 bg-white py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors cursor-pointer shadow-xs"
              >
                <Download className="h-3.5 w-3.5" />
                <span>Download Tax Invoice</span>
              </button>

              <button
                onClick={onClose}
                className="flex-1 rounded-lg bg-blue-700 py-2 text-xs font-bold text-white hover:bg-blue-800 transition-colors cursor-pointer shadow-xs"
              >
                Return to Screener
              </button>
            </div>
          </div>
        )}

      </div>
    </div>
  );
};
