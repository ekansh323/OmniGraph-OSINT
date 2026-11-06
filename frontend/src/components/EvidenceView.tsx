import React, { useState, useRef } from 'react';
import { api } from '../api';
import type { EvidenceItem } from '../api';
import { UploadCloud, FileText, CheckCircle2, Clock, Play, RefreshCw } from 'lucide-react';

interface EvidenceViewProps {
  evidenceList: EvidenceItem[];
  caseId: string;
  onRefresh: () => void;
}

export const EvidenceView: React.FC<EvidenceViewProps> = ({ evidenceList, caseId, onRefresh }) => {
  const [isUploading, setIsUploading] = useState(false);
  const [processingId, setProcessingId] = useState<string | null>(null);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    setUploadError(null);
    try {
      await api.uploadEvidence(caseId, file);
      onRefresh();
    } catch (err: any) {
      setUploadError('Failed to upload evidence: ' + (err.response?.data?.detail || err.message));
    } finally {
      setIsUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handleTriggerProcess = async (id: string) => {
    setProcessingId(id);
    try {
      await api.processEvidence(id);
      onRefresh();
    } catch (err: any) {
      alert('Processing error: ' + (err.response?.data?.detail || err.message));
    } finally {
      setProcessingId(null);
    }
  };

  const formatBytes = (bytes: number) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  };

  return (
    <div style={{ padding: 'var(--spacing-24)' }}>
      {/* Upload Zone */}
      <div 
        style={{
          border: '1px dashed var(--color-ash-stroke)',
          borderRadius: 'var(--radius-cards)',
          padding: '32px',
          textAlign: 'center',
          backgroundColor: '#0d0d0d',
          marginBottom: '28px',
          cursor: 'pointer',
          transition: 'border-color 0.15s ease',
        }}
        onClick={() => fileInputRef.current?.click()}
      >
        <input 
          type="file" 
          ref={fileInputRef} 
          onChange={handleFileUpload} 
          style={{ display: 'none' }} 
        />
        <UploadCloud size={32} style={{ color: 'var(--color-pale-stone)', margin: '0 auto 12px auto' }} />
        <h3 style={{ fontSize: '15px', fontWeight: 500, color: 'var(--color-bone)', marginBottom: '4px' }}>
          {isUploading ? 'Uploading & Computing SHA-256 Hash...' : 'Ingest Forensics & Documents'}
        </h3>
        <p style={{ fontSize: '12px', color: 'var(--color-warm-granite)', maxWidth: '420px', margin: '0 auto' }}>
          Drop forensic PDF statements, phone toll records (CSV), images, or audio transcripts.
          Automatic spaCy NER extraction runs on ingest.
        </p>
      </div>

      {uploadError && (
        <div style={{ padding: '12px 16px', borderRadius: 'var(--radius-sm)', background: 'rgba(238, 96, 24, 0.1)', border: '1px solid var(--color-signal-orange)', color: 'var(--color-signal-orange)', marginBottom: '20px', fontSize: '12px' }}>
          {uploadError}
        </div>
      )}

      {/* Evidence Files List */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
        <div>
          <h2 style={{ fontSize: '18px', fontWeight: 500, color: 'var(--color-bone)' }}>
            Evidence Vault ({evidenceList.length})
          </h2>
          <p style={{ fontSize: '12px', color: 'var(--color-warm-granite)' }}>
            Cryptographically fingerprinted files with provenance chain of custody.
          </p>
        </div>
        <button onClick={onRefresh} className="btn btn-ghost btn-sm" title="Refresh files">
          <RefreshCw size={13} />
        </button>
      </div>

      <div className="table-container" style={{ border: '1px solid var(--color-ash-stroke)', borderRadius: 'var(--radius-cards)', background: '#0e0d0c' }}>
        <table className="factory-table">
          <thead>
            <tr>
              <th>File Artifact</th>
              <th>SHA-256 Integrity Hash</th>
              <th>MIME Format</th>
              <th>Size</th>
              <th>Extraction Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {evidenceList.map(item => (
              <tr key={item.id}>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <FileText size={15} style={{ color: 'var(--color-pale-stone)' }} />
                    <span style={{ fontWeight: 500, color: 'var(--color-bone)' }}>
                      {item.filename}
                    </span>
                  </div>
                </td>
                <td style={{ fontFamily: 'var(--font-geist-mono)', fontSize: '10px', color: 'var(--color-warm-granite)' }}>
                  {item.sha256 ? `${item.sha256.substring(0, 16)}...${item.sha256.substring(item.sha256.length - 8)}` : 'Pending'}
                </td>
                <td>
                  <span className="badge-tag" style={{ border: '1px solid var(--color-ash-stroke)' }}>
                    {item.mime_type || 'Unknown'}
                  </span>
                </td>
                <td style={{ fontFamily: 'var(--font-geist-mono)', fontSize: '11px', color: 'var(--color-warm-granite)' }}>
                  {formatBytes(item.size_bytes || 0)}
                </td>
                <td>
                  {item.processing_status === 'completed' ? (
                    <span className="badge-tag badge-medium" style={{ display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
                      <CheckCircle2 size={11} />
                      PROCESSED & EXTRACTED
                    </span>
                  ) : item.processing_status === 'processing' ? (
                    <span className="badge-tag" style={{ display: 'inline-flex', alignItems: 'center', gap: '4px', borderColor: 'var(--color-signal-orange)', color: 'var(--color-signal-orange)' }}>
                      <Clock size={11} />
                      PROCESSING...
                    </span>
                  ) : (
                    <span className="badge-tag" style={{ border: '1px solid var(--color-ash-stroke)' }}>
                      PENDING
                    </span>
                  )}
                </td>
                <td>
                  <button 
                    onClick={() => handleTriggerProcess(item.id)}
                    disabled={processingId === item.id || item.processing_status === 'completed'}
                    className="btn btn-ghost btn-sm"
                    style={{ fontSize: '10px', padding: '3px 8px' }}
                  >
                    <Play size={10} />
                    {processingId === item.id ? 'Extracting...' : 'Re-Extract'}
                  </button>
                </td>
              </tr>
            ))}
            {evidenceList.length === 0 && (
              <tr>
                <td colSpan={6} style={{ textAlign: 'center', padding: '40px', color: 'var(--color-warm-granite)' }}>
                  No evidence uploaded for this case yet. Upload files above to begin automated extraction.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
