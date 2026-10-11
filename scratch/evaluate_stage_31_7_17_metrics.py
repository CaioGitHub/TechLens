"""
Stage 31.7.17: Metrics Evaluation and Divergence Analysis Script.
Compares sealed ground truth against frozen system predictions.
Computes exact agreement, per-class metrics, macro-F1, confusion matrix,
divergences breakdown, and representation invariance.
"""

import json
from collections import defaultdict, Counter

p_gt = "scratch/stage_31_7_17_ground_truth.json"
p_pred = "scratch/stage_31_7_17_system_predictions.json"

with open(p_gt, "r", encoding="utf-8") as f:
    gt_data = json.load(f)

with open(p_pred, "r", encoding="utf-8") as f:
    pred_data = json.load(f)

gt_by_id = {c["id"]: c for c in gt_data}
pred_by_id = {c["id"]: c for c in pred_data}

CLASSES = ["DIRECT", "PARTIAL", "SUPPORTING", "RELATED", "OFF_TOPIC", "INSUFFICIENT", "UNKNOWN"]

# 1. Verification of IDs and total cases
assert len(gt_data) == 200, f"Expected 200 ground truth cases, got {len(gt_data)}"
assert len(pred_data) == 200, f"Expected 200 predictions, got {len(pred_data)}"
assert set(gt_by_id.keys()) == set(pred_by_id.keys()), "ID mismatch between GT and predictions"

# Confusion matrix: conf_matrix[ref][pred]
conf_matrix = {c: {p: 0 for p in CLASSES} for c in CLASSES}
divergences = []
concordances = []

for cid, gt in gt_by_id.items():
    pred = pred_by_id[cid]
    ref_cls = gt["human_classification"]
    pred_cls = pred["predicted_classification"]
    
    if ref_cls not in CLASSES or pred_cls not in CLASSES:
        raise ValueError(f"Unknown class encountered: ref={ref_cls}, pred={pred_cls} in case {cid}")
        
    conf_matrix[ref_cls][pred_cls] += 1
    
    if ref_cls == pred_cls:
        concordances.append((cid, ref_cls, gt, pred))
    else:
        divergences.append({
            "id": cid,
            "group": gt["group"],
            "question_text": gt["question_text"],
            "response_text": gt["response_text"],
            "reference_classification": ref_cls,
            "predicted_classification": pred_cls,
            "predicted_functional_contribution": pred["predicted_functional_contribution"],
            "demands": gt["demands"],
            "satisfied_aspects": gt["satisfied_aspects"],
            "semantic_rationale": gt["semantic_rationale"],
            "predicted_reason": pred["predicted_reason"],
            "linguistic_form": gt.get("linguistic_form"),
            "epistemic_status": gt.get("epistemic_status")
        })

total_cases = 200
exact_matches = len(concordances)
exact_agreement = exact_matches / total_cases

# Per-class TP, FP, FN
tp = {c: conf_matrix[c][c] for c in CLASSES}
fn = {c: sum(conf_matrix[c][p] for p in CLASSES if p != c) for c in CLASSES}
fp = {c: sum(conf_matrix[r][c] for r in CLASSES if r != c) for c in CLASSES}

precision = {}
recall = {}
f1 = {}

for c in CLASSES:
    precision[c] = tp[c] / (tp[c] + fp[c]) if (tp[c] + fp[c]) > 0 else 0.0
    recall[c] = tp[c] / (tp[c] + fn[c]) if (tp[c] + fn[c]) > 0 else 0.0
    f1[c] = (2 * precision[c] * recall[c]) / (precision[c] + recall[c]) if (precision[c] + recall[c]) > 0 else 0.0

macro_f1 = sum(f1.values()) / len(CLASSES)

# False DIRECT among divergences
total_divergences = len(divergences)
fp_direct = fp["DIRECT"]
false_direct_among_div = (fp_direct / total_divergences) if total_divergences > 0 else None

# Representation Invariance Pairs
# Pairs designed in benchmark:
invariance_pairs = [
    # DIRECT pairs:
    ("D01_vector_hnsw", "D02_vector_hnsw_informal"),
    ("D03_compaction_lsm", "D04_compaction_lsm_active"),
    ("D05_raft_log_matching", "D06_raft_log_matching_short"),
    ("D07_distributed_lock_fencing", "D08_distributed_lock_fencing_informal"),
    ("D09_kafka_zero_copy", "D10_kafka_zero_copy_active"),
    ("D11_crdt_pn_counter", "D12_crdt_pn_counter_informal"),
    ("D13_database_sharding_virtual_nodes", "D14_database_sharding_virtual_nodes_active"),
    ("D15_outbox_debezium_cdc", "D16_outbox_debezium_cdc_informal"),
    ("D17_saga_choreography_compensating", "D18_saga_choreography_compensating_short"),
    ("D43_long_direct_detailed", "D44_short_direct_concise"),
    # PARTIAL pairs:
    ("P05_explicit_omission_text", "P06_explicit_omission_text_informal"),
    ("P11_multi_aspect_idempotency_storage", "P12_multi_aspect_idempotency_storage_informal"),
    # OFF_TOPIC pairs:
    ("O01_antithesis_drop_locks", "O02_antithesis_drop_locks_inflected"),
]

invariance_matches = 0
invariance_total = len(invariance_pairs)
invariance_details = []

for id_a, id_b in invariance_pairs:
    pred_a = pred_by_id[id_a]["predicted_classification"]
    pred_b = pred_by_id[id_b]["predicted_classification"]
    is_inv = (pred_a == pred_b)
    if is_inv:
        invariance_matches += 1
    invariance_details.append({
        "pair": f"{id_a} <-> {id_b}",
        "pred_a": pred_a,
        "pred_b": pred_b,
        "invariant": is_inv
    })

invariance_rate = invariance_matches / invariance_total

# Performance by Semantic Group
group_stats = defaultdict(lambda: {"total": 0, "correct": 0})
for cid, gt in gt_by_id.items():
    grp = gt["group"]
    group_stats[grp]["total"] += 1
    if gt["human_classification"] == pred_by_id[cid]["predicted_classification"]:
        group_stats[grp]["correct"] += 1

# Output report to console and save to scratch
output = {
    "total_cases": total_cases,
    "exact_matches": exact_matches,
    "exact_agreement": round(exact_agreement, 4),
    "exact_agreement_pct": f"{exact_agreement * 100:.2f}%",
    "direct_recall": {
        "tp": tp["DIRECT"],
        "fn": fn["DIRECT"],
        "total_ref_direct": tp["DIRECT"] + fn["DIRECT"],
        "recall": round(recall["DIRECT"], 4),
        "recall_pct": f"{recall['DIRECT'] * 100:.2f}%"
    },
    "direct_precision": {
        "tp": tp["DIRECT"],
        "fp": fp["DIRECT"],
        "total_pred_direct": tp["DIRECT"] + fp["DIRECT"],
        "precision": round(precision["DIRECT"], 4),
        "precision_pct": f"{precision['DIRECT'] * 100:.2f}%"
    },
    "false_direct_among_divergences": {
        "fp_direct": fp_direct,
        "total_divergences": total_divergences,
        "rate": round(false_direct_among_div, 4) if false_direct_among_div is not None else None,
        "rate_pct": f"{false_direct_among_div * 100:.2f}%" if false_direct_among_div is not None else "N/A"
    },
    "partial_recall": {
        "tp": tp["PARTIAL"],
        "fn": fn["PARTIAL"],
        "total_ref_partial": tp["PARTIAL"] + fn["PARTIAL"],
        "recall": round(recall["PARTIAL"], 4),
        "recall_pct": f"{recall['PARTIAL'] * 100:.2f}%"
    },
    "representation_invariance": {
        "matches": invariance_matches,
        "total_pairs": invariance_total,
        "rate": round(invariance_rate, 4),
        "rate_pct": f"{invariance_rate * 100:.2f}%",
        "pairs": invariance_details
    },
    "macro_f1": round(macro_f1, 4),
    "macro_f1_pct": f"{macro_f1 * 100:.2f}%",
    "per_class": {
        c: {
            "ref_count": sum(conf_matrix[c].values()),
            "pred_count": sum(conf_matrix[r][c] for r in CLASSES),
            "tp": tp[c],
            "fp": fp[c],
            "fn": fn[c],
            "precision": round(precision[c], 4),
            "recall": round(recall[c], 4),
            "f1": round(f1[c], 4)
        } for c in CLASSES
    },
    "confusion_matrix": conf_matrix,
    "group_performance": {
        grp: {
            "correct": stat["correct"],
            "total": stat["total"],
            "accuracy": round(stat["correct"] / stat["total"], 4),
            "accuracy_pct": f"{(stat['correct'] / stat['total']) * 100:.2f}%"
        } for grp, stat in sorted(group_stats.items())
    },
    "divergences_count": total_divergences,
    "divergences": divergences
}

with open("scratch/stage_31_7_17_metrics_summary.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("=" * 80)
print("STAGE 31.7.17 BLIND VALIDATION METRICS SUMMARY")
print("=" * 80)
print(f"Total Cases: {total_cases}")
print(f"Exact Agreement: {exact_matches}/{total_cases} ({exact_agreement * 100:.2f}%) [Threshold: >= 75%]")
print(f"DIRECT Recall:   {tp['DIRECT']}/{tp['DIRECT'] + fn['DIRECT']} ({recall['DIRECT'] * 100:.2f}%) [Threshold: >= 85%]")
print(f"DIRECT Precision:{tp['DIRECT']}/{tp['DIRECT'] + fp['DIRECT']} ({precision['DIRECT'] * 100:.2f}%) [Threshold: >= 70%]")
print(f"False DIRECT among Divergences: {fp_direct}/{total_divergences} ({false_direct_among_div * 100:.2f}%) [Threshold: <= 10%]")
print(f"PARTIAL Recall:  {tp['PARTIAL']}/{tp['PARTIAL'] + fn['PARTIAL']} ({recall['PARTIAL'] * 100:.2f}%) [Threshold: >= 60%]")
print(f"Representation Invariance: {invariance_matches}/{invariance_total} ({invariance_rate * 100:.2f}%) [Threshold: >= 80%]")
print(f"Macro-F1:        {macro_f1 * 100:.2f}%")
print(f"Total Divergences: {total_divergences}")
print("=" * 80)
print("\nConfusion Matrix (Rows = Reference, Columns = Predicted):")
header = f"{'REF \\ PRED':<14}" + "".join(f"{c:>12}" for c in CLASSES) + f"{'TOTAL':>8}"
print(header)
print("-" * len(header))
for r in CLASSES:
    row = f"{r:<14}" + "".join(f"{conf_matrix[r][p]:>12}" for p in CLASSES) + f"{sum(conf_matrix[r].values()):>8}"
    print(row)
print("-" * len(header))
pred_totals = f"{'PRED TOTAL':<14}" + "".join(f"{sum(conf_matrix[r][c] for r in CLASSES):>12}" for c in CLASSES) + f"{total_cases:>8}"
print(pred_totals)

print("\nPer-Class Metrics:")
print(f"{'Class':<14}{'Ref':>6}{'Pred':>6}{'TP':>6}{'FP':>6}{'FN':>6}{'Precision':>12}{'Recall':>10}{'F1':>10}")
for c in CLASSES:
    ref_cnt = sum(conf_matrix[c].values())
    pred_cnt = sum(conf_matrix[r][c] for r in CLASSES)
    print(f"{c:<14}{ref_cnt:>6}{pred_cnt:>6}{tp[c]:>6}{fp[c]:>6}{fn[c]:>6}{precision[c]*100:>11.2f}%{recall[c]*100:>9.2f}%{f1[c]*100:>9.2f}%")

print("\nGroup Accuracy Breakdown:")
for grp, stat in sorted(group_stats.items()):
    pct = (stat['correct'] / stat['total']) * 100
    print(f"  {grp:<30}: {stat['correct']:>2}/{stat['total']:>2} ({pct:.1f}%)")

if divergences:
    print(f"\nDivergences List ({len(divergences)} cases):")
    for d in divergences:
        reason_str = (d['predicted_reason'] or '')[:60]
        print(f"  [{d['id']}] Ref={d['reference_classification']:<11} Pred={d['predicted_classification']:<11} | Q: {d['question_text'][:50]}... | Reason: {reason_str}...")
