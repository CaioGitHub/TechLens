import json

p = "C:/Users/caiop/.gemini/antigravity-ide/brain/8baa1ac5-b48e-4706-9d0f-5c766d5d6bc4/scratch/"
gt = json.load(open(p + "stage_31_7_13_ground_truth.json", encoding="utf-8"))
group_o = [c for c in gt if c.get("group") == "O"]
for c in group_o:
    print(f"ID: {c['id']} | Ref: {c['human_classification']}")
    print(f"Q: {c['question_text']}")
    print(f"R: {c['response_text']}")
    print("-" * 60)
