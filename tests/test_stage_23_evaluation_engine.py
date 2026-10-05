import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PILOT = (
    ROOT
    / "11 - Interview Evaluation"
    / "09 - Real Interview Pilot"
    / "Candidato-Piloto-01"
)
INDIVIDUALS = PILOT / "Individual Evaluations v2.md"
REPORT = PILOT / "Interview Evaluation v1.md"
EVIDENCE_SET = PILOT / "Evidence Set v1.md"


class Stage23EvaluationEngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.individuals = INDIVIDUALS.read_text(encoding="utf-8")
        cls.report = REPORT.read_text(encoding="utf-8")
        cls.evidence_set = EVIDENCE_SET.read_text(encoding="utf-8")
        cls.blocks = re.split(r"(?=^## EV-Q\d+ — Q\d+$)", cls.individuals, flags=re.MULTILINE)
        cls.blocks = [block for block in cls.blocks if block.startswith("## EV-Q")]

    def test_loads_exactly_ten_valid_individual_evaluations(self):
        expected = ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q9", "Q10", "Q11")
        question_ids = tuple(re.findall(r"^## EV-(Q\d+) — Q\d+$", self.individuals, re.MULTILINE))
        self.assertEqual(question_ids, expected)
        self.assertEqual(len(self.blocks), 10)
        for question_id in expected:
            self.assertIn(f"EV-{question_id}", self.report)

    def test_official_scores_are_unchanged(self):
        expected_scores = {
            "Q1": 2.0, "Q2": 6.0, "Q3": 4.0, "Q4": 8.0, "Q5": 4.0,
            "Q6": 4.0, "Q7": 7.0, "Q9": 4.0, "Q10": 4.0, "Q11": 4.0,
        }
        actual = {
            question_id: float(score)
            for question_id, score in re.findall(
                r"^## EV-(Q\d+) — Q\d+.*?^\s+value: ([0-9]+(?:\.[0-9])?)$",
                self.individuals,
                re.MULTILINE | re.DOTALL,
            )
        }
        self.assertEqual(actual, expected_scores)

    def test_statistics_are_correct(self):
        scores = [2.0, 6.0, 4.0, 8.0, 4.0, 4.0, 7.0, 4.0, 4.0, 4.0]
        self.assertAlmostEqual(sum(scores) / len(scores), 4.7)
        self.assertEqual(sorted(scores)[len(scores) // 2 - 1:len(scores) // 2 + 1], [4.0, 4.0])
        self.assertIn("Average score | 4.7 / 10", self.report)
        self.assertIn("Median | 4.0 / 10", self.report)
        self.assertIn("Minimum | 2.0 / 10", self.report)
        self.assertIn("Maximum | 8.0 / 10", self.report)

    def test_distribution_is_correct_and_explicit(self):
        expected_rows = (
            "| 0–2 | 0 |",
            "| 2–4 | 1 |",
            "| 4–6 | 6 |",
            "| 6–8 | 2 |",
            "| 8–10 | 1 |",
        )
        for row in expected_rows:
            self.assertIn(row, self.report)
        self.assertIn("lower-inclusive and upper-exclusive", self.report)

    def test_q8_q12_and_excluded_material_are_not_reintroduced(self):
        self.assertNotRegex(self.report, re.compile(r"^## EV-Q8\b", re.MULTILINE))
        self.assertNotRegex(self.report, re.compile(r"^## EV-Q12\b", re.MULTILINE))
        for forbidden in ("R31", "R24", "R26", "R41", "R52", "CQ1", "CQ2", "CQ3", "CQ4", "CQ5", "CQ6", "CQ7"):
            self.assertNotIn(forbidden, self.report)
        self.assertIn("Q8 was a follow-up of Q7", self.report)
        self.assertIn("Q12 was non-evaluable", self.report)

    def test_q5_and_q10_keep_audited_interpretations(self):
        self.assertIn("Q5", self.report)
        self.assertIn("context mismatch", self.report)
        self.assertIn("does not establish general absence of knowledge", self.report)
        self.assertIn("Q10", self.report)
        self.assertIn("logs, prints and local debugging", self.report)
        self.assertNotIn("Scroll", self.report)

    def test_no_new_evidence_or_external_context_is_used(self):
        evidence_ids = set(re.findall(r"\bE-\d{3}\b", self.report))
        known_ids = set(re.findall(r"^\s+- evidence_id: (E-\d+)$", self.evidence_set, re.MULTILINE))
        self.assertTrue(evidence_ids <= known_ids)
        for forbidden in ("CV", "LinkedIn", "Job Context", "cargo", "senioridade declarada"):
            self.assertNotIn(forbidden, self.report)
        self.assertIn("job_context_used: false", self.report)
        self.assertIn("external candidate information", self.report)

    def test_required_consolidation_sections_and_traceability_exist(self):
        for heading in (
            "## Summary",
            "## Indicators",
            "## Score distribution",
            "## Performance by domain",
            "## Performance by complexity",
            "## Dimensions observed",
            "## Strengths",
            "## Gaps",
            "## Relevant errors",
            "## Areas not evaluated",
            "## Global technical assessment",
            "## Limitations",
            "## Confidence",
            "## Traceability",
        ):
            self.assertIn(heading, self.report)
        self.assertIn("every_conclusion_has_question_and_evidence: true", self.report)
        self.assertIn("excluded_evidence_reintroduced: false", self.report)
        self.assertIn("new_evidence_created: false", self.report)

    def test_global_confidence_is_independent_and_no_prohibited_decisions_exist(self):
        self.assertIn("confidence: medium", self.report)
        self.assertIn("Global confidence is an independent qualitative judgment", self.report)
        for prohibited in (
            "seniority_score:",
            "hiring_recommendation:",
            "ranking:",
            "job_fit:",
            "approved",
            "rejected",
            "hire",
        ):
            self.assertNotRegex(self.report, re.compile(rf"^\s*{re.escape(prohibited)}", re.MULTILINE | re.IGNORECASE))
        self.assertIn("seniority_evaluated: false", self.report)
        self.assertIn("hiring_decision_created: false", self.report)
        self.assertIn("ranking_created: false", self.report)

    def test_exactly_one_consolidated_interview_evaluation_and_gate(self):
        self.assertEqual(self.report.count("# Interview Evaluation v1"), 1)
        self.assertIn("EVALUATION_ENGINE_COMPLETE_WITH_WARNINGS", self.report)
        self.assertIn("stage_24_executed: false", self.report)
        self.assertIn("final_report_generated: false", self.report)

    def test_idempotency_marker_and_input_source_are_present(self):
        self.assertIn("evaluation_source: Individual Evaluations v2.md", self.report)
        self.assertIn("source_evaluation: Individual Evaluations v2.md", self.report)
        self.assertIn("valid_evaluations: [EV-Q1, EV-Q2, EV-Q3, EV-Q4, EV-Q5, EV-Q6, EV-Q7, EV-Q9, EV-Q10, EV-Q11]", self.report)
        self.assertIn("This is a technical consolidation of the ten valid individual evaluations.", self.report)


if __name__ == "__main__":
    unittest.main()
