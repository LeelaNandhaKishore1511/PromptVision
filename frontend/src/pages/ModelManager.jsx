import React, { useState, useEffect } from 'react';
import { 
  Server, 
  Cpu, 
  HardDrive, 
  Activity, 
  CheckCircle2, 
  XCircle, 
  RefreshCw, 
  Trash2,
  Zap,
  ShieldAlert,
  Info
} from 'lucide-react';
import { getModels, selectModel, unloadModel, checkHealth } from '../services/api';

export default function ModelManager({ currentModel, onModelChanged, onRefreshHealth }) {
  const [modelData, setModelData] = useState(null);
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);
  const [actionMsg, setActionMsg] = useState('');

  async function loadModels() {
    setLoading(true);
    try {
      const [m, h] = await Promise.all([
        getModels().catch(() => ({ models: [] })),
        checkHealth().catch(() => ({ connected: false }))
      ]);
      setModelData(m);
      setHealth(h);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadModels();
  }, []);

  async function handleSelect(modelName) {
    try {
      await selectModel(modelName);
      setActionMsg(`Active model switched to ${modelName}`);
      if (onModelChanged) onModelChanged(modelName);
      loadModels();
      setTimeout(() => setActionMsg(''), 3000);
    } catch (err) {
      alert(`Model selection failed: ${err.message}`);
    }
  }

  async function handleUnload() {
    try {
      await unloadModel(currentModel);
      setActionMsg(`Model ${currentModel} unloaded from RAM to preserve system memory.`);
      if (onRefreshHealth) onRefreshHealth();
      setTimeout(() => setActionMsg(''), 4000);
    } catch (err) {
      alert(`Unload failed: ${err.message}`);
    }
  }

  const isConnected = health?.connected || false;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Header */}
      <div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span className="badge badge-amber">Infrastructure</span>
          <h2 style={{ fontSize: '1.4rem', fontWeight: 800 }}>Ollama Local Model Manager</h2>
        </div>
        <p style={{ color: 'var(--text-dim)', fontSize: '0.85rem', marginTop: '4px' }}>
          Configurable local model lifecycle, VLM selection, and memory management for Windows CPU execution.
        </p>
      </div>

      {actionMsg && (
        <div style={{ padding: '12px 16px', background: 'rgba(16, 185, 129, 0.15)', border: '1px solid var(--accent-green)', borderRadius: 'var(--radius-md)', color: '#6EE7B7', fontSize: '0.85rem' }}>
          {actionMsg}
        </div>
      )}

      {/* Ollama Connectivity & Controls */}
      <div className="grid-2">
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <h3 style={{ fontSize: '1rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Server size={18} color="var(--accent-blue)" />
              Ollama Server Endpoint
            </h3>
            <span className={`badge ${isConnected ? 'badge-green' : 'badge-red'}`}>
              {isConnected ? 'Connected' : 'Disconnected'}
            </span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '0.85rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 12px', background: 'var(--bg-main)', borderRadius: '6px' }}>
              <span style={{ color: 'var(--text-dim)' }}>Base URL:</span>
              <code style={{ color: 'var(--accent-cyan)' }}>http://localhost:11434</code>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 12px', background: 'var(--bg-main)', borderRadius: '6px' }}>
              <span style={{ color: 'var(--text-dim)' }}>Current Active Model:</span>
              <strong style={{ color: '#F1F5F9' }}>{currentModel}</strong>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 12px', background: 'var(--bg-main)', borderRadius: '6px' }}>
              <span style={{ color: 'var(--text-dim)' }}>Context Window:</span>
              <code style={{ color: '#E2E8F0' }}>4096 tokens (DEFAULT_NUM_CTX)</code>
            </div>
          </div>

          <div style={{ display: 'flex', gap: '10px', marginTop: '16px' }}>
            <button className="btn-secondary" onClick={loadModels} style={{ fontSize: '0.8rem' }}>
              <RefreshCw size={14} /> Refresh Status
            </button>
            <button className="btn-danger" onClick={handleUnload} style={{ fontSize: '0.8rem' }}>
              <Trash2 size={14} /> Unload Model from RAM
            </button>
          </div>
        </div>

        {/* Hardware & Memory Safeguards */}
        <div className="card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
            <Cpu size={18} color="var(--accent-amber)" />
            <h3 style={{ fontSize: '1rem', fontWeight: 700 }}>Target Hardware Profile & Protections</h3>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '6px' }}>
              <span>Processor:</span>
              <strong style={{ color: '#F1F5F9' }}>Intel Core i5-1235U (12th Gen)</strong>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '6px' }}>
              <span>System Memory:</span>
              <strong style={{ color: '#F1F5F9' }}>16 GB RAM (15.7 GB usable)</strong>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '6px' }}>
              <span>Integrated Graphics:</span>
              <strong style={{ color: '#F1F5F9' }}>Intel Iris Xe Graphics (CPU Inference)</strong>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '6px' }}>
              <span>Max Concurrent Models:</span>
              <strong style={{ color: 'var(--accent-green)' }}>1 Model (Strict Lock)</strong>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span>Strategy Inferences:</span>
              <strong style={{ color: 'var(--accent-cyan)' }}>Strictly Sequential</strong>
            </div>
          </div>

          <div style={{ marginTop: '14px', padding: '10px', background: 'rgba(245, 158, 11, 0.08)', borderRadius: '6px', border: '1px solid rgba(245, 158, 11, 0.2)', fontSize: '0.72rem', color: '#FCD34D' }}>
            <ShieldAlert size={14} style={{ display: 'inline', marginRight: '6px' }} />
            Zero external cloud APIs used. Inference runs 100% locally on localhost without leaking images or data.
          </div>
        </div>
      </div>

      {/* Installed Models Table */}
      <div className="card">
        <h3 style={{ fontSize: '1.05rem', fontWeight: 700, marginBottom: '12px' }}>
          Installed Local Ollama Models
        </h3>

        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.82rem', textAlign: 'left' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border-color)', color: 'var(--text-dim)' }}>
                <th style={{ padding: '10px' }}>Model Name</th>
                <th style={{ padding: '10px' }}>Disk Size</th>
                <th style={{ padding: '10px' }}>Primary Responsibility</th>
                <th style={{ padding: '10px' }}>Hardware Recommendation</th>
                <th style={{ padding: '10px', textAlign: 'right' }}>Status / Action</th>
              </tr>
            </thead>
            <tbody>
              {[
                {
                  name: 'qwen2.5vl:3b',
                  size: '~3.2 GB',
                  role: 'Default VLM: Summarisation, Analysis, Evaluation, Teach Mode, 3 Strategies',
                  rec: 'Optimal for Intel Core i5 & 16GB RAM CPU execution'
                },
                {
                  name: 'qwen3-vl:8b',
                  size: '~6.1 GB',
                  role: 'Advanced Multimodal VLM: Deep image reasoning and comparative benchmarking',
                  rec: 'Optional (Higher CPU/memory load on 16GB RAM)'
                },
                {
                  name: 'deepseek-ocr:latest',
                  size: '~6.7 GB',
                  role: 'Document text and diagram transcription (supplementary context)',
                  rec: 'Specialized OCR tasks'
                }
              ].map((m) => {
                const isSelected = currentModel === m.name;
                return (
                  <tr key={m.name} style={{ borderBottom: '1px solid var(--border-color)' }}>
                    <td style={{ padding: '12px 10px' }}>
                      <strong style={{ fontSize: '0.88rem', color: isSelected ? '#60A5FA' : '#F1F5F9', fontFamily: 'var(--font-mono)' }}>
                        {m.name}
                      </strong>
                    </td>
                    <td style={{ padding: '12px 10px', color: 'var(--text-muted)' }}>{m.size}</td>
                    <td style={{ padding: '12px 10px', color: 'var(--text-muted)', maxWidth: '320px' }}>{m.role}</td>
                    <td style={{ padding: '12px 10px', color: 'var(--text-dim)' }}>{m.rec}</td>
                    <td style={{ padding: '12px 10px', textAlign: 'right' }}>
                      {isSelected ? (
                        <span className="badge badge-green">Active Model</span>
                      ) : (
                        <button
                          className="btn-secondary"
                          style={{ padding: '6px 12px', fontSize: '0.75rem' }}
                          onClick={() => handleSelect(m.name)}
                        >
                          Select Model
                        </button>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
