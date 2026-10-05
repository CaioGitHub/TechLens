---
type: reference
status: understood
confidence: 100
created: 2026-10-04
updated: 2026-10-04
tags:
  - interview-evaluation
  - pipeline
  - end-to-end
  - test-results
---

# Stage 25 — End-to-End Test Results

## Specific test suite

```text
py -3 -m unittest tests.test_stage_25_end_to_end -v
11/11 PASS
```

Covered behaviors:

1. nominal integrated flow;
2. human-review gate;
3. validation block;
4. missing required artifact;
5. incomplete evaluation;
6. intermediate runtime failure;
7. warning propagation;
8. idempotent resume;
9. input-change invalidation;
10. version preservation;
11. invalid Evidence reference;
12. semantic exclusions and N/A;
13. numerical consistency from produced evaluations;
14. global-audit approval gate;
15. explicit report approval;
16. end-to-end source traceability.

## Regression results

| Validation | Result |
|---|---|
| Stage 25 tests | 11/11 PASS |
| Stage 24 tests | PASS |
| Full unittest suite | 256/256 PASS |
| Reference runtime | PASS |
| Synthetic interview | 81 PASS, 1 PASS_WITH_WARNING |
| Semantic blind calibration | PASS |
| Adversarial cases | 29 PASS, 4 PASS_WITH_WARNING, 1 expected BLOCKED |
| Stage 30.1 | 6/6 PASS |
| `git diff --check` | PASS |

## Numeric validation

The nominal scenario produced two evaluations with scores `8.0` and `8.5`. The test recalculated:

```yaml
count: 2
sum: 16.5
median: 8.25
minimum: 8.0
maximum: 8.5
```

The values were derived from the runtime output rather than copied from a fixed report.

## Failure and warning scenarios

All negative scenarios produced non-success states and identifiable blockers. Downstream artifacts were absent or marked incomplete when their prerequisites were unavailable. Warning scenarios retained warnings in the global pipeline and evaluation metadata without changing candidate evidence qualification.

## Real-pilot compatibility

No real-pilot processing, report persistence, score recalculation or artifact mutation occurred. The validation only exercised synthetic fixtures and the Stage 24 reference orchestration.

## Gate

```text
END_TO_END_VALIDATION_COMPLETE_WITH_WARNINGS
```
