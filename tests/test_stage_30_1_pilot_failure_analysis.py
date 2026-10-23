import copy
import unittest
from pathlib import Path

from reference_runtime import build_real_pilot_fixture, run_interview_pipeline, run_real_pilot


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
        # Same-version metamorphic oracle: an already excluded conversational
        # question must not affect technical evidence or scores. Historical
        # Stage 30 counts/scores remain in its reports, not runtime targets.
        fixture = build_real_pilot_fixture(SOURCE)
        without_context = copy.deepcopy(fixture)
        conversational_text = "E tem uma Daily também, só nossa, né?"
        removed = [r for r in fixture["raw_transcript"] if r["text"] == conversational_text]
        self.assertEqual(len(removed), 1)
        without_context["raw_transcript"] = [
            r for r in without_context["raw_transcript"] if r["text"] != conversational_text
        ]
        control = run_interview_pipeline(without_context)["artifacts"]
        for key in ("questions", "responses", "evidence", "evaluations"):
            self.assertEqual(self.artifacts[key], control[key], key)
        removed_ids = {r["id"] for r in removed}
        for item in control["evidence"]["evidence_set"]:
            self.assertTrue(removed_ids.isdisjoint(item["source"]["segment_ids"]))

    def test_reexecution_is_deterministic(self):
        repeated = run_real_pilot(SOURCE)["pipeline"]["artifacts"]
        for key in ("questions", "responses", "evidence", "evaluations"):
            self.assertEqual(self.artifacts[key], repeated[key])


if __name__ == "__main__":
    unittest.main()
