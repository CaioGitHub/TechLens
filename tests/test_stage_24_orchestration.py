import unittest

from reference_runtime import (
    APPROVAL_REQUIRED,
    BLOCKED,
    COMPLETED,
    COMPLETED_WITH_WARNINGS,
    OrchestrationStore,
    REQUIRES_HUMAN_REVIEW,
    resume_orchestration,
    run_orchestration,
    validate_orchestration_result,
)
from tests.fixtures import fixture_for_case, nominal_fixture


class Stage24OrchestrationTests(unittest.TestCase):
    def run_valid(self, fixture=None, **kwargs):
        return run_orchestration(
            fixture or nominal_fixture(),
            human_review_approved=True,
            global_audit_status="PASS_WITH_WARNINGS",
            **kwargs,
        )

    def test_complete_flow_requires_explicit_human_review(self):
        result = run_orchestration(
            nominal_fixture(),
            global_audit_status="PASS_WITH_WARNINGS",
        )
        self.assertEqual(result["pipeline"]["status"], REQUIRES_HUMAN_REVIEW)
        self.assertEqual(result["pipeline"]["readiness"], APPROVAL_REQUIRED)
        self.assertEqual(result["artifacts"], {})

        approved = self.run_valid()
        self.assertEqual(approved["pipeline"]["status"], COMPLETED)
        self.assertEqual(
            approved["pipeline"]["completed_stages"],
            ["20.1", "20.2", "20.3", "20.4", "20.5", "20.6", "20.7", "21", "22", "23", "23.1"],
        )

    def test_blocked_validation_stops_downstream(self):
        result = self.run_valid(fixture_for_case("blocked"))
        self.assertEqual(result["pipeline"]["status"], BLOCKED)
        self.assertEqual(result["pipeline"]["failed_stage"], "20.7")
        self.assertNotIn("evidence", result["artifacts"])
        self.assertNotIn("evaluations", result["artifacts"])
        self.assertNotIn("report", result["artifacts"])

    def test_missing_required_artifact_is_failed_before_execution(self):
        fixture = nominal_fixture()
        del fixture["participants"]
        result = run_orchestration(
            fixture,
            human_review_approved=True,
            global_audit_status="PASS",
        )
        self.assertEqual(result["pipeline"]["status"], "FAILED")
        self.assertEqual(result["pipeline"]["failed_stage"], "input")
        self.assertEqual(result["artifacts"], {})

    def test_warning_is_propagated_without_becoming_candidate_evidence(self):
        result = self.run_valid(fixture_for_case("ready_with_warnings"))
        self.assertEqual(result["pipeline"]["status"], COMPLETED_WITH_WARNINGS)
        self.assertTrue(result["warnings"])
        self.assertTrue(result["pipeline"]["warnings"])
        for item in result["artifacts"]["evidence"]["evidence_set"]:
            self.assertNotIn("warning", item.get("qualification", "").lower())

    def test_report_requires_audit_and_explicit_report_approval(self):
        no_audit = run_orchestration(
            nominal_fixture(),
            human_review_approved=True,
        )
        self.assertEqual(no_audit["pipeline"]["status"], APPROVAL_REQUIRED)
        self.assertNotIn("final_report", no_audit["artifacts"])

        not_approved = self.run_valid(generate_report=True)
        self.assertEqual(not_approved["pipeline"]["status"], APPROVAL_REQUIRED)
        self.assertNotIn("final_report", not_approved["artifacts"])

        approved = self.run_valid(generate_report=True, report_approved=True)
        self.assertIn("final_report", approved["artifacts"])
        self.assertTrue(approved["report_generation"]["generated"])

    def test_idempotent_resume_reuses_same_content(self):
        first = self.run_valid()
        second = resume_orchestration(
            first,
            nominal_fixture(),
            human_review_approved=True,
            global_audit_status="PASS_WITH_WARNINGS",
        )
        self.assertTrue(second["reused"])
        self.assertEqual(first["artifact_hashes"], second["artifact_hashes"])
        self.assertEqual(first["pipeline"]["input_hash"], second["pipeline"]["input_hash"])

    def test_input_change_invalidates_dependents_and_preserves_previous_version(self):
        store = OrchestrationStore()
        first = self.run_valid()
        store.record(first)
        changed = nominal_fixture()
        changed["transcript"][1]["text"] = "Resposta alterada."
        second = resume_orchestration(
            first,
            changed,
            human_review_approved=True,
            global_audit_status="PASS_WITH_WARNINGS",
            store=store,
        )
        self.assertFalse(second["reused"])
        self.assertTrue(second["invalidation"])
        self.assertNotEqual(first["pipeline"]["input_hash"], second["pipeline"]["input_hash"])
        self.assertEqual(len(store.history(first["pipeline"]["id"])), 2)

    def test_versions_are_not_overwritten(self):
        store = OrchestrationStore()
        first = self.run_valid(store=store)
        second = run_orchestration(
            nominal_fixture(),
            human_review_approved=True,
            global_audit_status="PASS_WITH_WARNINGS",
            store=store,
        )
        self.assertEqual(first["pipeline"]["id"], second["pipeline"]["id"])
        self.assertEqual(len(store.history(first["pipeline"]["id"])), 2)

    def test_invalid_traceability_blocks_or_is_detectable(self):
        result = self.run_valid()
        result["artifacts"]["evaluations"][0]["evidence_ids"] = ["EVD-MISSING"]
        issues = validate_orchestration_result(result)
        self.assertIn("orphan evidence reference: EVD-MISSING", issues)

    def test_excluded_candidate_question_does_not_enter_evidence(self):
        result = self.run_valid(fixture_for_case("candidate_question"))
        evidence_ids = {
            item["response_id"]
            for item in result["artifacts"]["evidence"]["evidence_set"]
        }
        self.assertNotIn("CQ1", evidence_ids)
        self.assertNotIn("CQ1", str(result["artifacts"]["evaluations"]))

    def test_report_handoff_does_not_recalculate_evaluations(self):
        result = self.run_valid()
        self.assertEqual(
            result["artifacts"]["report"]["evaluations"],
            result["artifacts"]["evaluations"],
        )
        self.assertNotIn("score", result["artifacts"]["evidence"]["evidence_set"][0])


if __name__ == "__main__":
    unittest.main()
