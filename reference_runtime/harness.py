"""Deterministic, isolated test harness for the reference runtime."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
from time import monotonic
from typing import Any, Callable, Iterable
from concurrent.futures import ThreadPoolExecutor

from .orchestration import content_hash


HARNESS_VERSION = "26-reference-harness-2"


@dataclass(frozen=True)
class Suite:
    name: str
    command: tuple[str, ...]
    warning_markers: tuple[str, ...] = ()
    dependencies: tuple[str, ...] = ()
    fixture_strategy: str = "isolated-copy"


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
    *,
    workspace: Path | None = None,
) -> dict[str, Any]:
    started = monotonic()
    errors: list[str] = []
    try:
        completed = runner(
            suite.command,
            cwd=workspace or root,
            capture_output=True,
            text=True,
            check=False,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        output = f"{completed.stdout}\n{completed.stderr}".strip()
        return_code = completed.returncode
    except Exception as error:
        output = ""
        return_code = 1
        errors.append(f"{type(error).__name__}: {error}")
    warnings = [
        marker
        for marker in suite.warning_markers
        if marker in output
    ]
    if return_code != 0:
        errors.append(output[-2000:] or "suite returned a non-zero exit code")
    blocked = "BLOCKED" in output and return_code != 0
    status = "BLOCKED" if blocked else ("FAIL" if return_code != 0 else (
        "PASS_WITH_WARNINGS" if warnings else "PASS"
    ))
    return {
        "id": suite.name,
        "name": suite.name,
        "command": list(suite.command),
        "status": status,
        "duration_ms": round((monotonic() - started) * 1000, 3),
        "return_code": return_code,
        "warnings": warnings,
        "errors": errors,
        "artifacts": [],
        "fixture_strategy": suite.fixture_strategy,
        "output_tail": output[-2000:],
    }


def _copy_workspace(root: Path, destination: Path) -> None:
    ignored = shutil.ignore_patterns(
        ".git",
        "__pycache__",
        ".pytest_cache",
        "stage25-harness-report.json",
        "stage26-harness-report.json",
    )
    shutil.copytree(root, destination, ignore=ignored)


def _run_isolated_suite(
    suite: Suite,
    root: Path,
    workspace_root: Path,
    runner: Callable[..., subprocess.CompletedProcess[str]],
) -> dict[str, Any]:
    workspace = workspace_root / suite.name
    _copy_workspace(root, workspace)
    return _run_suite(suite, root, runner, workspace=workspace)


def run_harness(
    root: Path,
    *,
    suites: Iterable[Suite] | None = None,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    parallel: bool = False,
    isolate: bool = True,
) -> dict[str, Any]:
    """Execute independent suites with per-suite filesystem isolation."""

    selected = tuple(suites or default_suites(root))
    with TemporaryDirectory(prefix="techlens-reference-harness-") as directory:
        workspace_root = Path(directory)
        if parallel:
            with ThreadPoolExecutor(max_workers=len(selected) or 1) as executor:
                futures = [
                    executor.submit(
                        _run_isolated_suite if isolate else _run_suite,
                        suite,
                        root,
                        workspace_root,
                        runner,
                    )
                    if isolate
                    else executor.submit(_run_suite, suite, root, runner)
                    for suite in selected
                ]
                results = [future.result() for future in futures]
        else:
            results = [
                _run_isolated_suite(suite, root, workspace_root, runner)
                if isolate
                else _run_suite(suite, root, runner)
                for suite in selected
            ]
    failed = [result for result in results if result["status"] == "FAIL"]
    blocked = [result for result in results if result["status"] == "BLOCKED"]
    warning_suites = [
        result for result in results
        if result["status"] == "PASS_WITH_WARNINGS"
    ]
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
        "blocked": len(blocked),
        "passed": sum(result["status"] == "PASS" for result in results),
        "warnings_count": len(warning_suites),
        "parallel": parallel,
        "isolated": isolate,
        "warnings": warnings,
        "status": (
            "FAIL"
            if failed
            else ("PASS_WITH_WARNINGS" if warnings or blocked else "PASS")
        ),
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
            if key not in {"started_at", "completed_at", "duration_ms"}
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
