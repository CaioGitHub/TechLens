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


class Stage301PilotFailureAnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pipeline = run_real_pilot(SOURCE)["pipeline"]
        cls.artifacts = cls.pipeline["artifacts"]

    def test_p101_real_contextual_tag_question_is_not_evaluable(self):
        questions = self.artifacts["questions"]
        self.assertNotIn(
            "E tem uma Daily também, só nossa, né?",
            [question["text"] for question in questions],
        )
        self.assertEqual(len(questions), 11)

    def test_valid_technical_questions_remain_evaluable(self):
        texts = [question["text"] for question in self.artifacts["questions"]]
        self.assertTrue(any("observabilidade" in text for text in texts))
        self.assertTrue(any("JDBC" in text for text in texts))

    def test_p102_unknowns_are_conservative_and_have_no_orphan_evidence(self):
        unknown = {
            response["response_id"]
            for response in self.artifacts["responses"]
            if response["question_id"] == "unknown"
        }
        self.assertIn("R26", unknown)
        self.assertIn("R43", unknown)
        evidence = self.artifacts["evidence"]["evidence_set"]
        self.assertFalse(
            any(item["response_id"] in {"R26", "R43"} for item in evidence)
        )

    def test_traceability_remains_transcript_based(self):
        segment_ids = {
            item["id"] for item in self.artifacts["speaker_attributed_transcript"]
        }
        evidence_by_id = {
            item["evidence_id"]: item
            for item in self.artifacts["evidence"]["evidence_set"]
        }
        for evaluation in self.artifacts["evaluations"]:
            for evidence_id in evaluation["evidence_ids"]:
                self.assertIn(evidence_id, evidence_by_id)
                self.assertTrue(
                    set(evidence_by_id[evidence_id]["source"]["segment_ids"])
                    <= segment_ids
                )

    def test_before_after_impact_is_limited_to_removed_context_question(self):
        baseline = {
            "questions": 12,
            "responses": 47,
            "evidence": 25,
            "evaluations": 12,
            "scores": [4.0, 7.05, 4.0, 7.05, 4.45, 5.85, 6.0, 7.05, 4.0, 7.65, 4.0, 6.0],
        }
        current_scores = [item["score"] for item in self.artifacts["evaluations"]]
        self.assertEqual(len(self.artifacts["responses"]), baseline["responses"])
        self.assertEqual(len(self.artifacts["questions"]), baseline["questions"] - 1)
        self.assertEqual(
            len(self.artifacts["evidence"]["evidence_set"]),
            baseline["evidence"] - 1,
        )
        self.assertEqual(len(self.artifacts["evaluations"]), baseline["evaluations"] - 1)
        self.assertEqual(current_scores, baseline["scores"][:-1])

    def test_reexecution_is_deterministic(self):
        repeated = run_real_pilot(SOURCE)["pipeline"]["artifacts"]
        for key in ("questions", "responses", "evidence", "evaluations"):
            self.assertEqual(self.artifacts[key], repeated[key])


if __name__ == "__main__":
    unittest.main()
