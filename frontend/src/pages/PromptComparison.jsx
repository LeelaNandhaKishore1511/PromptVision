import React, { useState, useEffect } from 'react';
import { 
  GitCompare, 
  Clock, 
  Zap, 
  Hash, 
  Star, 
  Check, 
  Save, 
  FileText,
  AlertCircle,
  Eye
} from 'lucide-react';
import { getExperiments, getExperiment, submitEvaluation } from '../services/api';

const DIMENSIONS = [
  { id: 'accuracy', label: 'Accuracy & Grounding' },
  { id: 'relevance', label: 'Relevance to Objective' },
  { id: 'completeness', label: 'Completeness & Depth' },
  { id: 'instruction_adherence', label: 'Instruction Adherence' },
  { id: 'consistency', label: 'Logical Consistency' },
  { id: 'clarity', label: 'Clarity & Formatting' },
  { id: 'hallucination_reduction', label: 'Hallucination Reduction' },
];

export default function PromptComparison({ activeExperimentId }) {
  const [experiments, setExperiments] = useState([]);
  const [selectedExpId, setSelectedExpId] = useState(activeExperimentId || null);
  const [currentExp, setCurrentExp] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('all'); // all, basic, costar, ai_optimized
  const [ratings, setRatings] = useState({});
  const [savedSuccess, setSavedSuccess] = useState(false);

  useEffect(() => {
    getExperiments().then(data => {
      setExperiments(data);
      if (!selectedExpId && data && data.length > 0) {
        setSelectedExpId(data[0].id);
      }
    }).catch(console.error);
  }, []);

  useEffect(() => {
    if (activeExperimentId) {
      setSelectedExpId(activeExperimentId);
    }
  }, [activeExperimentId]);

  useEffect(() => {
    if (!selectedExpId) return;
    setLoading(true);
    getExperiment(selectedExpId).then(exp => {
      setCurrentExp(exp);
      setRatings(exp.ratings || {
        basic: { accuracy: 4, relevance: 4, completeness: 3, instruction_adherence: 4, consistency: 4, clarity: 4, hallucination_reduction: 4 },
        costar: { accuracy: 4.5, relevance: 4.5, completeness: 4, instruction_adherence: 4.5, consistency: 4.5, clarity: 4.5, hallucination_reduction: 4.5 },
        ai_optimized: { accuracy: 5, relevance: 5, completeness: 4.8, instruction_adherence: 4.8, consistency: 4.8, clarity: 4.8, hallucination_reduction: 5 }
      });
      setSavedSuccess(false);
    }).catch(console.error).finally(() => setLoading(false));
  }, [selectedExpId]);

  function handleRatingChange(strategy, dimension, value) {
    setRatings(prev => ({
      ...prev,
      [strategy]: {
        ...(prev[strategy] || {}),
        [dimension]: value
      }
    }));
    setSavedSuccess(false);
  }

  async function handleSaveRatings() {
    if (!selectedExpId) return;
    try {
      await submitEvaluation(selectedExpId, ratings);
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 3000);
    } catch (err) {
      alert(`Save failed: ${err.message}`);
    }
  }

  if (!currentExp && !loading) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '48px 24px', color: 'var(--text-dim)' }}>
        <GitCompare size={40} style={{ opacity: 0.5, marginBottom: '12px' }} />
        <h3>No Experiment Selected</h3>
        <p style={{ fontSize: '0.88rem', marginTop: '6px' }}>Run a new experiment or select one from history to compare strategy outputs.</p>
      </div>
    );
  }

  const responses = currentExp?.responses || {};
  const metrics = currentExp?.metrics || {};
  const prompts = currentExp?.prompts || {};

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Top Controls: Selector and Metadata */}
      <div className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <span className="badge badge-purple">{currentExp?.selected_objective || 'Experiment'}</span>
            <h2 style={{ fontSize: '1.25rem', fontWeight: 800 }}>{currentExp?.title}</h2>
          </div>
          <p style={{ color: 'var(--text-dim)', fontSize: '0.8rem', marginTop: '4px' }}>
            Model: <strong style={{ color: 'var(--accent-cyan)' }}>{currentExp?.selected_model}</strong> • Target Image: {currentExp?.image_filename}
          </p>
        </div>

        {/* Experiment Switcher Dropdown */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Switch Run:</label>
          <select 
            value={selectedExpId || ''} 
            onChange={e => setSelectedExpId(e.target.value)}
            style={{ fontSize: '0.82rem' }}
          >
            {experiments.map(e => (
              <option key={e.id} value={e.id}>
                {e.title} ({e.selected_objective})
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Strategy View Tabs */}
      <div style={{ display: 'flex', gap: '8px' }}>
        {[
          { id: 'all', label: 'Side-by-Side 3-Way Comparison' },
          { id: 'basic', label: 'Strategy 1: Basic Baseline' },
          { id: 'costar', label: 'Strategy 2: CO-STAR Framework' },
          { id: 'ai_optimized', label: 'Strategy 3: AI-Generated Optimized' },
        ].map(t => (
          <button
            key={t.id}
            onClick={() => setActiveTab(t.id)}
            style={{
              padding: '8px 16px',
              borderRadius: 'var(--radius-md)',
              background: activeTab === t.id ? 'var(--accent-blue)' : 'var(--bg-card)',
              color: activeTab === t.id ? '#fff' : 'var(--text-muted)',
              border: `1px solid ${activeTab === t.id ? 'var(--accent-blue)' : 'var(--border-color)'}`,
              fontSize: '0.82rem',
              fontWeight: 600
            }}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* 3 Panels Comparison Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: activeTab === 'all' ? 'repeat(3, 1fr)' : '1fr',
        gap: '20px'
      }}>
        {/* STRATEGY 1: BASIC */}
        {(activeTab === 'all' || activeTab === 'basic') && (
          <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span className="badge badge-gray">Strategy 1</span>
              <strong style={{ fontSize: '0.9rem' }}>Basic Prompting</strong>
            </div>

            {/* Performance Metrics Pills */}
            <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', fontSize: '0.75rem', color: 'var(--text-dim)' }}>
              <span style={{ display: 'flex', alignItems: 'center', gap: '4px', background: 'var(--bg-main)', padding: '4px 8px', borderRadius: '4px' }}>
                <Clock size={12} color="var(--accent-cyan)" />
                {metrics?.basic?.latency_sec ? `${metrics.basic.latency_sec}s` : 'N/A'}
              </span>
              <span style={{ display: 'flex', alignItems: 'center', gap: '4px', background: 'var(--bg-main)', padding: '4px 8px', borderRadius: '4px' }}>
                <Hash size={12} color="var(--accent-purple)" />
                {metrics?.basic?.eval_count ? `${metrics.basic.eval_count} tokens` : 'N/A'}
              </span>
              {metrics?.basic?.tokens_per_sec && (
                <span style={{ display: 'flex', alignItems: 'center', gap: '4px', background: 'var(--bg-main)', padding: '4px 8px', borderRadius: '4px' }}>
                  <Zap size={12} color="var(--accent-green)" />
                  {metrics.basic.tokens_per_sec} tok/s
                </span>
              )}
            </div>

            {/* Collapsible Prompt Preview */}
            <details style={{ background: 'var(--bg-main)', borderRadius: '6px', padding: '8px 12px', border: '1px solid var(--border-color)', fontSize: '0.78rem' }}>
              <summary style={{ cursor: 'pointer', color: 'var(--text-muted)', fontWeight: 600 }}>
                View Basic Prompt ({prompts?.basic?.split(/\s+/).length || 0} words)
              </summary>
              <pre style={{ marginTop: '8px', whiteSpace: 'pre-wrap', color: 'var(--text-dim)', fontSize: '0.72rem' }}>
                {prompts?.basic}
              </pre>
            </details>

            {/* Model Response Body */}
            <div style={{ flex: 1, minHeight: '260px', background: 'var(--bg-main)', borderRadius: '8px', padding: '16px', border: '1px solid var(--border-color)', overflowY: 'auto' }}>
              <p style={{ fontSize: '0.85rem', lineHeight: 1.6, whiteSpace: 'pre-wrap', color: 'var(--text-main)' }}>
                {responses?.basic || 'No response captured for this strategy.'}
              </p>
            </div>
          </div>
        )}

        {/* STRATEGY 2: CO-STAR */}
        {(activeTab === 'all' || activeTab === 'costar') && (
          <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span className="badge badge-blue">Strategy 2</span>
              <strong style={{ fontSize: '0.9rem' }}>Framework-Based (CO-STAR)</strong>
            </div>

            {/* Performance Metrics Pills */}
            <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', fontSize: '0.75rem', color: 'var(--text-dim)' }}>
              <span style={{ display: 'flex', alignItems: 'center', gap: '4px', background: 'var(--bg-main)', padding: '4px 8px', borderRadius: '4px' }}>
                <Clock size={12} color="var(--accent-cyan)" />
                {metrics?.costar?.latency_sec ? `${metrics.costar.latency_sec}s` : 'N/A'}
              </span>
              <span style={{ display: 'flex', alignItems: 'center', gap: '4px', background: 'var(--bg-main)', padding: '4px 8px', borderRadius: '4px' }}>
                <Hash size={12} color="var(--accent-purple)" />
                {metrics?.costar?.eval_count ? `${metrics.costar.eval_count} tokens` : 'N/A'}
              </span>
              {metrics?.costar?.tokens_per_sec && (
                <span style={{ display: 'flex', alignItems: 'center', gap: '4px', background: 'var(--bg-main)', padding: '4px 8px', borderRadius: '4px' }}>
                  <Zap size={12} color="var(--accent-green)" />
                  {metrics.costar.tokens_per_sec} tok/s
                </span>
              )}
            </div>

            {/* Collapsible Prompt Preview */}
            <details style={{ background: 'var(--bg-main)', borderRadius: '6px', padding: '8px 12px', border: '1px solid var(--border-color)', fontSize: '0.78rem' }}>
              <summary style={{ cursor: 'pointer', color: 'var(--accent-blue)', fontWeight: 600 }}>
                View CO-STAR Prompt ({prompts?.costar?.split(/\s+/).length || 0} words)
              </summary>
              <pre style={{ marginTop: '8px', whiteSpace: 'pre-wrap', color: 'var(--text-dim)', fontSize: '0.72rem' }}>
                {prompts?.costar}
              </pre>
            </details>

            {/* Model Response Body */}
            <div style={{ flex: 1, minHeight: '260px', background: 'var(--bg-main)', borderRadius: '8px', padding: '16px', border: '1px solid var(--border-color)', overflowY: 'auto' }}>
              <p style={{ fontSize: '0.85rem', lineHeight: 1.6, whiteSpace: 'pre-wrap', color: 'var(--text-main)' }}>
                {responses?.costar || 'No response captured for this strategy.'}
              </p>
            </div>
          </div>
        )}

        {/* STRATEGY 3: AI-OPTIMIZED */}
        {(activeTab === 'all' || activeTab === 'ai_optimized') && (
          <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span className="badge badge-purple">Strategy 3</span>
              <strong style={{ fontSize: '0.9rem' }}>AI-Generated Optimized</strong>
            </div>

            {/* Performance Metrics Pills */}
            <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', fontSize: '0.75rem', color: 'var(--text-dim)' }}>
              <span style={{ display: 'flex', alignItems: 'center', gap: '4px', background: 'var(--bg-main)', padding: '4px 8px', borderRadius: '4px' }}>
                <Clock size={12} color="var(--accent-cyan)" />
                {metrics?.ai_optimized?.latency_sec ? `${metrics.ai_optimized.latency_sec}s` : 'N/A'}
              </span>
              <span style={{ display: 'flex', alignItems: 'center', gap: '4px', background: 'var(--bg-main)', padding: '4px 8px', borderRadius: '4px' }}>
                <Hash size={12} color="var(--accent-purple)" />
                {metrics?.ai_optimized?.eval_count ? `${metrics.ai_optimized.eval_count} tokens` : 'N/A'}
              </span>
              {metrics?.ai_optimized?.tokens_per_sec && (
                <span style={{ display: 'flex', alignItems: 'center', gap: '4px', background: 'var(--bg-main)', padding: '4px 8px', borderRadius: '4px' }}>
                  <Zap size={12} color="var(--accent-green)" />
                  {metrics.ai_optimized.tokens_per_sec} tok/s
                </span>
              )}
            </div>

            {/* Collapsible Prompt Preview */}
            <details style={{ background: 'var(--bg-main)', borderRadius: '6px', padding: '8px 12px', border: '1px solid var(--border-color)', fontSize: '0.78rem' }}>
              <summary style={{ cursor: 'pointer', color: 'var(--accent-purple)', fontWeight: 600 }}>
                View AI-Optimized Prompt ({prompts?.ai_optimized?.split(/\s+/).length || 0} words)
              </summary>
              <pre style={{ marginTop: '8px', whiteSpace: 'pre-wrap', color: 'var(--text-dim)', fontSize: '0.72rem' }}>
                {prompts?.ai_optimized}
              </pre>
            </details>

            {/* Model Response Body */}
            <div style={{ flex: 1, minHeight: '260px', background: 'var(--bg-main)', borderRadius: '8px', padding: '16px', border: '1px solid var(--border-color)', overflowY: 'auto' }}>
              <p style={{ fontSize: '0.85rem', lineHeight: 1.6, whiteSpace: 'pre-wrap', color: 'var(--text-main)' }}>
                {responses?.ai_optimized || 'No response captured for this strategy.'}
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Human Qualitative & Quantitative Evaluation Grid */}
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <div>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>Human Evaluation & Research Ratings</h3>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-dim)' }}>
              Rate each response on a 1-5 scale across the 7 research dimensions. Saved directly to the SQLite database.
            </p>
          </div>
          <button 
            className="btn-primary"
            onClick={handleSaveRatings}
            style={{ fontSize: '0.85rem', padding: '8px 16px' }}
          >
            {savedSuccess ? <Check size={16} /> : <Save size={16} />}
            {savedSuccess ? 'Ratings Saved!' : 'Save Ratings'}
          </button>
        </div>

        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.82rem' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border-color)', color: 'var(--text-dim)', textAlign: 'left' }}>
                <th style={{ padding: '10px' }}>Evaluation Dimension</th>
                <th style={{ padding: '10px' }}>Basic (Strategy 1)</th>
                <th style={{ padding: '10px' }}>CO-STAR (Strategy 2)</th>
                <th style={{ padding: '10px' }}>AI-Optimized (Strategy 3)</th>
              </tr>
            </thead>
            <tbody>
              {DIMENSIONS.map((dim) => (
                <tr key={dim.id} style={{ borderBottom: '1px solid var(--border-color)' }}>
                  <td style={{ padding: '10px', fontWeight: 600 }}>{dim.label}</td>
                  {['basic', 'costar', 'ai_optimized'].map((strat) => {
                    const currentVal = ratings[strat]?.[dim.id] || 4;
                    return (
                      <td key={strat} style={{ padding: '10px' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                          {[1, 2, 3, 4, 5].map((star) => (
                            <Star
                              key={star}
                              size={16}
                              onClick={() => handleRatingChange(strat, dim.id, star)}
                              style={{
                                cursor: 'pointer',
                                fill: star <= currentVal ? '#FBBF24' : 'transparent',
                                color: star <= currentVal ? '#FBBF24' : 'var(--text-dim)'
                              }}
                            />
                          ))}
                          <span style={{ marginLeft: '6px', fontFamily: 'var(--font-mono)', fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                            {currentVal}
                          </span>
                        </div>
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
