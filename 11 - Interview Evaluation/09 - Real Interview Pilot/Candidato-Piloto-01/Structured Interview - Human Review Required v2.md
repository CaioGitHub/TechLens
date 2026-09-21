---
type: reference
status: unresolved
confidence: 70
created: 2026-09-21
updated: 2026-09-21
tags:
  - interview-evaluation
  - real-interview-pilot
  - human-review
  - meta
---
# Stage 30 — Structured Interview — Human Review Required v2

## Pilot metadata

```yaml
pilot_id: REAL-PILOT-2026-09-14-01-v2
candidate_id: Candidato-Piloto-01
interview_date: 2026-09-14
source_scope: second user-provided transcript submission
runtime: reference_runtime
mode: read-only
```

The second submission covers `00:03–04:27` and `19:13–20:01`. The interval `04:27–19:13`, containing the remainder of the technical interview, is still absent.

## Initial run result

```yaml
status: COMPLETED
readiness: READY_WITH_WARNINGS
segments: 44
participants: 4
questions_detected: 5
responses_detected: 14
unanswered_questions: 1
unlinked_responses: 0
evaluations_materialized_by_runtime: 4
```

The runtime mechanically materialized downstream artifacts, but the Human Review Gate is mandatory. No downstream evaluation is valid for this pilot while the structure is blocked.

## Human review gate

```yaml
human_review:
  status: BLOCKED
  reviewed: false
  structural_issues:
    - transcript interval 04:27–19:13 is absent
    - the technical interview body cannot be reconstructed
  speaker_issues:
    - final label "Regina" is unresolved
  question_issues:
    - Q1 combines opening context with a conversational question
    - Q2 is a conversational confirmation incorrectly treated as a question
    - Q3 and Q4 are extracted from the available technical opening
    - Q5 is the first actual technical question, but its response is absent
  response_issues:
    - most professional-history segments were linked to Q2 because the missing interval interrupts context
    - closing acknowledgements were linked to Q5 even though they occur after the omitted technical interview
    - short confirmations such as "Yes", "Beijava" and "Is" require human interpretation
  reconstruction_issues:
    - terms such as "Beijava", "C Sharpe", "Angula", "produtos e consumes" and "4 VS/4 VR" are potentially corrupted or ambiguous
    - no normalization was applied automatically to these ambiguous terms
  linking_issues:
    - Q5 is unanswered in the supplied source
    - downstream links cannot be validated across the missing interval
  approved_for_evaluation: false
```

## P0/P1 findings

### P0 — incomplete source prevents reliable evaluation

The missing interval contains the majority of the technical interview. Any score or evidence summary would be incomplete and could misrepresent the candidate.

### P1 — conversational speech is extracted as questions

The runtime extracts opening and closing conversational statements as questions. This confirms the Stage 30 risk identified in the first run and requires a later anonymized regression fixture.

### P1 — response linking crosses semantic boundaries

Because the transcript gap is not represented as a structural boundary, the runtime groups the candidate's professional-history statements under the earlier conversational Q2 and links closing acknowledgements to Q5. This is not an acceptable structure for evaluation.

### P2 — ambiguous technical transcription

Several terms may require human review:

```text
Beijava
C Sharpe
Angula
produtos e consumes
4 VS / 4 VR
```

They must remain original until a reviewer confirms a normalization.

## Audit summaries

### Speaker audit

| Source label | Resolved role | Confidence | Review |
|---|---|---:|---|
| candidate label | candidate | high | pending |
| Michelly | interviewer | high | pending |
| Caio | interviewer | high | pending |
| Rodrigo | interviewer | high | pending |
| Regina | unknown | low/unresolved | required |

### Question audit

| ID | Source | Initial result | Review |
|---|---|---|---|
| Q1 | 00:19 | mixed introduction + conversational question | requires correction |
| Q2 | 01:32 | closing/transition statement | requires correction |
| Q3 | 03:42 | technologies used | pending |
| Q4 | 03:56 | Java version | pending |
| Q5 | 04:27 | REST “produtos e consumes” | pending; response missing |

### Response audit

The runtime produced 14 response records, including one missing response for Q4 and records that were linked to Q2/Q5 across the incomplete transcript. These links are not approved.

### Reconstruction audit

No ambiguous technical term was silently normalized. The original transcript remains the source of truth.

### Evidence and evaluation audit

Evidence and evaluations were mechanically emitted by the existing reference runtime, but they are marked **not valid for pilot conclusions** because `approved_for_evaluation: false`.

## Gate decision

```text
REAL_INTERVIEW_PILOT_COMPLETE: NOT_REACHED
STATUS: BLOCKED
```

The complete transcript is required before human review can approve the Structured Interview.

## Initial run history

| Run | Source coverage | Result |
|---|---|---|
| v1 | 00:03–01:38 and 19:13–20:01 | BLOCKED at Human Review |
| v2 | 00:03–04:27 and 19:13–20:01 | BLOCKED at Human Review |

No runtime code was changed between these runs.
