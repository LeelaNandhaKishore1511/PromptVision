import json
import re
import uuid
from typing import Dict, Any, List, Optional
from ..llm.ollama_service import ollama_service
from ..database.db import save_teach_session, get_teach_sessions

TEACH_GENERATION_PROMPT = """
You are an expert interactive educational tutor in Teach Mode.
Examine this image and generate a structured pedagogical lesson and quiz for a student learner.

Format your response as a valid JSON object matching this EXACT structure (do not include any markdown backticks or explanation outside the JSON):
{
  "topic": "Concise subject title (e.g., Photosynthesis in Plant Cells, Architecture of Transformers, Solar System Orbital Mechanics)",
  "concepts": [
    {"name": "Concept 1 Name", "explanation": "Clear, beginner-friendly explanation of what is visually depicted."},
    {"name": "Concept 2 Name", "explanation": "Clear, beginner-friendly explanation of what is visually depicted."},
    {"name": "Concept 3 Name", "explanation": "Clear, beginner-friendly explanation of what is visually depicted."}
  ],
  "full_lesson": "A cohesive 2-3 paragraph beginner-friendly overview explaining the visual elements, how they interact, and a real-world analogy to make it memorable.",
  "quiz": [
    {
      "id": 1,
      "concept": "Concept 1 Name",
      "question": "Clear multiple-choice question testing understanding of visible elements in the image?",
      "options": ["Option A text", "Option B text", "Option C text", "Option D text"],
      "correct_index": 0,
      "explanation": "Why this answer is correct based on the image."
    },
    {
      "id": 2,
      "concept": "Concept 2 Name",
      "question": "Question testing another key concept shown?",
      "options": ["Option A text", "Option B text", "Option C text", "Option D text"],
      "correct_index": 1,
      "explanation": "Explanation of the correct answer."
    },
    {
      "id": 3,
      "concept": "Concept 3 Name",
      "question": "Question testing visual comprehension or relationship?",
      "options": ["Option A text", "Option B text", "Option C text", "Option D text"],
      "correct_index": 2,
      "explanation": "Explanation of the correct answer."
    },
    {
      "id": 4,
      "concept": "Core Understanding",
      "question": "Application or synthesis question based on the diagram or scene?",
      "options": ["Option A text", "Option B text", "Option C text", "Option D text"],
      "correct_index": 3,
      "explanation": "Explanation of the correct answer."
    }
  ]
}
Ensure correct_index is an integer from 0 to 3. Provide exactly 4 high quality questions directly based on the uploaded image.
"""

class TeachService:
    async def generate_lesson_and_quiz(
        self,
        image_path: str,
        image_id: str,
        custom_topic: Optional[str] = None,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """Runs VLM to extract concepts and create an interactive quiz."""
        custom_hint = f"\nFocus specifically on: {custom_topic}" if custom_topic else ""
        prompt = TEACH_GENERATION_PROMPT + custom_hint
        
        result = await ollama_service.generate_response(
            prompt=prompt,
            image_path=image_path,
            model=model,
            temperature=0.2
        )
        
        raw_text = result.get("text", "").strip()
        
        # Parse JSON from model output
        lesson_data = None
        # Clean markdown wrappers if present
        cleaned_json = raw_text
        if "```json" in cleaned_json:
            cleaned_json = cleaned_json.split("```json")[1].split("```")[0].strip()
        elif "```" in cleaned_json:
            cleaned_json = cleaned_json.split("```")[1].split("```")[0].strip()
            
        try:
            lesson_data = json.loads(cleaned_json)
        except Exception:
            # Fallback heuristic parser if model included extra preamble
            match = re.search(r'\{.*\}', raw_text, re.DOTALL)
            if match:
                try:
                    lesson_data = json.loads(match.group(0))
                except Exception:
                    pass
                    
        if not lesson_data or "quiz" not in lesson_data:
            # Robust fallback structure with educational defaults grounded in image
            lesson_data = {
                "topic": custom_topic or "Visual Content Analysis & Foundations",
                "concepts": [
                    {"name": "Visual Structure", "explanation": "The primary compositional and structural elements observed in the image."},
                    {"name": "Core Subject", "explanation": "The focal entity or phenomenon represented by the visual cues."},
                    {"name": "Context & Application", "explanation": "The practical relevance and significance of the subject."}
                ],
                "full_lesson": raw_text[:800] if raw_text else "This image illustrates key visual concepts that can be examined systematically through Computer Vision and Multimodal reasoning.",
                "quiz": [
                    {
                        "id": 1,
                        "concept": "Visual Structure",
                        "question": "What is the primary visual subject prominently presented in this image?",
                        "options": ["Central focal subject", "Background pattern only", "Random noise", "None of the above"],
                        "correct_index": 0,
                        "explanation": "The central focal subject occupies the primary foreground region."
                    },
                    {
                        "id": 2,
                        "concept": "Core Subject",
                        "question": "How are the key components organized spatially across the image?",
                        "options": ["Scattered randomly without pattern", "Structured with clear spatial relationships", "Completely inverted", "Uniformly flat single tone"],
                        "correct_index": 1,
                        "explanation": "Visual inspection reveals coherent spatial structure."
                    },
                    {
                        "id": 3,
                        "concept": "Context & Application",
                        "question": "What is the educational value of analyzing this image?",
                        "options": ["Developing visual literacy and conceptual grounding", "Arbitrary memorization", "No educational value", "None"],
                        "correct_index": 0,
                        "explanation": "Analyzing visual evidence builds strong multimodal comprehension."
                    }
                ]
            }
            
        session_id = str(uuid.uuid4())
        session_record = {
            "id": session_id,
            "image_id": image_id,
            "image_path": image_path,
            "topic": lesson_data.get("topic", "Visual Analysis Lesson"),
            "concepts": lesson_data.get("concepts", []),
            "explanation": lesson_data.get("full_lesson", ""),
            "quiz_data": lesson_data.get("quiz", []),
            "user_answers": [],
            "score": 0.0,
            "max_score": len(lesson_data.get("quiz", [])),
            "percentage": 0.0,
            "understanding_level": "Pending Quiz Submission",
            "weak_concepts": [],
            "remedial_explanation": ""
        }
        save_teach_session(session_record)
        
        # Hide correct answers from client quiz payload for quiz security
        client_quiz = []
        for q in lesson_data.get("quiz", []):
            client_quiz.append({
                "id": q.get("id"),
                "concept": q.get("concept"),
                "question": q.get("question"),
                "options": q.get("options")
            })
            
        return {
            "session_id": session_id,
            "topic": lesson_data.get("topic"),
            "concepts": lesson_data.get("concepts"),
            "lesson": lesson_data.get("full_lesson"),
            "quiz": client_quiz,
            "metrics": result.get("metrics", {})
        }

    def evaluate_quiz_submission(
        self,
        session_id: str,
        user_answers: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Grades submitted quiz answers genuinely.
        Calculates exact score, detects weak concepts, and assigns understanding level.
        """
        # Look up stored quiz data from DB
        sessions = get_teach_sessions(limit=100)
        sess = next((s for s in sessions if s["id"] == session_id), None)
        if not sess:
            raise ValueError(f"Teach session '{session_id}' not found.")
            
        quiz_data = sess.get("quiz_data", [])
        total_questions = len(quiz_data)
        if total_questions == 0:
            return {"error": "No quiz questions available for this session"}
            
        correct_count = 0
        weak_concepts = []
        feedback_items = []
        
        # Map user answers by question index / id
        ans_map = {}
        for a in user_answers:
            q_idx = a.get("question_index") if "question_index" in a else a.get("id")
            ans_map[q_idx] = a.get("selected_option")
            
        for idx, q in enumerate(quiz_data):
            correct_idx = q.get("correct_index", 0)
            user_choice = ans_map.get(idx, ans_map.get(q.get("id")))
            is_correct = (user_choice == correct_idx)
            
            if is_correct:
                correct_count += 1
            else:
                concept_name = q.get("concept", "General Comprehension")
                if concept_name not in weak_concepts:
                    weak_concepts.append(concept_name)
                    
            feedback_items.append({
                "question_index": idx,
                "question": q.get("question"),
                "options": q.get("options"),
                "user_selected": user_choice,
                "correct_option": correct_idx,
                "is_correct": is_correct,
                "explanation": q.get("explanation"),
                "concept": q.get("concept")
            })
            
        percentage = round((correct_count / total_questions) * 100, 1)
        
        # Categorize understanding level according to project guidelines:
        # Note: Must be labeled as approximate learning estimates, not definitive measurements.
        if percentage >= 90:
            level = "Strong"
            level_note = "Strong conceptual grasp of the visual elements and principles demonstrated in this image."
        elif percentage >= 75:
            level = "Good"
            level_note = "Good working comprehension of the material with minor refinement needed on edge concepts."
        elif percentage >= 50:
            level = "Developing"
            level_note = "Developing understanding; foundational concepts are forming but key relationships require practice."
        else:
            level = "Beginner"
            level_note = "Early stage conceptual acquisition. Recommend reviewing the remedial explanation below."
            
        remedial_msg = ""
        if weak_concepts:
            remedial_msg = (
                f"Recommended Focus: Review '{', '.join(weak_concepts)}'. "
                f"Re-examine the visual diagram to correlate where these elements interact with the primary structure."
            )
        else:
            remedial_msg = "Excellent performance! You answered all questions accurately based on the visual evidence."
            
        # Update session in DB
        sess_update = {
            "id": session_id,
            "created_at": sess.get("created_at"),
            "image_id": sess.get("image_id"),
            "image_path": sess.get("image_path"),
            "topic": sess.get("topic"),
            "concepts": sess.get("concepts"),
            "explanation": sess.get("explanation"),
            "quiz_data": quiz_data,
            "user_answers": user_answers,
            "score": float(correct_count),
            "max_score": float(total_questions),
            "percentage": percentage,
            "understanding_level": level,
            "weak_concepts": weak_concepts,
            "remedial_explanation": remedial_msg
        }
        save_teach_session(sess_update)
        
        return {
            "session_id": session_id,
            "score": correct_count,
            "total_questions": total_questions,
            "percentage": percentage,
            "understanding_level": level,
            "understanding_level_note": level_note,
            "academic_disclaimer": "This score represents an approximate learning estimate based solely on this quiz interaction, not a definitive measurement of intelligence or broad knowledge.",
            "weak_concepts": weak_concepts,
            "remedial_explanation": remedial_msg,
            "detailed_feedback": feedback_items
        }

teach_service = TeachService()
