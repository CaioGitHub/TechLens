from __future__ import annotations

from typing import Any


def _evaluation(result: dict[str, Any]) -> dict[str, Any]:
    evaluations = result.get("artifacts", {}).get("evaluations", [])
    if not evaluations:
        raise ValueError("calibration result contains no evaluation")
    return evaluations[0]


def _evidence_types(result: dict[str, Any]) -> set[str]:
    return {
        item["type"]
        for item in result.get("artifacts", {}).get("evidence", {}).get("evidence_set", [])
    }


def _dimension_matches(actual: str, expected: str) -> bool:
    return expected.lower() in actual.lower()


def compare_calibration_case(
    case_id: str,
    result: dict[str, Any],
    reference: dict[str, Any],
) -> dict[str, Any]:
    evaluation = _evaluation(result)
    types = _evidence_types(result)
    divergences: list[dict[str, str]] = []
    for evidence_type in reference.get("must_have", []):
        if evidence_type == "multiple_evidence_types":
            if len(types) < 3:
                divergences.append({"kind": "missing_evidence", "detail": evidence_type})
        elif evidence_type == "na_dimension":
            dimensions = evaluation.get("dimensions", {})
            if any(
                dimensions.get(name, {}).get("applicable", True)
                for name in ("practical_application", "trade_offs")
            ):
                divergences.append({"kind": "dimension", "detail": evidence_type})
        elif evidence_type not in types:
            divergences.append({"kind": "missing_evidence", "detail": evidence_type})
    for evidence_type in reference.get("must_not_have", []):
        if evidence_type in types:
            divergences.append({"kind": "extrapolation", "detail": evidence_type})
    for dimension, expected in reference.get("dimensions", {}).items():
        actual = evaluation["dimensions"].get(dimension, {}).get("assessment", "N/A")
        if not _dimension_matches(actual, expected):
            divergences.append(
                {
                    "kind": "dimension",
                    "detail": f"{dimension}: expected {expected}, got {actual}",
                }
            )
    minimum, maximum = reference.get("score_range", (0.0, 10.0))
    score = evaluation["score"]
    if not minimum <= score <= maximum:
        divergences.append(
            {"kind": "score", "detail": f"{score} outside {minimum}..{maximum}"}
        )
    expected_confidence = reference.get("confidence")
    if expected_confidence and evaluation.get("confidence") != expected_confidence:
        divergences.append(
            {
                "kind": "confidence",
                "detail": f"expected {expected_confidence}, got {evaluation.get('confidence')}",
            }
        )
    status = "PASS" if not divergences else (
        "WARNING" if all(item["kind"] in {"score", "confidence"} for item in divergences)
        else "FAIL"
    )
    return {
        "case_id": case_id,
        "status": status,
        "system_result": {
            "score": evaluation["score"],
            "confidence": evaluation["confidence"],
            "dimensions": evaluation["dimensions"],
            "evidence_types": sorted(types),
        },
        "reference": reference,
        "divergences": divergences,
    }


def compare_calibration(
    results: dict[str, dict[str, Any]],
    references: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    cases = [
        compare_calibration_case(case_id, results[case_id], references[case_id])
        for case_id in sorted(results)
    ]
    counts = {status.lower(): sum(item["status"] == status for item in cases) for status in ("PASS", "WARNING", "FAIL")}
    alignment = {
        "strong": counts["pass"],
        "acceptable": counts["warning"],
        "weak": counts["fail"],
    }
    dimension_alignment = {}
    for dimension in (
        "correctness",
        "completeness",
        "depth",
        "reasoning",
        "practical_application",
        "trade_offs",
    ):
        dimension_alignment[dimension] = {
            "pass": sum(
                not any(
                    item["kind"] == "dimension" and item["detail"].startswith(f"{dimension}:")
                    for item in case["divergences"]
                )
                for case in cases
            ),
            "fail": sum(
                any(
                    item["kind"] == "dimension" and item["detail"].startswith(f"{dimension}:")
                    for item in case["divergences"]
                )
                for case in cases
            ),
        }
    confidence_alignment = {
        "pass": sum(
            not any(item["kind"] == "confidence" for item in case["divergences"])
            for case in cases
        ),
        "warning": sum(
            any(item["kind"] == "confidence" for item in case["divergences"])
            for case in cases
        ),
        "fail": 0,
    }
    return {
        "calibration": {
            "total_cases": len(cases),
            "pass": counts["pass"],
            "warning": counts["warning"],
            "fail": counts["fail"],
            "semantic_alignment": alignment,
            "dimension_alignment": dimension_alignment,
            "confidence_alignment": confidence_alignment,
            "cases": cases,
        }
    }


__all__ = ["compare_calibration", "compare_calibration_case"]
