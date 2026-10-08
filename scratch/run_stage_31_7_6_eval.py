"""
Stage 31.7.6 — Post-Generalization Blind Human vs System Revalidation Runner
Executes the blind validation strictly observing all firewall rules, determinism, isolation,
catalog leakage tests, representation invariance tests, and divergence categorization.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

# Workspace paths
WORKSPACE = Path(r"d:\Projetos\TechLens")
RUNTIME_PATH = WORKSPACE / "reference_runtime" / "runtime.py"
RAW_BENCHMARK_PATH = WORKSPACE / "scratch" / "stage_31_7_6_benchmark_raw.json"
OUTPUT_DIR = WORKSPACE / "11 - Interview Evaluation" / "09 - Real Interview Pilot" / "Candidato-Piloto-05"

EXPECTED_RUNTIME_HASH = "A0CFE48B933F587459BFF6AAF8B2BECABA5B7C00C4C87E7B5DDB6BDE985E46A6"

def verify_runtime_hash() -> str:
    content = RUNTIME_PATH.read_bytes()
    computed = hashlib.sha256(content).hexdigest().upper()
    if computed != EXPECTED_RUNTIME_HASH:
        raise RuntimeError(f"RUNTIME INTEGRITY VIOLATION! Expected {EXPECTED_RUNTIME_HASH}, got {computed}")
    return computed

def run_evaluation():
    print("=" * 70)
    print("STAGE 31.7.6 — POST-GENERALIZATION BLIND REVALIDATION RUNNER")
    print("=" * 70)

    # 1. Entry Hash Verification
    entry_hash = verify_runtime_hash()
    print(f"[OK] Entry Runtime Hash Verified: {entry_hash}")

    # Load Raw Benchmark
    with open(RAW_BENCHMARK_PATH, "r", encoding="utf-8") as f:
        benchmark_cases = json.load(f)
    print(f"[OK] Loaded {len(benchmark_cases)} benchmark cases from {RAW_BENCHMARK_PATH.name}")

    # 2. Blindness Firewall Separation
    blind_cases = []
    human_results = {}

    for c in benchmark_cases:
        cid = c["id"]
        blind_cases.append({
            "id": cid,
            "group": c["group"],
            "question": c["question"],
            "response": c["response"]
        })
        human_results[cid] = {
            "id": cid,
            "group": c["group"],
            "human_relation": c["human_relation"],
            "human_epistemic": c.get("human_epistemic", "conceptual"),
            "rationale": c.get("rationale", ""),
            "confidence": "HIGH"
        }

    # Persist Blind Cases & Human Results
    blind_cases_path = OUTPUT_DIR / "stage_31_7_6_blind_cases.json"
    human_results_path = OUTPUT_DIR / "stage_31_7_6_human_results.json"
    
    with open(blind_cases_path, "w", encoding="utf-8") as f:
        json.dump(blind_cases, f, indent=2, ensure_ascii=False)
    with open(human_results_path, "w", encoding="utf-8") as f:
        json.dump(human_results, f, indent=2, ensure_ascii=False)
    print(f"[OK] Persisted blind cases ({len(blind_cases)}) to {blind_cases_path.name}")
    print(f"[OK] Persisted human results ({len(human_results)}) to {human_results_path.name}")

    # Import Frozen Runtime
    if str(WORKSPACE) not in sys.path:
        sys.path.insert(0, str(WORKSPACE))
    import reference_runtime.runtime as runtime

    def execute_system(cases_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        results = {}
        for c in cases_list:
            cid = c["id"]
            q_dict = {"text": c["question"]}
            r_dict = {"reconstructed_text": c["response"]}
            rel = runtime._evaluate_semantic_relevance(q_dict, r_dict)
            specs = runtime._blind_evidence_specs(q_dict, r_dict)
            
            # Primary epistemic extraction from specs
            epistemic_types = [s.get("type") for s in specs] if specs else ["unknown"]
            primary_epistemic = epistemic_types[0] if epistemic_types else "unknown"

            results[cid] = {
                "id": cid,
                "group": c["group"],
                "system_relation": rel.get("classification"),
                "functional_contribution": rel.get("functional_contribution"),
                "relation_type": rel.get("relation_type"),
                "intent": rel.get("question_intent"),
                "system_epistemic": primary_epistemic,
                "all_epistemic_types": epistemic_types,
                "system_rationale": rel.get("rationale", ""),
                "confidence": rel.get("confidence", "MEDIUM")
            }
        return results

    # 3. System Evaluation Run A (Main Blind Run)
    print("\n--- Executing Run A (Main System Blind Run) ---")
    system_results_A = execute_system(blind_cases)
    system_results_path = OUTPUT_DIR / "stage_31_7_6_system_results.json"
    with open(system_results_path, "w", encoding="utf-8") as f:
        json.dump(system_results_A, f, indent=2, ensure_ascii=False)
    print(f"[OK] Run A complete. Persisted system results to {system_results_path.name}")

    # 4. Determinism Test (Run B vs Run A)
    print("\n--- Executing Run B (Determinism Test) ---")
    system_results_B = execute_system(blind_cases)
    dump_A = json.dumps(system_results_A, sort_keys=True)
    dump_B = json.dumps(system_results_B, sort_keys=True)
    determinism_pass = (dump_A == dump_B)
    print(f"[DETERMINISM TEST]: Match = {determinism_pass}")
    if not determinism_pass:
        print("[FAIL] Determinism check failed! Outputs differ between identical runs.")

    # 5. Isolation Test (Reverse order & Individual order)
    print("\n--- Executing Isolation Tests ---")
    # Reverse order run
    reverse_cases = list(reversed(blind_cases))
    system_results_rev = execute_system(reverse_cases)
    isolation_rev_pass = all(system_results_rev[cid]["system_relation"] == system_results_A[cid]["system_relation"] for cid in system_results_A)
    print(f"[ISOLATION TEST - Reverse Order]: Match = {isolation_rev_pass}")

    # 6. Catalog Leakage Test (State A vs State B: Empty _FUNCTIONAL_CAPABILITIES)
    print("\n--- Executing Catalog Leakage Test (State A vs State B) ---")
    orig_capabilities = copy.deepcopy(runtime._FUNCTIONAL_CAPABILITIES)
    try:
        runtime._FUNCTIONAL_CAPABILITIES.clear()
        system_results_empty_catalog = execute_system(blind_cases)
    finally:
        runtime._FUNCTIONAL_CAPABILITIES.update(orig_capabilities)

    catalog_leak_diffs = []
    for cid in system_results_A:
        rel_A = system_results_A[cid]["system_relation"]
        rel_B = system_results_empty_catalog[cid]["system_relation"]
        if rel_A != rel_B:
            catalog_leak_diffs.append({
                "id": cid,
                "group": system_results_A[cid]["group"],
                "state_A_relation": rel_A,
                "state_B_relation": rel_B
            })
    catalog_leak_pass = (len(catalog_leak_diffs) == 0)
    print(f"[CATALOG LEAKAGE TEST]: Invariance = {catalog_leak_pass} (Differences: {len(catalog_leak_diffs)})")
    if catalog_leak_diffs:
        print(f"Sample catalog diff: {catalog_leak_diffs[:3]}")

    # 7. Comparison and Metrics Calculation
    print("\n--- Performing Comparison & Divergence Analysis ---")
    comparisons = []
    divergences = []

    group_stats = {}
    confusion_matrix = {}
    relation_types = ["DIRECT", "SUPPORTING", "RELATED", "OFF_TOPIC", "PARTIAL", "INSUFFICIENT", "UNKNOWN"]
    for h in relation_types:
        confusion_matrix[h] = {s: 0 for s in relation_types}

    false_directs = []
    false_off_topics = []
    false_relateds = []
    false_supportings = []
    false_partials = []

    for c in blind_cases:
        cid = c["id"]
        grp = c["group"]
        h_eval = human_results[cid]
        s_eval = system_results_A[cid]

        h_rel = h_eval["human_relation"]
        s_rel = s_eval["system_relation"]

        # Confusion Matrix
        if h_rel in confusion_matrix and s_rel in confusion_matrix[h_rel]:
            confusion_matrix[h_rel][s_rel] += 1

        is_match = (h_rel == s_rel)

        if grp not in group_stats:
            group_stats[grp] = {"total": 0, "matches": 0, "divergences": 0}
        group_stats[grp]["total"] += 1
        if is_match:
            group_stats[grp]["matches"] += 1
        else:
            group_stats[grp]["divergences"] += 1

        comp_entry = {
            "id": cid,
            "group": grp,
            "question": c["question"],
            "response": c["response"],
            "human_relation": h_rel,
            "system_relation": s_rel,
            "match": is_match,
            "human_epistemic": h_eval["human_epistemic"],
            "system_epistemic": s_eval["system_epistemic"],
            "system_functional_contribution": s_eval["functional_contribution"],
            "human_rationale": h_eval["rationale"],
            "system_rationale": s_eval["system_rationale"]
        }
        comparisons.append(comp_entry)

        if not is_match:
            # Classify divergence per Section 19 taxonomy:
            div_category = "D10_other"
            if grp == "D_entity_anchor" and s_rel in ("DIRECT", "SUPPORTING") and h_rel not in ("DIRECT", "SUPPORTING"):
                div_category = "D3_entity_anchor_error"
                false_directs.append(cid)
            elif grp == "F_multi_aspect":
                div_category = "D5_multi_aspect_error"
                if s_rel == "DIRECT":
                    false_directs.append(cid)
                elif s_rel == "OFF_TOPIC":
                    false_off_topics.append(cid)
                else:
                    false_partials.append(cid)
            elif grp == "I_generic_tokens":
                div_category = "D4_lexical_dependency"
                if s_rel == "DIRECT":
                    false_directs.append(cid)
                elif s_rel == "OFF_TOPIC":
                    false_off_topics.append(cid)
            elif grp == "G_epistemology":
                div_category = "D7_epistemic_confusion"
                if s_rel == "DIRECT":
                    false_directs.append(cid)
                elif s_rel == "OFF_TOPIC":
                    false_off_topics.append(cid)
            elif grp == "K_unknown_insufficient":
                div_category = "D9_unknown_misuse"
                if s_rel == "OFF_TOPIC":
                    false_off_topics.append(cid)
            elif (s_rel == "RELATED" and h_rel == "SUPPORTING") or (s_rel == "SUPPORTING" and h_rel == "RELATED"):
                div_category = "D6_supporting_related_confusion"
                if s_rel == "RELATED":
                    false_relateds.append(cid)
                else:
                    false_supportings.append(cid)
            elif s_rel == "DIRECT" and h_rel != "DIRECT":
                div_category = "D1_semantic_false_positive"
                false_directs.append(cid)
            elif s_rel == "OFF_TOPIC" and h_rel in ("DIRECT", "SUPPORTING", "PARTIAL"):
                div_category = "D2_semantic_false_negative"
                false_off_topics.append(cid)
            elif grp == "H_representation_invariance":
                div_category = "D8_representation_invariance_failure"
                if s_rel == "OFF_TOPIC":
                    false_off_topics.append(cid)
                elif s_rel == "DIRECT":
                    false_directs.append(cid)

            divergences.append({
                "case_id": cid,
                "group": grp,
                "category": div_category,
                "human_relation": h_rel,
                "system_relation": s_rel,
                "question": c["question"],
                "response": c["response"],
                "observed_behavior": f"System returned {s_rel} while Human expected {h_rel}",
                "human_rationale": h_eval["rationale"],
                "system_rationale": s_eval["system_rationale"]
            })

    total_cases = len(blind_cases)
    total_matches = sum(1 for c in comparisons if c["match"])
    total_divergences = len(divergences)
    agreement_rate = (total_matches / total_cases) * 100 if total_cases > 0 else 0

    print(f"Total Cases: {total_cases}")
    print(f"Total Matches: {total_matches}")
    print(f"Total Divergences: {total_divergences}")
    print(f"Agreement Rate: {agreement_rate:.2f}%")
    print(f"False DIRECTs: {len(false_directs)}")
    print(f"False OFF_TOPICs: {len(false_off_topics)}")
    print(f"False RELATEDs: {len(false_relateds)}")
    print(f"False SUPPORTINGs: {len(false_supportings)}")
    print(f"False PARTIALs: {len(false_partials)}")

    print("\n--- Group Breakdown ---")
    for grp, s in sorted(group_stats.items()):
        grp_pct = (s["matches"] / s["total"]) * 100 if s["total"] > 0 else 0
        print(f"  {grp:25s}: {s['matches']:2d}/{s['total']:2d} ({grp_pct:5.1f}%) | Divs: {s['divergences']}")

    # 8. Representation Invariance Analysis (Group H)
    pair_groups = {}
    for c in blind_cases:
        if c["group"] == "H_representation_invariance":
            pid = next((b.get("pair_id") for b in benchmark_cases if b["id"] == c["id"]), None)
            if pid:
                if pid not in pair_groups:
                    pair_groups[pid] = []
                pair_groups[pid].append(c["id"])
    
    rep_inv_pairs = len(pair_groups)
    rep_inv_matches = 0
    rep_inv_details = []
    for pid, cids in pair_groups.items():
        if len(cids) == 2:
            rel_a = system_results_A[cids[0]]["system_relation"]
            rel_b = system_results_A[cids[1]]["system_relation"]
            pair_match = (rel_a == rel_b)
            if pair_match:
                rep_inv_matches += 1
            rep_inv_details.append({
                "pair_id": pid,
                "case_a": cids[0],
                "case_b": cids[1],
                "relation_a": rel_a,
                "relation_b": rel_b,
                "invariant": pair_match
            })
    rep_inv_pct = (rep_inv_matches / rep_inv_pairs * 100) if rep_inv_pairs > 0 else 0
    print(f"\n[REPRESENTATION INVARIANCE (Group H)]: {rep_inv_matches}/{rep_inv_pairs} ({rep_inv_pct:.1f}%)")

    # 9. Secret Lexical-Free Subset Analysis (Group C)
    group_c_cases = [c for c in comparisons if c["group"] == "C_zero_lexical_overlap"]
    c_matches = sum(1 for c in group_c_cases if c["match"])
    c_total = len(group_c_cases)
    c_pct = (c_matches / c_total * 100) if c_total > 0 else 0
    print(f"\n[SECRET LEXICAL-FREE SUBSET (Group C)]: {c_matches}/{c_total} ({c_pct:.1f}%)")

    # 10. Mutation Sensitivity Analysis (Group L)
    group_l_cases = [c for c in comparisons if c["group"] == "L_mutations"]
    l_matches = sum(1 for c in group_l_cases if c["match"])
    l_total = len(group_l_cases)
    l_pct = (l_matches / l_total * 100) if l_total > 0 else 0
    print(f"\n[MUTATION TESTS (Group L)]: {l_matches}/{l_total} ({l_pct:.1f}%)")

    # Divergence Categorization Counts
    div_cats = {}
    for d in divergences:
        cat = d["category"]
        div_cats[cat] = div_cats.get(cat, 0) + 1
    print("\n--- Divergence Categories ---")
    for cat, cnt in sorted(div_cats.items()):
        print(f"  {cat:32s}: {cnt}")

    # Persist Comparison and Divergences
    comparison_path = OUTPUT_DIR / "stage_31_7_6_comparison.json"
    divergences_path = OUTPUT_DIR / "stage_31_7_6_divergences.json"

    comparison_payload = {
        "metadata": {
            "stage": "31.7.6",
            "runtime_hash": entry_hash,
            "total_cases": total_cases,
            "total_matches": total_matches,
            "total_divergences": total_divergences,
            "agreement_rate_pct": round(agreement_rate, 2),
            "determinism_pass": determinism_pass,
            "isolation_pass": isolation_rev_pass,
            "catalog_leak_pass": catalog_leak_pass,
            "representation_invariance_score": f"{rep_inv_matches}/{rep_inv_pairs}",
            "secret_lexical_free_score": f"{c_matches}/{c_total}",
            "mutation_score": f"{l_matches}/{l_total}"
        },
        "group_stats": group_stats,
        "confusion_matrix": confusion_matrix,
        "divergence_categories": div_cats,
        "comparisons": comparisons
    }

    with open(comparison_path, "w", encoding="utf-8") as f:
        json.dump(comparison_payload, f, indent=2, ensure_ascii=False)
    with open(divergences_path, "w", encoding="utf-8") as f:
        json.dump(divergences, f, indent=2, ensure_ascii=False)

    print(f"\n[OK] Persisted comparison to {comparison_path.name}")
    print(f"[OK] Persisted divergences ({len(divergences)}) to {divergences_path.name}")

    # Verify Exit Runtime Hash
    exit_hash = verify_runtime_hash()
    print(f"[OK] Exit Runtime Hash Verified: {exit_hash} (unchanged: {entry_hash == exit_hash})")

if __name__ == "__main__":
    run_evaluation()
