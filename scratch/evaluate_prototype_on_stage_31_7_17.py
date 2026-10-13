"""
Evaluate RemediatedPropositionEngine prototype against stage_31_7_17_ground_truth.json
"""

import json
import sys
sys.path.insert(0, ".")
from scratch.test_remediation_prototype import RemediatedPropositionEngine

def run_evaluation():
    engine = RemediatedPropositionEngine()

    with open("11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_17_ground_truth.json", encoding="utf-8") as f:
        gt_data = json.load(f)

    results = []
    exact_matches = 0
    total = len(gt_data)
    
    classes = ["DIRECT", "PARTIAL", "SUPPORTING", "RELATED", "OFF_TOPIC", "INSUFFICIENT", "UNKNOWN"]
    conf_matrix = {r: {p: 0 for p in classes} for r in classes}

    direct_tp = 0
    direct_fp = 0
    direct_fn = 0
    partial_tp = 0
    partial_fn = 0

    for item in gt_data:
        cid = item["id"]
        q = item["question_text"]
        r = item["response_text"]
        ref = item["human_classification"]

        res = engine.evaluate(q, r)
        pred = res["classification"]

        conf_matrix[ref][pred] += 1
        if pred == ref:
            exact_matches += 1
            if ref == "DIRECT":
                direct_tp += 1
            elif ref == "PARTIAL":
                partial_tp += 1
        else:
            if pred == "DIRECT":
                direct_fp += 1
            if ref == "DIRECT":
                direct_fn += 1
            if ref == "PARTIAL":
                partial_fn += 1

        results.append({
            "id": cid,
            "ref": ref,
            "pred": pred,
            "match": pred == ref
        })

    exact_acc = exact_matches / total
    direct_prec = direct_tp / (direct_tp + direct_fp) if (direct_tp + direct_fp) > 0 else 0
    direct_rec = direct_tp / (direct_tp + direct_fn) if (direct_tp + direct_fn) > 0 else 0
    divergences = total - exact_matches
    fp_direct_among_div = direct_fp / divergences if divergences > 0 else 0
    partial_rec = partial_tp / (partial_tp + partial_fn) if (partial_tp + partial_fn) > 0 else 0

    print("--- EVALUATION RESULTS ON STAGE 31.7.17 BENCHMARK ---")
    print(f"Total Cases: {total}")
    print(f"Exact Agreement: {exact_matches} / {total} = {exact_acc:.4f} ({exact_acc*100:.2f}%) [Target >= 75.0%]")
    print(f"DIRECT Recall:   {direct_tp} / {direct_tp + direct_fn} = {direct_rec:.4f} ({direct_rec*100:.2f}%) [Target >= 85.0%]")
    print(f"DIRECT Precision:{direct_tp} / {direct_tp + direct_fp} = {direct_prec:.4f} ({direct_prec*100:.2f}%) [Target >= 70.0%]")
    print(f"FP DIRECT among Div: {direct_fp} / {divergences} = {fp_direct_among_div:.4f} ({fp_direct_among_div*100:.2f}%) [Target <= 10.0%]")
    print(f"PARTIAL Recall:  {partial_tp} / {partial_tp + partial_fn} = {partial_rec:.4f} ({partial_rec*100:.2f}%) [Target >= 60.0%]")

    print("\n--- CONFUSION MATRIX ---")
    print(f"{'REF \\ PRED':<14}" + "".join(f"{c:>12}" for c in classes) + f"{'TOTAL':>10}")
    for r in classes:
        row_str = f"{r:<14}" + "".join(f"{conf_matrix[r][c]:>12}" for c in classes) + f"{sum(conf_matrix[r].values()):>10}"
        print(row_str)

    # Invariance check
    with open("11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_17_metrics_summary.json", encoding="utf-8") as f:
        summary = json.load(f)
    pairs = summary["representation_invariance"]["pairs"]
    
    pred_map = {r["id"]: r["pred"] for r in results}
    inv_matches = 0
    print("\n--- INVARIANCE PAIRS ---")
    for p in pairs:
        pair_str = p["pair"]
        id_a, id_b = pair_str.split(" <-> ")
        pred_a = pred_map.get(id_a)
        pred_b = pred_map.get(id_b)
        is_inv = pred_a == pred_b
        if is_inv:
            inv_matches += 1
        print(f"  {id_a} ({pred_a}) <-> {id_b} ({pred_b}) : {'INVARIANT' if is_inv else 'BROKEN'}")
    inv_rate = inv_matches / len(pairs)
    print(f"Invariance Rate: {inv_matches} / {len(pairs)} = {inv_rate:.4f} ({inv_rate*100:.2f}%) [Target >= 80.0%]")

if __name__ == "__main__":
    run_evaluation()
