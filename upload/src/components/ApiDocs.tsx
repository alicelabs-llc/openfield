import React, { useState } from 'react';
import { Terminal, Copy, Check, Code2, Globe, Cpu } from 'lucide-react';

export const ApiDocs: React.FC = () => {
  const [activeLang, setActiveLang] = useState<'curl' | 'python' | 'node'>('curl');
  const [copied, setCopied] = useState(false);

  const snippets = {
    curl: `curl -X GET "https://api.verisanctions.com/api/screen?q=Vladimir+Putin&schema=Person&threshold=0.8" \\
  -H "Authorization: Bearer vs_live_99f28a7e4b" \\
  -H "Accept: application/json"`,
    python: `import requests

url = "https://api.verisanctions.com/api/screen"
headers = {
    "Authorization": "Bearer vs_live_99f28a7e4b",
    "Accept": "application/json"
}
params = {
    "q": "Vladimir Putin",
    "schema": "Person",
    "threshold": 0.8
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

print(f"Total Matches: {data['totalHits']}")
for match in data["results"]:
    print(f"- {match['caption']} (Risk: {match['properties']['riskLevel']})")`,
    node: `import fetch from 'node-fetch';

const params = new URLSearchParams({
  q: 'Vladimir Putin',
  schema: 'Person',
  threshold: '0.8'
});

const response = await fetch(\`https://api.verisanctions.com/api/screen?\${params}\`, {
  headers: {
    'Authorization': 'Bearer vs_live_99f28a7e4b',
    'Accept': 'application/json'
  }
});

const { totalHits, results } = await response.json();
console.log(\`Found \${totalHits} enforcement hits\`, results);`
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(snippets[activeLang]);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <section id="api-docs" className="py-16 border-b border-slate-200 bg-slate-50">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        
        <div className="max-w-3xl mb-8">
          <div className="text-xs font-bold uppercase tracking-wider text-blue-700 mb-1">
            Developer API & Integration
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            RESTful API for Automated Compliance
          </h2>
          <p className="mt-2 text-sm text-slate-600">
            Plug sanctions, PEP, and OFAC screening directly into your customer onboarding or payment rails in 5 minutes.
          </p>
        </div>

        {/* API Playground Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          
          {/* Left: Code Box */}
          <div className="lg:col-span-7 rounded-xl border border-slate-800 bg-slate-950 overflow-hidden shadow-md">
            {/* Header / Tabs */}
            <div className="flex items-center justify-between border-b border-slate-800 bg-slate-900 px-4 py-2.5">
              <div className="flex items-center gap-2">
                <Terminal className="h-4 w-4 text-blue-400" />
                <span className="text-xs font-mono font-semibold text-slate-200">
                  GET /api/screen
                </span>
              </div>

              <div className="flex items-center gap-1 bg-slate-950 p-0.5 rounded">
                <button
                  onClick={() => setActiveLang('curl')}
                  className={`px-2 py-0.5 text-xs font-medium rounded transition-colors cursor-pointer ${
                    activeLang === 'curl' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white'
                  }`}
                >
                  cURL
                </button>
                <button
                  onClick={() => setActiveLang('python')}
                  className={`px-2 py-0.5 text-xs font-medium rounded transition-colors cursor-pointer ${
                    activeLang === 'python' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white'
                  }`}
                >
                  Python
                </button>
                <button
                  onClick={() => setActiveLang('node')}
                  className={`px-2 py-0.5 text-xs font-medium rounded transition-colors cursor-pointer ${
                    activeLang === 'node' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white'
                  }`}
                >
                  Node.js
                </button>
              </div>

              <button
                onClick={handleCopy}
                className="flex items-center gap-1 text-xs text-slate-400 hover:text-white transition-colors cursor-pointer"
              >
                {copied ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
                <span className="text-[11px]">{copied ? 'Copied' : 'Copy'}</span>
              </button>
            </div>

            {/* Code Body */}
            <div className="p-4 overflow-x-auto bg-slate-950">
              <pre className="text-xs font-mono text-emerald-400 leading-relaxed">
                <code>{snippets[activeLang]}</code>
              </pre>
            </div>

            {/* Response preview */}
            <div className="border-t border-slate-800 bg-slate-900/60 p-3.5 text-xs">
              <div className="text-[11px] font-mono text-slate-400 mb-1.5 font-bold">
                SAMPLE RESPONSE (200 OK)
              </div>
              <pre className="text-[11px] font-mono text-slate-300 bg-slate-950 p-2.5 rounded border border-slate-800 overflow-x-auto max-h-40">
{`{
  "query": "Vladimir Putin",
  "schema": "Person",
  "timestamp": "2026-10-09T14:44:00Z",
  "durationMs": 312,
  "totalHits": 1,
  "dataSource": "OpenSanctions Cloud API (Live)",
  "results": [
    {
      "id": "Q7747",
      "caption": "Vladimir Vladimirovich Putin",
      "score": 0.99,
      "properties": {
        "topics": ["sanction", "role.pep"],
        "dataset": ["us_ofac_sdn", "eu_fsf", "un_sc_sanctions"],
        "riskLevel": "CRITICAL"
      }
    }
  ]
}`}
              </pre>
            </div>
          </div>

          {/* Right: Spec & Parameters */}
          <div className="lg:col-span-5 space-y-4">
            <div className="rounded-xl border border-slate-300 bg-white p-5 shadow-xs">
              <h4 className="text-sm font-bold text-slate-900 mb-3">Endpoint Parameters</h4>
              
              <div className="space-y-3 text-xs">
                <div className="border-b border-slate-100 pb-2">
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-blue-700 font-bold">q</span>
                    <span className="text-[10px] text-rose-700 font-bold uppercase">Required</span>
                    <span className="text-slate-400 font-mono">string</span>
                  </div>
                  <p className="text-slate-600 mt-0.5">Name or company to query against 494 global watchlists.</p>
                </div>

                <div className="border-b border-slate-100 pb-2">
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-blue-700 font-bold">schema</span>
                    <span className="text-[10px] text-slate-500 uppercase">Optional</span>
                    <span className="text-slate-400 font-mono">Person | Company | LegalEntity</span>
                  </div>
                  <p className="text-slate-600 mt-0.5">Filter by entity schema. Defaults to LegalEntity.</p>
                </div>

                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-blue-700 font-bold">threshold</span>
                    <span className="text-[10px] text-slate-500 uppercase">Optional</span>
                    <span className="text-slate-400 font-mono">float (0.5 - 1.0)</span>
                  </div>
                  <p className="text-slate-600 mt-0.5">Minimum fuzzy match score. Default 0.6.</p>
                </div>
              </div>
            </div>

            <div className="rounded-xl border border-slate-200 bg-white p-4 flex items-start gap-3 shadow-xs">
              <Cpu className="h-5 w-5 text-blue-700 shrink-0 mt-0.5" />
              <div className="text-xs text-slate-600">
                <strong className="text-slate-900 block mb-0.5">OpenSanctions Enterprise Schema</strong>
                Directly maps to the FollowTheMoney schema for seamless migration from sanctions.io or Dilisense.
              </div>
            </div>

          </div>

        </div>

      </div>
    </section>
  );
};
