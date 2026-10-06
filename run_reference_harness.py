import argparse
from pathlib import Path
import sys

from reference_runtime.harness import default_suites, run_harness, write_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the deterministic reference-runtime harness.")
    parser.add_argument("--root", default=".", help="repository root")
    parser.add_argument("--report", help="optional JSON report path")
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="run suites concurrently in isolated repository copies",
    )
    parser.add_argument(
        "--shared-workspace",
        action="store_true",
        help="disable per-suite filesystem copies (diagnostic mode only)",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    report = run_harness(
        root,
        suites=default_suites(root),
        parallel=args.parallel,
        isolate=not args.shared_workspace,
    )
    if args.report:
        write_report(report, Path(args.report).resolve())
    print(
        f"REFERENCE HARNESS: {report['status']} "
        f"({report['executed']}/{report['planned']} suites, "
        f"{report['failed']} failed)"
    )
    if report["warnings"]:
        print("WARNINGS: " + ", ".join(report["warnings"]))
    return 0 if report["status"] != "FAIL" else 1


if __name__ == "__main__":
    sys.exit(main())
