from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ImageMetadataResponse(BaseModel):
    image_id: str
    filename: str
    width: int
    height: int
    channels: int
    format: str
    file_size_bytes: int
    file_size_kb: float
    url: str

class CVProcessRequest(BaseModel):
    image_id: str
    operations: List[Dict[str, Any]] = Field(default_factory=list)
    second_image_id: Optional[str] = None

class CVProcessResultItem(BaseModel):
    operation_id: str
    operation_name: str
    module_name: str
    status: str
    execution_time_ms: float
    processed_image_url: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None

class CVProcessResponse(BaseModel):
    image_id: str
    results: List[CVProcessResultItem]
    aggregated_metadata: Dict[str, Any] = Field(default_factory=dict)

class UserPreferences(BaseModel):
    audience: str = "Student" # Beginner, Student, Intermediate, Expert, Researcher
    tone: str = "Professional" # Simple, Professional, Academic, Technical
    output_format: str = "Structured report" # Paragraph, Bullet points, Step-by-step, Structured report, Table
    length: str = "Medium" # Short, Medium, Detailed
    few_shot_setting: str = "zero-shot" # zero-shot, one-shot, few-shot
    include_examples: bool = True
    explain_terms: bool = True
    include_limitations: bool = True
    include_uncertainty: bool = True
    include_visual_evidence: bool = True
    compare_interpretations: bool = False
    advanced_instructions: Optional[str] = None

class PromptGenerationRequest(BaseModel):
    image_id: str
    objective: str = "Analyse" # Summarise, Analyse, Evaluate, Explain, Teach
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    cv_metadata: Dict[str, Any] = Field(default_factory=dict)

class GeneratedPromptsResponse(BaseModel):
    basic_prompt: str
    costar_prompt: str
    ai_optimized_prompt: str
    objective: str
    preferences: Dict[str, Any]
    cv_metadata_summary: Dict[str, Any]

class ExperimentRunRequest(BaseModel):
    title: Optional[str] = None
    image_id: str
    objective: str = "Analyse"
    cv_operations: List[Dict[str, Any]] = Field(default_factory=list)
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    model: Optional[str] = None
    strategies_to_run: List[str] = Field(default_factory=lambda: ["basic", "costar", "ai_optimized"])
    second_image_id: Optional[str] = None

class StrategyExecutionResult(BaseModel):
    strategy: str
    prompt: str
    response: str
    metrics: Dict[str, Any]
    error: Optional[str] = None

class ExperimentRunResponse(BaseModel):
    experiment_id: str
    title: str
    created_at: str
    selected_model: str
    selected_objective: str
    image_id: str
    image_url: str
    cv_results: List[CVProcessResultItem]
    results: Dict[str, StrategyExecutionResult]
    status: str

class EvaluationRatingRequest(BaseModel):
    experiment_id: str
    ratings: Dict[str, Dict[str, Any]] # { basic: {accuracy: 4, ...}, costar: {...}, ai_optimized: {...} }

class TeachGenerateRequest(BaseModel):
    image_id: str
    custom_topic: Optional[str] = None
    model: Optional[str] = None

class TeachSubmitAnswer(BaseModel):
    question_index: int
    selected_option: int

class TeachEvaluateRequest(BaseModel):
    session_id: str
    answers: List[TeachSubmitAnswer]
