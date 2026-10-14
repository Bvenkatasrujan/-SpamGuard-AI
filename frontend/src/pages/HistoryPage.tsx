import React, { useState } from 'react';
import { History, Search, Download, Trash2, ShieldAlert, CheckCircle, HelpCircle } from 'lucide-react';
import type { HistoryItem } from '../types';

interface HistoryPageProps {
  history: HistoryItem[];
  onClearHistory: () => void;
}

export const HistoryPage: React.FC<HistoryPageProps> = ({ history, onClearHistory }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterLabel, setFilterLabel] = useState<string>('all');

  const filteredHistory = history.filter((item) => {
    const matchesSearch = item.message.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter =
      filterLabel === 'all'
        ? true
        : filterLabel === 'spam'
        ? item.label === 'spam'
        : filterLabel === 'ham'
        ? item.label === 'ham'
        : filterLabel === 'high_risk'
        ? item.risk_level === 'high'
        : true;
    return matchesSearch && matchesFilter;
  });

  const exportCSV = () => {
    if (history.length === 0) return;
    const headers = ['Timestamp', 'Label', 'Confidence', 'Risk Level', 'Message', 'Indicators'];
    const rows = history.map((h) => [
      `"${h.timestamp}"`,
      `"${h.label}"`,
      (h.confidence * 100).toFixed(1) + '%',
      `"${h.risk_level}"`,
      `"${h.message.replace(/"/g, '""')}"`,
      `"${h.indicators.join('; ')}"`
    ]);
    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(e => e.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `spamguard_history_${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">Audit Log & History</h1>
          <p className="text-slate-400 text-sm mt-1">
            Locally stored log of messages scanned during your current browser session.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={exportCSV}
            disabled={history.length === 0}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-xl border border-slate-700 transition-all flex items-center space-x-2 disabled:opacity-40"
          >
            <Download className="w-4 h-4" />
            <span>Export CSV</span>
          </button>

          <button
            onClick={onClearHistory}
            disabled={history.length === 0}
            className="px-4 py-2 bg-red-950/40 hover:bg-red-900/60 text-red-400 text-xs font-semibold rounded-xl border border-red-800/40 transition-all flex items-center space-x-2 disabled:opacity-40"
          >
            <Trash2 className="w-4 h-4" />
            <span>Clear History</span>
          </button>
        </div>
      </div>

      {/* Search & Filter Controls */}
      <div className="glass-panel p-4 rounded-2xl border border-slate-800 flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="w-4 h-4 absolute left-3.5 top-3 text-slate-500" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search scanned message text..."
            className="w-full bg-slate-900/90 border border-slate-700/80 rounded-xl pl-10 pr-4 py-2 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
          />
        </div>

        <select
          value={filterLabel}
          onChange={(e) => setFilterLabel(e.target.value)}
          className="bg-slate-900/90 border border-slate-700/80 rounded-xl px-4 py-2 text-sm text-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
        >
          <option value="all">All Predictions</option>
          <option value="spam">Spam Only</option>
          <option value="ham">Legitimate Only</option>
          <option value="high_risk">High Risk Only</option>
        </select>
      </div>

      {/* History Table */}
      <div className="glass-panel rounded-2xl border border-slate-800 overflow-hidden">
        {filteredHistory.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-900/80 text-slate-400 text-xs uppercase tracking-wider border-b border-slate-800">
                  <th className="py-3.5 px-4 font-semibold">Time</th>
                  <th className="py-3.5 px-4 font-semibold">Classification</th>
                  <th className="py-3.5 px-4 font-semibold">Confidence</th>
                  <th className="py-3.5 px-4 font-semibold">Risk</th>
                  <th className="py-3.5 px-4 font-semibold">Message Excerpt</th>
                  <th className="py-3.5 px-4 font-semibold">Indicators</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-xs">
                {filteredHistory.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-800/30 transition-colors">
                    <td className="py-3.5 px-4 font-mono text-slate-400 whitespace-nowrap">{item.timestamp}</td>
                    
                    <td className="py-3.5 px-4 font-bold uppercase whitespace-nowrap">
                      {item.label === 'spam' ? (
                        <span className="inline-flex items-center space-x-1 text-red-400">
                          <ShieldAlert className="w-3.5 h-3.5" />
                          <span>Spam</span>
                        </span>
                      ) : item.label === 'ham' ? (
                        <span className="inline-flex items-center space-x-1 text-emerald-400">
                          <CheckCircle className="w-3.5 h-3.5" />
                          <span>Ham</span>
                        </span>
                      ) : (
                        <span className="inline-flex items-center space-x-1 text-amber-400">
                          <HelpCircle className="w-3.5 h-3.5" />
                          <span>Uncertain</span>
                        </span>
                      )}
                    </td>

                    <td className="py-3.5 px-4 font-mono text-indigo-300">{(item.confidence * 100).toFixed(1)}%</td>

                    <td className="py-3.5 px-4 whitespace-nowrap">
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase border ${
                        item.risk_level === 'high'
                          ? 'bg-red-500/20 text-red-300 border-red-500/40'
                          : item.risk_level === 'medium'
                          ? 'bg-amber-500/20 text-amber-300 border-amber-500/40'
                          : 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40'
                      }`}>
                        {item.risk_level}
                      </span>
                    </td>

                    <td className="py-3.5 px-4 text-slate-300 max-w-xs truncate" title={item.message}>
                      {item.message}
                    </td>

                    <td className="py-3.5 px-4 text-slate-400">
                      {item.indicators.length > 0 ? (
                        <span className="text-amber-400/90">{item.indicators.length} signals detected</span>
                      ) : (
                        <span className="text-slate-600">None</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="p-12 text-center text-slate-500 space-y-2">
            <History className="w-8 h-8 mx-auto text-slate-600" />
            <p className="text-sm font-medium">No scan history matches your query.</p>
          </div>
        )}
      </div>

    </div>
  );
};
