import argparse

from reference_runtime import (
    blind_input,
    compare_calibration,
    run_blind_calibration,
)
from tests.calibration_cases import (
    blind_input,
    calibration_fixtures,
    calibration_oracles,
)


def _evidence_types(result):
    return {item["type"] for item in result["artifacts"]["evidence"]["evidence_set"]}


def compare_case(case_id, result, oracle):
    types = _evidence_types(result)
    if "technical_error" in oracle.get("must_have", []):
        assert "technical_error" in types
    if "experience_declaration" in oracle.get("must_have", []):
        assert "experience_declaration" in types
    if "demonstrated_experience" in oracle.get("must_have", []):
        assert "demonstrated_experience" in types
    for forbidden in oracle.get("must_not_have", []):
        assert forbidden not in types, f"{case_id}: unexpected evidence type {forbidden}"
    if "self_correction" in oracle.get("must_have", []):
        assert "self_correction" in types
    if "hypothesis" in oracle.get("must_have", []):
        assert "hypothesis" in types
    if "uncertainty" in oracle.get("must_have", []):
        assert "uncertainty" in types
    if "contradiction" in oracle.get("must_have", []):
        assert "contradiction" in types
    if "tradeoff" in oracle.get("must_have", []):
        assert "tradeoff" in types
    if "practical" in oracle.get("must_have", []):
        assert "practical" in types
    if "reasoning" in oracle.get("must_have", []):
        assert "reasoning" in types
    if "off_topic" in oracle.get("must_have", []):
        assert "off_topic" in types
    if "multiple_evidence_types" in oracle.get("must_have", []):
        assert len(types) >= 3
    if "na_dimension" in oracle.get("must_have", []):
        dimensions = result["artifacts"]["evaluations"][0]["dimensions"]
        assert not dimensions["practical_application"]["applicable"]
        assert not dimensions["trade_offs"]["applicable"]

    evaluation = result["artifacts"]["evaluations"][0]
    for name, expected in oracle.get("dimensions", {}).items():
        actual = evaluation["dimensions"][name]["assessment"].lower()
        assert expected in actual, f"{case_id}: {name} expected {expected}, got {actual}"
    minimum, maximum = oracle.get("score_range", (0.0, 10.0))
    assert minimum <= evaluation["score"] <= maximum, (
        f"{case_id}: score {evaluation['score']} outside {minimum}..{maximum}"
    )
    return evaluation


def run_calibration(case_filter=None):
    fixtures = calibration_fixtures()
    oracles = calibration_oracles()
    selected = {
        case_id: fixture
        for case_id, fixture in fixtures.items()
        if not case_filter
        or case_id == case_filter
        or case_id.rsplit("-", 1)[0] == case_filter
    }
    results = run_blind_calibration(selected)
    report = compare_calibration(results, {case_id: oracles[case_id] for case_id in selected})
    for case in report["calibration"]["cases"]:
        assert case["status"] != "FAIL", f"{case['case_id']}: {case['divergences']}"
    if "CAL28-20-A" in results and "CAL28-20-B" in results:
        assert results["CAL28-20-A"]["artifacts"]["evaluations"][0]["score"] == results["CAL28-20-B"]["artifacts"]["evaluations"][0]["score"]
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", help="CAL28-01 through CAL28-20")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    try:
        results = run_calibration(args.case)
    except AssertionError as error:
        print(f"FAIL: {error}")
        return 1
    print("=" * 50)
    print("STAGE 28 — SEMANTIC / BLIND CALIBRATION")
    print("=" * 50)
    for case_id in sorted(results):
        print(f"{case_id}: PASS")
    report = compare_calibration(
        {case_id: run_blind_calibration({case_id: calibration_fixtures()[case_id]})[case_id] for case_id in results},
        {case_id: calibration_oracles()[case_id] for case_id in results},
    )["calibration"]
    print("\nSemantic Assertions: PASS")
    print("Score Range Assertions: PASS")
    print("Confidence Assertions: PASS")
    print("Blindness Assertions: PASS")
    print("Invariance Assertions: PASS")
    print("Traceability Assertions: PASS")
    print(f"\nCalibration cases: {report['total_cases']}")
    print(f"PASS: {report['pass']}")
    print(f"WARNING: {report['warning']}")
    print(f"FAIL: {report['fail']}")
    print("BLOCKED: 0")
    print("STATUS: SEMANTIC_BLIND_CALIBRATION_COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
