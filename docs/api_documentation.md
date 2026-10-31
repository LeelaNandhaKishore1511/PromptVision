# Backend API Documentation — PromptVision

FastAPI backend endpoints providing complete programmatic access to the Computer Vision, Prompt Engineering, Model Management, and Evaluation services.

Base URL: `http://localhost:8000` (or `/api` via Vite dev proxy on `http://localhost:5173`).

---

## 1. System & Model Management

### `GET /api/health`
Checks backend and Ollama connectivity.
- **Response**:
  ```json
  {
    "status": "online",
    "service": "PromptVision Backend",
    "ollama": {
      "connected": true,
      "available_models": ["deepseek-ocr:latest", "qwen2.5vl:3b", "qwen3-vl:8b"],
      "current_model": "qwen2.5vl:3b"
    }
  }
  ```

### `GET /api/models`
Lists all installed local models in Ollama with sizes and active selection.

### `POST /api/models/select`
Switches the active Vision-Language Model.
- **Payload**: `{"model": "qwen2.5vl:3b"}`

### `POST /api/models/unload`
Unloads model from RAM to free system memory (`keep_alive: 0`).

---

## 2. Image Management

### `POST /api/image/upload`
Uploads an image file (`multipart/form-data`). Validates format and size.
- **Response**:
  ```json
  {
    "image_id": "a1b2c3d4e5f6",
    "filename": "diagram.png",
    "width": 640,
    "height": 480,
    "channels": 3,
    "format": "PNG",
    "file_size_kb": 128.4,
    "url": "/api/image/raw/a1b2c3d4e5f6.png"
  }
  ```

### `GET /api/image/raw/{filename}`
Serves original raw uploaded image.

### `GET /api/image/processed/{filename}`
Serves processed Computer Vision image result.

---

## 3. Computer Vision Engine

### `GET /api/cv/operations`
Returns the complete catalog of 5 syllabus modules, operations, parameter schemas, and descriptions.

### `POST /api/cv/process`
Executes one or more CV operations on an uploaded image.
- **Payload**:
  ```json
  {
    "image_id": "a1b2c3d4e5f6",
    "operations": [
      {"id": "canny_edges", "params": {"low_threshold": 50, "high_threshold": 150}},
      {"id": "contour_extraction", "params": {}}
    ]
  }
  ```
- **Response**: Returns processed image URLs, execution duration (ms), and extracted mathematical metadata.

---

## 4. Prompt Synthesis & Experiment Runner

### `POST /api/prompts/generate`
Generates prompts for all 3 strategies based on objective, preferences, and CV metadata without executing inference.

### `POST /api/experiments/run`
Runs the complete sequential multimodal experiment pipeline:
1. Validates image and executes selected CV operations.
2. Formulates 3 distinct prompts (Basic, CO-STAR, AI-Optimized).
3. Executes requests sequentially on the selected local VLM.
4. Extracts actual Ollama provider token counts and latencies.
5. Persists complete record to SQLite.

---

## 5. Experiment Management & Evaluation

### `GET /api/experiments`
Lists stored experiments with optional `?search=` filtering.

### `GET /api/experiments/{id}`
Retrieves complete experiment record including prompts, responses, metrics, and ratings.

### `DELETE /api/experiments/{id}`
Deletes an experiment record.

### `POST /api/experiments/{id}/evaluate`
Saves human evaluation ratings (1 to 5 stars) across the 7 research dimensions.

### `GET /api/experiments/export`
Streams a formatted CSV export of all experimental runs and token analytics.

---

## 6. Image-Based Teach Mode

### `POST /api/teach/generate`
Analyzes uploaded visual input and generates a beginner-friendly lesson, concepts list, and 4 multiple-choice questions.

### `POST /api/teach/evaluate`
Grades submitted quiz answers, calculates exact score and percentage, determines understanding level (Beginner / Developing / Good / Strong), and generates targeted remedial recommendations.
