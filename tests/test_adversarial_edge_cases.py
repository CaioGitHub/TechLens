import unittest
from copy import deepcopy

from reference_runtime import PipelineBlocked, run_pipeline
from tests.adversarial_cases import (
    adversarial_fixtures,
    adversarial_oracles,
    blind_adversarial_input,
)


class AdversarialEdgeCaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = adversarial_fixtures()
        cls.oracles = adversarial_oracles()
        cls.results = {}
        cls.blocked = {}
        for case_id, fixture in cls.fixtures.items():
            runtime_input = blind_adversarial_input(fixture)
            if case_id == "ADV-BLOCKED":
                try:
                    run_pipeline(runtime_input)
                except PipelineBlocked as error:
                    cls.blocked[case_id] = error.result
                continue
            cls.results[case_id] = run_pipeline(runtime_input)

    def result(self, case_id):
        return self.results[case_id]

    def evidence_types(self, case_id):
        return {
            item["type"]
            for item in self.result(case_id)["artifacts"]["evidence"]["evidence_set"]
        }

    def test_all_adversarial_inputs_are_blind(self):
        for fixture in self.fixtures.values():
            runtime_input = blind_adversarial_input(fixture)
            for forbidden in (
                "oracle",
                "expected_score",
                "expected_dimensions",
                "evidence_specs",
                "evaluation_specs",
                "adversarial_label",
            ):
                self.assertNotIn(forbidden, runtime_input)

    def test_all_non_blocked_cases_execute(self):
        self.assertEqual(len(self.results), 33)
        self.assertEqual(set(self.results) | set(self.blocked), set(self.fixtures))

    def test_contradiction_inside_response_is_preserved(self):
        self.assertIn("contradiction", self.evidence_types("ADV-01"))

    def test_partial_self_correction_preserves_error_and_correction(self):
        types = self.evidence_types("ADV-02")
        self.assertIn("self_correction", types)
        self.assertIn("technical_error", types)
        response = self.result("ADV-02")["artifacts"]["reconstructed_responses"][0]
        self.assertIn("thread do sistema operacional", response["original_text"])
        self.assertIn("threads virtuais", response["original_text"])

    def test_incorrect_self_correction_is_not_positive_by_itself(self):
        evaluation = self.result("ADV-03")["artifacts"]["evaluations"][0]
        self.assertNotEqual(evaluation["dimensions"]["correctness"]["assessment"], "Strong")
        self.assertIn("technical_error", self.evidence_types("ADV-03"))

    def test_interviewer_induced_confirmation_is_insufficient(self):
        for case_id in ("ADV-04", "ADV-05"):
            self.assertIn("confirmation", self.evidence_types(case_id))
            evaluation = self.result(case_id)["artifacts"]["evaluations"][0]
            self.assertEqual(evaluation["dimensions"]["correctness"]["assessment"], "Insufficient")

    def test_interviewer_content_is_not_candidate_source(self):
        result = self.result("ADV-05")
        evidence = result["artifacts"]["evidence"]["evidence_set"]
        self.assertTrue(all(item["source"]["segment_ids"] == ["ADV-05-03"] for item in evidence))

    def test_interrupted_multi_turn_response_preserves_order(self):
        result = self.result("ADV-06")
        response = result["artifacts"]["responses"][0]
        self.assertEqual(response["source"]["segment_ids"], ["ADV-06-02"])
        second = result["artifacts"]["responses"][1]
        self.assertEqual(second["source"]["segment_ids"], ["ADV-06-04"])

    def test_follow_up_and_scope_change_remain_separate(self):
        for case_id in ("ADV-07", "ADV-08"):
            result = self.result(case_id)
            self.assertEqual(len(result["artifacts"]["questions"]), 2)
            self.assertEqual(result["artifacts"]["questions"][1]["follow_up_of"], "Q1")
        self.assertEqual(len(self.result("ADV-08")["artifacts"]["evaluations"]), 2)

    def test_correct_answer_to_wrong_question_is_off_topic(self):
        self.assertIn("off_topic", self.evidence_types("ADV-09"))

    def test_jargon_does_not_create_high_quality_evidence(self):
        evaluation = self.result("ADV-10")["artifacts"]["evaluations"][0]
        self.assertLessEqual(evaluation["score"], 8.0)
        self.assertNotIn("tradeoff", self.evidence_types("ADV-10"))

    def test_eloquence_without_technical_content_is_not_inflated(self):
        evaluation = self.result("ADV-11")["artifacts"]["evaluations"][0]
        self.assertLessEqual(evaluation["score"], 8.0)

    def test_short_dense_answer_remains_technically_valid(self):
        evaluation = self.result("ADV-12")["artifacts"]["evaluations"][0]
        self.assertNotEqual(evaluation["dimensions"]["correctness"]["assessment"], "Weak")

    def test_declared_experience_does_not_become_demonstrated(self):
        types = self.evidence_types("ADV-13")
        self.assertIn("experience_declaration", types)
        self.assertNotIn("demonstrated_experience", types)

    def test_short_demonstrated_experience_is_preserved(self):
        self.assertIn("demonstrated_experience", self.evidence_types("ADV-14"))

    def test_uncertainty_is_not_negative_evidence(self):
        types = self.evidence_types("ADV-15")
        self.assertIn("uncertainty", types)
        self.assertNotIn("technical_error", types)

    def test_uncertainty_and_hypothesis_are_distinct(self):
        types = self.evidence_types("ADV-16")
        self.assertIn("uncertainty", types)
        self.assertIn("hypothesis", types)
        self.assertNotIn("demonstrated_experience", types)

    def test_cross_response_conflict_is_preserved(self):
        self.assertIn("contradiction", self.evidence_types("ADV-17"))

    def test_interviewer_challenge_does_not_erase_candidate_autocorrection(self):
        self.assertIn("self_correction", self.evidence_types("ADV-18"))
        response = self.result("ADV-18")["artifacts"]["reconstructed_responses"][1]
        self.assertIn("Ah, verdade", response["original_text"])

    def test_ambiguous_speaker_prefers_unknown_and_warning(self):
        result = self.result("ADV-19")
        segment = result["artifacts"]["speaker_attributed_transcript"][1]
        self.assertEqual(segment["speaker_id"], "unknown")
        self.assertTrue(segment["needs_review"])
        self.assertEqual(result["readiness"], "READY_WITH_WARNINGS")

    def test_obvious_term_normalization_preserves_original(self):
        response = self.result("ADV-20")["artifacts"]["reconstructed_responses"][0]
        self.assertIn("Spring Boto", response["original_text"])
        self.assertIn("Spring Boot", response["reconstructed_text"])

    def test_interrupted_answer_is_not_completed_by_inference(self):
        result = self.result("ADV-21")
        response_texts = [item["text"] for item in result["artifacts"]["responses"] if item["text"]]
        self.assertNotIn("eu investigaria primeiro o Application Insights", response_texts)
        self.assertEqual(len(response_texts), 2)

    def test_missing_question_response_is_not_negative(self):
        result = self.result("ADV-22")
        self.assertTrue(any(item["response_status"] == "missing" for item in result["artifacts"]["responses"]))
        self.assertFalse(result["artifacts"]["evidence"]["evidence_set"])

    def test_response_without_question_remains_unknown(self):
        result = self.result("ADV-23")
        response = result["artifacts"]["responses"][0]
        self.assertEqual(response["question_id"], "unknown")
        self.assertFalse(result["artifacts"]["evaluations"])

    def test_partial_correctness_preserves_error_and_partiality(self):
        types = self.evidence_types("ADV-24")
        self.assertIn("technical_error", types)
        evaluation = self.result("ADV-24")["artifacts"]["evaluations"][0]
        self.assertIn(evaluation["dimensions"]["correctness"]["assessment"], {"Weak", "Partial", "Adequate"})

    def test_multiple_conflicting_evidence_types_are_retained(self):
        types = self.evidence_types("ADV-25")
        self.assertTrue({"contradiction", "uncertainty", "hypothesis"} <= types)

    def test_interviewer_comment_is_not_candidate_evidence(self):
        result = self.result("ADV-26")
        evidence = result["artifacts"]["evidence"]["evidence_set"]
        self.assertTrue(evidence)
        self.assertTrue(all("ADV-26-03" in item["source"]["segment_ids"] for item in evidence))

    def test_candidate_question_is_not_evaluated(self):
        result = self.result("ADV-27")
        self.assertFalse(result["artifacts"]["questions"])
        self.assertFalse(result["artifacts"]["evaluations"])

    def test_correct_conclusion_with_wrong_argument_keeps_error(self):
        self.assertIn("technical_error", self.evidence_types("ADV-28"))

    def test_seniority_mutation_is_invariant(self):
        first = self.result("ADV-30-A")["artifacts"]["evaluations"]
        second = self.result("ADV-30-B")["artifacts"]["evaluations"]
        self.assertEqual(first, second)

    def test_blocking_stops_downstream(self):
        result = self.blocked["ADV-BLOCKED"]
        self.assertEqual(result["readiness"], "BLOCKED")
        self.assertNotIn("evidence", result["artifacts"])
        self.assertNotIn("evaluations", result["artifacts"])

    def test_warning_continues_downstream(self):
        result = self.result("ADV-WARNING")
        self.assertEqual(result["readiness"], "READY_WITH_WARNINGS")
        self.assertIn("evidence", result["artifacts"])
        self.assertIn("23", [stage["stage"] for stage in result["stages"]])

    def test_reconstruction_confidence_is_independent(self):
        result = self.result("ADV-LOW-RECON")
        response = result["artifacts"]["reconstructed_responses"][0]
        self.assertEqual(response["reconstruction_confidence"], "low")
        self.assertIn(result["artifacts"]["evaluations"][0]["confidence"], {"high", "medium"})

    def test_traceability_is_complete_for_adversarial_evidence(self):
        for result in self.results.values():
            for evaluation in result["artifacts"]["evaluations"]:
                evidence_by_id = {
                    item["evidence_id"]: item
                    for item in result["artifacts"]["evidence"]["evidence_set"]
                }
                self.assertTrue(evaluation["question_id"])
                self.assertTrue(evaluation["response_id"])
                for evidence_id in evaluation["evidence_ids"]:
                    source_ids = evidence_by_id[evidence_id]["source"]["segment_ids"]
                    self.assertTrue(source_ids)
                    self.assertTrue(
                        all(
                            segment_id
                            in {item["id"] for item in result["artifacts"]["speaker_attributed_transcript"]}
                            for segment_id in source_ids
                        )
                    )

    def test_idempotency_and_controlled_reprocessing(self):
        fixture = blind_adversarial_input(self.fixtures["ADV-01"])
        first = run_pipeline(fixture)
        second = run_pipeline(fixture)
        self.assertEqual(first["artifacts"]["evidence"], second["artifacts"]["evidence"])
        changed = deepcopy(fixture)
        changed["raw_transcript"][1]["text"] += " sem alterar a decisão."
        third = run_pipeline(changed)
        self.assertNotEqual(first["artifacts"]["reconstructed_responses"], third["artifacts"]["reconstructed_responses"])

    def test_mutation_suite_preserves_technical_result(self):
        base = blind_adversarial_input(self.fixtures["ADV-12"])
        mutations = [
            " Tenho 10 anos de experiência.",
            " Isso está no meu currículo.",
            " usando DDD, SOLID e CQRS.",
            " A arquitetura pode ter camadas e componentes adicionais.",
        ]
        baseline = run_pipeline(base)["artifacts"]["evaluations"][0]
        for suffix in mutations:
            mutated = deepcopy(base)
            mutated["raw_transcript"][1]["text"] += suffix
            evaluation = run_pipeline(mutated)["artifacts"]["evaluations"][0]
            self.assertEqual(baseline["score"], evaluation["score"])

    def test_responsibility_boundaries_remain_separate(self):
        result = self.result("ADV-01")
        self.assertNotIn("score", result["artifacts"]["evidence"])
        self.assertNotIn("raw_transcript", result["artifacts"]["evaluations"][0])
        self.assertNotIn("seniority", result["artifacts"]["evaluations"][0])


if __name__ == "__main__":
    unittest.main()
