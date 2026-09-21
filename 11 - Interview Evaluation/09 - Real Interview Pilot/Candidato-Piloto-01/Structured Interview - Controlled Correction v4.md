---
type: reference
status: unresolved
confidence: 75
created: 2026-09-21
updated: 2026-09-21
tags:
  - interview-evaluation
  - real-interview-pilot
  - controlled-correction
  - human-review
  - meta
---
# Stage 30 — Structured Interview — Controlled Correction v4

## Run metadata

```yaml
pilot_id: REAL-PILOT-2026-09-14-01-v4
source_version: REAL-PILOT-2026-09-14-01-v3
runtime: reference_runtime
pipeline_version: 30.1-reference-1
mode: read-only
blind_first_run: true
human_review:
  status: BLOCKED
  reviewed: false
  approved_for_evaluation: false
```

The original v3 source and initial v3 human-review artifact remain unchanged. This document records the controlled re-run after generic transcription-processing corrections.

## Corrected run result

```yaml
status: COMPLETED
readiness: READY_WITH_WARNINGS
segments: 164
participants: 4
questions_detected: 12
candidate_questions: 5
responses_detected: 47
unanswered_questions: 0
unlinked_responses: 24
segments_needing_review: 13
reconstruction_warnings: 0
evaluations_materialized_by_runtime: 12
```

The corrected run is structurally improved but is not approved for Evidence Model or Evaluation Engine conclusions. The 24 responses without a confident link are intentionally preserved as `unknown`/review-required rather than forcibly assigned.

## Corrections applied

### C30.1-001 — explicit question-kind classification

The raw adapter now distinguishes:

```text
interviewer_question
candidate_question
conversational_prompt
intervention
response
```

Candidate questions remain in the structured transcript but are excluded from evaluation questions and Evidence Model input.

### C30.1-002 — semantic response boundary

Substantive interviewer interventions after a candidate response close the previous response context. Subsequent candidate speech is not automatically attached to the earlier question.

### C30.1-003 — indirect question recognition

Generic indirect-question markers are recognized for experience, usage and scenario prompts, including formulations such as `queria entender`, `já chegou a usar`, `saberia também`, `trabalha com o que`, `vem utilizando` and `teria algum`.

### C30.1-004 — no hardcoded real-term normalization

The runtime no longer silently normalizes a specific corrupted technology name. Reconstruction is applied only when supplied through an explicit upstream reconstruction contract; otherwise original and reconstructed text remain equal.

### C30.1-005 — validation warnings for structural uncertainty

Validation now reports:

```text
candidate questions preserved outside evaluation questions
conversational prompts require classification review
responses without a confident question link require review
response extraction requires review
```

These warnings do not represent candidate performance and do not automatically become negative evidence.

## Human review gate

```yaml
human_review:
  status: BLOCKED
  reviewed: false
  structural_issues:
    - 24 response records remain without a confident question link
    - candidate questions are preserved separately but still require semantic review
    - question extraction still includes some contextual/organizational prompts
    - machine-generated evaluations are not valid before approval
  speaker_issues:
    - participant labels are stable; short acknowledgements remain context-sensitive
  question_issues:
    - technical, experience and organizational prompts need final human classification
  response_issues:
    - unknown links are safer than forced links but require review
  reconstruction_issues:
    - ambiguous technical terms remain unnormalized
  linking_issues:
    - linking confidence is insufficient for a subset of responses
  approved_for_evaluation: false
```

## Gate

```text
REAL_INTERVIEW_PILOT_COMPLETE: NOT_REACHED
STATUS: BLOCKED
```

The corrected runtime is ready for human review of the Structured Interview, but the interview is not cleared for valid downstream evaluation.
