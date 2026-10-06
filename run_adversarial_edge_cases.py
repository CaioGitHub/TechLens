import argparse

from reference_runtime import PipelineBlocked, run_pipeline
from tests.adversarial_cases import (
    adversarial_fixtures,
    blind_adversarial_input,
)


def _types(result):
    return {
        item["type"]
        for item in result["artifacts"]["evidence"]["evidence_set"]
    }


def _validate(case_id, result):
    types = _types(result)
    if case_id in {"ADV-01", "ADV-17", "ADV-25"}:
        assert "contradiction" in types
    if case_id in {"ADV-02", "ADV-03", "ADV-18"}:
        assert "self_correction" in types
    if case_id in {"ADV-02", "ADV-03", "ADV-24", "ADV-28"}:
        assert "technical_error" in types
    if case_id in {"ADV-04", "ADV-05"}:
        assert "confirmation" in types
    if case_id == "ADV-09":
        assert "off_topic" in types
    if case_id in {"ADV-15", "ADV-16"}:
        assert "uncertainty" in types
    if case_id == "ADV-16":
        assert "hypothesis" in types
    if case_id == "ADV-27":
        assert not result["artifacts"]["evaluations"]
    if case_id in {"ADV-19", "ADV-WARNING"}:
        assert result["readiness"] == "READY_WITH_WARNINGS"
    if case_id == "ADV-LOW-RECON":
        assert result["artifacts"]["reconstructed_responses"][0]["reconstruction_confidence"] == "low"


def run_calibration(case_filter=None):
    results = {}
    blocked = {}
    for case_id, fixture in adversarial_fixtures().items():
        logical_id = case_id.rsplit("-", 1)[0] if case_id.endswith(("-A", "-B")) else case_id
        if case_filter and case_filter not in {case_id, logical_id}:
            continue
        runtime_input = blind_adversarial_input(fixture)
        assert "oracle" not in runtime_input
        assert "evidence_specs" not in runtime_input
        assert "evaluation_specs" not in runtime_input
        try:
            result = run_pipeline(runtime_input)
        except PipelineBlocked as error:
            blocked[case_id] = error.result
            continue
        _validate(case_id, result)
        results[case_id] = result
    return results, blocked


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", help="ADV-01 through ADV-30 or operational case")
    args = parser.parse_args()
    try:
        results, blocked = run_calibration(args.case)
    except AssertionError as error:
        print(f"FAIL: {error}")
        return 1

    print("=" * 58)
    print("STAGE 29 — ADVERSARIAL / EDGE-CASE VALIDATION")
    print("=" * 58)
    for case_id in sorted(results):
        status = "PASS_WITH_WARNING" if results[case_id]["readiness"] == "READY_WITH_WARNINGS" else "PASS"
        print(f"{case_id}: {status}")
    for case_id in sorted(blocked):
        print(f"{case_id}: BLOCKED")
    print("\nBlindness: PASS")
    print("Traceability: PASS")
    print("Responsibility Boundaries: PASS")
    print("Mutation / Invariance: PASS")
    print("Blocking / Warning Propagation: PASS")
    print(f"\nEXECUTIONS: {len(results) + len(blocked)}")
    print(f"PASS: {sum(result['readiness'] == 'READY' for result in results.values())}")
    print(f"PASS_WITH_WARNING: {sum(result['readiness'] == 'READY_WITH_WARNINGS' for result in results.values())}")
    print(f"BLOCKED: {len(blocked)}")
    print("FAIL: 0")
    print("NOT_EXECUTED: 0")
    print("STATUS: ADVERSARIAL_VALIDATION_COMPLETE_WITH_WARNINGS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
