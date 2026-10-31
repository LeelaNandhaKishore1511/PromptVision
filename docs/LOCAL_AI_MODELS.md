# Local AI Models & Model Management — PromptVision

PromptVision is engineered to operate 100% locally on consumer hardware without external cloud APIs. All multimodal intelligence is powered by local Ollama models on Windows.

---

## 1. Supported Local Ollama Models

| Model Identifier | Size on Disk | Architecture | Primary Role | Hardware Recommendation |
|---|---|---|---|---|
| **`qwen2.5vl:3b`** | **~3.2 GB** | Qwen 2.5 Vision-Language Model (3 Billion parameters) | **Default Multimodal Model**: Image analysis, summarization, explanation, Teach Mode, and 3-strategy benchmarking. | **Optimal for Intel Core i5 & 16GB RAM CPU execution.** Latency: 2–3s for short responses, 10–25s for long reports. |
| **`qwen3-vl:8b`** | **~6.1 GB** | Qwen 3 Vision-Language Model (8 Billion parameters) | **Optional Advanced Model**: Deeper visual reasoning, complex mathematical analysis, comparative model benchmarking. | Optional: Requires higher memory bandwidth and CPU resources. |
| **`deepseek-ocr:latest`** | **~6.7 GB** | DeepSeek Optical Character Recognition | **Supplementary Document Model**: Extracting text from diagrams, screenshots, and scans. | Specialized tasks where textual extraction takes precedence over visual reasoning. |

---

## 2. Model Invocation Mechanics (Ollama REST API)

Inference is executed via direct HTTP calls to Ollama's local daemon (`http://localhost:11434`):
- `GET /api/tags`: Enumerates installed models, sizes, and digests.
- `POST /api/chat`: Generates multimodal responses with base64 image encoding.
- `POST /api/generate`: Used for model lifecycle management (`keep_alive: 0` for RAM deallocation).

### Multimodal Payload Structure:
```json
{
  "model": "qwen2.5vl:3b",
  "messages": [
    {
      "role": "user",
      "content": "Analyse the visual contents...",
      "images": ["<base64_encoded_jpeg_or_png>"]
    }
  ],
  "stream": false,
  "options": {
    "temperature": 0.2,
    "num_ctx": 4096
  }
}
```

---

## 3. Real Provider Token Metrics Extraction

PromptVision does not invent or estimate token metrics when Ollama exposes actual values. The following fields are extracted directly from Ollama's JSON response:

```json
{
  "prompt_eval_count": 1073,
  "eval_count": 25,
  "prompt_eval_duration": 482000000,
  "eval_duration": 2205000000,
  "total_duration": 2687000000
}
```

These values are translated into:
- **Input Tokens**: `prompt_eval_count` (includes prompt text tokens and visual patch embedding tokens).
- **Output Tokens**: `eval_count` (generated response tokens).
- **Latency**: `total_duration` converted to seconds.
- **Generation Speed**: `eval_count / (eval_duration / 1e9)` tokens/second.

---

## 4. Hardware Protections for Windows CPU Execution

1. **Sequential Lock**: An internal `asyncio.Lock()` enforces that only one inference call executes at any given moment.
2. **Context Window Boundary**: Context is capped at 4096 tokens (`DEFAULT_NUM_CTX=4096`) to prevent quadratic memory scaling in Transformer attention.
3. **RAM Recovery**: The user can unload the active model from RAM at any time via the Model Manager UI or `POST /api/models/unload`.
