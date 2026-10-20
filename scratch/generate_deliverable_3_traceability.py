import json
from pathlib import Path

pilot_dir = Path("11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05")
matrix_file = pilot_dir / "stage_31_7_31_contract_counterexample_matrix.json"
matrix_data = json.load(open(matrix_file, encoding="utf-8"))

traceability_records = []

for c in matrix_data["contracts"]:
    cid = c["contract_id"]
    scenario = c["scenario"]
    expected = c["expected_class"]
    
    # Map to increment and component
    if cid in ("SC-01", "SC-02", "SC-05", "SC-06", "SC-07", "SC-08", "SC-11", "SC-12"):
        inc = "INC-1"
        comp = "QuestionProfileExtractor / SufficiencyAssessmentEngine"
        test_case = f"tests.test_stage_31_7_34_increments::TestIncrement1::test_contract_{cid.replace('-', '_')}"
        evidence_field = "coverage_evaluation.coverage_ratio / demand_nexus_evaluations"
    elif cid in ("SC-17", "SC-18", "SC-20", "SC-21", "SC-22", "SC-32", "SC-33", "SC-34"):
        inc = "INC-2"
        comp = "DiscourseSegmentationEngine"
        test_case = f"tests.test_stage_31_7_34_increments::TestIncrement2::test_contract_{cid.replace('-', '_')}"
        evidence_field = "discourse_profile.propositions / discourse_profile.scopes"
    elif cid in ("SC-23-REV", "SC-29"):
        inc = "INC-3"
        comp = "ThematicAffinityEngine"
        test_case = f"tests.test_stage_31_7_34_increments::TestIncrement3::test_contract_{cid.replace('-', '_')}"
        evidence_field = "thematic_affinity_evaluation.presumption_status / is_alien"
    elif cid in ("SC-24-REV", "SC-25-REV", "SC-26-REV", "SC-27-REV", "SC-28-REV", "SC-30", "SC-31"):
        inc = "INC-4"
        comp = "ConceptualEquivalenceEngine / AnalogyResolutionEngine"
        test_case = f"tests.test_stage_31_7_34_increments::TestIncrement4::test_contract_{cid.replace('-', '_')}"
        evidence_field = "thematic_affinity_evaluation.equivalence_mode / analogy_evaluation"
    else: # SC-03, SC-04, SC-09, SC-10, SC-13, SC-14, SC-15, SC-16, SC-19, SC-35
        inc = "INC-5"
        comp = "StrictRelevanceAggregator"
        test_case = f"tests.test_stage_31_7_34_increments::TestIncrement5::test_contract_{cid.replace('-', '_')}"
        evidence_field = "final_decision.canonical_class / final_decision.decision_rule_id"

    traceability_records.append({
        "contract_id": cid,
        "scenario": scenario,
        "expected_class": expected,
        "responsible_increment": inc,
        "target_component": comp,
        "test_target": test_case,
        "required_evidence_node": evidence_field,
        "acceptance_criterion": f"Execução do teste confirma classe {expected} e registra evidência em {evidence_field} sem erros."
    })

doc = {
    "stage": "31.7.33",
    "title": "Stage 31.7.33 Contract to Component Traceability Matrix",
    "total_contracts_mapped": len(traceability_records),
    "traceability_matrix": traceability_records,
    "audit_declaration": "Mapeamento bidirecional estrito conectando cada um dos 35 contratos semânticos a seu incremento de implementação, componente de software, teste automatizado e nó de evidência no JSON de rastreabilidade."
}

with open(pilot_dir / "stage_31_7_33_contract_to_component_traceability.json", "w", encoding="utf-8") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)

print(f"Generated stage_31_7_33_contract_to_component_traceability.json with {len(traceability_records)} mapped contracts.")
