import json
import hashlib
import os
import sys
import time

def compute_sha256(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest().upper()

def main():
    expected_runtime_sha = "75C6841D14691D9AFC6FF628CA27F67F8201308EB48D6A46A35E41DEA997A6EC"
    runtime_path = "reference_runtime/runtime.py"
    
    current_sha = compute_sha256(runtime_path)
    if current_sha != expected_runtime_sha:
        print(f"ERROR: Runtime hash mismatch! Expected {expected_runtime_sha}, got {current_sha}")
        sys.exit(1)
    print(f"Pre-execution Runtime SHA-256 verified: {current_sha}")
    
    blind_input_path = "11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_21_blind_input.json"
    predictions_path = "11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_21_system_predictions.json"
    
    with open(blind_input_path, "r", encoding="utf-8") as f:
        blind_cases = json.load(f)
    print(f"Loaded {len(blind_cases)} blind cases from: {blind_input_path}")
    
    sys.path.insert(0, ".")
    from reference_runtime.runtime import evaluate_open_domain_semantic_relevance
    
    predictions = []
    total_start = time.perf_counter()
    for i, case in enumerate(blind_cases, start=1):
        case_id = case["id"]
        q_text = case["question_text"]
        r_text = case["response_text"]
        
        t0 = time.perf_counter()
        eval_result = evaluate_open_domain_semantic_relevance(q_text, r_text)
        elapsed_ms = round((time.perf_counter() - t0) * 1000, 3)
        
        pred_entry = {
            "id": case_id,
            "question_text": q_text,
            "response_text": r_text,
            "predicted_classification": eval_result.get("classification"),
            "predicted_functional_contribution": eval_result.get("functional_contribution"),
            "predicted_confidence": eval_result.get("confidence"),
            "predicted_reason": eval_result.get("rationale"),
            "relation_type": eval_result.get("relation_type"),
            "aspect_coverage": eval_result.get("aspect_coverage"),
            "epistemic_status": eval_result.get("epistemic_status"),
            "demand_nexus": eval_result.get("demand_nexus"),
            "needs_review": eval_result.get("needs_review"),
            "execution_time_ms": elapsed_ms
        }
        predictions.append(pred_entry)
        
        if i % 50 == 0 or i == len(blind_cases):
            print(f"Processed {i}/{len(blind_cases)} cases...")
            
    total_duration = time.perf_counter() - total_start
    print(f"Execution completed in {total_duration:.2f} seconds.")
    
    with open(predictions_path, "w", encoding="utf-8") as f:
        json.dump(predictions, f, ensure_ascii=False, indent=2)
        
    pred_sha = compute_sha256(predictions_path)
    print(f"Predictions saved to: {predictions_path}")
    print(f"Predictions SHA-256: {pred_sha} (Size: {os.path.getsize(predictions_path)} bytes)")
    
    post_sha = compute_sha256(runtime_path)
    if post_sha != expected_runtime_sha:
        print(f"CRITICAL ERROR: Runtime was modified during prediction run! Expected {expected_runtime_sha}, got {post_sha}")
        sys.exit(2)
    print(f"Post-execution Runtime SHA-256 verified unchanged: {post_sha}")

if __name__ == "__main__":
    main()
