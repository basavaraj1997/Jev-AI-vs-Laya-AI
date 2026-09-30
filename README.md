# TypeSafe AI (Jev) vs. Convai Innovations (Laya AI)

> The definitive developer guide, architectural benchmark, and local execution reference for **System 1 non-autoregressive AI decision engines**.

> 🚀 **Interactive Local REST API & Swagger UI**:  
> For the standalone FastAPI service featuring an interactive Swagger UI (`/docs`), 1-click Windows launchers, and pre-built scenario presets, visit:  
> 👉 [**`github.com/basavaraj1997/locally-run-Convai-Laya-AI`**](https://github.com/basavaraj1997/locally-run-Convai-Laya-AI)

---

## 📌 Executive Summary

Traditional Large Language Models (LLMs) like GPT-4, Claude, or LLaMA are **System 2 / autoregressive generative models**: they generate natural language token-by-token. While versatile for creative prose and multi-step reasoning, they introduce significant operational friction for software-to-software pipelines:
* **High latency:** Typically 1,000–5,000+ ms per query.
* **High operational cost:** Expensive per-token billing for both input and output.
* **Formatting fragility:** Prone to hallucinated keys, invalid JSON syntax, and regex/repair overhead.

**TypeSafe AI (Jev)** and **Convai Innovations (Laya AI)** represent the new paradigm of **"System 1" Decision Models**:
* **Non-autoregressive forward pass:** They evaluate an input state against questions in a single forward pass, skipping token-by-token generation.
* **Native typed predictions:** Directly return discrete categorical selections, continuous score intervals, and calibrated probabilities without JSON parsing.
* **Ultra-low latency:** **30–70 ms execution speed**, making them ideal for high-throughput microservice routing, real-time agent guardrails, and automated triage.

---

## ⚖️ Head-to-Head Comparison: Jev AI vs. Laya AI

| Feature / Dimension | TypeSafe AI (Jev) | Convai Innovations (Laya AI) |
| :--- | :--- | :--- |
| **Model Type** | Proprietary SaaS | **Open-Weight (Apache 2.0)** |
| **Hosting & Privacy** | Cloud API only (TypeSafe Cloud) | **100% Local (CPU / GPU) or Self-Hosted Cloud** |
| **Backbone Architecture**| Proprietary non-autoregressive encoder | ModernBERT-large (~421M params) / mmBERT |
| **Typical Latency** | ~70–150 ms (via network call) | **~30–40 ms (local GPU) / sub-second (CPU)** |
| **Hardware Required** | None (Hosted API) | Consumer CPU or NVIDIA GPU (cached locally) |
| **SDK / Python Package**| `typesafe-sdk` | `laya` |
| **Cost Model** | Pay-per-query API subscription | **Free & Open-Source (Zero API costs)** |
| **Air-Gapped / Offline** | ❌ Requires internet & API key | ✅ Fully functional offline & air-gapped |
| **Fine-Tuning Support** | Limited to vendor portal | Full weights access for custom training |
| **Native Output Types** | `choice`, `score`, `noul` | `choice`, `score`, `noul` |

---

## 🧩 The Three Core "System 1" Primitives

Both Jev and Laya operate on three foundational mathematical decision types:

1. **`choice` (Categorical Classification):**
   * Maps input context to the highest-probability option among a discrete set of criteria.
   * Returns: Winning label (`choice`) + complete probability distribution (`probabilities`).
   * *Common Workflows:* Support routing, department dispatch, intent classification.

2. **`noul` (Boolean Proposition / Hypothesis Verification):**
   * Evaluates the truth probability of a natural-language statement against the context.
   * Returns: Calibrated confidence float from `0.0` (definitely false) to `1.0` (definitely true).
   * *Common Workflows:* Guardrails, compliance checks, P0 outage triggers, refund eligibility.

3. **`score` (Ordinal Rubric Rating):**
   * Evaluates input along ordered rubric levels (from index 0 upward).
   * Returns: Continuous score metric + probability mass across rubric levels.
   * *Common Workflows:* Urgency scoring, customer sentiment, risk index, SLA priority.

---

## 🧪 55 Test Cases Benchmark & Evaluation Suite

This repository includes **55 production test cases** spanning **8 enterprise domains**:

* 🗄️ **Infrastructure & IT Incidents** (Database pool exhaustion, BGP route flaps, pod crash loops, disk exhaustion)
* 💳 **Billing & Financial Operations** (Duplicate chargebacks, tax invoice requests, SLA refund claims, pricing tiers)
* 🛡️ **Cybersecurity & Threat Detection** (SQL injection, LLM prompt injection, Tor exfiltration, BEC phishing)
* 💬 **Customer Experience & Support** (Account recovery, crash reports, feature requests, SLA breaches)
* 📦 **E-Commerce & Order Fulfillment** (Porch piracy, incorrect SKU shipments, transit breakage, medical delivery alerts)
* ⚙️ **DevOps & Engineering Pipelines** (ECR push auth failures, Terraform CIDR conflicts, canary rollbacks, flaky tests)
* 🚨 **Content Moderation & Trust & Safety** (Crypto spam, doxxing & harassment, physical threats, piracy warez)
* 🩺 **Healthcare & Clinical Triage** (Acute myocardial infarction, pediatric triage, toxic overdose, stroke code)

### Benchmark Resources

* **Catalog Documentation**: [**`TEST_CASES.md`**](TEST_CASES.md)
* **Machine-Readable Dataset**: [**`test_cases.json`**](test_cases.json)
* **Markdown Result Sheet**: [**`EVALUATION_RESULTS.md`**](EVALUATION_RESULTS.md)
* **CSV Result Sheet**: [**`test_results.csv`**](test_results.csv)

### Running the Evaluation Suite

```bash
# Automated validation across all 55 test cases
python evaluate_dataset.py

# Force live evaluation against local Laya model weights
python evaluate_dataset.py live
```

---

## 🚀 Part 1: Using TypeSafe AI (Jev)

Jev is provided as a managed cloud service. You must generate an API key from the [TypeSafe Console](https://console.typesafe.ai).

### 1. Installation

```bash
pip install typesafe-sdk
```

### 2. Python Implementation

```python
import os
from typesafe_sdk import TypeSafeClient

# Initialize client using your API key
client = TypeSafeClient(api_key=os.environ.get("TYPESAFE_API_KEY"))

# Input context state
state = "I ordered 2 items last week and my card was billed twice. Please refund me as soon as possible!"

# Send structured decision request
response = client.post(
    state=state,
    questions={
        "department": {
            "type": "choice",
            "instructions": "Which department handles this inquiry?",
            "options": ["billing", "technical_support", "sales"]
        },
        "is_refund_request": {
            "type": "noul",
            "instructions": "Is the user requesting a monetary refund?"
        },
        "urgency": {
            "type": "score",
            "instructions": "Rate how urgent this ticket is.",
            "levels": ["low", "normal", "high", "critical"]
        }
    }
)

print("Decision Output:", response)
```

---

## 💻 Part 2: Using Laya AI for Local Execution (Zero Cost, 100% Offline)

Because **Laya AI is open-weight**, it is ideal for local test environments, private enterprise data, air-gapped systems, and developer machines.

### 1. Environment Setup

```powershell
# 1. Clone repository
git clone https://github.com/basavaraj1997/Jev-AI-vs-Laya-AI.git
cd Jev-AI-vs-Laya-AI

# 2. Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # On Windows PowerShell
# source .venv/bin/activate    # On Linux/macOS

# 3. Install dependencies
pip install -r requirements.txt
```

### 2. Local Decision Script (`decision_engine.py`)

Run the standalone decision script locally:

```bash
python decision_engine.py
```

Code excerpt:

```python
import laya

# 1. Load model checkpoint (downloads and caches locally on first run)
agent = laya.load("convaiinnovations/laya")

# 2. Define input state context
state = {
    "text": "CRITICAL: Database connection pool exhausted on prod-us-east-1. Web apps returning HTTP 500."
}

# 3. Define schema with typed decision primitives
questions = {
    "routing_target": {
        "type": "choice",
        "instructions": "Which engineering team should handle this incident?",
        "criteria": ["sre_oncall", "billing_support", "frontend_team", "account_security"]
    },
    "is_p0_incident": {
        "type": "noul",
        "instructions": "Does this message report a critical production outage causing total business disruption?"
    },
    "urgency_score": {
        "type": "score",
        "instructions": "Rate the operational severity of this issue from low to critical.",
        "criteria": ["low", "normal", "high", "critical"]
    }
}

# 4. Predict decisions in a single non-autoregressive forward pass (~33ms)
result = agent.predict(state, questions)

print(result["answers"])
```

---

## 🌐 Running Laya as a Local HTTP Microservice

To integrate Laya with any existing backend (.NET, Node.js, Go, Java):

```bash
# Start the built-in REST API server on localhost:8000
laya serve --model convaiinnovations/laya --port 8000
```

### Querying via cURL / HTTP:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "state": "Could you help me renew my team annual subscription?",
    "questions": {
      "intent": {
        "type": "choice",
        "instructions": "What is the primary customer intent?",
        "criteria": ["renewal", "cancellation", "bug", "general"]
      }
    }
  }'
```

> 🌟 **Dedicated Standalone Service with Interactive Swagger UI**:  
> For the complete FastAPI microservice with automated model caching, interactive Swagger UI (`/docs`), pre-built enterprise presets, and 1-click Windows/PowerShell launchers, check out:  
> 👉 [**`https://github.com/basavaraj1997/locally-run-Convai-Laya-AI`**](https://github.com/basavaraj1997/locally-run-Convai-Laya-AI)

---

## 🔍 Keywords, Search Terms & R&D Taxonomy

For developers, machine learning researchers, and architects exploring System 1 AI decision systems, this repository covers the most frequent queries and keywords:

### 1. Model Names & Common Search Misspellings
* **TypeSafe AI (Jev)**: `gev typesafe ai`, `jev ai`, `typesafe ai`, `typesafe-sdk`, `typesafe jev`, `typesafe ai python`, `Diogo Almeida TypeSafe`
* **Convai Innovations (Laya)**: `convai laya`, `convai laya ai`, `laya ai mode`, `laya decision model`, `convaiinnovations/laya`, `laya python sdk`, `laya-multilingual`, `laya-typed-decisions`
* **Comparisons**: `typesafe ai vs laya ai`, `jev vs laya`, `laya vs jev`, `open source alternative to typesafe ai`, `self-hosted jev alternative`

### 2. Architecture & Performance Terminology
* `System 1 AI` vs `System 2 AI` (fast, intuitive decision-making vs slow, generative reasoning)
* `Non-autoregressive AI`, `non-autoregressive decision model`, `non-generative LLM`
* `ModernBERT decision head`, `ModernBERT-large`, `mmBERT-base`, `encoder-based decision engine`
* `Sub-100ms AI classification`, `sub-50ms model routing`, `low-latency AI triage`
* `Single forward pass decision making`, `parallel transformer inference`

### 3. Typed Primitives & Structured Outputs
* `choice primitive` (categorical classification without hallucinations or regex repair)
* `noul primitive` (calibrated boolean confidence, propositional truth testing)
* `score primitive` (ordinal rubric expectations, continuous value scoring)
* `calibrated probabilities in AI`, `guaranteed schema adherence`, `zero JSON repair`

### 4. R&D & PoC Workflows
* `System 1 AI PoC`, `System 1 AI R&D`, `local PoC for decision engine`
* `AI agent guardrails low latency`, `real-time model router`, `automated P0 incident triage`
* `Air-gapped AI classification`, `zero API cost enterprise decision engine`, `private data AI triage`

---

## 🎯 Architectural Selection Guide

* **Choose Laya AI when:**
  * You need **100% data sovereignty & privacy** (HIPAA, GDPR, internal company proprietary code/data).
  * You want **zero recurring API subscription costs**.
  * You require **offline, local, or air-gapped execution** on edge devices or private servers.
  * You want access to model weights to **fine-tune** on proprietary internal taxonomies.

* **Choose Jev (TypeSafe AI) when:**
  * You want a **fully managed cloud API** with zero infrastructure management.
  * You do not want to allocate local CPU or GPU memory for model checkpoints.
  * You require turnkey enterprise SLAs and hosted scalability from TypeSafe AI.
