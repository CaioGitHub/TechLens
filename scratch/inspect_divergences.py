import json

data = json.load(open('11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_28_divergence_analysis.json', encoding='utf-8'))
divs = data['divergent_cases']
print(f"Total divergences: {len(divs)}")

by_type = data['divergences_by_type']
for dt, cnt in sorted(by_type.items(), key=lambda x: -x[1]):
    print(f"  {dt:<25}: {cnt}")

print("\n--- Samples of OFF_TOPIC -> DIRECT ---")
off_to_direct = [d for d in divs if d['divergence_type'] == 'OFF_TOPIC -> DIRECT']
for d in off_to_direct[:10]:
    print(f"[{d['id']}] Q: {d['question_text']}")
    print(f"      R: {d['response_text']}")
    print(f"      RelType: {d['relation_type']}")
    print()

print("\n--- Samples of RELATED -> OFF_TOPIC ---")
rel_to_off = [d for d in divs if d['divergence_type'] == 'RELATED -> OFF_TOPIC']
for d in rel_to_off[:5]:
    print(f"[{d['id']}] Q: {d['question_text']}")
    print(f"      R: {d['response_text']}")
    print(f"      RelType: {d['relation_type']}")
    print()
