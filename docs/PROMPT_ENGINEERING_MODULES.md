# Prompt Engineering Modules Specification — PromptVision

PromptVision provides an interactive pedagogical and experimental learning laboratory covering all five units of the modern Prompt Engineering and Large Language Model curriculum.

---

## Unit 1: Foundations of Prompt Engineering & LLMs
Located in: [`frontend/src/pages/PromptLab.jsx`](file:///C:/Users/Nandhu/Documents/PromptVision/frontend/src/pages/PromptLab.jsx)

### Key Educational Concepts:
- **Large Language Model Architecture**: Transformer self-attention mechanisms, token embeddings, and multimodal projection layers.
- **Tokens vs Words/Characters**: Why subword tokenization (Byte-Pair Encoding - BPE) dictates computational cost, inference latency, and context limits.
- **Multimodal Visual Tokenization**: How Vision-Language Models convert 2D image matrices into discrete patch embeddings (e.g. 14x14 pixel patches) projected into the language embedding space.

### Interactive Components:
- **Interactive Token Counter**: Real-time comparison between raw character length, whitespace word count, and estimated subword token counts.
- **Context Window Capacity Explorer**: Visual attention horizon tracker modeling memory consumption within the 4096-token Ollama context window.

---

## Unit 2: Prompt Design Fundamentals & Anatomy

### Key Educational Concepts:
- **The 5-Part Prompt Anatomy**:
  1. *Instruction*: Primary actionable directive.
  2. *Context*: Domain background and situation framing.
  3. *Input Data*: Visual reference data and extracted metadata.
  4. *Output Format*: Structural layout constraints (JSON, bulleted list, report, table).
  5. *Constraints*: Operational boundaries (no speculation, uncertainty declaration).
- **In-Context Learning Exemplars**: Zero-shot vs One-shot vs Few-shot calibration.

### Interactive Components:
- **Prompt Anatomy Builder**: Interactive UI where users configure each of the 5 anatomical parts, view the assembled zero-shot prompt, and inspect structural clarity.

---

## Unit 3: Advanced Prompting Strategies

### Key Educational Concepts:
- **The CO-STAR Framework**: Comprehensive prompt specification covering Context, Objective, Style, Tone, Audience, and Response format.
- **Role Persona Engineering**: Calibrating domain vocabulary, depth, and assumptions by assigning specialized personas (e.g., *Principal Computer Vision Engineer* vs *Pedagogy Specialist*).
- **Prompt Chaining**: Dividing monolithic generation tasks into structured sequential phases:
  - Phase 1: Feature Grounding (identify visible components).
  - Phase 2: Sensor & CV Synthesis (correlate with edge/entropy metrics).
  - Phase 3: Calibrated Delivery (format according to audience preferences).

### Interactive Components:
- **Prompt Chaining Simulator**: Visual step-by-step reasoning simulator demonstrating intermediate phase outputs.

---

## Unit 4: Tools, Applications & Evaluation

### Key Educational Concepts:
- **Prompt Orchestration Frameworks**: Overview of LangChain, LCEL (LangChain Expression Language), and automated prompt chaining.
- **A/B Testing Methodology**: Establishing fair, controlled experimental protocols by holding the underlying model, parameters, and input image strictly identical while varying only the prompt structure.
- **Multi-Dimensional Quality Assessment**: Evaluating multimodal generation across seven balanced dimensions rather than relying on subjective impressions or LLM self-evaluation.

---

## Unit 5: Ethics, Automation & Anti-Hallucination Guardrails

### Key Educational Concepts:
- **Negative Constraints**: Explicit negative instructions forbidding the generation of unverified brand names, dates, or identities.
- **Uncertainty Calibration**: Mandatory instruction directing the model to output `"[Visual Uncertainty: ...]"` whenever visual regions are blurry, occluded, or ambiguous.
- **Privacy Preservation**: Ensuring facial detection algorithms strictly detect bounding coordinates without performing biometric identity recognition.

### Interactive Components:
- **Automated Guardrail Evaluator**: Real-time prompt scanner verifying the presence of uncertainty directives, negative constraints, and visual evidence grounding.
