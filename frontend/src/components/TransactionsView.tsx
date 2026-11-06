import React, { useState } from 'react';
import type { TransactionItem } from '../api';
import { ArrowUpRight, ShieldAlert, RefreshCw } from 'lucide-react';

interface TransactionsViewProps {
  transactions: TransactionItem[];
  onRefresh: () => void;
}

export const TransactionsView: React.FC<TransactionsViewProps> = ({ transactions, onRefresh }) => {
  const [filterSuspiciousOnly, setFilterSuspiciousOnly] = useState(false);
  const [minAmount, setMinAmount] = useState<number>(0);

  const filtered = transactions.filter(t => {
    if (filterSuspiciousOnly && !t.is_suspicious) return false;
    if (minAmount > 0 && t.amount < minAmount) return false;
    return true;
  });

  const totalVolume = transactions.reduce((acc, t) => acc + t.amount, 0);
  const suspiciousCount = transactions.filter(t => t.is_suspicious).length;

  return (
    <div style={{ padding: 'var(--spacing-24)' }}>
      {/* Top Controls Bar */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px', flexWrap: 'wrap', gap: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div>
            <h2 style={{ fontSize: '18px', fontWeight: 500, color: 'var(--color-bone)' }}>
              Financial Transactions Ledger
            </h2>
            <p style={{ fontSize: '12px', color: 'var(--color-warm-granite)' }}>
              Audited transaction stream across banking nodes and crypto wallets.
            </p>
          </div>

          <div style={{ display: 'flex', gap: '12px', marginLeft: '16px' }}>
            <div className="badge-tag" style={{ border: '1px solid var(--color-ash-stroke)', padding: '6px 12px' }}>
              <span className="text-muted">TOTAL TRACED: </span>
              <strong style={{ color: 'var(--color-bone)' }}>
                ${totalVolume.toLocaleString('en-US', { minimumFractionDigits: 2 })}
              </strong>
            </div>
            <div className="badge-tag badge-critical" style={{ padding: '6px 12px' }}>
              <span>{suspiciousCount} SUSPICIOUS TRANSFERS</span>
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', color: 'var(--color-bone)', cursor: 'pointer' }}>
            <input 
              type="checkbox" 
              checked={filterSuspiciousOnly} 
              onChange={e => setFilterSuspiciousOnly(e.target.checked)}
              style={{ accentColor: 'var(--color-signal-orange)' }}
            />
            <span>Suspicious Only</span>
          </label>

          <select
            value={minAmount}
            onChange={e => setMinAmount(Number(e.target.value))}
            className="form-input"
            style={{ width: '150px', fontSize: '12px', padding: '5px 10px' }}
          >
            <option value="0">All Amounts</option>
            <option value="9000">&gt; $9,000 (Structuring)</option>
            <option value="50000">&gt; $50,000 (High Value)</option>
            <option value="500000">&gt; $500,000 (Major Wire)</option>
          </select>

          <button onClick={onRefresh} className="btn btn-ghost btn-sm" title="Refresh transactions">
            <RefreshCw size={13} />
          </button>
        </div>
      </div>

      {/* Transactions Table */}
      <div className="table-container" style={{ border: '1px solid var(--color-ash-stroke)', borderRadius: 'var(--radius-cards)', background: '#0e0d0c' }}>
        <table className="factory-table">
          <thead>
            <tr>
              <th>Timestamp (UTC)</th>
              <th>Sender Entity</th>
              <th></th>
              <th>Receiver Entity</th>
              <th>Amount</th>
              <th>Currency</th>
              <th>Forensic Risk Assessment</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map(t => (
              <tr key={t.id} style={{ background: t.is_suspicious ? 'rgba(238, 96, 24, 0.03)' : undefined }}>
                <td style={{ fontFamily: 'var(--font-geist-mono)', fontSize: '11px', color: 'var(--color-warm-granite)', whiteSpace: 'nowrap' }}>
                  {new Date(t.timestamp).toLocaleDateString()} {new Date(t.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </td>
                <td style={{ fontWeight: 500, color: 'var(--color-bone)' }}>
                  {t.sender_name}
                </td>
                <td style={{ textAlign: 'center', color: 'var(--color-warm-granite)' }}>
                  <ArrowUpRight size={14} />
                </td>
                <td style={{ fontWeight: 500, color: 'var(--color-bone)' }}>
                  {t.receiver_name}
                </td>
                <td style={{ fontFamily: 'var(--font-geist-mono)', fontSize: '14px', fontWeight: 500, color: t.is_suspicious ? 'var(--color-signal-orange)' : 'var(--color-metric-green)', whiteSpace: 'nowrap' }}>
                  ${t.amount.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                </td>
                <td style={{ fontFamily: 'var(--font-geist-mono)', fontSize: '11px', color: 'var(--color-warm-granite)' }}>
                  {t.currency}
                </td>
                <td>
                  {t.is_suspicious ? (
                    <span className="badge-tag badge-critical" style={{ display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
                      <ShieldAlert size={11} />
                      {t.flag_reason || 'ANOMALY DETECTED'}
                    </span>
                  ) : (
                    <span className="font-mono-tag" style={{ color: 'var(--color-graphite-mid)' }}>
                      CLEARED
                    </span>
                  )}
                </td>
              </tr>
            ))}
            {filtered.length === 0 && (
              <tr>
                <td colSpan={7} style={{ textAlign: 'center', padding: '40px', color: 'var(--color-warm-granite)' }}>
                  No transactions match the selected filters.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
