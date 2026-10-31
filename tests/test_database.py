import unittest
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.database.db import (
    init_db,
    save_experiment,
    get_experiments,
    get_experiment_by_id,
    delete_experiment,
    save_ratings,
    get_stats_summary
)

class TestDatabaseOperations(unittest.TestCase):
    def setUp(self):
        init_db()
        self.exp_id = f"test_db_{uuid.uuid4().hex[:8]}"
        self.exp_data = {
            "id": self.exp_id,
            "title": "Unit Test Experiment Run",
            "image_id": "img_test_123",
            "image_path": "uploads/img_test_123.jpg",
            "image_filename": "img_test_123.jpg",
            "image_width": 640,
            "image_height": 480,
            "image_channels": 3,
            "selected_objective": "Analyse",
            "cv_operations": [{"id": "canny_edges", "params": {}}],
            "cv_metadata": {"canny_edges": {"edge_density_pct": 14.5}},
            "processed_image_urls": ["/api/image/processed/out1.jpg"],
            "selected_model": "qwen2.5vl:3b",
            "preferences": {"audience": "Student", "tone": "Technical"},
            "prompts": {"basic": "Basic prompt text", "costar": "CO-STAR prompt text", "ai_optimized": "Optimized prompt"},
            "responses": {"basic": "Basic output", "costar": "CO-STAR output", "ai_optimized": "Optimized output"},
            "metrics": {
                "basic": {"latency_sec": 4.2, "eval_count": 80},
                "costar": {"latency_sec": 6.1, "eval_count": 140},
                "ai_optimized": {"latency_sec": 8.5, "eval_count": 210}
            },
            "ratings": {"basic": {"accuracy": 4}, "costar": {"accuracy": 4.5}, "ai_optimized": {"accuracy": 5}},
            "status": "completed"
        }

    def test_save_and_retrieve_experiment(self):
        saved_id = save_experiment(self.exp_data)
        self.assertEqual(saved_id, self.exp_id)

        retrieved = get_experiment_by_id(self.exp_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["title"], "Unit Test Experiment Run")
        self.assertEqual(retrieved["selected_objective"], "Analyse")
        self.assertEqual(retrieved["selected_model"], "qwen2.5vl:3b")
        self.assertIsInstance(retrieved["metrics"], dict)
        self.assertEqual(retrieved["metrics"]["basic"]["eval_count"], 80)

    def test_save_ratings(self):
        save_experiment(self.exp_data)
        new_ratings = {"basic": {"accuracy": 5, "relevance": 5}}
        success = save_ratings(self.exp_id, new_ratings)
        self.assertTrue(success)

        updated = get_experiment_by_id(self.exp_id)
        self.assertEqual(updated["ratings"]["basic"]["accuracy"], 5)

    def test_list_and_search_experiments(self):
        save_experiment(self.exp_data)
        results = get_experiments(limit=10, search="Unit Test Experiment")
        self.assertGreaterEqual(len(results), 1)
        self.assertTrue(any(e["id"] == self.exp_id for e in results))

    def test_delete_experiment(self):
        save_experiment(self.exp_data)
        deleted = delete_experiment(self.exp_id)
        self.assertTrue(deleted)

        retrieved = get_experiment_by_id(self.exp_id)
        self.assertIsNone(retrieved)

    def test_stats_summary(self):
        save_experiment(self.exp_data)
        stats = get_stats_summary()
        self.assertIn("total_experiments", stats)
        self.assertIn("total_images", stats)
        self.assertGreaterEqual(stats["total_experiments"], 1)

if __name__ == "__main__":
    unittest.main()
