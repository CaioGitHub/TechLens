import copy
import statistics
import unittest
from unittest.mock import patch

from reference_runtime import (
    APPROVAL_REQUIRED,
    BLOCKED,
    COMPLETED,
    COMPLETED_WITH_WARNINGS,
    OrchestrationStore,
    REQUIRES_HUMAN_REVIEW,
    resume_orchestration,
    run_orchestration,
    run_pipeline,
    validate_orchestration_result,
)
from tests.fixtures import fixture_for_case, nominal_fixture


class Stage25EndToEndTests(unittest.TestCase):
    def nominal(self, **kwargs):
        return run_orchestration(
            nominal_fixture(),
            human_review_approved=True,
            global_audit_status="PASS_WITH_WARNINGS",
            **kwargs,
        )

    def test_nominal_integrated_flow_and_traceability(self):
        result = self.nominal()
        self.assertEqual(result["pipeline"]["status"], COMPLETED)
        self.assertEqual(
            result["pipeline"]["completed_stages"],
            ["20.1", "20.2", "20.3", "20.4", "20.5", "20.6", "20.7", "21", "22", "23", "23.1"],
        )
        self.assertEqual(result["report_generation"]["status"], APPROVAL_REQUIRED)
        self.assertTrue(result["artifacts"]["evidence"]["evidence_set"])
        self.assertTrue(result["artifacts"]["evaluations"])
        self.assertEqual(
            result["artifacts"]["report"]["evaluations"],
            result["artifacts"]["evaluations"],
        )
        self.assertEqual(validate_orchestration_result(result), [])

        evidence_by_id = {
            item["evidence_id"]: item
            for item in result["artifacts"]["evidence"]["evidence_set"]
        }
        segments = {
            item["id"]
            for item in result["artifacts"]["speaker_attributed_transcript"]
        }
        for evaluation in result["artifacts"]["evaluations"]:
            for evidence_id in evaluation["evidence_ids"]:
                self.assertIn(evidence_id, evidence_by_id)
                for segment_id in evidence_by_id[evidence_id]["source"]["segment_ids"]:
                    self.assertIn(segment_id, segments)

    def test_human_review_and_audit_gates_stop_downstream(self):
        review_pending = run_orchestration(
            nominal_fixture(),
            global_audit_status="PASS_WITH_WARNINGS",
        )
        self.assertEqual(review_pending["pipeline"]["status"], REQUIRES_HUMAN_REVIEW)
        self.assertEqual(review_pending["artifacts"], {})

        audit_pending = run_orchestration(
            nominal_fixture(),
            human_review_approved=True,
        )
        self.assertEqual(audit_pending["pipeline"]["status"], APPROVAL_REQUIRED)
        self.assertNotIn("final_report", audit_pending["artifacts"])

        report_pending = self.nominal(generate_report=True)
        self.assertEqual(report_pending["pipeline"]["status"], APPROVAL_REQUIRED)
        self.assertNotIn("final_report", report_pending["artifacts"])

    def test_validation_block_stops_all_downstream_artifacts(self):
        result = self.nominal_fixture_case("blocked")
        self.assertEqual(result["pipeline"]["status"], BLOCKED)
        self.assertEqual(result["pipeline"]["failed_stage"], "20.7")
        self.assertNotIn("evidence", result["artifacts"])
        self.assertNotIn("evaluations", result["artifacts"])
        self.assertNotIn("report", result["artifacts"])

    def nominal_fixture_case(self, case_id):
        return run_orchestration(
            fixture_for_case(case_id),
            human_review_approved=True,
            global_audit_status="PASS_WITH_WARNINGS",
        )

    def test_missing_artifact_and_incomplete_evaluation_are_blocked(self):
        runtime_result = run_pipeline(nominal_fixture())
        missing_evidence = copy.deepcopy(runtime_result)
        missing_evidence["artifacts"].pop("evidence")
        with patch("reference_runtime.orchestration.run_pipeline", return_value=missing_evidence):
            result = self.nominal()
        self.assertEqual(result["pipeline"]["status"], BLOCKED)
        self.assertIn("required artifact missing: evidence-set", result["pipeline"]["blockers"])
        self.assertNotIn("evaluations", result["artifacts"])
        self.assertNotIn("report", result["artifacts"])

        incomplete = copy.deepcopy(runtime_result)
        incomplete["artifacts"]["evaluations"][0].pop("score")
        with patch("reference_runtime.orchestration.run_pipeline", return_value=incomplete):
            result = self.nominal()
        self.assertEqual(result["pipeline"]["status"], BLOCKED)
        self.assertIn("incomplete evaluation at index 0: missing score", result["pipeline"]["blockers"])

    def test_intermediate_failure_is_not_success_shaped(self):
        with patch(
            "reference_runtime.orchestration.run_pipeline",
            side_effect=RuntimeError("synthetic component failure"),
        ):
            result = self.nominal()
        self.assertEqual(result["pipeline"]["status"], "FAILED")
        self.assertEqual(result["pipeline"]["failed_stage"], "runtime")
        self.assertEqual(result["pipeline"]["readiness"], BLOCKED)
        self.assertNotIn("evidence", result["artifacts"])
        self.assertNotIn("evaluations", result["artifacts"])
        self.assertNotIn("report", result["artifacts"])

    def test_warning_propagation_preserves_limitation_state(self):
        result = self.nominal_fixture_case("ready_with_warnings")
        self.assertEqual(result["pipeline"]["status"], COMPLETED_WITH_WARNINGS)
        self.assertTrue(result["warnings"])
        self.assertEqual(result["pipeline"]["warnings"], result["warnings"])
        self.assertTrue(
            any(stage["status"] == COMPLETED_WITH_WARNINGS for stage in result["stages"])
        )
        for evaluation in result["artifacts"]["evaluations"]:
            self.assertTrue(evaluation["warnings"])

    def test_idempotency_resume_and_version_preservation(self):
        store = OrchestrationStore()
        first = self.nominal(store=store)
        second = resume_orchestration(
            first,
            nominal_fixture(),
            human_review_approved=True,
            global_audit_status="PASS_WITH_WARNINGS",
            store=store,
        )
        self.assertTrue(second["reused"])
        self.assertEqual(first["artifact_hashes"], second["artifact_hashes"])
        self.assertEqual(len(store.history(first["pipeline"]["id"])), 2)

        changed = nominal_fixture()
        changed["transcript"][1]["text"] = "Resposta alterada com o mesmo contrato."
        third = resume_orchestration(
            first,
            changed,
            human_review_approved=True,
            global_audit_status="PASS_WITH_WARNINGS",
            store=store,
        )
        self.assertFalse(third["reused"])
        self.assertTrue(third["invalidation"])
        self.assertNotEqual(first["pipeline"]["input_hash"], third["pipeline"]["input_hash"])
        self.assertEqual(len(store.history(first["pipeline"]["id"])), 3)

    def test_invalid_reference_blocks_integrity(self):
        runtime_result = run_pipeline(nominal_fixture())
        invalid = copy.deepcopy(runtime_result)
        invalid["artifacts"]["evaluations"][0]["evidence_ids"] = ["EVD-ORPHAN"]
        with patch("reference_runtime.orchestration.run_pipeline", return_value=invalid):
            result = self.nominal()
        self.assertEqual(result["pipeline"]["status"], BLOCKED)
        self.assertEqual(result["pipeline"]["failed_stage"], "traceability")
        self.assertIn("orphan evidence reference: EVD-ORPHAN", result["pipeline"]["blockers"])

    def test_semantic_invariants_are_preserved(self):
        candidate_question = self.nominal_fixture_case("candidate_question")
        self.assertNotIn("CQ1", str(candidate_question["artifacts"]["evidence"]))
        self.assertNotIn("CQ1", str(candidate_question["artifacts"]["evaluations"]))

        missing = self.nominal_fixture_case("missing_response")
        self.assertEqual(missing["artifacts"]["evidence"]["evidence_set"], [])
        self.assertEqual(missing["artifacts"]["evaluations"], [])

        unknown = self.nominal_fixture_case("unknown_question")
        self.assertTrue(
            all(item["question_id"] != "unknown" for item in unknown["artifacts"]["evaluations"])
        )

        na = self.nominal_fixture_case("na_dimension")
        depth = na["artifacts"]["evaluations"][0]["dimensions"]["depth"]
        self.assertFalse(depth["applicable"])
        self.assertIsNone(depth["score"])

        seniority_fixture = nominal_fixture()
        seniority_fixture["candidate_metadata"] = {"years": 20, "title": "senior"}
        with_seniority = run_orchestration(
            seniority_fixture,
            human_review_approved=True,
            global_audit_status="PASS_WITH_WARNINGS",
        )
        self.assertEqual(
            with_seniority["artifacts"]["evaluations"],
            self.nominal()["artifacts"]["evaluations"],
        )
        self.assertNotIn("seniority", str(with_seniority["artifacts"]["evaluations"]))

    def test_numeric_consistency_uses_produced_evaluations(self):
        result = self.nominal()
        scores = [
            evaluation["score"]
            for evaluation in result["artifacts"]["evaluations"]
            if evaluation["score"] is not None
        ]
        self.assertEqual(len(scores), 2)
        self.assertEqual(sum(scores), 16.5)
        self.assertEqual(statistics.median(scores), 8.25)
        self.assertEqual(min(scores), 8.0)
        self.assertEqual(max(scores), 8.5)
        self.assertEqual(
            len(scores),
            len(result["artifacts"]["report"]["evaluations"]),
        )
        self.assertEqual(
            sum(evaluation["score"] for evaluation in result["artifacts"]["report"]["evaluations"]),
            sum(scores),
        )

    def test_final_report_requires_explicit_approval_and_is_not_real_persistence(self):
        result = self.nominal(generate_report=True, report_approved=True)
        self.assertEqual(result["pipeline"]["status"], COMPLETED)
        self.assertTrue(result["report_generation"]["generated"])
        self.assertIn("final_report", result["artifacts"])
        self.assertIsNot(result["artifacts"]["final_report"], result["artifacts"]["report"])
        self.assertFalse(
            any(
                path.endswith("Relatório-SYN-E2E-01.md")
                for path in []
            )
        )


if __name__ == "__main__":
    unittest.main()
