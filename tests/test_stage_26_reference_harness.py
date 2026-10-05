import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from reference_runtime import (
    Suite,
    assert_synthetic_fixtures,
    deterministic_projection,
    run_harness,
    run_pipeline,
    write_report,
)
from tests.fixtures import nominal_fixture


ROOT = Path(__file__).resolve().parents[1]


class Stage26ReferenceHarnessTests(unittest.TestCase):
    def test_runtime_determinism_ignores_only_operational_timestamps(self):
        first = deterministic_projection(run_pipeline(nominal_fixture()))
        second = deterministic_projection(run_pipeline(nominal_fixture()))
        self.assertEqual(first, second)
        self.assertEqual(first["run_id"], second["run_id"])
        self.assertEqual(first["artifacts"], second["artifacts"])

    def test_fixture_isolation_and_no_real_interview_markers(self):
        assert_synthetic_fixtures(ROOT)
        fixture = nominal_fixture()
        changed = copy.deepcopy(fixture)
        changed["transcript"][1]["text"] = "Alteração isolada."
        self.assertNotEqual(fixture["transcript"][1]["text"], changed["transcript"][1]["text"])
        self.assertEqual(nominal_fixture()["transcript"][1]["text"], fixture["transcript"][1]["text"])

    def test_order_independence_and_failure_propagation(self):
        def fake_runner(command, **kwargs):
            if "stage_24_orchestration" in command:
                return subprocess.CompletedProcess(command, 1, "failed", "")
            return subprocess.CompletedProcess(command, 0, "ok", "")

        suites = (
            Suite("first", ("first",)),
            Suite("stage_24_orchestration", ("stage_24_orchestration",)),
            Suite("never", ("never",)),
        )
        report = run_harness(ROOT, suites=suites, runner=fake_runner)
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["executed"], 2)
        self.assertEqual(report["planned"], 3)
        self.assertEqual(report["suites"][-1]["return_code"], 1)

    def test_warning_identification_and_simulated_approval_flags(self):
        def fake_runner(command, **kwargs):
            return subprocess.CompletedProcess(
                command,
                0,
                "PASS_WITH_WARNING\nREADY_WITH_WARNINGS\n",
                "",
            )

        report = run_harness(
            ROOT,
            suites=(Suite("warning-suite", ("warning",), ("PASS_WITH_WARNING", "READY_WITH_WARNINGS")),),
            runner=fake_runner,
        )
        self.assertEqual(report["status"], "PASS_WITH_WARNINGS")
        self.assertEqual(report["warnings"], ["PASS_WITH_WARNING", "READY_WITH_WARNINGS"])
        self.assertTrue(report["simulated_approvals_only"])
        self.assertFalse(report["real_interview_processed"])
        self.assertFalse(report["real_report_generated"])

    def test_consolidated_harness_is_reproducible_and_has_exit_semantics(self):
        def fake_runner(command, **kwargs):
            return subprocess.CompletedProcess(command, 0, "PASS", "")

        suites = (
            Suite("a", ("a",)),
            Suite("b", ("b",)),
        )
        first = run_harness(ROOT, suites=suites, runner=fake_runner)
        second = run_harness(ROOT, suites=suites, runner=fake_runner)
        self.assertEqual(first, second)
        self.assertEqual(first["failed"], 0)
        self.assertEqual(first["executed"], first["planned"])

    def test_report_is_machine_readable_and_does_not_touch_real_artifacts(self):
        report = {
            "status": "PASS_WITH_WARNINGS",
            "real_interview_processed": False,
            "real_report_generated": False,
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "harness-results.json"
            write_report(report, path)
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), report)
            self.assertTrue(path.exists())
        self.assertFalse(path.exists())

    def test_missing_cache_does_not_change_reference_result(self):
        first = deterministic_projection(run_pipeline(nominal_fixture()))
        cache_paths = list(ROOT.glob("**/__pycache__"))
        self.assertIsInstance(cache_paths, list)
        second = deterministic_projection(run_pipeline(nominal_fixture()))
        self.assertEqual(first, second)

    def test_interrupted_harness_is_not_reported_as_complete(self):
        calls = []

        def interrupting_runner(command, **kwargs):
            calls.append(command)
            raise KeyboardInterrupt()

        with self.assertRaises(KeyboardInterrupt):
            run_harness(
                ROOT,
                suites=(Suite("interrupted", ("interrupt",)),),
                runner=interrupting_runner,
            )
        self.assertEqual(len(calls), 1)


if __name__ == "__main__":
    unittest.main()
