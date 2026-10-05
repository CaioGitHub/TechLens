"""Stage 24 orchestration over the deterministic reference runtime.

This module coordinates existing component contracts. It deliberately does not
reimplement transcription processing, evidence generation, scoring, or report
semantics.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
import json
from hashlib import sha256
from typing import Any

from .runtime import PipelineBlocked, run_pipeline


PIPELINE_VERSION = "24-orchestration-1"
STAGE_ORDER = (
    "20.1",
    "20.2",
    "20.3",
    "20.4",
    "20.5",
    "20.6",
    "20.7",
    "21",
    "22",
    "23",
    "23.1",
    "report",
)

PENDING = "PENDING"
RUNNING = "RUNNING"
COMPLETED = "COMPLETED"
COMPLETED_WITH_WARNINGS = "COMPLETED_WITH_WARNINGS"
BLOCKED = "BLOCKED"
FAILED = "FAILED"
REQUIRES_HUMAN_REVIEW = "REQUIRES_HUMAN_REVIEW"
APPROVAL_REQUIRED = "APPROVAL_REQUIRED"


class OrchestrationError(RuntimeError):
    """Raised only for programmer/configuration errors in the orchestrator."""


@dataclass
class OrchestrationStore:
    """In-memory version registry used by tests and controlled executions."""

    versions: dict[str, list[dict[str, Any]]] = field(default_factory=dict)

    def record(self, result: dict[str, Any]) -> dict[str, Any]:
        pipeline_id = result["pipeline"]["id"]
        snapshot = deepcopy(result)
        self.versions.setdefault(pipeline_id, []).append(snapshot)
        return deepcopy(snapshot)

    def history(self, pipeline_id: str) -> list[dict[str, Any]]:
        return deepcopy(self.versions.get(pipeline_id, []))


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def content_hash(value: Any) -> str:
    return sha256(_canonical(value).encode("utf-8")).hexdigest()


def _pipeline_id(fixture: dict[str, Any]) -> str:
    return f"PIPE-{fixture.get('fixture_id', 'synthetic-input')}"


def _base_result(
    fixture: dict[str, Any],
    input_hash: str,
    *,
    human_review_approved: bool,
) -> dict[str, Any]:
    return {
        "pipeline": {
            "id": _pipeline_id(fixture),
            "status": PENDING,
            "current_stage": "",
            "completed_stages": [],
            "warnings": [],
            "blockers": [],
            "failed_stage": None,
            "affected_artifacts": [],
            "candidate": None,
            "readiness": None,
            "input_hash": input_hash,
            "pipeline_version": PIPELINE_VERSION,
            "human_review_approved": human_review_approved,
        },
        "stages": [],
        "artifacts": {},
        "warnings": [],
        "errors": [],
        "invalidation": [],
        "reused": False,
        "report_generation": {
            "status": PENDING,
            "approval_required": True,
            "generated": False,
        },
    }


def _blocked_result(
    fixture: dict[str, Any],
    input_hash: str,
    *,
    status: str,
    reason: str,
    failed_stage: str | None = None,
    human_review_approved: bool = False,
) -> dict[str, Any]:
    result = _base_result(
        fixture,
        input_hash,
        human_review_approved=human_review_approved,
    )
    result["pipeline"]["status"] = status
    result["pipeline"]["readiness"] = APPROVAL_REQUIRED if status == REQUIRES_HUMAN_REVIEW else BLOCKED
    result["pipeline"]["current_stage"] = failed_stage or "approval"
    result["pipeline"]["failed_stage"] = failed_stage
    result["pipeline"]["blockers"] = [reason]
    result["errors"] = [reason] if status in (FAILED, BLOCKED) else []
    result["warnings"] = []
    return result


def _validate_input(fixture: Any) -> str | None:
    if not isinstance(fixture, dict):
        return "input must be a mapping"
    if not fixture.get("fixture_id"):
        return "missing required input: fixture_id"
    if not isinstance(fixture.get("participants"), list):
        return "missing required input: participants"
    if not isinstance(fixture.get("transcript"), list):
        return "missing required input: transcript"
    return None


def _artifact_hashes(result: dict[str, Any]) -> dict[str, str]:
    return {
        name: content_hash(artifact)
        for name, artifact in result.get("artifacts", {}).items()
    }


def _validate_traceability(result: dict[str, Any]) -> list[str]:
    artifacts = result.get("artifacts", {})
    evidence = {
        item["evidence_id"]: item
        for item in artifacts.get("evidence", {}).get("evidence_set", [])
    }
    segments = {
        item["id"]
        for item in artifacts.get("speaker_attributed_transcript", [])
    }
    issues: list[str] = []
    for evaluation in artifacts.get("evaluations", []):
        for evidence_id in evaluation.get("evidence_ids", []):
            item = evidence.get(evidence_id)
            if item is None:
                issues.append(f"orphan evidence reference: {evidence_id}")
                continue
            for segment_id in item.get("source", {}).get("segment_ids", []):
                if segment_id not in segments:
                    issues.append(f"orphan source segment reference: {segment_id}")
    return issues


def _validate_required_artifacts(result: dict[str, Any]) -> list[str]:
    artifacts = result.get("artifacts", {})
    issues: list[str] = []
    evidence = artifacts.get("evidence")
    if not isinstance(evidence, dict) or not isinstance(evidence.get("evidence_set"), list):
        issues.append("required artifact missing: evidence-set")
    evaluations = artifacts.get("evaluations")
    if not isinstance(evaluations, list):
        issues.append("required artifact missing: evaluations")
    else:
        required_fields = ("id", "question_id", "response_id", "evidence_ids", "score", "confidence")
        for index, evaluation in enumerate(evaluations):
            missing = [field for field in required_fields if field not in evaluation]
            if missing:
                issues.append(
                    f"incomplete evaluation at index {index}: missing {', '.join(missing)}"
                )
    if not isinstance(artifacts.get("report"), dict):
        issues.append("required artifact missing: report-handoff")
    return issues


def validate_orchestration_result(result: dict[str, Any]) -> list[str]:
    """Return traceability violations without mutating the supplied result."""

    return _validate_required_artifacts(result) + _validate_traceability(result)


def _append_stage(result: dict[str, Any], stage: str, status: str, warnings: list[str] | None = None) -> None:
    result["stages"].append(
        {
            "stage": stage,
            "status": status,
            "warnings": list(warnings or []),
            "errors": [],
        }
    )
    if status in (COMPLETED, COMPLETED_WITH_WARNINGS):
        result["pipeline"]["completed_stages"].append(stage)
    result["pipeline"]["current_stage"] = stage


def _finalize(result: dict[str, Any], runtime_result: dict[str, Any]) -> dict[str, Any]:
    result["artifacts"] = deepcopy(runtime_result.get("artifacts", {}))
    result["stages"].extend(
        {
            "stage": stage["stage"],
            "status": (
                APPROVAL_REQUIRED
                if stage["stage"] == "report"
                else COMPLETED_WITH_WARNINGS
                if stage["status"] == "READY_WITH_WARNINGS"
                else BLOCKED
                if stage["status"] in ("BLOCKED", "FAILED")
                else COMPLETED
            ),
            "warnings": list(stage.get("warnings", [])),
            "errors": list(stage.get("errors", [])),
        }
        for stage in runtime_result.get("stages", [])
    )
    result["warnings"] = list(dict.fromkeys(runtime_result.get("warnings", [])))
    result["errors"] = list(runtime_result.get("errors", []))
    result["pipeline"]["warnings"] = list(result["warnings"])
    result["pipeline"]["candidate"] = next(
        (
            participant
            for participant in result["artifacts"].get("participants", [])
            if participant.get("role") == "candidate"
        ),
        None,
    )
    result["pipeline"]["completed_stages"] = [
        stage["stage"]
        for stage in result["stages"]
        if stage["status"] in (COMPLETED, COMPLETED_WITH_WARNINGS)
    ]
    result["pipeline"]["completed_stages"].sort(
        key=lambda stage: STAGE_ORDER.index(stage) if stage in STAGE_ORDER else len(STAGE_ORDER)
    )
    return result


def run_orchestration(
    fixture: dict[str, Any],
    *,
    human_review_approved: bool = False,
    global_audit_status: str | None = None,
    report_approved: bool = False,
    generate_report: bool = False,
    store: OrchestrationStore | None = None,
    previous_result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run the controlled orchestration without processing a real interview.

    Human review is always explicit. The runtime's ``report`` artifact remains
    a handoff artifact unless report generation is explicitly approved.
    """

    input_error = _validate_input(fixture)
    input_hash = content_hash(fixture) if isinstance(fixture, dict) else content_hash(str(fixture))
    if input_error:
        result = _blocked_result(
            fixture if isinstance(fixture, dict) else {},
            input_hash,
            status=FAILED,
            reason=input_error,
            failed_stage="input",
        )
        if store:
            store.record(result)
        return result

    if previous_result is not None:
        previous_hash = previous_result.get("pipeline", {}).get("input_hash")
        if previous_hash == input_hash:
            reused = deepcopy(previous_result)
            reused["reused"] = True
            if store:
                store.record(reused)
            return reused

    if not human_review_approved:
        result = _blocked_result(
            fixture,
            input_hash,
            status=REQUIRES_HUMAN_REVIEW,
            reason="explicit human approval is required before downstream processing",
        )
        if store:
            store.record(result)
        return result

    result = _base_result(
        fixture,
        input_hash,
        human_review_approved=True,
    )
    result["pipeline"]["status"] = RUNNING
    try:
        runtime_result = run_pipeline(fixture)
    except PipelineBlocked as error:
        result = _finalize(result, error.result)
        result["pipeline"]["status"] = BLOCKED
        result["pipeline"]["readiness"] = BLOCKED
        result["pipeline"]["blockers"] = list(error.result.get("errors", []))
        result["pipeline"]["failed_stage"] = next(
            (
                stage["stage"]
                for stage in result["stages"]
                if stage["status"] == "BLOCKED"
            ),
            "20.7",
        )
        result["pipeline"]["affected_artifacts"] = [
            "evidence",
            "evaluations",
            "report",
        ]
        if store:
            store.record(result)
        return result
    except Exception as error:  # pragma: no cover - defensive boundary
        result["pipeline"]["status"] = FAILED
        result["pipeline"]["readiness"] = BLOCKED
        result["pipeline"]["failed_stage"] = "runtime"
        result["pipeline"]["blockers"] = [str(error)]
        result["errors"] = [str(error)]
        if store:
            store.record(result)
        return result

    _finalize(result, runtime_result)
    integrity_issues = validate_orchestration_result(result)
    if integrity_issues:
        result["pipeline"]["status"] = BLOCKED
        result["pipeline"]["readiness"] = BLOCKED
        result["pipeline"]["blockers"] = integrity_issues
        result["pipeline"]["failed_stage"] = (
            "artifact-integrity"
            if any(issue.startswith(("required artifact", "incomplete evaluation")) for issue in integrity_issues)
            else "traceability"
        )
        result["pipeline"]["affected_artifacts"] = ["evidence", "evaluations", "report"]
        if any(issue.startswith("required artifact missing: evidence-set") for issue in integrity_issues):
            result["artifacts"].pop("evaluations", None)
            result["artifacts"].pop("report", None)
        if store:
            store.record(result)
        return result

    for stage in ("22", "23", "23.1"):
        if stage not in result["pipeline"]["completed_stages"]:
            _append_stage(result, stage, COMPLETED_WITH_WARNINGS if result["warnings"] else COMPLETED)
    result["pipeline"]["completed_stages"].sort(
        key=lambda stage: STAGE_ORDER.index(stage) if stage in STAGE_ORDER else len(STAGE_ORDER)
    )

    if global_audit_status not in ("PASS", "PASS_WITH_WARNINGS"):
        result["pipeline"]["status"] = APPROVAL_REQUIRED
        result["pipeline"]["readiness"] = APPROVAL_REQUIRED
        result["pipeline"]["current_stage"] = "23.1"
        result["pipeline"]["blockers"] = [
            "global evaluation audit approval is required before report generation"
        ]
        result["report_generation"]["status"] = APPROVAL_REQUIRED
        result["report_generation"]["audit_status"] = global_audit_status
        if store:
            store.record(result)
        return result

    result["report_generation"]["audit_status"] = global_audit_status
    result["report_generation"]["status"] = APPROVAL_REQUIRED
    if generate_report:
        if not report_approved:
            result["pipeline"]["status"] = APPROVAL_REQUIRED
            result["pipeline"]["readiness"] = APPROVAL_REQUIRED
            result["pipeline"]["blockers"] = [
                "explicit report approval is required before report generation"
            ]
            if store:
                store.record(result)
            return result
        result["artifacts"]["final_report"] = deepcopy(result["artifacts"].get("report"))
        result["report_generation"] = {
            "status": COMPLETED_WITH_WARNINGS if result["warnings"] else COMPLETED,
            "approval_required": True,
            "approved": True,
            "generated": True,
            "audit_status": global_audit_status,
        }
        _append_stage(result, "report", result["report_generation"]["status"])
    else:
        result["report_generation"]["status"] = APPROVAL_REQUIRED

    result["pipeline"]["status"] = (
        COMPLETED_WITH_WARNINGS if result["warnings"] else COMPLETED
    )
    result["pipeline"]["readiness"] = (
        "READY_WITH_WARNINGS" if result["warnings"] else "READY"
    )
    result["pipeline"]["current_stage"] = "report" if generate_report else "23.1"
    result["pipeline"]["affected_artifacts"] = []
    result["artifact_hashes"] = _artifact_hashes(result)
    if store:
        store.record(result)
    return result


def resume_orchestration(
    previous_result: dict[str, Any],
    fixture: dict[str, Any],
    **kwargs: Any,
) -> dict[str, Any]:
    """Resume only when content is unchanged; otherwise invalidate dependents."""

    current_hash = content_hash(fixture)
    previous_hash = previous_result.get("pipeline", {}).get("input_hash")
    result = run_orchestration(
        fixture,
        previous_result=previous_result,
        **kwargs,
    )
    if previous_hash != current_hash:
        result["invalidation"] = [
            {
                "from_stage": "20.1",
                "reason": "input content hash changed",
                "invalidated_stages": list(STAGE_ORDER),
            }
        ]
        result["reused"] = False
    return result


__all__ = [
    "APPROVAL_REQUIRED",
    "BLOCKED",
    "COMPLETED",
    "COMPLETED_WITH_WARNINGS",
    "FAILED",
    "OrchestrationStore",
    "PIPELINE_VERSION",
    "REQUIRES_HUMAN_REVIEW",
    "RUNNING",
    "content_hash",
    "resume_orchestration",
    "run_orchestration",
    "validate_orchestration_result",
]
