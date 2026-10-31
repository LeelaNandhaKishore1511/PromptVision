import React, { useEffect, useState } from 'react';
import { 
  FlaskConical, 
  Eye, 
  CheckCircle2, 
  Cpu, 
  ArrowRight, 
  Layers, 
  Zap,
  TrendingUp,
  FileText
} from 'lucide-react';
import { getDashboardStats, getResearchSummary } from '../services/api';

export default function Dashboard({ onNavigate, currentModel, health }) {
  const [stats, setStats] = useState(null);
  const [researchSummary, setResearchSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [dash, res] = await Promise.all([
          getDashboardStats().catch(() => null),
          getResearchSummary().catch(() => null)
        ]);
        setStats(dash);
        setResearchSummary(res);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const totalExps = stats?.total_experiments || 0;
  const totalImgs = stats?.total_images || 0;
  const totalTeach = stats?.total_teach_sessions || 0;
  const recentExps = stats?.recent_experiments || [];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '28px' }}>
      {/* Hero Welcome Banner */}
      <div style={{
        background: 'linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9))',
        border: '1px solid var(--border-color)',
        borderRadius: 'var(--radius-lg)',
        padding: '28px 32px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        position: 'relative',
        overflow: 'hidden'
      }}>
        <div style={{ maxWidth: '680px', zIndex: 2 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
            <span className="badge badge-blue">Final Year Project • B.Tech AIML</span>
            <span className="badge badge-green">Local CPU Inference</span>
          </div>
          <h2 style={{ fontSize: '1.75rem', fontWeight: 800, letterSpacing: '-0.02em', marginBottom: '8px' }}>
            Automated Option-Driven Prompt Engineering & CV Analysis
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem', lineHeight: 1.6 }}>
            Eliminate manual prompt crafting. Upload visual inputs, choose your research objective and structured preferences, extract empirical Computer Vision features, and benchmark three prompt strategies on local VLMs.
          </p>
          <div style={{ display: 'flex', gap: '12px', marginTop: '20px' }}>
            <button 
              className="btn-primary"
              onClick={() => onNavigate('new-experiment')}
            >
              <FlaskConical size={18} />
              Start New Experiment
            </button>
            <button 
              className="btn-secondary"
              onClick={() => onNavigate('cv-lab')}
            >
              <Eye size={18} />
              Explore CV Lab
            </button>
          </div>
        </div>
      </div>

      {/* Top 4 Stat Cards */}
      <div className="grid-4">
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-dim)', marginBottom: '8px' }}>
            <span style={{ fontSize: '0.82rem', fontWeight: 600 }}>TOTAL EXPERIMENTS</span>
            <FlaskConical size={18} color="var(--accent-blue)" />
          </div>
          <p style={{ fontSize: '1.8rem', fontWeight: 800 }}>{totalExps}</p>
          <span style={{ fontSize: '0.75rem', color: 'var(--accent-green)' }}>Controlled multimodal runs</span>
        </div>

        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-dim)', marginBottom: '8px' }}>
            <span style={{ fontSize: '0.82rem', fontWeight: 600 }}>IMAGES PROCESSED</span>
            <Eye size={18} color="var(--accent-cyan)" />
          </div>
          <p style={{ fontSize: '1.8rem', fontWeight: 800 }}>{totalImgs}</p>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Unique visual inputs analyzed</span>
        </div>

        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-dim)', marginBottom: '8px' }}>
            <span style={{ fontSize: '0.82rem', fontWeight: 600 }}>TEACH SESSIONS</span>
            <CheckCircle2 size={18} color="var(--accent-purple)" />
          </div>
          <p style={{ fontSize: '1.8rem', fontWeight: 800 }}>{totalTeach}</p>
          <span style={{ fontSize: '0.75rem', color: 'var(--accent-purple)' }}>Interactive quizzes evaluated</span>
        </div>

        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-dim)', marginBottom: '8px' }}>
            <span style={{ fontSize: '0.82rem', fontWeight: 600 }}>ACTIVE VISION MODEL</span>
            <Cpu size={18} color="var(--accent-amber)" />
          </div>
          <p style={{ fontSize: '1.2rem', fontWeight: 700, fontFamily: 'var(--font-mono)' }}>
            {currentModel}
          </p>
          <span style={{ fontSize: '0.75rem', color: health?.connected ? 'var(--accent-green)' : 'var(--accent-red)' }}>
            {health?.connected ? 'Ollama Ready (Local)' : 'Ollama Offline'}
          </span>
        </div>
      </div>

      {/* Main 2-Column Section */}
      <div className="grid-2">
        {/* Computer Vision Modules Overview */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <div>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>Computer Vision Engine</h3>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-dim)' }}>Five complete B.Tech syllabus modules</p>
            </div>
            <button className="btn-secondary" style={{ padding: '6px 12px', fontSize: '0.8rem' }} onClick={() => onNavigate('cv-lab')}>
              Open CV Lab <ArrowRight size={14} />
            </button>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {[
              { mod: 'Module 1', title: 'Introduction & Representations', ops: 'Sampling, Pixel Stats, 2D FFT, Haar Wavelet' },
              { mod: 'Module 2', title: 'Image Filtering & Enhancement', ops: 'Gaussian, Bilateral, Otsu, Morphological, CLAHE' },
              { mod: 'Module 3', title: 'Feature Detection & Matching', ops: 'Harris, Canny, Hough Grid, Contours, ORB, Haar Face/Eye' },
              { mod: 'Module 4', title: 'Image Segmentation', ops: 'Snakes, Quadtree Split-Merge, Watershed, Mean Shift, SLIC' },
              { mod: 'Module 5', title: 'Transforms, Alignment & Motion', ops: 'Rigid, Affine, ORB RANSAC Registration, Farneback Flow' },
            ].map((m, idx) => (
              <div 
                key={idx}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '12px 14px',
                  background: 'var(--bg-main)',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--border-color)'
                }}
              >
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span className="badge badge-blue" style={{ fontSize: '0.65rem' }}>{m.mod}</span>
                    <strong style={{ fontSize: '0.88rem' }}>{m.title}</strong>
                  </div>
                  <p style={{ fontSize: '0.75rem', color: 'var(--text-dim)', marginTop: '4px' }}>{m.ops}</p>
                </div>
                <CheckCircle2 size={16} color="var(--accent-green)" />
              </div>
            ))}
          </div>
        </div>

        {/* 3 Prompt Strategies & Research Dimensions */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <div>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>3 Prompt Engineering Strategies</h3>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-dim)' }}>Comparative evaluation protocol on identical VLM</p>
            </div>
            <button className="btn-secondary" style={{ padding: '6px 12px', fontSize: '0.8rem' }} onClick={() => onNavigate('pe-lab')}>
              Learning Lab <ArrowRight size={14} />
            </button>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <div style={{ padding: '14px', background: 'var(--bg-main)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span className="badge badge-gray">Strategy 1</span>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>Zero-Shot Baseline</span>
              </div>
              <h4 style={{ fontSize: '0.95rem', fontWeight: 700, marginTop: '6px' }}>Basic Prompting</h4>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                Objective-specific prompt anatomy (Instruction, Context, Input, Output, Constraints) establishing an un-optimized control baseline.
              </p>
            </div>

            <div style={{ padding: '14px', background: 'var(--bg-main)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span className="badge badge-blue">Strategy 2</span>
                <span style={{ fontSize: '0.75rem', color: 'var(--accent-blue)' }}>CO-STAR Framework</span>
              </div>
              <h4 style={{ fontSize: '0.95rem', fontWeight: 700, marginTop: '6px' }}>Framework-Based Prompting</h4>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                Context, Objective, Style, Tone, Audience, Response format with zero-, one-, and few-shot exemplars and MCQ preferences.
              </p>
            </div>

            <div style={{ padding: '14px', background: 'var(--bg-main)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span className="badge badge-purple">Strategy 3</span>
                <span style={{ fontSize: '0.75rem', color: 'var(--accent-purple)' }}>CV-Grounding & Guardrails</span>
              </div>
              <h4 style={{ fontSize: '0.95rem', fontWeight: 700, marginTop: '6px' }}>AI-Generated Optimized Prompt</h4>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                Automated role persona, empirical CV feature integration, uncertainty handling, and strict anti-hallucination negative constraints.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Experiments Section */}
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <div>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>Recent Experimental Runs</h3>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-dim)' }}>Latest multimodal benchmark experiments</p>
          </div>
          <button className="btn-secondary" style={{ padding: '6px 12px', fontSize: '0.8rem' }} onClick={() => onNavigate('history')}>
            View All History <ArrowRight size={14} />
          </button>
        </div>

        {recentExps.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '36px 16px', color: 'var(--text-dim)' }}>
            <FileText size={36} style={{ marginBottom: '8px', opacity: 0.5 }} />
            <p>No experiments saved yet. Launch your first experiment using the button above!</p>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {recentExps.slice(0, 5).map((exp) => (
              <div 
                key={exp.id}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '12px 16px',
                  background: 'var(--bg-main)',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--border-color)'
                }}
              >
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span className="badge badge-purple">{exp.selected_objective}</span>
                    <strong style={{ fontSize: '0.9rem' }}>{exp.title}</strong>
                  </div>
                  <p style={{ fontSize: '0.75rem', color: 'var(--text-dim)', marginTop: '4px' }}>
                    Model: <code style={{ color: 'var(--accent-cyan)' }}>{exp.selected_model}</code> • CV Operations: {exp.cv_operations?.length || 0}
                  </p>
                </div>
                <button 
                  className="btn-secondary"
                  style={{ padding: '6px 12px', fontSize: '0.78rem' }}
                  onClick={() => onNavigate('history')}
                >
                  View Details
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
