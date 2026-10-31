import React, { useState, useEffect } from 'react';
import { 
  Upload, 
  Image as ImageIcon, 
  CheckCircle, 
  Layers, 
  Settings, 
  Play, 
  Loader2, 
  ChevronRight, 
  ChevronLeft,
  Sparkles,
  Info,
  Check,
  Cpu,
  AlertTriangle
} from 'lucide-react';
import { 
  uploadImage, 
  getCVOperations, 
  processCV, 
  generatePrompts, 
  runExperiment,
  getFullImageUrl 
} from '../services/api';

const OBJECTIVES = [
  { id: 'Summarise', title: 'Summarise', desc: 'Synthesizes primary visual elements into a clear, high-level overview.' },
  { id: 'Analyse', title: 'Analyse', desc: 'Decomposes visual components, spatial geometry, and structural relationships.' },
  { id: 'Evaluate', title: 'Evaluate', desc: 'Critically appraises image quality, composition, fidelity, and limitations.' },
  { id: 'Explain', title: 'Explain', desc: 'Step-by-step educational breakdown of concepts and visual phenomena.' },
  { id: 'Teach', title: 'Teach', desc: 'Pedagogical instruction with definitions, analogies, and learning checkpoints.' },
];

export default function NewExperiment({ onNavigate, currentModel, onExperimentCompleted }) {
  const [step, setStep] = useState(1);
  
  // Step 1: Image
  const [file, setFile] = useState(null);
  const [imageMeta, setImageMeta] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState(null);
  
  // Step 2: Objective
  const [selectedObjective, setSelectedObjective] = useState('Analyse');
  
  // Step 3: CV Operations
  const [cvCatalog, setCvCatalog] = useState(null);
  const [selectedOps, setSelectedOps] = useState(['canny_edges', 'contour_extraction']);
  const [opParams, setOpParams] = useState({});
  const [cvRunning, setCvRunning] = useState(false);
  const [cvResults, setCvResults] = useState(null);
  
  // Step 4: Preferences
  const [preferences, setPreferences] = useState({
    audience: 'Student',
    tone: 'Professional',
    output_format: 'Structured report',
    length: 'Medium',
    few_shot_setting: 'zero-shot',
    include_examples: true,
    explain_terms: true,
    include_limitations: true,
    include_uncertainty: true,
    include_visual_evidence: true,
    compare_interpretations: false,
    advanced_instructions: ''
  });
  
  // Step 5: Prompts & Run
  const [generatedPrompts, setGeneratedPrompts] = useState(null);
  const [generatingPrompts, setGeneratingPrompts] = useState(false);
  const [selectedModel, setSelectedModel] = useState(currentModel || 'qwen2.5vl:3b');
  const [experimentTitle, setExperimentTitle] = useState('');
  const [executingExperiment, setExecutingExperiment] = useState(false);
  const [executionStatus, setExecutionStatus] = useState('');
  const [executionError, setExecutionError] = useState(null);

  useEffect(() => {
    getCVOperations().then(setCvCatalog).catch(console.error);
  }, []);

  useEffect(() => {
    if (currentModel) setSelectedModel(currentModel);
  }, [currentModel]);

  // Handle Image Upload
  async function handleFileChange(e) {
    const selectedFile = e.target.files[0];
    if (!selectedFile) return;
    setFile(selectedFile);
    setUploading(true);
    setUploadError(null);
    try {
      const meta = await uploadImage(selectedFile);
      setImageMeta(meta);
      setExperimentTitle(`${selectedObjective} - ${meta.filename}`);
    } catch (err) {
      setUploadError(err.message);
    } finally {
      setUploading(false);
    }
  }

  // Toggle CV Operation Selection
  function toggleOp(opId) {
    if (selectedOps.includes(opId)) {
      setSelectedOps(selectedOps.filter(id => id !== opId));
    } else {
      setSelectedOps([...selectedOps, opId]);
    }
  }

  // Execute CV Processing
  async function handleRunCV() {
    if (!imageMeta) return;
    setCvRunning(true);
    try {
      const opsPayload = selectedOps.map(id => ({
        id,
        params: opParams[id] || {}
      }));
      const res = await processCV({
        image_id: imageMeta.image_id,
        operations: opsPayload
      });
      setCvResults(res);
    } catch (err) {
      alert(`CV Error: ${err.message}`);
    } finally {
      setCvRunning(false);
    }
  }

  // Generate Prompts when reaching Step 5
  async function prepareStep5() {
    setGeneratingPrompts(true);
    try {
      const res = await generatePrompts({
        image_id: imageMeta.image_id,
        objective: selectedObjective,
        preferences,
        cv_metadata: cvResults?.aggregated_metadata || {}
      });
      setGeneratedPrompts(res);
      setStep(5);
    } catch (err) {
      alert(`Prompt Generation Error: ${err.message}`);
    } finally {
      setGeneratingPrompts(false);
    }
  }

  // Launch Full Sequential Multimodal Experiment
  async function handleExecuteRun() {
    setExecutingExperiment(true);
    setExecutionError(null);
    setExecutionStatus('Starting sequential execution on local VLM (strictly 1 model loaded)...');
    
    try {
      setExecutionStatus('Running Strategy 1 (Basic Prompting)...');
      
      const payload = {
        title: experimentTitle || `${selectedObjective} Experiment`,
        image_id: imageMeta.image_id,
        objective: selectedObjective,
        cv_operations: selectedOps.map(id => ({ id, params: opParams[id] || {} })),
        preferences,
        model: selectedModel,
        strategies_to_run: ['basic', 'costar', 'ai_optimized']
      };

      const res = await runExperiment(payload);
      setExecutionStatus('Inference completed! Saving experiment and evaluating metrics...');
      
      if (onExperimentCompleted) {
        onExperimentCompleted(res.experiment_id, res);
      }
      onNavigate('compare');
    } catch (err) {
      setExecutionError(err.message);
    } finally {
      setExecutingExperiment(false);
    }
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Wizard Progress Stepper */}
      <div className="card" style={{ padding: '16px 24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          {[
            { n: 1, label: '1. Upload Image' },
            { n: 2, label: '2. Select Objective' },
            { n: 3, label: '3. CV Processing' },
            { n: 4, label: '4. Preferences' },
            { n: 5, label: '5. Benchmark & Run' },
          ].map(s => (
            <div 
              key={s.n} 
              style={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: '8px',
                color: step === s.n ? 'var(--accent-blue)' : step > s.n ? 'var(--accent-green)' : 'var(--text-dim)',
                fontWeight: step === s.n ? 700 : 500,
                fontSize: '0.88rem'
              }}
            >
              <div style={{
                width: '28px',
                height: '28px',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                background: step === s.n ? 'rgba(59, 130, 246, 0.2)' : step > s.n ? 'rgba(16, 185, 129, 0.2)' : 'var(--bg-main)',
                border: `1px solid ${step === s.n ? 'var(--accent-blue)' : step > s.n ? 'var(--accent-green)' : 'var(--border-color)'}`,
                color: step === s.n ? '#60A5FA' : step > s.n ? '#34D399' : 'var(--text-dim)',
                fontSize: '0.75rem',
                fontWeight: 700
              }}>
                {step > s.n ? <Check size={14} /> : s.n}
              </div>
              <span>{s.label}</span>
            </div>
          ))}
        </div>
      </div>

      {/* STEP 1: Upload Image */}
      {step === 1 && (
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 700 }}>Step 1: Upload Input Image</h3>
            <p style={{ color: 'var(--text-dim)', fontSize: '0.85rem' }}>
              Select a photograph, chart, diagram, or grayscale image (JPG, PNG, WEBP).
            </p>
          </div>

          <div 
            style={{
              border: '2px dashed var(--border-color)',
              borderRadius: 'var(--radius-lg)',
              padding: '40px',
              textAlign: 'center',
              background: 'var(--bg-main)',
              cursor: 'pointer',
              position: 'relative'
            }}
            onClick={() => document.getElementById('file-upload-input').click()}
          >
            <input 
              id="file-upload-input"
              type="file" 
              accept=".jpg,.jpeg,.png,.webp,.bmp" 
              onChange={handleFileChange}
              style={{ display: 'none' }}
            />
            {uploading ? (
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '10px' }}>
                <Loader2 size={32} className="spin" color="var(--accent-blue)" />
                <p>Decoding image and extracting dimensions...</p>
              </div>
            ) : imageMeta ? (
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '24px' }}>
                <img 
                  src={getFullImageUrl(imageMeta.url)} 
                  alt="Uploaded preview" 
                  style={{ maxHeight: '200px', maxWidth: '300px', borderRadius: '8px', objectFit: 'contain', border: '1px solid var(--border-color)' }}
                />
                <div style={{ textAlign: 'left' }}>
                  <h4 style={{ fontSize: '1.1rem', fontWeight: 700 }}>{imageMeta.filename}</h4>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', marginTop: '10px', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                    <span>Dimensions: <strong style={{ color: '#fff' }}>{imageMeta.width} x {imageMeta.height} px</strong></span>
                    <span>Channels: <strong style={{ color: '#fff' }}>{imageMeta.channels} ({imageMeta.format})</strong></span>
                    <span>File Size: <strong style={{ color: '#fff' }}>{imageMeta.file_size_kb} KB</strong></span>
                    <span className="badge badge-green" style={{ width: 'fit-content', marginTop: '6px' }}>Ready for CV Engine</span>
                  </div>
                </div>
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '12px' }}>
                <div style={{ width: '56px', height: '56px', borderRadius: '50%', background: 'rgba(59, 130, 246, 0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Upload size={28} color="var(--accent-blue)" />
                </div>
                <h4 style={{ fontSize: '1.05rem', fontWeight: 600 }}>Click or Drag Image to Upload</h4>
                <p style={{ color: 'var(--text-dim)', fontSize: '0.8rem' }}>Supports JPG, JPEG, PNG, WEBP up to 15 MB</p>
              </div>
            )}
          </div>

          {uploadError && (
            <div style={{ color: 'var(--accent-red)', fontSize: '0.85rem' }}>{uploadError}</div>
          )}

          <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '12px' }}>
            <button 
              className="btn-primary" 
              disabled={!imageMeta || uploading}
              onClick={() => setStep(2)}
              style={{ opacity: !imageMeta ? 0.5 : 1 }}
            >
              Next: Select Objective <ChevronRight size={16} />
            </button>
          </div>
        </div>
      )}

      {/* STEP 2: Select Objective */}
      {step === 2 && (
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 700 }}>Step 2: Select Research Objective</h3>
            <p style={{ color: 'var(--text-dim)', fontSize: '0.85rem' }}>
              Choose what you want the system to do. The user does not need to manually write prompt text.
            </p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px' }}>
            {OBJECTIVES.map((obj) => {
              const isSelected = selectedObjective === obj.id;
              return (
                <div 
                  key={obj.id}
                  onClick={() => setSelectedObjective(obj.id)}
                  style={{
                    padding: '20px',
                    borderRadius: 'var(--radius-lg)',
                    background: isSelected ? 'rgba(59, 130, 246, 0.12)' : 'var(--bg-main)',
                    border: `2px solid ${isSelected ? 'var(--accent-blue)' : 'var(--border-color)'}`,
                    cursor: 'pointer',
                    transition: 'all 0.2s',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '8px'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <h4 style={{ fontSize: '1.1rem', fontWeight: 700, color: isSelected ? '#60A5FA' : 'var(--text-main)' }}>
                      {obj.title}
                    </h4>
                    {isSelected && <CheckCircle size={18} color="var(--accent-blue)" />}
                  </div>
                  <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', lineHeight: 1.5 }}>
                    {obj.desc}
                  </p>
                </div>
              );
            })}
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '12px' }}>
            <button className="btn-secondary" onClick={() => setStep(1)}>
              <ChevronLeft size={16} /> Back
            </button>
            <button className="btn-primary" onClick={() => setStep(3)}>
              Next: Select CV Operations <ChevronRight size={16} />
            </button>
          </div>
        </div>
      )}

      {/* STEP 3: Select Computer Vision Operations */}
      {step === 3 && (
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <h3 style={{ fontSize: '1.2rem', fontWeight: 700 }}>Step 3: Select Computer Vision Operations</h3>
              <p style={{ color: 'var(--text-dim)', fontSize: '0.85rem' }}>
                Select compatible operations from the 5 CV modules. Algorithms run in Python using OpenCV, NumPy, and scikit-image.
              </p>
            </div>
            <button 
              className="btn-primary" 
              onClick={handleRunCV}
              disabled={cvRunning || selectedOps.length === 0}
              style={{ fontSize: '0.85rem', padding: '8px 16px' }}
            >
              {cvRunning ? <Loader2 size={16} className="spin" /> : <Play size={16} />}
              Execute CV Pre-Processing
            </button>
          </div>

          {/* Module Operation Groups */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {cvCatalog && Object.values(cvCatalog).map((mod) => (
              <div 
                key={mod.id}
                style={{
                  background: 'var(--bg-main)',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--border-color)',
                  padding: '16px'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
                  <Layers size={16} color="var(--accent-cyan)" />
                  <strong style={{ fontSize: '0.95rem' }}>{mod.title}</strong>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>• {mod.syllabus}</span>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '10px' }}>
                  {mod.operations.map((op) => {
                    const isChecked = selectedOps.includes(op.id);
                    return (
                      <div 
                        key={op.id}
                        onClick={() => toggleOp(op.id)}
                        style={{
                          display: 'flex',
                          alignItems: 'flex-start',
                          gap: '10px',
                          padding: '10px 12px',
                          borderRadius: 'var(--radius-sm)',
                          background: isChecked ? 'rgba(59, 130, 246, 0.1)' : 'var(--bg-card)',
                          border: `1px solid ${isChecked ? 'rgba(59, 130, 246, 0.4)' : 'var(--border-color)'}`,
                          cursor: 'pointer',
                        }}
                      >
                        <input 
                          type="checkbox" 
                          checked={isChecked} 
                          onChange={() => {}} 
                          style={{ marginTop: '3px', cursor: 'pointer' }}
                        />
                        <div>
                          <strong style={{ fontSize: '0.85rem', color: isChecked ? '#93C5FD' : 'var(--text-main)' }}>
                            {op.name}
                          </strong>
                          <p style={{ fontSize: '0.72rem', color: 'var(--text-dim)', marginTop: '2px' }}>
                            {op.description}
                          </p>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>

          {/* CV Results Preview */}
          {cvResults && (
            <div style={{ marginTop: '16px', padding: '16px', background: 'rgba(16, 185, 129, 0.05)', border: '1px solid rgba(16, 185, 129, 0.3)', borderRadius: 'var(--radius-md)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
                <CheckCircle size={18} color="var(--accent-green)" />
                <strong style={{ color: '#34D399', fontSize: '0.95rem' }}>CV Operations Executed Successfully</strong>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '12px' }}>
                {cvResults.results.map((r, i) => (
                  <div key={i} style={{ background: 'var(--bg-main)', borderRadius: '6px', padding: '10px', border: '1px solid var(--border-color)' }}>
                    {r.processed_image_url && (
                      <img 
                        src={getFullImageUrl(r.processed_image_url)} 
                        alt={r.operation_name}
                        style={{ width: '100%', height: '120px', objectFit: 'cover', borderRadius: '4px', marginBottom: '8px' }}
                      />
                    )}
                    <strong style={{ fontSize: '0.8rem' }}>{r.operation_name}</strong>
                    <p style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>Time: {r.execution_time_ms} ms</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '12px' }}>
            <button className="btn-secondary" onClick={() => setStep(2)}>
              <ChevronLeft size={16} /> Back
            </button>
            <button className="btn-primary" onClick={() => setStep(4)}>
              Next: Structured Preferences <ChevronRight size={16} />
            </button>
          </div>
        </div>
      )}

      {/* STEP 4: Structured Preferences (MCQs) */}
      {step === 4 && (
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 700 }}>Step 4: Collect Structured Preferences</h3>
            <p style={{ color: 'var(--text-dim)', fontSize: '0.85rem' }}>
              Select target audience, tone, format, and depth through structured options.
            </p>
          </div>

          <div className="grid-2">
            <div>
              <label style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)' }}>Target Audience</label>
              <select 
                value={preferences.audience}
                onChange={e => setPreferences({...preferences, audience: e.target.value})}
                style={{ width: '100%', marginTop: '6px' }}
              >
                {['Beginner', 'Student', 'Intermediate', 'Expert', 'Researcher'].map(opt => (
                  <option key={opt} value={opt}>{opt}</option>
                ))}
              </select>
            </div>

            <div>
              <label style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)' }}>Tone & Voice</label>
              <select 
                value={preferences.tone}
                onChange={e => setPreferences({...preferences, tone: e.target.value})}
                style={{ width: '100%', marginTop: '6px' }}
              >
                {['Simple', 'Professional', 'Academic', 'Technical'].map(opt => (
                  <option key={opt} value={opt}>{opt}</option>
                ))}
              </select>
            </div>

            <div>
              <label style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)' }}>Output Format</label>
              <select 
                value={preferences.output_format}
                onChange={e => setPreferences({...preferences, output_format: e.target.value})}
                style={{ width: '100%', marginTop: '6px' }}
              >
                {['Structured report', 'Bullet points', 'Paragraph', 'Step-by-step', 'Table'].map(opt => (
                  <option key={opt} value={opt}>{opt}</option>
                ))}
              </select>
            </div>

            <div>
              <label style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)' }}>Response Length</label>
              <select 
                value={preferences.length}
                onChange={e => setPreferences({...preferences, length: e.target.value})}
                style={{ width: '100%', marginTop: '6px' }}
              >
                {['Short', 'Medium', 'Detailed'].map(opt => (
                  <option key={opt} value={opt}>{opt}</option>
                ))}
              </select>
            </div>

            <div>
              <label style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)' }}>Strategy 2 Setting (CO-STAR)</label>
              <select 
                value={preferences.few_shot_setting}
                onChange={e => setPreferences({...preferences, few_shot_setting: e.target.value})}
                style={{ width: '100%', marginTop: '6px' }}
              >
                <option value="zero-shot">Zero-shot (Direct framework prompt)</option>
                <option value="one-shot">One-shot (Include 1 reference exemplar)</option>
                <option value="few-shot">Few-shot (Include 2 reference exemplars)</option>
              </select>
            </div>
          </div>

          {/* Checkbox Toggles */}
          <div style={{ marginTop: '12px' }}>
            <label style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '8px', display: 'block' }}>
              Additional Methodological Preferences
            </label>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '10px' }}>
              {[
                { key: 'include_examples', label: 'Include concrete examples' },
                { key: 'explain_terms', label: 'Define technical terminology' },
                { key: 'include_limitations', label: 'Explicitly state visual limitations' },
                { key: 'include_uncertainty', label: 'Flag low-confidence visual areas' },
                { key: 'include_visual_evidence', label: 'Anchor claims to visual evidence' },
                { key: 'compare_interpretations', label: 'Compare alternative interpretations' },
              ].map(chk => (
                <label 
                  key={chk.key} 
                  style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.82rem', cursor: 'pointer', padding: '8px 10px', background: 'var(--bg-main)', borderRadius: '6px', border: '1px solid var(--border-color)' }}
                >
                  <input 
                    type="checkbox"
                    checked={preferences[chk.key]}
                    onChange={e => setPreferences({...preferences, [chk.key]: e.target.checked})}
                  />
                  <span>{chk.label}</span>
                </label>
              ))}
            </div>
          </div>

          <div>
            <label style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)' }}>Optional Advanced Instructions</label>
            <input 
              type="text" 
              placeholder="e.g. Focus specifically on the top-right quadrant or color saturation"
              value={preferences.advanced_instructions}
              onChange={e => setPreferences({...preferences, advanced_instructions: e.target.value})}
              style={{ width: '100%', marginTop: '6px' }}
            />
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '12px' }}>
            <button className="btn-secondary" onClick={() => setStep(3)}>
              <ChevronLeft size={16} /> Back
            </button>
            <button 
              className="btn-primary" 
              onClick={prepareStep5}
              disabled={generatingPrompts}
            >
              {generatingPrompts ? <Loader2 size={16} className="spin" /> : null}
              Next: Generate Prompts & Review <ChevronRight size={16} />
            </button>
          </div>
        </div>
      )}

      {/* STEP 5: Review & Run Benchmark */}
      {step === 5 && (
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 700 }}>Step 5: Review Prompts & Execute Benchmark</h3>
            <p style={{ color: 'var(--text-dim)', fontSize: '0.85rem' }}>
              All three strategies will be executed on the SAME selected Vision-Language Model sequentially.
            </p>
          </div>

          {/* Model Selection and Title */}
          <div className="grid-2">
            <div>
              <label style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)' }}>Experiment Title</label>
              <input 
                type="text"
                value={experimentTitle}
                onChange={e => setExperimentTitle(e.target.value)}
                style={{ width: '100%', marginTop: '6px' }}
              />
            </div>
            <div>
              <label style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)' }}>Selected Vision-Language Model</label>
              <select 
                value={selectedModel}
                onChange={e => setSelectedModel(e.target.value)}
                style={{ width: '100%', marginTop: '6px' }}
              >
                <option value="qwen2.5vl:3b">qwen2.5vl:3b (Recommended for 16GB CPU)</option>
                <option value="qwen3-vl:8b">qwen3-vl:8b (Advanced - Higher RAM requirement)</option>
              </select>
            </div>
          </div>

          {/* Notice Banner */}
          <div style={{ padding: '12px 16px', background: 'rgba(59, 130, 246, 0.08)', borderRadius: 'var(--radius-md)', border: '1px solid rgba(59, 130, 246, 0.3)', display: 'flex', gap: '10px' }}>
            <Info size={20} color="var(--accent-blue)" style={{ flexShrink: 0, marginTop: '2px' }} />
            <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)', lineHeight: 1.5 }}>
              <strong style={{ color: '#93C5FD' }}>Hardware-Safe Sequential Execution: </strong>
              To prevent RAM exhaustion on Intel Core i5 with 16GB, inferences are queued with an internal lock. Only 1 model instance is loaded at any time.
            </div>
          </div>

          {/* 3 Generated Prompts Preview */}
          {generatedPrompts && (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '14px', marginTop: '8px' }}>
              <div style={{ background: 'var(--bg-main)', padding: '14px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)', display: 'flex', flexDirection: 'column' }}>
                <span className="badge badge-gray" style={{ width: 'fit-content', marginBottom: '8px' }}>Strategy 1: Basic</span>
                <pre style={{ fontSize: '0.75rem', color: 'var(--text-muted)', whiteSpace: 'pre-wrap', maxHeight: '200px', overflowY: 'auto' }}>
                  {generatedPrompts.basic_prompt}
                </pre>
              </div>

              <div style={{ background: 'var(--bg-main)', padding: '14px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)', display: 'flex', flexDirection: 'column' }}>
                <span className="badge badge-blue" style={{ width: 'fit-content', marginBottom: '8px' }}>Strategy 2: CO-STAR</span>
                <pre style={{ fontSize: '0.75rem', color: 'var(--text-muted)', whiteSpace: 'pre-wrap', maxHeight: '200px', overflowY: 'auto' }}>
                  {generatedPrompts.costar_prompt}
                </pre>
              </div>

              <div style={{ background: 'var(--bg-main)', padding: '14px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)', display: 'flex', flexDirection: 'column' }}>
                <span className="badge badge-purple" style={{ width: 'fit-content', marginBottom: '8px' }}>Strategy 3: AI-Optimized</span>
                <pre style={{ fontSize: '0.75rem', color: 'var(--text-muted)', whiteSpace: 'pre-wrap', maxHeight: '200px', overflowY: 'auto' }}>
                  {generatedPrompts.ai_optimized_prompt}
                </pre>
              </div>
            </div>
          )}

          {/* Execution Progress & Status */}
          {executingExperiment && (
            <div style={{ padding: '20px', background: 'rgba(59, 130, 246, 0.1)', border: '1px solid var(--accent-blue)', borderRadius: 'var(--radius-md)', textAlign: 'center' }}>
              <Loader2 size={32} className="spin" color="var(--accent-blue)" style={{ margin: '0 auto 12px auto' }} />
              <h4 style={{ fontSize: '1rem', fontWeight: 700 }}>Executing Multimodal Experiment...</h4>
              <p style={{ color: 'var(--accent-cyan)', fontSize: '0.85rem', marginTop: '6px' }}>{executionStatus}</p>
              <p style={{ color: 'var(--text-dim)', fontSize: '0.75rem', marginTop: '4px' }}>
                Running CPU inference through Ollama ({selectedModel}). This typically takes 10-30 seconds per strategy.
              </p>
            </div>
          )}

          {executionError && (
            <div style={{ padding: '14px', background: 'rgba(239, 68, 68, 0.15)', border: '1px solid var(--accent-red)', borderRadius: 'var(--radius-md)', color: '#FCA5A5', fontSize: '0.85rem' }}>
              <AlertTriangle size={18} style={{ display: 'inline', marginRight: '6px' }} />
              <strong>Error:</strong> {executionError}
            </div>
          )}

          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '12px' }}>
            <button className="btn-secondary" onClick={() => setStep(4)} disabled={executingExperiment}>
              <ChevronLeft size={16} /> Back
            </button>
            <button 
              className="btn-primary" 
              onClick={handleExecuteRun}
              disabled={executingExperiment}
            >
              {executingExperiment ? <Loader2 size={16} className="spin" /> : <Play size={16} />}
              Launch 3-Strategy Experiment
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
