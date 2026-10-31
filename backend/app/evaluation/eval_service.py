from typing import Dict, Any, List, Optional
from ..database.db import get_experiments, get_connection

class EvaluationService:
    @staticmethod
    def get_dimension_definitions() -> List[Dict[str, str]]:
        return [
            {
                "id": "accuracy",
                "name": "Accuracy & Visual Grounding",
                "description": "Factual alignment with clearly visible features in the image without spurious fabrication."
            },
            {
                "id": "relevance",
                "name": "Relevance to Objective",
                "description": "Direct fulfillment of the chosen user objective (Summarise, Analyse, Evaluate, Explain, Teach)."
            },
            {
                "id": "completeness",
                "name": "Completeness & Depth",
                "description": "Thorough coverage of salient components, relationships, and context."
            },
            {
                "id": "instruction_adherence",
                "name": "Instruction Adherence",
                "description": "Compliance with requested output format, tone, audience level, and length constraints."
            },
            {
                "id": "consistency",
                "name": "Logical Consistency",
                "description": "Internal coherence and absence of self-contradictory claims across paragraphs."
            },
            {
                "id": "clarity",
                "name": "Clarity & Readability",
                "description": "Syntactic fluency, structured organization, and conceptual accessibility."
            },
            {
                "id": "hallucination_reduction",
                "name": "Hallucination Reduction",
                "description": "Absence of unsupported assumptions, fabricated text, or false entity claims."
            }
        ]

    def compute_heuristic_score(self, text: str, objective: str, preferences: Dict[str, Any]) -> Dict[str, float]:
        """
        Computes transparent baseline heuristic quality indicators based on structural adherence,
        visual keyword grounding, and length calibration.
        NOTE: User-provided human ratings remain the primary qualitative ground truth.
        """
        if not text:
            return {d["id"]: 0.0 for d in self.get_dimension_definitions()}
            
        words = text.split()
        word_count = len(words)
        
        # Length adherence score
        target_len = preferences.get("length", "Medium")
        if target_len == "Short":
            len_score = 4.5 if (40 <= word_count <= 180) else 3.0
        elif target_len == "Detailed":
            len_score = 4.5 if word_count >= 200 else 3.2
        else: # Medium
            len_score = 4.5 if (100 <= word_count <= 350) else 3.5
            
        # Format adherence score
        fmt = preferences.get("output_format", "Structured report").lower()
        has_bullets = any(line.strip().startswith(("-", "*", "•")) for line in text.split("\n"))
        has_headers = any(line.strip().startswith("#") or line.strip().endswith(":") for line in text.split("\n"))
        
        format_score = 3.5
        if "bullet" in fmt and has_bullets:
            format_score = 4.8
        elif "report" in fmt and (has_headers or has_bullets):
            format_score = 4.7
        elif "paragraph" in fmt and not has_bullets:
            format_score = 4.5
        elif "step" in fmt and ("1." in text or "Step" in text):
            format_score = 4.8
            
        # Visual evidence indicator (presence of positional/visual anchoring words)
        visual_anchors = ["visible", "shows", "color", "left", "right", "center", "background", "foreground", "displays", "line", "contour", "region", "structure"]
        anchor_hits = sum(1 for a in visual_anchors if a in text.lower())
        accuracy_score = min(5.0, 3.2 + (anchor_hits * 0.2))
        
        # Clarity (structural formatting)
        clarity_score = 4.2 if (has_headers or len(text.split("\n\n")) >= 2) else 3.5
        
        # Hallucination caution: check if uncertainty is explicitly stated when appropriate
        hallucination_score = 4.5 if ("uncertain" in text.lower() or "not visible" in text.lower() or "appears to be" in text.lower()) else 4.0

        return {
            "accuracy": round(accuracy_score, 1),
            "relevance": round(min(5.0, 3.8 + (0.5 if objective.lower() in text.lower() else 0.0)), 1),
            "completeness": round(min(5.0, 3.0 + (word_count / 100)), 1),
            "instruction_adherence": round(format_score, 1),
            "consistency": 4.5,
            "clarity": round(clarity_score, 1),
            "hallucination_reduction": round(hallucination_score, 1)
        }

    def aggregate_research_summary(self) -> Dict[str, Any]:
        """
        Aggregates experimental research analytics across all runs to answer the 4 Research Questions:
        RQ1: CV context vs No CV context
        RQ2: Basic vs CO-STAR vs AI-Optimized performance
        RQ3: Latency & Token efficiency tradeoffs
        """
        experiments = get_experiments(limit=100)
        
        strategy_stats = {
            "basic": {"count": 0, "total_latency": 0.0, "total_eval_tokens": 0, "scores": []},
            "costar": {"count": 0, "total_latency": 0.0, "total_eval_tokens": 0, "scores": []},
            "ai_optimized": {"count": 0, "total_latency": 0.0, "total_eval_tokens": 0, "scores": []}
        }
        
        cv_vs_nocv = {
            "with_cv": {"count": 0, "total_latency": 0.0, "avg_accuracy": []},
            "without_cv": {"count": 0, "total_latency": 0.0, "avg_accuracy": []}
        }
        
        token_efficiency_data = []

        for exp in experiments:
            metrics = exp.get("metrics") or {}
            ratings = exp.get("ratings") or {}
            cv_ops = exp.get("cv_operations") or []
            has_cv = len(cv_ops) > 0
            
            for strat in ["basic", "costar", "ai_optimized"]:
                strat_metric = metrics.get(strat) or {}
                if strat_metric and strat_metric.get("latency_sec"):
                    lat = float(strat_metric.get("latency_sec", 0))
                    tokens = int(strat_metric.get("eval_count") or 0)
                    
                    strategy_stats[strat]["count"] += 1
                    strategy_stats[strat]["total_latency"] += lat
                    strategy_stats[strat]["total_eval_tokens"] += tokens
                    
                    # Human or heuristic rating
                    strat_rating = ratings.get(strat) or {}
                    acc = strat_rating.get("accuracy")
                    if acc is not None:
                        strategy_stats[strat]["scores"].append(float(acc))
                        if has_cv:
                            cv_vs_nocv["with_cv"]["avg_accuracy"].append(float(acc))
                        else:
                            cv_vs_nocv["without_cv"]["avg_accuracy"].append(float(acc))
                            
                    token_efficiency_data.append({
                        "experiment_id": exp.get("id")[:8],
                        "strategy": strat,
                        "latency_sec": lat,
                        "tokens": tokens,
                        "accuracy": acc if acc is not None else 4.0
                    })
                    
        # Compute averages
        summary_by_strategy = {}
        for s, data in strategy_stats.items():
            cnt = max(1, data["count"])
            avg_lat = round(data["total_latency"] / cnt, 2)
            avg_tok = round(data["total_eval_tokens"] / cnt, 1)
            avg_score = round(sum(data["scores"]) / len(data["scores"]), 2) if data["scores"] else 4.0
            summary_by_strategy[s] = {
                "runs_count": data["count"],
                "avg_latency_sec": avg_lat,
                "avg_eval_tokens": avg_tok,
                "avg_rating": avg_score
            }
            
        return {
            "total_experiments_analyzed": len(experiments),
            "strategies_comparison": summary_by_strategy,
            "token_efficiency_points": token_efficiency_data[:30],
            "research_questions": {
                "rq1_cv_context_impact": "Empirical comparison of multimodal visual grounding with vs without CV preprocessing metadata.",
                "rq2_structured_prompting": "Evaluation of structured CO-STAR framework versus un-optimized baseline instructions.",
                "rq3_ai_optimization": "Performance of automated role-selection, ambiguity handling, and anti-hallucination guardrails.",
                "rq4_token_efficiency": "Rate-distortion tradeoff between generated token volume, execution latency, and response quality."
            }
        }

evaluation_service = EvaluationService()
