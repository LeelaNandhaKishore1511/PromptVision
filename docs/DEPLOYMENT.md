# Deployment Guide — PromptVision

## 1. Primary Target Deployment: Local Windows Workstation

PromptVision is engineered as an offline, local-first research platform. Because the core multimodal intelligence relies on local Ollama models (`qwen2.5vl:3b`, `qwen3-vl:8b`), local deployment on the user's laptop is the primary and recommended operational configuration.

### Local Ports Topology:
- **Port 5173**: React Frontend (Vite development server)
- **Port 8000**: FastAPI Backend (Python Uvicorn server)
- **Port 11434**: Ollama Local Inference Engine (Loopback `127.0.0.1:11434`)

### Production Unified Mode (Single Port 8000):
To run PromptVision as a single bundled production server without requiring Node.js at runtime:
1. Build the frontend production bundle:
   ```cmd
   cd frontend
   npm run build
   ```
   This generates the optimized static assets in `frontend/dist/`.
2. The FastAPI backend can mount `frontend/dist` to serve the static HTML, JS, and CSS alongside API routes on port 8000.

---

## 2. Important Architectural Notice Regarding Cloud / Vercel Deployment

> [!WARNING]
> **Cloud / Vercel Deployment Limitations**:
> - Vercel is a serverless static hosting platform that **cannot execute or host local Ollama model weights** (~3.2 GB to ~6.7 GB).
> - A public Vercel frontend cannot access `http://localhost:11434` on a user's laptop unless custom tunneling (e.g. ngrok or Cloudflare tunnels) is established, which exposes local hardware endpoints to the public internet and violates local security guarantees.
> - PromptVision strictly guarantees **zero external data egress** and **100% offline inference**. Therefore, public cloud deployments must be decoupled:
>   - **Static UI Preview**: Demonstrates the frontend layout, CV algorithms, and Prompt Engineering Lab.
>   - **Local Inference Node**: Executes actual VLM reasoning against local Ollama models.

---

## 3. Environment Variables Configuration

Create a `.env` file in the project root based on `.env.example`:

```env
# Ollama Local Service
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_VISION_MODEL=qwen2.5vl:3b
ADVANCED_VISION_MODEL=qwen3-vl:8b
OCR_MODEL=deepseek-ocr:latest

# Performance & Context
DEFAULT_NUM_CTX=4096
MAX_CONCURRENT_MODELS=1
INFERENCE_TIMEOUT=300

# Server Ports
HOST=127.0.0.1
PORT=8000
```
