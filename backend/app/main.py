import io
import os
import csv
import uuid
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image

from .config import (
    UPLOADS_DIR,
    PROCESSED_DIR,
    ALLOWED_EXTENSIONS,
    MAX_IMAGE_SIZE_MB,
    DEFAULT_VISION_MODEL
)
from .database.db import (
    init_db,
    save_experiment,
    get_experiments,
    get_experiment_by_id,
    delete_experiment,
    save_ratings,
    get_stats_summary
)
from .llm.ollama_service import ollama_service
from .cv.cv_service import cv_service
from .prompting.prompt_service import prompt_service
from .teach.teach_service import teach_service
from .evaluation.eval_service import evaluation_service
from .schemas.schemas import (
    ImageMetadataResponse,
    CVProcessRequest,
    CVProcessResponse,
    PromptGenerationRequest,
    GeneratedPromptsResponse,
    ExperimentRunRequest,
    EvaluationRatingRequest,
    TeachGenerateRequest,
    TeachEvaluateRequest
)

# Initialize Database
init_db()

app = FastAPI(
    title="PromptVision API",
    description="An Option-Driven Automated Prompt Engineering and Computer Vision Analysis Framework (B.Tech Final Year Project)",
    version="1.0.0"
)

# Enable CORS for local frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- HEALTH & MODEL MANAGER -----------------

@app.get("/api/health")
async def health_check():
    ollama_info = await ollama_service.check_health()
    return {
        "status": "online",
        "service": "PromptVision Backend",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ollama": ollama_info
    }

@app.get("/api/models")
async def list_models():
    models = await ollama_service.list_models()
    health = await ollama_service.check_health()
    return {
        "connected": health.get("connected", False),
        "current_model": ollama_service.current_model,
        "models": models
    }

@app.get("/api/models/status")
async def get_model_status():
    return await ollama_service.check_health()

@app.post("/api/models/select")
async def select_model(payload: Dict[str, str]):
    model_name = payload.get("model")
    if not model_name:
        raise HTTPException(status_code=400, detail="Missing 'model' parameter")
    res = await ollama_service.set_active_model(model_name)
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res.get("error"))
    return res

@app.post("/api/models/unload")
async def unload_model(payload: Optional[Dict[str, str]] = None):
    target = payload.get("model") if payload else None
    return await ollama_service.unload_model(target)

# ----------------- IMAGE UPLOAD & METADATA -----------------

@app.post("/api/image/upload", response_model=ImageMetadataResponse)
async def upload_image(file: UploadFile = File(...)):
    filename = file.filename or "upload.png"
    ext = Path(filename).suffix.lower()
    
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format '{ext}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
        
    image_id = str(uuid.uuid4())[:12]
    saved_filename = f"{image_id}{ext}"
    dest_path = UPLOADS_DIR / saved_filename
    
    # Save content
    content = await file.read()
    if len(content) > MAX_IMAGE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"Image exceeds max size of {MAX_IMAGE_SIZE_MB}MB")
        
    with open(dest_path, "wb") as f:
        f.write(content)
        
    # Analyze with PIL to extract factual metadata
    try:
        with Image.open(dest_path) as img:
            width, height = img.size
            format_name = img.format or ext.replace(".", "").upper()
            channels = len(img.getbands())
    except Exception as e:
        dest_path.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail=f"Corrupt or invalid image file: {str(e)}")
        
    file_size_bytes = len(content)
    file_size_kb = round(file_size_bytes / 1024.0, 2)
    
    return ImageMetadataResponse(
        image_id=image_id,
        filename=filename,
        width=width,
        height=height,
        channels=channels,
        format=format_name,
        file_size_bytes=file_size_bytes,
        file_size_kb=file_size_kb,
        url=f"/api/image/raw/{saved_filename}"
    )

@app.get("/api/image/raw/{filename}")
async def get_raw_image(filename: str):
    p = UPLOADS_DIR / filename
    if not p.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(p)

@app.get("/api/image/processed/{filename}")
async def get_processed_image(filename: str):
    p = PROCESSED_DIR / filename
    if not p.exists():
        raise HTTPException(status_code=404, detail="Processed image not found")
    return FileResponse(p)

@app.get("/api/image/{image_id}/metadata")
async def get_image_metadata(image_id: str):
    path = cv_service._resolve_image_path(image_id)
    if not path or not path.exists():
        raise HTTPException(status_code=404, detail="Image ID not found")
    with Image.open(path) as img:
        return {
            "image_id": image_id,
            "filename": path.name,
            "width": img.width,
            "height": img.height,
            "channels": len(img.getbands()),
            "format": img.format,
            "file_size_kb": round(path.stat().st_size / 1024.0, 2),
            "url": f"/api/image/raw/{path.name}"
        }

# ----------------- COMPUTER VISION ENDPOINTS -----------------

@app.get("/api/cv/operations")
async def get_cv_operations():
    return cv_service.get_catalog()

@app.post("/api/cv/process", response_model=CVProcessResponse)
async def process_cv(payload: CVProcessRequest):
    try:
        res = cv_service.process_image_pipeline(
            image_id=payload.image_id,
            operations=payload.operations,
            second_image_id=payload.second_image_id
        )
        return res
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CV Execution failed: {str(e)}")

# ----------------- PROMPT GENERATION -----------------

@app.post("/api/prompts/generate", response_model=GeneratedPromptsResponse)
async def generate_prompts(payload: PromptGenerationRequest):
    prompts = prompt_service.generate_all_strategies(
        objective=payload.objective,
        preferences=payload.preferences.model_dump(),
        cv_metadata=payload.cv_metadata
    )
    return GeneratedPromptsResponse(
        basic_prompt=prompts["basic"],
        costar_prompt=prompts["costar"],
        ai_optimized_prompt=prompts["ai_optimized"],
        objective=payload.objective,
        preferences=payload.preferences.model_dump(),
        cv_metadata_summary=payload.cv_metadata
    )

# ----------------- EXPERIMENT RUNNER -----------------

@app.post("/api/experiments/run")
async def run_experiment(payload: ExperimentRunRequest):
    """
    Executes the full research pipeline:
    1. Validates image.
    2. Runs selected CV operations (if provided) and collects metadata.
    3. Generates prompts for selected strategies.
    4. Executes model requests sequentially with the SAME selected Vision-Language Model.
    5. Collects real Ollama provider metrics.
    6. Persists complete experiment to SQLite.
    """
    img_path = cv_service._resolve_image_path(payload.image_id)
    if not img_path or not img_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
        
    with Image.open(img_path) as img:
        img_w, img_h = img.size
        img_channels = len(img.getbands())
        
    # Execute CV operations if requested
    cv_res = None
    cv_metadata = {}
    processed_urls = []
    if payload.cv_operations:
        cv_res = cv_service.process_image_pipeline(
            image_id=payload.image_id,
            operations=payload.cv_operations,
            second_image_id=payload.second_image_id
        )
        cv_metadata = cv_res.get("aggregated_metadata", {})
        processed_urls = [r["processed_image_url"] for r in cv_res.get("results", []) if r.get("processed_image_url")]

    # Generate the 3 prompts
    pref_dict = payload.preferences.model_dump()
    all_prompts = prompt_service.generate_all_strategies(
        objective=payload.objective,
        preferences=pref_dict,
        cv_metadata=cv_metadata
    )

    # Selected Model: CRITICAL RULE - same model used for all strategies
    chosen_model = payload.model or ollama_service.current_model
    
    # Execute strategies sequentially
    results = {}
    responses_dict = {}
    metrics_dict = {}
    
    strategies = payload.strategies_to_run or ["basic", "costar", "ai_optimized"]
    for strat in strategies:
        strat_key = strat.lower()
        prompt_text = all_prompts.get(strat_key, "")
        if not prompt_text:
            continue
            
        # Call Ollama local inference with sequential lock
        inf_result = await ollama_service.generate_response(
            prompt=prompt_text,
            image_path=str(img_path),
            model=chosen_model
        )
        
        results[strat_key] = {
            "strategy": strat_key,
            "prompt": prompt_text,
            "response": inf_result.get("text", ""),
            "metrics": inf_result.get("metrics", {}),
            "error": inf_result.get("error")
        }
        responses_dict[strat_key] = inf_result.get("text", "")
        metrics_dict[strat_key] = inf_result.get("metrics", {})

    # Compute baseline heuristic ratings so comparison radar/charts render immediately
    initial_ratings = {}
    for s_k, resp_text in responses_dict.items():
        initial_ratings[s_k] = evaluation_service.compute_heuristic_score(
            resp_text, payload.objective, pref_dict
        )

    # Persist experiment
    exp_id = str(uuid.uuid4())
    exp_record = {
        "id": exp_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "title": payload.title or f"{payload.objective} Experiment - {datetime.now().strftime('%b %d, %H:%M')}",
        "image_id": payload.image_id,
        "image_path": str(img_path),
        "image_filename": img_path.name,
        "image_width": img_w,
        "image_height": img_h,
        "image_channels": img_channels,
        "selected_objective": payload.objective,
        "cv_operations": payload.cv_operations,
        "cv_metadata": cv_metadata,
        "processed_image_urls": processed_urls,
        "selected_model": chosen_model,
        "preferences": pref_dict,
        "prompts": all_prompts,
        "responses": responses_dict,
        "metrics": metrics_dict,
        "ratings": initial_ratings,
        "status": "completed"
    }
    save_experiment(exp_record)

    return {
        "experiment_id": exp_id,
        "title": exp_record["title"],
        "created_at": exp_record["created_at"],
        "selected_model": chosen_model,
        "selected_objective": payload.objective,
        "image_id": payload.image_id,
        "image_url": f"/api/image/raw/{img_path.name}",
        "cv_results": cv_res.get("results", []) if cv_res else [],
        "prompts": all_prompts,
        "results": results,
        "ratings": initial_ratings,
        "status": "completed"
    }

# ----------------- EXPERIMENTS HISTORY & EVALUATION -----------------

@app.get("/api/experiments")
async def list_experiments(limit: int = 50, offset: int = 0, search: Optional[str] = None):
    return get_experiments(limit=limit, offset=offset, search=search)

@app.get("/api/experiments/export")
async def export_experiments_csv():
    experiments = get_experiments(limit=500)
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Headers
    writer.writerow([
        "Experiment ID", "Date", "Title", "Objective", "Model",
        "CV Operations Count", "Strategy", "Latency (sec)",
        "Prompt Tokens", "Output Tokens", "Total Tokens",
        "Accuracy Rating", "Relevance", "Clarity", "Response Length (Words)"
    ])
    
    for exp in experiments:
        exp_id = exp.get("id")
        created = exp.get("created_at")
        title = exp.get("title")
        obj = exp.get("selected_objective")
        model = exp.get("selected_model")
        cv_count = len(exp.get("cv_operations") or [])
        
        metrics = exp.get("metrics") or {}
        ratings = exp.get("ratings") or {}
        responses = exp.get("responses") or {}
        
        for strat in ["basic", "costar", "ai_optimized"]:
            m = metrics.get(strat) or {}
            r = ratings.get(strat) or {}
            resp_text = responses.get(strat) or ""
            words = len(resp_text.split())
            
            writer.writerow([
                exp_id,
                created,
                title,
                obj,
                model,
                cv_count,
                strat,
                m.get("latency_sec", ""),
                m.get("prompt_eval_count", ""),
                m.get("eval_count", ""),
                m.get("total_tokens", ""),
                r.get("accuracy", ""),
                r.get("relevance", ""),
                r.get("clarity", ""),
                words
            ])
            
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=promptvision_experiments_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"}
    )

@app.get("/api/experiments/{experiment_id}")
async def get_experiment(experiment_id: str):
    exp = get_experiment_by_id(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@app.delete("/api/experiments/{experiment_id}")
async def remove_experiment(experiment_id: str):
    success = delete_experiment(experiment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"success": True, "message": "Experiment deleted"}

@app.post("/api/experiments/{experiment_id}/evaluate")
async def evaluate_experiment(experiment_id: str, payload: EvaluationRatingRequest):
    exp = get_experiment_by_id(experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
        
    current_ratings = exp.get("ratings") or {}
    current_ratings.update(payload.ratings)
    save_ratings(experiment_id, current_ratings)
    return {"success": True, "ratings": current_ratings}

# ----------------- TEACH MODE -----------------

@app.post("/api/teach/generate")
async def teach_generate(payload: TeachGenerateRequest):
    path = cv_service._resolve_image_path(payload.image_id)
    if not path or not path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
        
    return await teach_service.generate_lesson_and_quiz(
        image_path=str(path),
        image_id=payload.image_id,
        custom_topic=payload.custom_topic,
        model=payload.model
    )

@app.post("/api/teach/evaluate")
async def teach_evaluate(payload: TeachEvaluateRequest):
    try:
        answers = [a.model_dump() for a in payload.answers]
        return teach_service.evaluate_quiz_submission(
            session_id=payload.session_id,
            user_answers=answers
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------------- RESEARCH & SUMMARY -----------------

@app.get("/api/research/summary")
async def get_research_summary():
    return evaluation_service.aggregate_research_summary()

@app.get("/api/dashboard/stats")
async def get_dashboard_stats():
    return get_stats_summary()

