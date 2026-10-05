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
  - validation
---

# Stage 25 — End-to-End Validation

## Status

```text
END_TO_END_VALIDATION_COMPLETE_WITH_WARNINGS
```

The supported reference orchestration was executed end to end with synthetic fixtures. The real pilot was not reprocessed and no real report was persisted.

## Scope

Validated flow:

```text
Synthetic input
→ 20.1–20.7
→ Structured Interview / validation
→ explicit simulated human approval
→ Evidence Set
→ individual evaluations
→ Evaluation Engine reference output
→ global audit gate
→ report approval gate
→ in-memory final-report handoff
```

The human approval and audit approval in these tests are explicit simulated inputs. They are not automatic approvals and do not represent a production human-review system.

## Components actually integrated

| Component | Execution |
|---|---|
| 20.1–20.7 reference runtime | Integrated and executed |
| Evidence Set reference stage | Integrated and executed |
| Individual Evaluation reference stage | Integrated and executed |
| Stage 23 report handoff | Integrated and executed |
| Stage 23.1 approval gate | Integrated as orchestration input |
| Final report generation | Tested in memory only; no filesystem persistence |
| Real pilot artifacts | Not executed |

## Nominal scenario

The nominal fixture `SYN-E2E-01` traversed all supported processing stages. The completed stages were:

```text
20.1, 20.2, 20.3, 20.4, 20.5, 20.6, 20.7,
21, 22, 23, 23.1
```

The report-generation state remained `APPROVAL_REQUIRED` until explicit report approval was supplied. The produced report handoff consumed the exact individual evaluations and did not recalculate them.

## Traceability matrix

| Result | Individual evaluation | Evidence item | Response | Source segment |
|---|---|---|---|---|
| report evaluation | `EVAL-...` | `EVD-...` | `R1` / `R1.1` | `S02` / `S04` |

The automated validation additionally iterates over every produced evaluation, resolves every referenced Evidence Item and verifies every `source.segment_id` against the speaker-attributed transcript. Orphan references block the orchestration.

## Semantic invariants

The end-to-end tests verified that:

- candidate questions do not enter the Evidence Set or evaluations;
- missing responses produce no negative evidence;
- unknown question links remain unscored;
- N/A dimensions remain non-applicable with `score: None`;
- warnings remain metadata and propagate downstream;
- seniority metadata does not change evaluations;
- report handoff does not recalculate scores;
- no hiring, ranking, job-fit or seniority conclusion is created.

## Gates

| Scenario | Expected state | Result |
|---|---|---|
| no human approval | `REQUIRES_HUMAN_REVIEW` | PASS |
| validation blocker | `BLOCKED` | PASS |
| missing Evidence Set | `BLOCKED` | PASS |
| incomplete evaluation | `BLOCKED` | PASS |
| invalid Evidence reference | `BLOCKED` | PASS |
| audit pending | `APPROVAL_REQUIRED` | PASS |
| report not approved | `APPROVAL_REQUIRED` | PASS |

## Limitations

1. The executors are deterministic reference components driven by synthetic fixtures.
2. No free-form transcript parser, production Evidence Model or production semantic evaluator is exercised.
3. The Stage 23.1 audit is represented by its explicit status input; the real pilot audit artifact is not re-executed.
4. Human approval is simulated explicitly and is not inferred.
5. Report generation is tested as an in-memory artifact only.
6. The `OrchestrationStore` is in-memory and is not production persistence.

## Protected artifacts

The following real-pilot artifacts were not read as execution inputs and were not modified:

```text
Structured Interview - Controlled Correction v6.md
Evidence Set v1.md
Individual Evaluations v2.md
Interview Evaluation v1.md
Stage 23.1 — Global Evaluation Semantic Audit.md
Human Review Decisions v5.md
```

Stage 26 and later stages were not executed.

## Gate

```text
END_TO_END_VALIDATION_COMPLETE_WITH_WARNINGS
```
