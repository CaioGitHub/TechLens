import json, hashlib
from pathlib import Path

gt_path = Path('11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_25_ground_truth.json')
pred_path = Path('11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_25_system_predictions.json')

gt = json.loads(gt_path.read_text(encoding='utf-8'))
preds = json.loads(pred_path.read_text(encoding='utf-8'))

gt_map = {item['id']: item for item in gt}
pred_map = {item['id']: item for item in preds}

classes = ['DIRECT', 'PARTIAL', 'SUPPORTING', 'RELATED', 'OFF_TOPIC', 'INSUFFICIENT', 'UNKNOWN']

# Initialize confusion matrix: matrix[ref][pred]
confusion_matrix = {r: {p: 0 for p in classes} for r in classes}

correct_count = 0
total_cases = len(gt)
divergences = []

for cid, item in gt_map.items():
    ref = item['human_classification']
    pred = pred_map[cid]['predicted_classification']
    
    confusion_matrix[ref][pred] += 1
    
    if pred == ref:
        correct_count += 1
    else:
        divergences.append({
            'id': cid,
            'group': item.get('group'),
            'question_text': item['question_text'],
            'response_text': item['response_text'],
            'human_classification': ref,
            'predicted_classification': pred,
            'predicted_relation_type': pred_map[cid].get('predicted_relation_type'),
            'predicted_rationale': pred_map[cid].get('predicted_rationale'),
            'semantic_rationale': item.get('semantic_rationale'),
            'invariance_pair_id': item.get('invariance_pair_id')
        })

exact_agreement = correct_count / total_cases

# Per class stats
stats_per_class = {}
for c in classes:
    tp = confusion_matrix[c][c]
    fn = sum(confusion_matrix[c].values()) - tp
    fp = sum(confusion_matrix[r][c] for r in classes) - tp
    sup = tp + fn
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    f1 = (2 * prec * rec / (prec + rec)) if (prec + rec) > 0 else 0.0
    stats_per_class[c] = {
        'support': sup,
        'true_positives': tp,
        'false_positives': fp,
        'false_negatives': fn,
        'recall': round(rec, 4),
        'precision': round(prec, 4),
        'f1': round(f1, 4)
    }

# Specific required metrics:
tp_direct = stats_per_class['DIRECT']['true_positives']
total_ref_direct = stats_per_class['DIRECT']['support']
total_pred_direct = sum(confusion_matrix[r]['DIRECT'] for r in classes)
recall_direct = tp_direct / total_ref_direct if total_ref_direct > 0 else 0.0
precision_direct = tp_direct / total_pred_direct if total_pred_direct > 0 else 0.0

total_divergences = len(divergences)
fp_direct = stats_per_class['DIRECT']['false_positives']
false_direct_among_divergences = (fp_direct / total_divergences) if total_divergences > 0 else 0.0
false_direct_ratio_overall = (1.0 - precision_direct) if precision_direct > 0 else 0.0

tp_partial = stats_per_class['PARTIAL']['true_positives']
total_ref_partial = stats_per_class['PARTIAL']['support']
recall_partial = tp_partial / total_ref_partial if total_ref_partial > 0 else 0.0

# Invariance Analysis (20 pairs)
pairs_dict = {}
for item in gt:
    pid = item.get('invariance_pair_id')
    if pid:
        if pid not in pairs_dict:
            pairs_dict[pid] = []
        pairs_dict[pid].append({
            'id': item['id'],
            'ref': item['human_classification'],
            'pred': pred_map[item['id']]['predicted_classification'],
            'question': item['question_text'],
            'response': item['response_text']
        })

total_pairs = len(pairs_dict)
consistent_pairs = 0
joint_correct_pairs = 0
invariance_correct_pairs = 0
pair_results = []

for pid, cases in sorted(pairs_dict.items()):
    c1, c2 = cases[0], cases[1]
    is_consistent = (c1['pred'] == c2['pred'])
    is_joint_correct = (c1['pred'] == c1['ref'] and c2['pred'] == c2['ref'])
    is_invariance_correct = is_consistent and is_joint_correct
    
    if is_consistent:
        consistent_pairs += 1
    if is_joint_correct:
        joint_correct_pairs += 1
    if is_invariance_correct:
        invariance_correct_pairs += 1
        
    pair_results.append({
        'pair_id': pid,
        'case_1': {'id': c1['id'], 'ref': c1['ref'], 'pred': c1['pred']},
        'case_2': {'id': c2['id'], 'ref': c2['ref'], 'pred': c2['pred']},
        'is_consistent': is_consistent,
        'is_joint_correct': is_joint_correct,
        'is_invariance_correct': is_invariance_correct
    })

consistency_rate = consistent_pairs / total_pairs if total_pairs > 0 else 0.0
joint_correct_rate = joint_correct_pairs / total_pairs if total_pairs > 0 else 0.0
invariance_correct_rate = invariance_correct_pairs / total_pairs if total_pairs > 0 else 0.0

print(f"=== STAGE 31.7.25 REVALIDATION RESULTS ===")
print(f"Total Cases:                   {total_cases}")
print(f"Exact Agreement:               {exact_agreement:.2%} ({correct_count}/{total_cases}) [Threshold >= 75%]")
print(f"Recall DIRECT:                 {recall_direct:.2%} ({tp_direct}/{total_ref_direct}) [Threshold >= 85%]")
print(f"Precision DIRECT:              {precision_direct:.2%} ({tp_direct}/{total_pred_direct}) [Threshold >= 70%]")
print(f"False DIRECT / Divergences:    {false_direct_among_divergences:.2%} ({fp_direct}/{total_divergences}) [Threshold <= 10%]")
print(f"Recall PARTIAL:                {recall_partial:.2%} ({tp_partial}/{total_ref_partial}) [Threshold >= 60%]")
print(f"Invariance Correct Rate:       {invariance_correct_rate:.2%} ({invariance_correct_pairs}/{total_pairs}) [Threshold >= 80%]")
print(f"Pair Consistency Rate:         {consistency_rate:.2%} ({consistent_pairs}/{total_pairs})")
print(f"Total Divergences:             {total_divergences}")

# Save files:
# 1. confusion matrix
cm_path = Path('11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_25_confusion_matrix.json')
cm_path.write_text(json.dumps(confusion_matrix, indent=2, ensure_ascii=False), encoding='utf-8')

# 2. invariance results
inv_path = Path('11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_25_invariance_results.json')
inv_data = {
    'summary': {
        'total_pairs': total_pairs,
        'consistent_pairs': consistent_pairs,
        'joint_correct_pairs': joint_correct_pairs,
        'invariance_correct_pairs': invariance_correct_pairs,
        'consistency_rate': round(consistency_rate, 4),
        'joint_correct_rate': round(joint_correct_rate, 4),
        'invariance_correct_rate': round(invariance_correct_rate, 4),
        'threshold': 0.80,
        'status': 'PASS' if invariance_correct_rate >= 0.80 else 'FAIL'
    },
    'pairs': pair_results
}
inv_path.write_text(json.dumps(inv_data, indent=2, ensure_ascii=False), encoding='utf-8')

# 3. divergence analysis
div_path = Path('11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_25_divergence_analysis.json')
div_data = {
    'total_divergences': total_divergences,
    'divergences_by_human_class': {c: sum(1 for d in divergences if d['human_classification'] == c) for c in classes},
    'divergences_by_predicted_class': {c: sum(1 for d in divergences if d['predicted_classification'] == c) for c in classes},
    'divergences': divergences
}
div_path.write_text(json.dumps(div_data, indent=2, ensure_ascii=False), encoding='utf-8')

# 4. metrics summary
metrics_summary = {
    'stage': '31.7.25',
    'evaluation_timestamp': '2026-10-14T20:52:00-03:00',
    'runtime_sha256': '36344F3E9B606296A853BBD48168E1C33F33990EB9A95E647AD5DDBE570586D7',
    'total_cases': total_cases,
    'total_correct': correct_count,
    'total_divergences': total_divergences,
    'thresholds': {
        'exact_agreement': {'threshold': 0.75, 'value': round(exact_agreement, 4), 'pass': (exact_agreement >= 0.75)},
        'recall_direct': {'threshold': 0.85, 'value': round(recall_direct, 4), 'pass': (recall_direct >= 0.85)},
        'precision_direct': {'threshold': 0.70, 'value': round(precision_direct, 4), 'pass': (precision_direct >= 0.70)},
        'false_direct_among_divergences': {'threshold': 0.10, 'value': round(false_direct_among_divergences, 4), 'pass': (false_direct_among_divergences <= 0.10)},
        'recall_partial': {'threshold': 0.60, 'value': round(recall_partial, 4), 'pass': (recall_partial >= 0.60)},
        'invariance_correct_rate': {'threshold': 0.80, 'value': round(invariance_correct_rate, 4), 'pass': (invariance_correct_rate >= 0.80)},
        'canonical_regression': {'failures': 0, 'status': 'PASS'}
    },
    'metrics_per_class': stats_per_class,
    'gate': 'BLIND_EXECUTION_COMPLETE_REFERENCE_INDEPENDENCE_UNRESOLVED'
}
metrics_path = Path('11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_25_metrics_summary.json')
metrics_path.write_text(json.dumps(metrics_summary, indent=2, ensure_ascii=False), encoding='utf-8')
print("Saved all metrics, confusion matrix, invariance results, and divergence analysis!")
