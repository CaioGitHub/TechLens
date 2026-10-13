"""
Check remaining FP DIRECTs by reference class
"""
import json
import sys
sys.path.insert(0, ".")
from scratch.test_remediation_prototype import RemediatedPropositionEngine

engine = RemediatedPropositionEngine()
with open("11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_17_ground_truth.json", encoding="utf-8") as f:
    gt_data = json.load(f)

for item in gt_data:
    cid = item["id"]
    q = item["question_text"]
    r = item["response_text"]
    ref = item["human_classification"]

    res = engine.evaluate(q, r)
    pred = res["classification"]
    if pred == "DIRECT" and ref != "DIRECT":
        print(f"[{cid}] Ref: {ref} -> Pred: {pred}")
        print(f"  Q: {q}")
        print(f"  R: {r}")
        print(f"  Nexus: {res['demand_nexus']}")
        print()
