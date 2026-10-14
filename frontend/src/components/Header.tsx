import React from 'react';
import { ShieldAlert, Activity, Cpu, BarChart2, History, Code, Info } from 'lucide-react';

interface HeaderProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  apiConnected: boolean;
}

export const Header: React.FC<HeaderProps> = ({ activeTab, setActiveTab, apiConnected }) => {
  const tabs = [
    { id: 'analyze', label: 'Analyze', icon: ShieldAlert },
    { id: 'dashboard', label: 'Dashboard', icon: Activity },
    { id: 'history', label: 'History', icon: History },
    { id: 'model', label: 'Model', icon: Cpu },
    { id: 'comparison', label: 'Benchmarks', icon: BarChart2 },
    { id: 'api', label: 'API & SDK', icon: Code },
    { id: 'about', label: 'About', icon: Info },
  ];

  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo & Title */}
          <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setActiveTab('analyze')}>
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-cyan-400 flex items-center justify-center shadow-lg shadow-indigo-500/30">
              <ShieldAlert className="w-6 h-6 text-white" />
            </div>
            <div>
              <span className="text-xl font-bold bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
                SPAMGUARD<span className="text-indigo-400 ml-1">AI</span>
              </span>
              <span className="block text-[10px] tracking-wider text-slate-400 uppercase font-medium">
                Hybrid NLP Security Engine
              </span>
            </div>
          </div>

          {/* Navigation Tabs */}
          <nav className="hidden md:flex space-x-1">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 px-3.5 py-2 rounded-lg text-sm font-medium transition-all ${
                    isActive
                      ? 'bg-indigo-600/30 text-indigo-300 border border-indigo-500/40 shadow-sm'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </nav>

          {/* Backend API Connection Status Badge */}
          <div className="flex items-center space-x-2 bg-slate-900/80 px-3 py-1.5 rounded-full border border-slate-800">
            <span className={`w-2 h-2 rounded-full ${apiConnected ? 'bg-emerald-400 animate-pulse' : 'bg-amber-500'}`} />
            <span className="text-xs font-mono text-slate-300">
              {apiConnected ? 'FastAPI :8000 Live' : 'Connecting...'}
            </span>
          </div>

        </div>

        {/* Mobile Navigation */}
        <div className="md:hidden flex overflow-x-auto py-2 border-t border-slate-800/60 no-scrollbar space-x-1">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap ${
                  isActive
                    ? 'bg-indigo-600/30 text-indigo-300 border border-indigo-500/40'
                    : 'text-slate-400 hover:bg-slate-800/40'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

      </div>
    </header>
  );
};
