import hashlib
import tempfile
import unittest
from pathlib import Path

from reference_runtime.materialization import materialize_interview_evaluation_v2


ROOT = Path(__file__).resolve().parents[1]
PILOT = (
    ROOT
    / "11 - Interview Evaluation"
    / "09 - Real Interview Pilot"
    / "Candidato-Piloto-01"
)


class Stage232InterviewEvaluationMaterializationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evaluations = PILOT / "Individual Evaluations v2.md"
        cls.evidence = PILOT / "Evidence Set v1.md"
        cls.v1 = PILOT / "Interview Evaluation v1.md"
        cls.protected = [
            cls.evaluations,
            cls.evidence,
            PILOT / "Structured Interview - Controlled Correction v6.md",
            ROOT / "11 - Interview Evaluation" / "04 - Rubrics" / "Scoring Rubric.md",
            ROOT / "11 - Interview Evaluation" / "08 - Evidence Model" / "21 - Evidence Model.md",
            ROOT / "11 - Interview Evaluation" / "01 - Evaluation Framework" / "Evaluation Engine.md",
            PILOT / "Stage 23.1 — Global Evaluation Semantic Audit.md",
            cls.v1,
        ]

    @staticmethod
    def _hash(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def test_materialized_values_match_runtime_and_audit(self):
        with tempfile.TemporaryDirectory() as directory:
            result = materialize_interview_evaluation_v2(
                self.evaluations,
                self.evidence,
                Path(directory) / "Interview Evaluation v2.md",
            )
            output = result["runtime"]
            content = result["content"]

        self.assertEqual(result["gate"], "INTERVIEW_EVALUATION_V2_MATERIALIZED_WITH_WARNINGS")
        self.assertEqual(result["audit"]["mathematical_validation"], "PASS")
        self.assertEqual(output["summary"]["questions_evaluated"], 10)
        self.assertEqual(output["summary"]["average_score"], 4.7)
        self.assertEqual(output["summary"]["median_score"], 4.0)
        self.assertEqual(output["summary"]["minimum_score"], 2.0)
        self.assertEqual(output["summary"]["maximum_score"], 8.0)
        self.assertEqual(
            output["distribution"],
            {"0–2": 0, "2–4": 1, "4–6": 6, "6–8": 2, "8–10": 1},
        )
        self.assertIn("Perguntas avaliadas: 10", content)
        self.assertIn("Média: 4.7 / 10", content)
        self.assertIn("Mediana: 4.0 / 10", content)
        self.assertIn("Confiança global: Média", content)
        self.assertIn("Evidências utilizadas: 28", content)
        self.assertIn("Q5: severidade `relevant`", content)

    def test_exclusions_and_traceability_are_materialized(self):
        with tempfile.TemporaryDirectory() as directory:
            result = materialize_interview_evaluation_v2(
                self.evaluations,
                self.evidence,
                Path(directory) / "Interview Evaluation v2.md",
            )
        content = result["content"]
        self.assertFalse(result["audit"]["q8_independent_evaluation"])
        self.assertFalse(result["audit"]["q12_evaluation"])
        self.assertFalse(result["audit"]["candidate_questions_reintroduced"])
        self.assertIn("Q8", content)
        self.assertIn("Q12", content)
        self.assertIn("CQ1–CQ7", content)
        self.assertIn("R31 / \"Scroll.\"", content)
        self.assertIn("E-028", content)
        self.assertIn("RAW-070", content)
        self.assertNotIn("9.9", content)
        self.assertIn("INTERVIEW_EVALUATION_V2_MATERIALIZED_WITH_WARNINGS", content)

    def test_historical_report_mutation_does_not_change_materialization(self):
        with tempfile.TemporaryDirectory() as directory:
            historical_copy = Path(directory) / "Interview Evaluation v1.md"
            historical_copy.write_text(
                self.v1.read_text(encoding="utf-8")
                .replace("average_score: 4.7", "average_score: 9.9")
                .replace("confidence: medium", "confidence: high")
                + "\nGLOBAL_ASSESSMENT: Excelente\n",
                encoding="utf-8",
            )
            first = materialize_interview_evaluation_v2(
                self.evaluations,
                self.evidence,
                Path(directory) / "first.md",
            )
            second = materialize_interview_evaluation_v2(
                self.evaluations,
                self.evidence,
                Path(directory) / "second.md",
            )
        self.assertEqual(first["content"], second["content"])
        self.assertIn("Média: 4.7 / 10", second["content"])
        self.assertNotIn("Média: 9.9 / 10", second["content"])

    def test_materialization_is_idempotent_and_protects_inputs(self):
        hashes_before = {path: self._hash(path) for path in self.protected}
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "Interview Evaluation v2.md"
            first = materialize_interview_evaluation_v2(
                self.evaluations, self.evidence, destination
            )
            first_content = destination.read_text(encoding="utf-8")
            second = materialize_interview_evaluation_v2(
                self.evaluations, self.evidence, destination
            )
            second_content = destination.read_text(encoding="utf-8")
        self.assertEqual(first_content, second_content)
        self.assertEqual(first["runtime"], second["runtime"])
        self.assertEqual(
            hashes_before,
            {path: self._hash(path) for path in self.protected},
        )


if __name__ == "__main__":
    unittest.main()
