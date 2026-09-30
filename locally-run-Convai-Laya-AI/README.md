# Run Convai Laya AI Locally with Interactive Swagger UI & REST API

> **The 100% local, self-hosted System 1 decision engine server with interactive OpenAPI Swagger UI (`/docs`). Test custom payloads, classify text in sub-100ms, and verify Choice, Noul, and Score primitives on your own hardware with zero API fees.**

---

## ⚡ Quickstart: Run Locally in 3 Steps

### Step 1: Open Directory
```bash
cd locally-run-Convai-Laya-AI
```

### Step 2: Install Requirements
```bash
pip install -r requirements.txt
```

### Step 3: Start the Server
* **On Windows (1-Click)**: Double-click `run_server.bat` or run:
  ```powershell
  .\run_server.ps1
  ```
* **Or via Python / Uvicorn directly**:
  ```bash
  python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
  ```

Once started, open your web browser to:
👉 **Interactive Swagger Documentation**: [**`http://localhost:8000/docs`**](http://localhost:8000/docs)  
👉 **ReDoc Specification**: [**`http://localhost:8000/redoc`**](http://localhost:8000/redoc)

---

## 🖥️ Interactive Swagger UI Walkthrough

The Swagger UI provides an interactive web interface to test custom payloads in real time:

1. Open `http://localhost:8000/docs`.
2. Click on the **`POST /predict`** endpoint.
3. Click **"Try it out"**.
4. Paste your custom JSON payload (or select one of the built-in presets).
5. Click **"Execute"**.
6. View the sub-100ms non-autoregressive decision output with calibrated probabilities directly in your browser!

### Sample Request Payload

```json
{
  "state": {
    "text": "CRITICAL: PostgreSQL primary cluster database connection pool exhausted on prod-us-east-1. Web apps returning HTTP 500."
  },
  "questions": {
    "routing_team": {
      "type": "choice",
      "instructions": "Which engineering team is responsible for resolving this incident?",
      "criteria": ["sre_infrastructure", "billing_support", "frontend_ui", "account_security"]
    },
    "is_p0_outage": {
      "type": "noul",
      "instructions": "Does this incident cause an active user-facing production outage?"
    },
    "severity_score": {
      "type": "score",
      "instructions": "Rate the operational severity level from low to critical.",
      "criteria": ["P4_minor", "P3_moderate", "P2_major", "P1_blocker"]
    }
  }
}
```

### Sample Response (HTTP 200 OK)

```json
{
  "model": "laya-rl-agent",
  "status": "success",
  "latency_ms": 38.4,
  "answers": {
    "routing_team": {
      "type": "choice",
      "choice": "sre_infrastructure",
      "probabilities": {
        "sre_infrastructure": 0.892,
        "account_security": 0.054,
        "billing_support": 0.038,
        "frontend_ui": 0.016
      },
      "confidence": 0.892
    },
    "is_p0_outage": {
      "type": "noul",
      "noul": 0.9412,
      "confidence": 0.9412
    },
    "severity_score": {
      "type": "score",
      "score": 2.85,
      "legend": {
        "0": "P4_minor",
        "1": "P3_moderate",
        "2": "P2_major",
        "3": "P1_blocker"
      },
      "probabilities": {
        "0": 0.008,
        "1": 0.024,
        "2": 0.118,
        "3": 0.850
      }
    }
  },
  "usage": {
    "input_tokens": 42,
    "output_tokens": 0
  }
}
```

---

## 🎯 Pre-Configured Test Presets (`GET /presets`)

You can fetch or inspect built-in test scenarios using `GET /presets`:
* **`it_incident_triage`**: Real-time server outage classification, PagerDuty paging alert, and severity scoring.
* **`customer_support_billing`**: Duplicate chargeback dispute, refund eligibility verification, and churn risk.
* **`cybersecurity_guardrail`**: Adversarial LLM prompt injection and credential extraction detection.
* **`clinical_emergency_triage`**: Urgent patient symptom triage and Emergency Severity Index (ESI) scoring.

---

## 🧪 Automated Testing

To automatically verify all endpoints from the command line:

```bash
python test_api.py
```

This verifies:
1. `GET /health` -> Server and model readiness.
2. `GET /presets` -> Catalog retrieval.
3. `POST /predict` -> Live non-autoregressive inference and latency benchmarks.

---

## 🔍 Comprehensive Search Keywords & R&D Taxonomy

This repository and local endpoint are designed as the reference implementation for developers, researchers, and tech leads evaluating **System 1 decision models**. Below are the primary search keywords and taxonomy indexing this project:

### 1. Model Names & Common Misspellings
* **TypeSafe AI (Jev)**: `gev typesafe ai`, `jev ai`, `typesafe ai`, `typesafe-sdk`, `typesafe jev`, `typesafe ai python`, `typesafe ai api`, `Diogo Almeida TypeSafe AI`
* **Convai Innovations (Laya)**: `convai laya`, `convai laya ai`, `laya ai mode`, `laya decision model`, `convaiinnovations/laya`, `laya python`, `laya-multilingual`, `laya-typed-decisions`
* **Direct Comparisons**: `typesafe ai vs laya ai`, `jev vs laya`, `laya vs jev`, `open source alternative to typesafe ai`, `self hosted jev alternative`, `local jev alternative`

### 2. Architecture & Decision Paradigms
* `System 1 AI` vs `System 2 AI` (Fast, non-generative, probabilistic decision-making vs slow token-by-token generation)
* `Non-autoregressive AI`, `non-autoregressive decision model`, `non-generative LLM`
* `ModernBERT decision head`, `ModernBERT-large decision model`, `mmBERT-base`, `encoder-based decision engine`
* `Sub-100ms AI inference`, `sub-50ms model routing`, `low-latency AI triage`
* `Zero JSON formatting errors`, `deterministic structured outputs without regex parsing`

### 3. Primitive Types
* `choice primitive`: Multi-class categorical routing with complete probability distribution.
* `noul primitive`: Calibrated boolean confidence and propositional truth hypothesis testing (0.0 to 1.0).
* `score primitive`: Continuous expectations across ordered rubric levels.

### 4. Enterprise PoC & R&D Use Cases
* `Local PoC for System 1 AI`, `System 1 AI R&D`, `self-hosted decision engine`
* `AI agent guardrails low latency`, `real-time LLM model router`, `automated P0 incident triage`
* `Air-gapped AI classification`, `zero API cost enterprise decision engine`, `private data AI triage`
* `Local Swagger UI for AI decision engine`, `FastAPI endpoint for Convai Laya`

---

## 📁 Project Structure

```
locally-run-Convai-Laya-AI/
├── main.py              # FastAPI service with Swagger UI and /predict endpoint
├── schemas.py           # Pydantic validation models for Choice, Noul, Score
├── presets.py           # Pre-configured test scenario payloads
├── test_api.py          # Automated endpoint testing script
├── run_server.bat       # Windows 1-click batch launcher
├── run_server.ps1       # PowerShell launcher
├── requirements.txt     # Service dependencies (fastapi, uvicorn, laya, pydantic)
└── README.md            # Quickstart documentation and developer taxonomy
```
