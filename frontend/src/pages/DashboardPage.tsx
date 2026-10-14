import React from 'react';
import { Activity, ShieldAlert, CheckCircle, AlertTriangle } from 'lucide-react';
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip, BarChart, Bar, XAxis, YAxis } from 'recharts';
import type { HistoryItem } from '../types';

interface DashboardPageProps {
  history: HistoryItem[];
}

export const DashboardPage: React.FC<DashboardPageProps> = ({ history }) => {
  const totalAnalyzed = history.length;
  const spamCount = history.filter(h => h.label === 'spam').length;
  const hamCount = history.filter(h => h.label === 'ham').length;
  const uncertainCount = history.filter(h => h.label === 'uncertain').length;

  const spamRatio = totalAnalyzed > 0 ? ((spamCount / totalAnalyzed) * 100).toFixed(1) : '0';

  const pieData = [
    { name: 'Spam', value: spamCount || (totalAnalyzed === 0 ? 1 : 0), color: '#ef4444' },
    { name: 'Legitimate (Ham)', value: hamCount || (totalAnalyzed === 0 ? 3 : 0), color: '#10b981' },
    { name: 'Uncertain', value: uncertainCount, color: '#f59e0b' }
  ];

  const highRiskCount = history.filter(h => h.risk_level === 'high').length;
  const mediumRiskCount = history.filter(h => h.risk_level === 'medium').length;
  const lowRiskCount = history.filter(h => h.risk_level === 'low').length;

  const barData = [
    { name: 'High Risk', count: highRiskCount },
    { name: 'Medium Risk', count: mediumRiskCount },
    { name: 'Low Risk', count: lowRiskCount },
    { name: 'Uncertain', count: uncertainCount }
  ];

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      
      <div>
        <h1 className="text-3xl font-extrabold text-white tracking-tight">Security Analytics Dashboard</h1>
        <p className="text-slate-400 text-sm mt-1">
          Session-level message scanning metrics, classification ratios, and risk breakdown.
        </p>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        
        <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex items-center justify-between">
          <div>
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Total Scanned</span>
            <div className="text-3xl font-black text-white mt-1">{totalAnalyzed}</div>
            <span className="text-[11px] text-slate-500 mt-1 block">Local Session Log</span>
          </div>
          <div className="w-12 h-12 rounded-xl bg-indigo-500/20 text-indigo-400 flex items-center justify-center border border-indigo-500/30">
            <Activity className="w-6 h-6" />
          </div>
        </div>

        <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex items-center justify-between">
          <div>
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Spam Detected</span>
            <div className="text-3xl font-black text-red-400 mt-1">{spamCount}</div>
            <span className="text-[11px] text-slate-500 mt-1 block">{spamRatio}% of total scans</span>
          </div>
          <div className="w-12 h-12 rounded-xl bg-red-500/20 text-red-400 flex items-center justify-center border border-red-500/30">
            <ShieldAlert className="w-6 h-6" />
          </div>
        </div>

        <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex items-center justify-between">
          <div>
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Legitimate (Ham)</span>
            <div className="text-3xl font-black text-emerald-400 mt-1">{hamCount}</div>
            <span className="text-[11px] text-slate-500 mt-1 block">Verified clean</span>
          </div>
          <div className="w-12 h-12 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center border border-emerald-500/30">
            <CheckCircle className="w-6 h-6" />
          </div>
        </div>

        <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex items-center justify-between">
          <div>
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">High Risk Count</span>
            <div className="text-3xl font-black text-amber-400 mt-1">{highRiskCount}</div>
            <span className="text-[11px] text-slate-500 mt-1 block">Requires review</span>
          </div>
          <div className="w-12 h-12 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center border border-amber-500/30">
            <AlertTriangle className="w-6 h-6" />
          </div>
        </div>

      </div>

      {/* Visual Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Pie Chart */}
        <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
          <h3 className="text-base font-bold text-white">Classification Ratio</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={90}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '0.75rem', color: '#f8fafc' }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="flex justify-center space-x-6 text-xs">
            <div className="flex items-center space-x-2">
              <span className="w-3 h-3 rounded-full bg-red-500 inline-block" />
              <span className="text-slate-300">Spam ({spamCount})</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="w-3 h-3 rounded-full bg-emerald-500 inline-block" />
              <span className="text-slate-300">Legitimate ({hamCount})</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="w-3 h-3 rounded-full bg-amber-500 inline-block" />
              <span className="text-slate-300">Uncertain ({uncertainCount})</span>
            </div>
          </div>
        </div>

        {/* Risk Level Bar Chart */}
        <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
          <h3 className="text-base font-bold text-white">Risk Level Distribution</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={barData}>
                <XAxis dataKey="name" stroke="#64748b" fontSize={12} />
                <YAxis stroke="#64748b" fontSize={12} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '0.75rem', color: '#f8fafc' }}
                />
                <Bar dataKey="count" fill="#6366f1" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <p className="text-xs text-slate-500 text-center">
            Derived from local session analysis history.
          </p>
        </div>

      </div>

    </div>
  );
};
