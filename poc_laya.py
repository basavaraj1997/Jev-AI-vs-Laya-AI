"""
Laya AI (System 1 Decision Engine) - Local Proof of Concept (POC)
Demonstrates non-autoregressive decision making with typed outputs:
- Choice: Categorical classification
- Noul: Boolean / Propositional verification with calibrated probability
- Score: Ordinal score rating
"""

import sys

def run_poc():
    try:
        import laya
    except ImportError:
        print("[!] Package 'laya' is not installed.")
        print("    Please install it using: pip install laya")
        print("    Optional serving extension: pip install \"laya[serve]\"")
        sys.exit(1)

    print("=" * 65)
    print("  Laya AI (System 1 Decision Model) - Local POC Walkthrough")
    print("=" * 65)

    # 1. Load model checkpoint (downloads and caches locally on first execution)
    model_identifier = "convaiinnovations/laya"
    print(f"\n[1/3] Loading checkpoint '{model_identifier}'...")
    agent = laya.load(model_identifier)
    print("      Model loaded successfully into memory.")

    # 2. Define sample state context (e.g. support ticket / production error)
    sample_ticket = {
        "text": (
            "URGENT: Our production database cluster is unresponsive after the midnight deployment. "
            "Customers are experiencing checkout failures and timeout errors. Please escalate!"
        )
    }
    print(f"\n[2/3] Input State Context:\n      \"{sample_ticket['text']}\"")

    # 3. Define schema with typed decision primitives
    questions = [
        ("routing_target", {
            "type": "choice",
            "options": ["sre_oncall", "billing_support", "frontend_team", "account_security"]
        }),
        ("is_p0_incident", {
            "type": "noul",
            "statement": "This message reports a critical production outage causing total business disruption."
        }),
        ("urgency_score", {
            "type": "score",
            "levels": ["low", "normal", "high", "critical"]
        })
    ]

    # 4. Predict decisions in a single forward pass (~30-40ms on local CPU/GPU)
    print("\n[3/3] Performing non-autoregressive inference...")
    result = agent.predict(sample_ticket, questions)

    # 5. Extract typed results
    routing = result.answers["routing_target"]
    p0_check = result.answers["is_p0_incident"]
    urgency = result.answers["urgency_score"]

    print("\n" + "=" * 65)
    print("  DECISION RESULTS")
    print("=" * 65)
    print(f"  * Routing Category    : {routing.best}")
    print(f"    Confidence Breakdown : {routing.probabilities}")
    print(f"  * Is P0 Outage?       : {'YES' if p0_check.probability > 0.5 else 'NO'} "
          f"({p0_check.probability:.2%} confidence)")
    print(f"  * Urgency Rating      : {urgency.value} (rubric: {urgency.best})")
    print("=" * 65)

if __name__ == "__main__":
    run_poc()
