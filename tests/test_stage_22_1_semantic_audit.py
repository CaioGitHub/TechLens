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
EVIDENCE_SET = PILOT / "Evidence Set v1.md"
V1 = PILOT / "Individual Evaluations v1.md"
V2 = PILOT / "Individual Evaluations v2.md"
AUDIT = PILOT / "Stage 22.1 — Individual Evaluations Semantic Audit.md"


class Stage221SemanticAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidence_text = EVIDENCE_SET.read_text(encoding="utf-8")
        cls.v1_text = V1.read_text(encoding="utf-8")
        cls.v2_text = V2.read_text(encoding="utf-8")
        cls.audit_text = AUDIT.read_text(encoding="utf-8")
        start = cls.evidence_text.index("## Evidence items")
        end = cls.evidence_text.index("## Excluded material")
        evidence_block = cls.evidence_text[start:end]
        cls.evidence_ids = set(re.findall(r"^\s+- evidence_id: (E-\d+)$", evidence_block, re.MULTILINE))
        cls.evidence_questions = {
            evidence_id: question_id
            for evidence_id, question_id in re.findall(
                r"- evidence_id: (E-\d+)\s+question_id: (Q\d+)",
                evidence_block,
                re.DOTALL,
            )
        }
        cls.v2_blocks = re.split(r"(?=^## EV-Q\d+ — Q\d+$)", cls.v2_text, flags=re.MULTILINE)
        cls.v2_blocks = [block for block in cls.v2_blocks if block.startswith("## EV-Q")]

    def test_audit_covers_exactly_ten_questions(self):
        expected = ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q9", "Q10", "Q11")
        audited = tuple(re.findall(r"^### (Q\d+)$", self.audit_text, re.MULTILINE))
        self.assertEqual(audited, expected)
        self.assertEqual(len(self.v2_blocks), 10)

    def test_q8_and_q12_have_no_independent_evaluation(self):
        self.assertNotRegex(self.v2_text, re.compile(r"^## EV-Q8\b", re.MULTILINE))
        self.assertNotRegex(self.v2_text, re.compile(r"^## EV-Q12\b", re.MULTILINE))
        self.assertIn("Q8", self.audit_text)
        self.assertIn("Q12", self.audit_text)
        self.assertIn("Q8 has no score and no independent weight.", self.audit_text)

    def test_excluded_responses_and_candidate_questions_do_not_contaminate_v2(self):
        evaluation_body = self.v2_text.split("## Excluded", 1)[0]
        for identifier in ("R24", "R26", "R41", "R52", "CQ1", "CQ2", "CQ3", "CQ4", "CQ5", "CQ6", "CQ7"):
            self.assertNotRegex(evaluation_body, re.compile(rf"^\s+id: \[{identifier}(?:,|\])", re.MULTILINE))
        q10 = next(block for block in self.v2_blocks if block.startswith("## EV-Q10"))
        self.assertNotIn("RAW-065", q10)
        self.assertNotRegex(q10, re.compile(r"^\s+id: \[R27, R29, R31\]$", re.MULTILINE))
        self.assertIn("R31", self.v2_text.split("## Excluded", 1)[1])
        self.assertIn("R31/RAW-065", self.audit_text)

    def test_all_final_evidence_ids_exist_and_belong_to_the_question(self):
        for block in self.v2_blocks:
            question_id = re.search(r"^\s+question:\n\s+id: (Q\d+)$", block, re.MULTILINE).group(1)
            used = set(re.findall(r"\bE-\d{3}\b", block))
            self.assertTrue(used)
            self.assertTrue(used <= self.evidence_ids, question_id)
            self.assertTrue(
                all(self.evidence_questions[evidence_id] == question_id for evidence_id in used),
                question_id,
            )

    def test_scores_findings_rationales_and_canonical_fields_exist(self):
        for block in self.v2_blocks:
            self.assertRegex(block, re.compile(r"^\s+id: EV-Q\d+$", re.MULTILINE))
            self.assertRegex(block, re.compile(r"^\s+response:\n\s+id: \[R\d+(?:, R\d+)*\]$", re.MULTILINE))
            self.assertIn("dimensions:", block)
            self.assertRegex(block, re.compile(r"^\s+score:\n\s+value: (?:[0-9]|10)(?:\.0)?$", re.MULTILINE))
            self.assertRegex(block, re.compile(r"^\s+findings:\n", re.MULTILINE))
            self.assertRegex(block, re.compile(r"^\s+rationale: .+$", re.MULTILINE))
            self.assertRegex(block, re.compile(r"^\s+confidence: (high|medium|low)$", re.MULTILINE))

    def test_na_is_not_zero_and_normalized_weights_are_present(self):
        for block in self.v2_blocks:
            self.assertIn("weights:", block)
            self.assertIn("normalized:", block)
            self.assertIn('assessment: "N/A"', block)
            self.assertNotRegex(block, re.compile(r"assessment: \"N/A\"\s+evidence: \[[^\]]+\]"))

    def test_no_global_evaluation_or_prohibited_context_exists(self):
        for prohibited in (
            "average_score:",
            "overall_score:",
            "ranking:",
            "seniority_score:",
            "hiring_recommendation:",
            "job_fit:",
        ):
            self.assertNotRegex(self.v2_text, re.compile(rf"^\s*{re.escape(prohibited)}", re.MULTILINE))
        self.assertIn("global_score: not_created", self.v2_text)
        self.assertIn("global_average: not_created", self.v2_text)
        self.assertIn("No global score", self.audit_text)

    def test_q5_context_mismatch_is_explicit_and_relevant_not_central(self):
        q5 = next(block for block in self.v2_blocks if block.startswith("## EV-Q5"))
        self.assertIn("type: relevant", q5)
        self.assertIn("severity: relevant", q5)
        self.assertNotIn("type: central", q5)
        self.assertIn("context mismatch", self.audit_text)
        self.assertIn("partial messaging knowledge", self.audit_text)

    def test_experience_declarations_are_not_promoted_to_demonstrated_experience(self):
        for question_id in ("Q2", "Q9", "Q11"):
            block = next(block for block in self.v2_blocks if block.startswith(f"## EV-{question_id}"))
            self.assertIn("decl", block.lower())
        self.assertIn("Declared experience is not promoted automatically", self.audit_text)

    def test_related_knowledge_does_not_introduce_candidate_evidence(self):
        for block in self.v2_blocks:
            related = block.split("related_knowledge:", 1)[1].split("```", 1)[0]
            self.assertEqual(related.strip(), "[]")
        self.assertIn("related_knowledge", self.v2_text)

    def test_audit_decision_and_gate_are_persisted(self):
        self.assertIn("`Individual Evaluations v1.md` was preserved unchanged.", self.audit_text)
        self.assertIn("`Individual Evaluations v2.md` was created", self.audit_text)
        self.assertIn("STAGE_22_1_COMPLETE_WITH_WARNINGS", self.audit_text)
        self.assertIn("Stage 23", self.audit_text)
        self.assertIn("No global score, average", self.audit_text)

    def test_audit_invariants_and_idempotency_are_pass(self):
        self.assertIn("## Invariance", self.audit_text)
        self.assertIn("```text\nPASS\n```", self.audit_text)
        self.assertIn("## Idempotency", self.audit_text)
        self.assertIn("Re-running the deterministic audit", self.audit_text)


if __name__ == "__main__":
    unittest.main()
