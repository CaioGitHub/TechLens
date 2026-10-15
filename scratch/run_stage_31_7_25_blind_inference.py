import json, time, hashlib
from pathlib import Path
from reference_runtime.runtime import evaluate_open_domain_semantic_relevance

input_path = Path('11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_25_blind_input.json')
output_path = Path('11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_25_system_predictions.json')

print(f"Reading blind input from: {input_path}")
blind_cases = json.loads(input_path.read_text(encoding='utf-8'))
print(f"Loaded {len(blind_cases)} blind cases.")

predictions = []
total_t0 = time.perf_counter()

for idx, case in enumerate(blind_cases):
    cid = case['id']
    q = case['question_text']
    r = case['response_text']
    
    t0 = time.perf_counter()
    res = evaluate_open_domain_semantic_relevance(q, r)
    t1 = time.perf_counter()
    
    duration_ms = round((t1 - t0) * 1000, 2)
    
    predictions.append({
        'id': cid,
        'question_text': q,
        'response_text': r,
        'predicted_classification': res.get('classification'),
        'predicted_relation_type': res.get('relation_type'),
        'predicted_functional_contribution': res.get('functional_contribution'),
        'predicted_confidence': res.get('confidence'),
        'predicted_rationale': res.get('rationale'),
        'question_intent': res.get('question_intent'),
        'question_demands': res.get('question_demands'),
        'aspect_coverage': res.get('aspect_coverage'),
        'epistemic_status': res.get('epistemic_status'),
        'demand_nexus': res.get('demand_nexus'),
        'needs_review': res.get('needs_review'),
        'execution_time_ms': duration_ms
    })
    
    if (idx + 1) % 50 == 0:
        print(f"Processed {idx + 1}/{len(blind_cases)} cases...")

total_duration = round(time.perf_counter() - total_t0, 3)
print(f"Inference complete in {total_duration}s.")

output_path.write_text(json.dumps(predictions, indent=2, ensure_ascii=False), encoding='utf-8')
pred_hash = hashlib.sha256(output_path.read_bytes()).hexdigest().upper()
print(f"Saved {len(predictions)} predictions to {output_path} (SHA-256: {pred_hash})")
