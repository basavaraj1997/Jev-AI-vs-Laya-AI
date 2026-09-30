"""
Laya AI (System 1 Decision Engine) - Local Execution Suite
==========================================================
Demonstrates non-autoregressive decision making with typed outputs:
- Choice: Categorical classification
- Noul: Boolean / Propositional verification with calibrated probability
- Score: Ordinal score rating
"""

import sys
import time

def run_decision_engine():
    try:
        import laya
    except ImportError:
        print("[!] Package 'laya' is not installed.")
        print("    Please install it using: pip install laya")
        print("    Optional serving extension: pip install \"laya[serve]\"")
        sys.exit(1)

    print("=" * 65)
    print("  Laya AI (System 1 Decision Engine) - Local Execution")
    print("=" * 65)

    # 1. Load model checkpoint (weights are cached locally in ~/.cache/huggingface)
    model_identifier = "convaiinnovations/laya"
    print(f"\n[1/3] Loading checkpoint '{model_identifier}'...")
    agent = laya.load(model_identifier)
    print("      Model loaded successfully into memory.")

    # 2. Define sample state context (e.g. support ticket / production error)
    sample_ticket = {
        "text": (
            "URGENT: Our primary production PostgreSQL database cluster is unresponsive "
            "after the midnight deployment. Customers are experiencing checkout failures "
            "and timeout errors. Please escalate to on-call immediately!"
        )
    }
    print(f"\n[2/3] Input State Context:\n      \"{sample_ticket['text']}\"")

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

    # 4. Predict decisions in a single non-autoregressive forward pass
    print("\n[3/3] Performing non-autoregressive forward pass...")
    t0 = time.time()
    result = agent.predict(sample_ticket, questions)
    elapsed_ms = (time.time() - t0) * 1000

    # 5. Extract typed results
    answers = result.get("answers", {})
    routing = answers.get("routing_target", {})
    p0_check = answers.get("is_p0_incident", {})
    urgency = answers.get("urgency_score", {})

    print("\n" + "=" * 65)
    print(f"  DECISION RESULTS (Inference Latency: {elapsed_ms:.1f}ms)")
    print("=" * 65)
    print(f"  * Routing Category    : {routing.get('choice')} ")
    print(f"    Confidence Breakdown : {routing.get('probabilities')}")
    print(f"  * Is P0 Outage?       : {'YES' if p0_check.get('noul', 0) > 0.5 else 'NO'} "
          f"({p0_check.get('noul', 0):.2%} confidence)")
    print(f"  * Urgency Score       : {urgency.get('score')} "
          f"(Distribution: {urgency.get('probabilities')})")
    print("=" * 65)

if __name__ == "__main__":
    run_decision_engine()
