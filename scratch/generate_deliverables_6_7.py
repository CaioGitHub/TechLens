import json
from pathlib import Path

pilot_dir = Path("11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05")
div_file = pilot_dir / "stage_31_7_28_divergence_analysis.json"
gt_file = pilot_dir / "stage_31_7_28_ground_truth.json"
pred_file = pilot_dir / "stage_31_7_28_system_predictions.json"

div_data = json.load(open(div_file, encoding="utf-8"))
gt_data = json.load(open(gt_file, encoding="utf-8"))
pred_data = json.load(open(pred_file, encoding="utf-8"))

gt_cases = {c["id"]: c for c in gt_data["cases"]}
preds = {p["id"]: p for p in pred_data["predictions"]}

# 1. Audit False DIRECT cases (34 total: 26 OFF_TOPIC, 5 RELATED, 1 PARTIAL, 1 INSUFFICIENT, 1 UNKNOWN)
false_direct_cases = []
for d in div_data["divergent_cases"]:
    if d["predicted_relevance"] == "DIRECT":
        cid = d["id"]
        gt = gt_cases[cid]
        p = preds[cid]
        
        # Determine failure cause
        ref = d["reference_relevance"]
        if ref == "OFF_TOPIC":
            failure_cause = "BRITTLE_REGEX_DISJUNCTION_BYPASS: Alien domain vocabulary (crafts, construction, horticulture) was not matched by closed regex clusters in SemanticDomainDisjunctionEngine. Transitive action verbs led PropositionDiscourseFilter to mark is_operative=True, and open-domain fallback promoted to DIRECT."
        elif ref == "RELATED":
            failure_cause = "METADATA_WITH_ACTIVE_SYNTAX: Thematic metadata sentence contained compound technical verbs that bypassed non-operative filter and matched functional fallback."
        elif ref == "PARTIAL":
            failure_cause = "PARTIAL_UNDETECTED: Second mandatory demand was not flagged as unmet due to stem matching overlap."
        elif ref == "INSUFFICIENT":
            failure_cause = "CONVERSATIONAL_FILLER_FALLBACK: Conversational acknowledgment with technical nouns was treated as active proposition."
        elif ref == "UNKNOWN":
            failure_cause = "TAUTOLOGY_FALLBACK: Circular repetition with active verbs was treated as functional explanation."
        else:
            failure_cause = "OTHER_PROMOTION_FAILURE"
            
        false_direct_cases.append({
            "id": cid,
            "reference_relevance": ref,
            "predicted_relevance": "DIRECT",
            "semantic_family": d["semantic_family"],
            "question_text": d["question_text"],
            "response_text": d["response_text"],
            "system_relation_type": d["relation_type"],
            "system_rationale": d["system_rationale"],
            "ground_truth_rationale": d["reference_rationale"],
            "failure_mechanism": failure_cause,
            "pipeline_stage_of_failure": "SemanticDomainDisjunctionEngine -> DemandPropositionNexusBipartiteMatcher"
        })

output_fd = {
    "stage": "31.7.29",
    "audit_name": "Stage 31.7.29 False DIRECT Cases Forensic Audit",
    "total_false_directs": len(false_direct_cases),
    "breakdown_by_reference": {
        "OFF_TOPIC": sum(1 for c in false_direct_cases if c["reference_relevance"] == "OFF_TOPIC"),
        "RELATED": sum(1 for c in false_direct_cases if c["reference_relevance"] == "RELATED"),
        "PARTIAL": sum(1 for c in false_direct_cases if c["reference_relevance"] == "PARTIAL"),
        "INSUFFICIENT": sum(1 for c in false_direct_cases if c["reference_relevance"] == "INSUFFICIENT"),
        "UNKNOWN": sum(1 for c in false_direct_cases if c["reference_relevance"] == "UNKNOWN")
    },
    "cases": false_direct_cases
}

with open(pilot_dir / "stage_31_7_29_false_direct_case_audit.json", "w", encoding="utf-8") as f:
    json.dump(output_fd, f, indent=2, ensure_ascii=False)

# 2. Audit RELATED -> OFF_TOPIC cases (22 cases)
related_off_topic_cases = []
for d in div_data["divergent_cases"]:
    if d["reference_relevance"] == "RELATED" and d["predicted_relevance"] == "OFF_TOPIC":
        cid = d["id"]
        gt = gt_cases[cid]
        p = preds[cid]
        related_off_topic_cases.append({
            "id": cid,
            "reference_relevance": "RELATED",
            "predicted_relevance": "OFF_TOPIC",
            "semantic_family": d["semantic_family"],
            "question_text": d["question_text"],
            "response_text": d["response_text"],
            "system_relation_type": d["relation_type"],
            "system_rationale": d["system_rationale"],
            "ground_truth_rationale": d["reference_rationale"],
            "failure_mechanism": "NON_OPERATIVE_AGGREGATOR_SINK: Institutional or historical software metadata lacked operative action verbs (is_operative=False). Institutional regex in SemanticDomainDisjunctionEngine was brittle (e.g. required 'categoria de soluções' instead of 'categoria de ferramentas'). Fallback emitted NON_OPERATIVE nexus, which StrictOntologyRelevanceAggregator unconditionally dumped into OFF_TOPIC.",
            "pipeline_stage_of_failure": "SemanticDomainDisjunctionEngine (regex miss) -> StrictOntologyRelevanceAggregator (NON_OPERATIVE -> OFF_TOPIC)"
        })

output_rot = {
    "stage": "31.7.29",
    "audit_name": "Stage 31.7.29 RELATED -> OFF_TOPIC Cases Forensic Audit",
    "total_related_to_off_topic": len(related_off_topic_cases),
    "cases": related_off_topic_cases
}

with open(pilot_dir / "stage_31_7_29_related_off_topic_audit.json", "w", encoding="utf-8") as f:
    json.dump(output_rot, f, indent=2, ensure_ascii=False)

print(f"Generated false_direct_case_audit.json ({len(false_direct_cases)} cases)")
print(f"Generated related_off_topic_audit.json ({len(related_off_topic_cases)} cases)")
