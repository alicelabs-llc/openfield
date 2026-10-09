import React, { useState } from 'react';
import { Shield, Menu, X, ArrowUpRight } from 'lucide-react';

interface NavbarProps {
  onOpenLegal: () => void;
  onOpenBrandGuide: () => void;
  onScrollToSection: (sectionId: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  onOpenLegal,
  onOpenBrandGuide,
  onScrollToSection,
}) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-200 bg-white/95 backdrop-blur-md shadow-xs">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between gap-8 px-4 sm:px-6 lg:px-8">
        
        {/* Zone 1: Single text wordmark with corporate trust */}
        <a 
          href="#"
          onClick={(e) => { e.preventDefault(); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
          className="flex items-center gap-2.5 whitespace-nowrap shrink-0 group focus:outline-none"
        >
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-700 text-white shadow-xs">
            <Shield className="h-5 w-5" />
          </div>
          <div className="flex flex-col">
            <span className="text-lg font-bold tracking-tight text-slate-900 leading-none">
              VeriSanctions
            </span>
            <span className="text-[10px] font-medium text-slate-500 tracking-wide mt-0.5">
              by AliceLabs LLC
            </span>
          </div>
        </a>

        {/* Zone 2: 4-5 concise single-line text links */}
        <nav className="hidden md:flex items-center gap-8 text-sm font-semibold text-slate-600">
          <button 
            onClick={() => onScrollToSection('screener')}
            className="hover:text-blue-700 transition-colors whitespace-nowrap shrink-0 cursor-pointer"
          >
            Live Screener
          </button>
          <button 
            onClick={() => onScrollToSection('competitors')}
            className="hover:text-blue-700 transition-colors whitespace-nowrap shrink-0 cursor-pointer"
          >
            vs Competitors
          </button>
          <button 
            onClick={() => onScrollToSection('pricing')}
            className="hover:text-blue-700 transition-colors whitespace-nowrap shrink-0 cursor-pointer"
          >
            Pricing & Stripe
          </button>
          <button 
            onClick={() => onScrollToSection('api-docs')}
            className="hover:text-blue-700 transition-colors whitespace-nowrap shrink-0 cursor-pointer"
          >
            API Docs
          </button>
          <button 
            onClick={onOpenBrandGuide}
            className="text-slate-600 hover:text-blue-700 transition-colors whitespace-nowrap shrink-0 cursor-pointer"
          >
            US LLC Guide
          </button>
        </nav>

        {/* Zone 3: 1 primary action */}
        <div className="hidden md:flex items-center gap-3 shrink-0">
          <button
            onClick={() => onScrollToSection('screener')}
            className="flex items-center gap-1.5 rounded-lg bg-blue-700 px-4 py-2 text-xs font-semibold text-white shadow-xs transition-colors hover:bg-blue-800 focus-visible:outline-2 focus-visible:outline-blue-600 whitespace-nowrap shrink-0 cursor-pointer"
          >
            <span>Run Free Check</span>
            <ArrowUpRight className="h-3.5 w-3.5" />
          </button>
        </div>

        {/* Mobile menu trigger */}
        <div className="flex md:hidden">
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="p-2 text-slate-600 hover:text-slate-900 focus:outline-none"
            aria-label="Toggle navigation menu"
          >
            {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden border-b border-slate-200 bg-white px-4 py-5 space-y-3 shadow-lg">
          <button
            onClick={() => { onScrollToSection('screener'); setMobileMenuOpen(false); }}
            className="block w-full text-left py-2 text-sm font-semibold text-slate-700 hover:text-blue-700"
          >
            Live Screener
          </button>
          <button
            onClick={() => { onScrollToSection('competitors'); setMobileMenuOpen(false); }}
            className="block w-full text-left py-2 text-sm font-semibold text-slate-700 hover:text-blue-700"
          >
            vs Competitors
          </button>
          <button
            onClick={() => { onScrollToSection('pricing'); setMobileMenuOpen(false); }}
            className="block w-full text-left py-2 text-sm font-semibold text-slate-700 hover:text-blue-700"
          >
            Pricing & Stripe
          </button>
          <button
            onClick={() => { onScrollToSection('api-docs'); setMobileMenuOpen(false); }}
            className="block w-full text-left py-2 text-sm font-semibold text-slate-700 hover:text-blue-700"
          >
            API Documentation
          </button>
          <button
            onClick={() => { onOpenBrandGuide(); setMobileMenuOpen(false); }}
            className="block w-full text-left py-2 text-sm font-semibold text-blue-700"
          >
            US Brand & Domain Blueprint
          </button>
          <button
            onClick={() => { onOpenLegal(); setMobileMenuOpen(false); }}
            className="block w-full text-left py-2 text-sm font-semibold text-slate-600 hover:text-slate-900"
          >
            AliceLabs Legal & FCRA Terms
          </button>
          <button
            onClick={() => { onScrollToSection('screener'); setMobileMenuOpen(false); }}
            className="w-full mt-3 rounded-lg bg-blue-700 py-2.5 text-center text-xs font-semibold text-white hover:bg-blue-800"
          >
            Run Free Sanctions Check
          </button>
        </div>
      )}
    </header>
  );
};
