import sys
from pathlib import Path

sys.path.insert(0, '.')
from reference_runtime import runtime
from scratch.test_contract_definitions import CONTRACT_TEST_CASES

passed = 0
results = []
for tc in CONTRACT_TEST_CASES:
    res = runtime.evaluate_open_domain_semantic_relevance(tc['question'], tc['response'])
    cls = res['classification']
    ok = (cls == tc['expected'])
    if ok:
        passed += 1
    status = 'OK' if ok else 'FAIL'
    results.append({
        "id": tc['id'],
        "predicted": cls,
        "expected": tc['expected'],
        "status": status,
        "rationale": res.get("rationale", "")
    })
    print(f"{tc['id']}: pred={cls} exp={tc['expected']} -> {status}")

print(f"\nFinal: {passed}/{len(CONTRACT_TEST_CASES)} PASSED")
if passed != len(CONTRACT_TEST_CASES):
    sys.exit(1)
