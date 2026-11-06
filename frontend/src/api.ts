import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface CaseItem {
  id: string;
  title: string;
  description: string;
  created_at: string;
  updated_at: string;
  is_closed: boolean;
  evidence_count?: number;
  entity_count?: number;
  alert_count?: number;
}

export interface GraphNode {
  data: {
    id: string;
    label: string;
    type: string;
    confidence: number;
    color?: string;
  };
}

export interface GraphEdge {
  data: {
    id: string;
    source: string;
    target: string;
    label: string;
    type: string;
    confidence: number;
    kind: 'relationship' | 'transaction';
    amount?: number;
    currency?: string;
    timestamp?: string;
  };
}

export interface CaseGraph {
  nodes: GraphNode[];
  edges: GraphEdge[];
  stats: {
    node_count: number;
    edge_count: number;
    entity_types: string[];
  };
}

export interface TransactionItem {
  id: string;
  case_id: string;
  sender_entity_id: string;
  sender_name: string;
  receiver_entity_id: string;
  receiver_name: string;
  amount: number;
  currency: string;
  timestamp: string;
  evidence_id?: string;
  is_suspicious: boolean;
  flag_reason?: string;
}

export interface AlertItem {
  id: string;
  case_id: string;
  type: string;
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  description: string;
  related_entity_ids: string[];
  related_transaction_ids?: string[];
  created_at: string;
  acknowledged: boolean;
  acknowledgement_note?: string;
}

export interface EvidenceItem {
  id: string;
  case_id: string;
  filename: string;
  file_path: string;
  sha256: string;
  mime_type: string;
  size_bytes: number;
  uploaded_at: string;
  processing_status: string;
  processing_error?: string;
}

// API Methods
export const api = {
  // Cases
  async getCases(): Promise<CaseItem[]> {
    const res = await apiClient.get<CaseItem[]>('/api/cases/');
    return res.data;
  },

  async getCase(id: string): Promise<CaseItem> {
    const res = await apiClient.get<CaseItem>(`/api/cases/${id}`);
    return res.data;
  },

  async createCase(title: string, description: string): Promise<CaseItem> {
    const res = await apiClient.post<CaseItem>('/api/cases/', { title, description });
    return res.data;
  },

  // Graph
  async getCaseGraph(caseId: string, entityTypes?: string[], minConfidence: number = 0): Promise<CaseGraph> {
    const params: Record<string, any> = {};
    if (entityTypes && entityTypes.length > 0) {
      params.entity_types = entityTypes.join(',');
    }
    if (minConfidence > 0) {
      params.min_confidence = minConfidence;
    }
    const res = await apiClient.get<CaseGraph>(`/api/graph/cases/${caseId}`, { params });
    return res.data;
  },

  async findPath(caseId: string, sourceId: string, targetId: string, maxDepth: number = 5): Promise<{ paths: any[]; count: number }> {
    const res = await apiClient.post(`/api/graph/cases/${caseId}/path`, {
      source_id: sourceId,
      target_id: targetId,
      max_depth: maxDepth,
    });
    return res.data;
  },

  async getAnomalies(caseId: string): Promise<any[]> {
    const res = await apiClient.get(`/api/graph/cases/${caseId}/anomalies`);
    return res.data.anomalies || [];
  },

  // Transactions
  async getTransactions(caseId: string): Promise<TransactionItem[]> {
    const res = await apiClient.get<TransactionItem[]>(`/api/transactions/cases/${caseId}`);
    return res.data;
  },

  // Alerts
  async getAlerts(caseId: string): Promise<AlertItem[]> {
    const res = await apiClient.get<AlertItem[]>(`/api/alerts/cases/${caseId}`);
    return res.data;
  },

  async acknowledgeAlert(alertId: string, note: string): Promise<AlertItem> {
    const res = await apiClient.post<AlertItem>(`/api/alerts/${alertId}/acknowledge`, { note });
    return res.data;
  },

  // Evidence
  async getEvidence(caseId: string): Promise<EvidenceItem[]> {
    const res = await apiClient.get<EvidenceItem[]>(`/api/evidence/cases/${caseId}`);
    return res.data;
  },

  async uploadEvidence(caseId: string, file: File): Promise<EvidenceItem> {
    const formData = new FormData();
    formData.append('file', file);
    const res = await apiClient.post<EvidenceItem>(`/api/evidence/cases/${caseId}/upload`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return res.data;
  },

  async processEvidence(evidenceId: string): Promise<any> {
    const res = await apiClient.post(`/api/evidence/${evidenceId}/process`);
    return res.data;
  },

  // Demo Reseeding
  async resetDemo(): Promise<{ status: string; case_id: string }> {
    const res = await apiClient.post('/api/demo/reset');
    return res.data;
  },
};
