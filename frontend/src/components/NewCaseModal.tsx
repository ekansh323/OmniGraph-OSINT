import React, { useState } from 'react';
import { api } from '../api';
import type { CaseItem } from '../api';
import { FolderPlus, X } from 'lucide-react';

interface NewCaseModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCaseCreated: (newCase: CaseItem) => void;
}

export const NewCaseModal: React.FC<NewCaseModalProps> = ({ isOpen, onClose, onCaseCreated }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) {
      setError('Title is required');
      return;
    }
    setError(null);
    setIsSubmitting(true);
    try {
      const created = await api.createCase(title.trim(), description.trim());
      onCaseCreated(created);
      onClose();
    } catch (err: any) {
      setError('Failed to create case: ' + (err.response?.data?.detail || err.message));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <FolderPlus size={18} className="text-orange" />
            <h3 style={{ fontSize: '16px', fontWeight: 500, color: 'var(--color-bone)' }}>
              Open New Investigation Case
            </h3>
          </div>
          <button onClick={onClose} className="btn btn-ghost btn-sm" style={{ padding: '2px 6px' }}>
            <X size={14} />
          </button>
        </div>

        {error && (
          <div style={{ padding: '8px 12px', background: 'rgba(238, 96, 24, 0.1)', border: '1px solid var(--color-signal-orange)', color: 'var(--color-signal-orange)', borderRadius: 'var(--radius-sm)', marginBottom: '14px', fontSize: '12px' }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Investigation Code / Title</label>
            <input 
              type="text"
              value={title}
              onChange={e => setTitle(e.target.value)}
              placeholder="e.g. Operation Cobalt Hawk (Trade Sanctions)"
              className="form-input"
              autoFocus
            />
          </div>

          <div className="form-group">
            <label className="form-label">Case Narrative & Scope</label>
            <textarea
              value={description}
              onChange={e => setDescription(e.target.value)}
              placeholder="Detail targets of interest, suspected laundering vectors, and jurisdictional boundaries..."
              className="form-textarea"
              rows={4}
            />
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '20px' }}>
            <button type="button" onClick={onClose} className="btn btn-ghost">
              Cancel
            </button>
            <button type="submit" disabled={isSubmitting} className="btn btn-primary">
              {isSubmitting ? 'Initializing Case...' : 'Create Investigation'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
