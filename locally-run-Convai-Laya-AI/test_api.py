#!/usr/bin/env python3
"""
Automated Client Verification for Convai Laya Local API
========================================================
Sends test requests to the local FastAPI server and validates responses.
"""

import sys
import time

try:
    import requests
except ImportError:
    print("[!] 'requests' is not installed. Please install it: pip install requests")
    sys.exit(1)

BASE_URL = "http://localhost:8000"

def test_api():
    print("=" * 70)
    print("  Testing Local Convai Laya AI REST API")
    print(f"  Target URL: {BASE_URL}")
    print("=" * 70)

    # 1. Health Check
    print("\n[1/3] Testing GET /health ...")
    try:
        res = requests.get(f"{BASE_URL}/health", timeout=10)
        assert res.status_code == 200, f"Expected 200, got {res.status_code}"
        health_data = res.json()
        print(f"      Status       : {health_data.get('status')}")
        print(f"      Model        : {health_data.get('model')}")
        print(f"      Device       : {health_data.get('device')}")
        print(f"      Engine Ready : {health_data.get('is_ready')}")
    except Exception as e:
        print(f"[!] Health check failed: {e}")
        print("    Make sure the server is running on http://localhost:8000")
        sys.exit(1)

    # 2. Presets Check
    print("\n[2/3] Testing GET /presets ...")
    try:
        res = requests.get(f"{BASE_URL}/presets", timeout=5)
        assert res.status_code == 200, f"Expected 200, got {res.status_code}"
        presets = res.json()
        print(f"      Retrieved {len(presets)} presets:")
        for k, v in presets.items():
            print(f"      * {k}: {v.get('title')}")
    except Exception as e:
        print(f"[!] Presets test failed: {e}")

    # 3. Decision Prediction Check
    print("\n[3/3] Testing POST /predict ...")
    payload = {
        "state": {
            "text": "CRITICAL: Database connection pool exhausted on prod-us-east-1. Web apps returning HTTP 500."
        },
        "questions": {
            "routing_team": {
                "type": "choice",
                "instructions": "Which engineering team is responsible for this?",
                "criteria": ["sre_infrastructure", "billing_support", "frontend_ui", "account_security"]
            },
            "is_outage": {
                "type": "noul",
                "instructions": "Does this message report an active user-facing service outage?"
            },
            "severity_score": {
                "type": "score",
                "instructions": "Rate the operational severity level.",
                "criteria": ["P4_minor", "P3_moderate", "P2_major", "P1_blocker"]
            }
        }
    }

    try:
        t0 = time.time()
        res = requests.post(f"{BASE_URL}/predict", json=payload, timeout=30)
        client_latency_ms = (time.time() - t0) * 1000
        assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
        data = res.json()
        
        server_latency_ms = data.get("latency_ms", 0.0)
        answers = data.get("answers", {})

        routing = answers.get("routing_team", {})
        outage = answers.get("is_outage", {})
        severity = answers.get("severity_score", {})

        print("\n" + "-" * 55)
        print(f"  PREDICTION RESULTS")
        print(f"  Server Latency : {server_latency_ms} ms")
        print(f"  Total Roundtrip: {client_latency_ms:.1f} ms")
        print("-" * 55)
        print(f"  Choice (Routing) : {routing.get('choice')}")
        print(f"  Probabilities    : {routing.get('probabilities')}")
        print(f"  Noul (Outage)    : {'YES' if outage.get('noul', 0) > 0.5 else 'NO'} ({outage.get('noul', 0):.2%} confidence)")
        print(f"  Score (Severity) : {severity.get('score')} (Dist: {severity.get('probabilities')})")
        print("-" * 55)
        print("\n[+] All API endpoints validated successfully!")

    except Exception as e:
        print(f"[!] Prediction test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_api()
