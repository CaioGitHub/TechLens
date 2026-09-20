from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any


STAGES = (
    "20.1",
    "20.2",
    "20.3",
    "20.4",
    "20.5",
    "20.6",
    "20.7",
    "21",
    "23",
    "report",
)


class PipelineBlocked(RuntimeError):
    def __init__(self, result: dict[str, Any]):
        super().__init__("pipeline blocked")
        self.result = result


@dataclass(frozen=True)
class StageResult:
    stage: str
    status: str
    input_id: str
    output_id: str
    warnings: tuple[str, ...] = ()
    errors: tuple[str, ...] = ()


def _stable_id(prefix: str, value: str) -> str:
    digest = sha256(value.encode("utf-8")).hexdigest()[:8]
    return f"{prefix}-{digest}"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _stage(
    stage: str,
    status: str,
    input_id: str,
    output_id: str,
    warnings: list[str] | None = None,
    errors: list[str] | None = None,
) -> dict[str, Any]:
    result = StageResult(
        stage,
        status,
        input_id,
        output_id,
        tuple(warnings or ()),
        tuple(errors or ()),
    )
    return {
        "stage": result.stage,
        "status": result.status,
        "input_id": result.input_id,
        "output_id": result.output_id,
        "warnings": list(result.warnings),
        "errors": list(result.errors),
    }


def _fixture_id(fixture: dict[str, Any]) -> str:
    return fixture.get("fixture_id", "synthetic-input")


def _participants(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    return deepcopy(fixture.get("participants", []))


def _source(segment_id: str) -> dict[str, list[str]]:
    return {"segment_ids": [segment_id]}


def _find_segment(segments: list[dict[str, Any]], segment_id: str) -> dict[str, Any] | None:
    return next((segment for segment in segments if segment["id"] == segment_id), None)


def _stage_201(fixture: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    participants = _participants(fixture)
    if not participants:
        participants = [
            {"participant_id": "P-INTERVIEWER", "role": "interviewer"},
            {"participant_id": "P-CANDIDATE", "role": "candidate"},
        ]
    return participants, _stage("20.1", "COMPLETED", _fixture_id(fixture), "participants")


def _stage_202(
    fixture: dict[str, Any], participants: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    known_roles = {p["role"]: p["participant_id"] for p in participants}
    segments = []
    warnings: list[str] = []
    for source in fixture.get("transcript", []):
        segment = deepcopy(source)
        role = segment.get("speaker_role")
        if segment.get("ambiguous_speaker"):
            segment["speaker_id"] = "unknown"
            segment["participant_id"] = None
            segment["attribution_confidence"] = "low"
            segment["needs_review"] = True
            warnings.append(f"ambiguous speaker: {segment['id']}")
        else:
            segment["speaker_id"] = segment.get("speaker_id", role or "unknown")
            segment["participant_id"] = segment.get(
                "participant_id", known_roles.get(role)
            )
            segment["attribution_confidence"] = segment.get(
                "attribution_confidence", "high"
            )
            segment["needs_review"] = bool(segment.get("needs_review", False))
        segments.append(segment)
    return segments, _stage(
        "20.2",
        "READY_WITH_WARNINGS" if warnings else "COMPLETED",
        "participants",
        "speaker-attributed-transcript",
        warnings,
    )


def _stage_203(
    segments: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    questions: list[dict[str, Any]] = []
    for segment in segments:
        if segment.get("kind") != "question" or segment.get("candidate_question"):
            continue
        question_id = segment.get("question_id")
        if not question_id:
            continue
        question = {
            "question_id": question_id,
            "text": segment["text"],
            "primary_type": segment.get("primary_type", "technical"),
            "source": _source(segment["id"]),
            "question_status": "identified",
            "follow_up_of": segment.get("follow_up_of"),
            "reformulation_of": segment.get("reformulation_of"),
            "needs_review": bool(segment.get("needs_review", False)),
        }
        questions.append(question)
    return questions, _stage("20.3", "COMPLETED", "speaker-attributed-transcript", "questions")


def _stage_204(
    fixture: dict[str, Any],
    segments: list[dict[str, Any]],
    questions: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    question_ids = {question["question_id"] for question in questions}
    responses: list[dict[str, Any]] = []
    answered: set[str] = set()
    grouped: dict[str, dict[str, Any]] = {}
    for segment in segments:
        if segment.get("kind") != "response":
            continue
        response_id = segment.get("response_id") or _stable_id("R", segment["id"])
        question_id = segment.get("question_id", "unknown")
        group_id = segment.get("response_group_id", response_id)
        if group_id in grouped:
            grouped[group_id]["original_segments"].append(segment["id"])
            grouped[group_id]["text"] = (
                f"{grouped[group_id]['text']} {segment['text']}"
            )
            grouped[group_id]["source"]["segment_ids"].append(segment["id"])
            grouped[group_id]["needs_review"] = (
                grouped[group_id]["needs_review"]
                or bool(segment.get("needs_review", False))
            )
            continue
        response = {
            "response_id": group_id,
            "question_id": question_id if question_id in question_ids else "unknown",
            "text": segment["text"],
            "original_segments": [segment["id"]],
            "response_status": "identified",
            "response_type": segment.get("response_type", "direct"),
            "source": _source(segment["id"]),
            "needs_review": bool(segment.get("needs_review", False)),
            "speaker_id": segment.get("speaker_id"),
        }
        grouped[group_id] = response
        if response["question_id"] != "unknown":
            answered.add(response["question_id"])
    responses.extend(grouped.values())
    for question in questions:
        if question["question_id"] not in answered:
            responses.append(
                {
                    "response_id": None,
                    "question_id": question["question_id"],
                    "text": None,
                    "original_segments": [],
                    "response_status": "missing",
                    "response_type": None,
                    "source": {"segment_ids": []},
                    "needs_review": False,
                    "speaker_id": None,
                }
            )
    return responses, _stage("20.4", "COMPLETED", "questions", "responses")


def _stage_205(
    fixture: dict[str, Any], responses: list[dict[str, Any]], segments: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    by_id = {segment["id"]: segment for segment in segments}
    reconstructed: list[dict[str, Any]] = []
    for response in responses:
        item = deepcopy(response)
        if item["response_status"] == "missing":
            item["original_text"] = None
            item["reconstructed_text"] = None
            item["reconstruction_confidence"] = "high"
            reconstructed.append(item)
            continue
        source_ids = item["original_segments"]
        original = " ".join(by_id[segment_id]["text"] for segment_id in source_ids)
        item["original_text"] = original
        item["reconstructed_text"] = fixture.get("reconstructions", {}).get(
            item["response_id"], original
        )
        item["normalization_applied"] = (
            item["reconstructed_text"] != item["original_text"]
        )
        item["reconstruction_confidence"] = "high"
        reconstructed.append(item)
    return reconstructed, _stage("20.5", "COMPLETED", "responses", "reconstructed-responses")


def _stage_206(
    questions: list[dict[str, Any]], responses: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    links = []
    for response in responses:
        links.append(
            {
                "question_id": response["question_id"],
                "response_id": response["response_id"],
                "relation_type": "answers" if response["question_id"] != "unknown" else "unlinked",
                "needs_review": response["needs_review"]
                or response["question_id"] == "unknown",
            }
        )
    return links, _stage("20.6", "COMPLETED", "reconstructed-responses", "question-response-links")


def _stage_207(
    fixture: dict[str, Any],
    segments: list[dict[str, Any]],
    participants: list[dict[str, Any]],
    questions: list[dict[str, Any]],
    responses: list[dict[str, Any]],
    links: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any]]:
    blockers = list(fixture.get("validation_blockers", []))
    warnings = list(fixture.get("validation_warnings", []))
    segment_ids = {segment["id"] for segment in segments}
    for response in responses:
        for segment_id in response["source"]["segment_ids"]:
            if segment_id not in segment_ids:
                blockers.append(f"missing source segment: {segment_id}")
    if any(segment.get("ambiguous_speaker") for segment in segments):
        warnings.append("speaker attribution requires review")
    status = "BLOCKED" if blockers else ("READY_WITH_WARNINGS" if warnings else "READY")
    validation = {
        "status": status,
        "warnings": warnings,
        "blockers": blockers,
        "structured_interview": {
            "participants": deepcopy(participants),
            "segments": deepcopy(segments),
            "questions": deepcopy(questions),
            "responses": deepcopy(responses),
            "links": deepcopy(links),
        },
    }
    return validation, _stage(
        "20.7",
        status,
        "question-response-links",
        "structured-interview",
        warnings,
        blockers,
    )


def _stage_21(validation: dict[str, Any], fixture: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    if validation["status"] == "BLOCKED":
        return {}, _stage("21", "SKIPPED", "structured-interview", "evidence-set", errors=["upstream validation blocked"])
    evidence = []
    for response in validation["structured_interview"]["responses"]:
        if response["response_status"] == "missing" or response["response_id"] is None:
            continue
        spec = fixture.get("evidence_specs", {}).get(response["response_id"], {})
        if response["question_id"] == "unknown" and not spec.get("allow_unknown", False):
            continue
        evidence.append(
            {
                "evidence_id": spec.get(
                    "evidence_id", _stable_id("EVD", response["response_id"])
                ),
                "question_id": response["question_id"],
                "response_id": response["response_id"],
                "type": spec.get("type", "conceptual"),
                "qualification": spec.get("qualification", "positive"),
                "content": response["reconstructed_text"],
                "interpretation": spec.get("interpretation", "synthetic evidence"),
                "explicitness": spec.get("explicitness", "explicit"),
                "evidence_strength": spec.get("evidence_strength", "moderate"),
                "evidence_confidence": spec.get("evidence_confidence", "high"),
                "source": deepcopy(response["source"]),
                "needs_review": response["needs_review"],
                "relations": spec.get("relations", []),
            }
        )
    status = "READY_WITH_WARNINGS" if validation["status"] == "READY_WITH_WARNINGS" else "READY"
    result = {
        "evidence_set": evidence,
        "status": status,
        "warnings": list(validation["warnings"]),
    }
    return result, _stage("21", status, "structured-interview", "evidence-set", result["warnings"])


def _stage_23(
    fixture: dict[str, Any],
    validation: dict[str, Any],
    evidence_result: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if not evidence_result:
        return [], _stage("23", "SKIPPED", "evidence-set", "evaluations", errors=["evidence model did not execute"])
    evaluations = []
    for question in validation["structured_interview"]["questions"]:
        response = next(
            (item for item in validation["structured_interview"]["responses"] if item["question_id"] == question["question_id"]),
            None,
        )
        if response is None or response["response_status"] == "missing":
            continue
        evidence = [
            item
            for item in evidence_result["evidence_set"]
            if item["response_id"] == response["response_id"]
        ]
        spec = fixture.get("evaluation_specs", {}).get(question["question_id"], {})
        dimensions = deepcopy(
            spec.get(
                "dimensions",
                {
                    "correctness": {"assessment": "Strong", "score": 8, "applicable": True},
                    "completeness": {"assessment": "Adequate", "score": 7, "applicable": True},
                    "depth": {"assessment": "Adequate", "score": 7, "applicable": True},
                    "reasoning": {"assessment": "Adequate", "score": 7, "applicable": True},
                    "practical_application": {"assessment": "N/A", "score": None, "applicable": False},
                    "trade_offs": {"assessment": "N/A", "score": None, "applicable": False},
                },
            )
        )
        evaluations.append(
            {
                "id": spec.get("id", _stable_id("EVAL", question["question_id"])),
                "question_id": question["question_id"],
                "response_id": response["response_id"],
                "evidence_ids": [item["evidence_id"] for item in evidence],
                "dimensions": dimensions,
                "score": spec.get("score", 7.0),
                "confidence": spec.get("confidence", "high"),
                "rationale": spec.get("rationale", "Synthetic evaluation from the Evidence Set."),
                "warnings": list(evidence_result["warnings"]),
            }
        )
    status = "READY_WITH_WARNINGS" if evidence_result["status"] == "READY_WITH_WARNINGS" else "READY"
    return evaluations, _stage("23", status, "evidence-set", "evaluations")


def _stage_report(
    fixture: dict[str, Any],
    validation: dict[str, Any],
    evaluations: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any]]:
    report = {
        "report_id": _stable_id("REPORT", _fixture_id(fixture)),
        "fixture_id": _fixture_id(fixture),
        "evaluations": deepcopy(evaluations),
        "warnings": list(validation["warnings"]),
        "traceability": [
            {
                "evaluation_id": evaluation["id"],
                "question_id": evaluation["question_id"],
                "response_id": evaluation["response_id"],
                "evidence_ids": evaluation["evidence_ids"],
            }
            for evaluation in evaluations
        ],
    }
    return report, _stage("report", "COMPLETED", "evaluations", report["report_id"], report["warnings"])


def run_pipeline(fixture: dict[str, Any], job_context: dict[str, Any] | None = None) -> dict[str, Any]:
    fixture = deepcopy(fixture)
    run_id = _stable_id("RUN", _fixture_id(fixture))
    result: dict[str, Any] = {
        "run_id": run_id,
        "input_id": _fixture_id(fixture),
        "pipeline_version": "26-reference-1",
        "started_at": _now(),
        "completed_at": None,
        "status": "RUNNING",
        "readiness": None,
        "stages": [],
        "warnings": [],
        "errors": [],
        "artifacts": {},
        "job_context": deepcopy(job_context),
    }

    participants, stage = _stage_201(fixture)
    result["stages"].append(stage)
    result["artifacts"]["participants"] = participants

    segments, stage = _stage_202(fixture, participants)
    result["stages"].append(stage)
    result["artifacts"]["speaker_attributed_transcript"] = segments
    result["warnings"].extend(stage["warnings"])

    questions, stage = _stage_203(segments)
    result["stages"].append(stage)
    result["artifacts"]["questions"] = questions

    responses, stage = _stage_204(fixture, segments, questions)
    result["stages"].append(stage)
    result["artifacts"]["responses"] = responses

    responses, stage = _stage_205(fixture, responses, segments)
    result["stages"].append(stage)
    result["artifacts"]["reconstructed_responses"] = responses

    links, stage = _stage_206(questions, responses)
    result["stages"].append(stage)
    result["artifacts"]["links"] = links

    validation, stage = _stage_207(
        fixture, segments, participants, questions, responses, links
    )
    result["stages"].append(stage)
    result["artifacts"]["validation"] = validation
    result["warnings"].extend(validation["warnings"])
    if validation["status"] == "BLOCKED":
        result["status"] = "BLOCKED"
        result["readiness"] = "BLOCKED"
        result["errors"].extend(validation["blockers"])
        result["completed_at"] = _now()
        raise PipelineBlocked(result)

    evidence_result, stage = _stage_21(validation, fixture)
    result["stages"].append(stage)
    result["artifacts"]["evidence"] = evidence_result
    result["warnings"].extend(evidence_result.get("warnings", []))
    if fixture.get("upstream_version") != fixture.get("evidence_version"):
        if "stale downstream artifact: evidence-set" not in result["warnings"]:
            result["warnings"].append("stale downstream artifact: evidence-set")

    evaluations, stage = _stage_23(fixture, validation, evidence_result)
    result["stages"].append(stage)
    result["artifacts"]["evaluations"] = evaluations

    report, stage = _stage_report(fixture, validation, evaluations)
    result["stages"].append(stage)
    result["artifacts"]["report"] = report

    result["readiness"] = (
        "READY_WITH_WARNINGS"
        if result["warnings"] or validation["status"] == "READY_WITH_WARNINGS"
        else "READY"
    )
    result["status"] = "COMPLETED"
    result["completed_at"] = _now()
    return result
