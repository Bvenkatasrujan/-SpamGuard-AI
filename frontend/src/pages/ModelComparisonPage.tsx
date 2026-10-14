import React from 'react';
import { BarChart2, Award } from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Legend } from 'recharts';

export const ModelComparisonPage: React.FC = () => {
  const comparisonData = [
    { config: 'Hybrid NLP + Struct', model: 'Linear SVM', accuracy: 98.91, precision: 98.78, recall: 92.42, f1: 95.48 },
    { config: 'Word + Char TF-IDF', model: 'Linear SVM', accuracy: 98.79, precision: 98.74, recall: 91.44, f1: 94.95 },
    { config: 'Word TF-IDF', model: 'Linear SVM', accuracy: 98.76, precision: 97.37, recall: 92.61, f1: 94.92 },
    { config: 'Char TF-IDF', model: 'Linear SVM', accuracy: 98.67, precision: 98.72, recall: 90.47, f1: 94.41 },
    { config: 'Hybrid NLP + Struct', model: 'Naive Bayes', accuracy: 98.62, precision: 95.49, recall: 93.39, f1: 94.39 },
    { config: 'Word TF-IDF', model: 'Naive Bayes', accuracy: 98.57, precision: 98.12, recall: 90.27, f1: 94.03 },
    { config: 'Hybrid NLP + Struct', model: 'Logistic Reg.', accuracy: 98.52, precision: 98.73, recall: 89.31, f1: 93.76 },
    { config: 'Word + Char TF-IDF', model: 'Naive Bayes', accuracy: 98.45, precision: 94.71, recall: 92.81, f1: 93.72 },
    { config: 'Word + Char TF-IDF', model: 'Logistic Reg.', accuracy: 98.40, precision: 99.13, recall: 87.95, f1: 93.18 },
    { config: 'Word TF-IDF', model: 'Logistic Reg.', accuracy: 98.23, precision: 99.55, recall: 86.19, f1: 92.38 },
    { config: 'Char TF-IDF', model: 'Naive Bayes', accuracy: 98.09, precision: 94.59, recall: 89.89, f1: 92.13 },
    { config: 'Char TF-IDF', model: 'Logistic Reg.', accuracy: 98.09, precision: 99.32, recall: 85.22, f1: 91.73 },
  ];

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      
      <div>
        <h1 className="text-3xl font-extrabold text-white tracking-tight">Model & Feature Benchmarking</h1>
        <p className="text-slate-400 text-sm mt-1">
          Empirical 5-fold Stratified Cross-Validation results comparing 4 feature configurations across 3 machine learning algorithms.
        </p>
      </div>

      {/* Winning Highlight Card */}
      <div className="glass-panel p-6 rounded-2xl border border-indigo-500/40 bg-indigo-950/20 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div className="flex items-center space-x-4">
          <div className="w-12 h-12 rounded-2xl bg-indigo-500/20 text-indigo-400 flex items-center justify-center border border-indigo-500/40">
            <Award className="w-7 h-7" />
          </div>
          <div>
            <span className="text-xs font-semibold text-indigo-400 uppercase tracking-wider">HIGHEST VAL F1 SCORE</span>
            <h3 className="text-xl font-bold text-white">Hybrid NLP + Structural + Calibrated Linear SVM</h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Outperformed single TF-IDF representations by combining lexical, character obfuscation, and security features.
            </p>
          </div>
        </div>

        <div className="text-right">
          <div className="text-3xl font-black text-indigo-300">95.48%</div>
          <span className="text-xs text-slate-400">Validation Spam F1</span>
        </div>
      </div>

      {/* Comparison Chart */}
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
        <h3 className="text-base font-bold text-white flex items-center space-x-2">
          <BarChart2 className="w-5 h-5 text-indigo-400" />
          <span>Cross-Validation Spam F1 Score Comparison (%)</span>
        </h3>

        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={comparisonData.slice(0, 8)}>
              <XAxis dataKey="model" stroke="#64748b" fontSize={11} />
              <YAxis domain={[85, 100]} stroke="#64748b" fontSize={11} />
              <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '0.75rem', color: '#f8fafc' }} />
              <Legend />
              <Bar dataKey="f1" name="Spam F1 Score" fill="#6366f1" radius={[4, 4, 0, 0]} />
              <Bar dataKey="precision" name="Precision" fill="#10b981" radius={[4, 4, 0, 0]} />
              <Bar dataKey="recall" name="Recall" fill="#06b6d4" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Benchmarking Table */}
      <div className="glass-panel rounded-2xl border border-slate-800 overflow-hidden">
        <div className="p-4 border-b border-slate-800 bg-slate-900/60">
          <h3 className="text-sm font-bold text-white">Complete 12-Experiment Benchmark Matrix</h3>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-900/90 text-slate-400 text-xs uppercase tracking-wider border-b border-slate-800">
                <th className="py-3 px-4 font-semibold">Rank</th>
                <th className="py-3 px-4 font-semibold">Feature Configuration</th>
                <th className="py-3 px-4 font-semibold">Model Algorithm</th>
                <th className="py-3 px-4 font-semibold">Spam F1</th>
                <th className="py-3 px-4 font-semibold">Precision</th>
                <th className="py-3 px-4 font-semibold">Recall</th>
                <th className="py-3 px-4 font-semibold">Accuracy</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-xs font-mono">
              {comparisonData.map((row, idx) => (
                <tr key={idx} className={idx === 0 ? 'bg-indigo-950/40 text-white font-bold' : 'hover:bg-slate-800/30 text-slate-300'}>
                  <td className="py-3 px-4">
                    {idx === 0 ? <span className="text-indigo-400 font-black">#1 ★</span> : `#${idx + 1}`}
                  </td>
                  <td className="py-3 px-4 font-sans font-medium">{row.config}</td>
                  <td className="py-3 px-4 font-sans">{row.model}</td>
                  <td className="py-3 px-4 text-indigo-300 font-bold">{row.f1.toFixed(2)}%</td>
                  <td className="py-3 px-4 text-emerald-300">{row.precision.toFixed(2)}%</td>
                  <td className="py-3 px-4 text-cyan-300">{row.recall.toFixed(2)}%</td>
                  <td className="py-3 px-4 text-slate-300">{row.accuracy.toFixed(2)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
};
