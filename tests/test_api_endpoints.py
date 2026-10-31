import unittest
import sys
from pathlib import Path
from starlette.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.main import app

class TestAPIEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_health_endpoint(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "online")
        self.assertIn("ollama", data)

    def test_cv_operations_catalog(self):
        response = self.client.get("/api/cv/operations")
        self.assertEqual(response.status_code, 200)
        catalog = response.json()
        self.assertIn("module1", catalog)
        self.assertIn("module2", catalog)
        self.assertIn("module3", catalog)
        self.assertIn("module4", catalog)
        self.assertIn("module5", catalog)

    def test_prompt_generation_endpoint(self):
        payload = {
            "image_id": "test_img",
            "objective": "Analyse",
            "preferences": {
                "audience": "Student",
                "tone": "Professional",
                "output_format": "Structured report",
                "length": "Medium"
            },
            "cv_metadata": {"source_dimensions": "640x480"}
        }
        response = self.client.post("/api/prompts/generate", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("basic_prompt", data)
        self.assertIn("costar_prompt", data)
        self.assertIn("ai_optimized_prompt", data)

    def test_dashboard_stats_endpoint(self):
        response = self.client.get("/api/dashboard/stats")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("total_experiments", data)
        self.assertIn("total_images", data)

    def test_experiments_export_csv(self):
        response = self.client.get("/api/experiments/export")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/csv", response.headers.get("content-type", ""))
        self.assertIn("Experiment ID,Date,Title", response.text)

if __name__ == "__main__":
    unittest.main()
