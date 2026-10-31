import React, { useState } from 'react';
import { 
  GraduationCap, 
  Upload, 
  Play, 
  CheckCircle2, 
  XCircle, 
  HelpCircle, 
  Loader2, 
  BookOpen, 
  Award,
  AlertTriangle,
  RotateCcw
} from 'lucide-react';
import { uploadImage, generateTeachLesson, evaluateTeachQuiz } from '../services/api';

export default function TeachMode() {
  const [image, setImage] = useState(null);
  const [customTopic, setCustomTopic] = useState('');
  const [uploading, setUploading] = useState(false);
  
  // Lesson & Quiz state
  const [generating, setGenerating] = useState(false);
  const [lessonData, setLessonData] = useState(null);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [evaluating, setEvaluating] = useState(false);
  const [evaluationResult, setEvaluationResult] = useState(null);

  async function handleImageUpload(e) {
    const f = e.target.files[0];
    if (!f) return;
    setUploading(true);
    try {
      const meta = await uploadImage(f);
      setImage(meta);
      setLessonData(null);
      setEvaluationResult(null);
      setSelectedAnswers({});
    } catch (err) {
      alert(`Upload failed: ${err.message}`);
    } finally {
      setUploading(false);
    }
  }

  async function handleGenerateLesson() {
    if (!image) {
      alert('Please upload an image first.');
      return;
    }
    setGenerating(true);
    setEvaluationResult(null);
    setSelectedAnswers({});
    try {
      const res = await generateTeachLesson(image.image_id, customTopic || null);
      setLessonData(res);
    } catch (err) {
      alert(`Lesson generation failed: ${err.message}`);
    } finally {
      setGenerating(false);
    }
  }

  function handleSelectOption(qIndex, optionIndex) {
    if (evaluationResult) return; // Prevent changing after submission
    setSelectedAnswers({
      ...selectedAnswers,
      [qIndex]: optionIndex
    });
  }

  async function handleSubmitQuiz() {
    if (!lessonData || !lessonData.quiz) return;
    
    // Check if all questions are answered
    const unanswered = lessonData.quiz.some((_, i) => selectedAnswers[i] === undefined);
    if (unanswered) {
      if (!window.confirm('You have unanswered questions. Submit anyway?')) return;
    }

    setEvaluating(true);
    try {
      const answersPayload = lessonData.quiz.map((q, idx) => ({
        question_index: idx,
        selected_option: selectedAnswers[idx] !== undefined ? selectedAnswers[idx] : -1
      }));

      const res = await evaluateTeachQuiz(lessonData.session_id, answersPayload);
      setEvaluationResult(res);
    } catch (err) {
      alert(`Quiz grading failed: ${err.message}`);
    } finally {
      setEvaluating(false);
    }
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Header */}
      <div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span className="badge badge-purple">Pedagogical Engine</span>
          <h2 style={{ fontSize: '1.4rem', fontWeight: 800 }}>Image-Based Teach Mode & Interactive Assessment</h2>
        </div>
        <p style={{ color: 'var(--text-dim)', fontSize: '0.85rem', marginTop: '4px' }}>
          Multimodal educational assistant: extracts concepts from uploaded visuals, provides beginner explanations, and generates genuine interactive quizzes.
        </p>
      </div>

      {/* Upload and Topic Configuration */}
      <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <div className="grid-2">
          {/* Image Uploader */}
          <div>
            <label style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>
              Upload Educational Image (Diagram / Circuit / Cell / Chart)
            </label>
            <div 
              style={{
                border: '2px dashed var(--border-color)',
                borderRadius: 'var(--radius-md)',
                padding: '24px',
                textAlign: 'center',
                background: 'var(--bg-main)',
                cursor: 'pointer'
              }}
              onClick={() => document.getElementById('teach-file-input').click()}
            >
              <input id="teach-file-input" type="file" accept="image/*" onChange={handleImageUpload} style={{ display: 'none' }} />
              {uploading ? (
                <Loader2 size={24} className="spin" color="var(--accent-purple)" style={{ margin: '0 auto' }} />
              ) : image ? (
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '16px' }}>
                  <img src={image.url} alt="Uploaded" style={{ height: '80px', borderRadius: '6px', objectFit: 'contain' }} />
                  <div style={{ textAlign: 'left' }}>
                    <strong style={{ fontSize: '0.9rem' }}>{image.filename}</strong>
                    <p style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>{image.width}x{image.height} px</p>
                    <span className="badge badge-green" style={{ fontSize: '0.65rem', marginTop: '4px' }}>Image Loaded</span>
                  </div>
                </div>
              ) : (
                <div>
                  <Upload size={24} color="var(--accent-purple)" style={{ margin: '0 auto 6px auto' }} />
                  <p style={{ fontSize: '0.85rem', fontWeight: 600 }}>Click to select educational diagram or photo</p>
                </div>
              )}
            </div>
          </div>

          {/* Topic Customization and Action */}
          <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
            <div>
              <label style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>
                Optional Topic Focus
              </label>
              <input
                type="text"
                placeholder="e.g. Mitosis Phases, Backpropagation in Neural Nets, Hooke's Law"
                value={customTopic}
                onChange={e => setCustomTopic(e.target.value)}
                style={{ width: '100%', fontSize: '0.85rem' }}
              />
              <p style={{ fontSize: '0.75rem', color: 'var(--text-dim)', marginTop: '6px' }}>
                If left blank, the Vision-Language Model will automatically identify the visible subject matter.
              </p>
            </div>

            <button
              className="btn-primary"
              onClick={handleGenerateLesson}
              disabled={generating || !image}
              style={{ width: '100%', marginTop: '16px', justifyContent: 'center' }}
            >
              {generating ? <Loader2 size={16} className="spin" /> : <GraduationCap size={18} />}
              Generate Interactive Lesson & Quiz
            </button>
          </div>
        </div>
      </div>

      {/* Lesson Presentation */}
      {lessonData && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          {/* Lesson Overview Card */}
          <div className="card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
              <span className="badge badge-purple">Topic</span>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 800 }}>{lessonData.topic}</h3>
            </div>

            {/* Key Concepts List */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '12px', marginBottom: '16px' }}>
              {lessonData.concepts?.map((c, i) => (
                <div key={i} style={{ background: 'var(--bg-main)', padding: '12px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)' }}>
                  <strong style={{ fontSize: '0.85rem', color: '#C084FC' }}>{c.name}</strong>
                  <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '4px', lineHeight: 1.5 }}>
                    {c.explanation}
                  </p>
                </div>
              ))}
            </div>

            {/* Full Explanation & Analogy */}
            <div style={{ background: 'var(--bg-main)', padding: '16px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)', fontSize: '0.88rem', lineHeight: 1.7, color: 'var(--text-main)', whiteSpace: 'pre-wrap' }}>
              {lessonData.lesson}
            </div>
          </div>

          {/* Interactive Quiz Card */}
          <div className="card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
              <div>
                <h3 style={{ fontSize: '1.15rem', fontWeight: 700 }}>Interactive Knowledge Check</h3>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-dim)' }}>
                  Answer the questions below based on the visible contents of the image.
                </p>
              </div>
              {evaluationResult && (
                <span className="badge badge-green" style={{ fontSize: '0.85rem' }}>
                  Score: {evaluationResult.score} / {evaluationResult.total_questions} ({evaluationResult.percentage}%)
                </span>
              )}
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              {lessonData.quiz?.map((q, qIdx) => {
                const userChoice = selectedAnswers[qIdx];
                const fb = evaluationResult?.detailed_feedback?.[qIdx];

                return (
                  <div 
                    key={qIdx}
                    style={{
                      background: 'var(--bg-main)',
                      padding: '16px',
                      borderRadius: 'var(--radius-md)',
                      border: '1px solid var(--border-color)'
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                      <strong style={{ fontSize: '0.9rem', color: '#F1F5F9' }}>
                        {qIdx + 1}. {q.question}
                      </strong>
                      <span className="badge badge-gray" style={{ fontSize: '0.65rem' }}>{q.concept}</span>
                    </div>

                    {/* 4 Options */}
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '8px', marginTop: '12px' }}>
                      {q.options?.map((opt, optIdx) => {
                        const isSelected = userChoice === optIdx;
                        let optBg = isSelected ? 'rgba(59, 130, 246, 0.15)' : 'var(--bg-card)';
                        let optBorder = isSelected ? 'var(--accent-blue)' : 'var(--border-color)';

                        if (fb) {
                          if (optIdx === fb.correct_option) {
                            optBg = 'rgba(16, 185, 129, 0.2)';
                            optBorder = 'var(--accent-green)';
                          } else if (isSelected && !fb.is_correct) {
                            optBg = 'rgba(239, 68, 68, 0.2)';
                            optBorder = 'var(--accent-red)';
                          }
                        }

                        return (
                          <div
                            key={optIdx}
                            onClick={() => handleSelectOption(qIdx, optIdx)}
                            style={{
                              padding: '10px 14px',
                              borderRadius: '6px',
                              background: optBg,
                              border: `1px solid ${optBorder}`,
                              cursor: evaluationResult ? 'default' : 'pointer',
                              fontSize: '0.82rem',
                              color: 'var(--text-main)',
                              display: 'flex',
                              alignItems: 'center',
                              gap: '8px',
                              transition: 'all 0.15s'
                            }}
                          >
                            <span style={{
                              width: '20px',
                              height: '20px',
                              borderRadius: '50%',
                              background: isSelected ? 'var(--accent-blue)' : 'var(--bg-main)',
                              color: isSelected ? '#fff' : 'var(--text-dim)',
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'center',
                              fontSize: '0.72rem',
                              fontWeight: 700,
                              flexShrink: 0
                            }}>
                              {String.fromCharCode(65 + optIdx)}
                            </span>
                            <span>{opt}</span>
                          </div>
                        );
                      })}
                    </div>

                    {/* Question Feedback Explanation after submission */}
                    {fb && (
                      <div style={{ marginTop: '10px', padding: '10px', background: fb.is_correct ? 'rgba(16, 185, 129, 0.08)' : 'rgba(239, 68, 68, 0.08)', borderRadius: '6px', fontSize: '0.78rem' }}>
                        <span style={{ fontWeight: 700, color: fb.is_correct ? '#34D399' : '#F87171' }}>
                          {fb.is_correct ? '✓ Correct! ' : '✗ Incorrect. '}
                        </span>
                        <span style={{ color: 'var(--text-muted)' }}>{fb.explanation}</span>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>

            {/* Quiz Submission Button / Results Card */}
            {!evaluationResult ? (
              <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '16px' }}>
                <button
                  className="btn-primary"
                  onClick={handleSubmitQuiz}
                  disabled={evaluating}
                >
                  {evaluating ? <Loader2 size={16} className="spin" /> : <Award size={16} />}
                  Submit Answers & Calculate Score
                </button>
              </div>
            ) : (
              <div style={{ marginTop: '20px', padding: '20px', background: 'var(--bg-main)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '10px' }}>
                  <div>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)', textTransform: 'uppercase' }}>ESTIMATED UNDERSTANDING LEVEL</span>
                    <h4 style={{ fontSize: '1.4rem', fontWeight: 800, color: '#C084FC', marginTop: '2px' }}>
                      {evaluationResult.understanding_level} ({evaluationResult.percentage}%)
                    </h4>
                    <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                      {evaluationResult.understanding_level_note}
                    </p>
                  </div>
                  <button
                    className="btn-secondary"
                    onClick={() => {
                      setEvaluationResult(null);
                      setSelectedAnswers({});
                    }}
                    style={{ fontSize: '0.82rem' }}
                  >
                    <RotateCcw size={14} /> Retake Quiz
                  </button>
                </div>

                {evaluationResult.weak_concepts && evaluationResult.weak_concepts.length > 0 && (
                  <div style={{ marginTop: '14px', padding: '12px', background: 'rgba(245, 158, 11, 0.1)', border: '1px solid rgba(245, 158, 11, 0.3)', borderRadius: '6px', fontSize: '0.8rem', color: '#FCD34D' }}>
                    <strong>Remedial Learning Guidance: </strong>
                    {evaluationResult.remedial_explanation}
                  </div>
                )}

                <p style={{ fontSize: '0.7rem', color: 'var(--text-dim)', marginTop: '12px', fontStyle: 'italic' }}>
                  {evaluationResult.academic_disclaimer}
                </p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
