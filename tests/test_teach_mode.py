import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.database.db import init_db, save_teach_session
from app.teach.teach_service import teach_service

class TestTeachModeScoring(unittest.TestCase):
    def setUp(self):
        init_db()
        self.session_id = "test_teach_session_grading"
        self.mock_session = {
            "id": self.session_id,
            "image_id": "mock_img_001",
            "image_path": "uploads/mock.png",
            "topic": "Neural Network Architecture",
            "concepts": [{"name": "Hidden Layers", "explanation": "Intermediate computation"}],
            "explanation": "Lesson explaining neural network topology.",
            "quiz_data": [
                {
                    "id": 1,
                    "concept": "Input Layer",
                    "question": "What is the role of the input layer?",
                    "options": ["Receive raw features", "Calculate loss", "Backpropagate errors", "None"],
                    "correct_index": 0,
                    "explanation": "Input layer accepts input vectors."
                },
                {
                    "id": 2,
                    "concept": "Activation Function",
                    "question": "Why use non-linear activations?",
                    "options": ["Decrease speed", "Enable non-linear function approximation", "Reduce weights to zero", "None"],
                    "correct_index": 1,
                    "explanation": "Non-linearities allow fitting non-linear decision boundaries."
                },
                {
                    "id": 3,
                    "concept": "Loss Function",
                    "question": "What does loss measure?",
                    "options": ["Accuracy only", "Distance between prediction and ground truth", "Number of nodes", "RAM usage"],
                    "correct_index": 1,
                    "explanation": "Loss quantifies discrepancy."
                },
                {
                    "id": 4,
                    "concept": "Optimization",
                    "question": "Which algorithm updates weights using gradients?",
                    "options": ["Gradient Descent", "Random Forest", "K-Means", "DBSCAN"],
                    "correct_index": 0,
                    "explanation": "Gradient Descent adjusts weights."
                }
            ]
        }
        save_teach_session(self.mock_session)

    def test_perfect_score_strong_level(self):
        # All correct answers: 0, 1, 1, 0
        answers = [
            {"question_index": 0, "selected_option": 0},
            {"question_index": 1, "selected_option": 1},
            {"question_index": 2, "selected_option": 1},
            {"question_index": 3, "selected_option": 0}
        ]
        result = teach_service.evaluate_quiz_submission(self.session_id, answers)
        self.assertEqual(result["score"], 4)
        self.assertEqual(result["total_questions"], 4)
        self.assertEqual(result["percentage"], 100.0)
        self.assertEqual(result["understanding_level"], "Strong")
        self.assertEqual(len(result["weak_concepts"]), 0)

    def test_partial_score_developing_level(self):
        # 2 correct out of 4 (50%) -> Developing
        answers = [
            {"question_index": 0, "selected_option": 0}, # correct
            {"question_index": 1, "selected_option": 0}, # wrong (correct is 1)
            {"question_index": 2, "selected_option": 1}, # correct
            {"question_index": 3, "selected_option": 3}  # wrong (correct is 0)
        ]
        result = teach_service.evaluate_quiz_submission(self.session_id, answers)
        self.assertEqual(result["score"], 2)
        self.assertEqual(result["percentage"], 50.0)
        self.assertEqual(result["understanding_level"], "Developing")
        self.assertIn("Activation Function", result["weak_concepts"])
        self.assertIn("Optimization", result["weak_concepts"])
        self.assertIn("Recommended Focus", result["remedial_explanation"])

    def test_low_score_beginner_level(self):
        # 1 correct out of 4 (25%) -> Beginner
        answers = [
            {"question_index": 0, "selected_option": 3}, # wrong
            {"question_index": 1, "selected_option": 3}, # wrong
            {"question_index": 2, "selected_option": 1}, # correct
            {"question_index": 3, "selected_option": 3}  # wrong
        ]
        result = teach_service.evaluate_quiz_submission(self.session_id, answers)
        self.assertEqual(result["score"], 1)
        self.assertEqual(result["percentage"], 25.0)
        self.assertEqual(result["understanding_level"], "Beginner")

if __name__ == "__main__":
    unittest.main()
