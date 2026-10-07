import copy
import hashlib
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
REPORT = PILOT / "Stage 31.1 — Human vs System Failure Analysis.md"


class Stage311FailureAnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
        cls.fixture = build_real_pilot_fixture(SOURCE)
        cls.artifacts = run_real_pilot(SOURCE)["pipeline"]["artifacts"]

    def test_priority_divergences_are_reproducible_from_source(self):
        by_question = {item["question_id"]: item for item in self.artifacts["evaluations"]}
        scores = {question_id: by_question[question_id]["score"] for question_id in ("Q1", "Q3", "Q5", "Q6", "Q9", "Q11")}
        self.assertEqual(scores["Q5"], 4.45)
        self.assertLess(scores["Q5"], 7.05)
        self.assertLess(scores["Q1"], 6.0)
        self.assertLess(scores["Q11"], 7.65)

    def test_q5_is_rest_question_with_messaging_answer(self):
        question = next(item for item in self.artifacts["questions"] if item["question_id"] == "Q5")
        response = next(item for item in self.artifacts["responses"] if item["response_id"] == "R17")
        self.assertIn("api rest", question["text"].lower())
        self.assertIn("Kafka", response["text"])
        self.assertIn("Rabbit", response["text"])
        self.assertIn("off_topic", {item["type"] for item in self.artifacts["evidence"]["evidence_set"] if item["response_id"] == "R17"})

    def test_sparse_answers_fall_back_to_positive_conceptual_evidence(self):
        evidence = {
            question_id: next(
                item for item in self.artifacts["evidence"]["evidence_set"]
                if item["question_id"] == question_id
            )
            for question_id in ("Q1", "Q3", "Q6", "Q9", "Q11")
        }
        self.assertEqual(evidence["Q1"]["qualification"], "insufficient")
        self.assertEqual(evidence["Q6"]["qualification"], "partial")
        self.assertEqual(evidence["Q11"]["type"], "experience_declaration")

    def test_dimension_and_score_overinterpretation_is_reproducible(self):
        evaluations = {
            item["question_id"]: item
            for item in self.artifacts["evaluations"]
            if item["question_id"] in {"Q1", "Q3", "Q5", "Q6", "Q9", "Q11"}
        }
        self.assertTrue(all(item["dimensions"]["correctness"]["assessment"] != "Strong" for item in evaluations.values()))
        self.assertNotEqual(evaluations["Q5"]["dimensions"]["correctness"]["score"], 9)
        self.assertNotEqual(evaluations["Q11"]["dimensions"]["reasoning"]["score"], 9)

    def test_daily_and_unknown_handling_remain_unchanged(self):
        self.assertNotIn(
            "E tem uma Daily também, só nossa, né?",
            [item["text"] for item in self.artifacts["questions"]],
        )
        unknown = {item["response_id"] for item in self.artifacts["responses"] if item["question_id"] == "unknown"}
        self.assertIn("R26", unknown)
        self.assertIn("R43", unknown)

    def test_no_source_or_pipeline_mutation_during_analysis(self):
        self.assertEqual(self.source_hash, hashlib.sha256(SOURCE.read_bytes()).hexdigest())
        repeated = run_real_pilot(SOURCE)["pipeline"]["artifacts"]
        self.assertEqual(self.artifacts["evaluations"], repeated["evaluations"])
        self.assertEqual(self.artifacts["evidence"], repeated["evidence"])

    def test_external_context_does_not_explain_divergences(self):
        baseline = self.artifacts["evaluations"]
        mutated = copy.deepcopy(self.fixture)
        mutated["job_context"] = {"title": "staff", "seniority": "staff", "company": "Other"}
        self.assertEqual(
            baseline,
            run_interview_pipeline(mutated)["artifacts"]["evaluations"],
        )

    def test_analysis_report_is_persisted_and_block_is_preserved(self):
        self.assertTrue(REPORT.exists())
        text = REPORT.read_text(encoding="utf-8")
        self.assertIn("HUMAN_VS_SYSTEM_BLOCKED", text)
        self.assertIn("HUMAN_VS_SYSTEM_FAILURE_ANALYSIS_COMPLETE_WITH_WARNINGS", text)
        for finding_id in ("FRA-001", "FRA-002", "FRA-003", "FRA-004", "FRA-005", "FRA-006"):
            self.assertIn(finding_id, text)


if __name__ == "__main__":
    unittest.main()
