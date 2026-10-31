from typing import Dict, Any

ROLE_MAP = {
    "Summarise": "Senior Multimodal Information Synthesis Specialist and Lead Research Analyst",
    "Analyse": "Principal Computer Vision and Visual Data Diagnostics Engineer",
    "Evaluate": "Lead Quality Assurance Architect and Visual Evaluation Specialist",
    "Explain": "Distinguished Technical Educator and Science Communicator",
    "Teach": "Master Pedagogy Director and Interactive Learning Specialist"
}

def format_cv_metadata_for_prompt(cv_meta: Dict[str, Any]) -> str:
    """Transforms raw CV processing results into structured, concise prompt context."""
    if not cv_meta:
        return "No automated Computer Vision pre-processing metadata was attached for this run."
        
    lines = []
    if "source_dimensions" in cv_meta:
        lines.append(f"- Native Resolution: {cv_meta['source_dimensions']} (Channels: {cv_meta.get('source_channels', 3)})")
        
    # Check specific operation metadata keys
    for k, v in cv_meta.items():
        if k in ["source_dimensions", "source_channels", "operations_executed"]:
            continue
        if isinstance(v, dict):
            op_title = v.get("algorithm") or v.get("filter") or v.get("transformation") or k.replace('_', ' ').title()
            desc = v.get("description", "")
            
            key_metrics = []
            if "shannon_entropy" in v:
                key_metrics.append(f"Shannon Entropy: {v['shannon_entropy']} bits")
            if "edge_density_pct" in v:
                key_metrics.append(f"Canny Edge Density: {v['edge_density_pct']}%")
            if "total_contours_found" in v:
                key_metrics.append(f"Topological Contours: {v['total_contours_found']}")
            if "extracted_bounding_boxes" in v:
                key_metrics.append(f"Salient Bounding Boxes: {v['extracted_bounding_boxes']}")
            if "keypoints_detected" in v:
                key_metrics.append(f"ORB Keypoints: {v['keypoints_detected']}")
            if "detected_faces_count" in v:
                key_metrics.append(f"Detected Face Regions: {v['detected_faces_count']}")
            if "identified_catchment_basins" in v:
                key_metrics.append(f"Watershed Basins: {v['identified_catchment_basins']}")
            if "total_graph_components" in v:
                key_metrics.append(f"Graph Segments: {v['total_graph_components']}")
            if "low_frequency_energy_percentage" in v:
                key_metrics.append(f"Fourier Low-Freq Energy: {v['low_frequency_energy_percentage']}%")
                
            metrics_str = f" ({', '.join(key_metrics)})" if key_metrics else ""
            lines.append(f"- [{op_title}]: {desc}{metrics_str}")
            
    if not lines:
        return "Computer Vision operations executed successfully; see processed images for visual evidence."
        
    return "\n".join(lines)

def generate_ai_optimized_prompt(
    objective: str,
    preferences: Dict[str, Any],
    cv_metadata: Dict[str, Any]
) -> str:
    """
    Strategy 3: AI-Generated Optimized Prompting.
    Implements automated role selection, prompt chaining structure, CV metadata grounding,
    strict anti-hallucination guardrails, and uncertainty calibration.
    """
    role = ROLE_MAP.get(objective, "Senior Computer Vision and Prompt Engineering Researcher")
    audience = preferences.get("audience", "Student")
    tone = preferences.get("tone", "Professional")
    output_format = preferences.get("output_format", "Structured report")
    length = preferences.get("length", "Medium")
    advanced_inst = preferences.get("advanced_instructions", "")
    
    cv_context_text = format_cv_metadata_for_prompt(cv_metadata)
    
    prompt = (
        f"### SYSTEM ROLE & PERSONA:\n"
        f"You are the {role}. You specialize in rigorous multimodal visual reasoning, "
        f"grounded in empirical Computer Vision measurements and zero tolerance for fabricated observations.\n\n"
        
        f"### COMPUTER VISION EXTRACTED CONTEXT (EMPIRICAL SENSOR GROUNDING):\n"
        f"{cv_context_text}\n\n"
        
        f"### PRIMARY OBJECTIVE & USER PREFERENCES:\n"
        f"- Target Objective: {objective.upper()}\n"
        f"- Target Audience: {audience} (level-appropriate conceptual depth and terminology)\n"
        f"- Preferred Tone: {tone}\n"
        f"- Desired Output Format: {output_format}\n"
        f"- Scope Length: {length}\n"
        + (f"- Custom Instructions: {advanced_inst}\n" if advanced_inst else "") +
        f"\n"
        
        f"### CHAIN-OF-THOUGHT EXECUTION DIRECTIVES:\n"
        f"Follow this structured 3-phase reasoning protocol:\n"
        f"1. Visual Grounding Phase: Identify visible focal entities, layouts, textures, or text. "
        f"Correlate them with the CV metadata reported above (e.g. edge density, contours, frequency distribution).\n"
        f"2. Analytical Synthesis Phase: Fulfill the '{objective}' objective directly. Maintain strict logical coherence.\n"
        f"3. Calibration & Formatting Phase: Present the final response strictly in '{output_format}' matching '{length}'.\n\n"
        
        f"### UNCERTAINTY & ANTI-HALLUCINATION GUARDRAILS:\n"
        f"- Never invent or assume non-visible details (e.g., do not fabricate exact product models, identities, or unreadable fine text).\n"
        f"- If an area is blurry, occluded, or visually ambiguous, explicitly state: '[Visual Uncertainty: ...]' rather than guessing.\n"
        f"- Anchor all factual statements to clear visual evidence visible in the image."
    )
    return prompt
