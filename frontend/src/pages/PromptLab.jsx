import React, { useState } from 'react';
import { 
  BookOpen, 
  Cpu, 
  Code2, 
  Layers, 
  ShieldCheck, 
  Sparkles, 
  HelpCircle,
  Copy,
  Check,
  CheckCircle2,
  ArrowRight
} from 'lucide-react';

const UNITS = [
  { id: 'unit1', title: 'Unit 1: Foundations of Prompt Engineering & LLMs', icon: Cpu },
  { id: 'unit2', title: 'Unit 2: Prompt Design Fundamentals & Anatomy', icon: Code2 },
  { id: 'unit3', title: 'Unit 3: Advanced Strategies & Prompt Chaining', icon: Layers },
  { id: 'unit4', title: 'Unit 4: Tools, LCEL & Multimodal Evaluation', icon: BookOpen },
  { id: 'unit5', title: 'Unit 5: Ethics, Uncertainty & Automated AI', icon: ShieldCheck },
];

export default function PromptLab() {
  const [activeUnit, setActiveUnit] = useState('unit1');
  
  // Unit 1 state: Tokenizer demo
  const [demoText, setDemoText] = useState('Computer Vision and Multimodal Prompt Engineering with local Ollama models on Windows.');
  
  // Unit 2 state: Anatomy Builder
  const [anatomy, setAnatomy] = useState({
    instruction: 'Analyse the architectural structure shown in this image.',
    context: 'Historical preservation and structural engineering assessment.',
    input: 'Photographic facade of Romanesque cathedral.',
    format: 'Bullet points with technical structural terms bolded.',
    constraints: 'Ground claims solely in visible masonry; state uncertainty for shadowed areas.'
  });
  
  // Unit 3 state: Prompt Chaining
  const [chainStep, setChainStep] = useState(1);
  
  // Unit 5 state: Guardrail check
  const [guardrailPrompt, setGuardrailPrompt] = useState(
    'Analyse the uploaded image. If visual details are blurred or occluded, state "[Visual Uncertainty]" rather than speculating. Do not fabricate unverified text or brand names.'
  );

  // Token calculations (BPE approximation)
  const charCount = demoText.length;
  const wordCount = demoText.trim() ? demoText.trim().split(/\s+/).length : 0;
  // Standard rule-of-thumb: ~4 characters or 0.75 words per token in English
  const tokenEstimate = Math.ceil(charCount / 3.8);
  const contextLimit = 4096;
  const contextPct = ((tokenEstimate / contextLimit) * 100).toFixed(2);

  // Check guardrails
  const hasUncertainty = guardrailPrompt.toLowerCase().includes('uncertain') || guardrailPrompt.toLowerCase().includes('not visible');
  const hasNegativeConstraint = guardrailPrompt.toLowerCase().includes('do not') || guardrailPrompt.toLowerCase().includes('never') || guardrailPrompt.toLowerCase().includes('avoid');
  const hasGrounding = guardrailPrompt.toLowerCase().includes('image') || guardrailPrompt.toLowerCase().includes('visible');

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Header */}
      <div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span className="badge badge-purple">Educational Lab</span>
          <h2 style={{ fontSize: '1.4rem', fontWeight: 800 }}>Prompt Engineering Learning Laboratory</h2>
        </div>
        <p style={{ color: 'var(--text-dim)', fontSize: '0.85rem', marginTop: '4px' }}>
          Comprehensive interactive exploration across all five Prompt Engineering syllabus units.
        </p>
      </div>

      {/* Unit Selector Tabs */}
      <div style={{ display: 'flex', gap: '8px', overflowX: 'auto', paddingBottom: '4px' }}>
        {UNITS.map(u => {
          const Icon = u.icon;
          const isActive = activeUnit === u.id;
          return (
            <button
              key={u.id}
              onClick={() => setActiveUnit(u.id)}
              style={{
                padding: '10px 16px',
                borderRadius: 'var(--radius-md)',
                background: isActive ? 'var(--accent-purple)' : 'var(--bg-card)',
                color: isActive ? '#fff' : 'var(--text-muted)',
                fontWeight: 600,
                fontSize: '0.82rem',
                border: `1px solid ${isActive ? 'var(--accent-purple)' : 'var(--border-color)'}`,
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                whiteSpace: 'nowrap'
              }}
            >
              <Icon size={16} />
              <span>{u.title}</span>
            </button>
          );
        })}
      </div>

      {/* UNIT 1: Foundations of Prompt Engineering & LLMs */}
      {activeUnit === 'unit1' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div className="card">
            <h3 style={{ fontSize: '1.15rem', fontWeight: 700, marginBottom: '6px' }}>
              Unit 1: How LLMs and Vision-Language Models Process Information
            </h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', lineHeight: 1.6 }}>
              Large Language Models do not read characters or whole sentences as humans do; they break text into discrete numerical identifiers called <strong>tokens</strong>. In Vision-Language Models (such as Qwen2.5-VL), images are similarly split into 2D patches and mapped into visual tokens in the same embedding space.
            </p>
          </div>

          {/* Interactive Tokenizer & Context Window Explorer */}
          <div className="grid-2">
            <div className="card">
              <h4 style={{ fontSize: '0.95rem', fontWeight: 700, marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Cpu size={16} color="var(--accent-cyan)" />
                Interactive Tokenizer Demonstration
              </h4>
              <p style={{ fontSize: '0.78rem', color: 'var(--text-dim)', marginBottom: '8px' }}>
                Type or paste prompt text to observe the critical difference between character count, word count, and token count:
              </p>
              <textarea
                rows={4}
                value={demoText}
                onChange={e => setDemoText(e.target.value)}
                style={{ width: '100%', fontSize: '0.85rem' }}
              />

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '10px', marginTop: '16px' }}>
                <div style={{ background: 'var(--bg-main)', padding: '10px', borderRadius: '6px', textAlign: 'center', border: '1px solid var(--border-color)' }}>
                  <p style={{ fontSize: '0.72rem', color: 'var(--text-dim)' }}>CHARACTERS</p>
                  <strong style={{ fontSize: '1.3rem', color: '#93C5FD' }}>{charCount}</strong>
                </div>
                <div style={{ background: 'var(--bg-main)', padding: '10px', borderRadius: '6px', textAlign: 'center', border: '1px solid var(--border-color)' }}>
                  <p style={{ fontSize: '0.72rem', color: 'var(--text-dim)' }}>WORDS</p>
                  <strong style={{ fontSize: '1.3rem', color: '#6EE7B7' }}>{wordCount}</strong>
                </div>
                <div style={{ background: 'var(--bg-main)', padding: '10px', borderRadius: '6px', textAlign: 'center', border: '1px solid var(--border-color)' }}>
                  <p style={{ fontSize: '0.72rem', color: 'var(--text-dim)' }}>ESTIMATED TOKENS</p>
                  <strong style={{ fontSize: '1.3rem', color: '#C084FC' }}>{tokenEstimate}</strong>
                </div>
              </div>
            </div>

            {/* Context Window Capacity */}
            <div className="card">
              <h4 style={{ fontSize: '0.95rem', fontWeight: 700, marginBottom: '12px' }}>
                Context Window (Attention Horizon)
              </h4>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', lineHeight: 1.5 }}>
                Local models allocate a fixed context buffer (default: <code>4096 tokens</code> in our Ollama config). This window holds both your visual prompt tokens and generated response tokens.
              </p>

              <div style={{ marginTop: '20px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.78rem', marginBottom: '6px' }}>
                  <span>Allocated Context Usage:</span>
                  <strong style={{ fontFamily: 'var(--font-mono)' }}>{tokenEstimate} / {contextLimit} ({contextPct}%)</strong>
                </div>
                <div style={{ width: '100%', height: '10px', background: 'var(--bg-main)', borderRadius: '999px', overflow: 'hidden', border: '1px solid var(--border-color)' }}>
                  <div style={{ width: `${Math.min(100, Math.max(2, contextPct * 10))}%`, height: '100%', background: 'linear-gradient(90deg, #3B82F6, #8B5CF6)' }} />
                </div>
              </div>

              <div style={{ marginTop: '20px', padding: '12px', background: 'var(--bg-main)', borderRadius: '6px', border: '1px solid var(--border-color)', fontSize: '0.78rem' }}>
                <strong style={{ color: 'var(--accent-amber)' }}>B.Tech Research Insight:</strong>
                <p style={{ color: 'var(--text-dim)', marginTop: '4px' }}>
                  Unnecessary verbose prompt padding consumes context window and increases CPU inference latency on Intel Core i5. Optimized structured prompts maximize informational density per token.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* UNIT 2: Prompt Design Fundamentals & Anatomy */}
      {activeUnit === 'unit2' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div className="card">
            <h3 style={{ fontSize: '1.15rem', fontWeight: 700, marginBottom: '6px' }}>
              Unit 2: The 5-Part Prompt Anatomy
            </h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', lineHeight: 1.6 }}>
              A rigorous engineering prompt consists of 5 foundational elements: Instruction, Context, Input, Output Format, and Constraints. In Strategy 1 (Basic Prompting), we enforce this structure without few-shot examples or iterative optimization.
            </p>
          </div>

          <div className="grid-2">
            {/* Interactive Anatomy Editor */}
            <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <h4 style={{ fontSize: '0.95rem', fontWeight: 700 }}>Interactive Anatomy Builder</h4>
              
              <div>
                <label style={{ fontSize: '0.75rem', fontWeight: 700, color: '#60A5FA' }}>1. INSTRUCTION (Primary Task)</label>
                <input 
                  type="text" 
                  value={anatomy.instruction} 
                  onChange={e => setAnatomy({...anatomy, instruction: e.target.value})}
                  style={{ width: '100%', marginTop: '4px', fontSize: '0.8rem' }}
                />
              </div>

              <div>
                <label style={{ fontSize: '0.75rem', fontWeight: 700, color: '#34D399' }}>2. CONTEXT (Domain / Background)</label>
                <input 
                  type="text" 
                  value={anatomy.context} 
                  onChange={e => setAnatomy({...anatomy, context: e.target.value})}
                  style={{ width: '100%', marginTop: '4px', fontSize: '0.8rem' }}
                />
              </div>

              <div>
                <label style={{ fontSize: '0.75rem', fontWeight: 700, color: '#FBBF24' }}>3. INPUT DATA (Visual Reference)</label>
                <input 
                  type="text" 
                  value={anatomy.input} 
                  onChange={e => setAnatomy({...anatomy, input: e.target.value})}
                  style={{ width: '100%', marginTop: '4px', fontSize: '0.8rem' }}
                />
              </div>

              <div>
                <label style={{ fontSize: '0.75rem', fontWeight: 700, color: '#C084FC' }}>4. OUTPUT FORMAT (Style & Structure)</label>
                <input 
                  type="text" 
                  value={anatomy.format} 
                  onChange={e => setAnatomy({...anatomy, format: e.target.value})}
                  style={{ width: '100%', marginTop: '4px', fontSize: '0.8rem' }}
                />
              </div>

              <div>
                <label style={{ fontSize: '0.75rem', fontWeight: 700, color: '#F87171' }}>5. CONSTRAINTS (Boundaries & Limits)</label>
                <input 
                  type="text" 
                  value={anatomy.constraints} 
                  onChange={e => setAnatomy({...anatomy, constraints: e.target.value})}
                  style={{ width: '100%', marginTop: '4px', fontSize: '0.8rem' }}
                />
              </div>
            </div>

            {/* Compiled Prompt Preview */}
            <div className="card">
              <h4 style={{ fontSize: '0.95rem', fontWeight: 700, marginBottom: '12px' }}>
                Assembled Zero-Shot Baseline Prompt
              </h4>
              <pre style={{
                background: 'var(--bg-main)',
                padding: '16px',
                borderRadius: '8px',
                border: '1px solid var(--border-color)',
                fontSize: '0.78rem',
                color: 'var(--text-muted)',
                whiteSpace: 'pre-wrap',
                lineHeight: 1.6
              }}>
                {`You are an image analysis assistant.\n\nInstruction: ${anatomy.instruction}\nContext: ${anatomy.context}\nInput: ${anatomy.input}\nOutput Format: ${anatomy.format}\nConstraints: ${anatomy.constraints}\n\nPlease proceed with the instruction for the provided image.`}
              </pre>
            </div>
          </div>
        </div>
      )}

      {/* UNIT 3: Advanced Strategies & Chaining */}
      {activeUnit === 'unit3' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div className="card">
            <h3 style={{ fontSize: '1.15rem', fontWeight: 700, marginBottom: '6px' }}>
              Unit 3: Role-Based Prompting & Prompt Chaining
            </h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', lineHeight: 1.6 }}>
              Rather than asking a model to jump from raw image to complex conclusion in one unguided step, <strong>Prompt Chaining</strong> divides the reasoning pathway into structured sequential stages: Visual Grounding → Empirical Correlation → Synthesis.
            </p>
          </div>

          {/* Chain Simulator */}
          <div className="card">
            <div style={{ display: 'flex', gap: '12px', marginBottom: '20px' }}>
              {[
                { step: 1, title: 'Phase 1: Feature Grounding' },
                { step: 2, title: 'Phase 2: Sensor & CV Correlation' },
                { step: 3, title: 'Phase 3: Pedagogical Synthesis' },
              ].map(s => (
                <button
                  key={s.step}
                  onClick={() => setChainStep(s.step)}
                  style={{
                    flex: 1,
                    padding: '12px',
                    borderRadius: 'var(--radius-md)',
                    background: chainStep === s.step ? 'rgba(168, 85, 247, 0.2)' : 'var(--bg-main)',
                    border: `1px solid ${chainStep === s.step ? 'var(--accent-purple)' : 'var(--border-color)'}`,
                    color: chainStep === s.step ? '#C084FC' : 'var(--text-muted)',
                    fontWeight: 600,
                    fontSize: '0.85rem'
                  }}
                >
                  {s.title}
                </button>
              ))}
            </div>

            <div style={{ padding: '20px', background: 'var(--bg-main)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)' }}>
              {chainStep === 1 && (
                <div>
                  <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: '#C084FC' }}>
                    Phase 1 Directive: Grounding Visible Entities
                  </h4>
                  <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '8px' }}>
                    The model identifies salient foreground objects, bounding coordinates, text labels, and color palettes without drawing speculative conclusions yet.
                  </p>
                  <pre style={{ marginTop: '12px', fontSize: '0.75rem', color: 'var(--accent-cyan)' }}>
                    {`Prompt Directive: "List every distinct visual element in the scene along with its relative spatial quadrant (top-left, center, etc.). Do not infer intent yet."`}
                  </pre>
                </div>
              )}
              {chainStep === 2 && (
                <div>
                  <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: '#C084FC' }}>
                    Phase 2 Directive: Correlating Computer Vision Metadata
                  </h4>
                  <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '8px' }}>
                    The model incorporates OpenCV measurements (Shannon entropy, Canny edge density, contour counts) to substantiate physical sharpness and texture complexity.
                  </p>
                  <pre style={{ marginTop: '12px', fontSize: '0.75rem', color: 'var(--accent-cyan)' }}>
                    {`Prompt Directive: "Given OpenCV Canny edge density of 14.2% and Laplacian focus variance of 185.3, confirm that edge boundaries are sharp and high-contrast."`}
                  </pre>
                </div>
              )}
              {chainStep === 3 && (
                <div>
                  <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: '#C084FC' }}>
                    Phase 3 Directive: Calibrated Synthesis & Delivery
                  </h4>
                  <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '8px' }}>
                    The model produces the final report formatted according to the user's structured preferences, clearly distinguishing fact from uncertainty.
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* UNIT 4: Tools, LCEL & Evaluation */}
      {activeUnit === 'unit4' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div className="card">
            <h3 style={{ fontSize: '1.15rem', fontWeight: 700, marginBottom: '6px' }}>
              Unit 4: Prompt Engineering Frameworks & Evaluation Methodology
            </h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', lineHeight: 1.6 }}>
              In enterprise systems, prompt orchestration is structured through templates and composition languages (such as LangChain Expression Language - LCEL). For research rigor, we evaluate outputs across seven balanced dimensions.
            </p>
          </div>

          <div className="grid-2">
            <div className="card">
              <h4 style={{ fontSize: '0.95rem', fontWeight: 700, marginBottom: '10px' }}>
                7 Research Evaluation Dimensions
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '0.8rem' }}>
                {[
                  { n: '1. Accuracy', d: 'Factual fidelity to visible elements in the image.' },
                  { n: '2. Relevance', d: 'Alignment with user objective (Summarise, Analyse, etc.).' },
                  { n: '3. Completeness', d: 'Coverage of salient entities without omissions.' },
                  { n: '4. Adherence', d: 'Compliance with tone, audience, and format constraints.' },
                  { n: '5. Consistency', d: 'Logical harmony across paragraphs.' },
                  { n: '6. Clarity', d: 'Syntactic readability and structural layout.' },
                  { n: '7. Hallucination Reduction', d: 'Zero fabrication of unverified details.' }
                ].map((dim, i) => (
                  <div key={i} style={{ padding: '8px', background: 'var(--bg-main)', borderRadius: '6px', border: '1px solid var(--border-color)' }}>
                    <strong style={{ color: '#93C5FD' }}>{dim.n}: </strong>
                    <span style={{ color: 'var(--text-muted)' }}>{dim.d}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="card">
              <h4 style={{ fontSize: '0.95rem', fontWeight: 700, marginBottom: '10px' }}>
                A/B Testing Methodology
              </h4>
              <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', lineHeight: 1.6 }}>
                In controlled A/B testing:
              </p>
              <ul style={{ paddingLeft: '20px', fontSize: '0.8rem', color: 'var(--text-dim)', lineHeight: 1.8, marginTop: '8px' }}>
                <li>Keep the underlying model strictly fixed (e.g., <code>qwen2.5vl:3b</code>).</li>
                <li>Keep the input image and visual context identical.</li>
                <li>Vary only the prompt construction strategy.</li>
                <li>Collect quantitative latency, token usage, and human ratings to measure quality gain per token.</li>
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* UNIT 5: Ethics & Uncertainty */}
      {activeUnit === 'unit5' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div className="card">
            <h3 style={{ fontSize: '1.15rem', fontWeight: 700, marginBottom: '6px' }}>
              Unit 5: AI Ethics, Privacy & Anti-Hallucination Guardrails
            </h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', lineHeight: 1.6 }}>
              Responsible AI requires privacy preservation (e.g. Haar face cascades detect geometry without identifying biometric identity), uncertainty calibration, and negative constraints that explicitly forbid speculative fabrication.
            </p>
          </div>

          <div className="card">
            <h4 style={{ fontSize: '0.95rem', fontWeight: 700, marginBottom: '10px' }}>
              Automated Guardrail Evaluator
            </h4>
            <textarea
              rows={3}
              value={guardrailPrompt}
              onChange={e => setGuardrailPrompt(e.target.value)}
              style={{ width: '100%', fontSize: '0.85rem' }}
            />

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '12px', marginTop: '16px' }}>
              <div style={{ padding: '12px', background: hasUncertainty ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)', borderRadius: '6px', border: `1px solid ${hasUncertainty ? 'rgba(16, 185, 129, 0.3)' : 'rgba(239, 68, 68, 0.3)'}` }}>
                <span style={{ fontSize: '0.75rem', fontWeight: 700, color: hasUncertainty ? '#34D399' : '#F87171' }}>
                  {hasUncertainty ? '✓ Uncertainty Instruction Present' : '✗ Lacks Uncertainty Directives'}
                </span>
                <p style={{ fontSize: '0.72rem', color: 'var(--text-dim)', marginTop: '4px' }}>
                  Explicitly instructs model how to declare visual ambiguity.
                </p>
              </div>

              <div style={{ padding: '12px', background: hasNegativeConstraint ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)', borderRadius: '6px', border: `1px solid ${hasNegativeConstraint ? 'rgba(16, 185, 129, 0.3)' : 'rgba(239, 68, 68, 0.3)'}` }}>
                <span style={{ fontSize: '0.75rem', fontWeight: 700, color: hasNegativeConstraint ? '#34D399' : '#F87171' }}>
                  {hasNegativeConstraint ? '✓ Negative Constraints Included' : '✗ Lacks Negative Guardrails'}
                </span>
                <p style={{ fontSize: '0.72rem', color: 'var(--text-dim)', marginTop: '4px' }}>
                  Restricts hallucinations by forbidding speculative statements.
                </p>
              </div>

              <div style={{ padding: '12px', background: hasGrounding ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)', borderRadius: '6px', border: `1px solid ${hasGrounding ? 'rgba(16, 185, 129, 0.3)' : 'rgba(239, 68, 68, 0.3)'}` }}>
                <span style={{ fontSize: '0.75rem', fontWeight: 700, color: hasGrounding ? '#34D399' : '#F87171' }}>
                  {hasGrounding ? '✓ Visual Evidence Grounding' : '✗ Missing Visual Anchor'}
                </span>
                <p style={{ fontSize: '0.72rem', color: 'var(--text-dim)', marginTop: '4px' }}>
                  Ties claims strictly to verifiable image features.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
