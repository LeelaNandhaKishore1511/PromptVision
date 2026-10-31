# Prompt Engineering Syllabus Mapping — PromptVision

This document details the complete mapping of the five Prompt Engineering syllabus units implemented in the PromptVision platform.

---

## UNIT 1: Foundations of Prompt Engineering and LLMs

### Syllabus Topics
- Evolution of LLMs and multimodal vision-language models.
- Mathematical mechanics: tokenization, vocabulary embeddings, context windows.
- Role of prompt engineering as an interface layer.
- Applications in education, research, healthcare, and engineering.

### Platform Implementation (`frontend/src/pages/PromptLab.jsx`)
1. **Interactive Tokenizer vs Character/Word Demonstrator**:
   - Compares raw character length, whitespace-delimited word counts, and Byte-Pair Encoding (BPE) subword token counts.
   - Clarifies why subword tokens govern latency, cost, and memory rather than characters.
2. **Context Window Attention Horizon Explorer**:
   - Visualizes allocation against the 4096-token Ollama local buffer.
   - Demonstrates how visual image tokens (patch embeddings) occupy the shared attention window alongside prompt text.
3. **Multimodal Domain Application Benchmarks**:
   - Interactive examples in Education, Healthcare, Software Engineering, and Computer Vision diagnostics.

---

## UNIT 2: Prompt Design Fundamentals

### Syllabus Topics
- Prompt anatomy: Instruction, Context, Input, Output Format, Constraints.
- Zero-shot, One-shot, and Few-shot prompting methodologies.
- Clarity, precision, tone, and length control.
- Task-specific formulations (Summarization, Explanation, Question Answering).

### Platform Implementation (`backend/app/prompting/strategies/basic.py`)
1. **The 5-Part Prompt Anatomy Builder**:
   - Interactive UI allowing learners to assemble prompts from foundational components:
     1. **Instruction**: Unambiguous directive.
     2. **Context**: Operational domain background.
     3. **Input Data**: Visual reference image.
     4. **Output Format**: Structural specification (bulleted list, structured report, table).
     5. **Constraints**: Methodological boundaries (e.g. no speculation, state uncertainty).
2. **Strategy 1 (Basic Prompting Baseline)**:
   - Evaluates pure zero-shot prompts constructed strictly according to prompt anatomy without few-shot examples or iterative optimization, serving as the experimental control baseline.

---

## UNIT 3: Advanced Prompting Strategies

### Syllabus Topics
- Role/persona-based prompting.
- The CO-STAR framework.
- Prompt chaining and multi-stage reasoning.
- Iterative prompt refinement and ambiguity resolution.

### Platform Implementation (`backend/app/prompting/frameworks/costar.py` & `ai_optimized.py`)
1. **CO-STAR Framework (Strategy 2)**:
   - Systematically structures prompt context across 6 dimensions:
     - **[C] Context**: Situation background.
     - **[O] Objective**: Primary task goal.
     - **[S] Style**: Writing manner (academic, concise).
     - **[T] Tone**: Emotional resonance (professional, technical).
     - **[A] Audience**: Tailored depth (beginner, student, expert, researcher).
     - **[R] Response Format**: Structural delivery (table, step-by-step, report).
   - Supports zero-shot, one-shot, and few-shot exemplars tailored by objective.
2. **Role Persona Engineering & Multi-Stage Prompt Chaining (Strategy 3)**:
   - Dynamic persona assignment (e.g., Principal Computer Vision Engineer).
   - 3-Phase reasoning protocol: (1) Visual Grounding -> (2) Sensor & CV Synthesis -> (3) Calibrated Delivery.

---

## UNIT 4: Prompt Engineering Tools, Applications & Evaluation

### Syllabus Topics
- Integration with external frameworks (LangChain, LCEL).
- Local vs Cloud model comparison tradeoffs.
- Controlled A/B testing methodology.
- Multi-dimensional response evaluation.

### Platform Implementation (`backend/app/evaluation/eval_service.py`)
1. **Controlled A/B Testing Execution**:
   - Executes identical visual inputs across Strategy 1, Strategy 2, and Strategy 3 sequentially through the identical local vision-language model (`qwen2.5vl:3b`).
2. **7 Balanced Evaluation Dimensions**:
   - Accuracy, Relevance, Completeness, Instruction Adherence, Consistency, Clarity, and Hallucination Reduction.
3. **Actual Token & Latency Analytics**:
   - Directly extracts provider metrics (`prompt_eval_count`, `eval_count`, `latency_sec`, `tokens_per_sec`) from Ollama's API response.

---

## UNIT 5: Ethics, Automation & Capstone

### Syllabus Topics
- Multimodal AI safety, bias mitigation, and privacy preservation.
- Negative constraints and anti-hallucination guardrails.
- Uncertainty handling and confidence calibration.
- Option-driven automated prompt synthesis.

### Platform Implementation
1. **Automated Prompt Construction**:
   - Users select visual objectives and structured preferences via cards and MCQs, completely eliminating manual prompt formulation.
2. **Anti-Hallucination Guardrails & Negative Constraints**:
   - Strategy 3 explicitly incorporates negative constraints forbidding speculative claims.
   - Enforces uncertainty declarations (`"[Visual Uncertainty: ...]"` when features are occluded or low-contrast).
3. **Privacy Preserving Geometry**:
   - CV Module 3 face detection detects geometric bounding coordinates without facial recognition or identity tracking.
