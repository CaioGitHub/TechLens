import json
import sys
sys.path.insert(0, ".")
from scratch.test_stage_31_7_16_prototype import EnhancedPropositionEngine

p = "C:/Users/caiop/.gemini/antigravity-ide/brain/8baa1ac5-b48e-4706-9d0f-5c766d5d6bc4/scratch/"
gt = json.load(open(p + "stage_31_7_13_ground_truth.json", encoding="utf-8"))
eng = EnhancedPropositionEngine()

misclassified = []
for c in gt:
    res = eng.evaluate(c["question_text"], c["response_text"])
    pred = res["classification"]
    ref = c["human_classification"]
    if ref != "DIRECT" and pred == "DIRECT":
        misclassified.append((ref, c["id"], c["question_text"], c["response_text"]))

print(f"Total False DIRECT: {len(misclassified)}")
from collections import Counter
counts = Counter([m[0] for m in misclassified])
print("Breakdown by ref:", counts)
print("\n--- Samples from each category ---")
for ref_cat in ["OFF_TOPIC", "RELATED", "SUPPORTING", "PARTIAL", "UNKNOWN"]:
    samples = [m for m in misclassified if m[0] == ref_cat]
    print(f"\n[{ref_cat}] (total {len(samples)}):")
    for s in samples[:5]:
        print(f"ID: {s[1]}")
        print(f"  Q: {s[2]}")
        print(f"  R: {s[3]}")
