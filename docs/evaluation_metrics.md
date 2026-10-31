# Evaluation Metrics & Research Dimensions — PromptVision

PromptVision adopts a balanced qualitative and quantitative evaluation framework designed to benchmark multimodal vision-language model responses.

---

## 1. Qualitative Evaluation Dimensions (1 to 5 Scale)

Each model response is rated across seven balanced dimensions:

### 1. Accuracy & Visual Grounding
- **Definition**: The degree to which claims in the response align with factual, clearly visible features in the image.
- **Scoring**:
  - `5`: Completely accurate; all claims directly verifiable in the image.
  - `3`: Mostly accurate with minor unsubstantiated observations.
  - `1`: Substantially incorrect or describes elements not present.

### 2. Relevance to Objective
- **Definition**: Direct alignment with the selected objective (Summarise, Analyse, Evaluate, Explain, Teach).
- **Scoring**:
  - `5`: Fulfills the exact objective directly and completely.
  - `3`: Partially addresses the objective with tangential commentary.
  - `1`: Irrelevant or diverges entirely from requested task.

### 3. Completeness & Depth
- **Definition**: Thoroughness of coverage of salient visual elements, spatial relationships, and context.
- **Scoring**:
  - `5`: Captures all primary foreground, background, and relational elements.
  - `3`: Covers prominent features but overlooks key structural relationships.
  - `1`: Superficial description omitting core subject matter.

### 4. Instruction Adherence
- **Definition**: Strict compliance with user preferences (Audience level, Tone, Output Format, and Length).
- **Scoring**:
  - `5`: 100% adherence to requested format (e.g. structured bullet points), audience calibration, and length bounds.
  - `3`: Follows tone and audience but deviates from requested formatting constraints.
  - `1`: Ignores formatting, tone, and length instructions.

### 5. Logical Consistency
- **Definition**: Internal coherence, sound reasoning progression, and absence of contradictory statements.
- **Scoring**:
  - `5`: Completely coherent progression without logical conflicts.
  - `3`: Coherent with minor ambiguous phrasing.
  - `1`: Self-contradictory claims within the same response.

### 6. Clarity & Readability
- **Definition**: Syntactic fluency, clear organization, and structural readability.
- **Scoring**:
  - `5`: Clean typography, well-organized sections, concise phrasing.
  - `3`: Understandable but dense with poor visual chunking.
  - `1`: Disorganized or unreadable text stream.

### 7. Hallucination & Unsupported-Claim Reduction
- **Definition**: Absence of fabricated details, invented text, or speculative identities.
- **Scoring**:
  - `5`: Zero hallucinated elements; explicitly states uncertainty when visual evidence is ambiguous.
  - `3`: Mild speculative assumptions without stated uncertainty.
  - `1`: Severe hallucinations of non-existent objects, text, or figures.

---

## 2. Quantitative Provider Metrics (Ollama API)

Directly captured from Ollama inference headers:
- `prompt_eval_count`: Number of input tokens (prompt text + image patch embeddings).
- `eval_count`: Number of generated output tokens in the response.
- `total_tokens`: Total computational token volume ($prompt + output$).
- `latency_sec`: Wall-clock execution duration in seconds.
- `tokens_per_sec`: Generation throughput: $\frac{\text{eval\_count}}{\text{eval\_duration\_sec}}$.
- `quality_per_1000_tokens`: Rate-distortion efficiency metric: $\frac{\text{Average Quality Score}}{\text{Total Tokens}} \times 1000$.
