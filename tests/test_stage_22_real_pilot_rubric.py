import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_SET = (
    ROOT
    / "11 - Interview Evaluation"
    / "09 - Real Interview Pilot"
    / "Candidato-Piloto-01"
    / "Evidence Set v1.md"
)
EVALUATIONS = (
    ROOT
    / "11 - Interview Evaluation"
    / "09 - Real Interview Pilot"
    / "Candidato-Piloto-01"
    / "Individual Evaluations v1.md"
)


class Stage22RealPilotRubricTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidence_text = EVIDENCE_SET.read_text(encoding="utf-8")
        cls.evaluations_text = EVALUATIONS.read_text(encoding="utf-8")
        evidence_start = cls.evidence_text.index("## Evidence items")
        evidence_end = cls.evidence_text.index("## Excluded material")
        cls.evidence_block = cls.evidence_text[evidence_start:evidence_end]
        cls.evidence_ids = set(re.findall(r"^\s+- evidence_id: (E-\d+)$", cls.evidence_block, re.MULTILINE))
        cls.evaluation_blocks = re.split(
            r"(?=^## EV-Q\d+ — Q\d+$)", cls.evaluations_text, flags=re.MULTILINE
        )
        cls.evaluation_blocks = [
            block for block in cls.evaluation_blocks if block.startswith("## EV-Q")
        ]

    def test_exactly_the_ten_eligible_questions_are_evaluated(self):
        question_ids = re.findall(r"^## EV-(Q\d+) — (Q\d+)$", self.evaluations_text, re.MULTILINE)
        self.assertEqual(len(question_ids), 10)
        self.assertEqual([question for _, question in question_ids], [
            "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q9", "Q10", "Q11"
        ])
        self.assertEqual(
            re.findall(r"^\s+id: (EV-Q\d+)$", self.evaluations_text, re.MULTILINE),
            [f"EV-{question}" for question in ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q9", "Q10", "Q11")],
        )

    def test_every_evaluation_has_question_response_and_evidence_traceability(self):
        for block in self.evaluation_blocks:
            self.assertRegex(block, re.compile(r"^\s+id: EV-Q\d+$", re.MULTILINE), block.splitlines()[0])
            self.assertRegex(block, re.compile(r"^\s+question:\n\s+id: Q\d+$", re.MULTILINE))
            self.assertRegex(block, re.compile(r"^\s+response:\n\s+id: \[R\d+(?:, R\d+)*\]$", re.MULTILINE))
            evidence_ids = re.findall(r"\bE-\d{3}\b", block)
            self.assertTrue(evidence_ids, block.splitlines()[0])
            self.assertTrue(set(evidence_ids) <= self.evidence_ids, block.splitlines()[0])

    def test_all_evidence_items_are_used_once_by_the_question_map(self):
        used = set()
        for block in self.evaluation_blocks:
            used.update(re.findall(r"\bE-\d{3}\b", block))
        self.assertEqual(used, self.evidence_ids)

    def test_excluded_material_is_not_evaluated(self):
        evaluation_body = self.evaluations_text.split("## Excluded", 1)[0]
        self.assertNotRegex(evaluation_body, re.compile(r"^## EV-Q8\b", re.MULTILINE))
        self.assertNotRegex(evaluation_body, re.compile(r"^## EV-Q12\b", re.MULTILINE))
        for identifier in ("R24", "R26", "R41", "R52", "CQ1", "CQ2", "CQ3", "CQ4", "CQ5", "CQ6", "CQ7"):
            self.assertNotRegex(
                evaluation_body,
                re.compile(rf"^\s+id: \[{identifier}\]", re.MULTILINE),
            )
        self.assertIn("independent_evaluation: false", self.evaluations_text)

    def test_dimensions_and_na_weights_are_normalized(self):
        for block in self.evaluation_blocks:
            self.assertIn("weights:\n", block)
            self.assertIn("original:", block)
            self.assertIn("normalized:", block)
            applicable = re.findall(
                r"^\s{4}(\w+):\n\s{6}applicable: true$", block, re.MULTILINE
            )
            for dimension in applicable:
                self.assertRegex(
                    block,
                    re.compile(rf"normalized: .*{dimension}: (?!null)[0-9.]+"),
                    block.splitlines()[0],
                )

    def test_scores_have_rationale_and_valid_range(self):
        for block in self.evaluation_blocks:
            score = float(re.search(r"^\s+value: ([0-9]+(?:\.[0-9])?)$", block, re.MULTILINE).group(1))
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 10.0)
            self.assertRegex(block, re.compile(r"^\s+rationale: .+$", re.MULTILINE))

    def test_errors_are_classified_and_traceable(self):
        error_blocks = re.findall(
            r"      - type: (peripheral|relevant|central|critical)\n"
            r"        severity: (peripheral|relevant|central|critical)\n"
            r"        evidence_id: (E-\d{3})",
            self.evaluations_text,
        )
        for error_type, severity, evidence_id in error_blocks:
            self.assertEqual(error_type, severity)
            self.assertIn(evidence_id, self.evidence_ids)

    def test_confidence_is_separate_and_no_global_scoring_exists(self):
        for block in self.evaluation_blocks:
            self.assertRegex(block, re.compile(r"^\s+confidence: (high|medium|low)$", re.MULTILINE))
            self.assertIn("score:", block)
        self.assertIn("global_score: not_created", self.evaluations_text)
        self.assertIn("overall_average: not_created", self.evaluations_text)
        self.assertNotRegex(self.evaluations_text, re.compile(r"^\s+overall_(?:score|assessment):", re.MULTILINE))
        self.assertNotRegex(self.evaluations_text, re.compile(r"^\s+ranking:", re.MULTILINE))
        self.assertNotRegex(self.evaluations_text, re.compile(r"^\s+hiring_decision:", re.MULTILINE))

    def test_q8_is_not_an_independent_evaluation(self):
        self.assertNotRegex(self.evaluations_text, re.compile(r"^## EV-Q8\b", re.MULTILINE))
        self.assertRegex(
            self.evaluations_text,
            r"- id: Q8\s+reason: follow_up_or_continuation_of_Q7\s+independent_evaluation: false",
        )

    def test_idempotency_marker_and_gate_are_present(self):
        self.assertIn("idempotency: PASS", self.evaluations_text)
        self.assertIn("traceability: PASS", self.evaluations_text)
        self.assertIn("no_invention: PASS", self.evaluations_text)
        self.assertIn("RUBRIC_COMPLETE_WITH_WARNINGS", self.evaluations_text)
        self.assertIn("Stage 23 — Evaluation Engine was not executed.", self.evaluations_text)


if __name__ == "__main__":
    unittest.main()
