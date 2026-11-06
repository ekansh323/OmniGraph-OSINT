import { useEffect, useState, useCallback } from 'react';
import { 
  RotateCcw, 
  Plus, 
  Network, 
  DollarSign, 
  FileText, 
  ShieldAlert, 
  BookOpen, 
  Users
} from 'lucide-react';
import { api } from './api';
import type { CaseItem, CaseGraph, TransactionItem, AlertItem, EvidenceItem } from './api';
import { GraphView } from './components/GraphView';
import { TransactionsView } from './components/TransactionsView';
import { EvidenceView } from './components/EvidenceView';
import { AlertsView } from './components/AlertsView';
import { DossierView } from './components/DossierView';
import { NewCaseModal } from './components/NewCaseModal';

export function App() {
  const [cases, setCases] = useState<CaseItem[]>([]);
  const [activeCaseId, setActiveCaseId] = useState<string>('');
  const [activeTab, setActiveTab] = useState<'graph' | 'transactions' | 'evidence' | 'alerts' | 'dossier'>('graph');

  // Case details and data
  const [graphData, setGraphData] = useState<CaseGraph | null>(null);
  const [transactions, setTransactions] = useState<TransactionItem[]>([]);
  const [alerts, setAlerts] = useState<AlertItem[]>([]);
  const [evidenceList, setEvidenceList] = useState<EvidenceItem[]>([]);

  // UI state
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isResetting, setIsResetting] = useState<boolean>(false);
  const [isNewCaseOpen, setIsNewCaseOpen] = useState<boolean>(false);

  // Load cases list
  const loadCases = async (preferredId?: string) => {
    try {
      const data = await api.getCases();
      setCases(data);
      if (data.length > 0) {
        let targetId = preferredId;
        if (!targetId) {
          const shadow = data.find(c => c.title.toLowerCase().includes('shadow ledger'));
          targetId = shadow ? shadow.id : data[0].id;
        }
        setActiveCaseId(targetId);
      }
    } catch (err) {
      console.error('Failed to load cases:', err);
    }
  };

  // Load all case data
  const loadCaseData = useCallback(async (caseId: string) => {
    if (!caseId) return;
    setIsLoading(true);
    try {
      const [g, t, a, e] = await Promise.all([
        api.getCaseGraph(caseId),
        api.getTransactions(caseId),
        api.getAlerts(caseId),
        api.getEvidence(caseId),
      ]);
      setGraphData(g);
      setTransactions(t);
      setAlerts(a);
      setEvidenceList(e);
    } catch (err) {
      console.error('Failed to load case data:', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadCases();
  }, []);

  useEffect(() => {
    if (activeCaseId) {
      loadCaseData(activeCaseId);
    }
  }, [activeCaseId, loadCaseData]);

  // Demo Reseeding
  const handleResetDemo = async () => {
    if (!window.confirm('Reset demo data to default Shadow Ledger investigation?')) return;
    setIsResetting(true);
    try {
      const res = await api.resetDemo();
      await loadCases(res.case_id);
    } catch (err) {
      alert('Failed to reset demo: ' + err);
    } finally {
      setIsResetting(false);
    }
  };

  const activeCase = cases.find(c => c.id === activeCaseId) || null;
  const totalVolume = transactions.reduce((acc, t) => acc + t.amount, 0);
  const criticalAlertsCount = alerts.filter(a => a.severity === 'CRITICAL' && !a.acknowledged).length;

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Top Navbar */}
      <header className="top-navbar">
        <div className="nav-brand">
          <div className="status-pulse active" />
          <div className="nav-wordmark">
            FACTORY <span className="subtext">// OMNIGRAPH OSINT</span>
          </div>
          <span className="font-mono-tag" style={{ border: '1px solid var(--color-ash-stroke)', padding: '2px 8px', borderRadius: '3px' }}>
            WAR ROOM v0.1.0
          </span>
        </div>

        <div className="nav-controls">
          {/* Case Switcher */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span className="font-mono-tag">CASE:</span>
            <select
              value={activeCaseId}
              onChange={e => setActiveCaseId(e.target.value)}
              className="case-selector"
            >
              {cases.map(c => (
                <option key={c.id} value={c.id}>
                  {c.title}
                </option>
              ))}
            </select>
          </div>

          <button
            onClick={() => setIsNewCaseOpen(true)}
            className="btn btn-ghost btn-sm"
          >
            <Plus size={13} />
            New Case
          </button>

          <button
            onClick={handleResetDemo}
            disabled={isResetting}
            className="btn btn-primary btn-sm"
            title="Reset to default multi-hop forensic scenario"
          >
            <RotateCcw size={13} />
            {isResetting ? 'Reseeding...' : 'Reset Demo Scenario'}
          </button>
        </div>
      </header>

      {/* Main Workspace Frame */}
      <main className="dashboard-window">
        <div className="window-chrome">
          {/* macOS Terminal Chrome Header */}
          <div className="window-header">
            <div className="traffic-dots">
              <span className="traffic-dot red" />
              <span className="traffic-dot yellow" />
              <span className="traffic-dot green" />
            </div>

            <div className="window-title">
              CONTROL SURFACE // {activeCase ? activeCase.title.toUpperCase() : 'NO ACTIVE CASE'}
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span className="status-pulse green" style={{ width: '5px', height: '5px' }} />
              <span className="font-mono-tag" style={{ color: 'var(--color-metric-green)' }}>
                FEED ACTIVE
              </span>
            </div>
          </div>

          {/* Metric Tiles Strip */}
          <div className="metrics-grid">
            {/* Tile 1 */}
            <div className="metric-tile">
              <div className="metric-label">
                <span>Targets & Nodes</span>
                <Users size={13} style={{ color: 'var(--color-pale-stone)' }} />
              </div>
              <div className="metric-value">
                {graphData?.stats.node_count || 0}
              </div>
              <div className="metric-sub">
                <span className="text-muted">Extracted entities across files</span>
              </div>
            </div>

            {/* Tile 2 */}
            <div className="metric-tile">
              <div className="metric-label">
                <span>Traced Capital Volume</span>
                <DollarSign size={13} style={{ color: 'var(--color-metric-green)' }} />
              </div>
              <div className="metric-value" style={{ color: 'var(--color-bone)' }}>
                ${totalVolume >= 1000000 ? `${(totalVolume / 1000000).toFixed(2)}M` : totalVolume.toLocaleString()}
              </div>
              <div className="metric-sub">
                <span className="text-green">Direct wire & crypto transfers</span>
              </div>
            </div>

            {/* Tile 3 */}
            <div className="metric-tile">
              <div className="metric-label">
                <span>Graph Provenance Hops</span>
                <Network size={13} style={{ color: 'var(--color-pale-stone)' }} />
              </div>
              <div className="metric-value">
                {graphData?.stats.edge_count || 0}
              </div>
              <div className="metric-sub">
                <span className="text-muted">Directed relationships & flows</span>
              </div>
            </div>

            {/* Tile 4 */}
            <div className="metric-tile">
              <div className="metric-label">
                <span>Forensic Threat Alerts</span>
                <ShieldAlert size={13} style={{ color: 'var(--color-signal-orange)' }} />
              </div>
              <div className="metric-value" style={{ color: criticalAlertsCount > 0 ? 'var(--color-signal-orange)' : 'var(--color-bone)' }}>
                {alerts.length}
              </div>
              <div className="metric-sub">
                <span className={criticalAlertsCount > 0 ? 'text-orange' : 'text-muted'}>
                  {criticalAlertsCount} unresolved critical signals
                </span>
              </div>
            </div>
          </div>

          {/* Tabs Bar */}
          <div className="tabs-bar">
            <button
              onClick={() => setActiveTab('graph')}
              className={`tab-btn ${activeTab === 'graph' ? 'active' : ''}`}
            >
              <Network size={14} />
              <span>Knowledge Graph</span>
              <span className="badge">{graphData?.stats.node_count || 0}</span>
            </button>

            <button
              onClick={() => setActiveTab('transactions')}
              className={`tab-btn ${activeTab === 'transactions' ? 'active' : ''}`}
            >
              <DollarSign size={14} />
              <span>Transactions & Flows</span>
              <span className="badge">{transactions.length}</span>
            </button>

            <button
              onClick={() => setActiveTab('evidence')}
              className={`tab-btn ${activeTab === 'evidence' ? 'active' : ''}`}
            >
              <FileText size={14} />
              <span>Evidence Vault</span>
              <span className="badge">{evidenceList.length}</span>
            </button>

            <button
              onClick={() => setActiveTab('alerts')}
              className={`tab-btn ${activeTab === 'alerts' ? 'active' : ''}`}
            >
              <ShieldAlert size={14} />
              <span>Threat Alerts</span>
              {criticalAlertsCount > 0 && (
                <span className="badge" style={{ background: 'var(--color-signal-orange)', color: '#101010', fontWeight: 600 }}>
                  {criticalAlertsCount}
                </span>
              )}
            </button>

            <button
              onClick={() => setActiveTab('dossier')}
              className={`tab-btn ${activeTab === 'dossier' ? 'active' : ''}`}
            >
              <BookOpen size={14} />
              <span>Case Dossier</span>
            </button>
          </div>

          {/* Tab Views */}
          <div style={{ background: 'var(--color-obsidian-canvas)', minHeight: '600px' }}>
            {isLoading ? (
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '400px', gap: '12px' }}>
                <span className="status-pulse active" />
                <span className="font-mono-tag">LOADING WAR ROOM DATA...</span>
              </div>
            ) : (
              <>
                {activeTab === 'graph' && (
                  <GraphView 
                    graphData={graphData} 
                    caseId={activeCaseId} 
                    onRefresh={() => loadCaseData(activeCaseId)} 
                  />
                )}
                {activeTab === 'transactions' && (
                  <TransactionsView 
                    transactions={transactions} 
                    onRefresh={() => loadCaseData(activeCaseId)} 
                  />
                )}
                {activeTab === 'evidence' && (
                  <EvidenceView 
                    evidenceList={evidenceList} 
                    caseId={activeCaseId} 
                    onRefresh={() => loadCaseData(activeCaseId)} 
                  />
                )}
                {activeTab === 'alerts' && (
                  <AlertsView 
                    alerts={alerts} 
                    caseId={activeCaseId} 
                    onRefresh={() => loadCaseData(activeCaseId)} 
                  />
                )}
                {activeTab === 'dossier' && (
                  <DossierView 
                    activeCase={activeCase} 
                    graphData={graphData} 
                    alertCount={alerts.length} 
                    transactionCount={transactions.length} 
                  />
                )}
              </>
            )}
          </div>
        </div>
      </main>

      {/* New Case Modal */}
      <NewCaseModal
        isOpen={isNewCaseOpen}
        onClose={() => setIsNewCaseOpen(false)}
        onCaseCreated={(newCase) => {
          loadCases(newCase.id);
        }}
      />
    </div>
  );
}

export default App;
