"""
Evaluate remediated reference_runtime.runtime directly against stage_31_7_17_ground_truth.json
"""

import json
import sys
sys.path.insert(0, ".")
from reference_runtime.runtime import evaluate_open_domain_semantic_relevance

def run_evaluation():
    with open("11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_17_ground_truth.json", encoding="utf-8") as f:
        gt_data = json.load(f)

    classes = ["DIRECT", "PARTIAL", "SUPPORTING", "RELATED", "OFF_TOPIC", "INSUFFICIENT", "UNKNOWN"]
    conf_matrix = {r: {p: 0 for p in classes} for r in classes}

    exact_matches = 0
    total = len(gt_data)

    direct_tp = 0
    direct_fp = 0
    direct_fn = 0
    partial_tp = 0
    partial_fn = 0
    divergence_count = 0
    false_direct_count = 0

    # For invariance tracking (Group I cases)
    invariance_cases = {}

    for item in gt_data:
        cid = item["id"]
        q = item["question_text"]
        r = item["response_text"]
        ref = item["human_classification"]

        res = evaluate_open_domain_semantic_relevance(q, r)
        pred = res["classification"]

        conf_matrix[ref][pred] += 1
        if pred == ref:
            exact_matches += 1
        else:
            divergence_count += 1
            if pred == "DIRECT":
                false_direct_count += 1

        if ref == "DIRECT":
            if pred == "DIRECT":
                direct_tp += 1
            else:
                direct_fn += 1
        else:
            if pred == "DIRECT":
                direct_fp += 1

        if ref == "PARTIAL":
            if pred == "PARTIAL":
                partial_tp += 1
            else:
                partial_fn += 1

    # Canonical 13 invariance pairs from Stage 31.7.17 benchmark
    invariance_pairs = [
        ("D01_vector_hnsw", "D02_vector_hnsw_informal"),
        ("D03_compaction_lsm", "D04_compaction_lsm_active"),
        ("D05_raft_log_matching", "D06_raft_log_matching_short"),
        ("D07_distributed_lock_fencing", "D08_distributed_lock_fencing_informal"),
        ("D09_kafka_zero_copy", "D10_kafka_zero_copy_active"),
        ("D11_crdt_pn_counter", "D12_crdt_pn_counter_informal"),
        ("D13_database_sharding_virtual_nodes", "D14_database_sharding_virtual_nodes_active"),
        ("D15_outbox_debezium_cdc", "D16_outbox_debezium_cdc_informal"),
        ("D17_saga_choreography_compensating", "D18_saga_choreography_compensating_short"),
        ("D43_long_direct_detailed", "D44_short_direct_concise"),
        ("P05_explicit_omission_text", "P06_explicit_omission_text_informal"),
        ("P11_multi_aspect_idempotency_storage", "P12_multi_aspect_idempotency_storage_informal"),
        ("O01_antithesis_drop_locks", "O02_antithesis_drop_locks_inflected"),
    ]
    preds_by_id = {item["id"]: evaluate_open_domain_semantic_relevance(item["question_text"], item["response_text"])["classification"] for item in gt_data}
    inv_stable_pairs = sum(1 for a, b in invariance_pairs if preds_by_id[a] == preds_by_id[b])
    inv_total_pairs = len(invariance_pairs)
    inv_rate = (inv_stable_pairs / inv_total_pairs) * 100

    exact_acc = (exact_matches / total) * 100
    direct_recall = (direct_tp / (direct_tp + direct_fn)) * 100 if (direct_tp + direct_fn) > 0 else 0
    direct_prec = (direct_tp / (direct_tp + direct_fp)) * 100 if (direct_tp + direct_fp) > 0 else 0
    partial_recall = (partial_tp / (partial_tp + partial_fn)) * 100 if (partial_tp + partial_fn) > 0 else 0
    false_direct_rate = (false_direct_count / divergence_count) * 100 if divergence_count > 0 else 0

    print("=" * 70)
    print("STAGE 31.7.20 — REMEDIATED RUNTIME DIAGNOSTIC BENCHMARK EVALUATION")
    print("=" * 70)
    print(f"Total Cases: {total}")
    print(f"Exact Agreement: {exact_matches}/{total} ({exact_acc:.2f}%) [Threshold: >= 75%]")
    print(f"DIRECT Recall: {direct_tp}/{direct_tp + direct_fn} ({direct_recall:.2f}%) [Threshold: >= 85%]")
    print(f"DIRECT Precision: {direct_tp}/{direct_tp + direct_fp} ({direct_prec:.2f}%) [Threshold: >= 70%]")
    print(f"False DIRECTs among Divergences: {false_direct_count}/{divergence_count} ({false_direct_rate:.2f}%) [Threshold: <= 10%]")
    print(f"PARTIAL Recall: {partial_tp}/{partial_tp + partial_fn} ({partial_recall:.2f}%) [Threshold: >= 60%]")
    print(f"Representation Invariance: {inv_stable_pairs}/{inv_total_pairs} ({inv_rate:.2f}%) [Threshold: >= 80%]")
    print("\nConfusion Matrix (Rows=Human Ref, Columns=Remediated Runtime):")
    header = f"{'Ref \\ Pred':<14}" + "".join(f"{c:>12}" for c in classes) + f"{'Total':>8}"
    print(header)
    print("-" * len(header))
    for r in classes:
        row_str = f"{r:<14}" + "".join(f"{conf_matrix[r][p]:>12}" for p in classes) + f"{sum(conf_matrix[r].values()):>8}"
        print(row_str)
    print("=" * 70)

if __name__ == "__main__":
    run_evaluation()
