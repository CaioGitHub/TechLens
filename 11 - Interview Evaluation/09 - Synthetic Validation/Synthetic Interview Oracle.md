---
type: reference
status: understood
confidence: 100
created: 2026-10-04
updated: 2026-10-04
tags:
  - interview-evaluation
  - synthetic
  - oracle
---

# Synthetic Interview Oracle

The oracle is implemented independently in `tests/synthetic_interview_oracle.py`. It checks observable properties rather than reproducing the runtime's transformation logic or requiring literal rationales.

## Required properties

```yaml
roles:
  candidate: P-CANDIDATE-27
  interviewer: P-INTERVIEWER-27
  observer: P-OBSERVER-27
response_types:
  R6: self_correction
  R8: experience_declaration
  R9: demonstrated_experience
  R10: hypothetical
  R11: uncertainty
evidence:
  R5: negative
  R8: insufficient
  R9: positive
  R10: conditional
  R11: insufficient
exclusions:
  candidate_question: CQ7
  missing_question: Q4
  ambiguous_segment: RAW-26
  interviewer_intervention: RAW-06
reconstruction:
  response: R12
  original_contains: Spring Boto
  reconstructed_contains: Spring Boot
```

The oracle intentionally does not prescribe a global score, a literal rationale or a hiring conclusion.
