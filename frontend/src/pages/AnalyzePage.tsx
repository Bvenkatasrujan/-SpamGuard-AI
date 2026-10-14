import React, { useState } from 'react';
import { Send, Trash2, AlertTriangle, CheckCircle, HelpCircle, ShieldAlert, Sparkles } from 'lucide-react';
import type { PredictionResult, HistoryItem } from '../types';

interface AnalyzePageProps {
  onAddHistory: (item: HistoryItem) => void;
}

export const AnalyzePage: React.FC<AnalyzePageProps> = ({ onAddHistory }) => {
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const presets = [
    {
      label: 'SMS Spam',
      text: "URGENT! Congratulations! You won £50,000 cash reward. Claim now at http://bit.ly/prize-claim"
    },
    {
      label: 'SMS Legitimate',
      text: "Hey, are we still meeting for lunch at 1 PM today?"
    },
    {
      label: 'Email Phishing',
      text: "Subject: Urgent Security Alert: Your Account Has Been Restricted!\n\nDear Customer,\nWe detected an unauthorized login attempt from an unknown IP address. Please click the link below to verify your identity and restore full access within 24 hours:\nhttps://secure-bank-verify.com/login\n\nIf you do not verify, your account will be permanently suspended."
    },
    {
      label: 'Email Spam',
      text: "Subject: Photoshop, Windows, Office - 90% OFF Discount Sale!\n\nGet the best software deals online! Exclusive offer for valued members. Buy cheap software keys now. Click here to claim your discount: http://cheap-software-deals.biz/buy\n\nUnsubscribe from list."
    },
    {
      label: 'Email Legitimate',
      text: "Subject: Q3 Project Roadmap & Team Sync Notes\n\nHi team,\nFollowing up on our discussion yesterday. Attached is the project schedule for the upcoming sprint. Let me know if you have any questions before our sync meeting on Thursday at 10 AM.\n\nBest regards,\nAlex"
    }
  ];

  const handleAnalyze = async () => {
    if (!inputText.trim()) return;
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/v1/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: inputText }),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Prediction failed');
      }

      const data: PredictionResult = await response.json();
      setResult(data);

      const historyItem: HistoryItem = {
        ...data,
        id: Date.now().toString(),
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        message: inputText
      };
      onAddHistory(historyItem);

    } catch (err: any) {
      setError(err.message || 'Error connecting to SpamGuard engine');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setInputText('');
    setResult(null);
    setError(null);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      
      {/* Hero Banner */}
      <div className="glass-panel p-8 rounded-2xl relative overflow-hidden border border-slate-800">
        <div className="absolute -right-16 -bottom-16 w-64 h-64 bg-indigo-600/10 rounded-full blur-3xl pointer-events-none" />
        <div className="relative z-10 max-w-3xl">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-semibold mb-4">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Multi-Domain SMS & Email Spam Classifier Engine</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Analyze SMS & Email Security
          </h1>
          <p className="mt-2 text-slate-400 text-sm sm:text-base">
            Input any SMS text message or Email content to inspect spam probability,
            risk level, structural indicators, and security explanation tags.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Left Column: Input Panel */}
        <div className="lg:col-span-7 space-y-4">
          <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
            
            <div className="flex items-center justify-between">
              <label className="text-sm font-medium text-slate-300">
                Message Content
              </label>
              <span className="text-xs text-slate-500">
                {inputText.length} / 10000 chars
              </span>
            </div>

            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Paste message text here (e.g. URGENT! You won a prize! Claim now at http://bit.ly/example)..."
              rows={6}
              className="w-full bg-slate-900/90 border border-slate-700/80 rounded-xl p-4 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 text-sm resize-none transition-all"
            />

            {/* Presets */}
            <div>
              <span className="text-xs font-medium text-slate-400 block mb-2">Try Sample Presets:</span>
              <div className="flex flex-wrap gap-2">
                {presets.map((preset, idx) => (
                  <button
                    key={idx}
                    onClick={() => { setInputText(preset.text); setResult(null); }}
                    className="px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-indigo-900/40 hover:border-indigo-500/50 border border-slate-700/60 text-xs text-slate-300 transition-all text-left"
                  >
                    {preset.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Actions */}
            <div className="flex items-center justify-end space-x-3 pt-2">
              <button
                onClick={handleClear}
                disabled={!inputText && !result}
                className="px-4 py-2.5 rounded-xl border border-slate-700/80 hover:bg-slate-800 text-slate-400 hover:text-slate-200 text-sm font-medium transition-all flex items-center space-x-2 disabled:opacity-40"
              >
                <Trash2 className="w-4 h-4" />
                <span>Clear</span>
              </button>

              <button
                onClick={handleAnalyze}
                disabled={!inputText.trim() || loading}
                className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-cyan-600 hover:from-indigo-500 hover:to-cyan-500 text-white text-sm font-semibold shadow-lg shadow-indigo-600/30 transition-all flex items-center space-x-2 disabled:opacity-50"
              >
                {loading ? (
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                ) : (
                  <Send className="w-4 h-4" />
                )}
                <span>{loading ? 'Analyzing...' : 'Scan Message'}</span>
              </button>
            </div>

          </div>

          {error && (
            <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 text-red-400 text-sm flex items-start space-x-3">
              <AlertTriangle className="w-5 h-5 flex-shrink-0 mt-0.5" />
              <div>
                <span className="font-semibold">Analysis Error:</span> {error}
              </div>
            </div>
          )}
        </div>

        {/* Right Column: Prediction Output Card */}
        <div className="lg:col-span-5">
          {result ? (
            <div className={`glass-panel p-6 rounded-2xl border transition-all duration-300 space-y-6 ${
              result.label === 'spam'
                ? 'border-red-500/40 glow-spam bg-red-950/20'
                : result.label === 'ham'
                ? 'border-emerald-500/40 glow-ham bg-emerald-950/20'
                : 'border-amber-500/40 glow-uncertain bg-amber-950/20'
            }`}>
              
              {/* Result Header */}
              <div className="flex items-center justify-between pb-4 border-b border-slate-800/80">
                <div className="flex items-center space-x-3">
                  {result.label === 'spam' ? (
                    <div className="w-12 h-12 rounded-xl bg-red-500/20 text-red-400 flex items-center justify-center border border-red-500/40">
                      <ShieldAlert className="w-7 h-7" />
                    </div>
                  ) : result.label === 'ham' ? (
                    <div className="w-12 h-12 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center border border-emerald-500/40">
                      <CheckCircle className="w-7 h-7" />
                    </div>
                  ) : (
                    <div className="w-12 h-12 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center border border-amber-500/40">
                      <HelpCircle className="w-7 h-7" />
                    </div>
                  )}

                  <div>
                    <span className="text-xs font-semibold tracking-wider text-slate-400 uppercase">CLASSIFICATION</span>
                    <h2 className="text-2xl font-black uppercase tracking-wide text-white">
                      {result.label === 'spam' ? (
                        <span className="text-red-400">SPAM DETECTED</span>
                      ) : result.label === 'ham' ? (
                        <span className="text-emerald-400">LEGITIMATE (HAM)</span>
                      ) : (
                        <span className="text-amber-400">UNCERTAIN</span>
                      )}
                    </h2>
                  </div>
                </div>

                {/* Risk Badge */}
                <div className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider border ${
                  result.risk_level === 'high'
                    ? 'bg-red-500/20 text-red-300 border-red-500/40'
                    : result.risk_level === 'medium'
                    ? 'bg-amber-500/20 text-amber-300 border-amber-500/40'
                    : result.risk_level === 'low'
                    ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40'
                    : 'bg-slate-700/40 text-slate-300 border-slate-600'
                }`}>
                  Risk: {result.risk_level}
                </div>
              </div>

              {/* Confidence Gauge */}
              <div className="space-y-2">
                <div className="flex justify-between text-xs font-semibold">
                  <span className="text-slate-400">MODEL CONFIDENCE</span>
                  <span className="text-indigo-300 font-mono">{(result.confidence * 100).toFixed(1)}%</span>
                </div>
                <div className="w-full bg-slate-900 rounded-full h-3 overflow-hidden p-0.5 border border-slate-800">
                  <div
                    className={`h-full rounded-full transition-all duration-700 ${
                      result.label === 'spam'
                        ? 'bg-gradient-to-r from-orange-500 to-red-500'
                        : result.label === 'ham'
                        ? 'bg-gradient-to-r from-teal-500 to-emerald-400'
                        : 'bg-amber-500'
                    }`}
                    style={{ width: `${Math.max(5, result.confidence * 100)}%` }}
                  />
                </div>
              </div>

              {/* Security Indicators */}
              <div className="space-y-3">
                <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  Security Indicators ({result.indicators.length})
                </h3>
                {result.indicators.length > 0 ? (
                  <div className="space-y-2">
                    {result.indicators.map((ind, i) => (
                      <div key={i} className="flex items-center space-x-2 text-xs bg-slate-900/60 p-2.5 rounded-lg border border-slate-800 text-slate-200">
                        <AlertTriangle className="w-4 h-4 text-amber-400 flex-shrink-0" />
                        <span>{ind}</span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-xs text-slate-500 bg-slate-900/40 p-3 rounded-lg border border-slate-800/60">
                    No suspicious indicators detected.
                  </div>
                )}
              </div>

              {/* Message Structure Breakdown */}
              <div className="pt-4 border-t border-slate-800/80 space-y-3">
                <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  Extracted Feature Metadata
                </h3>
                <div className="grid grid-cols-2 gap-2 text-xs font-mono">
                  <div className="bg-slate-900/80 p-2 rounded-lg border border-slate-800/80">
                    <span className="text-slate-500 block">Length / Words</span>
                    <span className="text-slate-200 font-bold">{result.metadata.message_length} chars / {result.metadata.word_count} words</span>
                  </div>
                  <div className="bg-slate-900/80 p-2 rounded-lg border border-slate-800/80">
                    <span className="text-slate-500 block">Uppercase Ratio</span>
                    <span className="text-slate-200 font-bold">{(result.metadata.uppercase_ratio * 100).toFixed(1)}%</span>
                  </div>
                  <div className="bg-slate-900/80 p-2 rounded-lg border border-slate-800/80">
                    <span className="text-slate-500 block">Digit Ratio</span>
                    <span className="text-slate-200 font-bold">{(result.metadata.digit_ratio * 100).toFixed(1)}%</span>
                  </div>
                  <div className="bg-slate-900/80 p-2 rounded-lg border border-slate-800/80">
                    <span className="text-slate-500 block">URL / Shortener</span>
                    <span className="text-slate-200 font-bold">
                      {result.metadata.has_url ? (result.metadata.has_shortened_url ? 'Yes (Shortener)' : 'Yes (Standard)') : 'None'}
                    </span>
                  </div>
                </div>
              </div>

            </div>
          ) : (
            <div className="glass-panel p-8 rounded-2xl border border-slate-800/80 text-center space-y-4 flex flex-col items-center justify-center min-h-[360px]">
              <div className="w-16 h-16 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-slate-600">
                <ShieldAlert className="w-8 h-8" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-slate-300">Awaiting Message Input</h3>
                <p className="text-xs text-slate-500 max-w-xs mt-1">
                  Click 'Scan Message' or choose one of the sample presets to run live hybrid classification.
                </p>
              </div>
            </div>
          )}
        </div>

      </div>
    </div>
  );
};
