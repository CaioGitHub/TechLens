import argparse
import unittest


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", default="all", help="all or e2e-01 through e2e-30")
    args = parser.parse_args()
    loader = unittest.defaultTestLoader
    if args.case == "all":
        suite = loader.discover("tests")
    else:
        case_number = int(args.case.split("-")[-1])
        name = f"test_e2e_{case_number:02d}_"
        module = __import__("tests.test_reference_runtime", fromlist=["ReferenceRuntimeTests"])
        methods = [method for method in dir(module.ReferenceRuntimeTests) if method.startswith(name)]
        if not methods:
            parser.error(f"unknown case: {args.case}")
        suite = unittest.TestSuite(
            loader.loadTestsFromName(
                f"tests.test_reference_runtime.ReferenceRuntimeTests.{method}"
            )
            for method in methods
        )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(
        "\ntest_run:\n"
        "  runtime: reference_runtime\n"
        f"  total: {result.testsRun}\n"
        f"  passed: {result.testsRun - len(result.failures) - len(result.errors)}\n"
        f"  failed: {len(result.failures) + len(result.errors)}\n"
        "  blocked: 0\n"
        "  not_executed: 0\n"
        "  status: "
        f"{'PASS' if result.wasSuccessful() else 'FAIL'}"
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
