import unittest

from reference_runtime import run_pipeline


PARTICIPANTS = [
    {"participant_id": "P-CANDIDATE", "name": "Synthetic Candidate", "role": "candidate"},
    {"participant_id": "P-INTERVIEWER", "name": "Synthetic Interviewer", "role": "interviewer"},
]


def _fixture(transcript, fixture_id="STAGE30-1"):
    return {
        "fixture_id": fixture_id,
        "pipeline_version": "30.1-reference-1",
        "participants": PARTICIPANTS,
        "raw_transcript": [
            {
                "id": f"{fixture_id}-{index:02d}",
                "timestamp": f"12:00:{index:02d}",
                **item,
            }
            for index, item in enumerate(transcript, start=1)
        ],
    }


class Stage30FailureAnalysisTests(unittest.TestCase):
    def test_conversational_prompt_is_preserved_but_not_extracted(self):
        result = run_pipeline(
            _fixture(
                [
                    {"speaker": "Synthetic Interviewer", "text": "Como investigaria a falha?"},
                    {"speaker": "Synthetic Candidate", "text": "Eu começaria pelos logs."},
                    {"speaker": "Synthetic Interviewer", "text": "Você tem alguma dúvida?"},
                    {"speaker": "Synthetic Candidate", "text": "Não."},
                ],
                "STAGE30-1-CONVERSATION",
            )
        )
        questions = result["artifacts"]["questions"]
        self.assertEqual(len(questions), 1)
        self.assertEqual(result["artifacts"]["candidate_questions"], [])
        self.assertIn("conversational prompts", " ".join(result["warnings"]))

    def test_interviewer_explanation_is_not_a_question_or_candidate_evidence(self):
        result = run_pipeline(
            _fixture(
                [
                    {"speaker": "Synthetic Interviewer", "text": "Como investigaria a falha?"},
                    {"speaker": "Synthetic Interviewer", "text": "Nós normalmente começamos pelo Application Insights porque o cliente exige rastreabilidade e comunicação rápida."},
                    {"speaker": "Synthetic Candidate", "text": "Sim."},
                ],
                "STAGE30-1-INTERVIEWER-CONTENT",
            )
        )
        self.assertEqual(len(result["artifacts"]["questions"]), 1)
        evidence = result["artifacts"]["evidence"]["evidence_set"]
        self.assertTrue(all("STAGE30-1-INTERVIEWER-CONTENT-02" not in item["source"]["segment_ids"] for item in evidence))

    def test_candidate_question_is_preserved_and_does_not_contaminate_linking(self):
        result = run_pipeline(
            _fixture(
                [
                    {"speaker": "Synthetic Interviewer", "text": "Como investigaria a falha?"},
                    {"speaker": "Synthetic Candidate", "text": "Eu começaria pelos logs."},
                    {"speaker": "Synthetic Candidate", "text": "Como funciona a equipe de suporte?"},
                    {"speaker": "Synthetic Interviewer", "text": "A equipe acompanha tickets diariamente."},
                ],
                "STAGE30-1-CANDIDATE-QUESTION",
            )
        )
        self.assertEqual(len(result["artifacts"]["questions"]), 1)
        self.assertEqual(len(result["artifacts"]["candidate_questions"]), 1)
        self.assertEqual(result["artifacts"]["candidate_questions"][0]["question_id"], "CQ1")
        self.assertTrue(all(item["question_id"] != "CQ1" for item in result["artifacts"]["evaluations"]))

    def test_substantive_interviewer_intervention_closes_previous_response(self):
        result = run_pipeline(
            _fixture(
                [
                    {"speaker": "Synthetic Interviewer", "text": "Você já usou observabilidade?"},
                    {"speaker": "Synthetic Candidate", "text": "Sim, usei uma ferramenta."},
                    {"speaker": "Synthetic Interviewer", "text": "Aqui nós usamos métricas e traces em todos os projetos e compartilhamos os incidentes com várias equipes."},
                    {"speaker": "Synthetic Candidate", "text": "Não, nunca configurei isso."},
                ],
                "STAGE30-1-BOUNDARY",
            )
        )
        responses = [item for item in result["artifacts"]["responses"] if item["response_status"] != "missing"]
        self.assertEqual(responses[0]["question_id"], "Q1")
        self.assertEqual(responses[1]["question_id"], "unknown")
        self.assertTrue(responses[1]["needs_review"])

    def test_ambiguous_term_is_not_silently_normalized(self):
        result = run_pipeline(
            _fixture(
                [
                    {"speaker": "Synthetic Interviewer", "text": "Qual tecnologia você usou?"},
                    {"speaker": "Synthetic Candidate", "text": "Usei uma ferramenta com nome incerto."},
                ],
                "STAGE30-1-AMBIGUITY",
            )
        )
        response = result["artifacts"]["reconstructed_responses"][0]
        self.assertEqual(response["original_text"], response["reconstructed_text"])

    def test_same_input_is_idempotent(self):
        fixture = _fixture(
            [
                {"speaker": "Synthetic Interviewer", "text": "Como investigaria a falha?"},
                {"speaker": "Synthetic Candidate", "text": "Eu começaria pelos logs."},
                {"speaker": "Synthetic Candidate", "text": "Posso fazer uma pergunta?"},
            ],
            "STAGE30-1-IDEMPOTENCY",
        )
        first = run_pipeline(fixture)
        second = run_pipeline(fixture)
        self.assertEqual(first["artifacts"]["questions"], second["artifacts"]["questions"])
        self.assertEqual(first["artifacts"]["responses"], second["artifacts"]["responses"])
        self.assertEqual(first["artifacts"]["validation"], second["artifacts"]["validation"])


if __name__ == "__main__":
    unittest.main()
