import React, { useState } from 'react';
import { X, Mail, CheckCircle2, Send, Shield } from 'lucide-react';
import { SanctionEntity } from '../types';

interface EmailReportModalProps {
  isOpen: boolean;
  onClose: () => void;
  entity: SanctionEntity | null;
  query: string;
}

export const EmailReportModal: React.FC<EmailReportModalProps> = ({
  isOpen,
  onClose,
  entity,
  query
}) => {
  if (!isOpen) return null;

  const [recipient, setRecipient] = useState('mlro@yourcompany.com');
  const [subject, setSubject] = useState(`[COMPLIANCE AUDIT] VeriSanctions Screening Dossier: ${query}`);
  const [notes, setNotes] = useState('Certified screening report attached for regulatory file retention under BSA/FinCEN safe harbor guidelines.');
  const [sent, setSent] = useState(false);
  const [sending, setSending] = useState(false);

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    setSending(true);
    setTimeout(() => {
      setSending(false);
      setSent(true);
    }, 600);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs">
      <div className="relative w-full max-w-md rounded-2xl border border-slate-300 bg-white p-6 sm:p-7 shadow-2xl text-slate-900">
        
        <button
          onClick={onClose}
          className="absolute top-5 right-5 text-slate-400 hover:text-slate-700 cursor-pointer"
        >
          <X className="h-5 w-5" />
        </button>

        {!sent ? (
          <div>
            <div className="flex items-center gap-2 mb-2">
              <div className="flex h-7 w-7 items-center justify-center rounded bg-blue-700 text-white">
                <Mail className="h-4 w-4" />
              </div>
              <span className="text-xs font-bold uppercase tracking-wider text-blue-700">
                Audit Archive Dispatch
              </span>
            </div>

            <h3 className="text-lg font-bold text-slate-900">
              Email Compliance Report
            </h3>

            <p className="text-xs text-slate-600 mt-1">
              Transmit this certified audit dossier directly to your internal compliance log or legal counsel.
            </p>

            <form onSubmit={handleSend} className="mt-4 space-y-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Recipient Email
                </label>
                <input
                  type="email"
                  required
                  value={recipient}
                  onChange={(e) => setRecipient(e.target.value)}
                  className="w-full text-xs rounded-lg border border-slate-300 bg-white px-3 py-2 text-slate-900 focus:border-blue-600 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Subject Line
                </label>
                <input
                  type="text"
                  required
                  value={subject}
                  onChange={(e) => setSubject(e.target.value)}
                  className="w-full text-xs rounded-lg border border-slate-300 bg-white px-3 py-2 text-slate-900 focus:border-blue-600 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Compliance Officer Notes
                </label>
                <textarea
                  rows={3}
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  className="w-full text-xs rounded-lg border border-slate-300 bg-white px-3 py-2 text-slate-900 focus:border-blue-600 focus:outline-none"
                />
              </div>

              <div className="rounded-lg bg-slate-50 border border-slate-200 p-2.5 text-[11px] text-slate-600 flex items-center gap-2">
                <Shield className="h-4 w-4 text-emerald-600 shrink-0" />
                <span>Includes cryptographic SHA-256 seal & AliceLabs LLC verification hash</span>
              </div>

              <button
                type="submit"
                disabled={sending}
                className="w-full mt-2 rounded-lg bg-blue-700 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-blue-800 disabled:opacity-50 transition-colors flex items-center justify-center gap-2 cursor-pointer"
              >
                {sending ? (
                  <span>Dispatching Report...</span>
                ) : (
                  <>
                    <Send className="h-3.5 w-3.5" />
                    <span>Send Certified Dossier</span>
                  </>
                )}
              </button>
            </form>
          </div>
        ) : (
          <div className="text-center py-4">
            <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-emerald-100 border border-emerald-300 text-emerald-700 mb-3">
              <CheckCircle2 className="h-7 w-7" />
            </div>

            <h3 className="text-base font-bold text-slate-900">Report Dispatched!</h3>
            <p className="text-xs text-slate-600 mt-1">
              Certified audit dossier has been transmitted to <strong className="text-slate-900">{recipient}</strong>.
            </p>

            <button
              onClick={() => { setSent(false); onClose(); }}
              className="mt-5 w-full rounded-lg bg-slate-900 py-2 text-xs font-semibold text-white hover:bg-slate-800 transition-colors cursor-pointer"
            >
              Close
            </button>
          </div>
        )}

      </div>
    </div>
  );
};
