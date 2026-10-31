const API_BASE = '/api';

export async function checkHealth() {
  const res = await fetch(`${API_BASE}/health`);
  return res.json();
}

export async function getModels() {
  const res = await fetch(`${API_BASE}/models`);
  return res.json();
}

export async function selectModel(modelName) {
  const res = await fetch(`${API_BASE}/models/select`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ model: modelName }),
  });
  return res.json();
}

export async function unloadModel(modelName) {
  const res = await fetch(`${API_BASE}/models/unload`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ model: modelName }),
  });
  return res.json();
}

export async function uploadImage(file) {
  const formData = new FormData();
  formData.append('file', file);
  const res = await fetch(`${API_BASE}/image/upload`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Upload failed' }));
    throw new Error(err.detail || 'Image upload failed');
  }
  return res.json();
}

export async function getCVOperations() {
  const res = await fetch(`${API_BASE}/cv/operations`);
  return res.json();
}

export async function processCV(payload) {
  const res = await fetch(`${API_BASE}/cv/process`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'CV Processing failed' }));
    throw new Error(err.detail || 'CV Processing failed');
  }
  return res.json();
}

export async function generatePrompts(payload) {
  const res = await fetch(`${API_BASE}/prompts/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Prompt generation failed' }));
    throw new Error(err.detail || 'Prompt generation failed');
  }
  return res.json();
}

export async function runExperiment(payload) {
  const res = await fetch(`${API_BASE}/experiments/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Experiment execution failed' }));
    throw new Error(err.detail || 'Experiment execution failed');
  }
  return res.json();
}

export async function getExperiments(search = '') {
  const url = search ? `${API_BASE}/experiments?search=${encodeURIComponent(search)}` : `${API_BASE}/experiments`;
  const res = await fetch(url);
  return res.json();
}

export async function getExperiment(id) {
  const res = await fetch(`${API_BASE}/experiments/${id}`);
  if (!res.ok) throw new Error('Experiment not found');
  return res.json();
}

export async function deleteExperiment(id) {
  const res = await fetch(`${API_BASE}/experiments/${id}`, { method: 'DELETE' });
  return res.json();
}

export async function submitEvaluation(experimentId, ratings) {
  const res = await fetch(`${API_BASE}/experiments/${experimentId}/evaluate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ experiment_id: experimentId, ratings }),
  });
  return res.json();
}

export async function generateTeachLesson(imageId, customTopic = null, model = null) {
  const res = await fetch(`${API_BASE}/teach/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image_id: imageId, custom_topic: customTopic, model }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Teach generation failed' }));
    throw new Error(err.detail || 'Teach generation failed');
  }
  return res.json();
}

export async function evaluateTeachQuiz(sessionId, answers) {
  const res = await fetch(`${API_BASE}/teach/evaluate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId, answers }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Quiz evaluation failed' }));
    throw new Error(err.detail || 'Quiz evaluation failed');
  }
  return res.json();
}

export async function getResearchSummary() {
  const res = await fetch(`${API_BASE}/research/summary`);
  return res.json();
}

export async function getDashboardStats() {
  const res = await fetch(`${API_BASE}/dashboard/stats`);
  return res.json();
}
