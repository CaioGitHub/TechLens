import tempfile
import unittest
from pathlib import Path

from reference_runtime import (
    PilotPaths,
    detect_stale_artifacts,
    run_interview_pipeline,
    semantic_projection,
)
from tests.fixtures import fixture_for_case, nominal_fixture


ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "11 - Interview Evaluation" / "09 - Real Interview Pilot" / "Candidato-Piloto-01"


class Stage24PipelineOrchestrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.paths = PilotPaths(
            PILOT / "Individual Evaluations v2.md",
            PILOT / "Evidence Set v1.md",
            PILOT / "Interview Evaluation v2.md",
            PILOT / "Structured Interview - Controlled Correction v6.md",
            PILOT / "Stage 23.1 — Global Evaluation Semantic Audit.md",
        )

    def test_happy_path_runs_all_stages(self):
        result = run_interview_pipeline(self.paths)
        self.assertEqual(result["pipeline"]["status"], "READY_WITH_WARNINGS")
        self.assertEqual([item["stage"] for item in result["stages"]], [
            "20.7", "21", "22", "23", "23.1", "23.2"
        ])
        self.assertEqual(result["artifacts"]["evaluation_result"]["summary"]["average_score"], 4.7)
        self.assertTrue(result["readiness"]["ready_for_next_stage"])

    def test_blocked_20_7_stops_downstream(self):
        result = run_interview_pipeline(
            self.paths,
            stage_overrides={"20.7": {"status": "BLOCKED", "gate": "BLOCKED"}},
        )
        self.assertEqual(result["pipeline"]["status"], "BLOCKED")
        self.assertEqual(result["pipeline"]["failed_stage"], "20.7")
        self.assertNotIn("23", [item["stage"] for item in result["stages"]])

    def test_warning_20_7_is_propagated(self):
        result = run_interview_pipeline(
            self.paths,
            stage_overrides={
                "20.7": {
                    "status": "READY_WITH_WARNINGS",
                    "gate": "TRANSCRIPTION_PROCESSING_COMPLETE",
                    "warnings": ["W-001: speaker review required"],
                }
            },
        )
        self.assertEqual(result["pipeline"]["status"], "READY_WITH_WARNINGS")
        self.assertIn("W-001: speaker review required", result["warnings"])

    def test_blocked_21_stops_22_and_later(self):
        result = run_interview_pipeline(
            self.paths,
            stage_overrides={"21": {"status": "BLOCKED", "gate": "BLOCKED"}},
        )
        self.assertEqual(result["pipeline"]["failed_stage"], "21")
        self.assertNotIn("23.1", [item["stage"] for item in result["stages"]])

    def test_blocked_23_stops_audit_and_materialization(self):
        result = run_interview_pipeline(
            self.paths,
            stage_overrides={"23": {"status": "BLOCKED", "gate": "BLOCKED"}},
        )
        self.assertEqual(result["pipeline"]["failed_stage"], "23")
        self.assertNotIn("23.1", [item["stage"] for item in result["stages"]])

    def test_audit_failure_blocks_materialization(self):
        result = run_interview_pipeline(
            self.paths,
            stage_overrides={"23.1": {"status": "READY", "gate": "BLOCKED"}},
        )
        self.assertEqual(result["pipeline"]["status"], "BLOCKED")
        self.assertNotIn("23.2", [item["stage"] for item in result["stages"]])

    def test_warnings_from_multiple_stages_are_preserved(self):
        result = run_interview_pipeline(
            self.paths,
            stage_overrides={
                "20.7": {"status": "READY_WITH_WARNINGS", "warnings": ["W-20.7"]},
                "23.1": {"status": "READY_WITH_WARNINGS", "gate": "GLOBAL_EVALUATION_AUDIT_COMPLETE_WITH_WARNINGS", "warnings": ["W-23.1"]},
            },
        )
        self.assertIn("W-20.7", result["warnings"])
        self.assertIn("W-23.1", result["warnings"])

    def test_confidence_is_separate_from_pipeline_status(self):
        result = run_interview_pipeline(self.paths)
        self.assertEqual(result["confidence"]["evaluation"], "medium")
        self.assertNotIn("seniority", result)
        self.assertNotIn("pipeline_confidence", result)

    def test_needs_review_is_preserved_in_structured_runtime(self):
        result = run_interview_pipeline(fixture_for_case("needs_review"))
        self.assertEqual(result["pipeline"]["status"], "READY_WITH_WARNINGS")
        self.assertTrue(any(item.get("needs_review") for item in result["artifacts"]["responses"]))

    def test_traceability_is_preserved(self):
        result = run_interview_pipeline(self.paths)
        trace = result["traceability"]
        self.assertEqual(len(trace["question_ids"]), 10)
        self.assertEqual(len(trace["evaluation_ids"]), 10)
        self.assertEqual(len(trace["evidence_ids"]), 28)

    def test_idempotency_ignores_operational_timestamps(self):
        first = run_interview_pipeline(self.paths, run_id="same-run")
        second = run_interview_pipeline(self.paths, run_id="same-run", previous_result=first)
        self.assertEqual(semantic_projection(first), semantic_projection(second))
        self.assertTrue(second["reused"])

    def test_stale_artifacts_are_blocked(self):
        versions = {
            "transcript": "A",
            "structured_interview": "B",
            "evidence_set": "B",
        }
        self.assertEqual(detect_stale_artifacts(versions), ["structured_interview"])
        result = run_interview_pipeline(self.paths, artifact_versions=versions)
        self.assertEqual(result["pipeline"]["status"], "BLOCKED")
        self.assertIn("structured_interview", result["stale_artifacts"])

    def test_partial_failure_preserves_previous_artifacts(self):
        result = run_interview_pipeline(
            nominal_fixture(),
            stage_overrides={"23": {"status": "FAILED", "gate": "FAILED"}},
        )
        self.assertEqual(result["pipeline"]["status"], "FAILED")
        self.assertIn("questions", result["artifacts"])
        self.assertNotIn("23.1", [item["stage"] for item in result["stages"]])

    def test_reprocessing_same_run_reuses_result(self):
        first = run_interview_pipeline(self.paths, run_id="reprocess")
        second = run_interview_pipeline(self.paths, run_id="reprocess", previous_result=first)
        self.assertTrue(second["reused"])
        self.assertEqual(first["artifacts"], second["artifacts"])

    def test_v1_is_not_an_operational_input(self):
        with tempfile.TemporaryDirectory() as directory:
            corrupted = Path(directory) / "Interview Evaluation v1.md"
            corrupted.write_text("average: 9.9\nconfidence: high\n", encoding="utf-8")
            result = run_interview_pipeline(self.paths)
        self.assertEqual(result["artifacts"]["evaluation_result"]["summary"]["average_score"], 4.7)
        self.assertNotIn("Interview Evaluation v1.md", str(result["artifacts"]["evaluation_result"]["input"]))

    def test_no_hiring_or_seniority_output(self):
        result = run_interview_pipeline(self.paths)
        serialized = repr(result).lower()
        self.assertNotIn("hiring_decision", serialized)
        self.assertNotIn("seniority", serialized)
        self.assertNotIn("contratar", serialized)

    def test_job_context_does_not_change_canonical_result(self):
        first = run_interview_pipeline(self.paths)
        second = run_interview_pipeline(self.paths)
        self.assertEqual(
            first["artifacts"]["evaluation_result"]["summary"],
            second["artifacts"]["evaluation_result"]["summary"],
        )

    def test_orchestrator_does_not_duplicate_scoring(self):
        result = run_interview_pipeline(self.paths)
        self.assertEqual(
            result["artifacts"]["evaluation_result"]["summary"]["average_score"],
            4.7,
        )
        self.assertNotIn("individual_scores", result)

    def test_orchestrator_does_not_create_evidence(self):
        result = run_interview_pipeline(self.paths)
        self.assertEqual(len(result["traceability"]["evidence_ids"]), 28)
        self.assertEqual(result["artifacts"]["evaluation_result"]["traceability"]["new_evidence_created"], False)

    def test_stage_order_is_monotonic(self):
        result = run_interview_pipeline(self.paths)
        indexes = [("20.7", "21", "22", "23", "23.1", "23.2").index(item["stage"]) for item in result["stages"]]
        self.assertEqual(indexes, sorted(indexes))


if __name__ == "__main__":
    unittest.main()
