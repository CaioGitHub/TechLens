import json
from pathlib import Path

gt_p = Path('11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_25_ground_truth.json')
pred_p = Path('11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_25_system_predictions.json')
cm_p = Path('11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_25_confusion_matrix.json')
metrics_p = Path('11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_25_metrics_summary.json')

gt = json.loads(gt_p.read_text(encoding='utf-8'))
preds = json.loads(pred_p.read_text(encoding='utf-8'))
saved_cm = json.loads(cm_p.read_text(encoding='utf-8'))
saved_metrics = json.loads(metrics_p.read_text(encoding='utf-8'))

gt_map = {item['id']: item for item in gt}
pred_map = {item['id']: item for item in preds}

classes = ['DIRECT', 'PARTIAL', 'SUPPORTING', 'RELATED', 'OFF_TOPIC', 'INSUFFICIENT', 'UNKNOWN']
calc_cm = {r: {p: 0 for p in classes} for r in classes}

correct = 0
divs = []

for cid, item in gt_map.items():
    ref = item['human_classification']
    pred = pred_map[cid]['predicted_classification']
    calc_cm[ref][pred] += 1
    if ref == pred:
        correct += 1
    else:
        divs.append((cid, ref, pred))

print(f"Total cases: {len(gt)}")
print(f"Recalculated correct: {correct} ({correct/len(gt):.2%})")
print(f"Recalculated divergences: {len(divs)}")
print(f"CM matches saved: {calc_cm == saved_cm}")

total_cm_cells = sum(sum(calc_cm[r].values()) for r in classes)
print(f"Total CM cell sum: {total_cm_cells}")

fp_direct = sum(calc_cm[r]['DIRECT'] for r in classes if r != 'DIRECT')
print(f"FP DIRECT total: {fp_direct}")
print("FP DIRECT by ref class:")
for r in classes:
    if r != 'DIRECT' and calc_cm[r]['DIRECT'] > 0:
        print(f"  {r} -> DIRECT: {calc_cm[r]['DIRECT']}")

tp_direct = calc_cm['DIRECT']['DIRECT']
total_ref_direct = sum(calc_cm['DIRECT'].values())
total_pred_direct = sum(calc_cm[r]['DIRECT'] for r in classes)

print("\nExact Numerators & Denominators:")
print(f"Exact Agreement: {correct} / {len(gt)} = {correct/len(gt):.4f}")
print(f"Recall DIRECT: {tp_direct} / {total_ref_direct} = {tp_direct/total_ref_direct:.4f}")
print(f"Precision DIRECT: {tp_direct} / {total_pred_direct} = {tp_direct/total_pred_direct:.4f}")
print(f"False DIRECT among Divergences: {fp_direct} / {len(divs)} = {fp_direct/len(divs):.4f}")
tp_partial = calc_cm['PARTIAL']['PARTIAL']
total_ref_partial = sum(calc_cm['PARTIAL'].values())
print(f"Recall PARTIAL: {tp_partial} / {total_ref_partial} = {tp_partial/total_ref_partial:.4f}")
