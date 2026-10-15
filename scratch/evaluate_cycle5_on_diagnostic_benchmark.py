import json, sys
from pathlib import Path

sys.path.insert(0, '.')
from scratch.test_refined_cycle5_runtime import refined_engine

gt_p = Path('11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_25_ground_truth.json')
gt = json.loads(gt_p.read_text(encoding='utf-8'))
gt_map = {item['id']: item for item in gt}

pred_p = Path('11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_25_system_predictions.json')
preds = json.loads(pred_p.read_text(encoding='utf-8'))
pred_map = {item['id']: item for item in preds}

classes = ["DIRECT", "PARTIAL", "SUPPORTING", "RELATED", "OFF_TOPIC", "INSUFFICIENT", "UNKNOWN"]
confusion = {r: {p: 0 for p in classes} for r in classes}

correct = 0
total = len(gt)
baseline_correct = sum(1 for cid, p in pred_map.items() if p['predicted_classification'] == gt_map[cid]['human_classification'])

for c in gt:
    cid = c['id']
    ref = c['human_classification']
    res = refined_engine.evaluate_relevance(c['question_text'], c['response_text'])
    pred_cls = res['classification']
    confusion[ref][pred_cls] += 1
    if ref == pred_cls:
        correct += 1

print(f"Total cases: {total}")
print(f"Baseline (Stage 31.7.25) correct: {baseline_correct} ({baseline_correct/total*100:.2f}%)")
print(f"Cycle 5 Prototype correct: {correct} ({correct/total*100:.2f}%)")
print(f"Net gain: +{correct - baseline_correct} cases (+{(correct - baseline_correct)/total*100:.2f} percentage points)")

tp_direct = confusion["DIRECT"]["DIRECT"]
fp_direct = sum(confusion[r]["DIRECT"] for r in classes if r != "DIRECT")
fn_direct = sum(confusion["DIRECT"][p] for p in classes if p != "DIRECT")
prec_direct = tp_direct / (tp_direct + fp_direct) if (tp_direct + fp_direct) > 0 else 0
rec_direct = tp_direct / (tp_direct + fn_direct) if (tp_direct + fn_direct) > 0 else 0
divergences = total - correct
false_direct_rate = fp_direct / divergences if divergences > 0 else 0

print("\n--- Cycle 5 Prototype DIRECT Metrics ---")
print(f"TP DIRECT: {tp_direct}")
print(f"FP DIRECT: {fp_direct} (was 70 in Stage 31.7.25)")
print(f"FN DIRECT: {fn_direct}")
print(f"Recall DIRECT: {rec_direct*100:.2f}% (limiar >= 85%)")
print(f"Precision DIRECT: {prec_direct*100:.2f}% (limiar >= 70%) (was 41.67%)")
print(f"False DIRECT rate among divergences: {false_direct_rate*100:.2f}% (limiar <= 10%) (was 71.43%)")

print("\n--- Confusion Matrix ---")
header = f"{'Ref \\ Pred':<15}" + "".join(f"{c:<13}" for c in classes)
print(header)
for r in classes:
    row = f"{r:<15}" + "".join(f"{confusion[r][c]:<13}" for c in classes)
    print(row)
