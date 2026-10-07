import copy
import hashlib
import json
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
REPORT = PILOT / "Stage 30.2.1 — Final Semantic Audit.md"


def _projection(artifacts):
    return {
        key: artifacts[key]
        for key in ("questions", "responses", "reconstructed_responses", "links", "evidence", "evaluations")
    }


class Stage3021FinalSemanticAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
        cls.original_fixture = build_real_pilot_fixture(SOURCE)
        cls.pipeline = run_real_pilot(SOURCE)["pipeline"]
        cls.artifacts = cls.pipeline["artifacts"]

    def test_source_of_truth_and_participant_integrity(self):
        self.assertEqual(self.source_hash, hashlib.sha256(SOURCE.read_bytes()).hexdigest())
        self.assertEqual(
            {item["role"] for item in self.artifacts["participants"]},
            {"candidate", "interviewer", "observer"},
        )
        self.assertEqual(
            next(item for item in self.artifacts["participants"] if item["role"] == "candidate")[
                "participant_id"
            ],
            "P-05-CANDIDATE",
        )

    def test_speaker_question_response_and_reconstruction_integrity(self):
        self.assertTrue(all(item["speaker_id"] == "candidate" for item in self.artifacts["responses"]))
        self.assertEqual(len(self.artifacts["questions"]), 11)
        self.assertEqual(len(self.artifacts["responses"]), 47)
        self.assertTrue(
            all(
                item["original_text"] == item["reconstructed_text"]
                for item in self.artifacts["reconstructed_responses"]
            )
        )

    def test_stage_301_correction_and_p102_conservative_handling(self):
        question_texts = [item["text"] for item in self.artifacts["questions"]]
        self.assertNotIn("E tem uma Daily também, só nossa, né?", question_texts)
        self.assertTrue(any("observabilidade" in text for text in question_texts))
        self.assertTrue(any("JDBC" in text for text in question_texts))
        unknown = {
            item["response_id"]
            for item in self.artifacts["responses"]
            if item["question_id"] == "unknown"
        }
        self.assertIn("R26", unknown)
        self.assertIn("R43", unknown)

    def test_unknown_responses_have_no_evidence_or_forced_link(self):
        unknown = {
            item["response_id"]
            for item in self.artifacts["responses"]
            if item["question_id"] == "unknown"
        }
        self.assertTrue(
            all(
                item["relation_type"] == "unlinked"
                for item in self.artifacts["links"]
                if item["response_id"] in unknown
            )
        )
        self.assertTrue(
            all(item["response_id"] not in unknown for item in self.artifacts["evidence"]["evidence_set"])
        )

    def test_candidate_questions_and_non_evaluable_content_are_excluded(self):
        candidate_questions = self.artifacts["candidate_questions"]
        self.assertEqual(len(candidate_questions), 5)
        self.assertTrue(all(item["evaluation_eligible"] is False for item in candidate_questions))
        evaluated_questions = {item["question_id"] for item in self.artifacts["evaluations"]}
        self.assertTrue(
            evaluated_questions.isdisjoint(item["question_id"] for item in candidate_questions)
        )

    def test_evidence_is_exactly_supported_and_traceable(self):
        responses = {item["response_id"]: item for item in self.artifacts["responses"]}
        questions = {item["question_id"] for item in self.artifacts["questions"]}
        segments = {item["id"] for item in self.artifacts["speaker_attributed_transcript"]}
        for evidence in self.artifacts["evidence"]["evidence_set"]:
            response = responses[evidence["response_id"]]
            self.assertIn(evidence["question_id"], questions)
            self.assertEqual(evidence["question_id"], response["question_id"])
            self.assertIn(evidence["content"], response["text"])
            self.assertTrue(set(evidence["source"]["segment_ids"]) <= segments)

    def test_evaluations_and_scores_are_traceable_and_valid(self):
        evidence = {
            item["evidence_id"]: item
            for item in self.artifacts["evidence"]["evidence_set"]
        }
        for evaluation in self.artifacts["evaluations"]:
            self.assertGreaterEqual(evaluation["score"], 0)
            self.assertLessEqual(evaluation["score"], 10)
            self.assertTrue(evaluation["evidence_ids"])
            for evidence_id in evaluation["evidence_ids"]:
                self.assertEqual(evidence[evidence_id]["question_id"], evaluation["question_id"])
                self.assertEqual(evidence[evidence_id]["response_id"], evaluation["response_id"])

    def test_no_external_context_or_expected_scores_affect_result(self):
        baseline = _projection(self.artifacts)
        variants = []
        for context in (
            {"title": "principal engineer", "seniority": "staff", "company": "Other"},
            {"title": "intern", "seniority": "junior", "job_context": "unrelated"},
        ):
            fixture = copy.deepcopy(self.original_fixture)
            fixture["job_context"] = context
            variants.append(_projection(run_interview_pipeline(fixture)["artifacts"]))
        for variant in variants:
            self.assertEqual(baseline, variant)

    def test_historical_and_expected_score_mutations_do_not_affect_result(self):
        baseline = _projection(self.artifacts)
        for key, value in (
            ("historical_report", "candidate is excellent"),
            ("expected_scores", {"Q1": 10}),
            ("expected_evaluations", [{"question_id": "Q1", "score": 10}]),
        ):
            fixture = copy.deepcopy(self.original_fixture)
            fixture[key] = value
            self.assertEqual(baseline, _projection(run_interview_pipeline(fixture)["artifacts"]))

    def test_transcript_and_response_mutations_affect_derived_output(self):
        transcript_mutation = copy.deepcopy(self.original_fixture)
        transcript_mutation["raw_transcript"][2]["text"] = "Tenho pouca experiência com o projeto."
        changed_transcript = run_interview_pipeline(transcript_mutation)["artifacts"]
        self.assertNotEqual(self.artifacts["evidence"], changed_transcript["evidence"])

        response_mutation = copy.deepcopy(self.original_fixture)
        response_mutation["raw_transcript"][36]["text"] = "Não sei explicar JDBC."
        changed_response = run_interview_pipeline(response_mutation)["artifacts"]
        self.assertNotEqual(self.artifacts["evaluations"], changed_response["evaluations"])

    def test_determinism_and_global_proportionality(self):
        repeated = run_real_pilot(SOURCE)["pipeline"]["artifacts"]
        self.assertEqual(_projection(self.artifacts), _projection(repeated))
        scores = [item["score"] for item in self.artifacts["evaluations"]]
        self.assertEqual(len(scores), 11)
        self.assertEqual(round(sum(scores) / len(scores), 2), 5.55)
        self.assertEqual(sorted(scores)[len(scores) // 2], 5.85)

    def test_artifact_protection_and_report_gate(self):
        self.assertEqual(self.source_hash, hashlib.sha256(SOURCE.read_bytes()).hexdigest())
        self.assertTrue(REPORT.exists())
        report = REPORT.read_text(encoding="utf-8")
        self.assertIn("FINAL_SEMANTIC_AUDIT_COMPLETE_WITH_WARNINGS", report)
        self.assertIn("FSA-001", report)


if __name__ == "__main__":
    unittest.main()
