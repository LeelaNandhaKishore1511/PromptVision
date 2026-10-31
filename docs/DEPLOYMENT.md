# Deployment Guide — PromptVision (Local, Render & Vercel)

This comprehensive guide details how to deploy PromptVision across:
1. **Local Windows Workstation (Recommended / Default)**
2. **Render (Backend API Service)**
3. **Vercel (Frontend Client)**

---

## 1. Architecture of the Deployment

```
+-------------------------------------------------------------+
|                 FRONTEND (Vercel Cloud)                     |
|           https://promptvision.vercel.app                   |
|   (Vite + React 19 + Recharts + Lucide Icons + vercel.json) |
+-------------------------------------------------------------+
                              |
                              | HTTP / JSON Requests (VITE_API_URL)
                              v
+-------------------------------------------------------------+
|                 BACKEND (Render Web Service)                |
|         https://promptvision-backend.onrender.com           |
|        (Python + FastAPI + OpenCV + SQLite + Uvicorn)       |
+-------------------------------------------------------------+
                              |
                              | Localhost or Tunnel (OLLAMA_BASE_URL)
                              v
+-------------------------------------------------------------+
|               LOCAL INFERENCE ENGINE (Ollama)               |
|            http://localhost:11434 (on user laptop)          |
|      (qwen2.5vl:3b, qwen3-vl:8b, deepseek-ocr:latest)       |
+-------------------------------------------------------------+
```

---

## 2. Deploying the Backend to Render

[Render](https://render.com) is a modern cloud hosting platform with a free tier suitable for hosting Python FastAPI applications.

### Step-by-Step Render Deployment:

1. **Sign in to Render**:
   - Go to [dashboard.render.com](https://dashboard.render.com) and sign in with your GitHub account (`LeelaNandhaKishore1511`).
2. **Create a New Web Service**:
   - Click **New +** $\rightarrow$ **Web Service**.
   - Select **Build and deploy from a Git repository**.
   - Choose your repository: `LeelaNandhaKishore1511/PromptVision`.
3. **Configure Service Settings**:
   - **Name**: `promptvision-backend`
   - **Region**: Oregon (US West) or Frankfurt (EU)
   - **Branch**: `main`
   - **Root Directory**: *(leave blank for repository root)*
   - **Runtime**: `Python 3`
   - **Build Command**:
     ```bash
     pip install -r backend/requirements.txt
     ```
   - **Start Command**:
     ```bash
     uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
     ```
   - **Instance Type**: `Free`
4. **Environment Variables**:
   Under **Environment Variables**, add:
   - `PYTHON_VERSION`: `3.11.9`
   - `DEFAULT_VISION_MODEL`: `qwen2.5vl:3b`
   - `DEFAULT_NUM_CTX`: `4096`
   - `MAX_CONCURRENT_MODELS`: `1`
5. **Deploy**:
   - Click **Create Web Service**.
   - Render will build your dependencies and start FastAPI. Once deployment finishes, you will receive a public URL:
     `https://promptvision-backend.onrender.com`
   - Verify health at: `https://promptvision-backend.onrender.com/api/health`
   - View interactive API docs at: `https://promptvision-backend.onrender.com/docs`

---

## 3. Deploying the Frontend to Vercel

[Vercel](https://vercel.com) provides instant, global edge deployment for Vite and React applications.

### Step-by-Step Vercel Deployment:

1. **Sign in to Vercel**:
   - Go to [vercel.com](https://vercel.com) and log in with your GitHub account.
2. **Import Repository**:
   - Click **Add New...** $\rightarrow$ **Project**.
   - Select `LeelaNandhaKishore1511/PromptVision`.
3. **Configure Project Settings**:
   - **Framework Preset**: `Vite`
   - **Root Directory**: Click *Edit* and select **`frontend`** (or leave as root; both are supported via `vercel.json`).
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. **Configure Environment Variable**:
   Under **Environment Variables**, add:
   - **Key**: `VITE_API_URL`
   - **Value**: Your Render backend URL (e.g., `https://promptvision-backend.onrender.com`)
   *(Note: Do not include a trailing slash)*
5. **Deploy**:
   - Click **Deploy**.
   - In ~45 seconds, Vercel will deploy your application and provide your production URL:
     `https://promptvision.vercel.app` (or `https://promptvision-<username>.vercel.app`).

---

## 4. Connecting the Cloud Backend to Local Ollama

Because the free tiers of Render and Vercel cannot host 6–10 GB local Ollama model weights in GPU memory, the cloud backend needs access to an Ollama endpoint to run live VLM inference.

You have two choices:

### Option A: Local-Only Mode (Recommended for Thesis Defense)
- Run the full system locally as detailed in [`docs/INSTALLATION_WINDOWS.md`](INSTALLATION_WINDOWS.md):
  - Frontend: `http://localhost:5173`
  - Backend: `http://127.0.0.1:8000`
  - Ollama: `http://localhost:11434`
- **Zero latency, zero cost, and 100% data privacy.**

### Option B: Cloud Deployment with Free Cloudflare / ngrok Tunnel
If you want your cloud Render backend (`https://promptvision-backend.onrender.com`) to query the Ollama models running on your Windows laptop during a live demo:
1. On your Windows laptop, open a terminal and run [ngrok](https://ngrok.com) or Cloudflare Tunnel:
   ```cmd
   ngrok http 11434
   ```
2. Copy the resulting forwarding URL:
   `https://random-subdomain.ngrok-free.app`
3. On your Render Dashboard $\rightarrow$ `promptvision-backend` $\rightarrow$ **Environment Variables**:
   - Set `OLLAMA_BASE_URL` to: `https://random-subdomain.ngrok-free.app`
   - Click **Save Changes**.
4. Now, any experiment launched from Vercel will process CV on Render and execute sequential VLM inference through your laptop's Ollama engine!
