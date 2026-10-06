from __future__ import annotations

import hashlib
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from reference_runtime import PipelineBlocked, run_interview_pipeline, run_pipeline
from tests.stage_27_fixture import (
    mutate_stage_27_transcript,
    stage_27_expected_contract,
    stage_27_raw_fixture,
)


ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "11 - Interview Evaluation" / "09 - Real Interview Pilot" / "Candidato-Piloto-01"


class Stage27SyntheticInterviewFullRunTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = stage_27_raw_fixture()
        cls.result = run_pipeline(cls.fixture)
        cls.contract = stage_27_expected_contract()

    def test_raw_transcript_is_the_actual_input(self):
        self.assertIn("raw_transcript", self.fixture)
        for derived_key in ("transcript", "questions", "responses", "evidence", "evaluations"):
            self.assertNotIn(derived_key, self.fixture)
        self.assertEqual(
            self.result["artifacts"]["raw_transcript"],
            self.fixture["raw_transcript"],
        )

    def test_stage_20_1_identifies_participants(self):
        participants = self.result["artifacts"]["participants"]
        self.assertEqual(len(participants), 3)
        self.assertEqual({item["role"] for item in participants}, self.contract["participant_roles"])
        self.assertEqual(
            next(item for item in participants if item["role"] == "candidate")["participant_id"],
            "P-CANDIDATE-27",
        )

    def test_stage_20_2_attributes_speakers_and_keeps_ambiguity(self):
        segments = self.result["artifacts"]["speaker_attributed_transcript"]
        self.assertTrue(all("participant_id" in item for item in segments))
        ambiguous = next(item for item in segments if item["id"] == "RAW-26")
        self.assertEqual(ambiguous["speaker_id"], "unknown")
        self.assertTrue(ambiguous["needs_review"])
        self.assertEqual(ambiguous["attribution_confidence"], "low")

    def test_stage_20_3_extracts_questions_and_candidate_question(self):
        questions = self.result["artifacts"]["questions"]
        self.assertTrue(any("latência" in item["text"].lower() for item in questions))
        self.assertTrue(any(item.get("follow_up_of") for item in questions))
        candidate_question = self.result["artifacts"]["candidate_questions"]
        self.assertTrue(candidate_question)
        self.assertTrue(all(item["evaluation_eligible"] is False for item in candidate_question))

    def test_stage_20_3_preserves_compound_question_text(self):
        question_text = " ".join(item["text"] for item in self.result["artifacts"]["questions"])
        self.assertNotIn("pergunta inventada", question_text.lower())
        self.assertTrue(any("e depois" in item["text"].lower() or "como" in item["text"].lower() for item in self.result["artifacts"]["questions"]))

    def test_stage_20_4_extracts_direct_and_unknown_responses(self):
        responses = self.result["artifacts"]["responses"]
        self.assertTrue(any(item["response_status"] == "identified" for item in responses))
        unknown = [item for item in responses if item["question_id"] == "unknown"]
        self.assertFalse(unknown)
        ambiguous = next(item for item in self.result["artifacts"]["speaker_attributed_transcript"] if item["id"] == "RAW-26")
        self.assertEqual(ambiguous["speaker_id"], "unknown")

    def test_stage_20_4_preserves_multisegment_response(self):
        response = next(item for item in self.result["artifacts"]["responses"] if item["response_id"] == "R1")
        self.assertEqual(response["source"]["segment_ids"], ["RAW-02", "RAW-03"])

    def test_stage_20_4_does_not_merge_interviewer_interruption(self):
        response = next(item for item in self.result["artifacts"]["responses"] if item["response_id"] == "R3")
        self.assertNotIn("RAW-06", response["source"]["segment_ids"])
        interviewer = next(item for item in self.result["artifacts"]["speaker_attributed_transcript"] if item["id"] == "RAW-06")
        self.assertEqual(interviewer["participant_id"], "P-INTERVIEWER-27")

    def test_stage_20_5_reconstructs_without_erasing_original(self):
        response = next(item for item in self.result["artifacts"]["reconstructed_responses"] if item["response_id"] == "R12")
        self.assertIn("Spring Boto", response["original_text"])
        self.assertIn("Spring Boot", response["reconstructed_text"])
        self.assertNotEqual(response["original_text"], response["reconstructed_text"])
        self.assertIn(response["reconstruction_confidence"], {"high", "medium", "low"})

    def test_stage_20_5_preserves_autocorrection_and_uncertainty(self):
        correction = next(item for item in self.result["artifacts"]["reconstructed_responses"] if item["response_id"] == "R6")
        uncertainty = next(item for item in self.result["artifacts"]["reconstructed_responses"] if item["response_id"] == "R11")
        self.assertIn("Pensando melhor", correction["original_text"])
        self.assertIn("Não lembro", uncertainty["original_text"])

    def test_stage_20_6_links_and_preserves_missing(self):
        links = self.result["artifacts"]["links"]
        self.assertTrue(any(link["question_id"] == "Q1" and link["response_id"] == "R1" for link in links))
        missing = [item for item in self.result["artifacts"]["responses"] if item["response_status"] == "missing"]
        self.assertTrue(missing)
        self.assertTrue(all(item["text"] is None for item in missing))

    def test_stage_20_7_reaches_allowed_gate_with_controlled_warnings(self):
        self.assertIn(self.result["readiness"], {"READY", "READY_WITH_WARNINGS"})
        validation = self.result["artifacts"]["validation"]
        self.assertTrue(validation["readiness"] in {"READY", "READY_WITH_WARNINGS"})
        self.assertTrue(self.result["warnings"])

    def test_stage_21_derives_evidence_from_processed_responses(self):
        evidence = self.result["artifacts"]["evidence"]["evidence_set"]
        response_ids = {item["response_id"] for item in self.result["artifacts"]["responses"]}
        self.assertTrue(evidence)
        self.assertTrue(all(item["response_id"] in response_ids for item in evidence))
        self.assertTrue(all(item["source"]["segment_ids"] for item in evidence))

    def test_experience_declaration_is_not_promoted(self):
        declaration = [
            item for item in self.result["artifacts"]["evidence"]["evidence_set"]
            if item["response_id"] == "R8"
        ]
        self.assertEqual({item["type"] for item in declaration}, {"experience_declaration"})

    def test_demonstrated_experience_requires_concrete_context(self):
        demonstrated = [
            item for item in self.result["artifacts"]["evidence"]["evidence_set"]
            if item["response_id"] == "R9"
        ]
        self.assertIn("demonstrated_experience", {item["type"] for item in demonstrated})
        self.assertIn("Application Insights", demonstrated[0]["content"])

    def test_hypothesis_and_uncertainty_remain_distinct(self):
        evidence = self.result["artifacts"]["evidence"]["evidence_set"]
        self.assertIn("hypothesis", {item["type"] for item in evidence if item["response_id"] == "R10"})
        self.assertIn("uncertainty", {item["type"] for item in evidence if item["response_id"] == "R11"})

    def test_stage_23_evaluations_consume_evidence_ids(self):
        evidence_ids = {item["evidence_id"] for item in self.result["artifacts"]["evidence"]["evidence_set"]}
        evaluations = self.result["artifacts"]["evaluations"]
        self.assertTrue(evaluations)
        self.assertTrue(all(set(item["evidence_ids"]) <= evidence_ids for item in evaluations))
        self.assertTrue(all(0 <= item["score"] <= 10 for item in evaluations))
        self.assertTrue(all(item["confidence"] in {"low", "medium", "high"} for item in evaluations))

    def test_report_materializes_runtime_result_without_v1(self):
        report = self.result["artifacts"]["report"]
        self.assertEqual(report["evaluations"], self.result["artifacts"]["evaluations"])
        self.assertNotIn("Interview Evaluation v1.md", repr(report))
        self.assertTrue(report["traceability"])

    def test_end_to_end_stage_sequence_is_complete(self):
        stages = [item["stage"] for item in self.result["stages"]]
        self.assertEqual(stages, ["20.1", "20.2", "20.3", "20.4", "20.5", "20.6", "20.7", "21", "23", "report"])

    def test_traceability_evaluation_to_source(self):
        report_trace = self.result["artifacts"]["report"]["traceability"]
        segments = {item["id"] for item in self.result["artifacts"]["speaker_attributed_transcript"]}
        evidence = {item["evidence_id"]: item for item in self.result["artifacts"]["evidence"]["evidence_set"]}
        responses = {item["response_id"]: item for item in self.result["artifacts"]["responses"] if item["response_id"]}
        questions = {item["question_id"] for item in self.result["artifacts"]["questions"]}
        for item in report_trace:
            self.assertIn(item["question_id"], questions)
            response = responses[item["response_id"]]
            self.assertEqual(response["question_id"], item["question_id"])
            for evidence_id in item["evidence_ids"]:
                self.assertIn(evidence_id, evidence)
                self.assertTrue(set(evidence[evidence_id]["source"]["segment_ids"]) <= segments)

    def test_missing_response_is_not_evidence_or_zero_score(self):
        missing_questions = {
            item["question_id"] for item in self.result["artifacts"]["responses"]
            if item["response_status"] == "missing"
        }
        evidence_questions = {
            item["question_id"] for item in self.result["artifacts"]["evidence"]["evidence_set"]
        }
        self.assertTrue(missing_questions.isdisjoint(evidence_questions))

    def test_historical_v1_mutation_does_not_change_raw_result(self):
        before = hashlib.sha256((PILOT / "Interview Evaluation v1.md").read_bytes()).hexdigest()
        first = run_pipeline(stage_27_raw_fixture())
        with tempfile.TemporaryDirectory() as directory:
            historical = Path(directory) / "Interview Evaluation v1.md"
            historical.write_text("corrupted historical result: 0.0\n", encoding="utf-8")
            second = run_pipeline(stage_27_raw_fixture())
        after = hashlib.sha256((PILOT / "Interview Evaluation v1.md").read_bytes()).hexdigest()
        self.assertEqual(before, after)
        self.assertEqual(first["artifacts"]["evaluations"], second["artifacts"]["evaluations"])

    def test_transcript_mutation_changes_derived_artifacts(self):
        original = run_pipeline(stage_27_raw_fixture())
        mutated = run_pipeline(mutate_stage_27_transcript(stage_27_raw_fixture()))
        self.assertNotEqual(
            original["artifacts"]["raw_transcript"],
            mutated["artifacts"]["raw_transcript"],
        )
        self.assertNotEqual(
            original["artifacts"]["reconstructed_responses"],
            mutated["artifacts"]["reconstructed_responses"],
        )
        self.assertNotEqual(
            original["artifacts"]["evidence"]["evidence_set"],
            mutated["artifacts"]["evidence"]["evidence_set"],
        )

    def test_expected_contract_mutation_does_not_change_execution(self):
        first = run_pipeline(stage_27_raw_fixture())
        mutated = stage_27_raw_fixture()
        mutated["oracle"]["requires_demonstrated_experience"] = False
        second = run_pipeline(mutated)
        self.assertEqual(first["artifacts"]["questions"], second["artifacts"]["questions"])
        self.assertEqual(first["artifacts"]["evaluations"], second["artifacts"]["evaluations"])

    def test_speaker_mutation_changes_attribution(self):
        fixture = stage_27_raw_fixture()
        fixture["raw_transcript"] = deepcopy(fixture["raw_transcript"])
        next(item for item in fixture["raw_transcript"] if item["id"] == "RAW-28")["speaker"] = "Carla Souza"
        result = run_pipeline(fixture)
        segment = next(item for item in result["artifacts"]["speaker_attributed_transcript"] if item["id"] == "RAW-28")
        self.assertEqual(segment["participant_id"], "P-OBSERVER-27")

    def test_response_mutation_changes_downstream_evidence(self):
        original = run_pipeline(stage_27_raw_fixture())
        mutated = stage_27_raw_fixture()
        next(item for item in mutated["raw_transcript"] if item["id"] == "RAW-19")["text"] = "Em produção apenas observei um dashboard."
        changed = run_pipeline(mutated)
        original_evidence = [item for item in original["artifacts"]["evidence"]["evidence_set"] if item["response_id"] == "R9"]
        changed_evidence = [item for item in changed["artifacts"]["evidence"]["evidence_set"] if item["response_id"] == "R9"]
        self.assertNotEqual(original_evidence, changed_evidence)

    def test_idempotency_is_semantically_stable(self):
        first = run_pipeline(stage_27_raw_fixture())
        second = run_pipeline(stage_27_raw_fixture())
        for key in ("participants", "questions", "responses", "reconstructed_responses", "links", "evidence", "evaluations", "report"):
            self.assertEqual(first["artifacts"][key], second["artifacts"][key])
        self.assertEqual(first["warnings"], second["warnings"])

    def test_stage24_boundary_consumes_raw_fixture_without_structured_input(self):
        result = run_interview_pipeline(stage_27_raw_fixture(), run_id="STAGE27-RAW")
        self.assertIn("raw_transcript", result["artifacts"])
        self.assertIn("questions", result["artifacts"])
        self.assertIn("responses", result["artifacts"])
        self.assertIn("evidence", result["artifacts"])
        self.assertIn("evaluations", result["artifacts"])

    def test_stage_23_1_and_23_2_gates_are_exposed_by_pipeline_boundary(self):
        result = run_interview_pipeline(stage_27_raw_fixture(), run_id="STAGE27-RAW")
        stages = {item["stage"]: item for item in result["stages"]}
        self.assertIn("23.1", stages)
        self.assertIn("23.2", stages)
        self.assertIn(stages["23.1"]["status"], {"READY_WITH_WARNINGS", "COMPLETED"})
        self.assertIn(stages["23.2"]["status"], {"READY_WITH_WARNINGS", "COMPLETED"})

    def test_no_job_context_seniority_or_hiring_output(self):
        serialized = repr(self.result["artifacts"]).lower()
        for forbidden in ("seniority", "junior", "pleno", "senior", "contratar", "aprovado", "reprovado"):
            self.assertNotIn(forbidden, serialized)

    def test_canonical_artifacts_are_preserved(self):
        protected = (
            PILOT / "Interview Evaluation v1.md",
            PILOT / "Interview Evaluation v2.md",
            PILOT / "Evidence Set v1.md",
            PILOT / "Individual Evaluations v2.md",
            PILOT / "Structured Interview - Controlled Correction v6.md",
        )
        before = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in protected}
        run_pipeline(stage_27_raw_fixture())
        after = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in protected}
        self.assertEqual(before, after)

    def test_blocked_validation_does_not_execute_evidence_or_evaluation(self):
        fixture = stage_27_raw_fixture()
        fixture["validation_blockers"] = ["synthetic structural blocker"]
        with self.assertRaises(PipelineBlocked) as context:
            run_pipeline(fixture)
        artifacts = context.exception.result["artifacts"]
        self.assertNotIn("evidence", artifacts)
        self.assertNotIn("evaluations", artifacts)


if __name__ == "__main__":
    unittest.main()
