"""
Deep dive into the 76 divergences of Stage 31.7.17.
Categorizes root causes:
1. PARTIAL promoted to DIRECT (14 cases)
2. RELATED promoted to DIRECT (15 cases)
3. OFF_TOPIC promoted to DIRECT (7 cases - antitrust/orthogonal)
4. UNKNOWN / Tautologies promoted to DIRECT/OFF_TOPIC/RELATED (12 cases)
5. INSUFFICIENT classified as UNKNOWN/OFF_TOPIC/DIRECT (9 cases)
6. DIRECT demoted to OFF_TOPIC/SUPPORTING/RELATED (5 cases)
7. PARTIAL demoted to OFF_TOPIC (5 cases)
"""

import json
from collections import defaultdict

data = json.load(open("scratch/stage_31_7_17_metrics_summary.json", encoding="utf-8"))
divs = data["divergences"]

print(f"Total Divergences: {len(divs)}")

patterns = defaultdict(list)

for d in divs:
    transition = f"{d['reference_classification']} -> {d['predicted_classification']}"
    patterns[transition].append(d)

for trans, items in sorted(patterns.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"\n=== Transition: {trans} ({len(items)} cases) ===")
    for item in items[:5]:
        print(f"  [{item['id']}] Q: {item['question_text'][:60]}...")
        print(f"     R: {item['response_text'][:70]}...")
        print(f"     Demands: {item['demands']}")
        print(f"     Satisfied: {item['satisfied_aspects']}")
        print(f"     Reason: {item['predicted_reason']}")
        print()
    if len(items) > 5:
        print(f"     ... and {len(items)-5} more cases")
