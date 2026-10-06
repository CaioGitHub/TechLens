from __future__ import annotations

from copy import deepcopy

from tests.synthetic_interview import synthetic_interview_fixture


def stage_27_raw_fixture() -> dict:
    fixture = deepcopy(synthetic_interview_fixture())
    fixture.pop("evidence_specs", None)
    fixture.pop("evaluation_specs", None)
    fixture["fixture_id"] = "SYN-STAGE27-RAW-02"
    fixture["pipeline_version"] = "27-reference-1"
    fixture["oracle"] = {
        "source": "raw_transcript",
        "expected_participants": 3,
        "requires_unknown_speaker": True,
        "requires_candidate_question": True,
        "requires_missing_response": True,
        "requires_multisegment_response": True,
        "requires_self_correction": True,
        "requires_hypothesis": True,
        "requires_uncertainty": True,
        "requires_experience_declaration": True,
        "requires_demonstrated_experience": True,
        "requires_normalization": True,
    }
    return fixture


def stage_27_expected_contract() -> dict:
    return {
        "participant_roles": {"candidate", "interviewer", "observer"},
        "required_raw_ids": {"RAW-01", "RAW-17", "RAW-19", "RAW-26", "RAW-28"},
        "required_evidence_types": {
            "reasoning",
            "technical_error",
            "self_correction",
            "experience_declaration",
            "demonstrated_experience",
            "hypothesis",
            "uncertainty",
        },
    }


def mutate_stage_27_transcript(fixture: dict) -> dict:
    mutated = deepcopy(fixture)
    for segment in mutated["raw_transcript"]:
        if segment["id"] == "RAW-19":
            segment["text"] = (
                "Em produção configurei alertas e investiguei falhas de dependência; "
                "o resultado foi reduzir o tempo de diagnóstico."
            )
            break
    return mutated
