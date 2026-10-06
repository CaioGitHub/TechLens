from __future__ import annotations

from copy import deepcopy
from typing import Any, Iterable

from .runtime import run_pipeline


FORBIDDEN_REFERENCE_KEYS = {
    "oracle",
    "reference",
    "expected_score",
    "expected_score_range",
    "expected_dimensions",
    "expected_quality",
    "calibration_label",
    "evidence_specs",
    "evaluation_specs",
}


def blind_input(fixture: dict[str, Any]) -> dict[str, Any]:
    """Return only execution data; calibration references never cross this boundary."""
    return {
        key: deepcopy(value)
        for key, value in fixture.items()
        if key not in FORBIDDEN_REFERENCE_KEYS
    }


def run_blind_case(fixture: dict[str, Any]) -> dict[str, Any]:
    runtime_input = blind_input(fixture)
    leaked = FORBIDDEN_REFERENCE_KEYS.intersection(runtime_input)
    if leaked:
        raise ValueError(f"calibration reference leaked into runtime input: {sorted(leaked)}")
    return run_pipeline(runtime_input)


def run_blind_calibration(
    fixtures: dict[str, dict[str, Any]],
    case_ids: Iterable[str] | None = None,
) -> dict[str, dict[str, Any]]:
    selected = set(case_ids) if case_ids is not None else set(fixtures)
    return {
        case_id: run_blind_case(fixture)
        for case_id, fixture in fixtures.items()
        if case_id in selected
    }


__all__ = ["FORBIDDEN_REFERENCE_KEYS", "blind_input", "run_blind_case", "run_blind_calibration"]
