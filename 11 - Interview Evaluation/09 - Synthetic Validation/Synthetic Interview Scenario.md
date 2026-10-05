---
type: reference
status: understood
confidence: 100
created: 2026-10-04
updated: 2026-10-04
tags:
  - interview-evaluation
  - synthetic
  - validation
---

# Synthetic Interview Scenario

## Identity

```yaml
fixture_id: SYN-STAGE27-01
source: tests/synthetic_interview.py
real_interview: false
candidate: synthetic-only
```

## Coverage

The scenario uses Java 21, observability, architecture and troubleshooting themes. It includes basic, intermediate and advanced prompts, although the reference adapter supplies controlled evaluation specifications rather than deriving semantic scores from free-form text.

The scenario intentionally includes:

- strong and partial answers;
- a technical error;
- a vague/uncertain answer;
- conceptual evidence with limited application;
- practical evidence with a trade-off;
- follow-up and reformulation;
- a candidate question;
- an interviewer intervention;
- an observer statement;
- an ambiguous speaker;
- a missing response;
- a transcription error with controlled reconstruction.

## Expected boundaries

The scenario must never:

- turn the candidate question into a technical question;
- attribute interviewer or observer text to the candidate;
- turn missing or unknown material into negative evidence;
- turn declared experience into demonstrated experience;
- create a real report or decision.
