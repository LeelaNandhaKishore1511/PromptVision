# Project Overview — PromptVision

**PromptVision: An Option-Driven Automated Prompt Engineering and Computer Vision Analysis Framework**  
*A Final Year B.Tech Project in Artificial Intelligence and Machine Learning*

---

## 1. Executive Summary

PromptVision addresses a critical bottleneck in multimodal artificial intelligence: **the friction, inconsistency, and vulnerability of manual text prompt crafting**. 

In conventional vision-language model (VLM) usage, end-users are forced to guess prompt formulations, often omitting critical domain constraints, hallucinating non-existent objects, or failing to communicate exact structural requirements.

PromptVision introduces a deterministic, option-driven research framework that:
1. Accepts user images and allows users to define their goal via structured selection cards (*Summarise, Analyse, Evaluate, Explain, Teach*).
2. Collects structured multiple-choice preferences (Audience level, Tone, Format, Scope, and negative constraints).
3. Executes deterministic Computer Vision algorithms (OpenCV, scikit-image, SciPy, PyWavelets) across 5 B.Tech syllabus modules.
4. Extracts factual mathematical and topological features (Shannon entropy, Canny edge density, contours, frequency distribution).
5. Synthesizes three distinct Prompt Engineering strategies:
   - **Strategy 1 (Basic Prompting)**: Direct prompt anatomy baseline.
   - **Strategy 2 (Framework-Based Prompting)**: CO-STAR methodology with zero/one/few-shot exemplars.
   - **Strategy 3 (AI-Generated Optimized Prompting)**: Automated role persona, CV sensor grounding, uncertainty calibration, and negative anti-hallucination guardrails.
6. Executes all three strategies sequentially on the **exact same selected local Vision-Language Model** (`qwen2.5vl:3b` default).
7. Evaluates outputs across 7 balanced qualitative dimensions and extracts actual Ollama token statistics (`prompt_eval_count`, `eval_count`, `latency_sec`, `tokens_per_sec`).
8. Provides an interactive **Teach Mode** for learning visual concepts and testing comprehension with automated scoring.

---

## 2. Key Research Contributions

1. **Option-Driven Interface**: Eliminates the manual "blank text box" paradigm for multimodal prompts, transforming free-form text input into structured, reproducible preference vectors.
2. **Empirical Computer Vision Grounding**: Proves that feeding deterministic CV-derived measurements (edges, frequency ratios, contours) directly into VLM prompt context significantly reduces visual hallucinations.
3. **Controlled Multi-Strategy Benchmark**: Provides the first unified educational workbench comparing Basic Anatomy, CO-STAR, and AI-Optimized prompts under identical model and hardware conditions.
4. **Hardware-Safe Local Execution**: Demonstrates high-utility multimodal AI inference completely offline on standard commodity laptop hardware (Intel Core i5, 16GB RAM, no dedicated GPU).
