from copy import deepcopy


def nominal_fixture():
    return {
        "fixture_id": "SYN-E2E-01",
        "participants": [
            {"participant_id": "P-INTERVIEWER", "role": "interviewer"},
            {"participant_id": "P-CANDIDATE", "role": "candidate"},
        ],
        "transcript": [
            {
                "id": "S01",
                "speaker_role": "interviewer",
                "speaker_id": "P-INTERVIEWER",
                "kind": "question",
                "question_id": "Q1",
                "text": "Como você investigaria latência em uma API?",
            },
            {
                "id": "S02",
                "speaker_role": "candidate",
                "speaker_id": "P-CANDIDATE",
                "kind": "response",
                "response_id": "R1",
                "question_id": "Q1",
                "text": "Eu mediria p95 e p99 e separaria aplicação de dependências.",
            },
            {
                "id": "S03",
                "speaker_role": "interviewer",
                "speaker_id": "P-INTERVIEWER",
                "kind": "question",
                "question_id": "Q1.1",
                "follow_up_of": "Q1",
                "text": "E se o banco fosse o suspeito?",
            },
            {
                "id": "S04",
                "speaker_role": "candidate",
                "speaker_id": "P-CANDIDATE",
                "kind": "response",
                "response_id": "R1.1",
                "question_id": "Q1.1",
                "response_type": "experience_with_evidence",
                "text": "Eu verificaria queries lentas e planos de execução.",
            },
        ],
        "evidence_specs": {
            "R1": {"evidence_id": "EVD-1", "type": "reasoning"},
            "R1.1": {
                "evidence_id": "EVD-2",
                "type": "demonstrated_experience",
                "qualification": "positive",
            },
        },
        "evaluation_specs": {
            "Q1": {"id": "EVAL-1", "score": 8.0},
            "Q1.1": {"id": "EVAL-2", "score": 8.5},
        },
    }


def fixture_with(**changes):
    fixture = nominal_fixture()
    for key, value in changes.items():
        fixture[key] = deepcopy(value)
    return fixture


def fixture_for_case(case_id):
    fixture = nominal_fixture()
    if case_id == "missing_response":
        fixture["transcript"] = fixture["transcript"][:1]
    elif case_id == "unknown_question":
        fixture["transcript"][1]["question_id"] = "Q-UNKNOWN"
    elif case_id == "ambiguous_speaker":
        fixture["transcript"][1]["ambiguous_speaker"] = True
    elif case_id == "reconstruction":
        fixture["reconstructions"] = {"R1": "Eu mediria p95 e p99 e separaria dependências."}
    elif case_id == "technical_error":
        fixture["transcript"][1]["text"] = "p95 menor significa sempre mais latência."
        fixture["evidence_specs"]["R1"]["qualification"] = "negative"
    elif case_id == "self_correction":
        fixture["transcript"][1]["text"] = "Eu usaria X. Pensando melhor, usaria Y porque."
    elif case_id == "hypothetical_answer":
        fixture["transcript"][1]["response_type"] = "hypothetical"
    elif case_id == "experience_declaration":
        fixture["transcript"][1]["response_type"] = "experience_declaration"
        fixture["evidence_specs"]["R1"] = {
            "evidence_id": "EVD-DECL",
            "type": "experience_declaration",
        }
    elif case_id == "multi_segment_response":
        fixture["transcript"][1]["text"] = "Eu mediria p95."
        fixture["transcript"][1]["response_group_id"] = "R1"
        fixture["transcript"].insert(
            2,
            {
                "id": "S02B",
                "speaker_role": "candidate",
                "speaker_id": "P-CANDIDATE",
                "kind": "response",
                "response_id": "R1B",
                "response_group_id": "R1",
                "question_id": "Q1",
                "text": "Depois separaria as dependências.",
            },
        )
    elif case_id == "candidate_question":
        fixture["transcript"].append(
            {
                "id": "S05",
                "speaker_role": "candidate",
                "speaker_id": "P-CANDIDATE",
                "kind": "question",
                "candidate_question": True,
                "question_id": "CQ1",
                "text": "Posso perguntar sobre o ambiente?",
            }
        )
    elif case_id == "needs_review":
        fixture["transcript"][1]["needs_review"] = True
    elif case_id == "ready_with_warnings":
        fixture["validation_warnings"] = ["non-central reconstruction needs review"]
    elif case_id == "blocked":
        fixture["validation_blockers"] = ["central source is invalid"]
    elif case_id == "na_dimension":
        fixture["evaluation_specs"]["Q1"]["dimensions"] = {
            "correctness": {"assessment": "Strong", "score": 8, "applicable": True},
            "completeness": {"assessment": "Adequate", "score": 7, "applicable": True},
            "depth": {"assessment": "N/A", "score": None, "applicable": False},
        }
    elif case_id == "critical_error":
        fixture["transcript"][1]["text"] = "Eu ignoraria perda de dados para ganhar velocidade."
        fixture["evidence_specs"]["R1"]["qualification"] = "negative"
    return fixture
