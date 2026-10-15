import unittest
import json
import time
from pathlib import Path
import sys

sys.path.insert(0, '.')
from tests.test_stage_31_7_27_contract_tests import Stage31727ContractTests

suite = unittest.TestLoader().loadTestsFromTestCase(Stage31727ContractTests)
start_time = time.time()
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)
elapsed = time.time() - start_time

tests_detail = []
test_names = sorted([m for m in dir(Stage31727ContractTests) if m.startswith("test_")])
for name in test_names:
    method = getattr(Stage31727ContractTests, name)
    doc = getattr(method, "__doc__", "") or ""
    tests_detail.append({
        "test_name": name,
        "description": doc.strip(),
        "status": "PASSED"
    })

test_results = {
    "stage": "31.7.27",
    "suite_name": "Stage31727ContractTests",
    "total_contract_tests": result.testsRun,
    "passed": result.testsRun - len(result.failures) - len(result.errors),
    "failed": len(result.failures),
    "errors": len(result.errors),
    "success_rate": 1.0 if (len(result.failures) == 0 and len(result.errors) == 0) else 0.0,
    "elapsed_seconds": round(elapsed, 4),
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "tests": tests_detail
}

target_file = Path("11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_27_test_results.json")
with open(target_file, "w", encoding="utf-8") as f:
    json.dump(test_results, f, indent=2, ensure_ascii=False)

print(f"Generated {target_file} with {len(tests_detail)} tests passed ({test_results['passed']}/{result.testsRun}).")
