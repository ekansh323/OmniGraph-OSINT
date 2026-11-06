import React, { useEffect, useRef, useState, useMemo } from 'react';
import cytoscape from 'cytoscape';
import type { Core } from 'cytoscape';
import { 
  ZoomIn, 
  ZoomOut, 
  Maximize2, 
  RotateCw, 
  Search, 
  Route, 
  X, 
  ArrowRight,
  Building,
  User,
  CreditCard,
  Coins,
  MapPin,
  Phone,
  Mail
} from 'lucide-react';
import { api } from '../api';
import type { CaseGraph } from '../api';

interface GraphViewProps {
  graphData: CaseGraph | null;
  caseId: string;
  onRefresh: () => void;
}

export const GraphView: React.FC<GraphViewProps> = ({ graphData, caseId }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const cyRef = useRef<Core | null>(null);

  // Filter state
  const [selectedTypes, setSelectedTypes] = useState<string[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  
  // Selected element in inspector
  const [selectedNode, setSelectedNode] = useState<any>(null);
  const [selectedEdge, setSelectedEdge] = useState<any>(null);

  // Path finder state
  const [pathSource, setPathSource] = useState<string>('');
  const [pathTarget, setPathTarget] = useState<string>('');
  const [pathResults, setPathResults] = useState<any[] | null>(null);
  const [isFindingPath, setIsFindingPath] = useState(false);
  const [pathError, setPathError] = useState<string | null>(null);

  // Available entity types in this graph
  const availableTypes = useMemo(() => {
    if (!graphData) return [];
    const set = new Set<string>();
    graphData.nodes.forEach(n => set.add(n.data.type));
    return Array.from(set);
  }, [graphData]);

  // Color mapping per DESIGN.md tokens
  const getNodeColor = (type: string) => {
    switch (type.toUpperCase()) {
      case 'PERSON':
        return '#eeeeee'; // Bone
      case 'ORGANIZATION':
        return '#b8b3b0'; // Pale Stone
      case 'BANK_ACCOUNT':
        return '#ee6018'; // Signal Orange
      case 'CRYPTO_WALLET':
        return '#ee6018'; // Signal Orange
      case 'LOCATION':
        return '#8a8380'; // Warm Granite
      case 'PHONE':
      case 'EMAIL':
        return '#a0ca92'; // Metric Green
      default:
        return '#b8b3b0';
    }
  };

  const getNodeShape = (type: string) => {
    switch (type.toUpperCase()) {
      case 'PERSON':
        return 'ellipse';
      case 'ORGANIZATION':
        return 'round-rectangle';
      case 'BANK_ACCOUNT':
        return 'round-hexagon';
      case 'CRYPTO_WALLET':
        return 'hexagon';
      case 'LOCATION':
        return 'diamond';
      default:
        return 'ellipse';
    }
  };

  // Initialize Cytoscape
  useEffect(() => {
    if (!containerRef.current || !graphData) return;

    // Filter nodes by selected type
    const filteredNodes = graphData.nodes.filter(n => 
      selectedTypes.length === 0 || selectedTypes.includes(n.data.type)
    );
    const nodeIds = new Set(filteredNodes.map(n => n.data.id));
    const filteredEdges = graphData.edges.filter(e => 
      nodeIds.has(e.data.source) && nodeIds.has(e.data.target)
    );

    const cy = cytoscape({
      container: containerRef.current,
      elements: {
        nodes: filteredNodes.map(n => ({
          data: {
            ...n.data,
            nodeColor: getNodeColor(n.data.type),
            nodeShape: getNodeShape(n.data.type),
            labelColor: n.data.type.toUpperCase() === 'PERSON' ? '#101010' : '#eeeeee',
          }
        })),
        edges: filteredEdges.map(e => ({
          data: {
            ...e.data,
            lineColor: e.data.kind === 'transaction' 
              ? (e.data.amount && e.data.amount > 50000 ? '#ee6018' : '#a0ca92')
              : '#4d4947',
            lineWidth: e.data.kind === 'transaction' ? 2.5 : 1.5,
          }
        })),
      },
      style: [
        {
          selector: 'node',
          style: {
            'shape': 'data(nodeShape)' as any,
            'background-color': 'data(nodeColor)',
            'label': 'data(label)',
            'color': '#eeeeee',
            'font-family': 'Geist, sans-serif',
            'font-size': '11px',
            'font-weight': 400,
            'text-valign': 'bottom',
            'text-margin-y': 6,
            'width': 36,
            'height': 36,
            'border-width': 1,
            'border-color': '#3d3a39',
            'transition-property': 'background-color, border-color, border-width, width, height',
            'transition-duration': 0.15,
          }
        },
        {
          selector: 'node:selected',
          style: {
            'border-width': 3,
            'border-color': '#eeeeee',
            'border-opacity': 1,
          }
        },
        {
          selector: 'node.highlighted',
          style: {
            'border-width': 3,
            'border-color': '#ee6018',
            'width': 44,
            'height': 44,
          }
        },
        {
          selector: 'edge',
          style: {
            'width': 'data(lineWidth)',
            'line-color': 'data(lineColor)',
            'target-arrow-color': 'data(lineColor)',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            'label': 'data(label)',
            'font-family': 'Geist Mono, monospace',
            'font-size': '9px',
            'color': '#8a8380',
            'text-background-color': '#101010',
            'text-background-opacity': 0.8,
            'text-background-padding': '2px',
            'arrow-scale': 0.9,
          }
        },
        {
          selector: 'edge:selected',
          style: {
            'line-color': '#eeeeee',
            'target-arrow-color': '#eeeeee',
            'width': 3,
          }
        },
        {
          selector: 'edge.highlighted',
          style: {
            'line-color': '#ee6018',
            'target-arrow-color': '#ee6018',
            'width': 3.5,
            'color': '#ee6018',
          }
        }
      ],
      layout: {
        name: 'cose',
        animate: true,
        animationDuration: 500,
        nodeDimensionsIncludeLabels: true,
        idealEdgeLength: 100,
        nodeOverlap: 20,
        refresh: 20,
        fit: true,
        padding: 50,
      } as any,
    });

    // Node click handler
    cy.on('tap', 'node', (evt) => {
      const node = evt.target;
      setSelectedNode(node.data());
      setSelectedEdge(null);
    });

    // Edge click handler
    cy.on('tap', 'edge', (evt) => {
      const edge = evt.target;
      setSelectedEdge(edge.data());
      setSelectedNode(null);
    });

    // Tap background handler
    cy.on('tap', (evt) => {
      if (evt.target === cy) {
        setSelectedNode(null);
        setSelectedEdge(null);
      }
    });

    cyRef.current = cy;

    return () => {
      cy.destroy();
    };
  }, [graphData, selectedTypes]);

  // Handle Search
  useEffect(() => {
    if (!cyRef.current) return;
    const cy = cyRef.current;
    if (!searchQuery.trim()) {
      cy.nodes().removeClass('highlighted');
      return;
    }
    const query = searchQuery.toLowerCase();
    const matched = cy.nodes().filter(n => 
      n.data('label').toLowerCase().includes(query) ||
      n.data('type').toLowerCase().includes(query)
    );
    cy.nodes().removeClass('highlighted');
    matched.addClass('highlighted');
    if (matched.length > 0) {
      cy.animate({
        center: { eles: matched },
        zoom: 1.2,
        duration: 300,
      });
    }
  }, [searchQuery]);

  // Zoom and Layout Controls
  const handleZoomIn = () => cyRef.current?.zoom(cyRef.current.zoom() * 1.25);
  const handleZoomOut = () => cyRef.current?.zoom(cyRef.current.zoom() * 0.8);
  const handleFit = () => cyRef.current?.fit(undefined, 40);
  const handleResetLayout = () => {
    cyRef.current?.layout({
      name: 'cose',
      animate: true,
      animationDuration: 400,
      fit: true,
      padding: 50,
    } as any).run();
  };

  // Toggle Type Filter
  const toggleType = (type: string) => {
    setSelectedTypes(prev => 
      prev.includes(type) ? prev.filter(t => t !== type) : [...prev, type]
    );
  };

  // Find Path between nodes
  const executePathSearch = async () => {
    if (!pathSource || !pathTarget || pathSource === pathTarget) {
      setPathError('Please select two distinct entities.');
      return;
    }
    setPathError(null);
    setIsFindingPath(true);
    try {
      const res = await api.findPath(caseId, pathSource, pathTarget, 6);
      setPathResults(res.paths);

      if (cyRef.current && res.paths.length > 0) {
        const cy = cyRef.current;
        cy.elements().removeClass('highlighted');
        
        // Highlight nodes and edges in the first path
        const firstPath = res.paths[0];
        firstPath.path.forEach((nid: string) => {
          cy.getElementById(nid).addClass('highlighted');
        });
        firstPath.edge_ids.forEach((eid: string) => {
          cy.getElementById(eid).addClass('highlighted');
        });
        
        // Fit highlighted elements
        const pathEles = cy.elements('.highlighted');
        cy.animate({
          fit: { eles: pathEles, padding: 60 },
          duration: 400,
        });
      } else if (res.paths.length === 0) {
        setPathError('No direct multi-hop path found within 6 hops.');
      }
    } catch (err: any) {
      setPathError('Failed to execute path query: ' + (err.response?.data?.detail || err.message));
    } finally {
      setIsFindingPath(false);
    }
  };

  const clearPathHighlight = () => {
    cyRef.current?.elements().removeClass('highlighted');
    setPathResults(null);
    setPathError(null);
  };

  const getTypeIcon = (type: string) => {
    switch (type.toUpperCase()) {
      case 'PERSON': return <User size={13} />;
      case 'ORGANIZATION': return <Building size={13} />;
      case 'BANK_ACCOUNT': return <CreditCard size={13} />;
      case 'CRYPTO_WALLET': return <Coins size={13} />;
      case 'LOCATION': return <MapPin size={13} />;
      case 'PHONE': return <Phone size={13} />;
      case 'EMAIL': return <Mail size={13} />;
      default: return <User size={13} />;
    }
  };

  return (
    <div className="graph-workspace">
      {/* Viewport */}
      <div className="graph-viewport">
        <div id="cy-container" ref={containerRef} />

        {/* Top-Left Toolbar */}
        <div className="graph-toolbar">
          <button className="btn btn-ghost btn-sm" onClick={handleZoomIn} title="Zoom In">
            <ZoomIn size={14} />
          </button>
          <button className="btn btn-ghost btn-sm" onClick={handleZoomOut} title="Zoom Out">
            <ZoomOut size={14} />
          </button>
          <button className="btn btn-ghost btn-sm" onClick={handleFit} title="Fit Graph">
            <Maximize2 size={14} />
          </button>
          <button className="btn btn-ghost btn-sm" onClick={handleResetLayout} title="Rearrange Force Layout">
            <RotateCw size={14} />
          </button>
          <div style={{ width: '1px', height: '16px', background: 'var(--color-ash-stroke)', margin: '0 4px' }} />
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Search size={13} style={{ color: 'var(--color-warm-granite)' }} />
            <input
              type="text"
              placeholder="Search entity..."
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              className="form-input"
              style={{ padding: '3px 8px', fontSize: '11px', width: '130px', background: 'transparent' }}
            />
          </div>
        </div>

        {/* Bottom Filter Chips */}
        <div className="graph-filter-bar">
          <span className="font-mono-tag" style={{ marginRight: '4px' }}>FILTER:</span>
          {availableTypes.map(t => {
            const active = selectedTypes.length === 0 || selectedTypes.includes(t);
            return (
              <button
                key={t}
                onClick={() => toggleType(t)}
                className={`filter-chip ${active ? 'active' : ''}`}
                style={{ display: 'flex', alignItems: 'center', gap: '4px' }}
              >
                {getTypeIcon(t)}
                <span>{t}</span>
              </button>
            );
          })}
        </div>

        {/* Top-Right Multi-Hop Path Finder Panel */}
        <div className="path-finder-panel">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <Route size={14} className="text-orange" />
              <span className="font-mono-tag" style={{ color: 'var(--color-bone)', fontSize: '11px' }}>
                RECURSIVE CTE PATH FINDER
              </span>
            </div>
            {pathResults && (
              <button onClick={clearPathHighlight} className="btn btn-ghost btn-sm" style={{ padding: '2px 6px' }}>
                <X size={12} />
              </button>
            )}
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
            <select
              value={pathSource}
              onChange={e => setPathSource(e.target.value)}
              className="form-input"
              style={{ fontSize: '11px', padding: '5px' }}
            >
              <option value="">Origin Entity...</option>
              {graphData?.nodes.map(n => (
                <option key={n.data.id} value={n.data.id}>
                  {n.data.label} ({n.data.type})
                </option>
              ))}
            </select>

            <div style={{ display: 'flex', justifyContent: 'center' }}>
              <ArrowRight size={12} className="text-muted" />
            </div>

            <select
              value={pathTarget}
              onChange={e => setPathTarget(e.target.value)}
              className="form-input"
              style={{ fontSize: '11px', padding: '5px' }}
            >
              <option value="">Target Entity...</option>
              {graphData?.nodes.map(n => (
                <option key={n.data.id} value={n.data.id}>
                  {n.data.label} ({n.data.type})
                </option>
              ))}
            </select>

            <button
              onClick={executePathSearch}
              disabled={isFindingPath}
              className="btn btn-primary btn-sm"
              style={{ marginTop: '4px', width: '100%' }}
            >
              {isFindingPath ? 'Traversing Graph...' : 'Trace Connection Path'}
            </button>
          </div>

          {pathError && (
            <div style={{ marginTop: '8px', fontSize: '11px', color: 'var(--color-signal-orange)' }}>
              {pathError}
            </div>
          )}

          {pathResults && pathResults.length > 0 && (
            <div style={{ marginTop: '8px', fontSize: '11px', color: 'var(--color-metric-green)' }}>
              ✓ Found {pathResults.length} path(s). Highlighted path of {pathResults[0].depth} hops.
            </div>
          )}
        </div>
      </div>

      {/* Side Inspector Drawer */}
      <div className="graph-inspector">
        {selectedNode ? (
          <div>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
              <span className="font-mono-tag">ENTITY INSPECTOR</span>
              <button onClick={() => setSelectedNode(null)} className="btn btn-ghost btn-sm" style={{ padding: '2px 6px' }}>
                <X size={12} />
              </button>
            </div>

            <div style={{ marginBottom: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
                <span 
                  style={{ 
                    display: 'inline-flex', 
                    padding: '4px', 
                    borderRadius: '3px', 
                    background: 'var(--color-carbon-lift)',
                    color: selectedNode.nodeColor 
                  }}
                >
                  {getTypeIcon(selectedNode.type)}
                </span>
                <span className="badge-tag" style={{ border: '1px solid var(--color-ash-stroke)' }}>
                  {selectedNode.type}
                </span>
              </div>
              <h3 style={{ fontSize: '18px', fontWeight: 500, color: 'var(--color-bone)', lineHeight: 1.2 }}>
                {selectedNode.label}
              </h3>
            </div>

            <div style={{ borderTop: '1px solid var(--color-ash-stroke)', paddingTop: '12px', marginBottom: '16px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '6px' }}>
                <span className="text-muted">OSINT Confidence:</span>
                <span className="text-green" style={{ fontFamily: 'var(--font-geist-mono)' }}>
                  {Math.round(selectedNode.confidence * 100)}%
                </span>
              </div>
              <div style={{ width: '100%', height: '4px', background: 'var(--color-carbon-lift)', borderRadius: '2px', overflow: 'hidden' }}>
                <div 
                  style={{ 
                    width: `${Math.round(selectedNode.confidence * 100)}%`, 
                    height: '100%', 
                    background: 'var(--color-metric-green)' 
                  }} 
                />
              </div>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginBottom: '16px' }}>
              <button 
                onClick={() => setPathSource(selectedNode.id)}
                className="btn btn-ghost btn-sm"
                style={{ width: '100%', justifyContent: 'flex-start' }}
              >
                Set as Path Origin
              </button>
              <button 
                onClick={() => setPathTarget(selectedNode.id)}
                className="btn btn-ghost btn-sm"
                style={{ width: '100%', justifyContent: 'flex-start' }}
              >
                Set as Path Destination
              </button>
            </div>

            <div style={{ fontSize: '11px', color: 'var(--color-warm-granite)', lineHeight: 1.4 }}>
              <span className="font-mono-tag" style={{ display: 'block', marginBottom: '4px' }}>ENTITY ID</span>
              <span style={{ fontFamily: 'var(--font-geist-mono)', wordBreak: 'break-all' }}>{selectedNode.id}</span>
            </div>
          </div>
        ) : selectedEdge ? (
          <div>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
              <span className="font-mono-tag">LINK INSPECTOR</span>
              <button onClick={() => setSelectedEdge(null)} className="btn btn-ghost btn-sm" style={{ padding: '2px 6px' }}>
                <X size={12} />
              </button>
            </div>

            <div style={{ marginBottom: '16px' }}>
              <span className={`badge-tag ${selectedEdge.kind === 'transaction' ? 'badge-critical' : 'badge-medium'}`} style={{ marginBottom: '8px' }}>
                {selectedEdge.kind.toUpperCase()}
              </span>
              <h3 style={{ fontSize: '16px', fontWeight: 500, color: 'var(--color-bone)', marginTop: '4px' }}>
                {selectedEdge.label}
              </h3>
            </div>

            {selectedEdge.amount && (
              <div style={{ background: 'var(--color-obsidian-canvas)', border: '1px solid var(--color-ash-stroke)', padding: '10px', borderRadius: '4px', marginBottom: '14px' }}>
                <span className="font-mono-tag">FUNDS TRANSFERRED</span>
                <div style={{ fontSize: '20px', color: 'var(--color-bone)', fontFamily: 'var(--font-geist-mono)', marginTop: '2px' }}>
                  ${selectedEdge.amount.toLocaleString('en-US', { minimumFractionDigits: 2 })} {selectedEdge.currency}
                </div>
                {selectedEdge.timestamp && (
                  <div style={{ fontSize: '10px', color: 'var(--color-warm-granite)', marginTop: '4px' }}>
                    {new Date(selectedEdge.timestamp).toUTCString()}
                  </div>
                )}
              </div>
            )}

            <div style={{ fontSize: '11px', color: 'var(--color-warm-granite)' }}>
              <span className="font-mono-tag" style={{ display: 'block', marginBottom: '4px' }}>EDGE TYPE</span>
              <span style={{ fontFamily: 'var(--font-geist-mono)' }}>{selectedEdge.type}</span>
            </div>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', textAlign: 'center', color: 'var(--color-warm-granite)' }}>
            <Building size={24} style={{ marginBottom: '8px', opacity: 0.4 }} />
            <div className="font-mono-tag">NO ELEMENT SELECTED</div>
            <div style={{ fontSize: '12px', marginTop: '6px', maxWidth: '200px' }}>
              Click any entity node or connection edge on the canvas to inspect provenance details.
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
