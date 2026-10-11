import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(".").resolve()))

from reference_runtime.runtime import evaluate_open_domain_semantic_relevance

p = "C:/Users/caiop/.gemini/antigravity-ide/brain/8baa1ac5-b48e-4706-9d0f-5c766d5d6bc4/scratch/"
gt = json.load(open(p + "stage_31_7_13_ground_truth.json", encoding="utf-8"))

classes = ["DIRECT", "PARTIAL", "SUPPORTING", "RELATED", "OFF_TOPIC", "INSUFFICIENT", "UNKNOWN"]
matrix = {c1: {c2: 0 for c2 in classes} for c1 in classes}
correct = 0

predictions = []
for item in gt:
    res = evaluate_open_domain_semantic_relevance(item["question_text"], item["response_text"])
    pred = res["classification"]
    ref = item["human_classification"]
    predictions.append({"id": item["id"], "ref": ref, "pred": pred})
    if pred == ref:
        correct += 1
    matrix[ref][pred] += 1

print(f"Total Cases: {len(gt)}")
print(f"Global Exact Agreement: {correct}/{len(gt)} ({correct/len(gt)*100:.2f}%)")

print("\nConfusion Matrix:")
print(f"{'REF / PRED':<14} | " + " | ".join(f"{c:>10}" for c in classes) + " | Total")
for ref in classes:
    tot = sum(matrix[ref].values())
    row_str = " | ".join(f"{matrix[ref][p]:>10}" for p in classes)
    print(f"{ref:<14} | {row_str} | {tot:>5}")

# Invariance Group O
group_o = [c for c in gt if c.get("group") == "O"]
o_dict = {c["id"]: evaluate_open_domain_semantic_relevance(c["question_text"], c["response_text"])["classification"] for c in group_o}
pairs_inv = 0
for i in range(1, 11):
    f_id = f"O{2*i-1:02d}"
    inf_id = f"O{2*i:02d}"
    f_matches = [k for k in o_dict if k.startswith(f_id)]
    inf_matches = [k for k in o_dict if k.startswith(inf_id)]
    if f_matches and inf_matches:
        f_pred = o_dict[f_matches[0]]
        inf_pred = o_dict[inf_matches[0]]
        match = f_pred == inf_pred
        if match:
            pairs_inv += 1
        print(f"Pair {i}: {f_matches[0]} ({f_pred}) vs {inf_matches[0]} ({inf_pred}) -> {'MATCH' if match else 'DIVERGE'}")

print(f"\nGroup O Representation Invariance: {pairs_inv}/10 ({pairs_inv/10*100:.1f}%)")

# Metrics for DIRECT
tp_dir = matrix["DIRECT"]["DIRECT"]
tot_pred_dir = sum(matrix[r]["DIRECT"] for r in classes)
tot_ref_dir = sum(matrix["DIRECT"].values())
fp_dir = tot_pred_dir - tp_dir
fn_dir = tot_ref_dir - tp_dir

prec_dir = tp_dir / tot_pred_dir if tot_pred_dir else 0
rec_dir = tp_dir / tot_ref_dir if tot_ref_dir else 0

tot_div = len(gt) - correct
fp_div = fp_dir / tot_div if tot_div else 0

print(f"\nDIRECT Recall: {tp_dir}/{tot_ref_dir} ({rec_dir*100:.2f}%)")
print(f"DIRECT Precision: {tp_dir}/{tot_pred_dir} ({prec_dir*100:.2f}%)")
print(f"False DIRECT among Divergences: {fp_dir}/{tot_div} ({fp_div*100:.2f}%)")

# PARTIAL metrics
tp_part = matrix["PARTIAL"]["PARTIAL"]
tot_ref_part = sum(matrix["PARTIAL"].values())
rec_part = tp_part / tot_ref_part if tot_ref_part else 0
print(f"PARTIAL Recall: {tp_part}/{tot_ref_part} ({rec_part*100:.2f}%)")

# Supporting metrics
tp_supp = matrix["SUPPORTING"]["SUPPORTING"]
tot_ref_supp = sum(matrix["SUPPORTING"].values())
rec_supp = tp_supp / tot_ref_supp if tot_ref_supp else 0
print(f"SUPPORTING Recall: {tp_supp}/{tot_ref_supp} ({rec_supp*100:.2f}%)")

# Related metrics
tp_rel = matrix["RELATED"]["RELATED"]
tot_ref_rel = sum(matrix["RELATED"].values())
rec_rel = tp_rel / tot_ref_rel if tot_ref_rel else 0
print(f"RELATED Recall: {tp_rel}/{tot_ref_rel} ({rec_rel*100:.2f}%)")

# Off-topic metrics
tp_off = matrix["OFF_TOPIC"]["OFF_TOPIC"]
tot_ref_off = sum(matrix["OFF_TOPIC"].values())
rec_off = tp_off / tot_ref_off if tot_ref_off else 0
print(f"OFF_TOPIC Recall: {tp_off}/{tot_ref_off} ({rec_off*100:.2f}%)")

# Save predictions for record
with open("scratch/stage_31_7_16_runtime_predictions.json", "w", encoding="utf-8") as f:
    json.dump(predictions, f, indent=2, ensure_ascii=False)
