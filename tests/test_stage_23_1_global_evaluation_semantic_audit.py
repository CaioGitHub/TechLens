import copy
import unittest
from pathlib import Path

from reference_runtime.evaluation_engine import load_pilot_input, run_evaluation_engine
from reference_runtime.global_audit import (
    GlobalAuditError,
    audit_global_output,
    audit_input_copy,
)


ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "11 - Interview Evaluation" / "09 - Real Interview Pilot" / "Candidato-Piloto-01"


class Stage231GlobalEvaluationSemanticAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.input = load_pilot_input(
            PILOT / "Individual Evaluations v2.md",
            PILOT / "Evidence Set v1.md",
        )
        cls.runtime = run_evaluation_engine(cls.input)["interview_evaluation"]
        cls.audit = audit_global_output(cls.input, cls.runtime)

    def test_runtime_output_passes_independent_audit(self):
        self.assertEqual(self.audit["mathematical_validation"], "PASS")
        self.assertEqual(self.audit["evaluation_count"], 10)
        self.assertEqual(self.audit["evidence_count"], 28)

    def test_independent_statistics_and_distribution(self):
        self.assertEqual(self.runtime["summary"]["average_score"], 4.7)
        self.assertEqual(self.runtime["summary"]["median_score"], 4.0)
        self.assertEqual(self.runtime["summary"]["minimum_score"], 2.0)
        self.assertEqual(self.runtime["summary"]["maximum_score"], 8.0)
        self.assertEqual(
            self.runtime["distribution"],
            {"0–2": 0, "2–4": 1, "4–6": 6, "6–8": 2, "8–10": 1},
        )

    def test_distribution_boundary_rule_is_explicit(self):
        mutated = audit_input_copy(self.input)
        for score in (2.0, 4.0, 6.0, 8.0):
            mutated.evaluations[0]["score"] = score
            output = run_evaluation_engine(mutated)["interview_evaluation"]
            audit_global_output(mutated, output)
        self.assertEqual(
            run_evaluation_engine(mutated)["interview_evaluation"]["distribution"]["8–10"],
            2,
        )

    def test_individual_scores_and_q5_are_preserved(self):
        scores = {item["question_id"]: item["score"] for item in self.input.evaluations}
        self.assertEqual(
            scores,
            {
                "Q1": 2.0,
                "Q2": 6.0,
                "Q3": 4.0,
                "Q4": 8.0,
                "Q5": 4.0,
                "Q6": 4.0,
                "Q7": 7.0,
                "Q9": 4.0,
                "Q10": 4.0,
                "Q11": 4.0,
            },
        )
        q5_error = next(error for error in self.runtime["errors"] if error["question_id"] == "Q5")
        self.assertEqual(q5_error["severity"], "relevant")
        self.assertIn("E-012", q5_error["evidence_ids"])

    def test_q10_q8_q12_candidate_questions_and_excluded_responses(self):
        serialized = repr(self.runtime)
        for token in ("R31", "RAW-065", "Scroll", "R24", "R26", "R41", "R52", "CQ1", "CQ2", "CQ3", "CQ4", "CQ5", "CQ6", "CQ7"):
            self.assertNotIn(token, serialized)
        self.assertNotIn("Q8", self.runtime["traceability"]["question_ids"])
        self.assertNotIn("Q12", self.runtime["traceability"]["question_ids"])
        self.assertFalse(self.runtime["traceability"]["candidate_questions_reintroduced"])

    def test_evidence_set_is_not_extended_or_orphaned(self):
        self.assertEqual(len(self.input.evidence), 28)
        self.assertEqual(
            set(self.runtime["traceability"]["evidence_ids"]),
            {
                evidence_id
                for evaluation in self.input.evaluations
                for evidence_id in evaluation["evidence_ids"]
            },
        )
        self.assertFalse(self.runtime["traceability"]["new_evidence_created"])
        audit_global_output(self.input, self.runtime)

    def test_domains_complexity_dimensions_and_coverage_are_proportional(self):
        self.assertIn("java", self.runtime["domains"])
        self.assertNotIn("azure", self.runtime["domains"])
        self.assertEqual(self.runtime["complexity"]["advanced"]["coverage"], "Not evaluated")
        for dimension in ("correctness", "completeness", "depth", "reasoning", "practical_application", "trade_offs"):
            self.assertIn(dimension, self.runtime["dimensions"])
        self.assertIn("limited question coverage", self.runtime["limitations"])
        self.assertIn("advanced complexity was not evaluated", self.runtime["limitations"])

    def test_strengths_gaps_errors_and_global_assessment_have_support(self):
        self.assertTrue(self.runtime["strengths"])
        self.assertTrue(self.runtime["gaps"])
        self.assertTrue(self.runtime["errors"])
        for item in self.runtime["strengths"] + self.runtime["gaps"]:
            self.assertTrue(item["evaluation_ids"])
            self.assertTrue(item["question_ids"])
        self.assertIn("bounded technical pattern", self.runtime["global_assessment"])
        self.assertNotIn("senior", self.runtime["global_assessment"].lower())
        self.assertNotIn("hire", repr(self.runtime).lower())

    def test_confidence_is_bounded_and_layered(self):
        self.assertEqual(self.runtime["summary"]["confidence"], "medium")
        self.assertNotIn("speaker_attribution_confidence", repr(self.runtime))
        self.assertNotIn("reconstruction_confidence", repr(self.runtime))
        self.assertNotIn("evidence_confidence", repr(self.runtime))

    def test_traceability_reaches_source_segments(self):
        traceability = self.runtime["traceability"]
        self.assertEqual(len(traceability["evaluation_ids"]), 10)
        self.assertEqual(len(traceability["question_ids"]), 10)
        for evidence_id in traceability["evidence_ids"]:
            self.assertTrue(traceability["evidence_sources"][evidence_id])

    def test_historical_report_mutation_does_not_change_runtime_or_audit(self):
        first = (copy.deepcopy(self.runtime), copy.deepcopy(self.audit))
        historical_copy = (PILOT / "Interview Evaluation v1.md").read_text(encoding="utf-8")
        corrupted = historical_copy.replace("average_score: 4.7", "average_score: 9.9").replace(
            "confidence: medium", "confidence: high"
        )
        self.assertIn("average_score: 9.9", corrupted)
        second_input = audit_input_copy(self.input)
        second_runtime = run_evaluation_engine(second_input)["interview_evaluation"]
        second_audit = audit_global_output(second_input, second_runtime)
        self.assertEqual(first, (second_runtime, second_audit))

    def test_mutating_evaluation_changes_runtime_and_is_detectable(self):
        mutated = audit_input_copy(self.input)
        mutated.evaluations[0]["score"] = 4.0
        output = run_evaluation_engine(mutated)["interview_evaluation"]
        self.assertNotEqual(output["summary"]["average_score"], self.runtime["summary"]["average_score"])
        audit_global_output(mutated, output)

    def test_mutating_excluded_evidence_does_not_contaminate_output(self):
        mutated = audit_input_copy(self.input)
        mutated.evidence.append(
            {
                "evidence_id": "E-EXCLUDED-R31",
                "question_id": "Q10",
                "response_id": "R31",
                "type": "uncertainty",
                "qualification": "positive",
                "source": {"segment_ids": ["RAW-065"]},
            }
        )
        output = run_evaluation_engine(mutated)["interview_evaluation"]
        self.assertEqual(output, self.runtime)

    def test_audit_rejects_tampered_output(self):
        tampered = copy.deepcopy(self.runtime)
        tampered["summary"]["average_score"] = 99.0
        with self.assertRaises(GlobalAuditError):
            audit_global_output(self.input, tampered)

    def test_inputs_remain_immutable_and_no_later_stage_runs(self):
        evaluations_before = copy.deepcopy(self.input.evaluations)
        evidence_before = copy.deepcopy(self.input.evidence)
        run_evaluation_engine(self.input)
        self.assertEqual(self.input.evaluations, evaluations_before)
        self.assertEqual(self.input.evidence, evidence_before)
        self.assertEqual(self.runtime["gates"]["stage_23_1"], "NOT_EXECUTED")

    def test_responsibility_boundaries(self):
        serialized = repr(self.runtime).lower()
        for forbidden in ("job_context", "linkedin", "curriculum", "hiring", "ranking", "seniority"):
            self.assertNotIn(forbidden, serialized)
        self.assertNotIn("Interview Evaluation v1.md", self.runtime["input"]["evaluations_source"])


if __name__ == "__main__":
    unittest.main()
