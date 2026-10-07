from __future__ import annotations

from copy import deepcopy
import re
from pathlib import Path
from typing import Any

from .interview_pipeline import run_interview_pipeline


SPEAKER_ROLES = {
    "Ingrid Mazoni": ("P-05-CANDIDATE", "candidate"),
    "Morais, Michelly Pereira de": ("P-05-INTERVIEWER-1", "interviewer"),
    "Paes, Caio Victor Pessoa de Vasconcelos": ("P-05-INTERVIEWER-2", "interviewer"),
    "Nascimento, Rodrigo Borges do": ("P-05-OBSERVER", "observer"),
}


def parse_source_transcript(path: str | Path) -> list[dict[str, str]]:
    text = Path(path).read_text(encoding="utf-8")
    block_match = re.search(r"```text\r?\n(.*?)\r?\n```", text, re.DOTALL)
    if not block_match:
        raise ValueError("source transcript code block not found")
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    header = re.compile(r"(.+?)\s+\u2014\s+(\d{2}:\d{2})$")
    for line in block_match.group(1).splitlines():
        match = header.match(line.strip())
        if match:
            if current:
                entries.append(current)
            current = {
                "speaker": match.group(1).strip(),
                "timestamp": match.group(2),
                "text": "",
            }
        elif current and line.strip():
            current["text"] = f"{current['text']} {line.strip()}".strip()
    if current:
        entries.append(current)
    if not entries:
        raise ValueError("source transcript contains no segments")
    return entries


def build_real_pilot_fixture(
    source_path: str | Path,
    *,
    fixture_id: str = "REAL-PILOT-05",
) -> dict[str, Any]:
    segments = parse_source_transcript(source_path)
    unknown = sorted({item["speaker"] for item in segments} - set(SPEAKER_ROLES))
    if unknown:
        raise ValueError(f"unmapped source speakers: {unknown}")
    participants = [
        {
            "participant_id": participant_id,
            "name": name,
            "role": role,
            "confidence": "high",
        }
        for name, (participant_id, role) in SPEAKER_ROLES.items()
    ]
    return {
        "fixture_id": fixture_id,
        "pipeline_version": "30-reference-1",
        "participants": participants,
        "raw_transcript": [
            {
                "id": f"RP05-{index:03d}",
                "timestamp": item["timestamp"],
                "speaker": item["speaker"],
                "text": item["text"],
            }
            for index, item in enumerate(segments, start=1)
        ],
    }


def run_real_pilot(source_path: str | Path) -> dict[str, Any]:
    fixture = build_real_pilot_fixture(source_path)
    return {
        "fixture": fixture,
        "pipeline": run_interview_pipeline(fixture, run_id="REAL-PILOT-05"),
    }


def _safe_participants(participants: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "participant_id": item.get("participant_id"),
            "role": item.get("role"),
            "confidence": item.get("confidence"),
            "needs_review": item.get("needs_review", False),
        }
        for item in participants
    ]


def render_derived_artifact(
    name: str,
    pipeline: dict[str, Any],
) -> str:
    artifacts = pipeline["artifacts"]
    if name == "structured":
        validation = artifacts.get("validation", {})
        body = {
            "participants": _safe_participants(artifacts.get("participants", [])),
            "questions": artifacts.get("questions", []),
            "responses": artifacts.get("responses", []),
            "links": artifacts.get("links", []),
            "validation": validation,
        }
    elif name == "evidence":
        body = artifacts.get("evidence", {})
    elif name == "evaluations":
        body = {"evaluations": artifacts.get("evaluations", [])}
    elif name == "global":
        body = {
            "stages": [
                item for item in pipeline.get("stages", [])
                if item.get("stage") in {"23", "23.1", "23.2"}
            ],
            "traceability": pipeline.get("traceability", {}),
            "readiness": pipeline.get("readiness", {}),
            "warnings": pipeline.get("warnings", []),
        }
    else:
        raise ValueError(f"unknown derived artifact: {name}")
    lines = [f"# {name.title()} — Candidato-Piloto-05", "", "```json"]
    import json
    lines.append(json.dumps(body, ensure_ascii=False, indent=2, sort_keys=True))
    lines.extend(["```", ""])
    return "\n".join(lines)


__all__ = [
    "build_real_pilot_fixture",
    "parse_source_transcript",
    "render_derived_artifact",
    "run_real_pilot",
]
