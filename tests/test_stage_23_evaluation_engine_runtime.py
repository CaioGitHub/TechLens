import copy
import re
import unittest
from pathlib import Path

from reference_runtime.evaluation_engine import (
    EvaluationInput,
    EvaluationInputError,
    load_pilot_input,
    run_evaluation_engine,
)


ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "11 - Interview Evaluation" / "09 - Real Interview Pilot" / "Candidato-Piloto-01"
EVALUATIONS_PATH = PILOT / "Individual Evaluations v2.md"
EVIDENCE_PATH = PILOT / "Evidence Set v1.md"
HISTORICAL_PATH = PILOT / "Interview Evaluation v1.md"


class Stage23EvaluationEngineRuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.input = load_pilot_input(EVALUATIONS_PATH, EVIDENCE_PATH)
        cls.output = run_evaluation_engine(cls.input)["interview_evaluation"]
        cls.evaluation_text_before = EVALUATIONS_PATH.read_text(encoding="utf-8")
        cls.evidence_text_before = EVIDENCE_PATH.read_text(encoding="utf-8")

    def test_loads_valid_input_and_calculates_statistics(self):
        summary = self.output["summary"]
        self.assertEqual(summary["questions_evaluated"], 10)
        self.assertEqual(summary["average_score"], 4.7)
        self.assertEqual(summary["median_score"], 4.0)
        self.assertEqual(summary["minimum_score"], 2.0)
        self.assertEqual(summary["maximum_score"], 8.0)

    def test_distribution_uses_explicit_half_open_buckets(self):
        self.assertEqual(
            self.output["distribution"],
            {"0–2": 0, "2–4": 1, "4–6": 6, "6–8": 2, "8–10": 1},
        )

    def test_q8_q12_and_candidate_questions_are_not_evaluations(self):
        questions = self.output["traceability"]["question_ids"]
        self.assertNotIn("Q8", questions)
        self.assertNotIn("Q12", questions)
        self.assertFalse(any(question.startswith("CQ") for question in questions))
        self.assertEqual(
            {item["question_id"] for item in self.output["not_evaluated"]},
            {"Q8", "Q12"},
        )

    def test_excluded_responses_and_q10_scroll_are_not_reintroduced(self):
        serialized = repr(self.output)
        for token in ("R24", "R26", "R41", "R52", "R31", "RAW-065", "Scroll"):
            self.assertNotIn(token, serialized)

    def test_q5_error_is_consumed_from_input(self):
        errors = [error for error in self.output["errors"] if error["question_id"] == "Q5"]
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["severity"], "relevant")

    def test_domains_complexity_dimensions_and_not_evaluated_coverage(self):
        self.assertIn("java", self.output["domains"])
        self.assertEqual(self.output["domains"]["java"]["question_count"], 2)
        self.assertGreater(self.output["complexity"]["basic"]["question_count"], 0)
        self.assertGreater(self.output["complexity"]["intermediate"]["question_count"], 0)
        self.assertEqual(self.output["complexity"]["advanced"]["coverage"], "Not evaluated")
        self.assertIn("correctness", self.output["dimensions"])
        self.assertGreater(self.output["dimensions"]["correctness"]["evaluated_count"], 0)

    def test_strengths_gaps_errors_limitations_and_global_assessment_are_derived(self):
        self.assertTrue(self.output["strengths"])
        self.assertTrue(self.output["gaps"])
        self.assertTrue(self.output["errors"])
        self.assertIn("limited question coverage", self.output["limitations"])
        self.assertIn("bounded technical pattern", self.output["global_assessment"])
        self.assertEqual(self.output["summary"]["confidence"], "medium")

    def test_traceability_is_explicit_and_no_new_evidence_is_created(self):
        traceability = self.output["traceability"]
        self.assertEqual(len(traceability["evaluation_ids"]), 10)
        self.assertEqual(len(traceability["question_ids"]), 10)
        self.assertEqual(len(traceability["evidence_ids"]), 28)
        self.assertFalse(traceability["new_evidence_created"])
        for evidence_id in traceability["evidence_ids"]:
            self.assertTrue(traceability["evidence_sources"][evidence_id])

    def test_idempotency_and_input_immutability(self):
        first = run_evaluation_engine(self.input)
        second = run_evaluation_engine(self.input)
        self.assertEqual(first, second)
        self.assertEqual(EVALUATIONS_PATH.read_text(encoding="utf-8"), self.evaluation_text_before)
        self.assertEqual(EVIDENCE_PATH.read_text(encoding="utf-8"), self.evidence_text_before)

    def test_reordering_evaluations_preserves_semantics(self):
        reordered = copy.deepcopy(self.input)
        reordered.evaluations.reverse()
        self.assertEqual(run_evaluation_engine(reordered), run_evaluation_engine(self.input))

    def test_renaming_ids_consistently_preserves_numeric_semantics(self):
        renamed = copy.deepcopy(self.input)
        evaluation_map = {}
        evidence_map = {}
        for index, evidence in enumerate(renamed.evidence, start=1):
            old = evidence["evidence_id"]
            evidence_map[old] = f"X-{index:03d}"
            evidence["evidence_id"] = evidence_map[old]
        for index, evaluation in enumerate(renamed.evaluations, start=1):
            old = evaluation["evaluation_id"]
            evaluation_map[old] = f"Y-{index:02d}"
            evaluation["evaluation_id"] = evaluation_map[old]
            evaluation["evidence_ids"] = [evidence_map[item] for item in evaluation["evidence_ids"]]
            for dimension in evaluation["dimensions"].values():
                dimension["evidence_ids"] = [
                    evidence_map[item] for item in dimension["evidence_ids"]
                ]
        result = run_evaluation_engine(renamed)["interview_evaluation"]
        self.assertEqual(result["summary"], self.output["summary"])
        self.assertEqual(result["distribution"], self.output["distribution"])

    def test_descriptive_text_and_external_metadata_do_not_change_numbers(self):
        altered = copy.deepcopy(self.input)
        altered.evaluations[0]["description"] = "Senior candidate with extensive CV"
        altered.evaluations[0]["external_cv"] = {"years": 15, "title": "Senior"}
        result = run_evaluation_engine(altered)["interview_evaluation"]
        self.assertEqual(result["summary"], self.output["summary"])

    def test_historical_report_is_not_used_as_input(self):
        historical = HISTORICAL_PATH.read_text(encoding="utf-8")
        corrupted = re.sub(r"average_score: 4\.7", "average_score: 99.0", historical)
        corrupted = re.sub(r"median_score: 4\.0", "median_score: 99.0", corrupted)
        self.assertIn("average_score: 99.0", corrupted)
        self.assertEqual(run_evaluation_engine(self.input)["interview_evaluation"]["summary"]["average_score"], 4.7)

    def test_changed_evaluation_changes_aggregate(self):
        changed = copy.deepcopy(self.input)
        changed.evaluations[0]["score"] = 4.0
        self.assertNotEqual(
            run_evaluation_engine(changed)["interview_evaluation"]["summary"]["average_score"],
            self.output["summary"]["average_score"],
        )

    def test_q5_severity_change_is_reflected_without_hardcoding(self):
        changed = copy.deepcopy(self.input)
        changed.evaluations[4]["errors"][0]["severity"] = "central"
        errors = run_evaluation_engine(changed)["interview_evaluation"]["errors"]
        self.assertEqual(next(error for error in errors if error["question_id"] == "Q5")["severity"], "central")

    def test_na_dimensions_are_not_counted_as_zero(self):
        changed = copy.deepcopy(self.input)
        changed.evaluations[1]["dimensions"]["depth"]["applicable"] = False
        changed.evaluations[1]["dimensions"]["depth"]["assessment"] = "N/A"
        result = run_evaluation_engine(changed)["interview_evaluation"]
        self.assertEqual(result["dimensions"]["depth"]["evaluated_count"], 4)
        self.assertGreater(result["dimensions"]["depth"]["not_applicable_count"], 0)

    def test_rejects_duplicate_evaluations_and_invalid_scores(self):
        duplicate = copy.deepcopy(self.input)
        duplicate.evaluations.append(copy.deepcopy(duplicate.evaluations[0]))
        with self.assertRaises(EvaluationInputError):
            run_evaluation_engine(duplicate)
        invalid = copy.deepcopy(self.input)
        invalid.evaluations[0]["score"] = 11
        with self.assertRaises(EvaluationInputError):
            run_evaluation_engine(invalid)

    def test_rejects_missing_evidence_and_candidate_question_evaluation(self):
        missing = copy.deepcopy(self.input)
        missing.evaluations[0]["evidence_ids"] = ["E-MISSING"]
        with self.assertRaises(EvaluationInputError):
            run_evaluation_engine(missing)
        candidate_question = copy.deepcopy(self.input)
        candidate_question.evaluations[0]["question_id"] = "CQ1"
        with self.assertRaises(EvaluationInputError):
            run_evaluation_engine(candidate_question)

    def test_output_does_not_execute_later_stages(self):
        self.assertEqual(self.output["gates"]["stage_23_1"], "NOT_EXECUTED")
        self.assertNotIn("report", self.output)
        self.assertNotIn("hiring", repr(self.output).lower())
        self.assertNotIn("seniority", repr(self.output).lower())


if __name__ == "__main__":
    unittest.main()
