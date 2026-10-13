import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from reference_runtime.runtime import OpenDomainPropositionEngine

engine = OpenDomainPropositionEngine()

p_gt = "11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_17_ground_truth.json"
gt_cases = {c["id"]: c for c in json.load(open(p_gt, encoding="utf-8"))}

def trace_case(cid):
    c = gt_cases[cid]
    q = c["question_text"]
    r = c["response_text"]
    ref = c["human_classification"]
    
    intent, demands = engine.decompose_question(q)
    props = engine.extract_response_propositions(r, q)
    prop = props[0]
    
    nexus_records = []
    for d in demands:
        nx = engine.assess_demand_nexus(d, prop, intent.central_entities[0] if intent.central_entities else "")
        nexus_records.append(nx)
        
    res = engine.evaluate_relevance(q, r)
    
    print(f"=== CASE {cid} ===")
    print(f"Q: {q}")
    print(f"R: {r}")
    print(f"Ref: {ref} | Pred: {res['classification']}")
    print(f"Intent Type: {intent.intent_type} | Central: {intent.central_entities}")
    print(f"Demands ({len(demands)}): {[d.target_problem for d in demands]}")
    print(f"Prop flags: is_op={prop.is_operative}, is_alien={prop.is_alien_domain}, is_anti={prop.is_antithesis}, is_triv={prop.is_trivia}, is_evas={prop.is_evasive}")
    print(f"Nexus records: {[(nx.demand_id, nx.nexus_relation, nx.rationale) for nx in nexus_records]}")
    print(f"Final Decision: {res['classification']} (type: {res['relation_type']})")
    print()

# Test sample across RCA categories:
print("--- RCA-02: RELATED -> DIRECT ---")
trace_case("R01_milvus_hnsw_description")
trace_case("R02_clickhouse_columnar_description")
trace_case("R04_sqlite_awards_history")

print("--- RCA-01: PARTIAL -> DIRECT ---")
trace_case("P09_compare_protobuf_json_omit_cpu")
trace_case("P10_compare_modular_monolith_microservices_omit_sagas")
trace_case("P23_compare_dynamo_spanner_omit_stale")

print("--- RCA-03: UNKNOWN -> DIRECT / OFF_TOPIC ---")
trace_case("U01_tautology_fast_is_quick")
trace_case("U02_tautology_locks_block")
trace_case("U04_tautology_cache_stores")

print("--- RCA-04: OFF_TOPIC -> DIRECT ---")
trace_case("O02_antithesis_drop_locks_inflected")
trace_case("O05_antithesis_grant_full_admin_no_auth")
trace_case("O07_antithesis_disable_rate_limiting")

print("--- RCA-06: INSUFFICIENT -> DIRECT ---")
trace_case("I11_evasive_depends_on_budget")
trace_case("I12_evasive_senior_consultant")
