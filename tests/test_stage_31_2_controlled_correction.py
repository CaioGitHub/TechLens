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
STAGE31_COMPARISON = PILOT / "Stage 31 — Human vs System Comparison.md"
STAGE311 = PILOT / "Stage 31.1 — Human vs System Failure Analysis.md"


def _fixture(question: str, answer: str, fixture_id: str = "STAGE-31-2"):
    return {
        "fixture_id": fixture_id,
        "pipeline_version": "31.2-reference-1",
        "participants": [
            {"participant_id": "P-INTERVIEWER", "name": "Interviewer", "role": "interviewer"},
            {"participant_id": "P-CANDIDATE", "name": "Candidate", "role": "candidate"},
        ],
        "raw_transcript": [
            {"id": f"{fixture_id}-Q", "timestamp": "00:00", "speaker": "Interviewer", "text": question},
            {"id": f"{fixture_id}-R", "timestamp": "00:10", "speaker": "Candidate", "text": answer},
        ],
    }


class Stage312ControlledCorrectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
        cls.baseline = {
            "Q1": 6.0,
            "Q3": 6.0,
            "Q5": 7.05,
            "Q6": 7.05,
            "Q9": 7.05,
            "Q11": 7.65,
        }
        cls.corrected = run_real_pilot(SOURCE)["pipeline"]["artifacts"]

    def test_baseline_is_recorded_and_correction_changes_priority_cases(self):
        corrected = {
            item["question_id"]: item["score"]
            for item in self.corrected["evaluations"]
            if item["question_id"] in self.baseline
        }
        self.assertEqual(set(corrected), set(self.baseline))
        self.assertNotEqual(corrected["Q5"], self.baseline["Q5"])
        self.assertLess(corrected["Q5"], self.baseline["Q5"])
        self.assertLess(corrected["Q1"], self.baseline["Q1"])
        self.assertLess(corrected["Q9"], self.baseline["Q9"])
        self.assertLess(corrected["Q11"], self.baseline["Q11"])

    def test_q5_is_classified_as_off_topic_without_inventing_rest_evidence(self):
        evidence = [
            item for item in self.corrected["evidence"]["evidence_set"]
            if item["question_id"] == "Q5"
        ]
        evaluation = next(item for item in self.corrected["evaluations"] if item["question_id"] == "Q5")
        self.assertIn("off_topic", {item["type"] for item in evidence})
        self.assertNotEqual(evaluation["dimensions"]["correctness"]["assessment"], "Strong")
        self.assertEqual(evaluation["confidence"], "medium")
        self.assertTrue(all("Kafka" in item["content"] or "Rabbit" in item["content"] for item in evidence))

    def test_correct_rest_answer_remains_positive(self):
        result = run_interview_pipeline(_fixture(
            "Explique REST e como funciona uma requisição HTTP.",
            "REST organiza recursos por URLs e usa HTTP, métodos como GET e POST, códigos de status e representações.",
            "REST-CORRECT",
        ))
        evaluation = result["artifacts"]["evaluations"][0]
        self.assertEqual(evaluation["dimensions"]["correctness"]["assessment"], "Strong")
        self.assertGreaterEqual(evaluation["score"], 6.0)

    def test_partial_rest_answer_is_not_promoted_to_strong(self):
        result = run_interview_pipeline(_fixture(
            "Explique REST e como funciona uma requisição HTTP.",
            "REST usa HTTP.",
            "REST-PARTIAL",
        ))
        evaluation = result["artifacts"]["evaluations"][0]
        self.assertNotEqual(evaluation["dimensions"]["correctness"]["assessment"], "Strong")

    def test_declaration_and_demonstrated_experience_remain_distinct(self):
        declaration = run_interview_pipeline(_fixture(
            "Você tem experiência com Azure Monitor?",
            "Já trabalhei bastante com Azure Monitor.",
            "DECLARATION",
        ))
        demonstrated = run_interview_pipeline(_fixture(
            "Você tem experiência com Azure Monitor?",
            "Em produção configurei Azure Monitor, criei alertas, investiguei falhas e reduzi o ruído.",
            "DEMONSTRATED",
        ))
        declaration_types = {
            item["type"] for item in declaration["artifacts"]["evidence"]["evidence_set"]
        }
        demonstrated_types = {
            item["type"] for item in demonstrated["artifacts"]["evidence"]["evidence_set"]
        }
        self.assertIn("experience_declaration", declaration_types)
        self.assertNotIn("demonstrated_experience", declaration_types)
        self.assertIn("demonstrated_experience", demonstrated_types)

    def test_hypothetical_answer_is_not_experience(self):
        result = run_interview_pipeline(_fixture(
            "Você tem experiência com mensageria?",
            "Eu usaria Kafka com retry e backoff se tivesse esse cenário.",
            "HYPOTHETICAL",
        ))
        types = {item["type"] for item in result["artifacts"]["evidence"]["evidence_set"]}
        self.assertIn("hypothesis", types)
        self.assertNotIn("demonstrated_experience", types)

    def test_mutations_change_semantics_but_jargon_does_not_inflate(self):
        base = run_interview_pipeline(_fixture(
            "Explique REST.",
            "REST usa HTTP para expor recursos.",
            "MUTATION-BASE",
        ))["artifacts"]["evaluations"][0]
        off_topic = run_interview_pipeline(_fixture(
            "Explique REST.",
            "Kafka usa producers, consumers e tópicos.",
            "MUTATION-OFF-TOPIC",
        ))["artifacts"]["evaluations"][0]
        jargon = run_interview_pipeline(_fixture(
            "Explique REST.",
            "REST, HTTP, microservices, CQRS, DDD, SOLID, Kafka, cloud e observabilidade.",
            "MUTATION-JARGON",
        ))["artifacts"]["evaluations"][0]
        self.assertNotEqual(base["score"], off_topic["score"])
        self.assertLessEqual(jargon["score"], base["score"])

    def test_context_isolation_and_idempotency(self):
        fixture = build_real_pilot_fixture(SOURCE)
        first = run_interview_pipeline(fixture)["artifacts"]
        second = run_interview_pipeline(copy.deepcopy(fixture))["artifacts"]
        self.assertEqual(first["evidence"], second["evidence"])
        self.assertEqual(first["evaluations"], second["evaluations"])
        mutated = copy.deepcopy(fixture)
        mutated["job_context"] = {"title": "staff", "seniority": "staff", "company": "Other"}
        self.assertEqual(first["evaluations"], run_interview_pipeline(mutated)["artifacts"]["evaluations"])

    def test_historical_reports_remain_unchanged_and_source_is_preserved(self):
        self.assertEqual(self.source_hash, hashlib.sha256(SOURCE.read_bytes()).hexdigest())
        self.assertIn("HUMAN_VS_SYSTEM_BLOCKED", STAGE31_COMPARISON.read_text(encoding="utf-8"))
        self.assertIn("HUMAN_VS_SYSTEM_FAILURE_ANALYSIS_COMPLETE_WITH_WARNINGS", STAGE311.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
