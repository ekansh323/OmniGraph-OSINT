import React from 'react';
import type { CaseItem, CaseGraph } from '../api';
import { FileDown, Layers, AlertOctagon } from 'lucide-react';

interface DossierViewProps {
  activeCase: CaseItem | null;
  graphData: CaseGraph | null;
  alertCount: number;
  transactionCount: number;
}

export const DossierView: React.FC<DossierViewProps> = ({ 
  activeCase, 
  graphData, 
  alertCount, 
  transactionCount 
}) => {
  if (!activeCase) return null;

  const handleExport = () => {
    window.print();
  };

  const entitiesByType: Record<string, number> = {};
  graphData?.nodes.forEach(n => {
    entitiesByType[n.data.type] = (entitiesByType[n.data.type] || 0) + 1;
  });

  return (
    <div style={{ padding: 'var(--spacing-24)', maxWidth: '1000px', margin: '0 auto' }}>
      {/* Signature Factory Move: Light Surface Card floating on Obsidian Ground */}
      <div className="card-light-figure" style={{ marginBottom: '32px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px', flexWrap: 'wrap', gap: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span className="status-pulse active" />
            <span style={{ fontFamily: 'var(--font-geist-mono)', fontSize: '11px', textTransform: 'uppercase', letterSpacing: '1px', color: '#101010', fontWeight: 600 }}>
              EXECUTIVE INTELLIGENCE BRIEFING // LAW ENFORCEMENT MEMORANDUM
            </span>
          </div>

          <button onClick={handleExport} className="btn btn-primary btn-sm" style={{ backgroundColor: '#101010', borderColor: '#101010', color: '#eeeeee' }}>
            <FileDown size={12} />
            Export Formal Dossier
          </button>
        </div>

        <h1 style={{ fontSize: '28px', fontWeight: 500, letterSpacing: '-0.8px', marginBottom: '12px', color: '#101010' }}>
          {activeCase.title}
        </h1>

        <p style={{ fontSize: '15px', color: '#3d3a39', lineHeight: 1.6, marginBottom: '24px' }}>
          {activeCase.description}
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px', borderTop: '1px solid #d4cfcb', paddingTop: '16px' }}>
          <div>
            <span style={{ fontFamily: 'var(--font-geist-mono)', fontSize: '10px', color: '#8a8380', display: 'block', textTransform: 'uppercase' }}>
              PROVENANCE NODES
            </span>
            <strong style={{ fontSize: '20px', color: '#101010', fontFamily: 'var(--font-geist-mono)' }}>
              {graphData?.nodes.length || 0}
            </strong>
          </div>
          <div>
            <span style={{ fontFamily: 'var(--font-geist-mono)', fontSize: '10px', color: '#8a8380', display: 'block', textTransform: 'uppercase' }}>
              DIRECTED HOPS
            </span>
            <strong style={{ fontSize: '20px', color: '#101010', fontFamily: 'var(--font-geist-mono)' }}>
              {graphData?.edges.length || 0}
            </strong>
          </div>
          <div>
            <span style={{ fontFamily: 'var(--font-geist-mono)', fontSize: '10px', color: '#8a8380', display: 'block', textTransform: 'uppercase' }}>
              TRANSACTIONS TRACED
            </span>
            <strong style={{ fontSize: '20px', color: '#101010', fontFamily: 'var(--font-geist-mono)' }}>
              {transactionCount}
            </strong>
          </div>
          <div>
            <span style={{ fontFamily: 'var(--font-geist-mono)', fontSize: '10px', color: '#8a8380', display: 'block', textTransform: 'uppercase' }}>
              THREAT ALERTS
            </span>
            <strong style={{ fontSize: '20px', color: '#ee6018', fontFamily: 'var(--font-geist-mono)' }}>
              {alertCount}
            </strong>
          </div>
        </div>
      </div>

      {/* Target Network Breakdown */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '32px' }}>
        <div className="card-dark">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
            <Layers size={16} className="text-orange" />
            <h3 style={{ fontSize: '15px', fontWeight: 500, color: 'var(--color-bone)' }}>
              Entity Classification Matrix
            </h3>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {Object.entries(entitiesByType).map(([type, count]) => (
              <div 
                key={type} 
                style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  justifyContent: 'space-between',
                  padding: '8px 12px',
                  background: '#101010',
                  border: '1px solid var(--color-ash-stroke)',
                  borderRadius: 'var(--radius-sm)'
                }}
              >
                <span className="font-mono-tag">{type}</span>
                <span style={{ fontFamily: 'var(--font-geist-mono)', color: 'var(--color-bone)', fontSize: '13px' }}>
                  {count} entities
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="card-dark">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
            <AlertOctagon size={16} className="text-orange" />
            <h3 style={{ fontSize: '15px', fontWeight: 500, color: 'var(--color-bone)' }}>
              Operational Vulnerabilities Found
            </h3>
          </div>

          <ul style={{ fontSize: '13px', color: 'var(--color-pale-stone)', display: 'flex', flexDirection: 'column', gap: '10px', paddingLeft: '16px' }}>
            <li>
              <strong>Circular Laundering Path:</strong> Closed 5-hop recursive CTE loop detected between Marcus Chen, TVC, BVI shell, and Singapore nominee.
            </li>
            <li>
              <strong>BSA / CTR Structuring:</strong> Sub-threshold $9,800 - $9,950 transfers spaced over 48 hours to evade Form 8300 reporting.
            </li>
            <li>
              <strong>Unhosted Crypto Bridge:</strong> Layering through unhosted genesis wallet 0x8f... into intermediary privacy mixer node.
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};
