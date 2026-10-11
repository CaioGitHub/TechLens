"""
Stage 31.7.17: Blind Execution Script.
Executes the candidate frozen runtime once over the sealed blind input (200 novel cases).
Records predictions, justification, and execution metadata without ground truth contamination.
"""

import json
import time
import hashlib
import sys
from pathlib import Path

# Ensure root directory is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from reference_runtime.runtime import evaluate_open_domain_semantic_relevance

p_input = "scratch/stage_31_7_17_blind_input.json"
p_output = "scratch/stage_31_7_17_system_predictions.json"

with open(p_input, "r", encoding="utf-8") as f:
    blind_cases = json.load(f)

print(f"Loaded {len(blind_cases)} blind cases from {p_input}.")

results = []
t0_total = time.perf_counter()

for i, case in enumerate(blind_cases, 1):
    cid = case["id"]
    q = case["question_text"]
    r = case["response_text"]
    
    t0 = time.perf_counter()
    pred = evaluate_open_domain_semantic_relevance(q, r)
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    
    results.append({
        "id": cid,
        "question_text": q,
        "response_text": r,
        "predicted_classification": pred.get("classification"),
        "predicted_functional_contribution": pred.get("functional_contribution"),
        "predicted_confidence": pred.get("confidence"),
        "predicted_reason": pred.get("reason"),
        "execution_time_ms": round(elapsed_ms, 3)
    })

total_time = time.perf_counter() - t0_total

with open(p_output, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# Compute hash
raw_bytes = open(p_output, "rb").read()
pred_hash = hashlib.sha256(raw_bytes).hexdigest().upper()

print(f"Execution completed in {total_time:.3f}s.")
print(f"Predictions written to {p_output} ({len(raw_bytes)} bytes).")
print(f"SHA-256 of predictions: {pred_hash}")
