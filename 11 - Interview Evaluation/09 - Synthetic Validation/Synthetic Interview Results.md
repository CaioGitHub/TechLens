---
type: reference
status: understood
confidence: 100
created: 2026-10-04
updated: 2026-10-04
tags:
  - interview-evaluation
  - synthetic
  - results
---

# Synthetic Interview Results

## Matrix

| Case | Expected behavior | Observed result | Status | Evidence |
|---|---|---|---|---|
| participant roles | candidate/interviewer/observer preserved | roles matched | PASS | participant IDs |
| candidate question | excluded from technical evaluation | `CQ7` absent from questions/evaluations | PASS | oracle |
| missing answer | no evidence created | `Q4` absent from Evidence Set | PASS | `missing` response |
| ambiguous speaker | unknown + review | `RAW-26` preserved as unknown | PASS_WITH_WARNING | validation warning |
| intervention | not candidate evidence | `RAW-06` absent from response sources | PASS | source segments |
| self-correction | both statements preserved | `R6` retained | PASS | reconstructed response |
| hypothesis | not demonstrated experience | `R10` remains hypothetical | PASS | response/evidence |
| declared experience | not upgraded | `R8` remains declaration | PASS | evidence type |
| demonstrated experience | concrete evidence preserved | `R9` positive | PASS | evidence item |
| technical error | negative qualification retained | `R5` negative | PASS | evidence item |
| transcription error | original + reconstruction | `Spring Boto` → `Spring Boot` | PASS | `R12` |
| traceability | evaluation→evidence→source | all references resolve | PASS | independent oracle |
| numeric summary | derive from observed scores | 10 evaluations validated | PASS | runtime output |
| global audit execution | integrated semantic auditor | not available in runtime | NOT_TESTED | limitation |
| real report persistence | no real file | no persistence performed | PASS | safety boundary |

## Gate

```text
SYNTHETIC_FULL_RUN_COMPLETE_WITH_WARNINGS
```

## Regression results

```yaml
stage_27_tests: 13/13
stage_24_to_26_tests: 30/30
full_unittest: 277/277
reference_harness: 8/8 suites, 0 failures
synthetic_runner: 81 PASS, 1 PASS_WITH_WARNING
semantic_calibration: PASS
adversarial_validation: 29 PASS, 4 PASS_WITH_WARNING, 1 expected BLOCKED
stage_30_1: 6/6
git_diff_check: PASS
```

The global semantic-audit executor remains `NOT_TESTED` in this scenario because it is not integrated into the raw-transcript reference runner.
