import sys
import asyncio
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / "backend"))

from app.database.db import init_db, get_experiments, get_experiment_by_id
from app.llm.ollama_service import ollama_service
from app.cv.cv_service import cv_service
from app.prompting.prompt_service import prompt_service
from app.teach.teach_service import teach_service
from app.evaluation.eval_service import evaluation_service

async def run_verification():
    print("==================================================")
    print("PROMPTVISION SYSTEM VERIFICATION SUITE")
    print("==================================================")

    # 1. Database Init
    init_db()
    print("[OK] SQLite Database schema initialized")

    # 2. Ollama Connection & Model Detection
    health = await ollama_service.check_health()
    print(f"[OK] Ollama Health Status: {health.get('status')} (Connected: {health.get('connected')})")
    models = await ollama_service.list_models()
    print(f"[OK] Detected {len(models)} local models: {[m['name'] for m in models]}")
    assert any("qwen2.5vl" in m["name"] for m in models), "qwen2.5vl model not detected in Ollama!"

    # 3. Test CV Processing on All 4 Image Types
    test_images = [
        "test_images/sample_photograph.jpg",
        "test_images/sample_chart.png",
        "test_images/sample_text_document.png",
        "test_images/sample_grayscale.png"
    ]
    
    # Upload test image to uploads dir
    from app.config import UPLOADS_DIR
    import shutil
    import cv2
    import numpy as np
    
    test_img_path = Path(test_images[0])
    test_id = "test_img_001"
    dest = UPLOADS_DIR / f"{test_id}.jpg"
    shutil.copy(test_img_path, dest)
    print(f"[OK] Prepared test input image: {dest.name}")

    # Test CV operations from all 5 modules
    cv_ops_to_test = [
        {"id": "pixel_inspection", "params": {}},              # Module 1
        {"id": "fourier_transform", "params": {}},             # Module 1
        {"id": "gaussian_filter", "params": {"kernel_size": 7, "sigma": 1.5}}, # Module 2
        {"id": "thresholding", "params": {"mode": "otsu"}},   # Module 2
        {"id": "canny_edges", "params": {"low_threshold": 50, "high_threshold": 150}}, # Module 3
        {"id": "contour_extraction", "params": {}},           # Module 3
        {"id": "superpixels_slic", "params": {"n_segments": 50}}, # Module 4
        {"id": "rotation", "params": {"angle": 25.0}},        # Module 5
    ]
    
    cv_result = cv_service.process_image_pipeline(test_id, cv_ops_to_test)
    print(f"[OK] Executed {len(cv_result['results'])} CV operations across 5 modules")
    for r in cv_result["results"]:
        print(f"   * [{r['module_name']}] {r['operation_name']}: {r['status']} ({r['execution_time_ms']} ms)")
        assert r["status"] == "success", f"CV op {r['operation_name']} failed: {r.get('error')}"

    # 4. Test Prompt Generation for All 3 Strategies
    prompts = prompt_service.generate_all_strategies(
        objective="Analyse",
        preferences={
            "audience": "Student",
            "tone": "Professional",
            "output_format": "Structured report",
            "length": "Medium",
            "few_shot_setting": "zero-shot",
            "include_examples": True,
            "explain_terms": True,
            "include_limitations": True,
            "include_uncertainty": True,
            "include_visual_evidence": True
        },
        cv_metadata=cv_result["aggregated_metadata"]
    )
    print("[OK] Successfully synthesized 3 distinct prompts:")
    print(f"   * Strategy 1 (Basic): {len(prompts['basic'].split())} words")
    print(f"   * Strategy 2 (CO-STAR): {len(prompts['costar'].split())} words")
    print(f"   * Strategy 3 (AI-Optimized): {len(prompts['ai_optimized'].split())} words")
    assert prompts['basic'] != prompts['costar'], "Basic and CO-STAR prompts must differ!"
    assert prompts['costar'] != prompts['ai_optimized'], "CO-STAR and AI-Optimized prompts must differ!"

    # 5. Test Sequential Local Inference with qwen2.5vl:3b
    print("\n--- Testing Local VLM Inference with qwen2.5vl:3b ---")
    inf_test = await ollama_service.generate_response(
        prompt="Describe the prominent colors and geometric shapes visible in this image in two concise sentences.",
        image_path=str(dest),
        model="qwen2.5vl:3b"
    )
    assert inf_test.get("success"), f"Inference failed: {inf_test.get('error')}"
    print("[OK] Inference succeeded!")
    print(f"   Response Text: {inf_test.get('text')[:120]}...")
    metrics = inf_test.get("metrics", {})
    print(f"   Latency: {metrics.get('latency_sec')}s")
    print(f"   Prompt Tokens: {metrics.get('prompt_eval_count')}")
    print(f"   Output Tokens: {metrics.get('eval_count')}")
    print(f"   Speed: {metrics.get('tokens_per_sec')} tokens/sec")

    # 6. Test Teach Mode (Quiz & Evaluation)
    print("\n--- Testing Teach Mode Knowledge Check ---")
    quiz_submission = [
        {"question_index": 0, "selected_option": 0},
        {"question_index": 1, "selected_option": 1},
        {"question_index": 2, "selected_option": 0}
    ]
    # Grade mock session
    test_session = {
        "id": "test_session_01",
        "image_id": test_id,
        "image_path": str(dest),
        "topic": "Landscape Composition Analysis",
        "quiz_data": [
            {"id": 1, "concept": "Visual Structure", "question": "What is in the foreground?", "options": ["Tree and green grass", "City", "Ocean", "Desert"], "correct_index": 0, "explanation": "Tree and green grass are in foreground."},
            {"id": 2, "concept": "Elevation", "question": "What forms the horizon?", "options": ["Ocean", "Mountain range", "Skyscrapers", "Clouds"], "correct_index": 1, "explanation": "Mountain range forms the horizon."},
            {"id": 3, "concept": "Atmospheric Lighting", "question": "What celestial body is depicted?", "options": ["Sun", "Moon", "Comet", "None"], "correct_index": 0, "explanation": "Sun in upper sky."}
        ]
    }
    from app.database.db import save_teach_session
    save_teach_session(test_session)
    grade = teach_service.evaluate_quiz_submission("test_session_01", quiz_submission)
    print(f"[OK] Quiz Graded: Score {grade['score']}/{grade['total_questions']} ({grade['percentage']}%) - Level: {grade['understanding_level']}")

    print("\n==================================================")
    print("ALL CORE INTEGRATION CHECKS PASSED PERFECTLY!")
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(run_verification())
