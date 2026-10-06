from __future__ import annotations

import hashlib
import unittest
from copy import deepcopy
from pathlib import Path

from reference_runtime import (
    EvaluationInput,
    EvaluationInputError,
    PipelineBlocked,
    run_pipeline,
    run_evaluation_engine,
)
from tests.adversarial_cases import (
    adversarial_fixtures,
    blind_adversarial_input,
)


ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "11 - Interview Evaluation" / "09 - Real Interview Pilot"


def _minimal_input(**changes):
    evaluations = [
        {
            "evaluation_id": "EV-Q1",
            "question_id": "Q1",
            "score": 7.0,
            "confidence": "medium",
            "evidence_ids": ["E1"],
            "dimensions": {},
        }
    ]
    evidence = [
        {
            "evidence_id": "E1",
            "question_id": "Q1",
            "response_id": "R1",
            "type": "conceptual",
            "source": {"segment_ids": ["S1"]},
        }
    ]
    data = {"evaluations": evaluations, "evidence": evidence}
    data.update(changes)
    return EvaluationInput(data["evaluations"], data["evidence"])


class Stage29AdversarialEdgeCaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = adversarial_fixtures()
        cls.results = {}
        cls.blocked = {}
        for case_id, fixture in cls.fixtures.items():
            try:
                cls.results[case_id] = run_pipeline(blind_adversarial_input(fixture))
            except PipelineBlocked as error:
                cls.blocked[case_id] = error.result

    def test_p0_existing_matrix_executes_without_failures(self):
        self.assertEqual(set(self.results) | set(self.blocked), set(self.fixtures))
        self.assertEqual(len(self.blocked), 1)
        self.assertEqual(self.blocked["ADV-BLOCKED"]["readiness"], "BLOCKED")

    def test_ambiguous_speaker_is_fail_safe(self):
        result = self.results["ADV-19"]
        segment = result["artifacts"]["speaker_attributed_transcript"][1]
        self.assertEqual(segment["speaker_id"], "unknown")
        self.assertTrue(segment["needs_review"])
        self.assertEqual(segment["attribution_confidence"], "low")

    def test_missing_and_unlinked_are_not_scored(self):
        missing = self.results["ADV-22"]
        self.assertTrue(any(item["response_status"] == "missing" for item in missing["artifacts"]["responses"]))
        self.assertFalse(missing["artifacts"]["evaluations"])
        unlinked = self.results["ADV-23"]
        self.assertEqual(unlinked["artifacts"]["responses"][0]["question_id"], "unknown")
        self.assertFalse(unlinked["artifacts"]["evaluations"])

    def test_interruption_and_continuation_do_not_invent_content(self):
        result = self.results["ADV-21"]
        texts = [item["text"] for item in result["artifacts"]["responses"] if item["text"]]
        self.assertNotIn("eu investigaria primeiro o Application Insights", texts)
        self.assertEqual(len(texts), 2)

    def test_cross_question_and_interviewer_content_remain_separate(self):
        result = self.results["ADV-26"]
        evidence = result["artifacts"]["evidence"]["evidence_set"]
        self.assertTrue(evidence)
        self.assertTrue(all(item["source"]["segment_ids"] == ["ADV-26-03"] for item in evidence))

    def test_reconstruction_preserves_original_and_rejects_weak_term_guess(self):
        normalized = self.results["ADV-20"]["artifacts"]["reconstructed_responses"][0]
        self.assertIn("Spring Boto", normalized["original_text"])
        self.assertIn("Spring Boot", normalized["reconstructed_text"])
        fixture = blind_adversarial_input(self.fixtures["ADV-20"])
        fixture.pop("reconstructions", None)
        fixture["raw_transcript"][1]["text"] = "Eu usaria Spring Insight Boot."
        changed = run_pipeline(fixture)
        response = changed["artifacts"]["reconstructed_responses"][0]
        self.assertNotIn("Spring Boot", response["reconstructed_text"])

    def test_experience_and_hypothesis_are_not_inflated(self):
        declaration = {
            item["type"]
            for item in self.results["ADV-13"]["artifacts"]["evidence"]["evidence_set"]
        }
        hypothesis = {
            item["type"]
            for item in self.results["ADV-16"]["artifacts"]["evidence"]["evidence_set"]
        }
        self.assertIn("experience_declaration", declaration)
        self.assertNotIn("demonstrated_experience", declaration)
        self.assertIn("hypothesis", hypothesis)
        self.assertNotIn("demonstrated_experience", hypothesis)

    def test_contradiction_uncertainty_and_correction_are_retained(self):
        for case_id, expected in (
            ("ADV-01", "contradiction"),
            ("ADV-02", "self_correction"),
            ("ADV-15", "uncertainty"),
            ("ADV-17", "contradiction"),
        ):
            types = {
                item["type"]
                for item in self.results[case_id]["artifacts"]["evidence"]["evidence_set"]
            }
            self.assertIn(expected, types)

    def test_metadata_score_and_historical_context_do_not_contaminate(self):
        base = blind_adversarial_input(self.fixtures["ADV-12"])
        baseline = run_pipeline(base)["artifacts"]["evaluations"]
        mutated = deepcopy(base)
        mutated.update(
            {
                "candidate": {"seniority": "Senior", "experience_years": 15},
                "cv": "exceptional architect with 20 years",
                "job_context": {"title": "Senior Java Architect"},
                "expected_score": 10,
                "historical_report": "Interview Evaluation v1.md: score 10",
            }
        )
        self.assertEqual(baseline, run_pipeline(mutated)["artifacts"]["evaluations"])

    def test_evidence_injection_without_source_is_rejected_by_canonical_contract(self):
        evidence = deepcopy(_minimal_input().evidence)
        evidence[0]["source"] = {}
        with self.assertRaises(EvaluationInputError):
            run_evaluation_engine(EvaluationInput(_minimal_input().evaluations, evidence))

    def test_broken_traceability_is_rejected(self):
        evaluations = deepcopy(_minimal_input().evaluations)
        evaluations[0]["evidence_ids"] = ["MISSING"]
        with self.assertRaises(EvaluationInputError):
            run_evaluation_engine(EvaluationInput(evaluations, _minimal_input().evidence))

    def test_duplicate_ids_are_rejected(self):
        evidence = deepcopy(_minimal_input().evidence)
        evidence.append(deepcopy(evidence[0]))
        with self.assertRaises(EvaluationInputError):
            run_evaluation_engine(EvaluationInput(_minimal_input().evaluations, evidence))

    def test_invalid_confidence_and_score_are_rejected(self):
        for field, value in (("confidence", "high-ish"), ("confidence", 150)):
            evaluations = deepcopy(_minimal_input().evaluations)
            evaluations[0][field] = value
            with self.assertRaises(EvaluationInputError):
                run_evaluation_engine(EvaluationInput(evaluations, _minimal_input().evidence))
        for value in (-1, 11, "eight"):
            evaluations = deepcopy(_minimal_input().evaluations)
            evaluations[0]["score"] = value
            with self.assertRaises(EvaluationInputError):
                run_evaluation_engine(EvaluationInput(evaluations, _minimal_input().evidence))

    def test_missing_required_fields_are_rejected(self):
        for field in ("evaluation_id", "question_id", "confidence"):
            evaluations = deepcopy(_minimal_input().evaluations)
            evaluations[0].pop(field)
            with self.assertRaises(EvaluationInputError):
                run_evaluation_engine(EvaluationInput(evaluations, _minimal_input().evidence))

    def test_empty_and_one_sided_interviews_do_not_create_evaluations(self):
        for transcript in (
            [],
            [{"speaker": "Interviewer Adversarial", "text": "Explique virtual threads?"}],
            [{"speaker": "Candidate Adversarial", "text": "Eu usaria métricas."}],
        ):
            fixture = deepcopy(self.fixtures["ADV-22"])
            fixture["raw_transcript"] = [
                {"id": f"EMPTY-{index}", "timestamp": "12:00:00", **item}
                for index, item in enumerate(transcript)
            ]
            result = run_pipeline(blind_adversarial_input(fixture))
            self.assertFalse(result["artifacts"]["evaluations"])

    def test_duplicate_repetition_does_not_change_source_identity(self):
        fixture = blind_adversarial_input(self.fixtures["ADV-12"])
        repeated = deepcopy(fixture)
        repeated["raw_transcript"].extend(deepcopy(fixture["raw_transcript"][1:]))
        result = run_pipeline(repeated)
        source_ids = {
            segment_id
            for item in result["artifacts"]["evidence"]["evidence_set"]
            for segment_id in item["source"]["segment_ids"]
        }
        self.assertEqual(len(source_ids), len(set(source_ids)))

    def test_unicode_empty_segments_and_timestamp_anomalies_are_preserved_safely(self):
        fixture = blind_adversarial_input(self.fixtures["ADV-12"])
        fixture["raw_transcript"].insert(
            1,
            {"id": "UNICODE", "timestamp": "12:00:00", "speaker": "Candidate Adversarial", "text": "çã 😀"},
        )
        fixture["raw_transcript"].append(
            {"id": "EMPTY", "timestamp": "11:00:00", "speaker": "Candidate Adversarial", "text": "   "},
        )
        result = run_pipeline(fixture)
        self.assertIn("çã 😀", repr(result["artifacts"]["speaker_attributed_transcript"]))
        self.assertEqual(result["status"], "COMPLETED")

    def test_source_mutation_changes_downstream_result(self):
        fixture = blind_adversarial_input(self.fixtures["ADV-01"])
        first = run_pipeline(fixture)
        changed = deepcopy(fixture)
        changed["raw_transcript"][1]["text"] = "Eu não sei responder isso."
        second = run_pipeline(changed)
        self.assertNotEqual(first["artifacts"]["evaluations"], second["artifacts"]["evaluations"])

    def test_repeated_execution_is_deterministic(self):
        fixture = blind_adversarial_input(self.fixtures["ADV-25"])
        first = run_pipeline(fixture)
        second = run_pipeline(fixture)
        for key in ("participants", "questions", "responses", "evidence", "evaluations", "report"):
            self.assertEqual(first["artifacts"][key], second["artifacts"][key])
        self.assertEqual(first["warnings"], second["warnings"])

    def test_protected_reports_remain_unchanged(self):
        protected = list(PILOT.rglob("Stage 27*")) + list(PILOT.rglob("Stage 28*"))
        before = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in protected}
        run_pipeline(blind_adversarial_input(self.fixtures["ADV-01"]))
        after = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in protected}
        self.assertEqual(before, after)

    def test_fail_and_blocked_are_distinct(self):
        warning = self.results["ADV-WARNING"]
        self.assertEqual(warning["status"], "COMPLETED")
        self.assertEqual(warning["readiness"], "READY_WITH_WARNINGS")
        blocked = self.blocked["ADV-BLOCKED"]
        self.assertEqual(blocked["status"], "BLOCKED")
        self.assertEqual(blocked["readiness"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
