import json
import re

p_hist = "C:/Users/caiop/.gemini/antigravity-ide/brain/8baa1ac5-b48e-4706-9d0f-5c766d5d6bc4/scratch/stage_31_7_13_ground_truth.json"
hist_data = json.load(open(p_hist, encoding="utf-8"))
hist_q = {c["question_text"].strip().lower(): c["id"] for c in hist_data}
hist_r = {c["response_text"].strip().lower(): c["id"] for c in hist_data}

with open("scratch/build_stage_31_7_17_dataset.py", encoding="utf-8") as f:
    content = f.read()

# Replace the asserts with warning prints so we see all collisions
modified = content.replace(
    'assert q_norm not in hist_questions, f"Duplicate question in historical benchmark: {q}"',
    'if q_norm in hist_questions: print(f"DUP Q [{cid}]: {q}")'
).replace(
    'assert r_norm not in hist_responses, f"Duplicate response in historical benchmark: {r}"',
    'if r_norm in hist_responses: print(f"DUP R [{cid}]: {r}")'
)

# Execute in isolated namespace
ns = {}
exec(modified, ns)
print(f"Total cases collected: {len(ns.get('cases', []))}")
