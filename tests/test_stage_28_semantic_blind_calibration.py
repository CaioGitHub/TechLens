from __future__ import annotations

import hashlib
import unittest
from copy import deepcopy
from pathlib import Path

from reference_runtime import (
    blind_input,
    compare_calibration,
    run_blind_calibration,
)
from tests.calibration_cases import calibration_fixtures, calibration_oracles


ROOT = Path(__file__).resolve().parents[1]


class Stage28SemanticBlindCalibrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = calibration_fixtures()
        cls.references = calibration_oracles()
        cls.results = run_blind_calibration(cls.fixtures)
        cls.report = compare_calibration(cls.results, cls.references)["calibration"]

    def test_minimum_diverse_case_count(self):
        self.assertGreaterEqual(self.report["total_cases"], 15)
        self.assertEqual(self.report["fail"], 0)

    def test_engine_input_is_blind(self):
        for fixture in self.fixtures.values():
            runtime_input = blind_input(fixture)
            for forbidden in ("oracle", "expected_score", "expected_score_range", "evidence_specs", "evaluation_specs"):
                self.assertNotIn(forbidden, runtime_input)

    def test_reference_is_not_in_system_output(self):
        for result in self.results.values():
            serialized = repr(result)
            self.assertNotIn("expected_score_range", serialized)
            self.assertNotIn("expected_dimensions", serialized)
            self.assertNotIn("expected_assessment", serialized)

    def test_experience_declaration_and_demonstration_differ(self):
        declaration = self.results["CAL28-09"]["artifacts"]["evaluations"][0]
        demonstrated = self.results["CAL28-10"]["artifacts"]["evaluations"][0]
        declaration_types = {
            item["type"]
            for item in self.results["CAL28-09"]["artifacts"]["evidence"]["evidence_set"]
        }
        demonstrated_types = {
            item["type"]
            for item in self.results["CAL28-10"]["artifacts"]["evidence"]["evidence_set"]
        }
        self.assertIn("experience_declaration", declaration_types)
        self.assertNotIn("demonstrated_experience", declaration_types)
        self.assertIn("demonstrated_experience", demonstrated_types)
        self.assertNotEqual(declaration["score"], demonstrated["score"])

    def test_semantic_dimensions_are_compared_separately(self):
        dimensions = self.report["dimension_alignment"]
        for name in ("correctness", "completeness", "depth", "reasoning", "practical_application", "trade_offs"):
            self.assertIn(name, dimensions)
            self.assertEqual(dimensions[name]["fail"], 0)

    def test_confidence_is_separate_from_extraction_confidence(self):
        result = self.results["CAL28-13"]
        evaluation = result["artifacts"]["evaluations"][0]
        evidence = result["artifacts"]["evidence"]["evidence_set"]
        self.assertEqual(evaluation["confidence"], "medium")
        self.assertTrue(all("evidence_confidence" in item for item in evidence))

    def test_short_and_long_equivalent_content_does_not_reward_length(self):
        short = self.results["CAL28-18"]["artifacts"]["evaluations"][0]
        verbose = self.results["CAL28-19"]["artifacts"]["evaluations"][0]
        self.assertLessEqual(verbose["score"], short["score"])

    def test_seniority_cv_and_title_metadata_do_not_change_result(self):
        base = deepcopy(self.fixtures["CAL28-20-A"])
        variants = []
        for seniority, years, title in (
            ("Junior", 5, "Software Engineer"),
            ("Pleno", 10, "Tech Lead"),
            ("Senior", 15, "Architect"),
            ("Principal", 20, "Consultant"),
        ):
            variant = deepcopy(base)
            variant["seniority"] = seniority
            variant["cv"] = {"years": years}
            variant["title"] = title
            variants.append(variant)
        results = run_blind_calibration({str(index): item for index, item in enumerate(variants)})
        scores = {result["artifacts"]["evaluations"][0]["score"] for result in results.values()}
        self.assertEqual(len(scores), 1)

    def test_reference_mutation_changes_only_comparator(self):
        baseline = compare_calibration(self.results, self.references)["calibration"]
        mutated = deepcopy(self.references)
        mutated["CAL28-01"]["score_range"] = (0.0, 1.0)
        changed = compare_calibration(self.results, mutated)["calibration"]
        self.assertEqual(
            self.results["CAL28-01"]["artifacts"]["evaluations"],
            run_blind_calibration({"CAL28-01": self.fixtures["CAL28-01"]})["CAL28-01"]["artifacts"]["evaluations"],
        )
        self.assertNotEqual(baseline["cases"], changed["cases"])

    def test_input_evidence_mutation_changes_engine_output(self):
        original = run_blind_calibration({"CAL28-10": self.fixtures["CAL28-10"]})["CAL28-10"]
        mutated_fixture = deepcopy(self.fixtures["CAL28-10"])
        mutated_fixture["raw_transcript"][1]["text"] = "Apenas ouvi falar de Azure Monitor."
        changed = run_blind_calibration({"CAL28-10": mutated_fixture})["CAL28-10"]
        self.assertNotEqual(
            original["artifacts"]["evaluations"],
            changed["artifacts"]["evaluations"],
        )

    def test_reproducibility(self):
        repeated = run_blind_calibration(self.fixtures)
        for case_id in self.results:
            self.assertEqual(
                self.results[case_id]["artifacts"]["evaluations"],
                repeated[case_id]["artifacts"]["evaluations"],
            )
            self.assertEqual(
                self.results[case_id]["artifacts"]["evidence"],
                repeated[case_id]["artifacts"]["evidence"],
            )

    def test_traceability_is_preserved(self):
        for result in self.results.values():
            evidence = result["artifacts"]["evidence"]["evidence_set"]
            evidence_ids = {item["evidence_id"] for item in evidence}
            for evaluation in result["artifacts"]["evaluations"]:
                self.assertTrue(set(evaluation["evidence_ids"]) <= evidence_ids)
                self.assertTrue(evaluation["question_id"])
                self.assertTrue(evaluation["response_id"])

    def test_na_is_not_zero(self):
        evaluation = self.results["CAL28-15"]["artifacts"]["evaluations"][0]
        self.assertFalse(evaluation["dimensions"]["practical_application"]["applicable"])
        self.assertIsNone(evaluation["dimensions"]["practical_application"]["score"])
        self.assertFalse(evaluation["dimensions"]["trade_offs"]["applicable"])

    def test_errors_uncertainty_contradiction_and_correction_are_distinct(self):
        cases = {
            "CAL28-04": "technical_error",
            "CAL28-11": "self_correction",
            "CAL28-13": "uncertainty",
            "CAL28-16": "contradiction",
        }
        for case_id, evidence_type in cases.items():
            types = {
                item["type"]
                for item in self.results[case_id]["artifacts"]["evidence"]["evidence_set"]
            }
            self.assertIn(evidence_type, types)

    def test_protected_repository_artifacts_are_not_modified(self):
        protected = list((ROOT / "11 - Interview Evaluation").rglob("Scoring Rubric.md"))
        before = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in protected}
        run_blind_calibration(self.fixtures)
        after = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in protected}
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
