from typing import Dict, Any

BASIC_OBJECTIVE_TEMPLATES = {
    "Summarise": (
        "Instruction: Summarise the uploaded image clearly.\n"
        "Context: General visual observation.\n"
        "Input: Visual image content.\n"
        "Output format: Short paragraph summarizing the primary elements.\n"
        "Constraints: Stick strictly to what is clearly visible without speculation."
    ),
    "Analyse": (
        "Instruction: Analyse the visual contents and structure of this image.\n"
        "Context: General image analysis.\n"
        "Input: Visual image data.\n"
        "Output format: Concise bullet points listing the key components and their visual relationships.\n"
        "Constraints: Limit to factual observations directly verifiable in the image."
    ),
    "Evaluate": (
        "Instruction: Evaluate the visual quality, composition, and presentation of the image.\n"
        "Context: Visual inspection and quality assessment.\n"
        "Input: Uploaded visual image.\n"
        "Output format: Brief structured critique with strengths and limitations.\n"
        "Constraints: Provide objective feedback based only on the visible image properties."
    ),
    "Explain": (
        "Instruction: Explain what this image portrays and the significance of its visible components.\n"
        "Context: Educational explanation for an interested observer.\n"
        "Input: Uploaded visual diagram or scene.\n"
        "Output format: Clear step-by-step explanation.\n"
        "Constraints: Avoid overly complex jargon and explain visible parts directly."
    ),
    "Teach": (
        "Instruction: Teach a student the main concept shown in this image.\n"
        "Context: Fundamental learning assistance.\n"
        "Input: Visual learning material.\n"
        "Output format: Beginner-friendly lesson with key terms defined.\n"
        "Constraints: Focus only on concepts visually depicted in the image."
    )
}

def generate_basic_prompt(objective: str, preferences: Dict[str, Any]) -> str:
    """
    Strategy 1: Basic Prompting.
    Establishes an un-optimized, direct baseline adhering to the 5 prompt anatomy components:
    Instruction, Context, Input, Output Format, Constraints.
    """
    clean_obj = objective.capitalize() if objective else "Analyse"
    template = BASIC_OBJECTIVE_TEMPLATES.get(clean_obj, BASIC_OBJECTIVE_TEMPLATES["Analyse"])
    
    # Minimal direct prompt adhering strictly to baseline definition
    prompt = (
        f"You are an image analysis assistant.\n\n"
        f"Prompt Anatomy:\n{template}\n\n"
        f"Please proceed with the instruction for the provided image."
    )
    return prompt
