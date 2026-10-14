import { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { AnalyzePage } from './pages/AnalyzePage';
import { DashboardPage } from './pages/DashboardPage';
import { HistoryPage } from './pages/HistoryPage';
import { ModelPage } from './pages/ModelPage';
import { ModelComparisonPage } from './pages/ModelComparisonPage';
import { ApiPage } from './pages/ApiPage';
import { AboutPage } from './pages/AboutPage';
import type { HistoryItem } from './types';

export function App() {
  const [activeTab, setActiveTab] = useState<string>('analyze');
  const [apiConnected, setApiConnected] = useState<boolean>(false);
  const [history, setHistory] = useState<HistoryItem[]>(() => {
    try {
      const saved = localStorage.getItem('spamguard_history');
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  useEffect(() => {
    localStorage.setItem('spamguard_history', JSON.stringify(history));
  }, [history]);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch('/api/v1/health');
        if (res.ok) {
          const data = await res.json();
          setApiConnected(data.model_loaded);
        } else {
          setApiConnected(false);
        }
      } catch {
        setApiConnected(false);
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, 10000);
    return () => clearInterval(interval);
  }, []);

  const handleAddHistory = (newItem: HistoryItem) => {
    setHistory((prev) => [newItem, ...prev]);
  };

  const handleClearHistory = () => {
    setHistory([]);
    localStorage.removeItem('spamguard_history');
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Header activeTab={activeTab} setActiveTab={setActiveTab} apiConnected={apiConnected} />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'analyze' && <AnalyzePage onAddHistory={handleAddHistory} />}
        {activeTab === 'dashboard' && <DashboardPage history={history} />}
        {activeTab === 'history' && <HistoryPage history={history} onClearHistory={handleClearHistory} />}
        {activeTab === 'model' && <ModelPage />}
        {activeTab === 'comparison' && <ModelComparisonPage />}
        {activeTab === 'api' && <ApiPage />}
        {activeTab === 'about' && <AboutPage />}
      </main>

      <footer className="border-t border-slate-900 py-6 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4">
          SpamGuard AI — Hybrid NLP Spam Detection & Message Security Engine | Powered by scikit-learn & FastAPI
        </div>
      </footer>
    </div>
  );
}

export default App;
