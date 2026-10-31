import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.prompting.prompt_service import prompt_service
from app.prompting.strategies.basic import generate_basic_prompt
from app.prompting.frameworks.costar import generate_costar_prompt
from app.prompting.refinement.ai_optimized import generate_ai_optimized_prompt

class TestPromptStrategies(unittest.TestCase):
    def setUp(self):
        self.preferences = {
            "audience": "Student",
            "tone": "Professional",
            "output_format": "Structured report",
            "length": "Medium",
            "few_shot_setting": "zero-shot",
            "include_examples": True,
            "explain_terms": True,
            "include_limitations": True,
            "include_uncertainty": True,
            "include_visual_evidence": True,
            "compare_interpretations": False,
            "advanced_instructions": "Highlight primary focal points"
        }
        self.cv_metadata = {
            "source_dimensions": "640x480",
            "source_channels": 3,
            "canny_edges": {
                "algorithm": "Canny Multi-Stage Edge Detector",
                "edge_density_pct": 12.5,
                "description": "Multi-stage edge detection"
            },
            "contour_extraction": {
                "algorithm": "Topological Contour Extraction",
                "total_contours_found": 24,
                "description": "Extracted 24 closed boundary contours"
            }
        }

    def test_strategy1_basic_prompt(self):
        prompt = generate_basic_prompt("Analyse", self.preferences)
        self.assertIn("Prompt Anatomy:", prompt)
        self.assertIn("Instruction:", prompt)
        self.assertIn("Context:", prompt)
        self.assertIn("Input:", prompt)
        self.assertIn("Output format:", prompt)
        self.assertIn("Constraints:", prompt)
        # Should NOT contain CO-STAR tags or CV sensor injection
        self.assertNotIn("### CO-STAR", prompt)
        self.assertNotIn("COMPUTER VISION EXTRACTED CONTEXT", prompt)

    def test_strategy2_costar_prompt(self):
        prompt = generate_costar_prompt("Analyse", self.preferences)
        self.assertIn("### CO-STAR FRAMEWORK SPECIFICATION", prompt)
        self.assertIn("[C] CONTEXT:", prompt)
        self.assertIn("[O] OBJECTIVE:", prompt)
        self.assertIn("[S] STYLE:", prompt)
        self.assertIn("[T] TONE:\nProfessional", prompt)
        self.assertIn("[A] AUDIENCE:\nTailored specifically for a Student", prompt)
        self.assertIn("[R] RESPONSE FORMAT:\nPresent your response in 'Structured report'", prompt)

    def test_strategy2_few_shot_exemplars(self):
        prefs_few_shot = dict(self.preferences)
        prefs_few_shot["few_shot_setting"] = "one-shot"
        prompt = generate_costar_prompt("Analyse", prefs_few_shot)
        self.assertIn("DEMONSTRATION EXEMPLAR", prompt)

    def test_strategy3_ai_optimized_prompt(self):
        prompt = generate_ai_optimized_prompt("Analyse", self.preferences, self.cv_metadata)
        self.assertIn("SYSTEM ROLE & PERSONA:", prompt)
        self.assertIn("COMPUTER VISION EXTRACTED CONTEXT", prompt)
        self.assertIn("12.5%", prompt) # Canny edge density included
        self.assertIn("CHAIN-OF-THOUGHT EXECUTION DIRECTIVES:", prompt)
        self.assertIn("UNCERTAINTY & ANTI-HALLUCINATION GUARDRAILS:", prompt)
        self.assertIn("[Visual Uncertainty:", prompt)

    def test_prompt_service_generates_three_distinct_prompts(self):
        res = prompt_service.generate_all_strategies("Analyse", self.preferences, self.cv_metadata)
        self.assertIn("basic", res)
        self.assertIn("costar", res)
        self.assertIn("ai_optimized", res)
        self.assertNotEqual(res["basic"], res["costar"])
        self.assertNotEqual(res["costar"], res["ai_optimized"])

if __name__ == "__main__":
    unittest.main()
