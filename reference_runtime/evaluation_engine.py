from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
import re
from statistics import median
from typing import Any, Iterable


DIMENSIONS = (
    "correctness",
    "completeness",
    "depth",
    "reasoning",
    "practical_application",
    "trade_offs",
)
CONFIDENCES = {"low", "medium", "high"}
EXCLUDED_RESPONSES = {"R24", "R26", "R41", "R52", "R31"}
EXCLUDED_SEGMENTS = {"RAW-065"}
BUCKETS = (
    ("0–2", 0.0, 2.0, False),
    ("2–4", 2.0, 4.0, False),
    ("4–6", 4.0, 6.0, False),
    ("6–8", 6.0, 8.0, False),
    ("8–10", 8.0, 10.0, True),
)


class EvaluationInputError(ValueError):
    """Raised when Stage 23 input violates the canonical contracts."""


@dataclass(frozen=True)
class EvaluationInput:
    evaluations: list[dict[str, Any]]
    evidence: list[dict[str, Any]]
    evaluations_source: str = "Individual Evaluations v2.md"
    evidence_source: str = "Evidence Set v1.md"


def _section(text: str, heading: str, next_headings: Iterable[str]) -> str:
    start = text.find(heading)
    if start < 0:
        return ""
    end = len(text)
    for candidate in next_headings:
        position = text.find(candidate, start + len(heading))
        if position >= 0:
            end = min(end, position)
    return text[start:end]


def _list_value(text: str, key: str) -> list[str]:
    match = re.search(rf"^\s*{re.escape(key)}:\s*\[([^\]]*)\]", text, re.MULTILINE)
    if not match:
        return []
    return re.findall(r"[A-Za-z][A-Za-z0-9_.-]*", match.group(1))


def _scalar(text: str, key: str) -> str | None:
    match = re.search(rf"^\s*{re.escape(key)}:\s*([^\n]+)", text, re.MULTILINE)
    return match.group(1).strip().strip('"') if match else None


def load_individual_evaluations(path: str | Path) -> list[dict[str, Any]]:
    text = Path(path).read_text(encoding="utf-8")
    blocks = re.split(r"(?=^## EV-Q\d+ — Q\d+$)", text, flags=re.MULTILINE)
    evaluations: list[dict[str, Any]] = []
    for block in blocks:
        header = re.search(r"^## (EV-(Q\d+)) — (Q\d+)$", block, re.MULTILINE)
        if not header:
            continue
        evaluation_id, question_id, header_question_id = header.groups()
        if question_id != header_question_id:
            raise EvaluationInputError(f"question mismatch in {evaluation_id}")
        score_match = re.search(r"^\s+value:\s*([0-9]+(?:\.[0-9])?)$", block, re.MULTILINE)
        if not score_match:
            raise EvaluationInputError(f"missing score for {evaluation_id}")
        response = _section(
            block,
            "  response:",
            ("  expected:", "  weights:", "  evidence:", "  dimensions:"),
        )
        evaluation: dict[str, Any] = {
            "evaluation_id": evaluation_id,
            "question_id": question_id,
            "score": float(score_match.group(1)),
            "confidence": _scalar(_section(block, "  score:", ("  findings:",)), "confidence"),
            "domain": _list_value(_section(block, "    domain:", ("    primary_type:",)), "domain"),
            "complexity": _scalar(_section(block, "    complexity:", ("  response:",)), "complexity"),
            "response_ids": _list_value(response, "id"),
            "evidence_ids": [],
            "dimensions": {},
            "strengths": [],
            "gaps": [],
            "errors": [],
        }
        for dimension in DIMENSIONS:
            dimension_text = _section(
                block,
                f"    {dimension}:",
                tuple(f"    {name}:" for name in DIMENSIONS if name != dimension),
            )
            if not dimension_text:
                continue
            applicable = _scalar(dimension_text, "applicable")
            evaluation["dimensions"][dimension] = {
                "applicable": applicable == "true",
                "assessment": _scalar(dimension_text, "assessment") or "N/A",
                "evidence_ids": _list_value(dimension_text, "evidence"),
            }
            evaluation["evidence_ids"].extend(
                evaluation["dimensions"][dimension]["evidence_ids"]
            )
        evidence_section = _section(
            block,
            "  evidence:",
            ("  dimensions:", "  score:", "  findings:"),
        )
        for category in ("positive", "partial", "negative", "contradictory", "absent", "insufficient"):
            evaluation["evidence_ids"].extend(_list_value(evidence_section, category))
        evaluation["evidence_ids"] = sorted(set(evaluation["evidence_ids"]))
        findings = _section(block, "  findings:", ("  rationale:", "  related_knowledge:"))
        strengths_text = _section(findings, "    strengths:", ("    gaps:", "    errors:"))
        gaps_text = _section(findings, "    gaps:", ("    errors:",))
        evaluation["strengths"] = re.findall(r'"([^"]+)"', strengths_text)
        evaluation["gaps"] = re.findall(r'"([^"]+)"', gaps_text)
        error_section = _section(findings, "    errors:", ())
        severity = _scalar(error_section, "severity")
        if severity:
            error_evidence = _list_value(error_section, "evidence")
            if not error_evidence:
                single_evidence = _scalar(error_section, "evidence_id")
                error_evidence = [single_evidence] if single_evidence else []
            evaluation["errors"].append(
                {
                    "severity": severity,
                    "question_id": question_id,
                    "evidence_ids": error_evidence,
                    "description": _scalar(error_section, "description") or "",
                }
            )
        evaluations.append(evaluation)
    return evaluations


def load_evidence_set(path: str | Path) -> list[dict[str, Any]]:
    text = Path(path).read_text(encoding="utf-8")
    items: list[dict[str, Any]] = []
    blocks = re.split(r"(?=^\s+- evidence_id: E-\d+$)", text, flags=re.MULTILINE)
    for block in blocks:
        evidence_id_match = re.search(r"^\s*-\s*evidence_id:\s*(E-\d+)\s*$", block, re.MULTILINE)
        evidence_id = evidence_id_match.group(1) if evidence_id_match else None
        if not evidence_id:
            continue
        items.append(
            {
                "evidence_id": evidence_id,
                "question_id": _scalar(block, "question_id"),
                "response_id": _scalar(block, "response_id"),
                "type": _scalar(block, "type"),
                "qualification": _scalar(block, "qualification"),
                "source": {
                    "segment_ids": _list_value(block, "segment_ids")
                },
            }
        )
    return items


def load_pilot_input(
    evaluations_path: str | Path, evidence_path: str | Path
) -> EvaluationInput:
    return EvaluationInput(
        load_individual_evaluations(evaluations_path),
        load_evidence_set(evidence_path),
        str(Path(evaluations_path)),
        str(Path(evidence_path)),
    )


def _validate(input_data: EvaluationInput) -> None:
    evaluations = input_data.evaluations
    evidence = input_data.evidence
    evaluation_ids = [item.get("evaluation_id") for item in evaluations]
    if any(not value for value in evaluation_ids) or len(set(evaluation_ids)) != len(evaluation_ids):
        raise EvaluationInputError("evaluation IDs must be unique and non-empty")
    evidence_ids = [item.get("evidence_id") for item in evidence]
    if any(not value for value in evidence_ids) or len(set(evidence_ids)) != len(evidence_ids):
        raise EvaluationInputError("evidence IDs must be unique and non-empty")
    evidence_by_id = {item["evidence_id"]: item for item in evidence}
    question_ids = {item.get("question_id") for item in evaluations}
    for evaluation in evaluations:
        score = evaluation.get("score")
        if not isinstance(score, (int, float)) or not 0 <= score <= 10:
            raise EvaluationInputError(f"invalid score for {evaluation.get('evaluation_id')}")
        if evaluation.get("confidence") not in CONFIDENCES:
            raise EvaluationInputError(f"invalid confidence for {evaluation.get('evaluation_id')}")
        if not evaluation.get("question_id"):
            raise EvaluationInputError("evaluation question_id is required")
        if evaluation["question_id"].startswith("CQ"):
            raise EvaluationInputError("candidate questions cannot be evaluations")
        for dimension in evaluation.get("dimensions", {}):
            if dimension not in DIMENSIONS:
                raise EvaluationInputError(f"unknown dimension: {dimension}")
        for evidence_id in evaluation.get("evidence_ids", []):
            if evidence_id not in evidence_by_id:
                raise EvaluationInputError(f"missing evidence: {evidence_id}")
            item = evidence_by_id[evidence_id]
            if item.get("question_id") not in question_ids:
                raise EvaluationInputError(f"evidence question is not evaluated: {evidence_id}")
            if item.get("response_id") in EXCLUDED_RESPONSES:
                raise EvaluationInputError(f"excluded response used as evidence: {item['response_id']}")
            if set(item.get("source", {}).get("segment_ids", ())) & EXCLUDED_SEGMENTS:
                raise EvaluationInputError(f"excluded source used as evidence: {evidence_id}")
            if not item.get("response_id") or not item.get("source", {}).get("segment_ids"):
                raise EvaluationInputError(f"untraceable evidence: {evidence_id}")
    for item in evidence:
        if not item.get("question_id") or not item.get("response_id"):
            raise EvaluationInputError(f"incomplete evidence: {item.get('evidence_id')}")


def _distribution(scores: list[float]) -> dict[str, int]:
    result = {label: 0 for label, *_ in BUCKETS}
    for score in scores:
        for label, lower, upper, final in BUCKETS:
            if lower <= score <= upper if final else lower <= score < upper:
                result[label] += 1
                break
    return result


def _aggregate_group(items: list[dict[str, Any]]) -> dict[str, Any]:
    scores = [float(item["score"]) for item in items]
    return {
        "question_count": len(items),
        "average_score": round(sum(scores) / len(scores), 2) if scores else None,
        "questions": [item["question_id"] for item in items],
        "coverage": "Evaluated" if items else "Not evaluated",
    }


def run_evaluation_engine(input_data: EvaluationInput | dict[str, Any]) -> dict[str, Any]:
    if isinstance(input_data, dict):
        input_data = EvaluationInput(
            deepcopy(input_data.get("evaluations", [])),
            deepcopy(input_data.get("evidence", [])),
            input_data.get("evaluations_source", "Individual Evaluations v2.md"),
            input_data.get("evidence_source", "Evidence Set v1.md"),
        )
    else:
        input_data = EvaluationInput(
            deepcopy(input_data.evaluations),
            deepcopy(input_data.evidence),
            input_data.evaluations_source,
            input_data.evidence_source,
        )
    _validate(input_data)
    evaluations = sorted(input_data.evaluations, key=lambda item: item["question_id"])
    evidence_by_id = {item["evidence_id"]: item for item in input_data.evidence}
    scores = [float(item["score"]) for item in evaluations]
    domains: dict[str, list[dict[str, Any]]] = {}
    complexities: dict[str, list[dict[str, Any]]] = {}
    dimensions: dict[str, list[dict[str, Any]]] = {name: [] for name in DIMENSIONS}
    for evaluation in evaluations:
        for domain in evaluation.get("domain", []):
            domains.setdefault(domain, []).append(evaluation)
        if evaluation.get("complexity"):
            complexities.setdefault(evaluation["complexity"], []).append(evaluation)
        for name, value in evaluation.get("dimensions", {}).items():
            if value.get("applicable"):
                dimensions[name].append(value)
    errors = [error for evaluation in evaluations for error in evaluation.get("errors", [])]
    strengths = []
    gaps = []
    for evaluation in evaluations:
        strengths.extend(
            {"text": text, "evaluation_ids": [evaluation["evaluation_id"]], "question_ids": [evaluation["question_id"]]}
            for text in evaluation.get("strengths", [])
        )
        gaps.extend(
            {"text": text, "evaluation_ids": [evaluation["evaluation_id"]], "question_ids": [evaluation["question_id"]]}
            for text in evaluation.get("gaps", [])
        )
    evidence_used = sorted(
        {evidence_id for evaluation in evaluations for evidence_id in evaluation["evidence_ids"]}
    )
    complexity_output = {}
    for name in ("basic", "intermediate", "advanced"):
        complexity_output[name] = _aggregate_group(complexities.get(name, []))
        complexity_output[name]["assessment"] = (
            "Not evaluated" if not complexities.get(name) else "Observed evidence is summarized from evaluated questions."
        )
    domain_output = {}
    for name in sorted(domains):
        group = _aggregate_group(domains[name])
        group["domain"] = name
        group["evidence_summary"] = sorted(
            {
                evidence_id
                for evaluation in domains[name]
                for evidence_id in evaluation["evidence_ids"]
            }
        )
        domain_output[name] = group
    dimension_output = {}
    for name, values in dimensions.items():
        dimension_output[name] = {
            "evaluated_count": len(values),
            "not_applicable_count": len(evaluations) - len(values),
            "assessments": sorted({value.get("assessment", "") for value in values}),
            "coverage": "Evaluated" if values else "Not evaluated",
        }
    warnings = []
    if len(evaluations) < 12:
        warnings.append("limited question coverage")
    if not complexities.get("advanced"):
        warnings.append("advanced complexity was not evaluated")
    if any(item["confidence"] != "high" for item in evaluations):
        warnings.append("individual evaluation confidence is not uniformly high")
    confidence = "medium" if warnings else "high"
    global_assessment = (
        f"The evaluated interview evidence shows a bounded technical pattern across "
        f"{len(evaluations)} questions, with an average score of {round(sum(scores) / len(scores), 2)}. "
        "The synthesis is limited to the domains and complexity levels actually evaluated."
    )
    traceability = {
        "evaluation_ids": [item["evaluation_id"] for item in evaluations],
        "question_ids": [item["question_id"] for item in evaluations],
        "evidence_ids": evidence_used,
        "evidence_sources": {
            evidence_id: deepcopy(evidence_by_id[evidence_id]["source"]["segment_ids"])
            for evidence_id in evidence_used
        },
        "excluded_responses_reintroduced": False,
        "candidate_questions_reintroduced": False,
        "new_evidence_created": False,
    }
    return {
        "interview_evaluation": {
            "stage": 23,
            "status": "EVALUATION_ENGINE_COMPLETE_WITH_WARNINGS" if warnings else "EVALUATION_ENGINE_COMPLETE",
            "input": {
                "evaluations_source": input_data.evaluations_source,
                "evidence_source": input_data.evidence_source,
            },
            "summary": {
                "questions_evaluated": len(evaluations),
                "average_score": round(sum(scores) / len(scores), 2),
                "median_score": float(median(scores)),
                "minimum_score": min(scores),
                "maximum_score": max(scores),
                "confidence": confidence,
            },
            "distribution": _distribution(scores),
            "domains": domain_output,
            "complexity": complexity_output,
            "dimensions": dimension_output,
            "strengths": strengths,
            "gaps": gaps,
            "errors": errors,
            "not_evaluated": [
                {"question_id": "Q8", "reason": "follow-up or continuation without independent evaluation"},
                {"question_id": "Q12", "reason": "non-evaluable"},
            ],
            "limitations": warnings,
            "global_assessment": global_assessment,
            "traceability": traceability,
            "warnings": warnings,
            "gates": {
                "stage_23": "EVALUATION_ENGINE_COMPLETE_WITH_WARNINGS" if warnings else "EVALUATION_ENGINE_COMPLETE",
                "stage_23_1": "NOT_EXECUTED",
            },
        }
    }


__all__ = [
    "EvaluationInput",
    "EvaluationInputError",
    "load_evidence_set",
    "load_individual_evaluations",
    "load_pilot_input",
    "run_evaluation_engine",
]
