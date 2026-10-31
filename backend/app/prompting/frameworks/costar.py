from typing import Dict, Any, List

# Exemplars for Few-Shot Prompting tailored by objective
EXEMPLARS = {
    "Summarise": [
        {
            "input": "Image of a classroom with teacher pointing at a whiteboard showing a quadratic equation.",
            "output": "Summary: An educational setting showing a mathematics instructor actively teaching quadratic formulas on a whiteboard to attentive students, emphasizing algebraic derivation."
        },
        {
            "input": "Image of an urban street intersection during evening rain with neon storefronts reflecting on wet asphalt.",
            "output": "Summary: A nocturnal metropolitan street scene characterized by wet, reflective asphalt surfaces capturing multicolored neon illumination from adjacent commercial signage."
        }
    ],
    "Analyse": [
        {
            "input": "Technical bar chart of quarterly clean energy adoption.",
            "output": "Analysis:\n- Primary Subject: Temporal solar vs. wind adoption across Q1-Q4.\n- Visual Salience: Highest peak in Q3 for solar (42% increase).\n- Structural Layout: Dual vertical bar groupings with discrete legend and percentage y-axis."
        },
        {
            "input": "Circuit schematic with resistors, capacitors, and an operational amplifier.",
            "output": "Analysis:\n- Component Topology: Non-inverting operational amplifier configuration with feedback resistor Rf.\n- Signal Pathway: Input source coupled to non-inverting pin; dual DC voltage rails indicated.\n- State / Conditions: Closed-loop gain determined by standard (1 + Rf/R1) ratio."
        }
    ],
    "Evaluate": [
        {
            "input": "Infographic depicting global carbon emission breakdowns.",
            "output": "Evaluation:\n- Strengths: High legibility with distinct color contrast for top 5 sectors; clean typography.\n- Limitations: Lacks absolute gigaton metrics on secondary wedges; time baseline is unspecified.\n- Verdict: Effective high-level summary but insufficient for quantitative research reproduction."
        }
    ],
    "Explain": [
        {
            "input": "Cross-section diagram of human eye showing cornea, lens, and retina.",
            "output": "Explanation:\n1. Light Entry: Incident light rays first pass through the clear cornea, which performs initial optical refraction.\n2. Focusing: The adjustable crystalline lens dynamically fine-tunes focal length.\n3. Transduction: Photoreceptor rods and cones on the retina convert photons into electrical impulses for the optic nerve."
        }
    ],
    "Teach": [
        {
            "input": "Diagram of photosynthesis in a green leaf.",
            "output": "Lesson:\n- Core Concept: Photosynthesis converts sunlight into biochemical energy (sugar).\n- Key Formula: Carbon Dioxide + Water + Sunlight -> Glucose + Oxygen.\n- Real-World Analogy: Think of the chloroplast as a miniature solar-powered kitchen that feeds the plant and purifies our air."
        }
    ]
}

def generate_costar_prompt(objective: str, preferences: Dict[str, Any]) -> str:
    """
    Strategy 2: Framework-Based Prompting (CO-STAR).
    Structures prompt strictly according to Context, Objective, Style, Tone, Audience, Response format.
    Incorporates zero-shot / one-shot / few-shot exemplars and MCQ preferences.
    """
    audience = preferences.get("audience", "Student")
    tone = preferences.get("tone", "Professional")
    output_format = preferences.get("output_format", "Structured report")
    length = preferences.get("length", "Medium")
    few_shot_setting = preferences.get("few_shot_setting", "zero-shot")
    
    include_examples = preferences.get("include_examples", True)
    explain_terms = preferences.get("explain_terms", True)
    include_limitations = preferences.get("include_limitations", True)
    include_visual_evidence = preferences.get("include_visual_evidence", True)
    
    # Map objective to specific context description
    obj_context_map = {
        "Summarise": "You are examining an uploaded image that requires a high-fidelity visual summary capturing the core subject, setting, and notable elements.",
        "Analyse": "You are conducting an in-depth visual and structural decomposition of an uploaded image, identifying relationships, components, spatial hierarchy, and visual anomalies.",
        "Evaluate": "You are performing a rigorous, critical appraisal of the provided image, assessing its visual clarity, informational fidelity, design quality, and potential weaknesses.",
        "Explain": "You are providing an educational and conceptual explanation of the phenomena, artifacts, or ideas represented in this image.",
        "Teach": "You are delivering a pedagogical lesson centered on the provided image, guiding a learner from foundational intuition to deeper conceptual grasp."
    }
    
    context = obj_context_map.get(objective, f"You are examining an image to provide a thorough {objective.lower()} for our research framework.")
    
    # Guidelines based on preferences
    style_guidelines = []
    if explain_terms:
        style_guidelines.append("Define specialized technical terms when introduced.")
    if include_examples:
        style_guidelines.append("Incorporate concrete visual examples directly tied to visible entities.")
    if include_limitations:
        style_guidelines.append("Explicitly state any visual ambiguities, occlusions, or limitations observed.")
    if include_visual_evidence:
        style_guidelines.append("Ground assertions in specific visual evidence (e.g. spatial position, colors, contours, text markings).")
    
    style_text = "; ".join(style_guidelines) if style_guidelines else "Objective, clear, and analytical."

    costar_sections = [
        "### CO-STAR FRAMEWORK SPECIFICATION",
        f"[C] CONTEXT:\n{context}",
        f"[O] OBJECTIVE:\nPerform a comprehensive '{objective}' of the uploaded image strictly aligned with user-specified preferences.",
        f"[S] STYLE:\n{style_text}",
        f"[T] TONE:\n{tone} (maintain an articulate, rigorous, and respectful voice).",
        f"[A] AUDIENCE:\nTailored specifically for a {audience} audience (calibrate vocabulary, technical depth, and assumptions accordingly).",
        f"[R] RESPONSE FORMAT:\nPresent your response in '{output_format}' style with a target length of '{length}'."
    ]
    
    # Handle Few-Shot exemplars if requested
    exemplar_list = EXEMPLARS.get(objective, EXEMPLARS["Analyse"])
    if few_shot_setting == "one-shot" and exemplar_list:
        ex = exemplar_list[0]
        costar_sections.append(
            f"\n### DEMONSTRATION EXEMPLAR (1-Shot Reference):\n"
            f"[Input Description]: {ex['input']}\n"
            f"[Reference Output]:\n{ex['output']}\n"
        )
    elif few_shot_setting == "few-shot" and exemplar_list:
        ex_text = "\n\n".join([f"Exemplar {i+1}:\nInput: {item['input']}\nOutput:\n{item['output']}" for i, item in enumerate(exemplar_list[:2])])
        costar_sections.append(f"\n### DEMONSTRATION EXEMPLARS (Few-Shot References):\n{ex_text}\n")
        
    costar_sections.append("Now, examine the provided image and generate your response strictly following the CO-STAR criteria above.")
    
    return "\n\n".join(costar_sections)
