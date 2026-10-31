# Changelog — PromptVision

All notable changes to the **PromptVision** framework are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-31

### Added
- **Core Framework**:
  - Implemented option-driven multimodal workflow replacing manual prompt formulation with structured cards and MCQs.
  - Developed FastAPI backend with RESTful API endpoints for health, model management, image upload, CV execution, prompt generation, experiment execution, history, and evaluation.
  - Implemented SQLite database persistence with tables for experiments, evaluations, teach sessions, and CV logs.
- **Computer Vision Engine (5 Modules)**:
  - Module 1 (Introduction): Channel decomposition, Shannon entropy inspection, Nyquist sampling theorem demonstration, 2D FFT magnitude spectrum, 2D Haar wavelet decomposition (LL, LH, HL, HH).
  - Module 2 (Filtering & Enhancement): Gaussian, median, bilateral edge-preserving smoothing, Otsu and adaptive thresholding, morphological operators, CLAHE, JPEG DCT compression artifact comparison.
  - Module 3 (Feature Detection): Template matching (`TM_CCOEFF_NORMED`), Harris corner detection, Sobel gradients, Canny edge detection with density calculation, Laplacian focus sharpness variance, Hough line grid detection, topological contour extraction, ORB keypoints and matching, Haar cascade face & eye detection.
  - Module 4 (Segmentation): Kass et al. Active Contours (Snakes), quadtree split-and-merge, marker-controlled watershed, Mean Shift clustering, Felzenszwalb graph segmentation, SLIC superpixel clustering.
  - Module 5 (Transformation & Motion): Rigid Euclidean isometry, general 6-DOF affine mapping, feature-based ORB RANSAC image registration, harmonic displacement field deformable registration demo, Gunnar Farneback dense optical flow HSV color wheel.
- **Three Prompt Engineering Strategies**:
  - Strategy 1 (Basic Prompting): 5-part prompt anatomy baseline (Instruction, Context, Input, Output Format, Constraints) establishing an un-optimized control.
  - Strategy 2 (Framework-Based Prompting): CO-STAR framework (Context, Objective, Style, Tone, Audience, Response format) with zero-, one-, and few-shot exemplars and MCQ preferences.
  - Strategy 3 (AI-Generated Optimized Prompting): Automated role persona selection, CV sensor metadata grounding, uncertainty calibration (`"[Visual Uncertainty: ...]"`), and negative anti-hallucination constraints.
- **Local AI & Memory Manager**:
  - Ollama integration supporting `qwen2.5vl:3b` (default), `qwen3-vl:8b` (advanced), and `deepseek-ocr:latest`.
  - Sequential inference enforcement via `asyncio.Lock()` to eliminate multi-model RAM thrashing on 16GB Intel Core i5.
  - Memory unload endpoint (`keep_alive: 0`) for dynamic RAM recovery.
  - Real provider token metrics capture (`prompt_eval_count`, `eval_count`, `latency_sec`, `tokens_per_sec`).
- **Interactive Teach Mode**:
  - Educational visual breakdown: Topic, Concepts, Lesson explanation, Real-world analogy.
  - Interactive 4-question knowledge check with real-time scoring, weak concept diagnostics, and understanding level estimation.
- **Research & Evaluation Dashboard**:
  - Multi-dimensional benchmarking across 7 balanced dimensions (Accuracy, Relevance, Completeness, Instruction Adherence, Consistency, Clarity, Hallucination Reduction).
  - Recharts visual charts: 7-dimension Radar comparison, Latency vs Output Tokens bar chart, Rate-Distortion quality per 1000 tokens.
  - CSV export streaming endpoint.
- **Frontend UI (10 Pages)**:
  - Dashboard, New Experiment Wizard, CV Lab, PE Lab, Prompt Comparison, Teach Mode, Research & Evaluation, History, Model Manager, About Project.
- **Automated Verification & CI**:
  - Comprehensive unit test suite in `tests/` covering CV algorithms, prompt strategies, grading, and API routes.
  - GitHub Actions CI workflow in `.github/workflows/ci.yml`.
