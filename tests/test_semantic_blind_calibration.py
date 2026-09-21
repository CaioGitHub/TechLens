import unittest

from reference_runtime import run_pipeline
from run_semantic_blind_calibration import compare_case
from tests.calibration_cases import (
    blind_input,
    calibration_fixtures,
    calibration_oracles,
)


class SemanticBlindCalibrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = calibration_fixtures()
        cls.oracles = calibration_oracles()
        cls.results = {
            case_id: run_pipeline(blind_input(fixture))
            for case_id, fixture in cls.fixtures.items()
        }

    def test_all_cases_are_blind(self):
        for fixture in self.fixtures.values():
            runtime_input = blind_input(fixture)
            self.assertNotIn("oracle", runtime_input)
            self.assertNotIn("evaluation_specs", runtime_input)
            self.assertNotIn("evidence_specs", runtime_input)

    def test_all_oracles_compare_after_execution(self):
        for case_id, result in self.results.items():
            compare_case(case_id, result, self.oracles[case_id])

    def test_excellent_answer_has_strong_signals(self):
        types = {item["type"] for item in self.results["CAL28-01"]["artifacts"]["evidence"]["evidence_set"]}
        self.assertTrue({"reasoning", "practical", "tradeoff"} <= types)

    def test_superficial_answer_is_not_strong_in_depth(self):
        evaluation = self.results["CAL28-02"]["artifacts"]["evaluations"][0]
        self.assertEqual(evaluation["dimensions"]["depth"]["assessment"], "Weak")

    def test_incomplete_correct_answer_is_not_negative(self):
        evaluation = self.results["CAL28-03"]["artifacts"]["evaluations"][0]
        self.assertNotEqual(evaluation["dimensions"]["correctness"]["assessment"], "Weak")

    def test_technical_error_affects_correctness(self):
        evaluation = self.results["CAL28-04"]["artifacts"]["evaluations"][0]
        self.assertEqual(evaluation["dimensions"]["correctness"]["assessment"], "Weak")

    def test_partial_answer_is_not_automatically_wrong(self):
        evaluation = self.results["CAL28-05"]["artifacts"]["evaluations"][0]
        self.assertNotEqual(evaluation["dimensions"]["correctness"]["assessment"], "Weak")

    def test_reasoning_is_independent_signal(self):
        types = {item["type"] for item in self.results["CAL28-06"]["artifacts"]["evidence"]["evidence_set"]}
        self.assertIn("reasoning", types)

    def test_practical_application_is_independent_signal(self):
        types = {item["type"] for item in self.results["CAL28-07"]["artifacts"]["evidence"]["evidence_set"]}
        self.assertIn("practical", types)

    def test_tradeoff_requires_explicit_consequence(self):
        types = {item["type"] for item in self.results["CAL28-08"]["artifacts"]["evidence"]["evidence_set"]}
        self.assertIn("tradeoff", types)

    def test_declaration_is_not_demonstration(self):
        types = {item["type"] for item in self.results["CAL28-09"]["artifacts"]["evidence"]["evidence_set"]}
        self.assertIn("experience_declaration", types)
        self.assertNotIn("demonstrated_experience", types)

    def test_concrete_experience_is_demonstrated(self):
        types = {item["type"] for item in self.results["CAL28-10"]["artifacts"]["evidence"]["evidence_set"]}
        self.assertIn("demonstrated_experience", types)

    def test_self_correction_is_preserved(self):
        types = {item["type"] for item in self.results["CAL28-11"]["artifacts"]["evidence"]["evidence_set"]}
        self.assertIn("self_correction", types)

    def test_hypothesis_is_not_experience(self):
        types = {item["type"] for item in self.results["CAL28-12"]["artifacts"]["evidence"]["evidence_set"]}
        self.assertIn("hypothesis", types)
        self.assertNotIn("demonstrated_experience", types)

    def test_uncertainty_reduces_confidence_without_becoming_negative(self):
        result = self.results["CAL28-13"]
        types = {item["type"] for item in result["artifacts"]["evidence"]["evidence_set"]}
        self.assertIn("uncertainty", types)
        self.assertEqual(result["artifacts"]["evaluations"][0]["confidence"], "medium")

    def test_off_topic_is_identified(self):
        types = {item["type"] for item in self.results["CAL28-14"]["artifacts"]["evidence"]["evidence_set"]}
        self.assertIn("off_topic", types)

    def test_na_is_not_zero(self):
        dimensions = self.results["CAL28-15"]["artifacts"]["evaluations"][0]["dimensions"]
        self.assertFalse(dimensions["practical_application"]["applicable"])
        self.assertIsNone(dimensions["practical_application"]["score"])
        self.assertFalse(dimensions["trade_offs"]["applicable"])

    def test_contradiction_is_preserved(self):
        types = {item["type"] for item in self.results["CAL28-16"]["artifacts"]["evidence"]["evidence_set"]}
        self.assertIn("contradiction", types)

    def test_multiple_evidence_types_are_retained(self):
        evidence = self.results["CAL28-17"]["artifacts"]["evidence"]["evidence_set"]
        self.assertGreaterEqual(len({item["type"] for item in evidence}), 3)

    def test_short_strong_answer_has_evidence(self):
        evaluation = self.results["CAL28-18"]["artifacts"]["evaluations"][0]
        self.assertNotEqual(evaluation["dimensions"]["correctness"]["assessment"], "Weak")

    def test_verbosity_does_not_create_depth(self):
        short = self.results["CAL28-18"]["artifacts"]["evaluations"][0]
        verbose = self.results["CAL28-19"]["artifacts"]["evaluations"][0]
        self.assertLessEqual(verbose["score"], short["score"])

    def test_seniority_does_not_change_score(self):
        first = self.results["CAL28-20-A"]["artifacts"]["evaluations"][0]
        second = self.results["CAL28-20-B"]["artifacts"]["evaluations"][0]
        self.assertEqual(first["score"], second["score"])

    def test_confidence_is_not_score(self):
        for result in self.results.values():
            evaluation = result["artifacts"]["evaluations"][0]
            self.assertIn(evaluation["confidence"], {"high", "medium", "low"})
            self.assertIsInstance(evaluation["score"], float)

    def test_evidence_to_evaluation_traceability(self):
        for result in self.results.values():
            evaluation = result["artifacts"]["evaluations"][0]
            evidence_ids = {item["evidence_id"] for item in result["artifacts"]["evidence"]["evidence_set"]}
            self.assertTrue(set(evaluation["evidence_ids"]) <= evidence_ids)

    def test_evaluation_to_report_traceability(self):
        for result in self.results.values():
            self.assertEqual(
                result["artifacts"]["report"]["evaluations"],
                result["artifacts"]["evaluations"],
            )

    def test_question_response_traceability(self):
        for result in self.results.values():
            self.assertTrue(all(item["question_id"] and item["response_id"] for item in result["artifacts"]["evaluations"]))

    def test_no_oracle_reaches_evaluation(self):
        for result in self.results.values():
            for evaluation in result["artifacts"]["evaluations"]:
                self.assertNotIn("oracle", evaluation)
                self.assertNotIn("expected_score", evaluation)
                self.assertNotIn("expected_dimensions", evaluation)

    def test_runtime_uses_raw_transcript(self):
        for result in self.results.values():
            self.assertIn("raw_transcript", result["artifacts"])
            self.assertTrue(result["artifacts"]["raw_transcript"])

    def test_all_cases_complete(self):
        for result in self.results.values():
            self.assertEqual(result["status"], "COMPLETED")


if __name__ == "__main__":
    unittest.main()
