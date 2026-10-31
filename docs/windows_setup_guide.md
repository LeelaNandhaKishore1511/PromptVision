# Windows Setup & Execution Guide — PromptVision

This guide provides instructions to run PromptVision locally on Windows 64-bit with Intel Core i5 and 16 GB RAM.

---

## 1. Prerequisites

1. **Python 3.10+** (Python 3.14 verified):
   ```cmd
   python --version
   ```
2. **Node.js 18+** (Node v24.21.0 verified):
   ```cmd
   node --version
   npm --version
   ```
3. **Ollama for Windows**:
   - Ensure Ollama is running at `http://localhost:11434`.
   - Verify installed models:
     ```cmd
     ollama list
     ```
     Should show:
     - `qwen2.5vl:3b`
     - `qwen3-vl:8b`
     - `deepseek-ocr:latest`

---

## 2. Backend Setup & Startup

From the project root:

```cmd
# 1. (Optional) Install Python dependencies if running in a fresh environment
pip install -r backend/requirements.txt

# 2. Start the FastAPI backend server
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

The backend will start and host the API at:
- `http://127.0.0.1:8000`
- Interactive API Docs: `http://127.0.0.1:8000/docs`

---

## 3. Frontend Setup & Startup

In a second terminal window:

```cmd
cd frontend

# Install node dependencies (if not already installed)
npm install

# Start Vite development server
npm run dev
```

The frontend will start at:
- `http://localhost:5173`

Vite automatically proxies `/api/*` requests to the FastAPI backend at `http://127.0.0.1:8000`.

---

## 4. Running the Complete Verification Suite

To verify all CV modules, Ollama local inference, token extraction, and quiz grading in one automated script:

```cmd
python test_system.py
```

All operations should report `[OK]`.
