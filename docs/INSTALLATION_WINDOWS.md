# Windows Installation & Setup Guide — PromptVision

This guide provides step-by-step instructions for running the PromptVision platform on Windows 10/11 64-bit systems.

---

## 1. System Requirements

- **Operating System**: Windows 10 / Windows 11 (64-bit).
- **Processor**: Intel Core i5 (12th Gen or higher recommended).
- **RAM**: 16 GB (15.7 GB usable minimum recommended for 3B/8B VLM CPU inference).
- **GPU**: Integrated Intel Iris Xe or dedicated GPU (system is designed CPU-first).
- **Storage**: ~20 GB free space for Ollama models and dependencies.

---

## 2. Software Prerequisites

### Step 2.1: Verify Python
Ensure Python 3.10+ (tested with Python 3.14) is installed and accessible in your PATH:
```cmd
python --version
pip --version
```

### Step 2.2: Verify Node.js
Ensure Node.js 18+ and npm are installed:
```cmd
node --version
npm --version
```

### Step 2.3: Verify Ollama & Models
Ensure Ollama for Windows is running:
```cmd
ollama --version
ollama list
```
Verify that the following models are installed:
- `qwen2.5vl:3b`
- `qwen3-vl:8b`
- `deepseek-ocr:latest`

If Ollama is not running, launch it from the Windows Start Menu or command prompt (`ollama serve`).

---

## 3. Repository Setup

```cmd
git clone https://github.com/LeelaNandhaKishore1511/PromptVision.git
cd PromptVision
```

---

## 4. Backend Startup

1. Open a PowerShell or Command Prompt terminal in the project root:
```cmd
pip install -r backend/requirements.txt
```

2. Start the FastAPI backend server:
```cmd
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
The backend server will start at:
- **API Root**: `http://127.0.0.1:8000`
- **Swagger Documentation**: `http://127.0.0.1:8000/docs`
- **Health Check**: `http://127.0.0.1:8000/api/health`

---

## 5. Frontend Startup

1. Open a second terminal window in the project root:
```cmd
cd frontend
npm install
npm run dev
```

2. Open your web browser and navigate to:
```text
http://localhost:5173
```

The Vite dev server automatically proxies API requests (`/api/*`) to the backend on `http://127.0.0.1:8000`.

---

## 6. Running the Verification Suite

To run the automated verification test suite verifying all 5 CV modules, Ollama local inference, token extraction, and quiz scoring:
```cmd
python test_system.py
```
Or to run the standard unit tests:
```cmd
python -m unittest discover tests
```

All tests should pass reporting `[OK]`.
