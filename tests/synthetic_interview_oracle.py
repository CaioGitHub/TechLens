"""Independent behavioral oracle for the Stage 27 synthetic interview."""

from __future__ import annotations


ORACLE = {
    "participant_roles": {
        "P-CANDIDATE-27": "candidate",
        "P-INTERVIEWER-27": "interviewer",
        "P-OBSERVER-27": "observer",
    },
    "required_response_types": {
        "R8": "experience_declaration",
        "R9": "experience_with_evidence",
        "R10": "hypothetical",
        "R11": "uncertainty",
    },
    "required_evidence_qualifications": {
        "R5": "negative",
        "R8": "insufficient",
        "R9": "positive",
        "R10": "conditional",
        "R11": "insufficient",
    },
    "exclusions": {
        "candidate_question_ids": {"CQ7"},
        "missing_question_ids": {"Q4"},
        "ambiguous_segment_ids": {"RAW-26"},
        "interviewer_intervention_ids": {"RAW-06"},
    },
}


def evaluate_behavior(result: dict) -> dict[str, bool]:
    artifacts = result["artifacts"]
    participants = {
        participant["participant_id"]: participant["role"]
        for participant in artifacts["participants"]
    }
    questions = {question["question_id"] for question in artifacts["questions"]}
    responses = {
        response["response_id"]: response
        for response in artifacts["responses"]
        if response.get("response_id")
    }
    evidence = {
        item["response_id"]: item
        for item in artifacts["evidence"]["evidence_set"]
    }
    evaluations = {
        evaluation["question_id"]: evaluation
        for evaluation in artifacts["evaluations"]
    }
    attributed = {
        segment["id"]: segment
        for segment in artifacts["speaker_attributed_transcript"]
    }
    reconstructed = {
        response["response_id"]: response
        for response in artifacts["reconstructed_responses"]
        if response.get("response_id")
    }
    return {
        "participants_match_roles": all(
            participants.get(participant_id) == role
            for participant_id, role in ORACLE["participant_roles"].items()
        ),
        "candidate_question_excluded": not any(
            question_id in questions or question_id in evaluations
            for question_id in ORACLE["exclusions"]["candidate_question_ids"]
        ),
        "missing_is_not_evidence": all(
            question_id not in {
                item["question_id"]
                for item in artifacts["evidence"]["evidence_set"]
            }
            for question_id in ORACLE["exclusions"]["missing_question_ids"]
        ),
        "ambiguous_segment_needs_review": all(
            attributed[segment_id]["speaker_id"] == "unknown"
            and attributed[segment_id]["needs_review"]
            for segment_id in ORACLE["exclusions"]["ambiguous_segment_ids"]
        ),
        "intervention_is_not_candidate_response": all(
            segment_id not in response["source"]["segment_ids"]
            for segment_id in ORACLE["exclusions"]["interviewer_intervention_ids"]
            for response in responses.values()
        ),
        "response_types_match": all(
            responses[response_id]["response_type"] == response_type
            for response_id, response_type in ORACLE["required_response_types"].items()
        ),
        "evidence_qualifications_match": all(
            evidence[response_id]["qualification"] == qualification
            for response_id, qualification in ORACLE["required_evidence_qualifications"].items()
        ),
        "reconstruction_preserves_original": (
            reconstructed["R12"]["original_text"] != reconstructed["R12"]["reconstructed_text"]
            and "Spring Boto" in reconstructed["R12"]["original_text"]
            and "Spring Boot" in reconstructed["R12"]["reconstructed_text"]
        ),
        "evaluations_are_traceable": all(
            evaluation["evidence_ids"]
            and all(
                any(item["evidence_id"] == evidence_id for item in artifacts["evidence"]["evidence_set"])
                for evidence_id in evaluation["evidence_ids"]
            )
            for evaluation in artifacts["evaluations"]
        ),
        "report_consumes_evaluations": (
            artifacts["report"]["evaluations"] == artifacts["evaluations"]
        ),
    }
