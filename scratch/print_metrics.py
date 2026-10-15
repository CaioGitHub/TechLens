import json

with open('11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_24_diagnostic_comparison.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

classes = ['DIRECT', 'PARTIAL', 'SUPPORTING', 'RELATED', 'OFF_TOPIC', 'INSUFFICIENT', 'UNKNOWN']
print(f"{'CLASS':<12} | {'SUP':>3} | {'OLD REC':>8} -> {'NEW REC':>8} | {'OLD PREC':>8} -> {'NEW PREC':>8} | {'OLD F1':>8} -> {'NEW F1':>8}")
print("-" * 80)
for c in classes:
    ob = d['per_class_metrics_baseline'][c]
    nb = d['per_class_metrics_remediated'][c]
    print(f"{c:<12} | {nb['support']:3} | {ob['recall']*100:7.2f}% -> {nb['recall']*100:7.2f}% | {ob['precision']*100:7.2f}% -> {nb['precision']*100:7.2f}% | {ob['f1']*100:7.2f}% -> {nb['f1']*100:7.2f}%")

print("\nIMPROVEMENTS BREAKDOWN:")
for imp in d['improvements']:
    print(f"[{imp['id']}] {imp['group']}: {imp['old']} -> {imp['new']} (ref: {imp['ref']})")
