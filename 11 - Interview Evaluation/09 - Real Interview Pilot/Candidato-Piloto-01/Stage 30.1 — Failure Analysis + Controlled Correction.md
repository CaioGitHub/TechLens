---
type: reference
status: unresolved
confidence: 85
created: 2026-09-21
updated: 2026-09-21
tags:
  - interview-evaluation
  - real-interview-pilot
  - failure-analysis
  - controlled-correction
  - meta
---
# Stage 30.1 — Failure Analysis + Controlled Correction

## 1. Objective

Analyze the initial real-interview pilot failure modes, implement only generic corrections in the transcription-processing reference runtime, add anonymized regressions, rerun Stages 26–29, and reprocess the real transcript without treating the result as a valid technical evaluation.

## 2. Initial state

The preserved initial run is:

```text
Stage 30 — v3 Initial Run
Runtime readiness: READY
Human Review: BLOCKED
```

The complete source is preserved in:

```text
Pilot Input - Source Transcript v3.md
```

The initial structural review is preserved in:

```text
Structured Interview - Human Review Required v3.md
```

## 3. Failure inventory

| ID | Category | Stage | Severity | Root cause | Correction |
|---|---|---|---|---|---|
| FA-30.1-001 | question_extraction / gate | 20.3/20.7 | P1 | punctuation and broad indirect-prefix heuristics treated conversational speech as evaluable questions | explicit question-kind classification and validation warnings |
| FA-30.1-002 | interviewer_intervention / evidence_boundary | 20.3/21 | P0 | interviewer comments were not represented as evaluation-ineligible structural units | preserve interventions with `evaluation_eligible: false`; exclude from question/evidence flow |
| FA-30.1-003 | response_extraction / linking | 20.4/20.6 | P1 | the last question remained active across substantive interviewer context | close response context after substantive intervention following a candidate response |
| FA-30.1-004 | candidate_intervention | 20.3/21 | P1 | candidate questions were detected inconsistently and could contaminate response context | stable candidate-question classification, preservation and exclusion from evaluation |
| FA-30.1-005 | question_extraction | 20.3 | P1 | indirect prompts without terminal punctuation were not consistently recognized | generic indirect-question markers for experience, usage and scenario prompts |
| FA-30.1-006 | question_response_linking | 20.6 | P0 | responses were forced to the last known question even when context changed | unknown links and review warnings instead of forced association |
| FA-30.1-007 | reconstruction | 20.5 | P2 | a specific corrupted term was hardcoded in the runtime | remove candidate-specific fallback normalization; preserve original unless upstream contract supplies reconstruction |
| FA-30.1-008 | validation | 20.7 | P1 | mechanical validation checked fields and source IDs but not structural uncertainty classes | warnings for candidate questions, conversational prompts, unknown links and review-required responses |

## 4. Corrections implemented

### C30.1-001

**Problem:** conversational prompts and comments became questions.

**Change:** added generic question-kind classification and excluded conversational prompts from extracted evaluation questions while preserving source segments.

**Regression:** `test_conversational_prompt_is_preserved_but_not_extracted`.

### C30.1-002

**Problem:** interviewer explanations could continue the previous response context.

**Change:** interviewer interventions are evaluation-ineligible; substantive interventions after a candidate response close the active link.

**Regression:** `test_interviewer_explanation_is_not_a_question_or_candidate_evidence` and `test_substantive_interviewer_intervention_closes_previous_response`.

### C30.1-003

**Problem:** candidate questions were not consistently separated.

**Change:** candidate questions receive `CQn`, `question_kind: candidate_question`, and `evaluation_eligible: false`; they remain available in the structured artifact.

**Regression:** `test_candidate_question_is_preserved_and_does_not_contaminate_linking`.

### C30.1-004

**Problem:** ambiguous terms could be silently normalized by a real-term fallback.

**Change:** removed hardcoded fallback normalization. Explicit reconstruction metadata remains supported and preserves `original_text`.

**Regression:** `test_ambiguous_term_is_not_silently_normalized`; existing explicit reconstruction tests remain green.

### C30.1-005

**Problem:** validation returned `READY` despite structural uncertainty.

**Change:** `20.7` now emits warnings for candidate questions, conversational prompts, unknown links and review-required responses.

**Regression:** Stage 30.1 suite plus existing Stage 26–29 suites.

All corrections are generic and candidate-specific: `false`.

## 5. Regression tests

Added:

```text
tests/test_stage_30_1.py
```

Coverage:

- conversational prompt;
- interviewer explanation;
- candidate question;
- semantic response boundary;
- ambiguous term preservation;
- idempotency.

The real transcript was not added to automated fixtures.

## 6. Regression results

```text
Stage 26: PASS
Stage 27: PASS
Stage 28: PASS
Stage 29: PASS
Stage 30.1: PASS
Full suite: 183/183 PASS
```

The full suite count increased from 177 to 183 because six Stage 30.1 regression tests were added.

## 7. Initial Run vs Corrected Run

| Item | Initial v3 | Corrected v4 | Result |
|---|---:|---:|---|
| Participants | 4 | 4 | preserved |
| Segments | 164 | 164 | preserved |
| Evaluation questions | 21 | 12 | conversational/invalid units reduced |
| Candidate questions | not separated | 5 | now preserved separately |
| Responses | 44 | 47 | source segments remain represented |
| Unanswered | 5 | 0 | no response records lost; links are now explicit |
| Unlinked/unknown | 0 | 24 | safer than forced links; review required |
| Needs review | not adequately surfaced | 13 segments plus response warnings | improved visibility |
| Reconstruction warnings | not surfaced reliably | 0 automatic normalizations | no silent correction |
| Linking warnings | not surfaced | explicit warning | improved gate signal |
| Validation | READY | READY_WITH_WARNINGS | more conservative |
| Human Review | BLOCKED | BLOCKED | correctly remains mandatory |
| Evaluations materialized | 16 | 12 | fewer invalid units |

The corrected run is not considered better solely because counts changed. The semantic improvements are:

- candidate questions are no longer evaluation questions;
- conversational prompts are preserved as non-evaluable interventions;
- interviewer interventions are not candidate evidence;
- unknown links replace forced links;
- original ambiguous terms are preserved;
- downstream materialization is reduced to the remaining machine question units.

## 8. Traceability

The runtime continues to preserve:

```text
participant_id
↓
speaker_id
↓
segment_id
↓
question_id / candidate_question_id
↓
response_id
↓
evidence_id
↓
evaluation.id
↓
report handoff
```

Original and reconstructed text remain separate. Reconstruction, linking, evidence and evaluation confidence remain independent fields.

## 9. Idempotency

The Stage 30.1 idempotency regression passed for questions, responses and validation artifacts. Reprocessing the same input does not duplicate structural units or change stable IDs.

## 10. Stale / reprocessing

Existing reprocessing and stale-detection tests passed. The corrected pipeline version is distinct from the initial pilot version, so initial downstream artifacts must not be treated as valid for v4.

## 11. Remaining issues

1. The runtime still cannot fully determine the semantic boundary of every real conversational block.
2. Twenty-four response records remain without a confident question link and require human review.
3. Candidate questions are preserved but require final classification as organizational, technical or non-evaluable.
4. Corrupted technical terms remain unresolved where context is not unequivocal.
5. The runtime readiness state is improved to `READY_WITH_WARNINGS`, but human approval remains a separate mandatory gate.

## 12. Human Review

```yaml
required: true
status: BLOCKED
approved_for_evaluation: false
```

No Evidence Model or Evaluation Engine result from this pilot is valid until the Structured Interview is reviewed and approved.

## 13. Limitations

- This is a deterministic reference runtime, not a production NLP/LLM parser.
- The real transcript was used only for pilot reprocessing, not as an automated fixture.
- The correction does not infer technical correctness or candidate quality.
- The correction does not produce hiring decisions, rankings or seniority conclusions.
- The correction does not alter Rubric, Evidence Model or Evaluation Engine contracts.

## 14. Gate

```text
REAL_INTERVIEW_FAILURE_ANALYSIS_COMPLETE
STATUS: READY_WITH_WARNINGS
```

The failure analysis and controlled corrections are complete, all regression suites pass, and the corrected pilot can proceed to human review. The interview itself remains blocked for downstream evaluation until that review is explicitly approved.
