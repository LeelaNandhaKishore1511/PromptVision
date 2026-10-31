# PromptVision: An Option-Driven Automated Prompt Engineering and Computer Vision Analysis Framework

**B.Tech Artificial Intelligence and Machine Learning — Final Year Project**

PromptVision is a complete research framework integrating empirical Computer Vision, automated Prompt Engineering, and local Multimodal Vision-Language Models (VLMs).

Instead of requiring users to manually formulate text prompts, PromptVision extracts visual context using actual OpenCV and scikit-image algorithms, synthesizes prompts across three distinct strategies (Basic Baseline, CO-STAR Framework, and AI-Generated Optimization), executes them sequentially through local Ollama models on Windows, and evaluates their performance across seven quantitative and qualitative research dimensions.

---

## Key System Features

- **5 Computer Vision Syllabus Modules**:
  1. *Introduction to CV*: RGB/Grayscale representation, Shannon entropy, sampling theorem aliasing demo, 2D FFT spectrum, Haar wavelet decomposition (LL, LH, HL, HH).
  2. *Image Filtering*: Gaussian, median, bilateral edge-preserving, Otsu and adaptive thresholding, morphological operators, CLAHE, JPEG DCT compression analysis.
  3. *Feature Detection*: Template matching, Harris corners, Sobel and Canny edges, Laplacian focus variance, Hough grid detection, contour extraction, bounding boxes, ORB keypoints and matching, Haar face and eye cascades.
  4. *Image Segmentation*: Active contours (Snakes), quadtree split-and-merge, marker-based watershed, Mean Shift clustering, Felzenszwalb graph segmentation, SLIC superpixels.
  5. *Transformation & Motion*: Rigid Euclidean isometry, general affine mapping, ORB RANSAC image registration, deformable displacement fields, Farneback dense optical flow.
- **3 Prompt Engineering Strategies**:
  1. *Basic Prompting*: Direct prompt anatomy baseline (Instruction, Context, Input, Format, Constraints).
  2. *Framework-Based (CO-STAR)*: Context, Objective, Style, Tone, Audience, Response format with zero-, one-, and few-shot exemplars.
  3. *AI-Generated Optimized Prompting*: Dynamic role persona, CV visual feature grounding, uncertainty calibration (`"[Visual Uncertainty]"`), and anti-hallucination negative constraints.
- **Hardware-Safe Sequential Model Execution**:
  - Optimized for **Intel Core i5-1235U CPU** with **16 GB RAM** on Windows.
  - Strictly 1 model loaded at a time via `asyncio.Lock()`.
  - Zero cloud API reliance; 100% offline inference using local Ollama (`qwen2.5vl:3b` default, `qwen3-vl:8b` advanced).
  - Captures genuine provider metrics (`prompt_eval_count`, `eval_count`, `latency_sec`, `tokens_per_sec`).
- **Interactive Image-Based Teach Mode**:
  - Understands visual diagrams, extracts key concepts, delivers beginner explanations, and generates interactive quizzes.
  - Genuinely grades user responses, diagnoses weak concepts, and estimates understanding levels (Beginner, Developing, Good, Strong).
- **10 Application Pages**:
  1. Dashboard
  2. New Experiment (End-to-end wizard)
  3. Computer Vision Lab (Interactive algorithm workbench)
  4. Prompt Engineering Lab (5 syllabus learning units)
  5. Prompt Comparison (3-way comparative view)
  6. Teach Mode (Interactive lessons and quizzes)
  7. Research and Evaluation (Radar charts, latency/token bar charts, RQ analysis)
  8. Experiment History (Search, filter, reopen, CSV export)
  9. Model Manager (Ollama connectivity, model lifecycle, memory unloading)
  10. About Project (Academic methodology and syllabus mapping)

---

## Quick Start on Windows

### 1. Ensure Ollama is running
```cmd
ollama list
```
Verify `qwen2.5vl:3b` is installed.

### 2. Start FastAPI Backend
```cmd
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
API running at `http://127.0.0.1:8000`.

### 3. Start Frontend (Vite)
```cmd
cd frontend
npm run dev
```
Open your browser at `http://localhost:5173`.

### 4. Run Automated Verification Suite
```cmd
python test_system.py
```

---

## Documentation
- [System Architecture](docs/architecture.md)
- [Computer Vision Syllabus Mapping](docs/cv_syllabus_mapping.md)
- [Prompt Engineering Syllabus Mapping](docs/pe_syllabus_mapping.md)
- [Research Methodology](docs/research_methodology.md)
- [Evaluation Metrics](docs/evaluation_metrics.md)
- [Backend API Documentation](docs/api_documentation.md)
- [Windows Setup Guide](docs/windows_setup_guide.md)
