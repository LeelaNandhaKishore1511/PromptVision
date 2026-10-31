import asyncio
import base64
import time
import httpx
from typing import Dict, Any, List, Optional
from ..config import OLLAMA_BASE_URL, DEFAULT_VISION_MODEL, DEFAULT_NUM_CTX, INFERENCE_TIMEOUT

# Lock to enforce strictly sequential Ollama calls (avoid overloading 16GB RAM / CPU inference)
_inference_lock = asyncio.Lock()

class OllamaService:
    def __init__(self, base_url: str = OLLAMA_BASE_URL):
        self.base_url = base_url.rstrip("/")
        self.current_model = DEFAULT_VISION_MODEL

    async def check_health(self) -> Dict[str, Any]:
        """Check if Ollama server is running and reachable."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                res = await client.get(f"{self.base_url}/api/tags")
                if res.status_code == 200:
                    data = res.json()
                    models = [m.get("name") for m in data.get("models", [])]
                    return {
                        "status": "online",
                        "connected": True,
                        "available_models": models,
                        "current_model": self.current_model,
                        "base_url": self.base_url
                    }
                return {
                    "status": "error",
                    "connected": False,
                    "error": f"Ollama returned HTTP {res.status_code}",
                    "current_model": self.current_model
                }
        except Exception as e:
            return {
                "status": "offline",
                "connected": False,
                "error": str(e),
                "current_model": self.current_model,
                "message": "Could not connect to Ollama at http://localhost:11434. Please ensure Ollama is running."
            }

    async def list_models(self) -> List[Dict[str, Any]]:
        """List all models registered in Ollama with size and modification date."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                res = await client.get(f"{self.base_url}/api/tags")
                if res.status_code == 200:
                    data = res.json()
                    models = []
                    for m in data.get("models", []):
                        size_gb = round(m.get("size", 0) / (1024**3), 2)
                        models.append({
                            "name": m.get("name"),
                            "size_gb": size_gb,
                            "modified_at": m.get("modified_at"),
                            "digest": m.get("digest")[:12] if m.get("digest") else None
                        })
                    return models
                return []
        except Exception:
            return []

    async def set_active_model(self, model_name: str) -> Dict[str, Any]:
        """Update current active model after validating availability."""
        models = await self.list_models()
        available_names = [m["name"] for m in models]
        
        # Check if model exists directly or with :latest
        found = None
        for name in available_names:
            if name == model_name or name.split(":")[0] == model_name:
                found = name
                break
                
        if found:
            self.current_model = found
            return {"success": True, "model": self.current_model}
        else:
            return {
                "success": False,
                "error": f"Model '{model_name}' is not found in Ollama. Available: {available_names}"
            }

    async def unload_model(self, model_name: Optional[str] = None) -> Dict[str, Any]:
        """Unload active model from memory to free system RAM."""
        target = model_name or self.current_model
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Ollama unloads a model when keep_alive is set to 0
                res = await client.post(
                    f"{self.base_url}/api/generate",
                    json={"model": target, "keep_alive": 0}
                )
                return {"success": True, "message": f"Model {target} unloaded from memory."}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def encode_image(image_path: str) -> str:
        """Convert image file to base64 string for Ollama vision API."""
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    async def generate_response(
        self,
        prompt: str,
        image_path: Optional[str] = None,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.2,
        num_ctx: int = DEFAULT_NUM_CTX
    ) -> Dict[str, Any]:
        """
        Execute inference through Ollama with sequential locking.
        Supports multimodal vision when image_path is provided.
        Returns model output and actual provider token statistics.
        """
        target_model = model or self.current_model
        
        # Build payload
        images = []
        if image_path:
            try:
                images.append(self.encode_image(image_path))
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Failed to load image for model: {str(e)}",
                    "text": "",
                    "metrics": {}
                }

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        user_message: Dict[str, Any] = {"role": "user", "content": prompt}
        if images:
            user_message["images"] = images
        messages.append(user_message)

        payload = {
            "model": target_model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_ctx": num_ctx
            }
        }

        # Acquire lock to ensure 100% sequential execution (protects laptop memory)
        async with _inference_lock:
            start_time = time.perf_counter()
            try:
                async with httpx.AsyncClient(timeout=INFERENCE_TIMEOUT) as client:
                    response = await client.post(f"{self.base_url}/api/chat", json=payload)
                    duration = time.perf_counter() - start_time
                    
                    if response.status_code == 200:
                        data = response.json()
                        message_content = data.get("message", {}).get("content", "")
                        
                        # Extract real Ollama metrics
                        prompt_eval_count = data.get("prompt_eval_count")
                        eval_count = data.get("eval_count")
                        prompt_eval_duration_ns = data.get("prompt_eval_duration", 0)
                        eval_duration_ns = data.get("eval_duration", 0)
                        total_duration_ns = data.get("total_duration", 0)
                        
                        prompt_eval_sec = round(prompt_eval_duration_ns / 1e9, 3) if prompt_eval_duration_ns else 0
                        eval_sec = round(eval_duration_ns / 1e9, 3) if eval_duration_ns else 0
                        tokens_per_sec = round(eval_count / eval_sec, 2) if (eval_count and eval_sec > 0) else None
                        
                        metrics = {
                            "prompt_eval_count": prompt_eval_count,
                            "eval_count": eval_count,
                            "total_tokens": (prompt_eval_count + eval_count) if (prompt_eval_count is not None and eval_count is not None) else None,
                            "latency_sec": round(duration, 3),
                            "prompt_eval_sec": prompt_eval_sec,
                            "eval_sec": eval_sec,
                            "tokens_per_sec": tokens_per_sec,
                            "model": target_model,
                            "actual_provider_data": True
                        }
                        
                        return {
                            "success": True,
                            "text": message_content,
                            "metrics": metrics,
                            "error": None
                        }
                    else:
                        return {
                            "success": False,
                            "text": "",
                            "metrics": {"latency_sec": round(duration, 3)},
                            "error": f"Ollama HTTP {response.status_code}: {response.text}"
                        }
            except httpx.TimeoutException:
                return {
                    "success": False,
                    "text": "",
                    "metrics": {"latency_sec": round(time.perf_counter() - start_time, 3)},
                    "error": f"Inference timed out after {INFERENCE_TIMEOUT} seconds on CPU. Consider using a smaller model (e.g. qwen2.5vl:3b) or reducing image resolution."
                }
            except Exception as e:
                return {
                    "success": False,
                    "text": "",
                    "metrics": {"latency_sec": round(time.perf_counter() - start_time, 3)},
                    "error": f"Ollama inference error: {str(e)}"
                }

# Global singleton
ollama_service = OllamaService()
