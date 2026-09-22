import re
import unittest
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_SET = (
    ROOT
    / "11 - Interview Evaluation"
    / "09 - Real Interview Pilot"
    / "Candidato-Piloto-01"
    / "Evidence Set v1.md"
)
STRUCTURED_INTERVIEW = (
    ROOT
    / "11 - Interview Evaluation"
    / "09 - Real Interview Pilot"
    / "Candidato-Piloto-01"
    / "Structured Interview - Controlled Correction v6.md"
)


class Stage21RealPilotEvidenceSetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidence_text = EVIDENCE_SET.read_text(encoding="utf-8")
        cls.structured_text = STRUCTURED_INTERVIEW.read_text(encoding="utf-8")
        cls.responses = {}
        for block in re.findall(r"```json\s*(.*?)\s*```", cls.structured_text, re.DOTALL):
            try:
                record = json.loads(block)
            except json.JSONDecodeError:
                continue
            if isinstance(record, dict) and "response_id" in record:
                cls.responses[record["response_id"]] = record
        start = cls.evidence_text.index("## Evidence items")
        end = cls.evidence_text.index("## Excluded material")
        cls.evidence_block = cls.evidence_text[start:end]

    def test_evidence_ids_are_unique_and_stable(self):
        evidence_ids = re.findall(r"^\s+- evidence_id: (E-\d+)$", self.evidence_block, re.MULTILINE)
        self.assertEqual(len(evidence_ids), 28)
        self.assertEqual(len(evidence_ids), len(set(evidence_ids)))
        self.assertEqual(evidence_ids, [f"E-{index:03d}" for index in range(1, 29)])

    def test_evidence_has_required_traceability_and_classification_fields(self):
        records = re.split(r"(?=^\s+- evidence_id: )", self.evidence_block, flags=re.MULTILINE)
        records = [record for record in records if "evidence_id:" in record]
        self.assertEqual(len(records), 28)
        required_fields = (
            "question_id:",
            "response_id:",
            "type:",
            "qualification:",
            "content:",
            "interpretation:",
            "explicitness:",
            "evidence_strength:",
            "evidence_confidence:",
            "source:",
            "segment_ids:",
            "relations:",
        )
        for record in records:
            for field in required_fields:
                self.assertIn(field, record, record.splitlines()[0])

    def test_sources_exist_in_structured_interview(self):
        source_ids = set(re.findall(r"\bRAW-\d{3}\b", self.structured_text))
        evidence_source_ids = set(re.findall(r"\bRAW-\d{3}\b", self.evidence_block))
        self.assertTrue(evidence_source_ids)
        self.assertTrue(evidence_source_ids <= source_ids)

    def test_evidence_references_only_eligible_candidate_responses(self):
        records = re.split(r"(?=^\s+- evidence_id: )", self.evidence_block, flags=re.MULTILINE)
        records = [record for record in records if "evidence_id:" in record]
        for record in records:
            response_id = re.search(r"^\s+response_id: (R\d+)$", record, re.MULTILINE).group(1)
            response = self.responses[response_id]
            self.assertTrue(response.get("evaluation_eligible"), response_id)
            self.assertEqual(response.get("speaker_id"), "candidate", response_id)
            source_ids = set(re.findall(r"\bRAW-\d{3}\b", record))
            response_source_ids = set(response["source"]["segment_ids"])
            self.assertTrue(source_ids <= response_source_ids, response_id)

    def test_excluded_material_never_receives_evidence(self):
        forbidden_ids = ("R24", "R26", "R41", "R52", "R42", "CQ1", "CQ2", "CQ3", "CQ4", "CQ5", "CQ6", "CQ7")
        for identifier in forbidden_ids:
            self.assertNotRegex(self.evidence_block, rf"response_id: {identifier}\b")

    def test_no_score_or_evaluation_fields_are_present(self):
        forbidden_fields = (
            "score:",
            "average:",
            "ranking:",
            "seniority:",
            "hiring_decision:",
            "recommendation:",
        )
        for field in forbidden_fields:
            self.assertNotIn(field, self.evidence_block)

    def test_output_gate_and_upstream_warnings_are_preserved(self):
        self.assertIn("status: COMPLETE_WITH_WARNINGS", self.evidence_text)
        self.assertIn("source_validation_status: READY_WITH_WARNINGS", self.evidence_text)
        self.assertIn("EVIDENCE_MODEL_COMPLETE_WITH_WARNINGS", self.evidence_text)
        for warning_id in ("W-001", "W-002", "W-003", "W-004"):
            self.assertIn(f"id: {warning_id}", self.evidence_text)


if __name__ == "__main__":
    unittest.main()
