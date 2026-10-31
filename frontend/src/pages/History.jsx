import React, { useState, useEffect } from 'react';
import { 
  History as HistoryIcon, 
  Search, 
  Trash2, 
  ExternalLink, 
  FileSpreadsheet, 
  RefreshCw,
  Clock,
  Layers,
  Cpu,
  Eye
} from 'lucide-react';
import { getExperiments, deleteExperiment, getFullImageUrl } from '../services/api';

export default function History({ onSelectExperiment, onNavigate }) {
  const [experiments, setExperiments] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  async function loadData(query = '') {
    setLoading(true);
    try {
      const data = await getExperiments(query);
      setExperiments(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData(search);
  }, [search]);

  async function handleDelete(id, title) {
    if (!window.confirm(`Are you sure you want to delete '${title}'?`)) return;
    try {
      await deleteExperiment(id);
      setExperiments(experiments.filter(e => e.id !== id));
    } catch (err) {
      alert(`Delete failed: ${err.message}`);
    }
  }

  function handleReopen(expId) {
    if (onSelectExperiment) {
      onSelectExperiment(expId);
    }
    if (onNavigate) {
      onNavigate('compare');
    }
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Header and Search */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span className="badge badge-purple">Persistence</span>
            <h2 style={{ fontSize: '1.4rem', fontWeight: 800 }}>Experiment History & Database</h2>
          </div>
          <p style={{ color: 'var(--text-dim)', fontSize: '0.85rem', marginTop: '4px' }}>
            Indexed experimental runs stored in SQLite (<code>promptvision.db</code>).
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{ position: 'relative' }}>
            <Search size={16} color="var(--text-dim)" style={{ position: 'absolute', left: '10px', top: '10px' }} />
            <input
              type="text"
              placeholder="Search runs by title, objective, or model..."
              value={search}
              onChange={e => setSearch(e.target.value)}
              style={{ paddingLeft: '32px', width: '280px', fontSize: '0.82rem' }}
            />
          </div>
          <a
            href={getFullImageUrl('/api/experiments/export')}
            download
            className="btn-secondary"
            style={{ textDecoration: 'none', fontSize: '0.82rem', padding: '8px 14px' }}
          >
            <FileSpreadsheet size={15} /> Export CSV
          </a>
        </div>
      </div>

      {/* Experiments Table Card */}
      <div className="card" style={{ padding: '0', overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.82rem', textAlign: 'left' }}>
          <thead>
            <tr style={{ background: 'rgba(0,0,0,0.2)', borderBottom: '1px solid var(--border-color)', color: 'var(--text-dim)' }}>
              <th style={{ padding: '14px 18px' }}>Experiment</th>
              <th style={{ padding: '14px 18px' }}>Objective</th>
              <th style={{ padding: '14px 18px' }}>Vision Model</th>
              <th style={{ padding: '14px 18px' }}>CV Operations</th>
              <th style={{ padding: '14px 18px' }}>Date & Time</th>
              <th style={{ padding: '14px 18px', textAlign: 'right' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={6} style={{ padding: '36px', textAlign: 'center', color: 'var(--text-dim)' }}>
                  Loading experiments from SQLite...
                </td>
              </tr>
            ) : experiments.length === 0 ? (
              <tr>
                <td colSpan={6} style={{ padding: '36px', textAlign: 'center', color: 'var(--text-dim)' }}>
                  No experiments found matching your criteria.
                </td>
              </tr>
            ) : (
              experiments.map((exp) => (
                <tr 
                  key={exp.id} 
                  style={{ borderBottom: '1px solid var(--border-color)', transition: 'background 0.15s' }}
                  onMouseEnter={e => e.currentTarget.style.background = 'rgba(255,255,255,0.02)'}
                  onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
                >
                  <td style={{ padding: '14px 18px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                      <Eye size={16} color="var(--accent-blue)" />
                      <div>
                        <strong style={{ fontSize: '0.88rem', color: '#F1F5F9' }}>{exp.title}</strong>
                        <p style={{ fontSize: '0.72rem', color: 'var(--text-dim)' }}>{exp.image_filename}</p>
                      </div>
                    </div>
                  </td>
                  <td style={{ padding: '14px 18px' }}>
                    <span className="badge badge-purple" style={{ fontSize: '0.7rem' }}>
                      {exp.selected_objective}
                    </span>
                  </td>
                  <td style={{ padding: '14px 18px' }}>
                    <code style={{ color: 'var(--accent-cyan)', fontSize: '0.78rem' }}>{exp.selected_model}</code>
                  </td>
                  <td style={{ padding: '14px 18px' }}>
                    <span style={{ color: 'var(--text-muted)' }}>
                      {exp.cv_operations?.length || 0} operations
                    </span>
                  </td>
                  <td style={{ padding: '14px 18px', color: 'var(--text-dim)', fontSize: '0.75rem' }}>
                    {new Date(exp.created_at).toLocaleString()}
                  </td>
                  <td style={{ padding: '14px 18px', textAlign: 'right' }}>
                    <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px' }}>
                      <button
                        className="btn-secondary"
                        style={{ padding: '6px 10px', fontSize: '0.75rem' }}
                        onClick={() => handleReopen(exp.id)}
                        title="Reopen and compare"
                      >
                        <ExternalLink size={13} /> Reopen
                      </button>
                      <button
                        className="btn-danger"
                        style={{ padding: '6px 10px', fontSize: '0.75rem' }}
                        onClick={() => handleDelete(exp.id, exp.title)}
                        title="Delete record"
                      >
                        <Trash2 size={13} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
