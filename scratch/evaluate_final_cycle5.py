import sys
import json
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, '.')
from reference_runtime import runtime
from scratch.build_stage_31_7_25_benchmark import raw_cases

print(f"Total benchmark cases to evaluate: {len(raw_cases)}")

matrix = defaultdict(lambda: defaultdict(int))
correct = 0
total = len(raw_cases)
by_group = defaultdict(lambda: {"total": 0, "correct": 0})
details = []

classes = ["DIRECT", "PARTIAL", "SUPPORTING", "RELATED", "OFF_TOPIC", "INSUFFICIENT", "UNKNOWN"]

for idx, case in enumerate(raw_cases):
    cid = f"CASE_{idx+1:03d}"
    group = case["group"]
    q = case["question_text"]
    r = case["response_text"]
    exp = case["human_classification"]
    
    res = runtime.evaluate_open_domain_semantic_relevance(q, r)
    pred = res["classification"]
    
    matrix[exp][pred] += 1
    by_group[group]["total"] += 1
    
    is_corr = (pred == exp)
    if is_corr:
        correct += 1
        by_group[group]["correct"] += 1
    
    details.append({
        "id": cid,
        "group": group,
        "question": q,
        "response": r,
        "expected": exp,
        "predicted": pred,
        "correct": is_corr,
        "relation_type": res.get("relation_type", ""),
        "rationale": res.get("rationale", "")
    })

accuracy = correct / total

# Class-level metrics
class_metrics = {}
for c in classes:
    tp = matrix[c][c]
    fp = sum(matrix[other][c] for other in classes if other != c)
    fn = sum(matrix[c][other] for other in classes if other != c)
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
    class_metrics[c] = {
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "support": tp + fn,
        "predicted_count": tp + fp,
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1": round(f1, 4)
    }

# False DIRECTs count
false_directs = sum(matrix[other]["DIRECT"] for other in classes if other != "DIRECT")

output_data = {
    "evaluation_type": "HISTORICAL_DIAGNOSTIC_ONLY",
    "note": "Informational diagnostic reference only; benchmark is not independent nor ground truth.",
    "total_cases": total,
    "correct": correct,
    "accuracy": round(accuracy, 4),
    "false_direct_count": false_directs,
    "false_direct_reduction_vs_stage_31_7_25": f"From 70 down to {false_directs} ({(70 - false_directs) / 70 * 100:.2f}% reduction)",
    "accuracy_gain_vs_stage_31_7_25": f"From 60.80% (152/250) up to {accuracy*100:.2f}% ({correct}/250) (+{correct - 152} cases gained)",
    "class_metrics": class_metrics,
    "group_metrics": {g: {"total": d["total"], "correct": d["correct"], "accuracy": round(d["correct"]/d["total"], 4)} for g, d in by_group.items()},
    "confusion_matrix": {exp: dict(preds) for exp, preds in matrix.items()}
}

print(json.dumps({k: v for k, v in output_data.items() if k != "confusion_matrix"}, indent=2))
print("\nConfusion Matrix:")
print("Expected \\ Predicted\t" + "\t".join(classes))
for exp in classes:
    row = [str(matrix[exp][p]) for p in classes]
    print(f"{exp:<15}\t" + "\t".join(row))

with open("11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_27_historical_diagnostic_metrics.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print("\nSaved deliverable: stage_31_7_27_historical_diagnostic_metrics.json")
