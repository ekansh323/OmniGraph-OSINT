import React, { useState } from 'react';
import { api } from '../api';
import type { AlertItem } from '../api';
import { CheckCircle, MessageSquare, AlertCircle, RefreshCw } from 'lucide-react';

interface AlertsViewProps {
  alerts: AlertItem[];
  caseId: string;
  onRefresh: () => void;
}

export const AlertsView: React.FC<AlertsViewProps> = ({ alerts, onRefresh }) => {
  const [selectedAlert, setSelectedAlert] = useState<AlertItem | null>(null);
  const [ackNote, setAckNote] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleAcknowledge = async () => {
    if (!selectedAlert) return;
    setIsSubmitting(true);
    try {
      await api.acknowledgeAlert(selectedAlert.id, ackNote);
      setSelectedAlert(null);
      setAckNote('');
      onRefresh();
    } catch (err: any) {
      alert('Failed to acknowledge alert: ' + (err.response?.data?.detail || err.message));
    } finally {
      setIsSubmitting(false);
    }
  };

  const criticalCount = alerts.filter(a => a.severity === 'CRITICAL' && !a.acknowledged).length;
  const highCount = alerts.filter(a => a.severity === 'HIGH' && !a.acknowledged).length;

  return (
    <div style={{ padding: 'var(--spacing-24)' }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <h2 style={{ fontSize: '18px', fontWeight: 500, color: 'var(--color-bone)' }}>
            Intelligence & Threat Alerts
          </h2>
          <p style={{ fontSize: '12px', color: 'var(--color-warm-granite)' }}>
            Real-time anomaly signals from recursive graph cycles, structuring patterns, and entity sanctions.
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div className="badge-tag badge-critical" style={{ padding: '6px 12px' }}>
            <span>{criticalCount} UNRESOLVED CRITICAL</span>
          </div>
          <div className="badge-tag badge-high" style={{ padding: '6px 12px' }}>
            <span>{highCount} HIGH SEVERITY</span>
          </div>
          <button onClick={onRefresh} className="btn btn-ghost btn-sm" title="Refresh alerts">
            <RefreshCw size={13} />
          </button>
        </div>
      </div>

      {/* Alerts Grid */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {alerts.map(a => {
          const isCritical = a.severity === 'CRITICAL';
          const isHigh = a.severity === 'HIGH';

          return (
            <div 
              key={a.id} 
              className="card-dark"
              style={{
                borderLeft: `3px solid ${isCritical ? 'var(--color-signal-orange)' : isHigh ? '#ffa366' : 'var(--color-metric-green)'}`,
                background: a.acknowledged ? '#121110' : '#1a1716',
                opacity: a.acknowledged ? 0.75 : 1,
              }}
            >
              <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '16px' }}>
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
                    <span className={`badge-tag ${isCritical ? 'badge-critical' : isHigh ? 'badge-high' : 'badge-medium'}`}>
                      {a.severity}
                    </span>
                    <span className="font-mono-tag">{a.type}</span>
                    <span style={{ fontSize: '11px', color: 'var(--color-warm-granite)' }}>
                      • {new Date(a.created_at).toLocaleString()}
                    </span>
                  </div>

                  <p style={{ fontSize: '14px', color: 'var(--color-bone)', lineHeight: 1.4, marginBottom: '10px' }}>
                    {a.description}
                  </p>

                  {a.acknowledged ? (
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '11px', color: 'var(--color-metric-green)', background: 'rgba(160, 202, 146, 0.08)', padding: '6px 10px', borderRadius: 'var(--radius-sm)', width: 'fit-content' }}>
                      <CheckCircle size={12} />
                      <span>Acknowledged: {a.acknowledgement_note || 'Reviewed by analyst'}</span>
                    </div>
                  ) : (
                    <button 
                      onClick={() => { setSelectedAlert(a); setAckNote(''); }}
                      className="btn btn-ghost btn-sm"
                      style={{ fontSize: '11px', padding: '4px 10px' }}
                    >
                      <MessageSquare size={12} />
                      Acknowledge & Record Note
                    </button>
                  )}
                </div>
              </div>
            </div>
          );
        })}

        {alerts.length === 0 && (
          <div style={{ textAlign: 'center', padding: '48px', color: 'var(--color-warm-granite)' }}>
            <AlertCircle size={24} style={{ margin: '0 auto 8px auto', opacity: 0.5 }} />
            <div>No alerts logged for this investigation.</div>
          </div>
        )}
      </div>

      {/* Acknowledge Modal */}
      {selectedAlert && (
        <div className="modal-overlay" onClick={() => setSelectedAlert(null)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <h3 style={{ fontSize: '16px', fontWeight: 500, color: 'var(--color-bone)', marginBottom: '12px' }}>
              Acknowledge Alert: {selectedAlert.type}
            </h3>
            <p style={{ fontSize: '13px', color: 'var(--color-pale-stone)', marginBottom: '16px' }}>
              {selectedAlert.description}
            </p>

            <div className="form-group">
              <label className="form-label">Investigator Note / Action Taken</label>
              <textarea
                value={ackNote}
                onChange={e => setAckNote(e.target.value)}
                placeholder="e.g. Subpoena requested, account frozen, SAR filed with FinCEN..."
                className="form-textarea"
                rows={3}
              />
            </div>

            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '20px' }}>
              <button onClick={() => setSelectedAlert(null)} className="btn btn-ghost">
                Cancel
              </button>
              <button onClick={handleAcknowledge} disabled={isSubmitting} className="btn btn-primary">
                {isSubmitting ? 'Saving...' : 'Confirm Acknowledgement'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
