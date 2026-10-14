import React from 'react';
import { Layers, AlertCircle, Sparkles } from 'lucide-react';

export const AboutPage: React.FC = () => {
  return (
    <div className="space-y-8 animate-in fade-in duration-300 max-w-5xl mx-auto">
      
      <div>
        <h1 className="text-3xl font-extrabold text-white tracking-tight">About SpamGuard AI</h1>
        <p className="text-slate-400 text-sm mt-1">
          Hybrid NLP-Based Spam Detection & Message Security Engine
        </p>
      </div>

      {/* Core Principle Card */}
      <div className="glass-panel p-6 rounded-2xl border border-indigo-500/30 bg-gradient-to-r from-indigo-950/20 to-slate-900 space-y-3">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-semibold">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Architectural Philosophy</span>
        </div>
        <h2 className="text-xl font-bold text-white">
          Reusable Engine First, API Second, Web Client Third
        </h2>
        <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
          SpamGuard AI is not merely an SMS spam website. The core product is a reusable Python NLP library (<code className="text-indigo-300">SpamGuard</code>)
          designed to classify generic text messages across SMS, email bodies, chat messages, notification streams, and web contact forms.
          The web application serves as a modern client interface to demonstrate the engine's real-time capabilities.
        </p>
      </div>

      {/* Architecture Flow */}
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
        <h3 className="text-base font-bold text-white flex items-center space-x-2">
          <Layers className="w-5 h-5 text-indigo-400" />
          <span>System Pipeline Flow</span>
        </h3>

        <div className="bg-slate-950 p-6 rounded-xl border border-slate-800 font-mono text-xs text-slate-300 space-y-3">
          <div className="text-center font-bold text-indigo-400">Input Generic Message</div>
          <div className="text-center text-slate-600">↓</div>
          <div className="text-center bg-slate-900 py-2 rounded border border-slate-800">Text Normalization & Tokenization</div>
          <div className="text-center text-slate-600">↓</div>
          <div className="grid grid-cols-3 gap-2 text-center">
            <div className="bg-indigo-950/60 p-2 rounded border border-indigo-800/40">Word TF-IDF (1,2)</div>
            <div className="bg-indigo-950/60 p-2 rounded border border-indigo-800/40">Char TF-IDF (3,5)</div>
            <div className="bg-indigo-950/60 p-2 rounded border border-indigo-800/40">26 Structural Signals</div>
          </div>
          <div className="text-center text-slate-600">↓</div>
          <div className="text-center bg-indigo-900/40 py-2 rounded border border-indigo-700/40 text-indigo-200">Hybrid Feature Combination Matrix</div>
          <div className="text-center text-slate-600">↓</div>
          <div className="text-center bg-emerald-950/40 py-2 rounded border border-emerald-700/40 text-emerald-200">Calibrated Linear SVM Classifier</div>
          <div className="text-center text-slate-600">↓</div>
          <div className="grid grid-cols-2 gap-2 text-center">
            <div className="bg-slate-900 p-2 rounded border border-slate-800">Risk & Uncertainty Engine</div>
            <div className="bg-slate-900 p-2 rounded border border-slate-800">Security Indicators Engine</div>
          </div>
          <div className="text-center text-slate-600">↓</div>
          <div className="text-center font-bold text-emerald-400">Structured Prediction Result</div>
        </div>
      </div>

      {/* Limitations & Defense */}
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
        <h3 className="text-base font-bold text-white flex items-center space-x-2">
          <AlertCircle className="w-5 h-5 text-amber-400" />
          <span>System Limitations & Academic Defense</span>
        </h3>

        <ul className="space-y-2 text-xs text-slate-300 list-disc list-inside">
          <li>Domain features act as structural signals, not absolute proof of malicious intent.</li>
          <li>Classifier probabilities are Platt-scaled calibrations from Linear SVM decision bounds.</li>
          <li>Model confidence below 60% automatically triggers an UNCERTAIN recommendation layer.</li>
          <li>Dataset statistics were generated programmatically from 10,151 clean SMS & Email records (UCI SMS + Enron Email benchmarks).</li>
        </ul>
      </div>

    </div>
  );
};
