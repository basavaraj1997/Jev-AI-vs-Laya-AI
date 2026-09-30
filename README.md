# TypeSafe AI (Jev) vs. Convai Innovations (Laya AI)

> A comprehensive guide, comparison, and local Proof-of-Concept (POC) walkthrough for **System 1 non-autoregressive AI decision engines**.

---

## 📌 Executive Summary

Traditional Large Language Models (LLMs) like GPT-4, Claude, or LLaMA are **System 2 / autoregressive generative models**: they generate natural language token-by-token. While flexible, they introduce:
* **High latency** (typically 1–5+ seconds per request).
* **High costs** (billing per input/output token).
* **Output non-determinism & schema parsing fragility** (regular expression parsing, JSON repair overhead, hallucination risks).

**TypeSafe AI (Jev)** and **Convai Innovations (Laya AI)** represent the new paradigm of **"System 1" Decision Models**:
* **Non-autoregressive forward pass:** They evaluate text in a single inference step rather than generating tokens iteratively.
* **Native typed predictions:** Directly return discrete categorical selections, continuous score intervals, and calibrated probabilities.
* **Ultra-low latency:** 30–70 ms execution speed, suitable for real-time networking, microservice routing, and high-throughput pipelines.

---

## ⚖️ Head-to-Head Comparison

| Attribute | TypeSafe AI (Jev) | Convai Innovations (Laya AI) |
| :--- | :--- | :--- |
| **Model Type** | Proprietary SaaS | **Open-Weight (Apache 2.0)** |
| **Hosting & Privacy** | Cloud API only (TypeSafe Cloud) | **100% Local (CPU / GPU) or Self-Hosted** |
| **Architecture** | Proprietary non-autoregressive encoder | ModernBERT-large (~421M params) / mmBERT |
| **Typical Latency** | ~70–150 ms (via network request) | **~30–40 ms (local execution)** |
| **Hardware Required** | None (Cloud API) | Runs on consumer CPU or NVIDIA GPU |
| **SDK / Library** | `typesafe-sdk` (Python, TypeScript) | `laya` (Python, PyTorch) |
| **Cost Model** | Pay-per-query API subscription | **Free & Open-Source (Self-hosted)** |
| **Offline Capability** | ❌ Requires internet & API Key | ✅ Works completely air-gapped / offline |
| **Output Types** | `choice`, `score`, `noul` | `choice`, `score`, `noul` |

---

## 🧩 The Three Core "System 1" Primitives

Both Jev and Laya structure their predictions into three primary mathematical decision types:

1. **`choice` (Categorical Classification):**
   * Selects the most probable category from a defined list of discrete options.
   * Returns: Winning option label + full probability distribution over all candidates.
   * *Use Cases:* Support ticket routing, intent detection, department assignment.

2. **`noul` (Boolean / Propositional Hypothesis Verification):**
   * Evaluates the truth probability of a specific assertion or statement against the input text.
   * Returns: A calibrated probability from `0.0` (definitely false) to `1.0` (definitely true).
   * *Use Cases:* Guardrails, spam detection, refund eligibility check, PagerDuty alert triggers.

3. **`score` (Ordinal Rubric Rating):**
   * Estimates a continuous score or rank along ordered levels.
   * Returns: Normalized score value and distribution across levels.
   * *Use Cases:* Urgency scoring, customer sentiment, risk index, SLA priority.

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

## 💻 Part 2: Using Laya AI for a Local POC (Zero Cost, 100% Offline)

Because **Laya AI is open-weight**, it is ideal for local POCs, private enterprise data, air-gapped systems, and developer machines.

### 1. Environment Setup

```powershell
# 1. Clone repository
git clone https://github.com/basavaraj1997/Jev-AI-vs-Laya-AI.git
cd Jev-AI-vs-Laya-AI

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

### 2. Local POC Script (`poc_laya.py`)

```python
import laya

def main():
    print("=" * 60)
    print("  Laya AI (System 1 Decision Engine) - Local POC")
    print("=" * 60)

    # 1. Load model weights from Hugging Face (cached locally after first run)
    print("\n[1/3] Loading model: convaiinnovations/laya ...")
    agent = laya.load("convaiinnovations/laya")

    # 2. Define input state (e.g. system incident, customer message, or log)
    state = {
        "text": "CRITICAL: Database connection pool exhausted on prod-us-east-1. Checkout service returning HTTP 500."
    }
    print(f"\n[2/3] Input State:\n  \"{state['text']}\"")

    # 3. Define questions schema
    questions = [
        ("service_domain", {
            "type": "choice",
            "options": ["infrastructure", "billing", "frontend_ui", "auth"]
        }),
        ("trigger_pagerduty", {
            "type": "noul",
            "statement": "This incident indicates a critical production blocker requiring on-call engineer intervention."
        }),
        ("severity_level", {
            "type": "score",
            "levels": ["P4_low", "P3_medium", "P2_high", "P1_critical"]
        })
    ]

    # 4. Execute non-autoregressive inference
    print("\n[3/3] Running inference...")
    result = agent.predict(state, questions)

    # 5. Display calibrated typed results
    print("\n" + "-" * 40)
    print("  RESULTS")
    print("-" * 40)
    print(f"Domain Assignment : {result.answers['service_domain'].best}")
    print(f"All Probabilities : {result.answers['service_domain'].probabilities}")
    print(f"PagerDuty Alert   : {result.answers['trigger_pagerduty'].probability > 0.7} "
          f"({result.answers['trigger_pagerduty'].probability:.2%} confidence)")
    print(f"Severity Score    : {result.answers['severity_level'].value} "
          f"(Level: {result.answers['severity_level'].best})")
    print("-" * 40)

if __name__ == "__main__":
    main()
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
        "options": ["renewal", "cancellation", "bug", "general"]
      },
      "requires_human": {
        "type": "noul",
        "statement": "Does this message require human representative involvement?"
      }
    }
  }'
```

---

## 🎯 When to Use Which?

* **Choose Laya AI when:**
  * You need complete data sovereignty (HIPAA, GDPR, internal company proprietary code/data).
  * You want zero API recurring costs.
  * You want to run in air-gapped environments or local edge devices.
  * You want the ability to fine-tune weights for domain-specific taxonomy.

* **Choose Jev (TypeSafe AI) when:**
  * You prefer a fully managed cloud API with zero infrastructure management.
  * You do not want to allocate local CPU or GPU memory for model weights.
  * You require turnkey enterprise SLAs from TypeSafe AI.

---

## 📄 License
This repository documentation and POC code are licensed under the [MIT License](LICENSE).
The Laya model weights and codebase are released under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0) by Convai Innovations.
