from typing import Dict, Any, Tuple
from .strategies.basic import generate_basic_prompt
from .frameworks.costar import generate_costar_prompt
from .refinement.ai_optimized import generate_ai_optimized_prompt

class PromptService:
    def generate_all_strategies(
        self,
        objective: str,
        preferences: Dict[str, Any],
        cv_metadata: Dict[str, Any]
    ) -> Dict[str, str]:
        """
        Generates three distinct prompts:
        1. Basic Prompting (Direct baseline with prompt anatomy)
        2. Framework-Based Prompting (CO-STAR with zero/one/few-shot exemplars)
        3. AI-Generated Optimized Prompting (CV grounding, role persona, anti-hallucination guardrails)
        """
        basic = generate_basic_prompt(objective, preferences)
        costar = generate_costar_prompt(objective, preferences)
        ai_opt = generate_ai_optimized_prompt(objective, preferences, cv_metadata)
        
        return {
            "basic": basic,
            "costar": costar,
            "ai_optimized": ai_opt
        }

prompt_service = PromptService()
