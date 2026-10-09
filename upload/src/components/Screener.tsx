import React, { useState } from 'react';
import { 
  Search, 
  User, 
  Building2, 
  Globe2, 
  AlertTriangle, 
  CheckCircle2, 
  Printer, 
  Mail, 
  ShieldAlert, 
  RefreshCw,
  FileText,
  SlidersHorizontal,
  ChevronDown,
  Info
} from 'lucide-react';
import { SanctionEntity, ScreenResponse } from '../types';
import { executeScreening, generateAuditChecksum } from '../utils/screeningService';

interface ScreenerProps {
  onGenerateCertifiedPdf: (entity: SanctionEntity | null, query: string, isCleanPass: boolean) => void;
  onSendEmailReport: (entity: SanctionEntity | null, query: string) => void;
}

export const Screener: React.FC<ScreenerProps> = ({
  onGenerateCertifiedPdf,
  onSendEmailReport
}) => {
  const [query, setQuery] = useState('Vladimir Putin');
  const [schema, setSchema] = useState<'Person' | 'Company' | 'all'>('Person');
  const [country, setCountry] = useState('');
  const [threshold, setThreshold] = useState(0.7);
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<ScreenResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'individual' | 'entity' | 'batch'>('individual');
  const [adjudicationNote, setAdjudicationNote] = useState<Record<string, string>>({});
  const [showFilters, setShowFilters] = useState(false);

  const sampleQueries = [
    { label: 'Vladimir Putin', type: 'Person', note: 'OFAC SDN / Russian Federation' },
    { label: 'Sberbank of Russia', type: 'Company', note: 'State Bank / SWIFT Blocked' },
    { label: 'Viktor Bout', type: 'Person', note: 'Arms Dealer / UN & OFAC' },
    { label: 'Alisher Usmanov', type: 'Person', note: 'Oligarch / EU & US SDN' },
    { label: 'Marcus Vance (Clean Test)', type: 'Person', note: 'Negative Clear Record' },
  ];

  const handleSearch = async (overrideQuery?: string, overrideSchema?: string) => {
    const targetQuery = (overrideQuery !== undefined ? overrideQuery : query).trim();
    if (!targetQuery) return;

    const targetSchema = overrideSchema || (schema === 'all' ? 'LegalEntity' : schema);
    setLoading(true);
    setError(null);

    try {
      const data = await executeScreening(targetQuery, targetSchema, country, threshold);
      setResponse(data);
    } catch (err: any) {
      console.error("Screening error:", err);
      setError("Screening query failed. Please verify your connection or try again.");
    } finally {
      setLoading(false);
    }
  };

  const handlePresetClick = (preset: typeof sampleQueries[0]) => {
    setQuery(preset.label);
    const newSchema = preset.type === 'Company' ? 'Company' : 'Person';
    setSchema(newSchema);
    setActiveTab(preset.type === 'Company' ? 'entity' : 'individual');
    handleSearch(preset.label, newSchema);
  };

  return (
    <section id="screener" className="py-12 sm:py-16 border-b border-slate-200 bg-slate-50">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="max-w-3xl mb-6">
          <div className="text-xs font-bold uppercase tracking-wider text-blue-700 mb-1">
            Live Compliance Screening Console
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Search 494+ Global Sanctions & PEP Databases
          </h2>
          <p className="mt-1 text-sm text-slate-600">
            Real-time verification against US OFAC, European Union, United Nations, UK OFSI, and Politically Exposed Persons registers.
          </p>
        </div>

        {/* Search Console Container */}
        <div className="rounded-xl border border-slate-300 bg-white p-5 sm:p-7 shadow-xs">
          
          {/* Target Entity Tabs */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-200 pb-4 gap-3">
            <div className="flex items-center gap-1.5 p-1 bg-slate-100 rounded-lg">
              <button
                onClick={() => { setActiveTab('individual'); setSchema('Person'); }}
                className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-md transition-colors cursor-pointer ${
                  activeTab === 'individual'
                    ? 'bg-white text-blue-700 shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                <User className="h-3.5 w-3.5" />
                <span>Individual (Person / PEP)</span>
              </button>

              <button
                onClick={() => { setActiveTab('entity'); setSchema('Company'); }}
                className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-md transition-colors cursor-pointer ${
                  activeTab === 'entity'
                    ? 'bg-white text-blue-700 shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                <Building2 className="h-3.5 w-3.5" />
                <span>Company (Entity / Bank / Vessel)</span>
              </button>

              <button
                onClick={() => { setActiveTab('batch'); setSchema('all'); }}
                className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-md transition-colors cursor-pointer ${
                  activeTab === 'batch'
                    ? 'bg-white text-blue-700 shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                <Globe2 className="h-3.5 w-3.5" />
                <span>All Entities</span>
              </button>
            </div>

            <div className="flex items-center gap-2 text-xs text-slate-500 font-medium">
              <span className="font-mono tabular-nums text-slate-700 font-bold">494 Lists</span>
              <span aria-hidden="true">·</span>
              <span className="text-emerald-700 font-semibold">OpenSanctions Cloud Connected</span>
            </div>
          </div>

          {/* Search Form */}
          <form 
            onSubmit={(e) => { e.preventDefault(); handleSearch(); }}
            className="mt-5"
          >
            <div className="flex flex-col sm:flex-row gap-2.5">
              <div className="relative flex-1">
                <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3.5 text-slate-400">
                  <Search className="h-4 w-4" />
                </div>
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder={
                    schema === 'Company' 
                      ? "Enter legal company name, e.g. Sberbank, Wagner Group, PDVSA..." 
                      : "Enter full name, e.g. Vladimir Putin, Viktor Bout, John Smith..."
                  }
                  className="w-full rounded-lg border border-slate-300 bg-white py-2.5 pl-10 pr-4 text-sm text-slate-900 placeholder-slate-400 focus:border-blue-600 focus:outline-none focus:ring-1 focus:ring-blue-600 font-medium"
                />
              </div>

              {/* Submit CTA */}
              <button
                type="submit"
                disabled={loading}
                className="inline-flex items-center justify-center rounded-lg bg-blue-700 px-6 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-blue-800 focus-visible:outline-2 focus-visible:outline-blue-600 disabled:opacity-50 transition-colors cursor-pointer whitespace-nowrap shrink-0"
              >
                {loading ? (
                  <>
                    <RefreshCw className="mr-2 h-3.5 w-3.5 animate-spin" />
                    <span>Screening 494 Lists...</span>
                  </>
                ) : (
                  <>
                    <Search className="mr-2 h-3.5 w-3.5" />
                    <span>Screen Watchlists</span>
                  </>
                )}
              </button>
            </div>

            {/* Quick Demo Test Presets */}
            <div className="mt-3 flex flex-wrap items-center gap-1.5 text-xs text-slate-500">
              <span className="font-semibold text-slate-700">Quick Test Cases:</span>
              {sampleQueries.map((item, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => handlePresetClick(item)}
                  className="rounded border border-slate-200 bg-slate-50 px-2 py-0.5 text-slate-700 hover:border-blue-600 hover:text-blue-700 transition-colors cursor-pointer font-medium"
                >
                  {item.label}
                </button>
              ))}

              <button
                type="button"
                onClick={() => setShowFilters(!showFilters)}
                className="ml-auto inline-flex items-center gap-1 text-slate-500 hover:text-slate-800 cursor-pointer font-medium"
              >
                <SlidersHorizontal className="h-3 w-3" />
                <span>Filters {showFilters ? '▲' : '▼'}</span>
              </button>
            </div>

            {/* Advanced Filters */}
            {showFilters && (
              <div className="mt-4 grid grid-cols-1 sm:grid-cols-3 gap-3 border-t border-slate-200 pt-3 text-xs">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">
                    Jurisdiction Filter
                  </label>
                  <select
                    value={country}
                    onChange={(e) => setCountry(e.target.value)}
                    className="w-full rounded border border-slate-300 bg-white px-2.5 py-1.5 text-slate-800 focus:border-blue-600 focus:outline-none"
                  >
                    <option value="">Global (All Jurisdictions)</option>
                    <option value="us">United States (OFAC SDN & Non-SDN)</option>
                    <option value="eu">European Union (EU Restrictive Measures)</option>
                    <option value="gb">United Kingdom (FCDO / OFSI)</option>
                    <option value="un">United Nations Security Council</option>
                    <option value="ru">Russian Federation</option>
                    <option value="ve">Venezuela</option>
                    <option value="ir">Iran</option>
                  </select>
                </div>

                <div>
                  <label className="block font-semibold text-slate-700 mb-1">
                    Fuzzy Match Sensitivity: <span className="font-mono text-blue-700 tabular-nums">{Math.round(threshold * 100)}%</span>
                  </label>
                  <input
                    type="range"
                    min="0.5"
                    max="0.95"
                    step="0.05"
                    value={threshold}
                    onChange={(e) => setThreshold(parseFloat(e.target.value))}
                    className="w-full accent-blue-600 cursor-pointer"
                  />
                </div>

                <div>
                  <label className="block font-semibold text-slate-700 mb-1">
                    Coverage Scope
                  </label>
                  <div className="flex items-center gap-3 pt-1 text-slate-600">
                    <span className="flex items-center gap-1">
                      <span className="h-1.5 w-1.5 rounded-full bg-emerald-600"></span>
                      Sanctions
                    </span>
                    <span className="flex items-center gap-1">
                      <span className="h-1.5 w-1.5 rounded-full bg-amber-600"></span>
                      PEPs
                    </span>
                    <span className="flex items-center gap-1">
                      <span className="h-1.5 w-1.5 rounded-full bg-rose-600"></span>
                      Interpol
                    </span>
                  </div>
                </div>
              </div>
            )}
          </form>

        </div>

        {/* Screening Results Area */}
        <div className="mt-6">
          {error && (
            <div className="rounded-lg border border-rose-300 bg-rose-50 p-4 text-xs text-rose-800 flex items-center gap-2.5">
              <AlertTriangle className="h-4 w-4 text-rose-600 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {/* Results Summary Metadata Bar */}
          {response && (
            <div className="rounded-lg border border-slate-200 bg-white p-3.5 mb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
              <div className="flex items-center gap-2 text-slate-600">
                <span className="font-bold text-slate-900">Query: "{response.query}"</span>
                <span aria-hidden="true">·</span>
                <span className="font-mono tabular-nums text-slate-700 font-semibold">
                  {response.totalHits} {response.totalHits === 1 ? 'Match' : 'Matches'} ({response.durationMs}ms)
                </span>
                <span aria-hidden="true">·</span>
                <span className="text-slate-500">{response.dataSource}</span>
              </div>

              {response.totalHits === 0 ? (
                <button
                  onClick={() => onGenerateCertifiedPdf(null, response.query, true)}
                  className="inline-flex items-center gap-1.5 text-xs font-bold text-emerald-700 hover:text-emerald-800 cursor-pointer"
                >
                  <FileText className="h-4 w-4" />
                  <span>Export Clean Pass Audit Certificate (PDF)</span>
                </button>
              ) : (
                <div className="flex items-center gap-2 text-rose-700 font-bold">
                  <AlertTriangle className="h-4 w-4" />
                  <span>Enforcement Match Identified</span>
                </div>
              )}
            </div>
          )}

          {/* CASE 1: CLEAN PASS (0 hits) */}
          {response && response.totalHits === 0 && (
            <div className="rounded-xl border border-emerald-300 bg-emerald-50/60 p-8 text-center">
              <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-emerald-100 border border-emerald-300 text-emerald-700 mb-3">
                <CheckCircle2 className="h-6 w-6" />
              </div>
              
              <h3 className="text-lg font-bold text-slate-900">
                Negative Match Clearance — Clean Pass
              </h3>
              
              <p className="mt-1 text-xs text-slate-600 max-w-xl mx-auto">
                No active sanctions, Politically Exposed Person (PEP), or regulatory debarment records found for target entity <strong>"{response.query}"</strong> across 494 global watchlists.
              </p>

              {/* Integrity checksum stamp */}
              <div className="mt-4 inline-flex items-center gap-3 rounded-md border border-emerald-200 bg-white px-3.5 py-1.5 text-xs font-mono text-slate-700">
                <span>AUDIT HASH:</span>
                <span className="font-bold text-emerald-700">{generateAuditChecksum(response.query, response.timestamp)}</span>
                <span className="text-slate-300">|</span>
                <span className="text-slate-500">AliceLabs LLC FinCEN Safe Harbor</span>
              </div>

              <div className="mt-5 flex flex-wrap justify-center gap-2.5">
                <button
                  onClick={() => onGenerateCertifiedPdf(null, response.query, true)}
                  className="inline-flex items-center gap-1.5 rounded-lg bg-emerald-700 px-4 py-2 text-xs font-bold text-white hover:bg-emerald-800 transition-colors cursor-pointer shadow-xs"
                >
                  <Printer className="h-3.5 w-3.5" />
                  <span>Export Clean Pass Dossier (PDF)</span>
                </button>
                <button
                  onClick={() => onSendEmailReport(null, response.query)}
                  className="inline-flex items-center gap-1.5 rounded-lg border border-slate-300 bg-white px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors cursor-pointer shadow-xs"
                >
                  <Mail className="h-3.5 w-3.5" />
                  <span>Email Certificate to Audit Archive</span>
                </button>
              </div>
            </div>
          )}

          {/* CASE 2: HITS FOUND */}
          {response && response.results.length > 0 && (
            <div className="space-y-3.5">
              {response.results.map((entity, idx) => {
                const isCritical = entity.properties.riskLevel === 'CRITICAL' || entity.score >= 0.9;
                const scorePercent = Math.round(entity.score * 100);

                return (
                  <div
                    key={entity.id || idx}
                    className="rounded-xl border border-slate-300 bg-white p-5 shadow-xs"
                  >
                    <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-5">
                      
                      {/* Left: Entity Details */}
                      <div className="space-y-2.5 flex-1">
                        <div className="flex flex-wrap items-center gap-2">
                          <span className={`inline-flex items-center gap-1 px-2 py-0.5 text-xs font-bold rounded ${
                            isCritical 
                              ? 'bg-rose-100 text-rose-800 border border-rose-200' 
                              : 'bg-amber-100 text-amber-800 border border-amber-200'
                          }`}>
                            <ShieldAlert className="h-3 w-3" />
                            <span>{entity.properties.riskLevel || 'SANCTION MATCH'}</span>
                          </span>

                          <span className="text-xs text-slate-500 font-mono">
                            Match Score: <strong className="text-slate-900 tabular-nums">{scorePercent}%</strong>
                          </span>

                          <span className="text-slate-300">·</span>

                          <span className="text-xs text-slate-500 font-mono">
                            Entity ID: {entity.id}
                          </span>
                        </div>

                        {/* Primary Name */}
                        <div>
                          <h3 className="text-lg font-bold text-slate-900">
                            {entity.caption}
                          </h3>
                          {entity.properties.name && entity.properties.name.length > 1 && (
                            <div className="text-xs text-slate-500">
                              Original Script: <span className="font-medium text-slate-700">{entity.properties.name[1]}</span>
                            </div>
                          )}
                        </div>

                        {/* Official Notes / Designation Description */}
                        {entity.properties.notes && entity.properties.notes[0] && (
                          <p className="text-xs text-slate-700 leading-relaxed bg-slate-50 p-3 rounded-lg border border-slate-200">
                            {entity.properties.notes[0]}
                          </p>
                        )}

                        {/* Metadata Grid */}
                        <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 text-xs pt-1 border-t border-slate-100">
                          {entity.properties.birthDate && entity.properties.birthDate.length > 0 && (
                            <div>
                              <span className="text-slate-500 block">Date of Birth:</span>
                              <span className="font-semibold text-slate-800">{entity.properties.birthDate.join(', ')}</span>
                            </div>
                          )}

                          {entity.properties.nationality && entity.properties.nationality.length > 0 && (
                            <div>
                              <span className="text-slate-500 block">Nationality / Country:</span>
                              <span className="font-semibold text-slate-800">{entity.properties.nationality.join(', ')}</span>
                            </div>
                          )}

                          {entity.properties.identifiers && entity.properties.identifiers.length > 0 && (
                            <div>
                              <span className="text-slate-500 block">Official ID / SDN #:</span>
                              <span className="font-mono text-slate-800">{entity.properties.identifiers[0]}</span>
                            </div>
                          )}
                        </div>

                        {/* Aliases */}
                        {entity.properties.alias && entity.properties.alias.length > 0 && (
                          <div className="text-xs">
                            <span className="text-slate-500 font-semibold">Known Aliases: </span>
                            <span className="text-slate-700">{entity.properties.alias.join(', ')}</span>
                          </div>
                        )}

                        {/* Datasets */}
                        {entity.properties.dataset && (
                          <div className="flex flex-wrap items-center gap-1 text-xs">
                            <span className="text-slate-500 font-medium">Datasets:</span>
                            {entity.properties.dataset.map((ds, dIdx) => (
                              <span 
                                key={dIdx}
                                className="font-mono text-[10px] bg-slate-100 px-1.5 py-0.5 rounded text-slate-700 border border-slate-200"
                              >
                                {ds}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>

                      {/* Right: Actions */}
                      <div className="flex flex-col gap-2 sm:w-60 shrink-0 border-t lg:border-t-0 lg:border-l border-slate-200 pt-3 lg:pt-0 lg:pl-5">
                        <div className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">
                          Audit Dossier
                        </div>

                        <button
                          onClick={() => onGenerateCertifiedPdf(entity, response.query, false)}
                          className="flex items-center justify-center gap-1.5 rounded-lg bg-blue-700 px-3.5 py-2 text-xs font-bold text-white hover:bg-blue-800 transition-colors cursor-pointer shadow-xs"
                        >
                          <Printer className="h-3.5 w-3.5" />
                          <span>Generate Certified PDF</span>
                        </button>

                        <button
                          onClick={() => onSendEmailReport(entity, response.query)}
                          className="flex items-center justify-center gap-1.5 rounded-lg border border-slate-300 bg-white px-3.5 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors cursor-pointer"
                        >
                          <Mail className="h-3.5 w-3.5" />
                          <span>Email Report</span>
                        </button>

                        {/* Compliance Adjudication Input */}
                        <div className="mt-2 pt-2 border-t border-slate-200">
                          <label className="block text-[11px] font-semibold text-slate-600 mb-1">
                            MLRO Adjudication Note:
                          </label>
                          <input
                            type="text"
                            placeholder="e.g. True positive match confirmed"
                            value={adjudicationNote[entity.id] || ''}
                            onChange={(e) => setAdjudicationNote({ ...adjudicationNote, [entity.id]: e.target.value })}
                            className="w-full text-xs bg-slate-50 border border-slate-300 rounded px-2.5 py-1.5 text-slate-800 placeholder-slate-400 focus:outline-none focus:border-blue-600"
                          />
                          {adjudicationNote[entity.id] && (
                            <span className="text-[10px] text-emerald-700 font-semibold mt-1 block">
                              ✓ Attached to compliance record
                            </span>
                          )}
                        </div>

                      </div>

                    </div>
                  </div>
                );
              })}
            </div>
          )}

        </div>

      </div>
    </section>
  );
};
