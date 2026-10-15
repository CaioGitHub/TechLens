import json

divs = json.load(open('11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_25_divergence_analysis.json', encoding='utf-8'))

print(f"Total divergences: {len(divs['divergences'])}")

# Check sample OFF_TOPIC predicted as DIRECT
off_to_dir = [d for d in divs['divergences'] if d['human_classification'] == 'OFF_TOPIC' and d['predicted_classification'] == 'DIRECT']
print(f"\nOFF_TOPIC predicted as DIRECT: {len(off_to_dir)}")
for d in off_to_dir[:3]:
    print(f"[{d['id']}] Q: {d['question_text']}")
    print(f"  R: {d['response_text']}")
    print(f"  Pred Rel: {d['predicted_relation_type']}")
    print(f"  Rationale: {d['predicted_rationale']}")
    print("-" * 60)

# Check sample RELATED predicted as DIRECT
rel_to_dir = [d for d in divs['divergences'] if d['human_classification'] == 'RELATED' and d['predicted_classification'] == 'DIRECT']
print(f"\nRELATED predicted as DIRECT: {len(rel_to_dir)}")
for d in rel_to_dir[:3]:
    print(f"[{d['id']}] Q: {d['question_text']}")
    print(f"  R: {d['response_text']}")
    print(f"  Pred Rel: {d['predicted_relation_type']}")
    print(f"  Rationale: {d['predicted_rationale']}")
    print("-" * 60)

# Check sample INSUFFICIENT predicted as OFF_TOPIC or DIRECT
insuf_to_other = [d for d in divs['divergences'] if d['human_classification'] == 'INSUFFICIENT']
print(f"\nINSUFFICIENT divergences: {len(insuf_to_other)}")
for d in insuf_to_other[:3]:
    print(f"[{d['id']}] Q: {d['question_text']}")
    print(f"  R: {d['response_text']}")
    print(f"  Pred: {d['predicted_classification']} (Rel: {d['predicted_relation_type']})")
    print(f"  Rationale: {d['predicted_rationale']}")
    print("-" * 60)
