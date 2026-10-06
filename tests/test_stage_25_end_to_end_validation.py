import hashlib
import tempfile
import unittest
from pathlib import Path

from reference_runtime import (
    PilotPaths,
    run_interview_pipeline,
    semantic_projection,
)
from tests.fixtures import fixture_for_case, nominal_fixture


ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "11 - Interview Evaluation" / "09 - Real Interview Pilot" / "Candidato-Piloto-01"


class Stage25EndToEndValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evaluations = PILOT / "Individual Evaluations v2.md"
        cls.evidence = PILOT / "Evidence Set v1.md"
        cls.v1 = PILOT / "Interview Evaluation v1.md"
        cls.v2 = PILOT / "Interview Evaluation v2.md"
        cls.structured = PILOT / "Structured Interview - Controlled Correction v6.md"
        cls.paths_protected = (
            cls.evaluations,
            cls.evidence,
            cls.v1,
            cls.v2,
            cls.structured,
        )

    def run_pilot(self, **kwargs):
        with tempfile.TemporaryDirectory() as directory:
            paths = PilotPaths(
                self.evaluations,
                self.evidence,
                Path(directory) / "Interview Evaluation v2.md",
                self.structured,
                PILOT / "Stage 23.1 — Global Evaluation Semantic Audit.md",
            )
            return run_interview_pipeline(paths, **kwargs)

    def test_e2e_01_happy_path(self):
        result = self.run_pilot()
        self.assertIn(result["pipeline"]["status"], {"READY", "READY_WITH_WARNINGS"})
        self.assertEqual(
            [stage["stage"] for stage in result["stages"]],
            ["20.7", "21", "22", "23", "23.1", "23.2"],
        )
        self.assertIn("evaluation_result", result["artifacts"])
        self.assertIn("global_audit", result["artifacts"])
        self.assertTrue(result["readiness"]["ready_for_next_stage"])

    def test_e2e_02_integrated_result_matches_baseline(self):
        result = self.run_pilot()
        runtime = result["artifacts"]["evaluation_result"]
        self.assertEqual(runtime["summary"]["questions_evaluated"], 10)
        self.assertEqual(runtime["summary"]["average_score"], 4.7)
        self.assertEqual(runtime["summary"]["median_score"], 4.0)
        self.assertEqual(runtime["summary"]["minimum_score"], 2.0)
        self.assertEqual(runtime["summary"]["maximum_score"], 8.0)
        self.assertEqual(runtime["summary"]["confidence"], "medium")
        self.assertEqual(runtime["distribution"], {"0–2": 0, "2–4": 1, "4–6": 6, "6–8": 2, "8–10": 1})
        self.assertEqual(result["artifacts"]["global_audit"]["evidence_count"], 28)

    def test_e2e_03_traceability_is_complete(self):
        result = self.run_pilot()
        trace = result["traceability"]
        self.assertEqual(len(trace["question_ids"]), 10)
        self.assertEqual(len(trace["evaluation_ids"]), 10)
        self.assertEqual(len(trace["evidence_ids"]), 28)
        self.assertEqual(
            set(trace["evaluation_ids"]),
            set(result["artifacts"]["evaluation_result"]["traceability"]["evaluation_ids"]),
        )

    def test_e2e_04_missing_response_remains_missing(self):
        result = run_interview_pipeline(fixture_for_case("missing_response"))
        missing = [item for item in result["artifacts"]["responses"] if item["response_status"] == "missing"]
        self.assertTrue(missing)
        self.assertTrue(all(item["text"] is None for item in missing))
        self.assertNotIn("does not know", repr(result).lower())

    def test_e2e_05_unknown_response_is_preserved_and_unlinked(self):
        result = run_interview_pipeline(fixture_for_case("unknown_question"))
        unknown = [item for item in result["artifacts"]["responses"] if item["question_id"] == "unknown"]
        self.assertTrue(unknown)
        self.assertTrue(all(item["response_status"] == "identified" for item in unknown))
        self.assertTrue(all(item["response_id"] in result["traceability"]["response_ids"] for item in unknown))
        self.assertFalse(any(item["response_id"] == unknown[0]["response_id"] for item in result["artifacts"]["evaluations"]))

    def test_e2e_06_needs_review_survives_handoffs(self):
        result = run_interview_pipeline(fixture_for_case("needs_review"))
        self.assertEqual(result["pipeline"]["status"], "READY_WITH_WARNINGS")
        self.assertTrue(any(item.get("needs_review") for item in result["artifacts"]["responses"]))
        self.assertFalse(any("needs_review" in item for item in result["artifacts"]["evaluations"]))

    def test_e2e_07_warning_propagation(self):
        result = self.run_pilot(
            stage_overrides={
                "20.7": {"status": "READY_WITH_WARNINGS", "warnings": ["W-20.7"]},
                "23.1": {
                    "status": "READY_WITH_WARNINGS",
                    "gate": "GLOBAL_EVALUATION_AUDIT_COMPLETE_WITH_WARNINGS",
                    "warnings": ["W-23.1"],
                },
            }
        )
        self.assertIn("W-20.7", result["warnings"])
        self.assertIn("W-23.1", result["warnings"])

    def test_e2e_08_blocked_propagation(self):
        for stage in ("20.7", "21", "23"):
            result = self.run_pilot(stage_overrides={stage: {"status": "BLOCKED", "gate": "BLOCKED"}})
            self.assertEqual(result["pipeline"]["status"], "BLOCKED")
            self.assertEqual(result["pipeline"]["failed_stage"], stage)
            executed = [item["stage"] for item in result["stages"]]
            downstream = {"20.7": {"21", "22", "23", "23.1", "23.2"}, "21": {"22", "23", "23.1", "23.2"}, "23": {"23.1", "23.2"}}[stage]
            self.assertTrue(downstream.isdisjoint(executed))

    def test_e2e_09_materialization_requires_audit_gate(self):
        result = self.run_pilot(stage_overrides={"23.1": {"status": "BLOCKED", "gate": "BLOCKED"}})
        self.assertEqual(result["pipeline"]["status"], "BLOCKED")
        self.assertNotIn("23.2", [item["stage"] for item in result["stages"]])
        self.assertNotIn("interview_evaluation_v2", result["artifacts"])

    def test_e2e_10_v1_is_not_operational_input(self):
        before = self.v1.read_bytes()
        result = self.run_pilot()
        after = self.v1.read_bytes()
        self.assertEqual(before, after)
        self.assertNotIn("Interview Evaluation v1.md", str(result["artifacts"]["evaluation_result"]["input"]))
        self.assertEqual(result["artifacts"]["evaluation_result"]["summary"]["average_score"], 4.7)

    def test_e2e_11_job_context_isolation(self):
        first = self.run_pilot()
        second = self.run_pilot()
        self.assertEqual(
            first["artifacts"]["evaluation_result"]["summary"],
            second["artifacts"]["evaluation_result"]["summary"],
        )
        self.assertNotIn("job_context", second)

    def test_e2e_12_seniority_isolation(self):
        result = self.run_pilot()
        serialized = repr(result).lower()
        for term in ("junior", "pleno", "senior", "especialista"):
            self.assertNotIn(term, serialized)

    def test_e2e_13_hiring_isolation(self):
        result = self.run_pilot()
        serialized = repr(result).lower()
        for term in ("aprovado", "reprovado", "contratar", "não contratar", "melhor candidato"):
            self.assertNotIn(term, serialized)

    def test_e2e_14_surface_and_metadata_invariance(self):
        base = fixture_for_case("hypothetical_answer")
        verbose = fixture_for_case("hypothetical_answer")
        verbose["transcript"][1]["text"] += " " + ("contexto técnico " * 40)
        first = run_interview_pipeline(base)
        second = run_interview_pipeline(verbose)
        self.assertEqual(
            first["artifacts"]["evaluations"][0]["score"],
            second["artifacts"]["evaluations"][0]["score"],
        )

    def test_e2e_15_hypothetical_is_not_experience(self):
        fixture = fixture_for_case("hypothetical_answer")
        fixture["transcript"][1]["text"] = "Eu faria uma investigação por p95 e dependências."
        fixture["evidence_specs"] = {}
        result = run_interview_pipeline(fixture)
        response_evidence = [
            item for item in result["artifacts"]["evidence"]["evidence_set"]
            if item["response_id"] == "R1"
        ]
        self.assertIn("hypothesis", {item["type"] for item in response_evidence})
        self.assertNotIn("demonstrated_experience", {item["type"] for item in response_evidence})

    def test_e2e_16_experience_declaration_remains_distinct(self):
        result = run_interview_pipeline(fixture_for_case("experience_declaration"))
        response_evidence = [
            item for item in result["artifacts"]["evidence"]["evidence_set"]
            if item["response_id"] == "R1"
        ]
        self.assertIn("experience_declaration", {item["type"] for item in response_evidence})
        self.assertNotIn("demonstrated_experience", {item["type"] for item in response_evidence})

    def test_e2e_17_self_correction_preserves_original_response(self):
        fixture = fixture_for_case("self_correction")
        fixture["evidence_specs"] = {}
        result = run_interview_pipeline(fixture)
        response = next(
            item for item in result["artifacts"]["reconstructed_responses"]
            if item["response_id"] == "R1"
        )
        self.assertIn("Eu usaria X.", response["original_text"])
        self.assertIn("Pensando melhor", response["reconstructed_text"])
        self.assertTrue(any(item["type"] == "self_correction" for item in result["artifacts"]["evidence"]["evidence_set"]))

    def test_e2e_18_contradiction_preserves_both_responses(self):
        result = run_interview_pipeline(fixture_for_case("technical_error"))
        self.assertEqual(len(result["artifacts"]["responses"]), 2)
        self.assertTrue(result["artifacts"]["evidence"]["evidence_set"])
        self.assertEqual(
            {item["response_id"] for item in result["artifacts"]["evidence"]["evidence_set"]},
            {"R1", "R1.1"},
        )

    def test_e2e_19_critical_error_is_not_universal_rejection(self):
        result = run_interview_pipeline(fixture_for_case("critical_error"))
        self.assertEqual(result["pipeline"]["status"], "READY")
        self.assertNotIn("reprovado", repr(result).lower())

    def test_e2e_20_excluded_material_is_not_reintroduced(self):
        result = self.run_pilot()
        serialized = repr(result)
        for token in ("R31", "RAW-065", "Scroll", "R24", "R26", "R41", "R52", "CQ1"):
            self.assertNotIn(token, serialized)

    def test_e2e_21_idempotency(self):
        first = self.run_pilot(run_id="e2e-idempotent")
        second = self.run_pilot(run_id="e2e-idempotent", previous_result=first)
        self.assertEqual(semantic_projection(first), semantic_projection(second))
        self.assertTrue(second["reused"])

    def test_e2e_22_stale_artifact_detection(self):
        result = self.run_pilot(
            artifact_versions={
                "transcript": "A",
                "structured_interview": "B",
                "evidence_set": "B",
            }
        )
        self.assertEqual(result["pipeline"]["status"], "BLOCKED")
        self.assertIn("structured_interview", result["stale_artifacts"])

    def test_e2e_23_partial_failure_preserves_prior_artifacts(self):
        result = run_interview_pipeline(
            nominal_fixture(),
            stage_overrides={"23": {"status": "FAILED", "gate": "FAILED"}},
        )
        self.assertEqual(result["pipeline"]["status"], "FAILED")
        self.assertIn("questions", result["artifacts"])
        self.assertIn("evidence", result["artifacts"])
        self.assertNotIn("23.1", [item["stage"] for item in result["stages"]])

    def test_e2e_24_reprocessing_after_failure(self):
        failed = run_interview_pipeline(
            nominal_fixture(),
            stage_overrides={"23": {"status": "FAILED", "gate": "FAILED"}},
        )
        recovered = run_interview_pipeline(nominal_fixture(), run_id="recovered")
        self.assertEqual(failed["pipeline"]["status"], "FAILED")
        self.assertIn("23.1", [item["stage"] for item in recovered["stages"]])
        self.assertIn("23.2", [item["stage"] for item in recovered["stages"]])

    def test_e2e_25_full_pilot_regression_and_protected_artifacts(self):
        hashes_before = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in self.paths_protected}
        result = self.run_pilot()
        hashes_after = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in self.paths_protected}
        self.assertEqual(hashes_before, hashes_after)
        self.assertEqual(result["artifacts"]["evaluation_result"]["summary"]["average_score"], 4.7)
        self.assertEqual(result["artifacts"]["global_audit"]["mathematical_validation"], "PASS")

    def test_stage25_does_not_reimplement_stage24(self):
        result = self.run_pilot()
        self.assertIn("23.2", [item["stage"] for item in result["stages"]])
        self.assertNotIn("individual_scores", result)
        self.assertIn("evaluation_result", result["artifacts"])


if __name__ == "__main__":
    unittest.main()
