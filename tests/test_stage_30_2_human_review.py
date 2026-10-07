import hashlib
import unittest
from pathlib import Path

from reference_runtime import run_real_pilot


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT
    / "11 - Interview Evaluation"
    / "09 - Real Interview Pilot"
    / "Candidato-Piloto-01"
    / "Pilot Input - Source Transcript v3.md"
)


class Stage302HumanReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
        cls.pipeline = run_real_pilot(SOURCE)["pipeline"]
        cls.artifacts = cls.pipeline["artifacts"]

    def test_participants_and_critical_speakers_are_identified(self):
        roles = {item["role"] for item in self.artifacts["participants"]}
        self.assertEqual(roles, {"candidate", "interviewer", "observer"})
        self.assertEqual(
            next(item for item in self.artifacts["participants"] if item["role"] == "candidate")[
                "participant_id"
            ],
            "P-05-CANDIDATE",
        )
        self.assertTrue(all(item["speaker_id"] == "candidate" for item in self.artifacts["responses"]))
        self.assertTrue(
            all(
                item["source"]["segment_ids"]
                for item in self.artifacts["responses"]
                if item["question_id"] != "unknown"
            )
        )

    def test_questions_are_faithful_and_conversational_prompt_is_excluded(self):
        questions = self.artifacts["questions"]
        self.assertEqual(len(questions), 11)
        self.assertNotIn(
            "E tem uma Daily também, só nossa, né?",
            [item["text"] for item in questions],
        )
        self.assertTrue(any("observabilidade" in item["text"] for item in questions))
        self.assertTrue(any("JDBC" in item["text"] for item in questions))

    def test_candidate_questions_are_preserved_outside_evaluation(self):
        candidate_questions = self.artifacts["candidate_questions"]
        self.assertEqual(len(candidate_questions), 5)
        self.assertTrue(all(item["evaluation_eligible"] is False for item in candidate_questions))
        self.assertTrue(all(item["question_id"].startswith("CQ") for item in candidate_questions))
        evaluated_questions = {item["question_id"] for item in self.artifacts["evaluations"]}
        self.assertTrue(
            evaluated_questions.isdisjoint(item["question_id"] for item in candidate_questions)
        )

    def test_unknown_links_are_conservative(self):
        unknown = [
            item for item in self.artifacts["responses"]
            if item["question_id"] == "unknown"
        ]
        self.assertGreater(len(unknown), 0)
        self.assertTrue(all(item["needs_review"] for item in unknown))
        self.assertTrue(
            all(
                link["relation_type"] == "unlinked"
                for link in self.artifacts["links"]
                if link["response_id"] in {item["response_id"] for item in unknown}
            )
        )

    def test_reconstruction_does_not_change_transcript_meaning(self):
        reconstructed = self.artifacts["reconstructed_responses"]
        self.assertEqual(len(reconstructed), len(self.artifacts["responses"]))
        self.assertTrue(
            all(item["original_text"] == item["reconstructed_text"] for item in reconstructed)
        )

    def test_every_evidence_item_is_supported_and_traceable(self):
        responses = {item["response_id"]: item for item in self.artifacts["responses"]}
        questions = {item["question_id"]: item for item in self.artifacts["questions"]}
        segment_ids = {
            item["id"] for item in self.artifacts["speaker_attributed_transcript"]
        }
        for evidence in self.artifacts["evidence"]["evidence_set"]:
            response = responses[evidence["response_id"]]
            self.assertEqual(evidence["question_id"], response["question_id"])
            self.assertIn(evidence["question_id"], questions)
            self.assertIn(evidence["content"], response["text"])
            self.assertTrue(set(evidence["source"]["segment_ids"]) <= segment_ids)

    def test_individual_scores_are_supported_by_linked_evidence(self):
        evidence = {
            item["evidence_id"]: item
            for item in self.artifacts["evidence"]["evidence_set"]
        }
        for evaluation in self.artifacts["evaluations"]:
            self.assertIn(evaluation["confidence"], {"high", "medium"})
            self.assertTrue(evaluation["evidence_ids"])
            for evidence_id in evaluation["evidence_ids"]:
                item = evidence[evidence_id]
                self.assertEqual(item["question_id"], evaluation["question_id"])
                self.assertEqual(item["response_id"], evaluation["response_id"])

    def test_no_external_context_contaminates_evaluation(self):
        serialized = repr(self.artifacts["evaluations"]).lower()
        for forbidden in (
            "currículo",
            "senioridade",
            "salário",
            "contratar",
            "aprovado",
            "reprovado",
        ):
            self.assertNotIn(forbidden, serialized)

    def test_approval_review_is_deterministic_and_does_not_change_scores(self):
        repeated = run_real_pilot(SOURCE)["pipeline"]["artifacts"]
        self.assertEqual(
            [item["score"] for item in self.artifacts["evaluations"]],
            [item["score"] for item in repeated["evaluations"]],
        )
        self.assertEqual(self.artifacts["questions"], repeated["questions"])
        self.assertEqual(self.artifacts["evidence"], repeated["evidence"])

    def test_original_transcript_is_unchanged(self):
        self.assertEqual(self.source_hash, hashlib.sha256(SOURCE.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
