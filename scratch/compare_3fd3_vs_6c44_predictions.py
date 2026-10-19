import json
import importlib.util
from pathlib import Path

# Load stage_31_7_27_pre_regression_fix (3FD3F80D...)
from importlib.machinery import SourceFileLoader
loader = SourceFileLoader('runtime_pre_fix', 'reference_runtime/runtime.py.stage_31_7_27_pre_regression_fix')
mod_pre_fix = loader.load_module()

pilot_dir = Path('11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05')
blind_data = json.load(open(pilot_dir / 'stage_31_7_28_blind_input.json', encoding='utf-8'))
sys_preds = json.load(open(pilot_dir / 'stage_31_7_28_system_predictions.json', encoding='utf-8'))
gt_data = json.load(open(pilot_dir / 'stage_31_7_28_ground_truth.json', encoding='utf-8'))

diffs = []
for c, p, gt in zip(blind_data['cases'], sys_preds['predictions'], gt_data['cases']):
    res_pre = mod_pre_fix.evaluate_open_domain_semantic_relevance(c['question_text'], c['response_text'])
    p_pre = res_pre['classification']
    p_actual = p['predicted_relevance']
    ref = gt['reference_relevance']
    if p_pre != p_actual:
        diffs.append({
            "id": c["id"],
            "ref": ref,
            "pred_3fd3": p_pre,
            "pred_6c44": p_actual,
            "question": c["question_text"][:60],
            "response": c["response_text"][:60]
        })

print(f"Total prediction differences between 3FD3F80D... and 6C44B7A8... on 250 cases: {len(diffs)}")
for d in diffs:
    print(f"[{d['id']}] Ref={d['ref']} | 3FD3={d['pred_3fd3']} | 6C44={d['pred_6c44']}")
    print(f"  Q: {d['question']}")
    print(f"  R: {d['response']}")
