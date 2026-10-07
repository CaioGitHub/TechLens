import copy
import hashlib
import re
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
PILOT = ROOT / "11 - Interview Evaluation" / "09 - Real Interview Pilot" / "Candidato-Piloto-05"
HUMAN = PILOT / "Stage 31 — Human Evaluation Independent.md"
COMPARISON = PILOT / "Stage 31 — Human vs System Comparison.md"


def _system_projection():
    return run_real_pilot(SOURCE)["pipeline"]["artifacts"]


class Stage31HumanVsSystemValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
        cls.fixture = build_real_pilot_fixture(SOURCE)
        cls.system = _system_projection()
        cls.human_text = HUMAN.read_text(encoding="utf-8")
        cls.comparison_text = COMPARISON.read_text(encoding="utf-8")

    def test_human_evaluation_is_independent_and_frozen(self):
        self.assertIn("HUMAN_EVALUATION_COMPLETE", self.human_text)
        self.assertIn("H-E01", self.human_text)
        self.assertNotIn("EVD-", self.human_text)
        self.assertNotIn("EVAL-", self.human_text)
        self.assertNotIn("After Correction - Evidence Set", self.human_text)

    def test_source_and_candidate_question_integrity(self):
        self.assertEqual(self.source_hash, hashlib.sha256(SOURCE.read_bytes()).hexdigest())
        self.assertEqual(len(self.system["candidate_questions"]), 5)
        self.assertTrue(all(item["evaluation_eligible"] is False for item in self.system["candidate_questions"]))
        self.assertIn("Daily", self.human_text)
        self.assertIn("R26", self.human_text)
        self.assertIn("R43", self.human_text)

    def test_system_and_human_compare_same_evaluable_question_set(self):
        self.assertEqual(len(self.system["questions"]), 11)
        self.assertEqual(len(self.system["evaluations"]), 11)
        for question_id in [f"Q{i}" for i in range(1, 12)]:
            self.assertIn(question_id, self.comparison_text)

    def test_independent_score_metrics_are_recorded(self):
        self.assertIn("Human average: `5.09`", self.comparison_text)
        self.assertIn("System average: `6.93`", self.comparison_text)
        self.assertIn("Mean absolute difference: `2.01`", self.comparison_text)
        self.assertIn("Maximum difference: `5.05`", self.comparison_text)

    def test_material_divergence_and_system_error_classifications_are_explicit(self):
        for question_id in ("Q1", "Q3", "Q5", "Q6", "Q9", "Q10", "Q11"):
            self.assertIn(question_id, self.comparison_text)
        self.assertIn("SYSTEM_ERROR", self.comparison_text)
        self.assertIn("VALID_TECHNICAL_DISAGREEMENT", self.comparison_text)
        self.assertIn("No score, rubric, evidence model or engine was changed here.", self.comparison_text)

    def test_external_context_does_not_change_system_side_of_comparison(self):
        baseline = self.system["evaluations"]
        for context in (
            {"title": "staff engineer", "seniority": "staff", "company": "Other"},
            {"title": "junior", "seniority": "junior", "job_context": "unrelated"},
        ):
            fixture = copy.deepcopy(self.fixture)
            fixture["job_context"] = context
            changed = run_interview_pipeline(fixture)["artifacts"]["evaluations"]
            self.assertEqual(baseline, changed)

    def test_comparison_is_deterministic(self):
        repeated = _system_projection()
        self.assertEqual(self.system["evaluations"], repeated["evaluations"])
        self.assertEqual(
            hashlib.sha256(COMPARISON.read_bytes()).hexdigest(),
            hashlib.sha256(COMPARISON.read_bytes()).hexdigest(),
        )

    def test_reports_and_gate_are_persisted(self):
        self.assertTrue(HUMAN.exists())
        self.assertTrue(COMPARISON.exists())
        self.assertIn("HUMAN_EVALUATION_COMPLETE", self.human_text)
        self.assertIn("HUMAN_VS_SYSTEM_BLOCKED", self.comparison_text)


if __name__ == "__main__":
    unittest.main()
