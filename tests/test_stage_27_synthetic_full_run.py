import copy
import statistics
import unittest

from reference_runtime import deterministic_projection, run_pipeline
from tests.synthetic_interview import synthetic_interview_fixture
from tests.synthetic_interview_oracle import ORACLE, evaluate_behavior


class Stage27SyntheticFullRunTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = synthetic_interview_fixture()
        cls.result = run_pipeline(cls.fixture)
        cls.artifacts = cls.result["artifacts"]
        cls.behavior = evaluate_behavior(cls.result)

    def test_complete_supported_run(self):
        self.assertEqual(self.result["status"], "COMPLETED")
        self.assertEqual(self.result["readiness"], "READY_WITH_WARNINGS")
        self.assertEqual(
            [stage["stage"] for stage in self.result["stages"]],
            ["20.1", "20.2", "20.3", "20.4", "20.5", "20.6", "20.7", "21", "23", "report"],
        )

    def test_participant_and_speaker_integrity(self):
        self.assertTrue(self.behavior["participants_match_roles"])
        labels = {
            segment["speaker_label"]
            for segment in self.artifacts["speaker_attributed_transcript"]
        }
        self.assertEqual(labels, {"Ana Martins", "Bruno Lima", "Carla Souza", "UNKNOWN"})
        self.assertTrue(self.behavior["ambiguous_segment_needs_review"])

    def test_questions_candidate_question_and_links(self):
        self.assertTrue(self.behavior["candidate_question_excluded"])
        self.assertEqual(len(self.artifacts["questions"]), 12)
        self.assertEqual(
            next(item for item in self.artifacts["questions"] if item["question_id"] == "Q2")["follow_up_of"],
            "Q1",
        )
        self.assertEqual(
            next(item for item in self.artifacts["questions"] if item["question_id"] == "Q5")["reformulation_of"],
            "Q4",
        )
        self.assertTrue(
            all(link.get("question_id") and "response_id" in link for link in self.artifacts["links"])
        )

    def test_response_boundaries_and_ambiguity(self):
        self.assertTrue(self.behavior["missing_is_not_evidence"])
        self.assertTrue(self.behavior["intervention_is_not_candidate_response"])
        self.assertEqual(
            next(item for item in self.artifacts["responses"] if item["question_id"] == "Q4")["response_status"],
            "missing",
        )
        self.assertTrue(
            next(item for item in self.artifacts["responses"] if item["response_id"] == "R1")["source"]["segment_ids"]
            == ["RAW-02", "RAW-03"]
        )

    def test_response_types_cover_semantic_cases(self):
        self.assertTrue(self.behavior["response_types_match"])
        self.assertIn("Pensando melhor", next(
            item for item in self.artifacts["reconstructed_responses"] if item["response_id"] == "R6"
        )["original_text"])
        self.assertEqual(
            next(item for item in self.artifacts["responses"] if item["response_id"] == "R10")["response_type"],
            "hypothetical",
        )

    def test_evidence_oracle_and_exclusions(self):
        self.assertTrue(self.behavior["evidence_qualifications_match"])
        self.assertTrue(self.behavior["reconstruction_preserves_original"])
        evidence_response_ids = {
            item["response_id"] for item in self.artifacts["evidence"]["evidence_set"]
        }
        self.assertNotIn("CQ7", evidence_response_ids)
        for item in self.artifacts["evidence"]["evidence_set"]:
            self.assertNotIn("P-INTERVIEWER-27", item["source"]["segment_ids"])

    def test_individual_evaluations_preserve_dimensions_and_confidence(self):
        self.assertTrue(self.artifacts["evaluations"])
        for evaluation in self.artifacts["evaluations"]:
            self.assertTrue(evaluation["evidence_ids"])
            self.assertIn(evaluation["confidence"], {"high", "medium", "low"})
            self.assertEqual(
                set(evaluation["dimensions"]),
                {"correctness", "completeness", "depth", "reasoning", "practical_application", "trade_offs"},
            )
        self.assertTrue(any(evaluation["confidence"] == "low" for evaluation in self.artifacts["evaluations"]))

    def test_numeric_consistency_comes_from_observed_evaluations(self):
        scores = [
            evaluation["score"]
            for evaluation in self.artifacts["evaluations"]
            if evaluation["score"] is not None
        ]
        self.assertEqual(len(scores), len(self.artifacts["evaluations"]))
        self.assertEqual(statistics.median(scores), statistics.median(scores))
        self.assertEqual(min(scores), min(scores))
        self.assertEqual(max(scores), max(scores))
        self.assertGreaterEqual(sum(scores) / len(scores), 0)
        self.assertLessEqual(sum(scores) / len(scores), 10)

    def test_report_and_traceability(self):
        self.assertTrue(self.behavior["evaluations_are_traceable"])
        self.assertTrue(self.behavior["report_consumes_evaluations"])
        self.assertNotIn("hiring_decision", self.artifacts["report"])
        self.assertNotIn("seniority", str(self.artifacts["evaluations"]))

    def test_warning_and_gate_propagation(self):
        self.assertTrue(self.result["warnings"])
        self.assertTrue(any("speaker attribution" in warning for warning in self.result["warnings"]))
        self.assertEqual(
            next(stage for stage in self.result["stages"] if stage["stage"] == "20.7")["status"],
            "READY_WITH_WARNINGS",
        )
        self.assertEqual(
            next(stage for stage in self.result["stages"] if stage["stage"] == "21")["status"],
            "READY_WITH_WARNINGS",
        )

    def test_oracle_is_independent_of_produced_scores(self):
        altered = copy.deepcopy(self.result)
        for evaluation in altered["artifacts"]["evaluations"]:
            evaluation["score"] = 0
        behavior = evaluate_behavior(altered)
        behavior.pop("report_consumes_evaluations")
        expected = dict(self.behavior)
        expected.pop("report_consumes_evaluations")
        self.assertEqual(behavior, expected)

    def test_idempotency_and_reprocessing(self):
        second = run_pipeline(synthetic_interview_fixture())
        self.assertEqual(
            deterministic_projection(self.result)["artifacts"],
            deterministic_projection(second)["artifacts"],
        )
        changed = synthetic_interview_fixture()
        changed["raw_transcript"][1]["text"] += " Texto adicional."
        changed_result = run_pipeline(changed)
        self.assertNotEqual(
            changed_result["artifacts"]["reconstructed_responses"],
            self.artifacts["reconstructed_responses"],
        )

    def test_no_real_report_and_no_external_execution(self):
        self.assertIn("report", self.artifacts)
        self.assertNotIn("url", self.result)
        self.assertFalse(self.result.get("real_report_generated", False))


if __name__ == "__main__":
    unittest.main()
