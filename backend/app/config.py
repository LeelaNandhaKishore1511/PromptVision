import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOADS_DIR = BASE_DIR / "uploads"
PROCESSED_DIR = BASE_DIR / "processed"
DATA_DIR = BASE_DIR / "data"

UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite:///{DATA_DIR / 'promptvision.db'}"
DATABASE_PATH = str(DATA_DIR / "promptvision.db")

# Ollama Settings
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_VISION_MODEL = os.getenv("DEFAULT_VISION_MODEL", "qwen2.5vl:3b")
ADVANCED_VISION_MODEL = os.getenv("ADVANCED_VISION_MODEL", "qwen3-vl:8b")
OCR_MODEL = os.getenv("OCR_MODEL", "deepseek-ocr:latest")
DEFAULT_NUM_CTX = int(os.getenv("DEFAULT_NUM_CTX", "4096"))
MAX_CONCURRENT_MODELS = int(os.getenv("MAX_CONCURRENT_MODELS", "1"))
INFERENCE_TIMEOUT = int(os.getenv("INFERENCE_TIMEOUT", "300"))

# Allowed Image Upload Extensions
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
MAX_IMAGE_SIZE_MB = 15
