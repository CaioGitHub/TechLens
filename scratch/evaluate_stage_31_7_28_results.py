import json
import hashlib
from pathlib import Path
from collections import defaultdict, Counter

pilot_dir = Path("11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05")
gt_file = pilot_dir / "stage_31_7_28_ground_truth.json"
pred_file = pilot_dir / "stage_31_7_28_system_predictions.json"

gt_data = json.load(open(gt_file, encoding="utf-8"))
pred_data = json.load(open(pred_file, encoding="utf-8"))

gt_cases = {c["id"]: c for c in gt_data["cases"]}
predictions = {p["id"]: p for p in pred_data["predictions"]}

classes = ["DIRECT", "PARTIAL", "SUPPORTING", "RELATED", "OFF_TOPIC", "INSUFFICIENT", "UNKNOWN"]
matrix = defaultdict(lambda: defaultdict(int))

total = len(gt_cases)
correct = 0
divergences = []

by_group = defaultdict(lambda: {"total": 0, "correct": 0})
by_family = defaultdict(lambda: {"total": 0, "correct": 0})
by_qtype = defaultdict(lambda: {"total": 0, "correct": 0})
by_ling = defaultdict(lambda: {"total": 0, "correct": 0})

for cid, gt in gt_cases.items():
    pred_record = predictions.get(cid)
    if not pred_record:
        raise ValueError(f"Missing prediction for {cid}")
        
    ref = gt["reference_relevance"]
    pred = pred_record["predicted_relevance"]
    group = gt["group"]
    family = gt["semantic_family"]
    qtype = gt.get("question_type", "unknown")
    ling = gt.get("linguistic_form", "unknown")
    
    matrix[ref][pred] += 1
    
    by_group[group]["total"] += 1
    by_family[family]["total"] += 1
    by_qtype[qtype]["total"] += 1
    by_ling[ling]["total"] += 1
    
    is_corr = (ref == pred)
    if is_corr:
        correct += 1
        by_group[group]["correct"] += 1
        by_family[family]["correct"] += 1
        by_qtype[qtype]["correct"] += 1
        by_ling[ling]["correct"] += 1
    else:
        divergences.append({
            "id": cid,
            "group": group,
            "semantic_family": family,
            "question_text": gt["question_text"],
            "response_text": gt["response_text"],
            "reference_relevance": ref,
            "predicted_relevance": pred,
            "relation_type": pred_record.get("relation_type", ""),
            "system_rationale": pred_record.get("rationale", ""),
            "reference_rationale": gt["adjudication_rationale"],
            "divergence_type": f"{ref} -> {pred}"
        })

accuracy = correct / total
divergent_count = len(divergences)

# Class metrics
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

# False DIRECTs among divergences
fp_direct = sum(matrix[other]["DIRECT"] for other in classes if other != "DIRECT")
false_direct_divergence_rate = fp_direct / divergent_count if divergent_count > 0 else 0.0

# Invariance Pairs Analysis
pairs = defaultdict(list)
for cid, gt in gt_cases.items():
    pid = gt.get("invariance_pair_id")
    if pid:
        base_id = pid[:-2] if (pid.endswith("_A") or pid.endswith("_B")) else pid
        pred = predictions[cid]["predicted_relevance"]
        pairs[base_id].append({
            "id": cid,
            "variant": pid[-1] if (pid.endswith("_A") or pid.endswith("_B")) else "single",
            "question": gt["question_text"],
            "response": gt["response_text"],
            "reference": gt["reference_relevance"],
            "predicted": pred,
            "correct": gt["reference_relevance"] == pred
        })

pair_results = []
consistent_pairs = 0
correct_pairs = 0

for base_id, plist in pairs.items():
    if len(plist) != 2:
        continue
    case_a = plist[0] if plist[0]["variant"] == "A" else plist[1]
    case_b = plist[1] if plist[1]["variant"] == "B" else plist[0]
    
    is_consistent = (case_a["predicted"] == case_b["predicted"])
    is_correct = (case_a["correct"] and case_b["correct"])
    
    if is_consistent:
        consistent_pairs += 1
    if is_correct:
        correct_pairs += 1
        
    pair_results.append({
        "pair_id": base_id,
        "reference_class": case_a["reference"],
        "case_a_id": case_a["id"],
        "case_a_pred": case_a["predicted"],
        "case_b_id": case_b["id"],
        "case_b_pred": case_b["predicted"],
        "consistent": is_consistent,
        "both_correct": is_correct
    })

total_pairs = len(pairs)
pair_consistency_rate = consistent_pairs / total_pairs if total_pairs > 0 else 0.0
pair_correctness_rate = correct_pairs / total_pairs if total_pairs > 0 else 0.0

# Compile criteria evaluation
criteria_eval = {
    "global_exact_accuracy": {
        "target": ">= 0.7500 (75.0%)",
        "achieved": round(accuracy, 4),
        "status": "PASSED" if accuracy >= 0.75 else "BLOCKED"
    },
    "recall_direct": {
        "target": ">= 0.8500 (85.0%)",
        "achieved": class_metrics["DIRECT"]["recall"],
        "status": "PASSED" if class_metrics["DIRECT"]["recall"] >= 0.85 else "BLOCKED"
    },
    "precision_direct": {
        "target": ">= 0.7000 (70.0%)",
        "achieved": class_metrics["DIRECT"]["precision"],
        "status": "PASSED" if class_metrics["DIRECT"]["precision"] >= 0.70 else "BLOCKED"
    },
    "false_direct_divergence_rate": {
        "target": "<= 0.1000 (10.0%)",
        "achieved": round(false_direct_divergence_rate, 4),
        "status": "PASSED" if false_direct_divergence_rate <= 0.10 else "BLOCKED"
    },
    "recall_partial": {
        "target": ">= 0.6000 (60.0%)",
        "achieved": class_metrics["PARTIAL"]["recall"],
        "status": "PASSED" if class_metrics["PARTIAL"]["recall"] >= 0.60 else "BLOCKED"
    },
    "invariance_paired_correctness": {
        "target": ">= 0.8000 (80.0%)",
        "achieved": round(pair_correctness_rate, 4),
        "status": "PASSED" if pair_correctness_rate >= 0.80 else "BLOCKED"
    }
}

all_passed = all(v["status"] == "PASSED" for v in criteria_eval.values())
recommended_gate = "BLIND_SEMANTIC_REVALIDATION_PASSED" if all_passed else "BLIND_SEMANTIC_REVALIDATION_BLOCKED"

print("================================================================================")
print("STAGE 31.7.28 BLIND EVALUATION METRICS REPORT")
print("================================================================================")
print(f"Total Cases Evaluated: {total}")
print(f"Total Correct: {correct} ({accuracy*100:.2f}%)")
print(f"Total Divergent: {divergent_count} ({(1-accuracy)*100:.2f}%)")
print(f"False DIRECTs count: {fp_direct} (Rate among divergences: {false_direct_divergence_rate*100:.2f}%)")
print(f"Paired Invariance: Consistent {consistent_pairs}/{total_pairs} ({pair_consistency_rate*100:.1f}%), Both Correct {correct_pairs}/{total_pairs} ({pair_correctness_rate*100:.1f}%)")
print(f"Recommended Gate: {recommended_gate}")
print("--------------------------------------------------------------------------------")
print("CRITERIA EVALUATION:")
for k, v in criteria_eval.items():
    print(f"  {k:<32}: target={v['target']:<20} achieved={v['achieved']} -> {v['status']}")

print("\nConfusion Matrix:")
print("Ref \\ Pred\t" + "\t".join(classes))
for r in classes:
    row = [str(matrix[r][p]) for p in classes]
    print(f"{r:<14}\t" + "\t".join(row))

# Export Deliverable 6: stage_31_7_28_metrics_summary.json
metrics_summary = {
    "stage": "31.7.28",
    "evaluation_mode": "INDEPENDENT_BLIND_VALIDATION",
    "runtime_evaluated": "reference_runtime/runtime.py",
    "runtime_sha256": "6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28",
    "total_cases": total,
    "correct_cases": correct,
    "divergent_cases": divergent_count,
    "global_exact_accuracy": round(accuracy, 4),
    "false_direct_count": fp_direct,
    "false_direct_rate_among_divergences": round(false_direct_divergence_rate, 4),
    "criteria_evaluation": criteria_eval,
    "gate_decision": recommended_gate,
    "provenance_limitation": "REFERENCE_INDEPENDENCE_UNRESOLVED",
    "class_metrics": class_metrics,
    "invariance_metrics": {
        "total_pairs": total_pairs,
        "consistent_pairs": consistent_pairs,
        "pair_consistency_rate": round(pair_consistency_rate, 4),
        "both_correct_pairs": correct_pairs,
        "pair_correctness_rate": round(pair_correctness_rate, 4)
    },
    "group_breakdown": {g: {"total": d["total"], "correct": d["correct"], "accuracy": round(d["correct"]/d["total"], 4)} for g, d in by_group.items()},
    "family_breakdown": {f: {"total": d["total"], "correct": d["correct"], "accuracy": round(d["correct"]/d["total"], 4)} for f, d in by_family.items()},
    "question_type_breakdown": {q: {"total": d["total"], "correct": d["correct"], "accuracy": round(d["correct"]/d["total"], 4)} for q, d in by_qtype.items()},
    "linguistic_form_breakdown": {l: {"total": d["total"], "correct": d["correct"], "accuracy": round(d["correct"]/d["total"], 4)} for l, d in by_ling.items()}
}

with open(pilot_dir / "stage_31_7_28_metrics_summary.json", "w", encoding="utf-8") as f:
    json.dump(metrics_summary, f, indent=2, ensure_ascii=False)

# Export Deliverable 7: stage_31_7_28_confusion_matrix.json
conf_matrix_data = {
    "classes": classes,
    "matrix": {r: dict(matrix[r]) for r in classes},
    "support": {c: sum(matrix[c].values()) for c in classes},
    "predicted_counts": {c: sum(matrix[r][c] for r in classes) for c in classes}
}
with open(pilot_dir / "stage_31_7_28_confusion_matrix.json", "w", encoding="utf-8") as f:
    json.dump(conf_matrix_data, f, indent=2, ensure_ascii=False)

# Export Deliverable 8: stage_31_7_28_invariance_results.json
invariance_data = {
    "total_pairs": total_pairs,
    "consistent_pairs": consistent_pairs,
    "consistency_rate": round(pair_consistency_rate, 4),
    "both_correct_pairs": correct_pairs,
    "correctness_rate": round(pair_correctness_rate, 4),
    "pairs": pair_results
}
with open(pilot_dir / "stage_31_7_28_invariance_results.json", "w", encoding="utf-8") as f:
    json.dump(invariance_data, f, indent=2, ensure_ascii=False)

# Export Deliverable 9: stage_31_7_28_divergence_analysis.json
divergence_output = {
    "total_divergences": len(divergences),
    "divergences_by_type": dict(Counter(d["divergence_type"] for d in divergences)),
    "divergent_cases": divergences
}
with open(pilot_dir / "stage_31_7_28_divergence_analysis.json", "w", encoding="utf-8") as f:
    json.dump(divergence_output, f, indent=2, ensure_ascii=False)

print("\nSaved deliverables:")
print("- stage_31_7_28_metrics_summary.json")
print("- stage_31_7_28_confusion_matrix.json")
print("- stage_31_7_28_invariance_results.json")
print("- stage_31_7_28_divergence_analysis.json")
