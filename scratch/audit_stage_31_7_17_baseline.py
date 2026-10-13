"""
Stage 31.7.18: Diagnostic Script to Recalculate and Audit Baseline Metrics
Reads directly from frozen artifacts:
- 11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_17_ground_truth.json
- 11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_17_system_predictions.json
"""

import json
from pathlib import Path

p_gt = Path("11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_17_ground_truth.json")
p_pred = Path("11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_17_system_predictions.json")

gt_data = json.loads(p_gt.read_text(encoding="utf-8"))
pred_data = json.loads(p_pred.read_text(encoding="utf-8"))

print(f"Total Ground Truth cases: {len(gt_data)}")
print(f"Total System Predictions: {len(pred_data)}")

gt_ids = [c["id"] for c in gt_data]
pred_ids = [c["id"] for c in pred_data]

# Check uniqueness
dup_gt = [x for x in gt_ids if gt_ids.count(x) > 1]
dup_pred = [x for x in pred_ids if pred_ids.count(x) > 1]
print(f"Duplicate GT IDs: {set(dup_gt)}")
print(f"Duplicate Pred IDs: {set(dup_pred)}")

# Check 1:1 match
diff_ids = set(gt_ids).symmetric_difference(set(pred_ids))
print(f"ID symmetric difference: {diff_ids}")

CLASSES = ["DIRECT", "PARTIAL", "SUPPORTING", "RELATED", "OFF_TOPIC", "INSUFFICIENT", "UNKNOWN"]

# Validate classes
gt_invalid = [c["id"] for c in gt_data if c["human_classification"] not in CLASSES]
pred_invalid = [c["id"] for c in pred_data if c["predicted_classification"] not in CLASSES]
print(f"Invalid GT classes: {gt_invalid}")
print(f"Invalid Pred classes: {pred_invalid}")

# Compute Confusion Matrix
gt_map = {c["id"]: c for c in gt_data}
pred_map = {c["id"]: c for c in pred_data}

conf_matrix = {r: {c: 0 for c in CLASSES} for r in CLASSES}
divergences = []
concordances = []

for cid in gt_ids:
    r_cls = gt_map[cid]["human_classification"]
    p_cls = pred_map[cid]["predicted_classification"]
    conf_matrix[r_cls][p_cls] += 1
    if r_cls == p_cls:
        concordances.append(cid)
    else:
        divergences.append((cid, r_cls, p_cls))

print("\n--- CONFUSION MATRIX ---")
header = f"{'REF \\ PRED':<14}" + "".join(f"{c:>12}" for c in CLASSES) + f"{'TOTAL':>8}"
print(header)
for r in CLASSES:
    row = f"{r:<14}" + "".join(f"{conf_matrix[r][c]:>12}" for c in CLASSES) + f"{sum(conf_matrix[r].values()):>8}"
    print(row)
pred_totals = f"{'TOTAL PRED':<14}" + "".join(f"{sum(conf_matrix[r][c] for r in CLASSES):>12}" for c in CLASSES) + f"{len(gt_ids):>8}"
print(pred_totals)

# Metrics
total = len(gt_ids)
exact_acc = len(concordances) / total
tp_direct = conf_matrix["DIRECT"]["DIRECT"]
fn_direct = sum(conf_matrix["DIRECT"][c] for c in CLASSES if c != "DIRECT")
fp_direct = sum(conf_matrix[r]["DIRECT"] for r in CLASSES if r != "DIRECT")

recall_direct = tp_direct / (tp_direct + fn_direct)
prec_direct = tp_direct / (tp_direct + fp_direct)

total_div = len(divergences)
fp_direct_div_rate = fp_direct / total_div

tp_partial = conf_matrix["PARTIAL"]["PARTIAL"]
fn_partial = sum(conf_matrix["PARTIAL"][c] for c in CLASSES if c != "PARTIAL")
recall_partial = tp_partial / (tp_partial + fn_partial)

print("\n--- RECALCULATED METRICS ---")
print(f"Exact Agreement: {len(concordances)} / {total} = {exact_acc:.4f} ({exact_acc*100:.2f}%)")
print(f"DIRECT Recall:   {tp_direct} / {tp_direct + fn_direct} = {recall_direct:.4f} ({recall_direct*100:.2f}%)")
print(f"DIRECT Precision:{tp_direct} / {tp_direct + fp_direct} = {prec_direct:.4f} ({prec_direct*100:.2f}%)")
print(f"FP DIRECT among Div: {fp_direct} / {total_div} = {fp_direct_div_rate:.4f} ({fp_direct_div_rate*100:.2f}%)")
print(f"PARTIAL Recall:  {tp_partial} / {tp_partial + fn_partial} = {recall_partial:.4f} ({recall_partial*100:.2f}%)")

# Audit breakdown of FP_DIRECT (44 cases)
fp_direct_sources = {}
for r in CLASSES:
    if r != "DIRECT":
        fp_direct_sources[r] = conf_matrix[r]["DIRECT"]
print("\n--- FP DIRECT BREAKDOWN BY REFERENCE CLASS ---")
for r, cnt in fp_direct_sources.items():
    print(f"  {r:<14} -> DIRECT : {cnt} cases ({cnt/fp_direct*100:.1f}%)")
