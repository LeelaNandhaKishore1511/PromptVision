import React from 'react';
import { 
  LayoutDashboard, 
  FlaskConical, 
  Eye, 
  BookOpen, 
  GitCompare, 
  GraduationCap, 
  BarChart3, 
  History, 
  Server, 
  Info,
  ChevronRight
} from 'lucide-react';

const NAV_ITEMS = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { id: 'new-experiment', label: 'New Experiment', icon: FlaskConical, highlight: true },
  { id: 'cv-lab', label: 'Computer Vision Lab', icon: Eye },
  { id: 'pe-lab', label: 'Prompt Engineering Lab', icon: BookOpen },
  { id: 'compare', label: 'Prompt Comparison', icon: GitCompare },
  { id: 'teach', label: 'Teach Mode', icon: GraduationCap },
  { id: 'research', label: 'Research & Evaluation', icon: BarChart3 },
  { id: 'history', label: 'Experiment History', icon: History },
  { id: 'models', label: 'Model Manager', icon: Server },
  { id: 'about', label: 'About Project', icon: Info },
];

export default function Sidebar({ activePage, onSelectPage }) {
  return (
    <aside style={{
      width: '260px',
      background: 'var(--bg-card)',
      borderRight: '1px solid var(--border-color)',
      display: 'flex',
      flexDirection: 'column',
      flexShrink: 0,
    }}>
      <div style={{ padding: '20px 16px 12px 16px' }}>
        <p style={{
          fontSize: '0.72rem',
          fontWeight: 700,
          textTransform: 'uppercase',
          letterSpacing: '0.08em',
          color: 'var(--text-dim)',
          paddingLeft: '12px',
          marginBottom: '8px'
        }}>
          Research System
        </p>
        <nav style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            const isActive = activePage === item.id;
            
            return (
              <button
                key={item.id}
                onClick={() => onSelectPage(item.id)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '10px 14px',
                  borderRadius: 'var(--radius-md)',
                  background: isActive 
                    ? 'rgba(59, 130, 246, 0.15)' 
                    : item.highlight 
                      ? 'rgba(99, 102, 241, 0.08)' 
                      : 'transparent',
                  color: isActive ? '#60A5FA' : item.highlight ? '#A5B4FC' : 'var(--text-muted)',
                  border: isActive 
                    ? '1px solid rgba(59, 130, 246, 0.3)' 
                    : item.highlight 
                      ? '1px solid rgba(99, 102, 241, 0.2)' 
                      : '1px solid transparent',
                  textAlign: 'left',
                  fontSize: '0.88rem',
                  fontWeight: isActive ? 600 : 500,
                  width: '100%',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <Icon size={18} color={isActive ? '#60A5FA' : item.highlight ? '#818CF8' : 'currentColor'} />
                  <span>{item.label}</span>
                </div>
                {isActive && <ChevronRight size={14} />}
              </button>
            );
          })}
        </nav>
      </div>

      <div style={{ marginTop: 'auto', padding: '16px', borderTop: '1px solid var(--border-color)' }}>
        <div style={{
          background: 'var(--bg-main)',
          padding: '12px',
          borderRadius: 'var(--radius-md)',
          border: '1px solid var(--border-color)',
          fontSize: '0.75rem',
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
            <span style={{ color: 'var(--text-dim)' }}>Project:</span>
            <span style={{ color: 'var(--text-muted)', fontWeight: 600 }}>B.Tech AI & ML</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
            <span style={{ color: 'var(--text-dim)' }}>Target HW:</span>
            <span style={{ color: '#E2E8F0', fontFamily: 'var(--font-mono)' }}>i5-1235U (16GB)</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span style={{ color: 'var(--text-dim)' }}>Execution:</span>
            <span style={{ color: 'var(--accent-green)', fontWeight: 600 }}>Local CPU / Ollama</span>
          </div>
        </div>
      </div>
    </aside>
  );
}
