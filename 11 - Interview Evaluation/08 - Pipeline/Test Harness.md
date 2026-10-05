---
type: reference
status: understood
confidence: 100
created: 2026-10-04
updated: 2026-10-04
tags:
  - interview-evaluation
  - test-harness
  - validation
---

# Etapa 26 — Test Harness

## Runner

The consolidated runner is:

```text
py -3 .\run_reference_harness.py
```

Optional machine-readable output:

```text
py -3 .\run_reference_harness.py --report .\session-harness-results.json
```

The runner executes, in order:

```text
Reference Runtime
Stage 24 orchestration
Stage 25 end-to-end validation
Full unittest suite
Synthetic Interview
Semantic Blind Calibration
Adversarial Edge Cases
Stage 30.1
```

It stops after the first non-zero suite and returns a non-zero process code. Warnings are reported separately from failures.

## Result contract

```yaml
harness_version: "26-reference-harness-1"
runtime: reference_runtime
input: synthetic fixtures only
execution_id: deterministic-content-prefix
suites: []
executed: 0
planned: 0
failed: 0
warnings: []
status: PASS
real_interview_processed: false
real_report_generated: false
simulated_approvals_only: true
```

`PASS_WITH_WARNINGS` is a successful process result with explicit limitations. `FAIL` indicates at least one suite returned a non-zero exit code.

## Isolation and cleanup

The runner does not use real interview inputs, does not write reports by default and disables Python bytecode writes in child processes. Temporary resources in tests use `TemporaryDirectory` and are removed by the owning test.

## Interruption and retry

An interrupted process is not converted into a passing report. A rerun starts a new harness execution and does not reuse mutable child-process state. Component-level idempotency and version preservation remain covered by the Stage 24 and Stage 25 suites.

## Synthetic approvals

Any human-review, audit or report approval used by fixtures is simulated through explicit test arguments. The harness never creates a real approval, processes the real pilot or authorizes production report generation.
