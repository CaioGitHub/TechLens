"""Deterministic, isolated test harness for the reference runtime."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from typing import Any, Callable, Iterable

from .orchestration import content_hash


HARNESS_VERSION = "26-reference-harness-1"


@dataclass(frozen=True)
class Suite:
    name: str
    command: tuple[str, ...]
    warning_markers: tuple[str, ...] = ()


def default_suites(root: Path) -> tuple[Suite, ...]:
    py = sys.executable
    return (
        Suite("reference_runtime", (py, "run_reference_runtime_tests.py")),
        Suite(
            "stage_24_orchestration",
            (py, "-m", "unittest", "tests.test_stage_24_orchestration"),
        ),
        Suite(
            "stage_25_end_to_end",
            (py, "-m", "unittest", "tests.test_stage_25_end_to_end"),
        ),
        Suite(
            "full_unittest",
            (py, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"),
        ),
        Suite("synthetic_interview", (py, "run_synthetic_interview.py"), ("PASS_WITH_WARNING",)),
        Suite("semantic_blind_calibration", (py, "run_semantic_blind_calibration.py"), ("READY_WITH_WARNINGS",)),
        Suite("adversarial_edge_cases", (py, "run_adversarial_edge_cases.py"), ("PASS_WITH_WARNING", "BLOCKED")),
        Suite(
            "stage_30_1",
            (py, "-m", "unittest", "tests.test_stage_30_1"),
        ),
    )


def _run_suite(
    suite: Suite,
    root: Path,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> dict[str, Any]:
    completed = runner(
        suite.command,
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    output = f"{completed.stdout}\n{completed.stderr}".strip()
    warnings = [
        marker
        for marker in suite.warning_markers
        if marker in output
    ]
    return {
        "name": suite.name,
        "command": list(suite.command),
        "return_code": completed.returncode,
        "status": "PASS" if completed.returncode == 0 else "FAIL",
        "warnings": warnings,
        "output_tail": output[-2000:],
    }


def run_harness(
    root: Path,
    *,
    suites: Iterable[Suite] | None = None,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> dict[str, Any]:
    """Execute suites in order and return a machine-readable harness report."""

    selected = tuple(suites or default_suites(root))
    results = []
    for suite in selected:
        result = _run_suite(suite, root, runner)
        results.append(result)
        if result["return_code"] != 0:
            break
    failed = [result for result in results if result["status"] == "FAIL"]
    warnings = sorted(
        {
            marker
            for result in results
            for marker in result["warnings"]
        }
    )
    report = {
        "harness_version": HARNESS_VERSION,
        "runtime": "reference_runtime",
        "input": "synthetic fixtures only",
        "execution_id": content_hash([suite.name for suite in selected])[:16],
        "suites": results,
        "executed": len(results),
        "planned": len(selected),
        "failed": len(failed),
        "warnings": warnings,
        "status": "FAIL" if failed else ("PASS_WITH_WARNINGS" if warnings else "PASS"),
        "real_interview_processed": False,
        "real_report_generated": False,
        "simulated_approvals_only": True,
    }
    return report


def write_report(report: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def deterministic_projection(value: Any) -> Any:
    """Remove operational timestamps while preserving all test-relevant data."""

    if isinstance(value, dict):
        return {
            key: deterministic_projection(item)
            for key, item in value.items()
            if key not in {"started_at", "completed_at"}
        }
    if isinstance(value, list):
        return [deterministic_projection(item) for item in value]
    return deepcopy(value)


def assert_synthetic_fixtures(root: Path) -> None:
    """Reject obvious real-interview identifiers from fixture modules."""

    forbidden = (
        "Candidato-Piloto-01",
        "REAL-PILOT",
        "Individual Evaluations v2",
        "Interview Evaluation v1",
        "Relatório-Candidato",
    )
    fixture_sources = (
        root / "tests" / "fixtures.py",
        root / "tests" / "synthetic_interview.py",
        root / "tests" / "calibration_cases.py",
        root / "tests" / "adversarial_cases.py",
    )
    for path in fixture_sources:
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        for marker in forbidden:
            if marker in content:
                raise AssertionError(f"real-interview marker in fixture/test source: {marker}")


def temporary_workspace() -> TemporaryDirectory[str]:
    """Return an isolated workspace owned by the caller."""

    return TemporaryDirectory(prefix="techlens-reference-harness-")
