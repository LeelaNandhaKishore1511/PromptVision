# Research Methodology — PromptVision

## 1. Research Objectives & Problem Formulation

Traditional multimodal interaction relies on manual, ad-hoc prompt crafting by end-users. This leads to high prompt variability, inconsistent model outputs, visual hallucinations, and inefficient token usage.

**PromptVision** formulates an option-driven alternative where:
1. Users specify intent via structured choices (Objective, Audience, Tone, Format, Scope).
2. The system executes empirical Computer Vision algorithms to extract deterministic visual metadata (edges, contours, frequency distribution, segments).
3. The system generates prompts across three distinct strategies and benchmarks them against the SAME local Vision-Language Model.

---

## 2. The Four Core Research Questions

### Research Question 1 (RQ1): Impact of CV Context
*Does supplementing raw visual inputs with empirical Computer Vision metadata improve multimodal response quality?*
- **Hypothesis**: Supplying explicit measurements (e.g., Canny edge density, contour counts, Shannon entropy) acts as an empirical sensor anchor, reducing speculative claims and improving structural accuracy.
- **Experimental Protocol**: Compare response quality for identical prompts with versus without attached CV metadata.

### Research Question 2 (RQ2): Structured Prompting vs Baseline
*Does structured framework prompting (CO-STAR) outperform basic direct instructions?*
- **Hypothesis**: Structuring context through Context, Objective, Style, Tone, Audience, and Response format provides higher instruction adherence and length calibration than unconstrained prompt anatomy.
- **Experimental Protocol**: Benchmark Strategy 1 (Basic Baseline) vs Strategy 2 (CO-STAR) across diverse image types (photographs, charts, diagrams, text documents).

### Research Question 3 (RQ3): Automated Optimization & Guardrails
*Does automated role persona selection and negative constraint injection reduce multimodal hallucinations?*
- **Hypothesis**: Role-specialization combined with mandatory uncertainty declarations (`"[Visual Uncertainty: ...]"`) forces the model to acknowledge low-confidence visual areas rather than fabricating details.
- **Experimental Protocol**: Evaluate Strategy 3 (AI-Optimized) against Strategy 1 and Strategy 2 on ambiguous or low-contrast visual samples.

### Research Question 4 (RQ4): Rate-Distortion & Token Efficiency
*What is the quantitative relationship between response quality, token volume, and execution latency?*
- **Hypothesis**: Quality gains exhibit diminishing returns beyond an optimal token budget (~250-350 tokens). Excessive verbosity increases CPU latency linearly without proportional accuracy gain.
- **Experimental Protocol**: Plot quality ratings versus total token count ($Quality / 1000 \text{ tokens}$) and execution latency (seconds).

---

## 3. Controlled Experimental Variables

To maintain scientific validity:
- **Independent Variable**: Prompt engineering strategy (Basic vs CO-STAR vs AI-Optimized) and CV context presence.
- **Dependent Variables**: 7 qualitative evaluation dimensions, inference duration (seconds), prompt tokens, generated tokens, and tokens per second.
- **Controlled Variables**: The identical image file, identical user preferences, and identical Vision-Language Model (`qwen2.5vl:3b`) across all strategies in an experimental run.
