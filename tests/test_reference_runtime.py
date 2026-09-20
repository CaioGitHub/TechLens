import unittest
from copy import deepcopy

from reference_runtime import PipelineBlocked, run_pipeline
from tests.fixtures import fixture_for_case, nominal_fixture


class ReferenceRuntimeTests(unittest.TestCase):
    def run_case(self, case_id):
        return run_pipeline(fixture_for_case(case_id))

    def test_e2e_01_nominal_traceability(self):
        result = run_pipeline(nominal_fixture())
        self.assertEqual(result["readiness"], "READY")
        self.assertEqual(len(result["artifacts"]["evaluations"]), 2)
        evaluation = result["artifacts"]["evaluations"][0]
        self.assertEqual(evaluation["evidence_ids"], ["EVD-1"])
        self.assertEqual(result["artifacts"]["report"]["traceability"][0]["question_id"], "Q1")

    def test_e2e_02_missing_is_not_negative(self):
        result = self.run_case("missing_response")
        missing = next(item for item in result["artifacts"]["responses"] if item["question_id"] == "Q1")
        self.assertEqual(missing["response_status"], "missing")
        self.assertEqual(result["artifacts"]["evidence"]["evidence_set"], [])

    def test_e2e_03_unknown_question_is_preserved(self):
        result = self.run_case("unknown_question")
        response = next(item for item in result["artifacts"]["responses"] if item["response_id"] == "R1")
        self.assertEqual(response["question_id"], "unknown")

    def test_e2e_04_ambiguous_speaker(self):
        result = self.run_case("ambiguous_speaker")
        segment = next(item for item in result["artifacts"]["speaker_attributed_transcript"] if item["id"] == "S02")
        self.assertEqual(segment["speaker_id"], "unknown")
        self.assertTrue(segment["needs_review"])
        self.assertEqual(result["readiness"], "READY_WITH_WARNINGS")

    def test_e2e_05_reconstruction_preserves_original(self):
        result = self.run_case("reconstruction")
        response = next(item for item in result["artifacts"]["reconstructed_responses"] if item["response_id"] == "R1")
        self.assertNotEqual(response["original_text"], response["reconstructed_text"])
        self.assertIn("p95", response["original_text"])

    def test_e2e_06_technical_error_preserved(self):
        result = self.run_case("technical_error")
        evidence = next(item for item in result["artifacts"]["evidence"]["evidence_set"] if item["response_id"] == "R1")
        self.assertEqual(evidence["qualification"], "negative")

    def test_e2e_07_self_correction_preserved(self):
        result = self.run_case("self_correction")
        response = next(item for item in result["artifacts"]["reconstructed_responses"] if item["response_id"] == "R1")
        self.assertIn("X", response["original_text"])
        self.assertIn("Y", response["original_text"])

    def test_e2e_08_hypothesis_preserved(self):
        result = self.run_case("hypothetical_answer")
        response = next(item for item in result["artifacts"]["responses"] if item["response_id"] == "R1")
        self.assertEqual(response["response_type"], "hypothetical")

    def test_e2e_09_experience_declaration(self):
        result = self.run_case("experience_declaration")
        evidence = next(item for item in result["artifacts"]["evidence"]["evidence_set"] if item["response_id"] == "R1")
        self.assertEqual(evidence["type"], "experience_declaration")

    def test_e2e_10_demonstrated_experience(self):
        result = run_pipeline(nominal_fixture())
        evidence = next(item for item in result["artifacts"]["evidence"]["evidence_set"] if item["response_id"] == "R1.1")
        self.assertEqual(evidence["type"], "demonstrated_experience")

    def test_e2e_11_follow_up(self):
        result = run_pipeline(nominal_fixture())
        question = next(item for item in result["artifacts"]["questions"] if item["question_id"] == "Q1.1")
        self.assertEqual(question["follow_up_of"], "Q1")

    def test_e2e_12_reformulation(self):
        fixture = nominal_fixture()
        fixture["transcript"][2]["reformulation_of"] = "Q1"
        result = run_pipeline(fixture)
        question = next(item for item in result["artifacts"]["questions"] if item["question_id"] == "Q1.1")
        self.assertEqual(question["reformulation_of"], "Q1")

    def test_e2e_13_multi_segment_order(self):
        result = self.run_case("multi_segment_response")
        response = next(item for item in result["artifacts"]["responses"] if item["response_id"] == "R1")
        self.assertEqual(response["source"]["segment_ids"], ["S02", "S02B"])

    def test_e2e_14_interviewer_not_candidate_evidence(self):
        result = run_pipeline(nominal_fixture())
        for evidence in result["artifacts"]["evidence"]["evidence_set"]:
            self.assertNotIn("P-INTERVIEWER", evidence["source"]["segment_ids"])

    def test_e2e_15_candidate_question_not_evaluated(self):
        result = self.run_case("candidate_question")
        self.assertNotIn("CQ1", [item["question_id"] for item in result["artifacts"]["questions"]])

    def test_e2e_16_needs_review_propagates(self):
        result = self.run_case("needs_review")
        response = next(item for item in result["artifacts"]["responses"] if item["response_id"] == "R1")
        evidence = next(item for item in result["artifacts"]["evidence"]["evidence_set"] if item["response_id"] == "R1")
        self.assertTrue(response["needs_review"])
        self.assertTrue(evidence["needs_review"])

    def test_e2e_17_warning_continues(self):
        result = self.run_case("ready_with_warnings")
        self.assertEqual(result["readiness"], "READY_WITH_WARNINGS")
        self.assertTrue(result["artifacts"]["evaluations"])
        self.assertTrue(result["warnings"])

    def test_e2e_18_blocked_stops_downstream(self):
        with self.assertRaises(PipelineBlocked) as context:
            self.run_case("blocked")
        result = context.exception.result
        self.assertEqual(result["status"], "BLOCKED")
        self.assertNotIn("evidence", result["artifacts"])
        self.assertNotIn("evaluations", result["artifacts"])

    def test_e2e_19_traceability(self):
        result = run_pipeline(nominal_fixture())
        evaluation = result["artifacts"]["evaluations"][0]
        evidence = result["artifacts"]["evidence"]["evidence_set"][0]
        self.assertEqual(evaluation["evidence_ids"][0], evidence["evidence_id"])
        self.assertTrue(evidence["source"]["segment_ids"])

    def test_e2e_20_idempotency(self):
        first = run_pipeline(nominal_fixture())
        second = run_pipeline(nominal_fixture())
        for key in ("participants", "questions", "responses", "evidence", "evaluations", "report"):
            self.assertEqual(first["artifacts"][key], second["artifacts"][key])
        self.assertEqual(first["run_id"], second["run_id"])

    def test_e2e_21_reprocessing_input_changes_artifact(self):
        original = run_pipeline(nominal_fixture())
        changed_fixture = nominal_fixture()
        changed_fixture["transcript"][1]["text"] = "Resposta alterada."
        changed = run_pipeline(changed_fixture)
        self.assertNotEqual(
            original["artifacts"]["reconstructed_responses"],
            changed["artifacts"]["reconstructed_responses"],
        )

    def test_e2e_22_stale_version_is_detectable(self):
        fixture = nominal_fixture()
        fixture["upstream_version"] = 2
        fixture["evidence_version"] = 1
        result = run_pipeline(fixture)
        self.assertEqual(result["input_id"], fixture["fixture_id"])
        self.assertIn("stale downstream artifact: evidence-set", result["warnings"])

    def test_e2e_23_na_dimension(self):
        result = self.run_case("na_dimension")
        evaluation = result["artifacts"]["evaluations"][0]
        self.assertFalse(evaluation["dimensions"]["depth"]["applicable"])
        self.assertIsNone(evaluation["dimensions"]["depth"]["score"])

    def test_e2e_24_critical_error_is_evidence(self):
        result = self.run_case("critical_error")
        evidence = next(item for item in result["artifacts"]["evidence"]["evidence_set"] if item["response_id"] == "R1")
        self.assertEqual(evidence["qualification"], "negative")

    def test_e2e_25_short_long_invariance_contract(self):
        short = run_pipeline(nominal_fixture())
        long_fixture = nominal_fixture()
        long_fixture["transcript"][1]["text"] += " Texto adicional irrelevante."
        long = run_pipeline(long_fixture)
        self.assertEqual(short["artifacts"]["evaluations"][0]["score"], long["artifacts"]["evaluations"][0]["score"])

    def test_e2e_26_eloquence_invariance_contract(self):
        direct = run_pipeline(nominal_fixture())
        articulate_fixture = nominal_fixture()
        articulate_fixture["transcript"][1]["text"] = "Com segurança, eu iniciaria por métricas percentis e isolamento de dependências."
        articulate = run_pipeline(articulate_fixture)
        self.assertEqual(direct["artifacts"]["evaluations"][0]["score"], articulate["artifacts"]["evaluations"][0]["score"])

    def test_e2e_27_seniority_invariance_contract(self):
        first = run_pipeline(nominal_fixture())
        second_fixture = nominal_fixture()
        second_fixture["candidate_metadata"] = {"years": 10}
        second = run_pipeline(second_fixture)
        self.assertEqual(first["artifacts"]["evaluations"], second["artifacts"]["evaluations"])

    def test_e2e_28_complexity_is_not_score(self):
        first = run_pipeline(nominal_fixture())
        second_fixture = nominal_fixture()
        second_fixture["question_complexity"] = "advanced"
        second = run_pipeline(second_fixture)
        self.assertEqual(first["artifacts"]["evaluations"], second["artifacts"]["evaluations"])

    def test_e2e_29_job_context_is_separate(self):
        first = run_pipeline(nominal_fixture(), {"title": "backend"})
        second = run_pipeline(nominal_fixture(), {"title": "platform"})
        self.assertEqual(first["artifacts"]["evidence"], second["artifacts"]["evidence"])
        self.assertEqual(first["artifacts"]["evaluations"], second["artifacts"]["evaluations"])

    def test_e2e_30_report_consumes_evaluations(self):
        result = run_pipeline(nominal_fixture())
        self.assertEqual(
            result["artifacts"]["report"]["evaluations"],
            result["artifacts"]["evaluations"],
        )

    def test_responsibility_boundaries(self):
        result = run_pipeline(nominal_fixture())
        self.assertNotIn("score", result["artifacts"]["evidence"])
        self.assertNotIn("raw_transcript", result["artifacts"]["evaluations"])
        self.assertNotIn("seniority", result["artifacts"]["evaluations"])


if __name__ == "__main__":
    unittest.main()
