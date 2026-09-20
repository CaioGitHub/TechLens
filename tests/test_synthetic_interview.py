import unittest

from reference_runtime import run_pipeline
from tests.synthetic_interview import (
    clone_with_raw_text_change,
    synthetic_interview_fixture,
)


class SyntheticInterviewFullRunTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = synthetic_interview_fixture()
        cls.result = run_pipeline(cls.fixture)

    def test_raw_transcript_is_preserved(self):
        self.assertEqual(self.result["artifacts"]["raw_transcript"], self.fixture["raw_transcript"])

    def test_three_participants(self):
        self.assertEqual(len(self.result["artifacts"]["participants"]), 3)

    def test_timestamps_are_preserved(self):
        self.assertTrue(self.result["artifacts"]["raw_transcript"][0]["timestamp"])

    def test_speaker_changes_are_preserved(self):
        labels = {item["speaker_label"] for item in self.result["artifacts"]["speaker_attributed_transcript"]}
        self.assertEqual(labels, {"Ana Martins", "Bruno Lima", "Carla Souza", "UNKNOWN"})

    def test_transcription_error_is_present(self):
        self.assertIn("Spring Boto", self.result["artifacts"]["raw_transcript"][-1]["text"])

    def test_participant_identification(self):
        self.assertEqual(self.result["artifacts"]["participants"][0]["role"], "candidate")

    def test_speaker_attribution(self):
        segment = self.result["artifacts"]["speaker_attributed_transcript"][1]
        self.assertEqual(segment["participant_id"], "P-CANDIDATE-27")

    def test_ambiguous_speaker(self):
        segment = next(item for item in self.result["artifacts"]["speaker_attributed_transcript"] if item["id"] == "RAW-26")
        self.assertEqual(segment["speaker_id"], "unknown")
        self.assertTrue(segment["needs_review"])

    def test_candidate_question_is_not_extracted(self):
        self.assertNotIn("CQ7", [item["question_id"] for item in self.result["artifacts"]["questions"]])

    def test_direct_questions(self):
        self.assertEqual(len(self.result["artifacts"]["questions"]), 12)

    def test_follow_up_question(self):
        question = next(item for item in self.result["artifacts"]["questions"] if item["question_id"] == "Q2")
        self.assertEqual(question["follow_up_of"], "Q1")

    def test_reformulation(self):
        question = next(item for item in self.result["artifacts"]["questions"] if item["question_id"] == "Q5")
        self.assertEqual(question["reformulation_of"], "Q4")

    def test_unanswered_question(self):
        response = next(item for item in self.result["artifacts"]["responses"] if item["question_id"] == "Q4")
        self.assertEqual(response["response_status"], "missing")

    def test_direct_response(self):
        response = next(item for item in self.result["artifacts"]["responses"] if item["response_id"] == "R1")
        self.assertEqual(response["response_status"], "identified")

    def test_multi_segment_response(self):
        response = next(item for item in self.result["artifacts"]["responses"] if item["response_id"] == "R1")
        self.assertEqual(response["source"]["segment_ids"], ["RAW-02", "RAW-03"])

    def test_interrupted_response_is_not_merged_with_interviewer(self):
        response = next(item for item in self.result["artifacts"]["responses"] if item["response_id"] == "R3")
        self.assertNotIn("RAW-06", response["source"]["segment_ids"])

    def test_autocorrection(self):
        response = next(item for item in self.result["artifacts"]["reconstructed_responses"] if item["response_id"] == "R6")
        self.assertIn("Pensando melhor", response["original_text"])

    def test_hypothesis(self):
        response = next(item for item in self.result["artifacts"]["responses"] if item["response_id"] == "R10")
        self.assertEqual(response["response_type"], "hypothetical")

    def test_uncertainty(self):
        response = next(item for item in self.result["artifacts"]["responses"] if item["response_id"] == "R11")
        self.assertEqual(response["response_type"], "uncertainty")

    def test_experience_declaration(self):
        evidence = next(item for item in self.result["artifacts"]["evidence"]["evidence_set"] if item["response_id"] == "R8")
        self.assertEqual(evidence["type"], "experience_declaration")

    def test_demonstrated_experience(self):
        evidence = next(item for item in self.result["artifacts"]["evidence"]["evidence_set"] if item["response_id"] == "R9")
        self.assertEqual(evidence["type"], "demonstrated_experience")

    def test_technical_error_is_preserved(self):
        evidence = next(item for item in self.result["artifacts"]["evidence"]["evidence_set"] if item["response_id"] == "R5")
        self.assertEqual(evidence["qualification"], "negative")

    def test_normalization_preserves_original(self):
        response = next(item for item in self.result["artifacts"]["reconstructed_responses"] if item["response_id"] == "R12")
        self.assertIn("Spring Boto", response["original_text"])
        self.assertIn("Spring Boot", response["reconstructed_text"])

    def test_normalization_has_confidence(self):
        response = next(item for item in self.result["artifacts"]["reconstructed_responses"] if item["response_id"] == "R12")
        self.assertIn(response["reconstruction_confidence"], {"high", "medium", "low"})

    def test_question_response_links(self):
        self.assertTrue(all("question_id" in link and "response_id" in link for link in self.result["artifacts"]["links"]))

    def test_unlinked_response_is_allowed(self):
        fixture = synthetic_interview_fixture()
        fixture["raw_transcript"].append({"id": "RAW-29", "timestamp": "10:12:00", "speaker": "UNKNOWN", "text": "Fala sem contexto."})
        result = run_pipeline(fixture)
        self.assertTrue(result["artifacts"]["speaker_attributed_transcript"][-1]["needs_review"])

    def test_validation_report_shape(self):
        validation = self.result["artifacts"]["validation"]
        self.assertIn("summary", validation)
        self.assertIn("issues", validation)
        self.assertIn("traceability", validation)
        self.assertIn("readiness", validation)

    def test_validation_warning_is_justified(self):
        self.assertEqual(self.result["readiness"], "READY_WITH_WARNINGS")
        self.assertTrue(self.result["warnings"])

    def test_evidence_fields(self):
        evidence = self.result["artifacts"]["evidence"]["evidence_set"][0]
        for field in ("evidence_id", "question_id", "response_id", "type", "qualification", "content", "interpretation", "explicitness", "evidence_strength", "evidence_confidence", "source", "relations"):
            self.assertIn(field, evidence)

    def test_evidence_source_traceability(self):
        self.assertTrue(all(item["source"]["segment_ids"] for item in self.result["artifacts"]["evidence"]["evidence_set"]))

    def test_missing_is_not_evidence(self):
        self.assertFalse(any(item["question_id"] == "Q4" for item in self.result["artifacts"]["evidence"]["evidence_set"]))

    def test_evaluation_dimensions(self):
        evaluation = self.result["artifacts"]["evaluations"][0]
        self.assertEqual(set(evaluation["dimensions"]), {"correctness", "completeness", "depth", "reasoning", "practical_application", "trade_offs"})

    def test_evaluation_weighting_contract(self):
        self.assertTrue(all("score" in item and "confidence" in item for item in self.result["artifacts"]["evaluations"]))

    def test_na_dimension_contract(self):
        fixture = synthetic_interview_fixture()
        fixture["evaluation_specs"]["Q1"]["dimensions"] = {"correctness": {"assessment": "N/A", "score": None, "applicable": False}}
        result = run_pipeline(fixture)
        self.assertFalse(result["artifacts"]["evaluations"][0]["dimensions"]["correctness"]["applicable"])

    def test_evaluation_confidence_is_separate(self):
        self.assertIn(self.result["artifacts"]["evaluations"][0]["confidence"], {"high", "medium", "low"})

    def test_evaluation_traceability(self):
        self.assertTrue(all(item["evidence_ids"] for item in self.result["artifacts"]["evaluations"]))

    def test_raw_transcript_not_in_evaluation(self):
        self.assertNotIn("raw_transcript", self.result["artifacts"]["evaluations"][0])

    def test_rubric_not_mutated(self):
        self.assertEqual(self.result["pipeline_version"], "27-reference-1")

    def test_pipeline_does_not_score_evidence(self):
        self.assertNotIn("score", self.result["artifacts"]["evidence"])

    def test_report_does_not_recalculate(self):
        self.assertEqual(self.result["artifacts"]["report"]["evaluations"], self.result["artifacts"]["evaluations"])

    def test_job_context_does_not_change_evidence(self):
        other = run_pipeline(synthetic_interview_fixture(), {"title": "platform", "seniority": "senior"})
        self.assertEqual(other["artifacts"]["evidence"], self.result["artifacts"]["evidence"])

    def test_job_context_does_not_change_evaluation(self):
        other = run_pipeline(synthetic_interview_fixture(), {"title": "platform", "seniority": "senior"})
        self.assertEqual(other["artifacts"]["evaluations"], self.result["artifacts"]["evaluations"])

    def test_idempotency_questions(self):
        self.assertEqual(run_pipeline(self.fixture)["artifacts"]["questions"], self.result["artifacts"]["questions"])

    def test_idempotency_evidence(self):
        self.assertEqual(run_pipeline(self.fixture)["artifacts"]["evidence"], self.result["artifacts"]["evidence"])

    def test_idempotency_evaluations(self):
        self.assertEqual(run_pipeline(self.fixture)["artifacts"]["evaluations"], self.result["artifacts"]["evaluations"])

    def test_reprocessing_changes_artifact(self):
        changed = run_pipeline(clone_with_raw_text_change())
        self.assertNotEqual(changed["artifacts"]["reconstructed_responses"], self.result["artifacts"]["reconstructed_responses"])

    def test_stale_artifact_detection(self):
        fixture = synthetic_interview_fixture()
        fixture["upstream_version"] = 2
        fixture["evidence_version"] = 1
        result = run_pipeline(fixture)
        self.assertIn("stale downstream artifact: evidence-set", result["warnings"])

    def test_report_candidate(self):
        self.assertEqual(self.result["artifacts"]["report"]["candidate"]["name"], "Ana Martins")

    def test_report_contains_questions(self):
        self.assertEqual(len(self.result["artifacts"]["report"]["questions"]), 12)

    def test_report_contains_responses(self):
        self.assertEqual(len(self.result["artifacts"]["report"]["responses"]), len(self.result["artifacts"]["responses"]))

    def test_report_contains_evidence(self):
        self.assertEqual(len(self.result["artifacts"]["report"]["evidence"]), len(self.result["artifacts"]["evidence"]["evidence_set"]))

    def test_report_contains_validation(self):
        self.assertEqual(self.result["artifacts"]["report"]["validation"]["status"], self.result["artifacts"]["validation"]["status"])

    def test_source_timestamps(self):
        question = self.result["artifacts"]["questions"][0]
        self.assertEqual(question["source"]["timestamps"], ["10:00:00"])

    def test_response_timestamps(self):
        response = self.result["artifacts"]["responses"][0]
        self.assertEqual(response["source"]["timestamps"], ["10:00:12", "10:00:24"])

    def test_interviewer_intervention_is_separate(self):
        intervention = next(item for item in self.result["artifacts"]["speaker_attributed_transcript"] if item["id"] == "RAW-06")
        self.assertEqual(intervention["kind"], "intervention")

    def test_observer_comment_is_separate(self):
        observer = next(item for item in self.result["artifacts"]["speaker_attributed_transcript"] if item["id"] == "RAW-11")
        self.assertEqual(observer["participant_id"], "P-OBSERVER-27")

    def test_candidate_question_has_no_evaluation(self):
        self.assertNotIn("CQ7", [item["question_id"] for item in self.result["artifacts"]["evaluations"]])

    def test_follow_up_link_is_traceable(self):
        link = next(item for item in self.result["artifacts"]["links"] if item["question_id"] == "Q2")
        self.assertEqual(link["question_id"], "Q2")

    def test_reformulation_link_is_traceable(self):
        question = next(item for item in self.result["artifacts"]["questions"] if item["question_id"] == "Q5")
        self.assertEqual(question["reformulation_of"], "Q4")

    def test_original_and_reconstructed_text_are_distinct(self):
        response = next(item for item in self.result["artifacts"]["reconstructed_responses"] if item["response_id"] == "R12")
        self.assertNotEqual(response["original_text"], response["reconstructed_text"])

    def test_hypothesis_not_experience(self):
        evidence = next(item for item in self.result["artifacts"]["evidence"]["evidence_set"] if item["response_id"] == "R10")
        self.assertNotEqual(evidence["type"], "demonstrated_experience")

    def test_declaration_not_demonstration(self):
        evidence = next(item for item in self.result["artifacts"]["evidence"]["evidence_set"] if item["response_id"] == "R8")
        self.assertNotEqual(evidence["type"], "demonstrated_experience")

    def test_unknown_speaker_warning_propagates(self):
        self.assertTrue(any("speaker attribution" in warning for warning in self.result["warnings"]))

    def test_validation_stage_status(self):
        stage = next(item for item in self.result["stages"] if item["stage"] == "20.7")
        self.assertEqual(stage["status"], "READY_WITH_WARNINGS")

    def test_evidence_stage_status(self):
        stage = next(item for item in self.result["stages"] if item["stage"] == "21")
        self.assertEqual(stage["status"], "READY_WITH_WARNINGS")

    def test_evaluation_stage_status(self):
        stage = next(item for item in self.result["stages"] if item["stage"] == "23")
        self.assertEqual(stage["status"], "READY_WITH_WARNINGS")

    def test_all_stages_have_contract_fields(self):
        for stage in self.result["stages"]:
            for field in ("stage", "status", "input_id", "output_id", "warnings", "errors"):
                self.assertIn(field, stage)

    def test_all_evaluations_have_question_response(self):
        self.assertTrue(all(item["question_id"] and item["response_id"] for item in self.result["artifacts"]["evaluations"]))

    def test_traceability_chain_has_source(self):
        for evaluation in self.result["artifacts"]["evaluations"]:
            evidence = next(item for item in self.result["artifacts"]["evidence"]["evidence_set"] if item["evidence_id"] in evaluation["evidence_ids"])
            self.assertTrue(evidence["source"]["segment_ids"])

    def test_cv_like_metadata_does_not_change_evaluation(self):
        fixture = synthetic_interview_fixture()
        fixture["candidate_metadata"] = {"company": "Synthetic Labs", "years": 10}
        self.assertEqual(run_pipeline(fixture)["artifacts"]["evaluations"], self.result["artifacts"]["evaluations"])

    def test_complexity_does_not_change_evaluation(self):
        fixture = synthetic_interview_fixture()
        fixture["question_complexity"] = "advanced"
        self.assertEqual(run_pipeline(fixture)["artifacts"]["evaluations"], self.result["artifacts"]["evaluations"])

    def test_verbosity_does_not_change_score(self):
        changed = run_pipeline(clone_with_raw_text_change())
        original_scores = [item["score"] for item in self.result["artifacts"]["evaluations"]]
        changed_scores = [item["score"] for item in changed["artifacts"]["evaluations"]]
        self.assertEqual(original_scores, changed_scores)

    def test_stage_27_version(self):
        self.assertEqual(self.result["pipeline_version"], "27-reference-1")

    def test_completion_status(self):
        self.assertEqual(self.result["status"], "COMPLETED")

    def test_ready_with_warnings_status(self):
        self.assertEqual(self.result["readiness"], "READY_WITH_WARNINGS")

    def test_no_real_report_written(self):
        self.assertIn("report", self.result["artifacts"])

    def test_no_external_services_required(self):
        self.assertNotIn("url", self.result)

    def test_no_candidate_decision(self):
        self.assertNotIn("hiring_decision", self.result["artifacts"]["report"])

    def test_no_seniority_inference(self):
        self.assertNotIn("seniority", self.result["artifacts"]["evaluations"][0])

    def test_no_score_in_transcription_artifacts(self):
        for key in ("participants", "speaker_attributed_transcript", "questions", "responses", "reconstructed_responses", "links"):
            self.assertNotIn("score", self.result["artifacts"][key])


if __name__ == "__main__":
    unittest.main()
