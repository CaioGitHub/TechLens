---
type: reference
status: understood
confidence: 100
created: 2026-10-04
updated: 2026-10-04
tags:
  - interview-evaluation
  - pipeline
  - synthetic
  - end-to-end
---

# Etapa 27 — Synthetic Interview Full Run

## Status

```text
SYNTHETIC_FULL_RUN_COMPLETE_WITH_WARNINGS
```

The supported raw-transcript reference adapter executed a complete synthetic interview flow. The execution validates the behavior of the reference contracts, not a production NLP parser or production semantic evaluator.

## Scenario

The scenario contains 28 synthetic transcript segments, three participants, interviewer questions, candidate answers, a follow-up, a reformulation, an interviewer intervention, a candidate question, an observer comment, an ambiguous speaker, a missing answer, a self-correction, a hypothesis, declared and demonstrated experience, a relevant technical error and an intentional transcription reconstruction.

## Supported flow

```text
Raw synthetic transcript
→ 20.1–20.7
→ Structured Interview
→ Evidence Set
→ individual evaluations
→ report handoff
```

The human-review and audit approvals are represented in the test oracle as explicit simulated conditions. The current `run_pipeline` execution does not invoke the Stage 24 orchestration approval gate; this is documented as a runtime limitation, not reported as production approval.

## Observed results

```yaml
participants: 3
segments: 28
questions: 12
responses: 13
evidence_items: 11
evaluations: 10
readiness: READY_WITH_WARNINGS
```

The warning is caused by the intentionally ambiguous `RAW-26` speaker. It propagates through validation, Evidence Set, evaluation and report handoff.

## Semantic cases exercised

| Case | Expected behavior |
|---|---|
| correct troubleshooting reasoning | preserve evidence and traceability |
| incomplete response | retain missing/limited state |
| technical error | preserve negative qualification and impact |
| self-correction | preserve initial and corrected statements |
| definition with limited application | separate conceptual evidence from application |
| declared experience | do not upgrade to demonstrated experience |
| demonstrated experience | preserve concrete action and outcome evidence |
| vague/uncertain answer | keep confidence and evidence limited |
| candidate question | exclude from technical evaluation |
| interviewer intervention | do not attribute to candidate |
| ambiguous speaker | preserve `unknown` and `needs_review` |
| transcription error | preserve original and controlled reconstruction |

## Audit limitation

The real Stage 23.1 semantic-audit executor is not integrated into `run_pipeline`. The test validates the audit contract through independent properties and explicitly records this limitation. No audit execution is claimed beyond the supported reference behavior.

## Safety

- no real interview was processed;
- no pilot artifact was modified;
- no real candidate report was generated;
- no external service was used;
- no hiring, seniority or job-fit decision was produced.

## Gate

```text
SYNTHETIC_FULL_RUN_COMPLETE_WITH_WARNINGS
```
