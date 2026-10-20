import json
import re
from reference_runtime.runtime import (
    VALID_INTENT_MODES,
    VALID_DISCOURSE_ROLES,
    VALID_THEMATIC_STATUSES,
    VALID_REBUTTAL_REASONS,
    VALID_NEXUS_RELATIONS,
    VALID_CONFIDENCE_LEVELS,
    VALID_CLASSIFICATIONS,
    validate_evidence_traceability_record,
    DemandSpecification,
    QuestionProfile,
    DiscourseProposition,
    DiscourseProfile,
    ThematicAffinityEvaluation,
    DemandNexusEvaluation,
    CoverageEvaluation,
    EpistemicUncertaintyRecord,
    FinalDecisionRecord,
    EvidenceTraceabilityRecord,
)

schema_path = '11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_34_evidence_traceability_schema.json'
with open(schema_path, 'r', encoding='utf-8') as f:
    schema = json.load(f)

print("1. JSON Syntax: OK")
print(f"2. $schema declaration: {schema.get('$schema')}")
print(f"3. Root type: {schema.get('type')}")
print(f"4. Title: {schema.get('title')}")

# Check enums alignment between runtime and schema
schema_enums = {
    "intent_mode": set(schema['properties']['question_profile']['properties']['intent_mode']['enum']),
    "discourse_role": set(schema['properties']['discourse_profile']['properties']['propositions']['items']['properties']['discourse_role']['enum']),
    "thematic_presumption_status": set(schema['properties']['thematic_affinity_evaluation']['properties']['thematic_presumption_status']['enum']),
    "rebuttal_reason": set(schema['properties']['thematic_affinity_evaluation']['properties']['rebuttal_reason']['enum']),
    "nexus_relation": set(schema['properties']['demand_nexus_evaluations']['items']['properties']['nexus_relation']['enum']),
    "confidence_level": set(schema['properties']['epistemic_uncertainty']['properties']['confidence_level']['enum']),
    "classification": set(schema['properties']['final_decision']['properties']['classification']['enum']),
}

runtime_enums = {
    "intent_mode": VALID_INTENT_MODES,
    "discourse_role": VALID_DISCOURSE_ROLES,
    "thematic_presumption_status": VALID_THEMATIC_STATUSES,
    "rebuttal_reason": VALID_REBUTTAL_REASONS,
    "nexus_relation": VALID_NEXUS_RELATIONS,
    "confidence_level": VALID_CONFIDENCE_LEVELS,
    "classification": VALID_CLASSIFICATIONS,
}

print("\n--- Enum Alignment Audit ---")
all_enums_match = True
for name in schema_enums:
    s_set = schema_enums[name]
    r_set = runtime_enums[name]
    match = (s_set == r_set)
    if not match:
        all_enums_match = False
        print(f"MISMATCH in {name}: schema - runtime = {s_set - r_set}, runtime - schema = {r_set - s_set}")
    else:
        print(f"MATCH: {name} ({len(s_set)} items)")

print(f"All enums match perfectly: {all_enums_match}")

# Check Draft-07 structural requirements
print("\n--- Draft-07 Metaschema Structural Checks ---")
# Check required properties lists
def check_required_lists(d, path="root"):
    issues = []
    if isinstance(d, dict):
        if "required" in d:
            if not isinstance(d["required"], list):
                issues.append(f"{path}.required is not an array")
            else:
                for item in d["required"]:
                    if not isinstance(item, str):
                        issues.append(f"{path}.required contains non-string: {item}")
                    if "properties" in d and item not in d["properties"]:
                        issues.append(f"{path}.required property '{item}' not in properties")
        if "properties" in d:
            for k, v in d["properties"].items():
                issues.extend(check_required_lists(v, f"{path}.properties.{k}"))
        if "items" in d:
            issues.extend(check_required_lists(d["items"], f"{path}.items"))
    return issues

issues = check_required_lists(schema)
print(f"Required lists structural issues: {len(issues)}")
for iss in issues:
    print(f"  Issue: {iss}")

# Check FINDING-06 in schema
final_dec_props = schema['properties']['final_decision']['properties']
has_applied_contract_ids = 'applied_contract_ids' in final_dec_props
print(f"FINDING-06 applied_contract_ids present in schema: {has_applied_contract_ids}")
if has_applied_contract_ids:
    ac_prop = final_dec_props['applied_contract_ids']
    print(f"  Type: {ac_prop.get('type')}, items: {ac_prop.get('items')}")
