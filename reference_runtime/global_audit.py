from __future__ import annotations

from copy import deepcopy
from statistics import median
from typing import Any

from .evaluation_engine import BUCKETS, EXCLUDED_RESPONSES, EXCLUDED_SEGMENTS, EvaluationInput


class GlobalAuditError(AssertionError):
    """Raised when the Stage 23 output violates an independent invariant."""


def _expected_distribution(scores: list[float]) -> dict[str, int]:
    result = {label: 0 for label, *_ in BUCKETS}
    for score in scores:
        for label, lower, upper, final in BUCKETS:
            in_bucket = lower <= score <= upper if final else lower <= score < upper
            if in_bucket:
                result[label] += 1
                break
        else:
            raise GlobalAuditError(f"score outside distribution buckets: {score}")
    return result


def audit_global_output(
    input_data: EvaluationInput,
    output: dict[str, Any],
) -> dict[str, Any]:
    """Validate independent Stage 23 invariants without recomputing the engine."""
    evaluations = input_data.evaluations
    evidence = {item["evidence_id"]: item for item in input_data.evidence}
    scores = [float(item["score"]) for item in evaluations]
    summary = output["summary"]
    expected = {
        "questions_evaluated": len(scores),
        "average_score": round(sum(scores) / len(scores), 2),
        "median_score": float(median(scores)),
        "minimum_score": min(scores),
        "maximum_score": max(scores),
    }
    for key, value in expected.items():
        if summary.get(key) != value:
            raise GlobalAuditError(f"{key}: expected {value!r}, got {summary.get(key)!r}")
    distribution = _expected_distribution(scores)
    if output.get("distribution") != distribution:
        raise GlobalAuditError("distribution does not match independent calculation")

    expected_questions = {item["question_id"] for item in evaluations}
    actual_questions = set(output["traceability"]["question_ids"])
    if actual_questions != expected_questions:
        raise GlobalAuditError("output question IDs differ from individual evaluations")
    if len(actual_questions) != len(evaluations):
        raise GlobalAuditError("duplicate or missing evaluated question")
    for excluded in ("Q8", "Q12"):
        if excluded in actual_questions:
            raise GlobalAuditError(f"{excluded} must not be independently evaluated")

    used_evidence = set(output["traceability"]["evidence_ids"])
    input_evidence = {
        evidence_id
        for item in evaluations
        for evidence_id in item.get("evidence_ids", [])
    }
    if used_evidence != input_evidence:
        raise GlobalAuditError("output evidence set differs from input references")
    if output["traceability"]["new_evidence_created"]:
        raise GlobalAuditError("runtime reported newly created evidence")
    for evidence_id in used_evidence:
        item = evidence.get(evidence_id)
        if item is None:
            raise GlobalAuditError(f"orphan evidence reference: {evidence_id}")
        if item.get("response_id") in EXCLUDED_RESPONSES:
            raise GlobalAuditError(f"excluded response reintroduced: {item['response_id']}")
        if set(item.get("source", {}).get("segment_ids", ())) & EXCLUDED_SEGMENTS:
            raise GlobalAuditError(f"excluded source reintroduced: {evidence_id}")
        if not output["traceability"]["evidence_sources"].get(evidence_id):
            raise GlobalAuditError(f"missing source traceability: {evidence_id}")

    if output["gates"].get("stage_23_1") != "NOT_EXECUTED":
        raise GlobalAuditError("Stage 23.1 was unexpectedly executed by Stage 23")
    if summary.get("confidence") != "medium":
        raise GlobalAuditError("current bounded pilot should have medium global confidence")
    if output.get("domains", {}).get("azure", {}).get("coverage") == "Evaluated":
        raise GlobalAuditError("unsupported domain was introduced")
    if output.get("complexity", {}).get("advanced", {}).get("coverage") != "Not evaluated":
        raise GlobalAuditError("advanced complexity must remain not evaluated")

    return {
        "mathematical_validation": "PASS",
        "evaluation_count": len(scores),
        "evidence_count": len(input_data.evidence),
        "questions": sorted(expected_questions),
        "evidence_ids": sorted(used_evidence),
        "excluded_responses_reintroduced": False,
        "candidate_questions_reintroduced": False,
        "q8_independent_evaluation": False,
        "q12_evaluation": False,
        "confidence": summary["confidence"],
    }


def audit_input_copy(input_data: EvaluationInput) -> EvaluationInput:
    """Return a safe copy for mutation tests without changing canonical inputs."""
    return EvaluationInput(
        deepcopy(input_data.evaluations),
        deepcopy(input_data.evidence),
        input_data.evaluations_source,
        input_data.evidence_source,
    )


__all__ = ["GlobalAuditError", "audit_global_output", "audit_input_copy"]
