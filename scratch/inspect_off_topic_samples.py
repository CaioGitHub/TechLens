import json, sys, re
from pathlib import Path

sys.path.insert(0, '.')
from reference_runtime.runtime import OpenDomainPropositionEngine, _normalize_text

# Load the 250 cases from Stage 31.7.25
gt_p = Path('11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_25_ground_truth.json')
gt = json.loads(gt_p.read_text(encoding='utf-8'))
gt_map = {item['id']: item for item in gt}

pred_p = Path('11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_25_system_predictions.json')
preds = json.loads(pred_p.read_text(encoding='utf-8'))
pred_map = {item['id']: item for item in preds}

# Let's inspect the 34 OFF_TOPIC cases that became DIRECT in Stage 31.7.25
off_topic_cases = [gt_map[cid] for cid, item in pred_map.items() if item['predicted_classification'] == 'DIRECT' and gt_map[cid]['human_classification'] == 'OFF_TOPIC']
print(f"Total OFF_TOPIC -> DIRECT cases: {len(off_topic_cases)}")
for c in off_topic_cases[:5]:
    print("Q:", c['question_text'])
    print("R:", c['response_text'])
    print("-" * 50)
