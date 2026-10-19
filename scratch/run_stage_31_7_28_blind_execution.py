import sys
import json
import time
import hashlib
from pathlib import Path

# Step 1: Strict Runtime Freeze Verification
runtime_path = Path("reference_runtime/runtime.py")
expected_hash = "6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28"
actual_hash = hashlib.sha256(runtime_path.read_bytes()).hexdigest().upper()

print(f"Verifying runtime freeze: {actual_hash}")
if actual_hash != expected_hash:
    raise RuntimeError(f"FROZEN RUNTIME HASH MISMATCH! Expected: {expected_hash}, Got: {actual_hash}")

sys.path.insert(0, ".")
from reference_runtime import runtime

# Step 2: Load Blind Input ONLY
pilot_dir = Path("11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05")
blind_input_file = pilot_dir / "stage_31_7_28_blind_input.json"
blind_data = json.load(open(blind_input_file, encoding="utf-8"))
cases = blind_data["cases"]

print(f"Starting blind inference on {len(cases)} cases...")
start_time = time.time()
predictions = []

for idx, case in enumerate(cases):
    cid = case["id"]
    q = case["question_text"]
    r = case["response_text"]
    
    # Strictly isolated evaluation
    res = runtime.evaluate_open_domain_semantic_relevance(q, r)
    
    pred_record = {
        "id": cid,
        "predicted_relevance": res["classification"],
        "functional_contribution": res["functional_contribution"],
        "relation_type": res.get("relation_type", ""),
        "rationale": res.get("rationale", "")
    }
    predictions.append(pred_record)
    
    if (idx + 1) % 50 == 0 or (idx + 1) == len(cases):
        print(f"Processed {idx + 1}/{len(cases)} cases...")

elapsed = time.time() - start_time
print(f"Completed blind inference in {elapsed:.3f} seconds ({elapsed/len(cases):.4f}s per case).")

# Step 3: Save System Predictions
pred_file = pilot_dir / "stage_31_7_28_system_predictions.json"
pred_output = {
    "stage": "31.7.28",
    "evaluation_mode": "BLIND_INDEPENDENT_EXECUTION",
    "runtime_sha256": actual_hash,
    "total_cases": len(predictions),
    "elapsed_seconds": round(elapsed, 4),
    "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "predictions": predictions
}

with open(pred_file, "w", encoding="utf-8") as f:
    json.dump(pred_output, f, indent=2, ensure_ascii=False)

pred_hash = hashlib.sha256(pred_file.read_bytes()).hexdigest().upper()
print(f"Saved system predictions to {pred_file}")
print(f"Predictions SHA-256: {pred_hash}")
