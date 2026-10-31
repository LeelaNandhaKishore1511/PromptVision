import React, { useState, useEffect } from 'react';
import { 
  Eye, 
  Upload, 
  Play, 
  Loader2, 
  Sliders, 
  Layers, 
  CheckCircle, 
  Info,
  Maximize2
} from 'lucide-react';
import { getCVOperations, processCV, uploadImage, getFullImageUrl } from '../services/api';

export default function CVLab() {
  const [catalog, setCatalog] = useState(null);
  const [selectedModule, setSelectedModule] = useState('module1');
  const [selectedOp, setSelectedOp] = useState('rgb_grayscale');
  const [params, setParams] = useState({});
  
  // Images
  const [primaryImage, setPrimaryImage] = useState(null);
  const [secondaryImage, setSecondaryImage] = useState(null);
  const [uploading, setUploading] = useState(false);
  
  // Results
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    getCVOperations().then(cat => {
      setCatalog(cat);
      if (cat && cat.module1 && cat.module1.operations.length > 0) {
        setSelectedOp(cat.module1.operations[0].id);
      }
    }).catch(console.error);
  }, []);

  // Update default params when operation changes
  useEffect(() => {
    if (!catalog || !catalog[selectedModule]) return;
    const opDef = catalog[selectedModule].operations.find(o => o.id === selectedOp);
    if (opDef && opDef.parameters) {
      const initial = {};
      opDef.parameters.forEach(p => {
        initial[p.name] = p.default;
      });
      setParams(initial);
    }
  }, [selectedModule, selectedOp, catalog]);

  async function handlePrimaryUpload(e) {
    const f = e.target.files[0];
    if (!f) return;
    setUploading(true);
    setError(null);
    try {
      const meta = await uploadImage(f);
      setPrimaryImage(meta);
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  }

  async function handleSecondaryUpload(e) {
    const f = e.target.files[0];
    if (!f) return;
    try {
      const meta = await uploadImage(f);
      setSecondaryImage(meta);
    } catch (err) {
      alert(err.message);
    }
  }

  async function handleExecute() {
    if (!primaryImage) {
      alert('Please upload an image first.');
      return;
    }
    setRunning(true);
    setError(null);
    try {
      const payload = {
        image_id: primaryImage.image_id,
        operations: [{ id: selectedOp, params }],
        second_image_id: secondaryImage?.image_id || null
      };
      const res = await processCV(payload);
      if (res.results && res.results.length > 0) {
        setResult(res.results[0]);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setRunning(false);
    }
  }

  const currentModObj = catalog ? catalog[selectedModule] : null;
  const currentOpObj = currentModObj ? currentModObj.operations.find(o => o.id === selectedOp) : null;
  const requiresSecondImage = ['template_matching', 'orb_matching', 'orb_registration', 'optical_flow'].includes(selectedOp);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span className="badge badge-cyan">Syllabus Engine</span>
            <h2 style={{ fontSize: '1.4rem', fontWeight: 800 }}>Computer Vision Interactive Laboratory</h2>
          </div>
          <p style={{ color: 'var(--text-dim)', fontSize: '0.85rem', marginTop: '4px' }}>
            Real-time execution of all 5 syllabus modules with OpenCV, NumPy, SciPy, and scikit-image.
          </p>
        </div>
      </div>

      {/* Module Selector Tabs */}
      <div style={{ display: 'flex', gap: '8px', overflowX: 'auto', paddingBottom: '4px' }}>
        {catalog && Object.values(catalog).map((m) => {
          const isActive = selectedModule === m.id;
          return (
            <button
              key={m.id}
              onClick={() => {
                setSelectedModule(m.id);
                if (m.operations && m.operations.length > 0) {
                  setSelectedOp(m.operations[0].id);
                }
              }}
              style={{
                padding: '10px 16px',
                borderRadius: 'var(--radius-md)',
                background: isActive ? 'var(--accent-blue)' : 'var(--bg-card)',
                color: isActive ? '#fff' : 'var(--text-muted)',
                fontWeight: 600,
                fontSize: '0.82rem',
                border: `1px solid ${isActive ? 'var(--accent-blue)' : 'var(--border-color)'}`,
                whiteSpace: 'nowrap'
              }}
            >
              {m.title}
            </button>
          );
        })}
      </div>

      {/* Main Workspace Layout */}
      <div style={{ display: 'grid', gridTemplateColumns: '320px 1fr', gap: '24px' }}>
        {/* Left Column: Operation Selection & Parameters */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {/* Operations List */}
          <div className="card" style={{ padding: '16px' }}>
            <h4 style={{ fontSize: '0.88rem', fontWeight: 700, marginBottom: '12px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Select Algorithm
            </h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
              {currentModObj && currentModObj.operations.map((op) => {
                const isSelected = selectedOp === op.id;
                return (
                  <button
                    key={op.id}
                    onClick={() => setSelectedOp(op.id)}
                    style={{
                      textAlign: 'left',
                      padding: '8px 12px',
                      borderRadius: 'var(--radius-sm)',
                      background: isSelected ? 'rgba(59, 130, 246, 0.15)' : 'transparent',
                      color: isSelected ? '#60A5FA' : 'var(--text-main)',
                      border: isSelected ? '1px solid rgba(59, 130, 246, 0.3)' : '1px solid transparent',
                      fontSize: '0.82rem',
                      fontWeight: isSelected ? 600 : 500,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between'
                    }}
                  >
                    <span>{op.name}</span>
                    {isSelected && <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: '#60A5FA' }} />}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Interactive Parameters Panel */}
          {currentOpObj && (
            <div className="card" style={{ padding: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '12px' }}>
                <Sliders size={16} color="var(--accent-cyan)" />
                <h4 style={{ fontSize: '0.88rem', fontWeight: 700 }}>Parameters</h4>
              </div>

              {currentOpObj.parameters.length === 0 ? (
                <p style={{ fontSize: '0.78rem', color: 'var(--text-dim)' }}>
                  This operation uses analytical defaults based on image dimensions and channel structure.
                </p>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                  {currentOpObj.parameters.map((p) => (
                    <div key={p.name}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.78rem', marginBottom: '4px' }}>
                        <span style={{ color: 'var(--text-muted)' }}>{p.label}</span>
                        <strong style={{ color: 'var(--accent-cyan)', fontFamily: 'var(--font-mono)' }}>
                          {params[p.name]}
                        </strong>
                      </div>
                      {p.type === 'slider' && (
                        <input
                          type="range"
                          min={p.min}
                          max={p.max}
                          step={p.step || 1}
                          value={params[p.name] !== undefined ? params[p.name] : p.default}
                          onChange={e => setParams({...params, [p.name]: parseFloat(e.target.value)})}
                          style={{ width: '100%' }}
                        />
                      )}
                      {p.type === 'select' && (
                        <select
                          value={params[p.name] || p.default}
                          onChange={e => setParams({...params, [p.name]: e.target.value})}
                          style={{ width: '100%', fontSize: '0.8rem' }}
                        >
                          {p.options.map(opt => (
                            <option key={opt} value={opt}>{opt}</option>
                          ))}
                        </select>
                      )}
                    </div>
                  ))}
                </div>
              )}

              {/* Second Image Upload if Operation requires pair */}
              {requiresSecondImage && (
                <div style={{ marginTop: '16px', paddingTop: '12px', borderTop: '1px solid var(--border-color)' }}>
                  <label style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--accent-amber)', display: 'block', marginBottom: '6px' }}>
                    Optional 2nd Image (Template / Target)
                  </label>
                  <input type="file" accept="image/*" onChange={handleSecondaryUpload} style={{ fontSize: '0.75rem', width: '100%' }} />
                  {secondaryImage && (
                    <p style={{ fontSize: '0.72rem', color: 'var(--accent-green)', marginTop: '4px' }}>
                      Attached: {secondaryImage.filename}
                    </p>
                  )}
                  <p style={{ fontSize: '0.7rem', color: 'var(--text-dim)', marginTop: '4px' }}>
                    If omitted, the algorithm automatically extracts a central patch or synthetically rotates the image.
                  </p>
                </div>
              )}

              {/* Run Button */}
              <button
                className="btn-primary"
                onClick={handleExecute}
                disabled={running || !primaryImage}
                style={{ width: '100%', marginTop: '16px', justifyContent: 'center' }}
              >
                {running ? <Loader2 size={16} className="spin" /> : <Play size={16} />}
                Execute Operation
              </button>
            </div>
          )}
        </div>

        {/* Right Column: Visualizer & Metadata */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {/* Upload Dropzone if no image yet */}
          {!primaryImage ? (
            <div 
              className="card"
              style={{
                padding: '48px 24px',
                textAlign: 'center',
                border: '2px dashed var(--border-color)',
                background: 'var(--bg-main)',
                cursor: 'pointer'
              }}
              onClick={() => document.getElementById('lab-file-input').click()}
            >
              <input id="lab-file-input" type="file" accept="image/*" onChange={handlePrimaryUpload} style={{ display: 'none' }} />
              <div style={{ width: '56px', height: '56px', borderRadius: '50%', background: 'rgba(59, 130, 246, 0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 12px auto' }}>
                <Upload size={28} color="var(--accent-blue)" />
              </div>
              <h4 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Upload an Image to Begin Laboratory Analysis</h4>
              <p style={{ color: 'var(--text-dim)', fontSize: '0.85rem', marginTop: '6px' }}>
                Load any visual photograph, chart, or diagram to benchmark CV operations
              </p>
            </div>
          ) : (
            <div className="card" style={{ padding: '20px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
                <div>
                  <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>{currentOpObj?.name}</h3>
                  <p style={{ fontSize: '0.8rem', color: 'var(--text-dim)' }}>{currentOpObj?.description}</p>
                </div>
                <div style={{ display: 'flex', gap: '8px' }}>
                  <button 
                    className="btn-secondary"
                    style={{ padding: '6px 12px', fontSize: '0.78rem' }}
                    onClick={() => document.getElementById('lab-file-input-change').click()}
                  >
                    Change Image
                  </button>
                  <input id="lab-file-input-change" type="file" accept="image/*" onChange={handlePrimaryUpload} style={{ display: 'none' }} />
                </div>
              </div>

              {/* Side-by-Side Comparison */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
                {/* Original */}
                <div style={{ background: 'var(--bg-main)', borderRadius: 'var(--radius-md)', padding: '12px', border: '1px solid var(--border-color)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-muted)' }}>Original Input</span>
                    <span style={{ fontSize: '0.72rem', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)' }}>
                      {primaryImage.width}x{primaryImage.height} ({primaryImage.channels}ch)
                    </span>
                  </div>
                  <img 
                    src={getFullImageUrl(primaryImage.url)} 
                    alt="Original" 
                    style={{ width: '100%', height: '280px', objectFit: 'contain', background: '#000', borderRadius: '4px' }}
                  />
                </div>

                {/* Processed Result */}
                <div style={{ background: 'var(--bg-main)', borderRadius: 'var(--radius-md)', padding: '12px', border: '1px solid var(--border-color)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span style={{ fontSize: '0.78rem', fontWeight: 600, color: '#34D399' }}>Processed Output</span>
                    {result && (
                      <span style={{ fontSize: '0.72rem', color: 'var(--accent-cyan)', fontFamily: 'var(--font-mono)' }}>
                        {result.execution_time_ms} ms
                      </span>
                    )}
                  </div>
                  {running ? (
                    <div style={{ width: '100%', height: '280px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '10px' }}>
                      <Loader2 size={32} className="spin" color="var(--accent-blue)" />
                      <p style={{ fontSize: '0.8rem', color: 'var(--text-dim)' }}>Executing {selectedOp}...</p>
                    </div>
                  ) : result && result.processed_image_url ? (
                    <img 
                      src={getFullImageUrl(result.processed_image_url)} 
                      alt="Processed" 
                      style={{ width: '100%', height: '280px', objectFit: 'contain', background: '#000', borderRadius: '4px' }}
                    />
                  ) : (
                    <div style={{ width: '100%', height: '280px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-dim)', fontSize: '0.85rem' }}>
                      Click 'Execute Operation' to run CV algorithm
                    </div>
                  )}
                </div>
              </div>

              {/* Extracted Metadata Inspection */}
              {result && result.metadata && (
                <div style={{ marginTop: '20px', padding: '16px', background: 'var(--bg-main)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
                    <CheckCircle size={16} color="var(--accent-green)" />
                    <strong style={{ fontSize: '0.88rem' }}>Extracted Computer Vision Metadata & Metrics</strong>
                  </div>
                  <pre style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)', background: 'rgba(0,0,0,0.3)', padding: '12px', borderRadius: '6px', overflowX: 'auto', maxHeight: '180px' }}>
                    {JSON.stringify(result.metadata, null, 2)}
                  </pre>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
