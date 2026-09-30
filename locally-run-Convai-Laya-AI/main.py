#!/usr/bin/env python3
"""
Convai Laya AI Local Decision Engine - FastAPI Service with Swagger UI
======================================================================
Provides interactive REST API endpoints for non-autoregressive System 1 decisions:
- Interactive Swagger UI: http://localhost:8000/docs
- Alternative ReDoc UI:   http://localhost:8000/redoc
- Decision endpoint:      POST /predict
- Health endpoint:        GET /health
- Presets catalog:        GET /presets
"""

from contextlib import asynccontextmanager
import time
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from schemas import (
    PredictionRequest,
    HealthResponse,
    ChoiceQuestion,
    NoulQuestion,
    ScoreQuestion
)
from presets import PRESETS

# Global agent handle and metadata
app_state: Dict[str, Any] = {
    "agent": None,
    "model_id": "convaiinnovations/laya",
    "start_time": time.time(),
    "device": "CPU",
    "is_ready": False,
    "total_predictions": 0
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager: Loads Laya weights once into RAM upon application startup."""
    print("=" * 70)
    print("  Starting Convai Laya AI Local Server...")
    print("=" * 70)
    try:
        import torch
        import laya
        
        device_name = "CUDA (GPU)" if torch.cuda.is_available() else "CPU"
        app_state["device"] = device_name
        
        print(f"[*] Loading model checkpoint '{app_state['model_id']}' on {device_name}...")
        t0 = time.time()
        agent = laya.load(app_state["model_id"])
        load_time = time.time() - t0
        
        app_state["agent"] = agent
        app_state["is_ready"] = True
        print(f"[+] Laya model loaded successfully into memory in {load_time:.2f}s!")
        print("[+] Swagger UI ready at: http://localhost:8000/docs\n")
    except Exception as exc:
        print(f"[!] Warning: Failed to load Laya weights on startup: {exc}")
        app_state["is_ready"] = False
    
    yield
    
    print("\n[*] Shutting down Convai Laya AI Local Server...")
    app_state["agent"] = None
    app_state["is_ready"] = False

# Initialize FastAPI application with rich OpenAPI metadata
app = FastAPI(
    title="Convai Laya AI - Local Decision Engine API",
    description="""
## ⚡ System 1 Non-Autoregressive Decision Engine

Welcome to the local REST API and interactive Swagger UI for **Convai Innovations Laya AI** (`convaiinnovations/laya`).

### Key Capabilities:
* **Sub-100ms Inference**: Non-autoregressive forward pass skips token-by-token generation.
* **Deterministic Typed Outputs**: Native support for **Choice** (categorical), **Noul** (calibrated boolean), and **Score** (ordinal rubric).
* **Zero Formatting Errors**: Replaces regex, JSON repair, and brittle schema extractors.
* **100% Local & Private**: Runs completely on your PC with zero API fees and complete data privacy.

---
### Quick Links:
* **Interactive Swagger UI**: [`/docs`](/docs)
* **ReDoc Specification**: [`/redoc`](/redoc)
* **Health & Diagnostics**: [`/health`](/health)
* **Pre-Configured Scenarios**: [`/presets`](/presets)
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def normalize_question(q_name: str, q_def: Any) -> Dict[str, Any]:
    """Ensures each question schema conforms to Laya's internal criteria/instructions."""
    if hasattr(q_def, "model_dump"):
        q_dict = q_def.model_dump()
    elif isinstance(q_def, dict):
        q_dict = dict(q_def)
    else:
        raise ValueError(f"Question '{q_name}' definition must be a dictionary or Pydantic model.")

    q_type = q_dict.get("type", "choice")
    instructions = q_dict.get("instructions") or q_dict.get("statement") or f"Evaluate question: {q_name}"
    
    criteria = q_dict.get("criteria") or q_dict.get("options") or q_dict.get("levels")

    if q_type == "choice":
        if not criteria:
            raise ValueError(f"Choice question '{q_name}' requires 'criteria' list of options.")
        return {
            "type": "choice",
            "instructions": instructions,
            "criteria": criteria
        }
    elif q_type == "noul":
        return {
            "type": "noul",
            "instructions": instructions
        }
    elif q_type == "score":
        if not criteria:
            raise ValueError(f"Score question '{q_name}' requires 'criteria' list of ordered levels.")
        return {
            "type": "score",
            "instructions": instructions,
            "criteria": criteria
        }
    return q_dict

@app.get("/", include_in_schema=False)
def root_redirect():
    """Redirects root URL directly to Swagger documentation."""
    return RedirectResponse(url="/docs")

@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Diagnostics & Health"],
    summary="Health check & engine status"
)
def get_health():
    """Returns real-time status of the local Laya engine, hardware device, and uptime."""
    import laya
    uptime = time.time() - app_state["start_time"]
    return {
        "status": "ready" if app_state["is_ready"] else "initializing",
        "model": app_state["model_id"],
        "device": app_state["device"],
        "version": getattr(laya, "__version__", "unknown"),
        "uptime_seconds": round(uptime, 2),
        "is_ready": app_state["is_ready"]
    }

@app.get(
    "/presets",
    tags=["Scenarios & Presets"],
    summary="List pre-configured test scenarios"
)
def list_presets():
    """Returns pre-built scenario payloads (IT triage, customer disputes, prompt injection) ready for testing."""
    return PRESETS

@app.get(
    "/presets/{preset_id}",
    tags=["Scenarios & Presets"],
    summary="Fetch a specific test preset"
)
def get_preset(preset_id: str):
    """Retrieves the request payload for a specific preset by ID."""
    if preset_id not in PRESETS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Preset '{preset_id}' not found. Available presets: {list(PRESETS.keys())}"
        )
    return PRESETS[preset_id]

@app.post(
    "/predict",
    tags=["Decision Engine"],
    summary="Execute System 1 Decision Inference",
    description="Processes an input state and returns strictly-typed decisions (Choice, Noul, Score) with calibrated probabilities."
)
def predict_decision(request: PredictionRequest):
    """
    Executes a single non-autoregressive forward pass:
    - **State**: The input context (e.g. ticket text, log alert, user prompt).
    - **Questions**: Schema containing choice, noul, or score primitives.
    """
    agent = app_state["agent"]
    if agent is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Laya AI model is not loaded. Check server logs or ensure weights are downloaded."
        )

    try:
        # 1. Normalize question schemas
        normalized_questions = {}
        for q_name, q_def in request.questions.items():
            normalized_questions[q_name] = normalize_question(q_name, q_def)

        # 2. Execute parallel non-autoregressive inference
        t0 = time.time()
        raw_result = agent.predict(request.state, normalized_questions)
        elapsed_ms = (time.time() - t0) * 1000

        # 3. Format structured response
        app_state["total_predictions"] += 1
        
        return {
            "model": raw_result.get("model", app_state["model_id"]),
            "status": "success",
            "latency_ms": round(elapsed_ms, 2),
            "answers": raw_result.get("answers", {}),
            "usage": raw_result.get("usage", {})
        }

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Inference error: {str(exc)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
