from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .evaluation_engine import load_pilot_input, run_evaluation_engine
from .global_audit import audit_global_output
from .materialization import materialize_interview_evaluation_v2
from .runtime import PipelineBlocked, run_pipeline


NOT_STARTED = "NOT_STARTED"
RUNNING = "RUNNING"
READY = "READY"
READY_WITH_WARNINGS = "READY_WITH_WARNINGS"
BLOCKED = "BLOCKED"
FAILED = "FAILED"

STAGE_ORDER = ("20.1", "20.2", "20.3", "20.4", "20.5", "20.6", "20.7", "21", "22", "23", "23.1", "23.2")
APPROVED_AUDIT_GATES = {"GLOBAL_EVALUATION_AUDIT_COMPLETE", "GLOBAL_EVALUATION_AUDIT_COMPLETE_WITH_WARNINGS"}


@dataclass(frozen=True)
class PilotPaths:
    evaluations: Path
    evidence: Path
    materialized_output: Path
    structured_interview: Path | None = None
    audit: Path | None = None


def _stage(stage: str, status: str, gate: str, *, warnings=None, errors=None, artifact=None) -> dict[str, Any]:
    return {
        "stage": stage,
        "status": status,
        "gate": gate,
        "warnings": list(warnings or []),
        "errors": list(errors or []),
        "artifact": artifact,
    }


def _base_result(run_id: str) -> dict[str, Any]:
    return {
        "pipeline": {
            "run_id": run_id,
            "status": RUNNING,
            "started_at": None,
            "completed_at": None,
            "failed_stage": None,
        },
        "stages": [],
        "artifacts": {},
        "warnings": [],
        "errors": [],
        "traceability": {
            "source_transcript": None,
            "question_ids": [],
            "response_ids": [],
            "evidence_ids": [],
            "evaluation_ids": [],
        },
        "confidence": {},
        "readiness": {"ready_for_next_stage": False},
        "reused": False,
    }


def _append(result: dict[str, Any], item: dict[str, Any]) -> None:
    result["stages"].append(item)
    result["warnings"].extend(item["warnings"])
    result["errors"].extend(item["errors"])


def _stop(result: dict[str, Any], stage: str, status: str, reason: str) -> dict[str, Any]:
    result["pipeline"]["status"] = status
    result["pipeline"]["failed_stage"] = stage
    result["pipeline"]["blockers"] = [reason]
    result["errors"].append(reason)
    result["readiness"]["ready_for_next_stage"] = False
    return result


def _trace_from_structured(result: dict[str, Any], structured: dict[str, Any]) -> None:
    result["traceability"]["question_ids"] = [
        item["question_id"] for item in structured.get("questions", []) if item.get("question_id")
    ]
    result["traceability"]["response_ids"] = [
        item["response_id"] for item in structured.get("responses", []) if item.get("response_id")
    ]
    result["traceability"]["source_transcript"] = structured.get("source_transcript")


def detect_stale_artifacts(versions: dict[str, str]) -> list[str]:
    """Return downstream artifacts whose recorded source version is stale."""
    checks = (
        ("structured_interview", "transcript"),
        ("evidence_set", "structured_interview"),
        ("individual_evaluations", "evidence_set"),
        ("evaluation_result", "individual_evaluations"),
        ("global_audit", "evaluation_result"),
        ("interview_evaluation_v2", "global_audit"),
    )
    return [
        artifact
        for artifact, upstream in checks
        if artifact in versions and upstream in versions and versions[artifact] != versions[upstream]
    ]


def semantic_projection(result: dict[str, Any]) -> dict[str, Any]:
    """Remove operational identity while retaining pipeline semantics."""
    projection = deepcopy(result)
    pipeline = projection.get("pipeline", {})
    pipeline.pop("started_at", None)
    pipeline.pop("completed_at", None)
    projection.pop("reused", None)
    return projection


def _run_canonical(
    paths: PilotPaths,
    result: dict[str, Any],
    *,
    stage_overrides: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    overrides = stage_overrides or {}
    for stage_id in ("20.7", "21", "22"):
        override = overrides.get(stage_id)
        if override:
            item = _stage(
                stage_id,
                override.get("status", READY),
                override.get("gate", "READY"),
                warnings=override.get("warnings"),
                errors=override.get("errors"),
                artifact=override.get("artifact"),
            )
        else:
            gate = "TRANSCRIPTION_PROCESSING_COMPLETE" if stage_id == "20.7" else (
                "EVIDENCE_MODEL_COMPLETE" if stage_id == "21" else "RUBRIC_COMPLETE"
            )
            item = _stage(stage_id, READY_WITH_WARNINGS if stage_id == "20.7" else READY, gate)
        _append(result, item)
        if item["status"] in {BLOCKED, FAILED}:
            return _stop(result, stage_id, item["status"], f"{stage_id} blocked the pipeline")

    try:
        override = overrides.get("23")
        if override and override.get("status") in {BLOCKED, FAILED}:
            _append(result, _stage("23", override["status"], override.get("gate", "BLOCKED"), warnings=override.get("warnings"), errors=override.get("errors")))
            return _stop(result, "23", override["status"], "23 blocked the pipeline")
        input_data = load_pilot_input(paths.evaluations, paths.evidence)
        runtime = run_evaluation_engine(input_data)["interview_evaluation"]
    except Exception as error:
        return _stop(result, "23", FAILED, str(error))
    result["artifacts"]["evaluation_result"] = deepcopy(runtime)
    result["traceability"]["question_ids"] = list(runtime["traceability"]["question_ids"])
    result["traceability"]["evaluation_ids"] = list(runtime["traceability"]["evaluation_ids"])
    result["traceability"]["evidence_ids"] = list(runtime["traceability"]["evidence_ids"])
    result["confidence"]["evaluation"] = runtime["summary"]["confidence"]
    _append(result, _stage(
        "23",
        READY_WITH_WARNINGS if runtime["warnings"] else READY,
        runtime["gates"]["stage_23"],
        warnings=runtime["warnings"],
        artifact=str(paths.evaluations),
    ))

    override = overrides.get("23.1")
    if override and override.get("status") in {BLOCKED, FAILED}:
        _append(result, _stage("23.1", override["status"], override.get("gate", "BLOCKED"), errors=override.get("errors")))
        return _stop(result, "23.1", override["status"], "global audit did not reach an approved gate")
    try:
        audit = audit_global_output(input_data, runtime)
    except Exception as error:
        _append(result, _stage("23.1", BLOCKED, "BLOCKED", errors=[str(error)]))
        return _stop(result, "23.1", BLOCKED, str(error))
    result["artifacts"]["global_audit"] = deepcopy(audit)
    audit_gate = "GLOBAL_EVALUATION_AUDIT_COMPLETE_WITH_WARNINGS" if runtime["warnings"] else "GLOBAL_EVALUATION_AUDIT_COMPLETE"
    _append(result, _stage(
        "23.1",
        READY_WITH_WARNINGS if runtime["warnings"] else READY,
        audit_gate,
        warnings=runtime["warnings"] + list((override or {}).get("warnings", [])),
        artifact=paths.audit,
    ))

    if override and override.get("gate") not in APPROVED_AUDIT_GATES:
        return _stop(result, "23.1", BLOCKED, "global audit gate is not approved for materialization")
    materialized = materialize_interview_evaluation_v2(
        paths.evaluations,
        paths.evidence,
        paths.materialized_output,
    )
    result["artifacts"]["interview_evaluation_v2"] = str(paths.materialized_output)
    _append(result, _stage(
        "23.2",
        READY_WITH_WARNINGS if runtime["warnings"] else READY,
        materialized["gate"],
        warnings=runtime["warnings"],
        artifact=str(paths.materialized_output),
    ))
    result["pipeline"]["status"] = READY_WITH_WARNINGS if runtime["warnings"] else READY
    result["pipeline"]["completed_at"] = None
    result["readiness"]["ready_for_next_stage"] = True
    return result


def _run_structured(
    fixture: dict[str, Any],
    result: dict[str, Any],
    *,
    stage_overrides: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    overrides = stage_overrides or {}
    try:
        runtime_result = run_pipeline(fixture)
    except PipelineBlocked as error:
        runtime_result = error.result
        for item in runtime_result.get("stages", []):
            _append(result, _stage(
                item["stage"],
                item["status"],
                item["status"],
                warnings=item.get("warnings"),
                errors=item.get("errors"),
            ))
        result["artifacts"].update(deepcopy(runtime_result.get("artifacts", {})))
        return _stop(result, "20.7", BLOCKED, "; ".join(runtime_result.get("errors", [])))
    result["artifacts"].update(deepcopy(runtime_result["artifacts"]))
    for item in runtime_result["stages"]:
        _append(result, _stage(
            item["stage"],
            item["status"],
            item["status"],
            warnings=item.get("warnings"),
            errors=item.get("errors"),
        ))
    for stage_id in ("21", "22", "23"):
        if stage_id in overrides and overrides[stage_id].get("status") in {BLOCKED, FAILED}:
            return _stop(result, stage_id, overrides[stage_id]["status"], f"{stage_id} blocked the pipeline")
    result["traceability"]["question_ids"] = [
        item.get("question_id") for item in result["artifacts"].get("questions", []) if item.get("question_id")
    ]
    result["traceability"]["response_ids"] = [
        item.get("response_id") for item in result["artifacts"].get("responses", []) if item.get("response_id")
    ]
    result["traceability"]["evidence_ids"] = [
        item.get("evidence_id")
        for item in result["artifacts"].get("evidence", {}).get("evidence_set", [])
        if item.get("evidence_id")
    ]
    result["traceability"]["evaluation_ids"] = [
        item.get("id") for item in result["artifacts"].get("evaluations", []) if item.get("id")
    ]
    for stage_id in ("23.1", "23.2"):
        override = overrides.get(stage_id)
        if override and override.get("status") in {BLOCKED, FAILED}:
            return _stop(result, stage_id, override["status"], f"{stage_id} blocked the pipeline")
        _append(result, _stage(stage_id, READY_WITH_WARNINGS if result["warnings"] else READY, override.get("gate", "READY") if override else "READY"))
    result["pipeline"]["status"] = READY_WITH_WARNINGS if result["warnings"] else READY
    result["readiness"]["ready_for_next_stage"] = True
    return result


def run_interview_pipeline(
    source: PilotPaths | dict[str, Any],
    *,
    run_id: str = "INTERVIEW-PIPELINE",
    stage_overrides: dict[str, dict[str, Any]] | None = None,
    previous_result: dict[str, Any] | None = None,
    artifact_versions: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Run the Stage 24 coordination boundary without duplicating stage semantics."""
    result = _base_result(run_id)
    stale = detect_stale_artifacts(artifact_versions or {})
    if stale:
        result["stale_artifacts"] = stale
        return _stop(result, "stale-detection", BLOCKED, f"stale downstream artifacts: {', '.join(stale)}")
    if previous_result and previous_result.get("pipeline", {}).get("run_id") == run_id:
        result["reused"] = True
        reused = deepcopy(previous_result)
        reused["reused"] = True
        return reused
    if isinstance(source, PilotPaths):
        return _run_canonical(source, result, stage_overrides=stage_overrides)
    return _run_structured(deepcopy(source), result, stage_overrides=stage_overrides)


__all__ = [
    "BLOCKED",
    "FAILED",
    "NOT_STARTED",
    "PilotPaths",
    "READY",
    "READY_WITH_WARNINGS",
    "RUNNING",
    "detect_stale_artifacts",
    "run_interview_pipeline",
    "semantic_projection",
]
