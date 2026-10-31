# The Three Prompt Engineering Strategies — PromptVision

PromptVision implements exactly three distinct Prompt Engineering strategies to facilitate rigorous empirical comparison under identical experimental conditions.

All three strategies are executed against the **SAME selected Vision-Language Model** (`qwen2.5vl:3b` default) sequentially.

---

## Strategy 1: Basic Prompting (Experimental Control Baseline)
Located in: [`backend/app/prompting/strategies/basic.py`](file:///C:/Users/Nandhu/Documents/PromptVision/backend/app/prompting/strategies/basic.py)

### Purpose
To establish an un-optimized, direct, zero-shot control baseline that reflects how typical non-expert users query vision-language models.

### Architectural Structure
Adheres strictly to the 5-part prompt anatomy without advanced optimizations:
```text
You are an image analysis assistant.

Prompt Anatomy:
Instruction: [Objective-specific directive: Summarise / Analyse / Evaluate / Explain / Teach]
Context: General visual observation.
Input: Visual image content.
Output format: Concise response.
Constraints: Stick strictly to what is clearly visible without speculation.

Please proceed with the instruction for the provided image.
```

### Characteristics
- Zero-shot (no reference exemplars).
- No automatic persona adaptation.
- No CV sensor metadata included.
- Minimal structural constraints.

---

## Strategy 2: Framework-Based Prompting (CO-STAR)
Located in: [`backend/app/prompting/frameworks/costar.py`](file:///C:/Users/Nandhu/Documents/PromptVision/backend/app/prompting/frameworks/costar.py)

### Purpose
To evaluate the impact of structured contextual framing using the industry-standard **CO-STAR** methodology.

### Architectural Structure
Organized strictly into six distinct sections:
```text
### CO-STAR FRAMEWORK SPECIFICATION

[C] CONTEXT:
[Situational background tailored to the research objective]

[O] OBJECTIVE:
Perform a comprehensive '[Objective]' of the uploaded image strictly aligned with user-specified preferences.

[S] STYLE:
[Style guidelines: Define technical terms, incorporate visual examples, state limitations]

[T] TONE:
[Tone selection: Simple / Professional / Academic / Technical]

[A] AUDIENCE:
Tailored specifically for a [Audience: Beginner / Student / Intermediate / Expert / Researcher] audience.

[R] RESPONSE FORMAT:
Present your response in '[Format: Structured report / Bullet points / Step-by-step / Table]' style with a target length of '[Length: Short / Medium / Detailed]'.

### DEMONSTRATION EXEMPLARS (Optional One-Shot or Few-Shot):
[Domain-relevant reference examples]
```

### Characteristics
- Fully incorporates user-selected MCQ preferences (Audience, Tone, Format, Length).
- Supports user-selectable zero-shot, one-shot, and few-shot exemplar modes.
- Enforces strict stylistic boundaries.

---

## Strategy 3: AI-Generated Optimized Prompt
Located in: [`backend/app/prompting/refinement/ai_optimized.py`](file:///C:/Users/Nandhu/Documents/PromptVision/backend/app/prompting/refinement/ai_optimized.py)

### Purpose
To maximize factual visual grounding, eliminate hallucinations, and calibrate uncertainty through automated persona engineering and deterministic Computer Vision context injection.

### Architectural Structure
```text
### SYSTEM ROLE & PERSONA:
You are the [Dynamically Selected Persona: e.g. Principal Computer Vision & Diagnostics Engineer]. You specialize in rigorous multimodal visual reasoning grounded in empirical Computer Vision measurements and zero tolerance for fabricated observations.

### COMPUTER VISION EXTRACTED CONTEXT (EMPIRICAL SENSOR GROUNDING):
- Native Resolution: [Width]x[Height] px (Channels: [Ch])
- [Canny Edge Detection]: Multi-stage edge detection (Edge Density: 14.2%)
- [Topological Contours]: Extracted 38 boundary contours (Largest Area: 4520.5 px)
- [Shannon Entropy]: Pixel intensity entropy 7.42 bits
- [Fourier Transform]: Low-frequency spectral energy 84.6%

### PRIMARY OBJECTIVE & USER PREFERENCES:
- Target Objective: [Objective]
- Target Audience: [Audience]
- Preferred Tone: [Tone]
- Desired Output Format: [Format]
- Scope Length: [Length]

### CHAIN-OF-THOUGHT EXECUTION DIRECTIVES:
Follow this structured 3-phase reasoning protocol:
1. Visual Grounding Phase: Identify visible focal entities and correlate them with the CV metadata reported above.
2. Analytical Synthesis Phase: Fulfill the objective directly with strict logical coherence.
3. Calibration & Formatting Phase: Present the final response strictly in the desired output format.

### UNCERTAINTY & ANTI-HALLUCINATION GUARDRAILS:
- Never invent or assume non-visible details (e.g. do not fabricate exact product models, identities, or unreadable fine text).
- If an area is blurry, occluded, or visually ambiguous, explicitly state: '[Visual Uncertainty: ...]' rather than guessing.
- Anchor all factual statements to clear visual evidence visible in the image.
```

### Characteristics
- Dynamically injects factual measurements from OpenCV/skimage pre-processing.
- Enforces a 3-phase chain-of-thought execution protocol.
- Includes mandatory negative constraints and explicit uncertainty declarations.
- Tailored for high-precision scientific analysis.

---

## Summary Comparison Matrix

| Property | Strategy 1 (Basic) | Strategy 2 (CO-STAR) | Strategy 3 (AI-Optimized) |
|---|---|---|---|
| **Underlying VLM** | Selected Model (e.g. `qwen2.5vl:3b`) | **Same Selected Model** | **Same Selected Model** |
| **Input Image** | Raw Image | Raw Image | Raw Image + Processed Visuals |
| **CV Sensor Context** | None | None | **Full Extracted CV Metadata** |
| **Persona Assignment** | Generic Assistant | Calibrated Voice | Specialized Domain Scientist |
| **MCQ Preference Calibration** | Minimal | High (Tone, Audience, Format) | Complete (Audience, Tone, Format, Custom) |
| **Exemplars** | Zero-Shot Only | Zero, One, or Few-Shot | Structured Protocol Demonstration |
| **Anti-Hallucination Guardrails** | Basic negative constraint | Moderate stylistic guidelines | **Mandatory Uncertainty Directives** |
| **Typical Word Count** | 50 – 70 words | 130 – 170 words | 300 – 400 words |
