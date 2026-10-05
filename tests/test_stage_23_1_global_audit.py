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
AUDIT = PILOT / "Stage 23.1 — Global Evaluation Semantic Audit.md"
EVIDENCE_SET = PILOT / "Evidence Set v1.md"


class Stage231GlobalAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.individuals = INDIVIDUALS.read_text(encoding="utf-8")
        cls.report = REPORT.read_text(encoding="utf-8")
        cls.audit = AUDIT.read_text(encoding="utf-8")
        cls.evidence = EVIDENCE_SET.read_text(encoding="utf-8")

    def test_ten_individual_evaluations_are_the_source(self):
        expected = ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q9", "Q10", "Q11")
        actual = tuple(re.findall(r"^## EV-(Q\d+) — Q\d+$", self.individuals, re.MULTILINE))
        self.assertEqual(actual, expected)
        self.assertIn("evaluation_source: Individual Evaluations v2.md", self.report)
        self.assertIn("source_evaluation: Individual Evaluations v2.md", self.report)

    def test_statistics_and_distribution_are_correct(self):
        scores = [2.0, 6.0, 4.0, 8.0, 4.0, 4.0, 7.0, 4.0, 4.0, 4.0]
        self.assertEqual(len(scores), 10)
        self.assertEqual(sum(scores), 47.0)
        self.assertAlmostEqual(sum(scores) / len(scores), 4.7)
        self.assertEqual(sorted(scores)[4:6], [4.0, 4.0])
        self.assertIn("average: 4.7", self.audit)
        self.assertIn("median: 4.0", self.audit)
        self.assertIn("minimum: 2.0", self.audit)
        self.assertIn("maximum: 8.0", self.audit)
        for row in ("| 0–2 | 0 |", "| 2–4 | 1 |", "| 4–6 | 6 |", "| 6–8 | 2 |", "| 8–10 | 1 |"):
            self.assertIn(row, self.report)

    def test_q8_q12_and_excluded_material_are_not_reintroduced(self):
        self.assertIn("Q8 was a follow-up of Q7", self.report)
        self.assertIn("Q12 was non-evaluable", self.report)
        for forbidden in ("R31", "R24", "R26", "R41", "R52", "CQ1", "CQ2", "CQ3", "CQ4", "CQ5", "CQ6", "CQ7"):
            self.assertNotIn(forbidden, self.report)
        self.assertIn("Q8_independent_evaluation: false", self.audit)
        self.assertIn("Q12_evaluation: false", self.audit)

    def test_q5_and_q10_audited_interpretations_are_preserved(self):
        self.assertIn("Q5 is specifically a context mismatch", self.report)
        self.assertIn("general conceptual ignorance", self.audit)
        self.assertIn("Q10 uses only E-023–E-026", self.audit)
        self.assertIn("R31_reintroduced: false", self.audit)

    def test_domain_complexity_and_dimension_audits_have_proportional_language(self):
        for section in ("## Domain audit", "## Complexity audit", "## Dimension audit", "## Coverage and limitations"):
            self.assertIn(section, self.audit)
        for phrase in ("limited", "not evaluated", "partial", "one question"):
            self.assertIn(phrase, self.audit.lower())
        self.assertIn("Advanced | None", self.audit)
        self.assertIn("do not establish broad mastery", self.report)

    def test_strengths_gaps_and_errors_are_traceable(self):
        for section in ("## Strengths", "## Gaps", "## Relevant errors"):
            self.assertIn(section, self.report)
        for evidence_id in ("E-011", "E-017", "E-020", "E-002", "E-008", "E-023", "E-026", "E-012", "E-016"):
            self.assertIn(evidence_id, self.report)
        self.assertIn("severity: relevant", self.report)
        self.assertIn("No critical error", self.report)
        self.assertIn("No ERROR or CRITICAL finding", self.audit)

    def test_confidence_is_global_qualitative_not_arithmetic_average(self):
        self.assertIn("level: medium", self.report)
        self.assertIn("Global confidence is an independent qualitative judgment", self.report)
        self.assertIn("not the arithmetic mean", self.report)
        self.assertIn("## Confidence audit", self.audit)

    def test_no_new_evidence_or_prohibited_decisions(self):
        known_evidence = set(re.findall(r"^\s+- evidence_id: (E-\d+)$", self.evidence, re.MULTILINE))
        report_evidence = set(re.findall(r"\bE-\d{3}\b", self.report))
        self.assertTrue(report_evidence <= known_evidence)
        self.assertIn("external_information_used: false", self.report)
        self.assertIn("job_context_used: false", self.report)
        self.assertIn("seniority_evaluated: false", self.report)
        self.assertIn("hiring_decision_created: false", self.report)
        self.assertIn("ranking_created: false", self.report)
        self.assertFalse((PILOT / "Interview Evaluation v2.md").exists())

    def test_language_and_traceability_are_explicit(self):
        self.assertIn("## Language and proportionality", self.audit)
        self.assertIn("## Traceability", self.audit)
        self.assertIn("every_conclusion_has_question_and_evidence: true", self.report)
        self.assertIn("↓\nEvidence item\n↓\nSource segment", self.report)
        self.assertIn("bounded technical synthesis", self.report)

    def test_findings_have_ids_and_decisions(self):
        findings = re.findall(r"^\s+- id: (GA-\d+)$", self.audit, re.MULTILINE)
        self.assertEqual(findings, ["GA-001", "GA-002", "GA-003"])
        self.assertEqual(len(re.findall(r"^\s+decision:", self.audit, re.MULTILINE)), 3)
        self.assertIn("## Corrections", self.audit)
        self.assertIn("None.", self.audit)

    def test_audit_gate_and_idempotency(self):
        self.assertIn("## Idempotency", self.audit)
        self.assertIn("PASS", self.audit)
        self.assertIn("GLOBAL_EVALUATION_AUDIT_COMPLETE_WITH_WARNINGS", self.audit)
        self.assertIn("Stage 24 and all later stages remain outside this task.", self.audit)


if __name__ == "__main__":
    unittest.main()
