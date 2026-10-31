import React from 'react';
import { 
  Sparkles, 
  Cpu, 
  Activity, 
  Terminal, 
  RefreshCw,
  HardDrive
} from 'lucide-react';

export default function Navbar({ health, currentModel, onRefreshStatus }) {
  const isOnline = health?.connected || false;

  return (
    <header style={{
      height: '64px',
      background: 'rgba(19, 26, 38, 0.85)',
      backdropFilter: 'blur(12px)',
      borderBottom: '1px solid var(--border-color)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 32px',
      position: 'sticky',
      top: 0,
      zIndex: 40,
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <div style={{
          width: '36px',
          height: '36px',
          borderRadius: '10px',
          background: 'linear-gradient(135deg, #3B82F6, #8B5CF6)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 0 15px rgba(59, 130, 246, 0.5)'
        }}>
          <Sparkles size={20} color="#fff" />
        </div>
        <div>
          <h1 style={{ fontSize: '1.15rem', fontWeight: 800, letterSpacing: '-0.02em', background: 'linear-gradient(90deg, #F8FAFC, #94A3B8)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
            PromptVision
          </h1>
          <p style={{ fontSize: '0.72rem', color: 'var(--text-dim)', fontWeight: 500 }}>
            Option-Driven Automated Prompt Engineering & Computer Vision Analysis Framework
          </p>
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        {/* Model Badge */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          padding: '6px 14px',
          background: 'var(--bg-main)',
          border: '1px solid var(--border-color)',
          borderRadius: 'var(--radius-full)',
          fontSize: '0.82rem'
        }}>
          <Cpu size={15} color="var(--accent-cyan)" />
          <span style={{ color: 'var(--text-muted)' }}>VLM:</span>
          <strong style={{ color: '#E2E8F0', fontFamily: 'var(--font-mono)' }}>
            {currentModel || 'qwen2.5vl:3b'}
          </strong>
        </div>

        {/* Ollama Status Badge */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          padding: '6px 14px',
          background: isOnline ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)',
          border: `1px solid ${isOnline ? 'rgba(16, 185, 129, 0.3)' : 'rgba(239, 68, 68, 0.3)'}`,
          borderRadius: 'var(--radius-full)',
          fontSize: '0.82rem'
        }}>
          <span style={{
            width: '8px',
            height: '8px',
            borderRadius: '50%',
            background: isOnline ? '#10B981' : '#EF4444',
            boxShadow: isOnline ? '0 0 8px #10B981' : '0 0 8px #EF4444'
          }} />
          <span style={{ color: isOnline ? '#34D399' : '#F87171', fontWeight: 600 }}>
            Ollama {isOnline ? 'Online (Local)' : 'Offline'}
          </span>
        </div>

        {/* Refresh Status Button */}
        <button 
          onClick={onRefreshStatus}
          title="Refresh Ollama connection"
          style={{
            background: 'transparent',
            color: 'var(--text-muted)',
            padding: '8px',
            borderRadius: 'var(--radius-md)',
            border: '1px solid var(--border-color)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}
        >
          <RefreshCw size={15} />
        </button>
      </div>
    </header>
  );
}
