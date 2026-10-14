import React, { useState } from 'react';
import { Code, Copy, Check, ExternalLink } from 'lucide-react';

export const ApiPage: React.FC = () => {
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  const copyToClipboard = (text: string, idx: number) => {
    navigator.clipboard.writeText(text);
    setCopiedIndex(idx);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  const snippets = [
    {
      title: '1. Reusable Python SDK',
      language: 'python',
      code: `from spamguard import SpamGuard

# Initialize SpamGuard engine
guard = SpamGuard()

# Single text prediction
result = guard.predict(
    "URGENT! Congratulations! You won £50,000 cash. Claim at http://bit.ly/prize"
)

print("Label      :", result["label"])
print("Confidence :", f"{result['confidence'] * 100:.1f}%")
print("Indicators :", result["indicators"])`
    },
    {
      title: '2. FastAPI REST Endpoint (cURL)',
      language: 'bash',
      code: `curl -X POST "http://localhost:8000/api/v1/predict" \\
     -H "Content-Type: application/json" \\
     -d '{
       "text": "URGENT! You won a free prize! Claim now."
     }'`
    },
    {
      title: '3. Python HTTP API Request',
      language: 'python',
      code: `import requests

response = requests.post(
    "http://localhost:8000/api/v1/predict",
    json={
        "text": "Hello, are we still having dinner at 7 PM?"
    }
)

data = response.json()
print("Result:", data["label"], "Confidence:", data["confidence"])`
    },
    {
      title: '4. JavaScript / TypeScript Fetch API',
      language: 'javascript',
      code: `const response = await fetch('http://localhost:8000/api/v1/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: 'Congratulations! You won a prize!'
  })
});

const data = await response.json();
console.log(data.label, data.risk_level, data.indicators);`
    },
    {
      title: '5. Command Line Interface (CLI)',
      language: 'bash',
      code: `# Run classification directly from terminal
python -m spamguard "Congratulations! You won a free prize! Claim now at http://bit.ly/claim"`
    }
  ];

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">API & Integration SDK</h1>
          <p className="text-slate-400 text-sm mt-1">
            Integrate SpamGuard AI engine into Python applications, SMS gateways, email microservices, and backend web apps.
          </p>
        </div>

        <a
          href="http://localhost:8000/docs"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center space-x-2 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-lg shadow-indigo-600/30 transition-all"
        >
          <span>Open Swagger Docs</span>
          <ExternalLink className="w-3.5 h-3.5" />
        </a>
      </div>

      {/* Snippet Cards */}
      <div className="space-y-6">
        {snippets.map((snippet, idx) => (
          <div key={idx} className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-base font-bold text-white flex items-center space-x-2">
                <Code className="w-4 h-4 text-indigo-400" />
                <span>{snippet.title}</span>
              </h3>

              <button
                onClick={() => copyToClipboard(snippet.code, idx)}
                className="px-3 py-1 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 text-xs font-medium rounded-lg transition-all flex items-center space-x-1.5"
              >
                {copiedIndex === idx ? (
                  <>
                    <Check className="w-3.5 h-3.5 text-emerald-400" />
                    <span className="text-emerald-400">Copied!</span>
                  </>
                ) : (
                  <>
                    <Copy className="w-3.5 h-3.5" />
                    <span>Copy</span>
                  </>
                )}
              </button>
            </div>

            <pre className="bg-slate-950 p-4 rounded-xl border border-slate-800 text-xs font-mono text-slate-200 overflow-x-auto">
              <code>{snippet.code}</code>
            </pre>
          </div>
        ))}
      </div>

    </div>
  );
};
