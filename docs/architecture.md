# System Architecture — PromptVision

## 1. High-Level System Overview

**PromptVision** is a research-oriented, full-stack framework integrating Computer Vision, Automated Prompt Engineering, and Local Multimodal Vision-Language Models (VLMs). Designed as a B.Tech Artificial Intelligence and Machine Learning Final Year Project, it replaces ad-hoc manual prompt typing with structured option-driven interaction and empirical Computer Vision context.

```
+----------------------------------------------------------------------------------------------------+
|                                    PROMPTVISION WORKFLOW PIPELINE                                  |
+----------------------------------------------------------------------------------------------------+
|  [User Image Ingestion] -> [Objective Selection] -> [Structured Preferences (MCQs)]               |
|                                     |                                                              |
|                                     v                                                              |
|                         [Computer Vision Engine]                                                   |
|                         * Module 1: Intro, Sampling, 2D FFT, Wavelets                              |
|                         * Module 2: Gaussian/Bilateral Filtering, Otsu Threshold, CLAHE            |
|                         * Module 3: Harris Corners, Canny Edges, Contours, ORB, Haar Cascades      |
|                         * Module 4: Active Contours, Split-Merge, Watershed, Mean Shift, SLIC      |
|                         * Module 5: Rigid, Affine, ORB RANSAC Alignment, Optical Flow              |
|                                     |                                                              |
|                                     v                                                              |
|                         [Visual Metadata Extraction]                                               |
|                         (Edge density, Shannon entropy, contour count, frequency spectrum, etc.)   |
|                                     |                                                              |
|                                     v                                                              |
|                     [3 Prompt Engineering Strategies]                                              |
|                     * Strategy 1: Basic Prompting (Direct Anatomy Baseline)                        |
|                     * Strategy 2: Framework-Based Prompting (CO-STAR with Exemplars)               |
|                     * Strategy 3: AI-Generated Optimized Prompting (CV Grounded + Guardrails)       |
|                                     |                                                              |
|                                     v                                                              |
|            [Local VLM Execution (Sequential Hardware-Safe Ollama API)]                             |
|            * Selected Vision Model: qwen2.5vl:3b / qwen3-vl:8b (Identical for all 3 strategies)    |
|            * Extraction of Real Provider Token Counts & Durations                                  |
|                                     |                                                              |
|                                     v                                                              |
|                    [Evaluation & Comparative Research Dashboard]                                   |
|                    * 7 Balanced Quality Dimensions                                                 |
|                    * Latency, Token Throughput, and Rate-Distortion Analytics                      |
|                    * SQLite Persistence (promptvision.db) & CSV Export                             |
+----------------------------------------------------------------------------------------------------+
```

## 2. Hardware Architecture & Memory Safeguards

Designed specifically for an **Intel Core i5-1235U CPU** with **16 GB RAM** and **Intel Iris Xe Graphics**:
- **Zero Cloud API Reliance**: Operates 100% offline via local Ollama (`http://localhost:11434`).
- **Single Model In-Memory Concurrency**: Enforces an internal `asyncio.Lock()` preventing concurrent model instances from thrashing system memory.
- **Sequential Strategy Execution**: The 3 prompt strategies are executed sequentially through the identical selected model, ensuring scientific control and hardware stability.
- **Dynamic Model Unloading**: Features explicit memory deallocation (`keep_alive: 0`) to free system RAM between extensive batches.
- **Resolution Capping for Dense Algorithms**: Computationally intensive CV routines (e.g., Felzenszwalb, Active Contours) dynamically downsample scratch images during computation to cap processing time under 150ms.

## 3. Technology Stack

- **Frontend**: React.js (v19), Vite (v8), Lucide Icons, Recharts.
- **Backend**: Python 3.14, FastAPI, Pydantic, Uvicorn, SQLite3.
- **Computer Vision**: OpenCV (opencv-python-headless), NumPy, Pillow, scikit-image, scikit-learn, SciPy, PyWavelets.
- **Inference Server**: Ollama local inference engine running `qwen2.5vl:3b`, `qwen3-vl:8b`, and `deepseek-ocr:latest`.
