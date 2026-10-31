import React from 'react';
import { 
  GraduationCap, 
  Layers, 
  Cpu, 
  ShieldCheck, 
  BookOpen, 
  Eye, 
  CheckCircle2, 
  FileText,
  Workflow
} from 'lucide-react';

export default function About() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Title Card */}
      <div className="card" style={{ padding: '28px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
          <span className="badge badge-purple">B.Tech AI & ML Final Year Project</span>
          <span className="badge badge-blue">Academic Research Project</span>
        </div>
        <h2 style={{ fontSize: '1.6rem', fontWeight: 800 }}>
          PromptVision: An Option-Driven Automated Prompt Engineering & Computer Vision Analysis Framework
        </h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', lineHeight: 1.6, marginTop: '8px' }}>
          PromptVision rethinks multimodal interaction by replacing manual prompt formulation with structured options and empirical Computer Vision context. The framework demonstrates that grounded CV features coupled with structured prompt strategies (CO-STAR, AI-Optimization) consistently outperform unguided zero-shot baselines on local vision-language models.
        </p>
      </div>

      {/* System Architecture Flow */}
      <div className="card">
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
          <Workflow size={20} color="var(--accent-cyan)" />
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>End-to-End System Architecture</h3>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '12px' }}>
          {[
            { step: '1. Image Ingestion', desc: 'Metadata extraction, dimension analysis, channel decomposition via PIL & OpenCV.' },
            { step: '2. Option Selection', desc: 'Objective cards (Summarise, Analyse, Evaluate, Explain, Teach) eliminating manual prompt typing.' },
            { step: '3. CV Engine', desc: 'OpenCV/NumPy/skimage execution across 5 syllabus modules for empirical visual grounding.' },
            { step: '4. Prompt Generation', desc: 'Synthesizes 3 distinct strategies: Basic Anatomy, CO-STAR Framework, and AI-Optimized.' },
            { step: '5. Sequential VLM', desc: 'Hardware-safe CPU inference through local Ollama using the identical selected vision model.' },
            { step: '6. Evaluation & Storage', desc: '7-dimensional benchmarking, actual token metrics, human ratings, and SQLite persistence.' },
          ].map((s, idx) => (
            <div 
              key={idx}
              style={{
                background: 'var(--bg-main)',
                padding: '14px',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--border-color)',
                display: 'flex',
                flexDirection: 'column',
                gap: '6px'
              }}
            >
              <span className="badge badge-blue" style={{ width: 'fit-content', fontSize: '0.65rem' }}>Phase {idx+1}</span>
              <strong style={{ fontSize: '0.85rem' }}>{s.step}</strong>
              <p style={{ fontSize: '0.75rem', color: 'var(--text-dim)', lineHeight: 1.4 }}>{s.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Syllabus Mappings (2 Columns) */}
      <div className="grid-2">
        {/* Computer Vision Syllabus Mapping */}
        <div className="card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
            <Eye size={18} color="var(--accent-blue)" />
            <h3 style={{ fontSize: '1rem', fontWeight: 700 }}>Computer Vision Syllabus Mapping</h3>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '0.8rem' }}>
            <div style={{ padding: '10px', background: 'var(--bg-main)', borderRadius: '6px' }}>
              <strong style={{ color: '#93C5FD' }}>Module 1: Introduction to CV</strong>
              <p style={{ color: 'var(--text-dim)', marginTop: '2px' }}>
                RGB/Grayscale representation, Shannon entropy, Nyquist sampling theorem, 2D FFT spectrum, 2D Haar wavelets (LL, LH, HL, HH).
              </p>
            </div>
            <div style={{ padding: '10px', background: 'var(--bg-main)', borderRadius: '6px' }}>
              <strong style={{ color: '#93C5FD' }}>Module 2: Image Filtering & Enhancement</strong>
              <p style={{ color: 'var(--text-dim)', marginTop: '2px' }}>
                Gaussian & Bilateral smoothing, Otsu & Adaptive thresholding, Morphological operators (Open/Close), CLAHE, JPEG DCT compression.
              </p>
            </div>
            <div style={{ padding: '10px', background: 'var(--bg-main)', borderRadius: '6px' }}>
              <strong style={{ color: '#93C5FD' }}>Module 3: Feature Detection & Matching</strong>
              <p style={{ color: 'var(--text-dim)', marginTop: '2px' }}>
                Harris corners, Canny & Sobel gradients, Laplacian focus variance, Hough line grids, Contours, ORB features & matching, Haar face/eye cascades.
              </p>
            </div>
            <div style={{ padding: '10px', background: 'var(--bg-main)', borderRadius: '6px' }}>
              <strong style={{ color: '#93C5FD' }}>Module 4: Image Segmentation</strong>
              <p style={{ color: 'var(--text-dim)', marginTop: '2px' }}>
                Active Contours (Snakes), Quadtree Split-and-Merge, Marker Watershed, Mean Shift clustering, Felzenszwalb graph segmentation, SLIC superpixels.
              </p>
            </div>
            <div style={{ padding: '10px', background: 'var(--bg-main)', borderRadius: '6px' }}>
              <strong style={{ color: '#93C5FD' }}>Module 5: Transformation, Alignment & Motion</strong>
              <p style={{ color: 'var(--text-dim)', marginTop: '2px' }}>
                Rigid Euclidean isometry, 6-DOF Affine mapping, ORB RANSAC image registration, Deformable displacement fields, Farneback dense optical flow.
              </p>
            </div>
          </div>
        </div>

        {/* Prompt Engineering Syllabus Mapping */}
        <div className="card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
            <BookOpen size={18} color="var(--accent-purple)" />
            <h3 style={{ fontSize: '1rem', fontWeight: 700 }}>Prompt Engineering Syllabus Mapping</h3>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '0.8rem' }}>
            <div style={{ padding: '10px', background: 'var(--bg-main)', borderRadius: '6px' }}>
              <strong style={{ color: '#C084FC' }}>Unit 1: Foundations of PE & LLMs</strong>
              <p style={{ color: 'var(--text-dim)', marginTop: '2px' }}>
                Tokenization mechanics, context windows, BPE token vs character distinctions, multimodal attention embeddings.
              </p>
            </div>
            <div style={{ padding: '10px', background: 'var(--bg-main)', borderRadius: '6px' }}>
              <strong style={{ color: '#C084FC' }}>Unit 2: Prompt Design Fundamentals</strong>
              <p style={{ color: 'var(--text-dim)', marginTop: '2px' }}>
                5-part prompt anatomy (Instruction, Context, Input, Format, Constraints), Zero-shot vs Few-shot calibration.
              </p>
            </div>
            <div style={{ padding: '10px', background: 'var(--bg-main)', borderRadius: '6px' }}>
              <strong style={{ color: '#C084FC' }}>Unit 3: Advanced Strategies & Chaining</strong>
              <p style={{ color: 'var(--text-dim)', marginTop: '2px' }}>
                CO-STAR framework, role persona engineering, prompt chaining pipelines, iterative refinement protocols.
              </p>
            </div>
            <div style={{ padding: '10px', background: 'var(--bg-main)', borderRadius: '6px' }}>
              <strong style={{ color: '#C084FC' }}>Unit 4: Tools, LCEL & Evaluation</strong>
              <p style={{ color: 'var(--text-dim)', marginTop: '2px' }}>
                A/B testing methodologies, 7 balanced evaluation dimensions, rate-distortion token efficiency metrics.
              </p>
            </div>
            <div style={{ padding: '10px', background: 'var(--bg-main)', borderRadius: '6px' }}>
              <strong style={{ color: '#C084FC' }}>Unit 5: Ethics, Automation & Capstone</strong>
              <p style={{ color: 'var(--text-dim)', marginTop: '2px' }}>
                Anti-hallucination negative constraints, uncertainty calibration, privacy-preserving face geometry, automated prompt synthesis.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
